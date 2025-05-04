# translation-py/tests/services/test_translation_service.py
import pytest
import logging
import httpx # Import httpx for RequestError
from unittest.mock import MagicMock, patch, ANY

# Adjust the import path based on your project structure
try:
    # Assuming tests run from the root of the translation-py subproject
    from src.services.translation_service import TranslationService, TranslationConfigError
    from src.config_loader import ConfigLoader
except ImportError:
    # Fallback if running from workspace root or structure differs
    from translation_py.src.services.translation_service import TranslationService, TranslationConfigError
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
def test_translate_text_api_error(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles API error response."""
    logger.debug("Running test_translate_text_api_error")
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 403
    mock_response.text = "Forbidden - Invalid API Key"
    # Configure raise_for_status to actually raise the error for non-2xx codes
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Client error '403 Forbidden' for url 'https://api-free.deepl.com/v2/translate'",
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

    with pytest.raises(RuntimeError, match="DeepL API Error 403: Forbidden - Invalid API Key"):
        service.translate_text("Hello World", "DE")

    mock_client_instance.post.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    logger.debug("test_translate_text_api_error finished")

@patch('httpx.Client')
def test_translate_text_network_error(mock_httpx_client_class, mock_config_loader):
    """Test translate_text handles network errors."""
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

    with pytest.raises(httpx.RequestError, match="Connection refused"):
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