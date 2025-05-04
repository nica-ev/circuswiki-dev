# translation-py/tests/services/test_translation_service.py
import pytest
import logging
import httpx # Import httpx for RequestError
import time # Import time for mocking sleep
from unittest.mock import MagicMock, patch, ANY, call

# Adjust the import path based on your project structure
try:
    # Assuming tests run from the root of the translation-py subproject
    from src.services.translation_service import (
        TranslationService, TranslationConfigError,
        TranslationError, TranslationAuthError, TranslationRateLimitError,
        TranslationAPIError, TranslationNetworkError # Import custom exceptions
    )
    from src.config_loader import ConfigLoader
except ImportError:
    # Fallback if running from workspace root or structure differs
    from translation_py.src.services.translation_service import (
        TranslationService, TranslationConfigError,
        TranslationError, TranslationAuthError, TranslationRateLimitError,
        TranslationAPIError, TranslationNetworkError # Import custom exceptions
    )
    from translation_py.src.config_loader import ConfigLoader

# Configure logging for tests (optional, but can be helpful)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_config_loader():
    """Fixture to create a MagicMock for ConfigLoader."""
    loader = MagicMock(spec=ConfigLoader)
    # Set default attributes that ConfigLoader would have after loading
    loader.settings = {}
    loader.env_vars = {}
    # Ensure the mock has the attributes accessed in TranslationService.__init__
    loader.settings.get = MagicMock(side_effect=lambda key, default=None: loader.settings.get(key, default))
    loader.env_vars.get = MagicMock(side_effect=lambda key, default=None: loader.env_vars.get(key, default))
    
    # --- Add Default Retry Settings to Mock --- 
    loader.settings['RETRY_MAX_ATTEMPTS'] = 3
    loader.settings['RETRY_BACKOFF_FACTOR'] = 0.1 # Use small backoff for tests
    loader.settings['RETRY_STATUS_CODES'] = [429, 503]
    # --- End Retry Settings --- 
    
    return loader

def test_init_success(mock_config_loader):
    """Test successful initialization with valid DeepL config."""
    logger.debug("Running test_init_success")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE', 'FR'],
        'TEST_MODE_BOOL': False # Explicitly set test mode to False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-deepl-key'}

    service = TranslationService(mock_config_loader)
    assert service.api_provider == 'DeepL'
    assert service.api_key == 'fake-deepl-key'
    assert service.target_languages == ['DE', 'FR']
    assert isinstance(service.logger, logging.Logger)
    logger.debug("test_init_success finished")


def test_init_success_test_mode(mock_config_loader):
    """Test successful initialization in test mode (no API key needed)."""
    logger.debug("Running test_init_success_test_mode")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE', 'FR'],
        'TEST_MODE_BOOL': True  # Test mode enabled
    }
    mock_config_loader.env_vars = {} # API key not required

    service = TranslationService(mock_config_loader)
    assert service.api_provider == 'DeepL'
    assert service.api_key is None # API key should not be loaded in test mode
    assert service.target_languages == ['DE', 'FR']
    logger.debug("test_init_success_test_mode finished")

def test_init_missing_api_key(mock_config_loader):
    """Test initialization fails if API key is missing (and not in test mode)."""
    logger.debug("Running test_init_missing_api_key")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE', 'FR'],
        'TEST_MODE_BOOL': False # Test mode is off
    }
    mock_config_loader.env_vars = {} # Missing API key

    with pytest.raises(TranslationConfigError, match="Missing API key for provider 'DeepL'"):
        TranslationService(mock_config_loader)
    logger.debug("test_init_missing_api_key finished")


def test_init_empty_target_languages(mock_config_loader):
    """Test initialization fails if TARGET_LANGUAGES_LIST is empty."""
    logger.debug("Running test_init_empty_target_languages")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': [], # Empty list
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-deepl-key'}

    with pytest.raises(TranslationConfigError, match="TARGET_LANGUAGES_LIST must be a non-empty list"):
        TranslationService(mock_config_loader)
    logger.debug("test_init_empty_target_languages finished")

