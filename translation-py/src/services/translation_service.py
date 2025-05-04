# translation-py/src/services/translation_service.py
import logging
import httpx
import time # Import time for sleep
from typing import List, Dict, Optional, Any, Tuple

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
    pass

class TranslationAPIError(TranslationError):
    """Raised for other 4xx/5xx API errors."""
    pass

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
        self.test_mode = self.config_loader.settings.get('TEST_MODE_BOOL', False)

        # --- Load API Provider --- 
        self.api_provider = self.config_loader.settings.get('API_PROVIDER')
        if not self.api_provider:
            raise TranslationConfigError("API_PROVIDER not specified or invalid in configuration.")
        self.logger.info(f"Initializing TranslationService with provider: {self.api_provider}")

        # --- Load API Key (unless in test mode) ---
        self.api_key: Optional[str] = None
        if not self.test_mode:
            # Construct the expected environment variable name (e.g., DEEPL_API_KEY)
            env_key_name = f"{self.api_provider.upper()}_API_KEY"
            self.api_key = self.config_loader.env_vars.get(env_key_name)
            if not self.api_key:
                raise TranslationConfigError(f"Missing API key for provider '{self.api_provider}'. "
                                           f"Set the {env_key_name} environment variable or ensure it's in the .env file.")
            self.logger.debug(f"API key loaded for {self.api_provider}.")
        else:
            self.logger.info("TranslationService running in TEST MODE. API calls will be simulated.")

        # --- Load Target Languages ---
        self.target_languages: List[str] = self.config_loader.settings.get('TARGET_LANGUAGES_LIST', [])
        if not self.target_languages or not isinstance(self.target_languages, list) or len(self.target_languages) == 0:
            raise TranslationConfigError("TARGET_LANGUAGES_LIST must be a non-empty list in configuration.")
        self.logger.debug(f"Supported target languages: {self.target_languages}")

        # --- Load Retry Configuration --- 
        self.retry_max_attempts = self.config_loader.settings.get('RETRY_MAX_ATTEMPTS', 3)
        self.retry_backoff_factor = self.config_loader.settings.get('RETRY_BACKOFF_FACTOR', 0.5)
        self.retry_status_codes = self.config_loader.settings.get('RETRY_STATUS_CODES', [429, 500, 502, 503, 504])
        self.logger.debug(f"Retry config: Max Attempts={self.retry_max_attempts}, Backoff={self.retry_backoff_factor}, Codes={self.retry_status_codes}")

        # Placeholder for HTTP client (e.g., httpx.Client)
        self._http_client: Optional[httpx.Client] = None # Initialize with type hint

        self.logger.info("TranslationService initialized successfully.")

    def _initialize_http_client(self):
        """Initializes the HTTP client if not already done."""
        if self._http_client is None and not self.test_mode:
            self.logger.debug("Initializing HTTPX client...")
            try:
                # Set default timeout, can be made configurable later
                self._http_client = httpx.Client(timeout=30.0)
                self.logger.info("HTTPX client initialized.")
            except Exception as e:
                self.logger.exception("Failed to initialize HTTPX client")
                # Decide if this should raise an error or just log
                # For now, let it proceed, subsequent calls will fail if client is None

    def get_supported_languages(self) -> List[str]:
        """Returns a copy of the list of supported target languages."""
        return self.target_languages.copy()

    def is_language_supported(self, language_code: Any) -> bool:
        """Checks if a given language code is in the list of supported target languages."""
        if not isinstance(language_code, str):
             return False
        return language_code in self.target_languages

    def _validate_target_language(self, target_language: str):
        """Raises an error if the target language is not supported."""
        if not self.is_language_supported(target_language):
             self.logger.error(f"Attempted translation to unsupported language: {target_language}")
             raise TranslationConfigError(f"Target language '{target_language}' is not supported.")

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

        if self.test_mode:
            self.logger.info(f"[TEST MODE] Simulating translation for text: '{text[:50]}...'")
            return f"[Translated {target_language}] {text}" # Simulate translation

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
        response = self._make_api_call_with_retry(deepl_api_url, headers, payload)

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

    def _make_api_call_with_retry(self, url: str, headers: Dict, payload: Dict) -> httpx.Response:
        """Makes the API POST request with exponential backoff retry logic."""
        last_exception: Optional[Exception] = None

        for attempt in range(self.retry_max_attempts):
            self.logger.debug(f"Attempt {attempt+1}/{self.retry_max_attempts} to call {url}")
            try:
                if not self._http_client:
                    raise RuntimeError("HTTP client became unavailable during retries.")
                
                response = self._http_client.post(url, headers=headers, data=payload)
                response.raise_for_status() # Check for 4xx/5xx errors
                # --- Success --- 
                self.logger.debug(f"API call successful on attempt {attempt+1}")
                return response

            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                error_text = e.response.text
                self.logger.warning(f"API call attempt {attempt+1} failed with HTTP status {status_code}")
                last_exception = e # Store the exception
                if status_code in [401, 403]:
                    error_to_check = TranslationAuthError(f"Authentication failed ({status_code}): {error_text}", status_code=status_code) 
                elif status_code == 429:
                    error_to_check = TranslationRateLimitError(f"Rate limit exceeded ({status_code}): {error_text}", status_code=status_code)
                else:
                    error_to_check = TranslationAPIError(f"API error ({status_code}): {error_text}", status_code=status_code)
            
            except httpx.RequestError as e:
                self.logger.warning(f"API call attempt {attempt+1} failed with network error: {e}")
                last_exception = e # Store the exception
                error_to_check = TranslationNetworkError(f"Network error during API call: {e}")
            
            except Exception as e:
                # Catch unexpected errors during the request itself
                self.logger.error(f"Unexpected error during API call attempt {attempt+1}: {e}", exc_info=True)
                last_exception = e
                error_to_check = TranslationError(f"Unexpected error during API call: {e}")

            # --- Retry Logic --- 
            if self._is_retryable_error(error_to_check):
                if attempt < self.retry_max_attempts - 1:
                    wait_time = self.retry_backoff_factor * (2 ** attempt)
                    # Add jitter? random.uniform(0.8, 1.2)
                    self.logger.warning(f"Retryable error detected. Retrying in {wait_time:.2f}s...")
                    try:
                        time.sleep(wait_time)
                    except KeyboardInterrupt:
                         self.logger.warning("Retry sleep interrupted by user.")
                         raise error_to_check from last_exception # Raise the caught error directly
                    continue # Go to the next attempt
                else:
                    self.logger.error(f"API call failed after {self.retry_max_attempts} attempts due to retryable error.")
                    raise error_to_check from last_exception # Raise the last caught retryable error
            else:
                # Non-retryable error occurred
                self.logger.error(f"Non-retryable error occurred on attempt {attempt+1}. Raising immediately.")
                raise error_to_check from last_exception # Raise the non-retryable error
        
        # This part should theoretically not be reached if max_attempts > 0
        # but included for safety. Raise the last exception if the loop finishes without returning/raising.
        if last_exception:
             raise TranslationError("API call failed after all retries without specific error type.") from last_exception
        else: # Should not happen if max_attempts >= 1
             raise TranslationError("API call failed unexpectedly without exceptions after retries.")

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

        if not texts:
            self.logger.warning("translate_batch called with an empty list of texts. Returning empty list.")
            return []
        
        # Simple type check for input
        if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
             raise TypeError("Input 'texts' must be a list of strings.")

        if self.test_mode:
            self.logger.info(f"[TEST MODE] Simulating batch translation for {len(texts)} items.")
            return [f"[Translated {target_language}] {text}" for text in texts]

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
        response = self._make_api_call_with_retry(deepl_api_url, headers, payload_list)

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