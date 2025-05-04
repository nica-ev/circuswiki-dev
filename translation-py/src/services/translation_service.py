# translation-py/src/services/translation_service.py
import logging
import httpx
import time # Import time for sleep
from typing import List, Dict, Optional, Any, Tuple
import random

# Adjust the import path based on your project structure
try:
    # Assuming running from the root of the translation-py subproject
    from src.config_loader import ConfigLoader
except ImportError:
    # Fallback if running from workspace root or structure differs
    from translation_py.src.config_loader import ConfigLoader

class TranslationConfigError(ValueError):
    """Custom exception for translation service configuration errors."""
    pass

# --- Custom Translation Exceptions ---
class TranslationError(Exception):
    """Base exception for translation service errors during API calls."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class TranslationAuthError(TranslationError):
    """Raised for authentication errors (401, 403)."""
    pass

class TranslationRateLimitError(TranslationError):
    """Raised for rate limit errors (429)."""
    def __init__(self, message, retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after

class TranslationAPIError(TranslationError):
    """Raised for other 4xx/5xx API errors."""
    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class TranslationNetworkError(TranslationError):
    """Raised for network connectivity issues."""
    pass
# --- End Custom Exceptions ---

class TranslationService:
    """Handles interaction with the configured translation API provider."""

    def __init__(self, config_loader: ConfigLoader):
        """Initializes the TranslationService.

        Args:
            config_loader: An instance of ConfigLoader containing application settings.

        Raises:
            TypeError: If config_loader is not an instance of ConfigLoader.
            TranslationConfigError: If essential configuration is missing or invalid.
        """
        if not isinstance(config_loader, ConfigLoader):
            raise TypeError("config_loader must be an instance of ConfigLoader")

        self.logger = logging.getLogger(__name__)
        self.config_loader = config_loader
        self._http_client: Optional[httpx.Client] = None

        # Load configuration values during initialization
        self.api_provider = self.config_loader.get_setting('API_PROVIDER')
        if not self.api_provider:
            raise ValueError("API_PROVIDER not specified in configuration")

        env_key_name = f"{self.api_provider.upper()}_API_KEY"
        self.api_key = self.config_loader.get_env_var(env_key_name)
        if not self.api_key:
            self.logger.warning(f"Missing API key for {self.api_provider}. Set {env_key_name} environment variable.")
            # Allow initialization without key, but raise error on API call if needed

        self.target_languages = self.config_loader.get_setting('TARGET_LANGUAGES_LIST', [])
        if not self.target_languages:
            raise ValueError("TARGET_LANGUAGES_LIST must be a non-empty list")

        self.request_timeout = self.config_loader.get_setting('API_REQUEST_TIMEOUT', 30)
        self.retry_max_attempts = self.config_loader.get_setting('RETRY_MAX_ATTEMPTS', 3)
        self.retry_backoff_factor = self.config_loader.get_setting('RETRY_BACKOFF_FACTOR', 1.5)
        self.retry_status_codes = self.config_loader.get_setting('RETRY_STATUS_CODES', [429, 500, 502, 503, 504])
        self.batch_size = self.config_loader.get_setting('BATCH_SIZE', 50)
        self.test_mode = self.config_loader.get_setting('TEST_MODE_BOOL', False) # Load test mode flag

        # Provider specific URLs (could be moved to config or provider classes later)
        self.api_urls = {
            'DeepL': "https://api-free.deepl.com/v2/translate" # Example, use correct endpoint
            # Add URLs for other providers
        }
        self.api_url = self.api_urls.get(self.api_provider)
        if not self.api_url:
            raise ValueError(f"API URL not configured for provider: {self.api_provider}")

        self.logger.info(f"TranslationService initialized with {self.api_provider} provider")
        if self.test_mode:
            self.logger.info("TranslationService is running in TEST MODE. No actual API calls will be made.")
        self.logger.debug(f"Supported target languages: {', '.join(self.target_languages)}")

    def _initialize_http_client(self):
        """Initialize the httpx client if it doesn't exist."""
        if self._http_client is None:
            self._http_client = httpx.Client(timeout=self.request_timeout)

    def _validate_target_language(self, target_language: str):
        """Check if the target language is supported."""
        if target_language not in self.target_languages:
            raise ValueError(f"Target language '{target_language}' is not supported. Supported: {self.target_languages}")

    def _is_test_mode_enabled(self) -> bool:
        """Check if the service is running in test mode."""
        return self.test_mode

    def _make_api_call_with_retry(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> httpx.Response:
        """Make an API call with retry logic."""
        self._initialize_http_client()

        # Check for API key just before making the call (unless in test mode)
        if not self.api_key and not self._is_test_mode_enabled():
            env_key_name = f"{self.api_provider.upper()}_API_KEY"
            raise TranslationAuthError(f"API key for {self.api_provider} ({env_key_name}) is missing.")

        headers = {'Authorization': f'DeepL-Auth-Key {self.api_key}'} # Example for DeepL

        for attempt in range(self.retry_max_attempts):
            try:
                self.logger.debug(f"Attempt {attempt + 1}/{self.retry_max_attempts}: Calling {method} {endpoint}")
                response = self._http_client.request(method, self.api_url + endpoint, headers=headers, data=payload) # Assuming base URL handles provider
                response.raise_for_status() # Raise HTTPStatusError for 4xx/5xx
                return response
            except httpx.TimeoutException as e:
                error = TranslationNetworkError(f"Request timed out: {e}")
                if attempt == self.retry_max_attempts - 1:
                    self.logger.error(f"API call timed out after {self.retry_max_attempts} attempts.")
                    raise error
            except httpx.RequestError as e:
                error = TranslationNetworkError(f"Network error: {e}")
                if attempt == self.retry_max_attempts - 1:
                    self.logger.error(f"API call failed after {self.retry_max_attempts} attempts due to network error.")
                    raise error
            except httpx.HTTPStatusError as e:
                error = self._handle_http_error(e.response)
                if not self._is_retryable_error(error) or attempt == self.retry_max_attempts - 1:
                    self.logger.error(f"API call failed: {error} (Attempt {attempt + 1}/{self.retry_max_attempts})")
                    raise error

            # If error is retryable and attempts remain
            wait_time = self.retry_backoff_factor * (2 ** attempt) * (0.8 + 0.4 * random.random()) # Add jitter
            self.logger.warning(
                f"API call failed, retrying in {wait_time:.2f} seconds...",
                extra={
                    "attempt": attempt + 1,
                    "max_attempts": self.retry_max_attempts,
                    "wait_time": wait_time,
                    "error_type": type(error).__name__,
                    "status_code": getattr(error, "status_code", None)
                }
            )
            time.sleep(wait_time)
        
        # Should not be reached if loop completes correctly, but raise generic error just in case
        raise TranslationError(f"API call failed after {self.retry_max_attempts} attempts.")

    def get_supported_languages(self) -> List[str]:
        """Returns a copy of the list of supported target languages."""
        return self.target_languages.copy()

    def is_language_supported(self, language_code: Any) -> bool:
        """Checks if a given language code is in the list of supported target languages."""
        if not isinstance(language_code, str):
             return False
        return language_code in self.target_languages

    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """Translates a single text string to the target language.

        Args:
            text: The text to translate.
            target_language: The target language code (e.g., 'DE').
            source_language: Optional source language code.

        Returns:
            The translated text.

        Raises:
            TranslationConfigError: If the target language is not supported.
            NotImplementedError: As the API call logic is not yet implemented.
            # Add other potential exceptions like API errors later
        """
        self._validate_target_language(target_language)
        self.logger.debug(f"translate_text called for target language: {target_language}, source: {source_language}")

        if self._is_test_mode_enabled():
            self.logger.info(f"[TEST MODE] Simulating translation for target language: {target_language}")
            return f"[Translated {target_language}] {text}" # Return simulated translation

        if not text:
            return ""

        # --- Prepare API Call --- 
        self._initialize_http_client()
        if not self._http_client:
             raise RuntimeError("HTTP client is not initialized. Cannot make API call.")

        # Determine API URL (consider making this configurable or provider-specific)
        # Using DeepL Free API endpoint as an example
        # TODO: Use config or provider pattern to get the correct URL
        deepl_api_url = "https://api-free.deepl.com/v2/translate"
        if self.api_provider.lower() != 'deepl':
            # Placeholder for other providers
            raise NotImplementedError(f"Translation provider '{self.api_provider}' is not yet supported.")

        headers = {
            'Authorization': f'DeepL-Auth-Key {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded' # DeepL uses form data
        }
        payload = {
            'text': text,
            'target_lang': target_language
        }
        if source_language:
            payload['source_lang'] = source_language

        # --- Execute API Call with Retry --- 
        response = self._make_api_call_with_retry('POST', deepl_api_url, payload)

        # --- Process Successful Response --- 
        # (Error handling is now inside _make_api_call_with_retry)
        try:
            response_data = response.json()
            self.logger.debug(f"Received API response data: {response_data}")

            if 'translations' in response_data and len(response_data['translations']) > 0:
                translated_text = response_data['translations'][0]['text']
                self.logger.info(f"Successfully translated text to {target_language}.")
                return translated_text
            else:
                self.logger.error("DeepL API response missing expected 'translations' data.")
                # If the API call succeeded (2xx) but data is wrong, raise a generic error
                raise TranslationError("Invalid response format received from DeepL API.")
        except ValueError as e:
            self.logger.error(f"Failed to parse successful API response JSON: {e}. Response text: {response.text[:100]}...", exc_info=True)
            raise TranslationError("Failed to parse successful API response.") from e
        except Exception as e:
             # Catch-all for unexpected issues during response processing
             self.logger.exception(f"An unexpected error occurred processing successful API response: {e}")
             raise TranslationError("Unexpected error processing API response.") from e

    def _is_retryable_error(self, error: Exception) -> bool:
        """Checks if a given exception represents a retryable condition."""
        if isinstance(error, (TranslationNetworkError, TranslationRateLimitError)):
            return True
        if isinstance(error, TranslationAPIError) and error.status_code in self.retry_status_codes:
            return True
        return False

    def _handle_http_error(self, response: httpx.Response) -> Exception:
        """Handles HTTP errors and returns a suitable exception."""
        status_code = response.status_code
        error_text = response.text
        self.logger.warning(f"API call failed with HTTP status {status_code}")
        if status_code in [401, 403]:
            return TranslationAuthError(f"Authentication failed ({status_code}): {error_text}", status_code=status_code)
        elif status_code == 429:
            return TranslationRateLimitError(f"Rate limit exceeded ({status_code}): {error_text}", retry_after=response.headers.get('Retry-After'))
        else:
            return TranslationAPIError(f"API error ({status_code}): {error_text}", status_code=status_code, response_body=error_text)

    def translate_batch(self, texts: List[str], target_language: str, source_language: Optional[str] = None) -> List[str]:
        """Translates a batch of text strings to the target language.

        Args:
            texts: A list of text strings to translate.
            target_language: The target language code.
            source_language: Optional source language code.

        Returns:
            A list of translated text strings, in the same order as the input.

        Raises:
            TranslationConfigError: If the target language is not supported.
            TranslationError: If the API response is invalid or translation count mismatches.
            Other Translation...Error exceptions from the underlying API call.
        """
        self._validate_target_language(target_language)
        self.logger.debug(f"translate_batch called for {len(texts)} items, target language: {target_language}")

        if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
            raise TypeError("Input 'texts' must be a list of strings.")

        if self._is_test_mode_enabled():
            self.logger.info(f"[TEST MODE] Simulating batch translation for {len(texts)} items to target language: {target_language}")
            return [f"[Translated {target_language}] {text}" for text in texts] # Return simulated batch translation

        if not texts:
            return []
        
        # --- Prepare API Call --- 
        self._initialize_http_client()
        if not self._http_client:
             raise RuntimeError("HTTP client is not initialized. Cannot make API call.")

        # Determine API URL (consistent with single translate)
        deepl_api_url = "https://api-free.deepl.com/v2/translate"
        if self.api_provider.lower() != 'deepl':
            raise NotImplementedError(f"Batch translation for provider '{self.api_provider}' is not yet supported.")

        headers = {
            'Authorization': f'DeepL-Auth-Key {self.api_key}',
            # Content-Type is typically set automatically by httpx for form data
        }
        # Payload as list of tuples for repeated 'text' keys
        payload_list: List[Tuple[str, str]] = [('text', text) for text in texts]
        payload_list.append(('target_lang', target_language))
        if source_language:
            payload_list.append(('source_lang', source_language))

        self.logger.debug(f"Sending batch request to {deepl_api_url}")

        # --- Execute API Call with Retry --- 
        # The retry helper handles underlying API/network errors
        response = self._make_api_call_with_retry('POST', deepl_api_url, payload_list)

        # --- Process Successful Response --- 
        try:
            response_data = response.json()
            self.logger.debug(f"Received batch API response data: {response_data}")

            if 'translations' not in response_data or not isinstance(response_data['translations'], list):
                 self.logger.error("DeepL batch API response missing or invalid 'translations' list.")
                 raise TranslationError("Invalid response format received from DeepL API (missing translations list).")

            translations = response_data['translations']
            
            if len(translations) != len(texts):
                 self.logger.error(f"API response translation count mismatch. Expected {len(texts)}, got {len(translations)}.")
                 raise TranslationError("API response translation count mismatch.")

            # Extract translated text in order
            translated_texts = [item.get('text') for item in translations]
            
            # Check if any text is missing in the response items
            if None in translated_texts:
                 self.logger.error("DeepL batch response item missing 'text' field.")
                 raise TranslationError("Invalid response format received from DeepL API (item missing text).")
                 
            self.logger.info(f"Successfully translated batch of {len(texts)} items to {target_language}.")
            # Explicitly cast to List[str] to satisfy type checker if needed, though list comprehension should produce it.
            return translated_texts # type: ignore
            
        except ValueError as e:
            self.logger.error(f"Failed to parse successful batch API response JSON: {e}. Response text: {response.text[:100]}...", exc_info=True)
            raise TranslationError("Failed to parse successful API response.") from e
        except Exception as e:
             # Catch-all for unexpected issues during response processing
             self.logger.exception(f"An unexpected error occurred processing successful batch API response: {e}")
             raise TranslationError("Unexpected error processing API response.") from e

    def close(self):
        """Closes any open resources, like the HTTP client."""
        self.logger.info("Closing HTTP client...")
        if self._http_client:
            try:
                self._http_client.close()
                self.logger.info("HTTP client closed.")
            except Exception as e:
                self.logger.error(f"Error closing HTTP client: {e}")
        self._http_client = None 