def test_init_missing_provider(mock_config_loader):
    """Test initialization fails if API_PROVIDER is missing."""
    logger.debug("Running test_init_missing_provider")
    mock_config_loader.settings = {
        # 'API_PROVIDER': 'DeepL', # Missing provider
        'TARGET_LANGUAGES_LIST': ['DE', 'FR'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-deepl-key'}

    with pytest.raises(TranslationConfigError, match="API_PROVIDER not specified or invalid"):
        TranslationService(mock_config_loader)
    logger.debug("test_init_missing_provider finished")

def test_init_invalid_config_loader_type():
    """Test initialization fails if config_loader is not a ConfigLoader instance."""
    logger.debug("Running test_init_invalid_config_loader_type")
    with pytest.raises(TypeError, match="config_loader must be an instance of ConfigLoader"):
        TranslationService("not a config loader") # Pass invalid type
    logger.debug("test_init_invalid_config_loader_type finished")


# --- Tests for helper methods ---

def test_get_supported_languages(mock_config_loader):
    """Test get_supported_languages returns a copy."""
    logger.debug("Running test_get_supported_languages")
    langs = ['DE', 'FR', 'ES']
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': langs,
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    supported_langs = service.get_supported_languages()
    assert supported_langs == langs
    # Check it's a copy
    supported_langs.append('IT')
    assert service.get_supported_languages() == langs
    logger.debug("test_get_supported_languages finished")

def test_is_language_supported(mock_config_loader):
    """Test is_language_supported works correctly."""
    logger.debug("Running test_is_language_supported")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE', 'FR'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    assert service.is_language_supported('DE') is True
    assert service.is_language_supported('FR') is True
    assert service.is_language_supported('ES') is False
    assert service.is_language_supported('') is False
    assert service.is_language_supported(None) is False
    assert service.is_language_supported(123) is False # Test invalid type
    logger.debug("test_is_language_supported finished")

# --- Tests for translate_text method ---

def test_translate_batch_not_implemented(mock_config_loader):
    """Test translate_batch raises NotImplementedError initially."""
    logger.debug("Running test_translate_batch_not_implemented")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    with pytest.raises(NotImplementedError):
        service.translate_batch(["Hello", "World"], "DE")
    logger.debug("test_translate_batch_not_implemented finished")

def test_translate_text_unsupported_language(mock_config_loader):
    """Test translate_text raises error for unsupported target language."""
    logger.debug("Running test_translate_text_unsupported_language")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    # Check before calling the (currently not implemented) method
    with pytest.raises(TranslationConfigError, match="Target language 'FR' is not supported."):
        service.translate_text("Hello", "FR") # FR is not in ['DE']
    logger.debug("test_translate_text_unsupported_language finished")

def test_translate_batch_unsupported_language(mock_config_loader):
    """Test translate_batch raises error for unsupported target language."""
    logger.debug("Running test_translate_batch_unsupported_language")
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    # Check before calling the (currently not implemented) method
    with pytest.raises(TranslationConfigError, match="Target language 'FR' is not supported."):
        service.translate_batch(["Hello", "World"], "FR") # FR is not in ['DE']
    logger.debug("test_translate_batch_unsupported_language finished")

@patch('httpx.Client') # Patch the Client class globally
def test_translate_text_success(mock_httpx_client_class, mock_config_loader):
    """Test translate_text success with mocked API call."""
    logger.debug("Running test_translate_text_success")
    # Configure the mock response
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {'translations': [{'detected_source_language': 'EN', 'text': 'Hallo Welt'}]}
    mock_response.raise_for_status = MagicMock() # Mock this to do nothing on success

    # Configure the mock client instance's post method
    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance # When Client() is called, return our mock instance

    # Setup service
    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    # Call the method under test
    translated_text = service.translate_text("Hello World", "DE")

    # Assertions
    assert translated_text == "Hallo Welt"
    mock_client_instance.post.assert_called_once_with(
        "https://api-free.deepl.com/v2/translate", # Or non-free URL if configured
        headers={'Authorization': 'DeepL-Auth-Key fake-key', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'text': 'Hello World', 'target_lang': 'DE'}
    )
    mock_response.raise_for_status.assert_called_once()
    logger.debug("test_translate_text_success finished")

@patch('httpx.Client')
def test_translate_text_auth_error_403(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles 403 Forbidden (Auth Error)."""
    logger.debug("Running test_translate_text_auth_error_403")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 403
    mock_response.text = "Forbidden - Invalid API Key"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message=f"Client error '{mock_response.status_code} Forbidden' for url '...'",
        request=MagicMock(),
        response=mock_response
    )

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationAuthError, match="Authentication failed \(403\): Forbidden - Invalid API Key"):
        service.translate_text("Hello World", "DE")

    mock_client_instance.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    logger.debug("test_translate_text_auth_error_403 finished")

@patch('httpx.Client')
def test_translate_text_rate_limit_error_429(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles 429 Too Many Requests (Rate Limit Error)."""
    logger.debug("Running test_translate_text_rate_limit_error_429")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 429
    mock_response.text = "Too Many Requests"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message=f"Client error '{mock_response.status_code} Too Many Requests' for url '...'",
        request=MagicMock(),
        response=mock_response
    )

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationRateLimitError, match="Rate limit exceeded \(429\): Too Many Requests"):
        service.translate_text("Hello World", "DE")

    mock_client_instance.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    logger.debug("test_translate_text_rate_limit_error_429 finished")


@patch('httpx.Client')
def test_translate_text_generic_api_error_500(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles 500 Internal Server Error (Generic API Error)."""
    logger.debug("Running test_translate_text_generic_api_error_500")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message=f"Server error '{mock_response.status_code} Internal Server Error' for url '...'",
        request=MagicMock(),
        response=mock_response
    )

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationAPIError, match="API error \(500\): Internal Server Error"):
        service.translate_text("Hello World", "DE")

    mock_client_instance.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    logger.debug("test_translate_text_generic_api_error_500 finished")


@patch('httpx.Client')
def test_translate_text_network_error(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles network errors and wraps in custom exception."""
    logger.debug("Running test_translate_text_network_error")
    mock_client_instance = MagicMock()
    network_error = httpx.RequestError("Connection refused")
    mock_client_instance.post.side_effect = network_error
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationNetworkError, match="Network error during API call: Connection refused"):
        service.translate_text("Hello World", "DE")

    mock_client_instance.post.assert_called_once()
    logger.debug("test_translate_text_network_error finished")


@patch('httpx.Client')
def test_translate_text_respects_test_mode(mock_httpx_client_class, mock_config_loader):
    """Test translate_text does not call API in test mode."""
    logger.debug("Running test_translate_text_respects_test_mode")
    mock_client_instance = MagicMock()
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': True # Test mode ON
    }
    mock_config_loader.env_vars = {} # No API key needed
    service = TranslationService(mock_config_loader)

    result = service.translate_text("Hello", "DE")

    assert result == "[Translated DE] Hello"
    # Crucially, assert the http client was NOT called
    mock_client_instance.post.assert_not_called()
    logger.debug("test_translate_text_respects_test_mode finished")

