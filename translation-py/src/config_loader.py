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

class ConfigValidationError(Exception):
    """Exception raised for configuration validation errors."""
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
        """Validates configuration parameters and raises ConfigValidationError if invalid."""
        required_settings = ['INPUT_DIR', 'OUTPUT_DIR', 'TARGET_LANGUAGES', 'API_PROVIDER']
        missing = [setting for setting in required_settings if not self.settings.get(setting)]
        if missing:
            raise ConfigValidationError(f"Missing required settings: {', '.join(missing)}")

        # Validate directories
        for dir_setting in ['INPUT_DIR', 'OUTPUT_DIR']:
            path = Path(self.settings[dir_setting]) # Ensure path is Path object
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True) # Added exist_ok=True
                    self.logger.info(f"Created directory: {path}")
                except Exception as e:
                    raise ConfigValidationError(f"Cannot create {dir_setting} directory: {path} - {str(e)}")
            elif not path.is_dir(): # Check if it exists but is not a directory
                 raise ConfigValidationError(f"{dir_setting} path exists but is not a directory: {path}")

        # Validate target languages
        target_langs = self.settings.get('TARGET_LANGUAGES')
        if not isinstance(target_langs, list) or not target_langs:
            raise ConfigValidationError("TARGET_LANGUAGES must be a non-empty list")
        self.settings['TARGET_LANGUAGES_LIST'] = [str(lang).strip() for lang in target_langs] # Simplified assignment

        # Validate API provider
        allowed_providers = ['DeepL', 'Google', 'Azure']
        if self.settings.get('API_PROVIDER') not in allowed_providers:
            raise ConfigValidationError(
                f"API_PROVIDER must be one of: {', '.join(allowed_providers)}"
            )

        # Process TEST_MODE (ensure it's boolean)
        test_mode_val = self.settings.get('TEST_MODE', False)
        if isinstance(test_mode_val, str):
            self.settings['TEST_MODE_BOOL'] = test_mode_val.lower() in ['true', '1', 'yes']
        else:
            self.settings['TEST_MODE_BOOL'] = bool(test_mode_val)

        # Validate YAML_TRANSLATE_FIELDS if present
        yaml_fields = self.settings.get('YAML_TRANSLATE_FIELDS')
        if yaml_fields is not None:
            if not isinstance(yaml_fields, list):
                 raise ConfigValidationError("YAML_TRANSLATE_FIELDS must be a list")
            self.settings['YAML_TRANSLATE_FIELDS_LIST'] = [str(field).strip() for field in yaml_fields] # Simplified assignment
        else:
             self.settings['YAML_TRANSLATE_FIELDS_LIST'] = []

        # Validate numeric types
        for key in ['API_REQUEST_TIMEOUT', 'BATCH_SIZE', 'RETRY_MAX_ATTEMPTS', 'RETRY_BACKOFF_FACTOR']:
            try:
                self.settings[key] = float(self.settings[key]) if key == 'RETRY_BACKOFF_FACTOR' else int(self.settings[key])
            except (ValueError, TypeError):
                 raise ConfigValidationError(f"Invalid numeric value for {key}: {self.settings.get(key)}")

        # Validate boolean types
        for key in ['PRESERVE_FORMATTING', 'SKIP_EXISTING']:
             val = self.settings.get(key)
             if isinstance(val, str):
                  self.settings[key] = val.lower() in ['true', '1', 'yes']
             else:
                  self.settings[key] = bool(val)

        # Validate list types
        for key in ['FILE_EXTENSIONS', 'RETRY_STATUS_CODES']:
             val = self.settings.get(key)
             if not isinstance(val, list):
                  raise ConfigValidationError(f"{key} must be a list")
             if key == 'RETRY_STATUS_CODES':
                  try:
                      self.settings[key] = [int(code) for code in val]
                  except ValueError:
                       raise ConfigValidationError(f"Invalid integer found in RETRY_STATUS_CODES: {val}")

        # Check for API keys when not in test mode
        if not self.settings.get('TEST_MODE_BOOL'):
            api_key_map = {
                'DeepL': 'DEEPL_API_KEY',
                'Google': 'GOOGLE_API_KEY', # Changed from GOOGLE_CLOUD_KEY
                'Azure': 'AZURE_API_KEY' # Changed from MICROSOFT_TRANSLATOR_KEY
            }
            provider = self.settings.get('API_PROVIDER')
            required_key = api_key_map.get(provider)
            if required_key and not self.env_vars.get(required_key):
                raise ConfigValidationError(f"Missing required API key for {provider}: {required_key}")

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
        """Get a validated configuration setting."""
        return self.settings.get(key, default)

    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get an environment variable."""
        return self.env_vars.get(key, default)

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