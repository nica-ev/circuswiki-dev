# translation-py/src/services/translation_service.py
import logging
import httpx
from typing import List, Dict, Optional, Any

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

        # --- Actual API call logic --- 
        self._initialize_http_client()
        if not self._http_client:
             # Initialization must have failed earlier
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

        self.logger.debug(f"Sending request to {deepl_api_url} with payload: {payload}")

        try:
            response = self._http_client.post(deepl_api_url, headers=headers, data=payload)

            self.logger.debug(f"Received response status: {response.status_code}")
            # Raise HTTP errors for 4xx/5xx responses
            response.raise_for_status() # Raises httpx.HTTPStatusError for bad responses

            # Parse successful response
            response_data = response.json()
            self.logger.debug(f"Received API response data: {response_data}")

            if 'translations' in response_data and len(response_data['translations']) > 0:
                translated_text = response_data['translations'][0]['text']
                self.logger.info(f"Successfully translated text to {target_language}.")
                return translated_text
            else:
                self.logger.error("DeepL API response missing expected 'translations' data.")
                raise RuntimeError("Invalid response format received from DeepL API.")

        except httpx.HTTPStatusError as e:
            self.logger.error(f"DeepL API HTTP Error: {e.response.status_code} - {e.response.text}", exc_info=True)
            # Re-raise as a runtime error for now, refine in subtask 8.3
            raise RuntimeError(f"DeepL API Error {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            self.logger.error(f"Network error during DeepL API call: {e}", exc_info=True)
            # Re-raise for now, refine in subtask 8.3/8.4
            raise # Keep original exception type for network issues
        except Exception as e:
            self.logger.exception(f"An unexpected error occurred during translation: {e}")
            raise RuntimeError("An unexpected error occurred during translation.") from e

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
            NotImplementedError: As the API call logic is not yet implemented.
             # Add other potential exceptions like API errors later
        """
        self._validate_target_language(target_language)
        self.logger.debug(f"translate_batch called for {len(texts)} items, target language: {target_language}")

        if self.test_mode:
            self.logger.info(f"[TEST MODE] Simulating batch translation for {len(texts)} items.")
            return [f"[Translated {target_language}] {text}" for text in texts]

        # --- Actual API call logic will go here in Subtask 8.5 --- 
        self._initialize_http_client()
        # TODO: Implement batch API call using self.api_provider, self.api_key, self._http_client
        raise NotImplementedError("API call logic for translate_batch is not yet implemented.")

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