@patch('httpx.Client')
def test_translate_text_with_source_language(mock_httpx_client_class, mock_config_loader):
    """Test translate_text includes source_lang in API call when provided."""
    logger.debug("Running test_translate_text_with_source_language")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {'translations': [{'detected_source_language': 'FR', 'text': 'Hello'}]}
    mock_response.raise_for_status = MagicMock()

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['EN'],
        'TEST_MODE_BOOL': False
    }
    mock_config_loader.env_vars = {'DEEPL_API_KEY': 'fake-key'}
    service = TranslationService(mock_config_loader)

    translated_text = service.translate_text("Bonjour", "EN", source_language="FR")

    assert translated_text == "Hello"
    mock_client_instance.post.assert_called_once_with(
        ANY, # URL
        headers=ANY,
        data={'text': 'Bonjour', 'target_lang': 'EN', 'source_lang': 'FR'} # Check data payload
    )
    logger.debug("test_translate_text_with_source_language finished")

# --- Tests for Retry Logic (Subtask 8.4) ---

@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_retries_network_error(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text retries on TranslationNetworkError and eventually succeeds."""
    logger.debug("Running test_translate_text_retries_network_error")
    mock_response_success = MagicMock(spec=httpx.Response)
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {'translations': [{'text': 'Success'}]}
    mock_response_success.raise_for_status = MagicMock()

    mock_client_instance = MagicMock()
    # Fail twice with network error, then succeed
    network_error = httpx.RequestError("Connection failed")
    mock_client_instance.post.side_effect = [network_error, network_error, mock_response_success]
    mock_httpx_client_class.return_value = mock_client_instance

    # Use retry settings from mock_config_loader fixture
    service = TranslationService(mock_config_loader)

    result = service.translate_text("Test", "DE")

    assert result == "Success"
    assert mock_client_instance.post.call_count == 3
    # Check sleep calls (0.1 * 2**0, 0.1 * 2**1)
    mock_sleep.assert_has_calls([call(0.1), call(0.2)])
    assert mock_sleep.call_count == 2
    logger.debug("test_translate_text_retries_network_error finished")

@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_retries_rate_limit_error(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text retries on TranslationRateLimitError (429)."""
    logger.debug("Running test_translate_text_retries_rate_limit_error")
    mock_response_success = MagicMock(spec=httpx.Response)
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {'translations': [{'text': 'OK'}]}
    mock_response_success.raise_for_status = MagicMock()

    mock_response_fail_429 = MagicMock(spec=httpx.Response)
    mock_response_fail_429.status_code = 429
    mock_response_fail_429.text = "Rate Limited"
    mock_response_fail_429.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Too Many Requests", request=MagicMock(), response=mock_response_fail_429
    )

    mock_client_instance = MagicMock()
    # Fail once with 429, then succeed
    mock_client_instance.post.side_effect = [mock_response_fail_429, mock_response_success]
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    result = service.translate_text("Test", "DE")

    assert result == "OK"
    assert mock_client_instance.post.call_count == 2
    mock_sleep.assert_called_once_with(0.1) # 0.1 * 2**0
    logger.debug("test_translate_text_retries_rate_limit_error finished")


