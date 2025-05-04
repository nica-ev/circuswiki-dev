import os
import logging
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
import re
import yaml
from ruamel.yaml import YAML as RuamelYAML
import copy # Import copy for deepcopy

from .utils.normalization import normalize_markdown_content
from .utils.hashing import calculate_content_hash, calculate_yaml_hash
from .utils.yaml_utils import normalize_yaml

# Custom Exceptions
class FileManagerError(Exception):
    """Base exception for FileManager errors."""
    pass

class DirectoryAccessError(FileManagerError):
    """Raised when a directory cannot be accessed."""
    pass

class ScanConfigurationError(FileManagerError):
    """Raised for invalid scan configuration."""
    pass

class FrontmatterParsingError(FileManagerError):
    """Custom exception for frontmatter parsing failures."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class FileWriteError(FileManagerError):
    """Raised when writing to a file fails."""
    pass


logger = logging.getLogger(__name__)

class FileManager:
    """Manages file system operations like scanning, reading, and writing files."""

    def __init__(self, config_loader):
        """Initializes the FileManager with configuration."""
        self.config_loader = config_loader
        self.input_dir = self.config_loader.get_setting('INPUT_DIR_PATH')
        self.output_dir = self.config_loader.get_setting('OUTPUT_DIR_PATH')
        self.file_extensions = self.config_loader.get_setting('FILE_EXTENSIONS', ['.md'])
        self.yaml_translate_fields = self.config_loader.get_setting('YAML_TRANSLATE_FIELDS', [])
        self.skip_existing = self.config_loader.get_setting('SKIP_EXISTING', False)

        if not self.input_dir or not self.input_dir.is_dir():
            raise DirectoryAccessError(f"Input directory does not exist or is not a directory: {self.input_dir}")
        if not self.output_dir:
            raise ScanConfigurationError("Output directory is not configured.")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.yaml_parser = RuamelYAML() # For preserving comments/formatting
        self.yaml_parser.preserve_quotes = True

        self.logger.info(f"FileManager initialized. Input: {self.input_dir}, Output: {self.output_dir}")
        self.logger.debug(f"Processing extensions: {self.file_extensions}")
        self.logger.debug(f"YAML fields to translate: {self.yaml_translate_fields}")

    # --- Directory and Path Management ---

    def get_output_path(self, file_path: Union[str, Path], lang_code: str) -> Path:
        """
        Constructs output file path based on language code and original file path.

        Args:
            file_path (str or Path): Original file path (absolute or relative)
            lang_code (str): Target language code (e.g., 'es', 'fr')

        Returns:
            Path: Absolute path to the output file

        Raises:
            ValueError: If file_path is not within input_dir or lang_code is empty.
            DirectoryAccessError: If output directory structure cannot be created.
        """
        if not lang_code:
            raise ValueError("Language code cannot be empty.")

        file_path = Path(file_path).resolve()

        # Verify file is within input directory to prevent path traversal
        try:
            relative_path = file_path.relative_to(self.input_dir)
        except ValueError:
            self.logger.error(f"File {file_path} is not within input directory {self.input_dir}")
            raise ValueError(f"File {file_path} is not within input directory {self.input_dir}")

        # Construct output path
        output_path = self.output_dir / lang_code / relative_path

        # Ensure parent directories exist
        self.ensure_output_directory(output_path) # Raises DirectoryAccessError on failure

        return output_path

    def ensure_output_directory(self, output_path: Path) -> bool:
        """
        Ensures the directory for the given output path exists, creating it if necessary.

        Args:
            output_path: Path object representing the intended output file

        Returns:
            bool: True if directory exists or was created successfully.

        Raises:
            DirectoryAccessError: If directory creation fails due to permissions or other system issues.
        """
        directory = output_path.parent
        if directory.exists():
            if not directory.is_dir():
                 raise DirectoryAccessError(f"Output path conflict: {directory} exists but is not a directory.")
            return True

        try:
            # Create directory and any missing parents with appropriate permissions
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created output directory: {directory}")
            return True
        except OSError as e:
            self.logger.error(f"Error creating directory for {output_path}: {e}", exc_info=True)
            raise DirectoryAccessError(f"Failed to create output directory {directory}: {e}") from e

    def prepare_output_directories(self, lang_codes: List[str]):
        """
        Creates output directories for all specified language codes.

        Args:
            lang_codes (list): List of language codes to prepare directories for

        Raises:
            DirectoryAccessError: If any directory creation fails.
        """
        self.logger.info(f"Preparing output directories for languages: {lang_codes}")
        if not self.output_dir.exists():
             self.output_dir.mkdir(parents=True, exist_ok=True)
             self.logger.debug(f"Created base output directory: {self.output_dir}")

        for lang_code in lang_codes:
            lang_dir = self.output_dir / lang_code
            if not lang_dir.exists():
                try:
                    lang_dir.mkdir(parents=True, exist_ok=True)
                    self.logger.debug(f"Created language directory: {lang_dir}")
                except OSError as e:
                    self.logger.error(f"Failed to create directory {lang_dir}: {e}", exc_info=True)
                    raise DirectoryAccessError(f"Failed to create language directory {lang_dir}: {e}") from e
            elif not lang_dir.is_dir():
                 raise DirectoryAccessError(f"Output path conflict: {lang_dir} exists but is not a directory.")

    # --- File Scanning ---

    def scan_markdown_files(self) -> List[Path]:
        """
        Scans the input directory recursively for Markdown files.

        Returns:
            List[Path]: A list of absolute paths to the found Markdown files.
        """
        self.logger.info(f"Scanning for files with extensions {self.file_extensions} in {self.input_dir}")
        found_files: List[Path] = []
        start_time = time.time()
        errors = []
        dirs_scanned = 0

        for root, _, files in os.walk(self.input_dir):
            dirs_scanned += 1
            current_dir = Path(root)
            for filename in files:
                if any(filename.lower().endswith(ext.lower()) for ext in self.file_extensions):
                    file_path = current_dir / filename
                    # Basic check to avoid potential symlink loops, might need enhancement
                    if file_path.is_file():
                        found_files.append(file_path.resolve())
                    else:
                         self.logger.warning(f"Skipping non-file entry: {file_path}")


        elapsed = time.time() - start_time
        self.logger.info(f"Scan completed in {elapsed:.2f}s. Found {len(found_files)} files in {dirs_scanned} directories.")
        if errors:
            self.logger.warning(f"{len(errors)} errors encountered during scan.")
            for path, error in errors:
                 self.logger.debug(f"  - {path}: {error}")
        return found_files

    # --- Frontmatter Handling ---

    @staticmethod
    def _extract_frontmatter_and_content(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Extracts YAML frontmatter and content from markdown text using regex.

        Returns:
            tuple: (frontmatter_dict or None, content_without_frontmatter or original_content)

        Raises:
            FrontmatterParsingError: When YAML parsing fails (wraps YAMLError).
        """
        # Regex to find --- delimited frontmatter at the start
        # Handles potential whitespace before/after delimiters
        pattern = r'^\\s*---\\s*\\n(.*?)\\n\\s*---\\s*\\n?(.*)$'
        match = re.match(pattern, content, re.DOTALL | re.MULTILINE)

        if not match:
            logger.debug("No frontmatter found.")
            return None, content

        frontmatter_yaml = match.group(1).strip()
        markdown_content = match.group(2).strip()

        if not frontmatter_yaml:
            logger.info("Empty frontmatter block found.")
            return {}, markdown_content # Return empty dict for empty block

        try:
            # Use safe_load to avoid arbitrary code execution
            frontmatter = yaml.safe_load(frontmatter_yaml)
            if not isinstance(frontmatter, dict):
                 logger.warning(f"Frontmatter parsed but is not a dictionary (type: {type(frontmatter)}). Treating as invalid.")
                 # Decide how to handle non-dict frontmatter, here returning None
                 return None, content # Or maybe raise FrontmatterParsingError?
            logger.debug("Successfully extracted frontmatter.")
            return frontmatter, markdown_content
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse frontmatter YAML: {e}", exc_info=True)
            raise FrontmatterParsingError(f"Invalid YAML in frontmatter: {e}", e) from e

    def read_markdown_with_frontmatter(self, file_path: Union[str, Path]) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Reads a markdown file, extracts frontmatter, and returns both parts.

        Args:
            file_path: Path to the markdown file.

        Returns:
            Tuple containing (frontmatter dictionary or None, content string).
            Returns (None, file_content) if no frontmatter is found or parsing fails.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            PermissionError: If the file cannot be read.
            FrontmatterParsingError: If YAML is malformed.
        """
        file_path = Path(file_path)
        self.logger.debug(f"Reading file with frontmatter: {file_path}")
        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            # Use the static method for extraction
            frontmatter, markdown_content = self._extract_frontmatter_and_content(content)
            return frontmatter, markdown_content
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except PermissionError:
            self.logger.error(f"Permission denied reading file: {file_path}")
            raise
        except FrontmatterParsingError:
            # Already logged in _extract_frontmatter_and_content
            raise # Re-raise to signal the issue upstream
        except Exception as e:
            self.logger.error(f"Unexpected error reading file {file_path}: {e}", exc_info=True)
            raise FileManagerError(f"Failed to read file {file_path}") from e


    def is_eligible_for_translation(self, file_path: Union[str, Path]) -> bool:
        """
        Determines if a Markdown file is eligible for translation based on frontmatter.
        Checks for the presence and value of the 'orig' key.

        Args:
            file_path: Path to the Markdown file.

        Returns:
            bool: True if file has 'orig: true' in frontmatter, False otherwise.
                  Returns False if file doesn't exist, can't be read, or frontmatter fails parsing.
        """
        try:
            frontmatter, _ = self.read_markdown_with_frontmatter(file_path)

            # Check if frontmatter exists and contains 'orig: true'
            if isinstance(frontmatter, dict):
                orig_value = frontmatter.get('orig')
                # Explicitly check for boolean True
                return orig_value is True
            return False # No frontmatter or not a dict

        except (FileNotFoundError, PermissionError, FrontmatterParsingError) as e:
             # Logged in read_markdown_with_frontmatter or _extract_frontmatter_and_content
             self.logger.debug(f"File not eligible due to read/parse error: {file_path} ({type(e).__name__})")
             return False
        except Exception as e:
            # Catch any other unexpected errors during read
            self.logger.error(f"Unexpected error checking eligibility for {file_path}: {e}", exc_info=True)
            return False

    @staticmethod
    def generate_frontmatter(
        original_frontmatter: Optional[Dict[str, Any]],
        translated_fields: Dict[str, Any],
        lang_code: str,
        source_hashes: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate frontmatter for translated files.

        Args:
            original_frontmatter (dict or None): Original frontmatter dictionary.
            translated_fields (dict): Dictionary of translated fields (can include nested paths).
            lang_code (str): Language code for the translation.
            source_hashes (dict, optional): Dictionary containing 'content' and 'yaml' hash keys
                                            of the source document.

        Returns:
            dict: New frontmatter dictionary ready for serialization.
        """
        logger.debug(f"Generating frontmatter for lang: {lang_code}")
        # Initialize with a deep copy of the original or an empty dict
        new_frontmatter = copy.deepcopy(original_frontmatter or {})

        # --- Set standard translation metadata ---
        new_frontmatter['lang'] = lang_code
        new_frontmatter['orig'] = False

        # --- Add source hash information under a specific key ---
        if source_hashes and isinstance(source_hashes, dict):
             # Use a sub-dictionary for clarity
             translation_meta = new_frontmatter.setdefault('_translation', {})
             if 'content' in source_hashes:
                 translation_meta['source_content_hash'] = source_hashes['content']
             if 'yaml' in source_hashes:
                 translation_meta['source_yaml_hash'] = source_hashes['yaml']
             logger.debug(f"Added source hashes: {translation_meta}")


        # --- Add translated fields, overwriting existing ones ---
        # Basic implementation for top-level fields. Needs enhancement for nested paths.
        # TODO: Enhance to handle nested paths in translated_fields if needed
        for key, value in translated_fields.items():
             if key in new_frontmatter:
                 logger.debug(f"Overwriting field '{key}' with translated value.")
             else:
                 logger.debug(f"Adding translated field '{key}'.")
             new_frontmatter[key] = value

        # --- Remove fields that should not be copied (like source hashes) ---
        # Example: If original frontmatter had hashes, remove them from translated version
        if '_translation' in new_frontmatter:
             # Keep our newly added hashes, but remove any old hash keys if they existed
             # This example assumes hashes are ONLY under _translation
             pass # Current logic replaces _translation content if hashes provided

        if 'content_hash' in new_frontmatter: # Example of removing old flat hash keys
             del new_frontmatter['content_hash']
        if 'yaml_hash' in new_frontmatter:
             del new_frontmatter['yaml_hash']


        logger.debug(f"Generated frontmatter keys: {list(new_frontmatter.keys())}")
        return new_frontmatter

    # --- File Reading/Writing ---

    def write_translated_file(self, output_path: Path, frontmatter: Dict[str, Any], content: str):
        """
        Writes the translated content with generated frontmatter to the output file.
        Uses RuamelYAML for serialization to preserve comments/formatting where possible.
        Implements safe atomic write (write to temp -> replace).

        Args:
            output_path: The absolute path where the translated file should be written.
            frontmatter: The dictionary representing the YAML frontmatter.
            content: The translated markdown content string.

        Raises:
            FileWriteError: If writing to the file fails.
            DirectoryAccessError: If the output directory cannot be created/accessed.
        """
        self.logger.info(f"Writing translated file: {output_path}")
        temp_path = None # Initialize in case directory creation fails

        try:
            # Ensure the output directory exists
            self.ensure_output_directory(output_path) # Raises DirectoryAccessError if fails

            # Serialize frontmatter using RuamelYAML
            from io import StringIO
            string_stream = StringIO()
            # Use the instance's yaml_parser configured in __init__
            self.yaml_parser.dump(frontmatter, string_stream)
            yaml_string = string_stream.getvalue()

            # Construct final file content with delimiters and newline
            # Ensure proper newlines regardless of yaml_string ending
            final_content = f"---\n{yaml_string.strip()}\n---\n\n{content}"

            # Define temporary file path
            temp_path = output_path.with_suffix(output_path.suffix + '.tmp')

            # Write to temporary file
            with temp_path.open('w', encoding='utf-8') as f:
                f.write(final_content)
            self.logger.debug(f"Wrote content to temporary file: {temp_path}")

            # Replace original file with temporary file atomically
            os.replace(temp_path, output_path)
            self.logger.debug(f"Successfully wrote and replaced file: {output_path}")

        except DirectoryAccessError: # Propagate directory errors
             raise
        except Exception as e:
            self.logger.error(f"Failed to write translated file {output_path}: {e}", exc_info=True)
            # Attempt to clean up temp file if it exists
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    self.logger.debug(f"Removed temporary file after error: {temp_path}")
                except OSError as unlink_err:
                    self.logger.warning(f"Could not remove temporary file after error: {temp_path}, Error: {unlink_err}")
            raise FileWriteError(f"Failed to write file {output_path}") from e


    # --- Hash Calculation ---

    def calculate_hashes(self, file_path: Union[str, Path]) -> Optional[Dict[str, str]]:
        """
        Calculates content_hash and yaml_hash for a given file.

        Args:
            file_path: Path to the markdown file.

        Returns:
            Dictionary with 'content' and 'yaml' hashes, or None if reading/parsing fails.
        """
        try:
            frontmatter, content = self.read_markdown_with_frontmatter(file_path)
            content_hash = calculate_content_hash(content)
            # Pass the original frontmatter dict (or empty dict if None)
            yaml_hash = calculate_yaml_hash(frontmatter if frontmatter is not None else {})
            return {'content': content_hash, 'yaml': yaml_hash}
        except (FileNotFoundError, PermissionError, FrontmatterParsingError) as e:
            self.logger.warning(f"Could not calculate hashes for {file_path}: {e}")
            return None
        except Exception as e:
             self.logger.error(f"Unexpected error calculating hashes for {file_path}: {e}", exc_info=True)
             return None

    def update_file_hashes(self, file_path: Union[str, Path], content_hash: str, yaml_hash: str) -> bool:
        """
        Updates the content_hash and yaml_hash in the source file's frontmatter.
        Uses a safe write mechanism (backup -> write temp -> replace).

        Args:
            file_path: Path to the source markdown file.
            content_hash: The new content hash.
            yaml_hash: The new yaml hash.

        Returns:
            True if update was successful, False otherwise.
        """
        file_path = Path(file_path).resolve()
        self.logger.info(f"Starting hash update for source file: {file_path}")
        backup_path = file_path.with_suffix(file_path.suffix + '.hashbak') # Use distinct backup suffix
        temp_path = file_path.with_suffix(file_path.suffix + '.tmp')

        try:
            # 1. Read original content and frontmatter
            original_content_str = file_path.read_text(encoding='utf-8')
            frontmatter, body_content = self._extract_frontmatter_and_content(original_content_str)
            if frontmatter is None: frontmatter = {}

            # 2. Update hash values
            system_meta = frontmatter.setdefault('_system', {})
            hashes_meta = system_meta.setdefault('hashes', {})
            hashes_meta['content'] = content_hash
            hashes_meta['yaml'] = yaml_hash
            hashes_meta['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            # 3. Serialize updated frontmatter
            from io import StringIO
            string_stream = StringIO()
            yaml.dump(frontmatter, string_stream, default_flow_style=False, allow_unicode=True, sort_keys=False)
            updated_yaml_string = string_stream.getvalue().strip()

            # 4. Reconstruct the full file content
            updated_full_content = f"---\n{updated_yaml_string}\n---\n{body_content}"

            # --- 5. Safe Write: Backup -> Write Temp -> Replace ---
            # Create backup (only if original file exists)
            if file_path.exists():
                os.replace(file_path, backup_path)
                self.logger.debug(f"Created backup: {backup_path}")

            # Write updated content to temporary file
            temp_path.write_text(updated_full_content, encoding='utf-8')
            self.logger.debug(f"Wrote updated content to temporary file: {temp_path}")

            # Replace original with temporary file (atomic on most systems)
            os.replace(temp_path, file_path)
            self.logger.info(f"Successfully updated hashes in {file_path}")

            # Remove backup on success
            if backup_path.exists():
                 backup_path.unlink()
                 self.logger.debug(f"Removed backup file: {backup_path}")

            return True

        except (FileNotFoundError, PermissionError, FrontmatterParsingError) as e:
            # Errors during reading/parsing are handled here, no need to restore backup
            self.logger.error(f"Failed during read/parse phase of hash update for {file_path}: {e}")
            # Clean up temp file if it was created due to partial failure
            if temp_path.exists():
                try: temp_path.unlink() 
                except OSError: pass
            return False
        except Exception as e:
            # Handle errors during write/replace, attempting to restore backup
            self.logger.error(f"Failed during write/replace phase of hash update for {file_path}: {e}", exc_info=True)
            if backup_path.exists():
                try:
                    os.replace(backup_path, file_path) # Try to restore original
                    self.logger.warning(f"Restored original file from backup: {backup_path}")
                except OSError as restore_err:
                    self.logger.critical(f"CRITICAL: Failed to restore {file_path} from backup {backup_path}. Manual intervention needed. Error: {restore_err}")
            # Clean up temp file if it exists
            if temp_path.exists():
                try: temp_path.unlink()
                except OSError: pass # Already logged the main error
            return False 