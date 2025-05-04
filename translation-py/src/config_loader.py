import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class ConfigFileNotFoundError(ConfigError):
    """Raised when a configuration file cannot be found."""
    pass

class ConfigFileNotReadableError(ConfigError):
    """Raised when a configuration file exists but cannot be read."""
    pass

class ConfigLoader:
    """Loads and validates configuration from settings.txt and translate.env files."""

    def __init__(self, settings_path: Optional[str] = None, env_path: Optional[str] = None):
        """
        Initializes the ConfigLoader, validates file paths, and sets up logging.

        Args:
            settings_path: Optional path to the settings.txt file.
            env_path: Optional path to the translate.env file.
        
        Raises:
            ConfigFileNotFoundError: If a config file doesn't exist.
            ConfigFileNotReadableError: If a config file exists but is not readable.
            ConfigError: For other configuration-related errors.
        """
        # Get the directory where this script's parent (src) is located
        base_dir = Path(__file__).parent.parent

        # Resolve absolute paths for config files
        self.settings_file: Path = Path(settings_path or base_dir / "config" / "settings.txt").resolve()
        self.env_file: Path = Path(env_path or base_dir / "config" / "translate.env").resolve()

        # Initialize empty configuration dictionaries
        self.settings: Dict[str, Any] = {}
        self.env_vars: Dict[str, str] = {}

        # Set up logging
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
             # Add handler if logger is not already configured (e.g., by root logger)
             handler = logging.StreamHandler()
             formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
             handler.setFormatter(formatter)
             self.logger.addHandler(handler)
             self.logger.setLevel(logging.INFO) # Default level

        self.logger.info("Initializing ConfigLoader...")
        self.logger.debug(f"Using settings file: {self.settings_file}")
        self.logger.debug(f"Using environment file: {self.env_file}")

        # Validate configuration files
        try:
            self._validate_file(self.settings_file)
            self._validate_file(self.env_file)
            self.logger.info("Configuration files validated successfully.")
        except ConfigError as e:
            self.logger.error(f"Configuration error during initialization: {e}")
            raise # Re-raise the specific config error

    def _validate_file(self, file_path: Path) -> None:
        """
        Validate that a configuration file exists and is readable.

        Args:
            file_path: Path object representing the configuration file.

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