@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_retries_server_error_503(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text retries on TranslationAPIError with retryable status code (503)."""
    logger.debug("Running test_translate_text_retries_server_error_503")
    mock_response_success = MagicMock(spec=httpx.Response)
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {'translations': [{'text': 'OK'}]}
    mock_response_success.raise_for_status = MagicMock()

    mock_response_fail_503 = MagicMock(spec=httpx.Response)
    mock_response_fail_503.status_code = 503
    mock_response_fail_503.text = "Service Unavailable"
    mock_response_fail_503.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Service Unavailable", request=MagicMock(), response=mock_response_fail_503
    )

    mock_client_instance = MagicMock()
    # Fail once with 503, then succeed
    mock_client_instance.post.side_effect = [mock_response_fail_503, mock_response_success]
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    result = service.translate_text("Test", "DE")

    assert result == "OK"
    assert mock_client_instance.post.call_count == 2
    mock_sleep.assert_called_once_with(0.1) # 0.1 * 2**0
    logger.debug("test_translate_text_retries_server_error_503 finished")


@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_retries_fail_after_max_attempts(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text stops retrying and raises error after max attempts."""
    logger.debug("Running test_translate_text_retries_fail_after_max_attempts")
    network_error = httpx.RequestError("Connection failed")
    
    mock_client_instance = MagicMock()
    # Fail max_attempts times
    max_attempts = mock_config_loader.settings['RETRY_MAX_ATTEMPTS'] # Should be 3
    mock_client_instance.post.side_effect = [network_error] * max_attempts 
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationNetworkError, match="Network error during API call: Connection failed"):
        service.translate_text("Test", "DE")

    assert mock_client_instance.post.call_count == max_attempts
    assert mock_sleep.call_count == max_attempts - 1
    mock_sleep.assert_has_calls([call(0.1), call(0.2)]) # Sleeps for attempts 0 and 1
    logger.debug("test_translate_text_retries_fail_after_max_attempts finished")


