"""
Configuration Loader Module.

Loads application settings from a settings.txt file and environment variables 
(like API keys) from a .env file (e.g., translate.env). It validates the 
configuration according to predefined rules.

Typical Usage:

  import logging
  from config_loader import ConfigLoader, ConfigError

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  try:
      config = ConfigLoader()
      logger.info(f"Input directory: {config.get_input_dir()}")
      logger.info(f"Target languages: {config.get_target_languages()}")
      logger.info(f"API Provider: {config.get_api_provider()}")
      if not config.is_test_mode():
          logger.info(f"API Key for provider: {config.get_api_key()}")
      
  except ConfigError as e:
      logger.error(f"Failed to load configuration: {e}")
      # Handle error appropriately (e.g., exit application)
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import yaml

class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class ConfigFileNotFoundError(ConfigError):
    """Raised when a configuration file cannot be found."""
    pass

class ConfigFileNotReadableError(ConfigError):
    """Raised when a configuration file exists but cannot be read."""
    pass

class ConfigValidationError(ConfigError):
    """Raised when configuration validation fails."""
    pass

class ConfigLoader:
    """Loads and validates configuration from settings.txt and translate.env files."""

    def __init__(self, env_file='.env', settings_file='settings.yaml', default_settings_file='settings.default.yaml'):
        self.env_file = env_file
        self.settings_file = settings_file
        self.default_settings_file = default_settings_file
        self.env_vars = {}
        self.settings = {}
        self.logger = logging.getLogger(__name__)
        self._load_config()

    def _load_dotenv(self):
        """Loads environment variables from the .env file."""
        try:
            if load_dotenv(dotenv_path=self.env_file, override=True):
                self.logger.info(f"Loaded environment variables from {self.env_file}")
            else:
                self.logger.debug(f"{self.env_file} not found or empty, relying on system environment variables.")
            # Load all environment variables (system + .env)
            self.env_vars = dict(os.environ)
        except Exception as e:
            self.logger.error(f"Error loading {self.env_file}: {e}", exc_info=True)

    def _load_yaml_settings(self):
        """Loads settings from YAML files, prioritizing user file over default."""
        loaded_settings = {}
        # Load defaults first
        try:
            with open(self.default_settings_file, 'r') as f:
                loaded_settings = yaml.safe_load(f) or {}
                self.logger.info(f"Loaded default settings from {self.default_settings_file}")
        except FileNotFoundError:
            self.logger.warning(f"Default settings file {self.default_settings_file} not found.")
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing {self.default_settings_file}: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Error reading {self.default_settings_file}: {e}", exc_info=True)

        # Load user settings and merge/override defaults
        try:
            with open(self.settings_file, 'r') as f:
                user_settings = yaml.safe_load(f) or {}
                self.logger.info(f"Loaded user settings from {self.settings_file}")
                # Simple top-level merge: user settings override defaults
                loaded_settings.update(user_settings)
        except FileNotFoundError:
            self.logger.info(f"User settings file {self.settings_file} not found, using defaults.")
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing {self.settings_file}: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Error reading {self.settings_file}: {e}", exc_info=True)

        self.settings = loaded_settings
        # --- Perform Type/Value Validation --- 
        self._validate_settings()

    def _validate_settings(self):
        """Validate essential settings after loading."""
        # Example validation (add more as needed)
        provider = self.settings.get('API_PROVIDER')
        if not provider or not isinstance(provider, str):
            self.logger.warning("API_PROVIDER setting is missing or not a string.")
            # Decide if this is critical enough to raise an error

        langs = self.settings.get('TARGET_LANGUAGES_LIST')
        if not isinstance(langs, list):
            self.logger.warning("TARGET_LANGUAGES_LIST is missing or not a list. Setting to empty list.")
            self.settings['TARGET_LANGUAGES_LIST'] = []

        test_mode = self.settings.get('TEST_MODE_BOOL')
        if not isinstance(test_mode, bool):
            self.logger.warning("TEST_MODE_BOOL is missing or not a boolean. Defaulting to False.")
            self.settings['TEST_MODE_BOOL'] = False

        # Validate Retry Settings
        retry_attempts = self.settings.get('RETRY_MAX_ATTEMPTS')
        if not isinstance(retry_attempts, int) or retry_attempts < 0:
            self.logger.warning("RETRY_MAX_ATTEMPTS is missing or invalid. Defaulting to 3.")
            self.settings['RETRY_MAX_ATTEMPTS'] = 3
        
        retry_backoff = self.settings.get('RETRY_BACKOFF_FACTOR')
        if not isinstance(retry_backoff, (int, float)) or retry_backoff < 0:
            self.logger.warning("RETRY_BACKOFF_FACTOR is missing or invalid. Defaulting to 0.5.")
            self.settings['RETRY_BACKOFF_FACTOR'] = 0.5

        retry_codes = self.settings.get('RETRY_STATUS_CODES')
        if not isinstance(retry_codes, list) or not all(isinstance(code, int) for code in retry_codes):
            self.logger.warning("RETRY_STATUS_CODES is missing or invalid. Defaulting to [429, 500, 502, 503, 504].")
            self.settings['RETRY_STATUS_CODES'] = [429, 500, 502, 503, 504]

        self.logger.debug(f"Final loaded settings: {self.settings}")

    def _load_config(self):
        """Loads all configuration sources."""
        self.logger.info("Starting configuration loading...")
        self._load_dotenv()
        self._load_yaml_settings()
        self.logger.info("Configuration loading complete.")

    def reload(self):
        """Reloads configuration from files."""
        self.logger.info("Reloading configuration...")
        self._load_config()

    def _validate_file(self, file_path: Path) -> None:
        """
        Validates that a specific configuration file exists and is readable.

        Args:
            file_path (Path): Path object representing the configuration file.

        Raises:
            ConfigFileNotFoundError: If the file doesn't exist or is not a file.
            ConfigFileNotReadableError: If the file exists but can't be read.
        """
        self.logger.debug(f"Validating configuration file path: {file_path}")

        if not file_path.exists():
            msg = f"Configuration file not found: {file_path}"
            self.logger.error(msg)
            raise ConfigFileNotFoundError(msg)

        if not file_path.is_file():
            msg = f"Path exists but is not a file: {file_path}"
            self.logger.error(msg)
            # Treat non-files as not found for simplicity
            raise ConfigFileNotFoundError(msg)

        if not os.access(file_path, os.R_OK):
            msg = f"Configuration file not readable (check permissions): {file_path}"
            self.logger.error(msg)
            raise ConfigFileNotReadableError(msg)

        self.logger.debug(f"File validation successful for: {file_path}")

    def _validate_config(self) -> None:
        """
        Validates the loaded configuration settings and environment variables.

        Checks for required fields, valid values, and necessary API keys based
        on the configuration. Converts certain string settings (like 
        TARGET_LANGUAGES, YAML_TRANSLATE_FIELDS, TEST_MODE) to appropriate types 
        and stores them back in self.settings (e.g., as '_LIST' or '_BOOL' suffixed keys).

        Raises:
            ConfigValidationError: If any validation check fails.
        """
        self.logger.info("Validating configuration...")
        required_settings = [
            'INPUT_DIR',
            'OUTPUT_DIR',
            'TARGET_LANGUAGES',
            'API_PROVIDER'
            # 'YAML_TRANSLATE_FIELDS' is optional
            # 'TEST_MODE' has a default
        ]

        # Check for required settings keys
        missing_keys = [key for key in required_settings if key not in self.settings]
        if missing_keys:
            msg = f"Missing required settings in {self.settings_file}: {', '.join(missing_keys)}"
            self.logger.error(msg)
            raise ConfigValidationError(msg)

        # --- Validate specific settings values ---

        # INPUT_DIR / OUTPUT_DIR: Check non-empty and if path looks valid.
        # Actual existence/permissions check should happen when the path is used.
        for key in ['INPUT_DIR', 'OUTPUT_DIR']:
            value = self.settings.get(key)
            if not value:
                msg = f"Setting '{key}' cannot be empty."
                self.logger.error(msg)
                raise ConfigValidationError(msg)
            try:
                # Attempt to create a Path object to catch basic syntax errors
                Path(value)
                self.logger.debug(f"Path syntax validated for {key}: {value}")
            except Exception as e:
                 msg = f"Invalid path format for {key}: '{value}'. Error: {e}"
                 self.logger.error(msg)
                 raise ConfigValidationError(msg)

        # TARGET_LANGUAGES: Check non-empty and convert to list
        target_languages_str = self.settings.get('TARGET_LANGUAGES')
        if not target_languages_str:
            msg = f"Setting 'TARGET_LANGUAGES' cannot be empty."
            self.logger.error(msg)
            raise ConfigValidationError(msg)
        try:
            self.settings['TARGET_LANGUAGES_LIST'] = [lang.strip() for lang in target_languages_str.split(',') if lang.strip()]
            if not self.settings['TARGET_LANGUAGES_LIST']:
                 raise ValueError("List cannot be empty after splitting.")
            self.logger.debug(f"TARGET_LANGUAGES processed into list: {self.settings['TARGET_LANGUAGES_LIST']}")
        except Exception as e:
            msg = f"Invalid format for TARGET_LANGUAGES: '{target_languages_str}'. Expected comma-separated list. Error: {e}"
            self.logger.error(msg)
            raise ConfigValidationError(msg)

        # API_PROVIDER: Check against allowed list
        allowed_providers = {'DeepL', 'Google', 'Azure'} # Using a set for efficient lookup
        api_provider = self.settings.get('API_PROVIDER')
        if api_provider not in allowed_providers:
            msg = f"Invalid API_PROVIDER '{api_provider}'. Allowed values: {', '.join(sorted(list(allowed_providers)))}"
            self.logger.error(msg)
            raise ConfigValidationError(msg)

        # TEST_MODE: Validate format and convert to boolean
        test_mode_str = self.settings.get('TEST_MODE', 'false') # Default to 'false' string if missing
        valid_bool_strs = {'true', 'false', 'yes', 'no', '1', '0'}
        if test_mode_str.lower() not in valid_bool_strs:
            msg = f"Invalid value for TEST_MODE: '{test_mode_str}'. Use true/false, yes/no, or 1/0."
            self.logger.error(msg)
            raise ConfigValidationError(msg)
        self.settings['TEST_MODE_BOOL'] = test_mode_str.lower() in {'true', 'yes', '1'}
        self.logger.debug(f"TEST_MODE evaluated to: {self.settings['TEST_MODE_BOOL']}")

        # YAML_TRANSLATE_FIELDS: Check non-empty if present and convert to list
        yaml_fields_str = self.settings.get('YAML_TRANSLATE_FIELDS')
        if yaml_fields_str is not None: # Check if the key exists
            if not yaml_fields_str.strip():
                 msg = f"Setting 'YAML_TRANSLATE_FIELDS' cannot be empty if specified."
                 self.logger.error(msg)
                 raise ConfigValidationError(msg)
            try:
                 self.settings['YAML_TRANSLATE_FIELDS_LIST'] = [field.strip() for field in yaml_fields_str.split(',') if field.strip()]
                 if not self.settings['YAML_TRANSLATE_FIELDS_LIST']:
                     raise ValueError("List cannot be empty after splitting.")
                 self.logger.debug(f"YAML_TRANSLATE_FIELDS processed into list: {self.settings['YAML_TRANSLATE_FIELDS_LIST']}")
            except Exception as e:
                 msg = f"Invalid format for YAML_TRANSLATE_FIELDS: '{yaml_fields_str}'. Expected comma-separated list. Error: {e}"
                 self.logger.error(msg)
                 raise ConfigValidationError(msg)
        else:
             # If not specified, default to empty list
             self.settings['YAML_TRANSLATE_FIELDS_LIST'] = []
             self.logger.debug("YAML_TRANSLATE_FIELDS not specified, defaulting to empty list.")

        # Check for required API key based on provider (only if not in test mode)
        if not self.settings['TEST_MODE_BOOL']:
            api_key_map = {
                'DeepL': 'DEEPL_API_KEY',
                'Google': 'GOOGLE_CLOUD_KEY',
                'Azure': 'MICROSOFT_TRANSLATOR_KEY'
            }
            required_key = api_key_map.get(api_provider) # Use .get for safety, though provider is validated

            if required_key and required_key not in self.env_vars:
                msg = f"API_PROVIDER is set to '{api_provider}', but the required environment variable '{required_key}' was not found in {self.env_file} or the environment."
                self.logger.error(msg)
                raise ConfigValidationError(msg)
            elif required_key:
                self.logger.info(f"Required API key '{required_key}' found for provider '{api_provider}'.")
        else:
            self.logger.info("TEST_MODE is enabled. Skipping API key validation.")

        self.logger.info("Configuration validation successful.")

    # --- Public Interface --- 

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Gets a specific setting value.

        Args:
            key: The setting key to retrieve.
            default: The default value to return if the key is not found.

        Returns:
            The value of the setting or the default value.
        """
        return self.settings.get(key, default)

    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Gets a specific environment variable value loaded from the .env file.

        Args:
            key: The environment variable key to retrieve.
            default: The default value to return if the key is not found.

        Returns:
            The value of the environment variable or the default value.
        """
        # Prefer directly stored value if populated, otherwise check os.environ
        return self.env_vars.get(key, os.getenv(key, default))

    def get_input_dir(self) -> Path:
        """Gets the validated input directory path.
        
        Returns:
            A Path object representing the input directory.
        """
        return Path(self.settings['INPUT_DIR'])

    def get_output_dir(self) -> Path:
        """Gets the validated output directory path.
        
        Returns:
            A Path object representing the output directory.
        """
        return Path(self.settings['OUTPUT_DIR'])

    def get_target_languages(self) -> list[str]:
        """Gets the list of target language codes.
        
        Returns:
            A list of strings, where each string is a target language code (e.g., ['DE', 'FR']).
        """
        return self.settings.get('TARGET_LANGUAGES_LIST', [])

    def get_api_provider(self) -> str:
        """Gets the configured API provider name.
        
        Returns:
            A string representing the API provider (e.g., 'DeepL').
        """
        return self.settings['API_PROVIDER'] # Already validated to exist

    def get_yaml_translate_fields(self) -> list[str]:
        """Gets the list of YAML fields specified for translation.
        
        Returns:
            A list of strings representing the YAML field names.
            Returns an empty list if not specified in the settings.
        """
        return self.settings.get('YAML_TRANSLATE_FIELDS_LIST', [])
        
    def is_test_mode(self) -> bool:
        """Checks if test mode is enabled.
        
        Returns:
            True if test mode is enabled, False otherwise.
        """
        return self.settings.get('TEST_MODE_BOOL', False)
        
    def get_api_key(self) -> Optional[str]:
        """Gets the API key for the configured provider.

        Returns None if in test mode or if the key is not found 
        (though validation should prevent the latter unless test mode is on).

        Returns:
            The API key string, or None.
        """
        if self.is_test_mode():
            return None
            
        api_provider = self.get_api_provider()
        api_key_map = {
            'DeepL': 'DEEPL_API_KEY',
            'Google': 'GOOGLE_CLOUD_KEY',
            'Azure': 'MICROSOFT_TRANSLATOR_KEY'
        }
        key_name = api_key_map.get(api_provider)
        
        if key_name:
            # Use get_env_var which checks self.env_vars and os.getenv
            return self.get_env_var(key_name)
            
        return None # Should not happen if provider is valid

# Example usage (for testing during development)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) # Set root logger level for testing
    logger = logging.getLogger()
    logger.info("Running ConfigLoader example...")

    try:
        # Test with default paths (assuming config files exist relative to src)
        config_loader = ConfigLoader()
        logger.info("ConfigLoader initialized successfully with default paths.")

        # Test with non-existent paths
        # config_loader_bad = ConfigLoader(settings_path='nonexistent/settings.txt')

    except ConfigError as e:
        logger.error(f"Caught configuration error: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}") 