@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_no_retry_auth_error(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text does not retry non-retryable errors like TranslationAuthError."""
    logger.debug("Running test_translate_text_no_retry_auth_error")
    mock_response_fail_403 = MagicMock(spec=httpx.Response)
    mock_response_fail_403.status_code = 403
    mock_response_fail_403.text = "Forbidden"
    mock_response_fail_403.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Forbidden", request=MagicMock(), response=mock_response_fail_403
    )

    mock_client_instance = MagicMock()
    mock_client_instance.post.side_effect = [mock_response_fail_403]
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)

    with pytest.raises(TranslationAuthError, match="Authentication failed \(403\): Forbidden"):
        service.translate_text("Test", "DE")

    assert mock_client_instance.post.call_count == 1
    mock_sleep.assert_not_called()
    logger.debug("test_translate_text_no_retry_auth_error finished")


@patch('time.sleep')
@patch('httpx.Client')
def test_translate_text_no_retry_generic_api_error_400(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_text does not retry non-retryable API errors (e.g., 400)."""
    logger.debug("Running test_translate_text_no_retry_generic_api_error_400")
    mock_response_fail_400 = MagicMock(spec=httpx.Response)
    mock_response_fail_400.status_code = 400
    mock_response_fail_400.text = "Bad Request"
    mock_response_fail_400.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Bad Request", request=MagicMock(), response=mock_response_fail_400
    )

    mock_client_instance = MagicMock()
    mock_client_instance.post.side_effect = [mock_response_fail_400]
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)

    # 400 is not in RETRY_STATUS_CODES ([429, 503]) for this test
    with pytest.raises(TranslationAPIError, match="API error \(400\): Bad Request"):
        service.translate_text("Test", "DE")

    assert mock_client_instance.post.call_count == 1
    mock_sleep.assert_not_called()
    logger.debug("test_translate_text_no_retry_generic_api_error_400 finished")


# --- End Tests for Retry Logic --- 

@patch('httpx.Client')
def test_translate_text_respects_test_mode(mock_httpx_client_class, mock_config_loader):
    """Test translate_text does not call API in test mode."""
    logger.debug("Running test_translate_text_respects_test_mode")
    mock_client_instance = MagicMock()
    mock_httpx_client_class.return_value = mock_client_instance

    mock_config_loader.settings = {
        'API_PROVIDER': 'DeepL',
        'TARGET_LANGUAGES_LIST': ['DE'],
        'TEST_MODE_BOOL': True # Test mode ON
    }
    mock_config_loader.env_vars = {} # No API key needed
    service = TranslationService(mock_config_loader)

    result = service.translate_text("Hello", "DE")

    assert result == "[Translated DE] Hello"
    # Crucially, assert the http client was NOT called
    mock_client_instance.post.assert_not_called()
    logger.debug("test_translate_text_respects_test_mode finished")

# --- Tests for translate_batch method (Subtask 8.5) ---

@patch('httpx.Client')
def test_translate_batch_success(mock_httpx_client_class, mock_config_loader):
    """Test translate_batch success with multiple texts."""
    logger.debug("Running test_translate_batch_success")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    # Simulate DeepL batch response
    mock_response.json.return_value = {
        'translations': [
            {'detected_source_language': 'EN', 'text': 'Hallo'},
            {'detected_source_language': 'EN', 'text': 'Welt'}
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    texts_to_translate = ["Hello", "World"]
    target_lang = "DE"
    
    translated_texts = service.translate_batch(texts_to_translate, target_lang)

    assert translated_texts == ["Hallo", "Welt"]
    # Check payload format (list of tuples)
    expected_payload = [
        ('text', 'Hello'), 
        ('text', 'World'), 
        ('target_lang', target_lang)
    ]
    mock_client_instance.post.assert_called_once_with(
        ANY, # URL
        headers=ANY,
        data=expected_payload
    )
    logger.debug("test_translate_batch_success finished")

def test_translate_batch_empty_input(mock_config_loader):
    """Test translate_batch returns empty list for empty input."""
    logger.debug("Running test_translate_batch_empty_input")
    service = TranslationService(mock_config_loader)
    # Patch post just to ensure it's not called
    with patch.object(service, '_http_client') as mock_client:
         result = service.translate_batch([], "DE")
         assert result == []
         mock_client.post.assert_not_called() 
    logger.debug("test_translate_batch_empty_input finished")

@patch('httpx.Client')
def test_translate_batch_respects_test_mode(mock_httpx_client_class, mock_config_loader):
    """Test translate_batch simulation in test mode."""
    logger.debug("Running test_translate_batch_respects_test_mode")
    mock_client_instance = MagicMock()
    mock_httpx_client_class.return_value = mock_client_instance

    # Enable test mode in config mock
    mock_config_loader.settings['TEST_MODE_BOOL'] = True
    service = TranslationService(mock_config_loader)
    texts = ["One", "Two"]
    target = "FR"

    result = service.translate_batch(texts, target)

    assert result == ["[Translated FR] One", "[Translated FR] Two"]
    mock_client_instance.post.assert_not_called()
    logger.debug("test_translate_batch_respects_test_mode finished")

@patch('time.sleep') # Retry logic involves sleep
@patch('httpx.Client')
def test_translate_batch_api_error(mock_httpx_client_class, mock_sleep, mock_config_loader):
    """Test translate_batch handles API errors correctly after retries."""
    logger.debug("Running test_translate_batch_api_error")
    mock_response_fail_503 = MagicMock(spec=httpx.Response)
    mock_response_fail_503.status_code = 503
    mock_response_fail_503.text = "Service Unavailable"
    mock_response_fail_503.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Service Unavailable", request=MagicMock(), response=mock_response_fail_503
    )

    mock_client_instance = MagicMock()
    # Fail max_attempts times (using settings from fixture)
    max_attempts = mock_config_loader.settings['RETRY_MAX_ATTEMPTS']
    mock_client_instance.post.side_effect = [mock_response_fail_503] * max_attempts
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    texts = ["Input1", "Input2"]

    with pytest.raises(TranslationAPIError, match="API error \(503\): Service Unavailable"):
        service.translate_batch(texts, "DE")

    assert mock_client_instance.post.call_count == max_attempts
    assert mock_sleep.call_count == max_attempts - 1
    logger.debug("test_translate_batch_api_error finished")


@patch('httpx.Client')
def test_translate_batch_response_mismatch(mock_httpx_client_class, mock_config_loader):
    """Test translate_batch raises error if response count mismatches input count."""
    logger.debug("Running test_translate_batch_response_mismatch")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    # Simulate response with only one translation for two inputs
    mock_response.json.return_value = {
        'translations': [
            {'text': 'Hallo'} 
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    texts_to_translate = ["Hello", "World"]
    
    with pytest.raises(TranslationError, match="API response translation count mismatch."):
        service.translate_batch(texts_to_translate, "DE")

    mock_client_instance.post.assert_called_once()
    logger.debug("test_translate_batch_response_mismatch finished")


@patch('httpx.Client')
def test_translate_batch_response_item_missing_text(mock_httpx_client_class, mock_config_loader):
    """Test translate_batch raises error if a translation item is missing 'text'."""
    logger.debug("Running test_translate_batch_response_item_missing_text")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    # Simulate response where one item lacks the 'text' key
    mock_response.json.return_value = {
        'translations': [
            {'detected_source_language': 'EN', 'text': 'Hallo'},
            {'detected_source_language': 'EN'} # Missing 'text'
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client_instance = MagicMock()
    mock_client_instance.post.return_value = mock_response
    mock_httpx_client_class.return_value = mock_client_instance

    service = TranslationService(mock_config_loader)
    texts_to_translate = ["Hello", "World"]
    
    with pytest.raises(TranslationError, match="Invalid response format received from DeepL API \(item missing text\)."):
        service.translate_batch(texts_to_translate, "DE")

    mock_client_instance.post.assert_called_once()
    logger.debug("test_translate_batch_response_item_missing_text finished")

# --- End Tests for translate_batch --- 