from pathlib import Path
import logging
import re
from ruamel.yaml import YAML, RoundTripDumper
from ruamel.yaml.error import YAMLError
from io import StringIO

logger = logging.getLogger(__name__)

# Custom Exception
class FrontmatterParsingError(Exception):
    """Custom exception for errors during frontmatter parsing."""
    pass

# Regex to find YAML frontmatter
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)---\s*\n', re.DOTALL | re.MULTILINE)

class FileManager:
    """Manages file system operations like scanning for specific file types."""

    def __init__(self, input_dir: str | Path):
        """Initializes the FileManager.

        Args:
            input_dir: The root directory to scan.

        Raises:
            FileNotFoundError: If the input directory does not exist.
            NotADirectoryError: If the input path is not a directory.
        """
        self.input_dir = Path(input_dir)
        self.target_extension = ".md"
        self.errors = [] # Store errors encountered during scanning

        if not self.input_dir.exists():
            msg = f"Input directory not found: {self.input_dir}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        if not self.input_dir.is_dir():
            msg = f"Input path is not a directory: {self.input_dir}"
            logger.error(msg)
            raise NotADirectoryError(msg)

        logger.info(f"FileManager initialized with input directory: {self.input_dir}")

    def _scan_directory(self, current_dir: Path) -> list[Path]:
        """Recursively scans a directory for files with the target extension.

        Args:
            current_dir: The directory to scan.

        Returns:
            A list of paths to found files.
        """
        found_files = []
        logger.debug(f"Scanning directory: {current_dir}")

        try:
            for item in current_dir.iterdir():
                try:
                    if item.is_dir():
                        # Recurse into subdirectory
                        logger.debug(f"Entering subdirectory: {item}")
                        # Add results and potentially errors from recursion
                        sub_files, sub_errors = self._scan_directory_recursive(item)
                        found_files.extend(sub_files)
                        self.errors.extend(sub_errors)
                    elif item.is_file() and item.suffix.lower() == self.target_extension:
                        # Found a target file
                        logger.debug(f"Found target file: {item}")
                        found_files.append(item)
                    # else: ignore other file types or symlinks etc.
                except PermissionError:
                    msg = f"Permission denied accessing: {item}"
                    logger.error(msg)
                    self.errors.append(msg)
                except Exception as e:
                    # Catch other potential errors during item processing
                    msg = f"Error processing item {item}: {e}"
                    logger.error(msg, exc_info=True)
                    self.errors.append(msg)

        except PermissionError:
            # Error accessing the current directory itself
            msg = f"Permission denied scanning directory: {current_dir}"
            logger.error(msg)
            self.errors.append(msg)
        except FileNotFoundError: # Should not happen if __init__ validation works
             msg = f"Directory not found during scan: {current_dir}"
             logger.error(msg)
             self.errors.append(msg)
        except Exception as e:
            # Catch other potential errors during iteration
            msg = f"Error scanning directory {current_dir}: {e}"
            logger.error(msg, exc_info=True)
            self.errors.append(msg)

        return found_files

    def _scan_directory_recursive(self, current_dir: Path) -> tuple[list[Path], list[str]]:
        """Helper for recursive scanning that also returns errors."""
        found_files = []
        errors = []
        logger.debug(f"Scanning directory: {current_dir}")

        try:
            for item in current_dir.iterdir():
                try:
                    if item.is_dir():
                        logger.debug(f"Entering subdirectory: {item}")
                        sub_files, sub_errors = self._scan_directory_recursive(item)
                        found_files.extend(sub_files)
                        errors.extend(sub_errors)
                    elif item.is_file() and item.suffix.lower() == self.target_extension:
                        logger.debug(f"Found target file: {item}")
                        found_files.append(item)
                except PermissionError:
                    msg = f"Permission denied accessing: {item}"
                    logger.error(msg)
                    errors.append(msg)
                except Exception as e:
                    msg = f"Error processing item {item}: {e}"
                    logger.error(msg, exc_info=True)
                    errors.append(msg)

        except PermissionError:
            msg = f"Permission denied scanning directory: {current_dir}"
            logger.error(msg)
            errors.append(msg)
        except FileNotFoundError:
            msg = f"Directory not found during scan: {current_dir}"
            logger.error(msg)
            errors.append(msg)
        except Exception as e:
            msg = f"Error scanning directory {current_dir}: {e}"
            logger.error(msg, exc_info=True)
            errors.append(msg)

        return found_files, errors

    def scan_markdown_files(self, relative_paths: bool = False) -> list[Path]:
        """Scans the input directory for Markdown files.

        Args:
            relative_paths: If True, return paths relative to the input directory.
                            Otherwise, return absolute paths.

        Returns:
            A list of pathlib.Path objects for the found Markdown files.
            Scan errors can be retrieved using get_scan_errors().
        """
        logger.info(f"Starting Markdown file scan in: {self.input_dir}")
        self.errors.clear() # Clear errors from previous scans

        found_files, initial_errors = self._scan_directory_recursive(self.input_dir)
        self.errors.extend(initial_errors)

        if relative_paths:
            processed_files = [
                file.relative_to(self.input_dir) for file in found_files
            ]
        else:
            # Ensure paths are absolute (pathlib usually handles this, but good practice)
            processed_files = [file.resolve() for file in found_files]

        logger.info(f"Scan complete. Found {len(processed_files)} Markdown files.")
        if self.errors:
            logger.warning(f"Encountered {len(self.errors)} errors during scan. Use get_scan_errors() for details.")
        
        return processed_files

    def get_scan_errors(self) -> list[str]:
        """Returns a list of error messages encountered during the last scan."""
        return self.errors

    def read_markdown_with_frontmatter(self, file_path: str | Path) -> tuple[dict | None, str]:
        """Reads a Markdown file and extracts frontmatter.

        Args:
            file_path: The path to the Markdown file.

        Returns:
            A tuple containing:
            - The parsed frontmatter as a dictionary (or None if none/error).
            - The content string without the frontmatter.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
            FrontmatterParsingError: If the frontmatter is present but malformed YAML.
        """
        file_path = Path(file_path)
        logger.debug(f"Reading file with frontmatter: {file_path}")

        if not file_path.is_file():
            # Ensure it's actually a file before reading
            msg = f"Path is not a file: {file_path}"
            logger.error(msg)
            # Or raise a more specific error? For now, FileNotFoundError might fit.
            raise FileNotFoundError(msg)

        try:
            content = file_path.read_text(encoding='utf-8')
            # Call the static extraction method
            frontmatter, content_without_frontmatter = self._extract_frontmatter_and_content(content)
            logger.debug(f"Successfully read and extracted frontmatter from: {file_path}")
            return frontmatter, content_without_frontmatter
        except FileNotFoundError:
            msg = f"File not found: {file_path}"
            logger.error(msg)
            raise
        except PermissionError:
            msg = f"Permission denied reading file: {file_path}"
            logger.error(msg)
            raise
        except FrontmatterParsingError: # Catch custom error from extraction
            # Logged in _extract_frontmatter_and_content, just re-raise
            raise
        except YAMLError: # Should now be caught by the custom error, but keep as fallback?
             logger.error(f"Unexpected YAML parsing error in file: {file_path}", exc_info=True)
             raise FrontmatterParsingError(f"YAML parsing error in {file_path}") from None # Wrap in custom error
        except Exception as e:
            msg = f"Error reading file {file_path}: {e}"
            logger.error(msg, exc_info=True)
            # Raise a generic exception or a custom one?
            raise IOError(msg) from e

    @staticmethod
    def _extract_frontmatter_and_content(content: str) -> tuple[dict | None, str]:
        """Extracts YAML frontmatter and the remaining content from a string.

        Args:
            content: The string content (typically from a file).

        Returns:
            A tuple containing:
            - The parsed frontmatter as a dictionary.
            - Returns None for frontmatter if:
                - No frontmatter block is found.
                - Frontmatter block is found but is not a valid YAML dictionary.
            - Returns {} for frontmatter if delimiters --- exist but are empty.
            - The content string without the frontmatter section.

        Raises:
            FrontmatterParsingError: If the frontmatter is present but malformed YAML.
        """
        frontmatter: dict | None = None
        match = FRONTMATTER_RE.match(content)

        if match:
            yaml_string = match.group(1)
            content_without_frontmatter = content[match.end():]

            if yaml_string.strip():
                try:
                    yaml = YAML(typ='safe')
                    parsed_data = yaml.load(yaml_string)
                    if isinstance(parsed_data, dict):
                        frontmatter = parsed_data
                    else:
                        # Valid YAML, but not a dictionary
                        logger.warning(
                            f"Frontmatter parsed successfully but is not a dictionary (type: {type(parsed_data)}). Treating as no frontmatter."
                        )
                        # Return original content as frontmatter wasn't usable
                        content_without_frontmatter = content
                        frontmatter = None # Explicitly None
                except YAMLError as e:
                    msg = f"Malformed YAML frontmatter detected: {e}"
                    logger.error(msg)
                    # Raise custom error, wrapping original
                    raise FrontmatterParsingError(msg) from e
            else:
                # Delimiters found, but empty content between them
                logger.debug("Found empty frontmatter block (--- ---). Returning {} for frontmatter.")
                frontmatter = {}
        else:
            # No --- delimiters found at the start
            logger.debug("No frontmatter block detected.")
            content_without_frontmatter = content
            frontmatter = None

        return frontmatter, content_without_frontmatter

    def is_eligible_for_translation(self, file_path: str | Path) -> bool:
        """Checks if a Markdown file is eligible for translation based on frontmatter.

        Eligibility requires the frontmatter to contain 'orig: true'.

        Args:
            file_path: The path to the Markdown file.

        Returns:
            True if the file is eligible, False otherwise.
        """
        file_path = Path(file_path)
        logger.debug(f"Checking translation eligibility for: {file_path}")

        try:
            frontmatter, _ = self.read_markdown_with_frontmatter(file_path)

            if isinstance(frontmatter, dict) and frontmatter.get('orig') is True:
                logger.debug(f"File IS eligible for translation (orig: true): {file_path}")
                return True
            else:
                logger.debug(f"File is NOT eligible for translation (orig: true not found or not True): {file_path}")
                return False

        except FileNotFoundError:
            logger.warning(f"Eligibility check failed: File not found {file_path}")
            return False
        except PermissionError:
            logger.warning(f"Eligibility check failed: Permission denied for {file_path}")
            return False
        except FrontmatterParsingError:
            logger.warning(f"Eligibility check failed: Frontmatter parsing error in {file_path}")
            return False
        except Exception as e:
            logger.error(f"Eligibility check failed: Unexpected error for {file_path}: {e}", exc_info=True)
            return False

    @staticmethod
    def _strip_frontmatter(content: str) -> str:
        """Removes the YAML frontmatter block from the start of a string.

        Args:
            content: The string content.

        Returns:
            The content string without the frontmatter block.
        """
        match = FRONTMATTER_RE.match(content)
        if match:
            return content[match.end():]
        else:
            return content

    def get_frontmatter_value(self, file_path: str | Path, key: str, default=None):
        """Gets a specific value from the frontmatter of a Markdown file.

        Args:
            file_path: The path to the Markdown file.
            key: The key to retrieve from the frontmatter dictionary.
            default: The value to return if the key is not found or file/frontmatter
                     cannot be read/parsed.

        Returns:
            The value associated with the key, or the default value.
        """
        file_path = Path(file_path)
        logger.debug(f"Getting frontmatter key '{key}' from: {file_path}")
        try:
            frontmatter, _ = self.read_markdown_with_frontmatter(file_path)
            if isinstance(frontmatter, dict):
                return frontmatter.get(key, default)
            else:
                # No frontmatter or not a dict
                return default
        except (FileNotFoundError, PermissionError, FrontmatterParsingError, IOError) as e:
            logger.warning(f"Could not get frontmatter value for '{key}' from {file_path} (Reason: {type(e).__name__}). Returning default.")
            return default
        except Exception as e:
            logger.error(f"Unexpected error getting frontmatter value for '{key}' from {file_path}: {e}", exc_info=True)
            return default

    def update_frontmatter(self, file_path: str | Path, updates_dict: dict):
        """Updates the YAML frontmatter of a Markdown file.

        Overwrites the existing file with updated frontmatter and original content.
        Attempts a basic round-trip dump to preserve some formatting, but complex
        comments/styles might be lost.

        Args:
            file_path: The path to the Markdown file.
            updates_dict: Dictionary containing keys and values to add/update.

        Raises:
            FileNotFoundError, PermissionError, FrontmatterParsingError, IOError:
                If the file cannot be read, parsed, or written.
        """
        file_path = Path(file_path)
        logger.info(f"Updating frontmatter for: {file_path}")

        try:
            # Read existing data
            # Note: read_markdown_with_frontmatter uses safe_load, losing comments.
            # For true round-trip, we might need to re-parse here with RoundTripLoader
            # or adjust the initial read method. For now, proceed with potential comment loss.
            frontmatter, content_without_frontmatter = self.read_markdown_with_frontmatter(file_path)

            if frontmatter is None:
                current_fm = {}
            else:
                current_fm = frontmatter # Already a dict or {}
            
            # Apply updates
            current_fm.update(updates_dict)

            # Dump updated frontmatter back to YAML string
            yaml = YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            string_stream = StringIO()
            yaml.dump(current_fm, string_stream)
            updated_yaml_string = string_stream.getvalue()

            # Construct new file content
            new_content = f"---\n{updated_yaml_string}---\n{content_without_frontmatter}"
            
            # Write back to file
            file_path.write_text(new_content, encoding='utf-8')
            logger.info(f"Successfully updated frontmatter for: {file_path}")

        except (FileNotFoundError, PermissionError, FrontmatterParsingError, IOError) as e:
            logger.error(f"Failed to update frontmatter for {file_path}: {e}", exc_info=True)
            raise # Re-raise file/parsing/IO errors
        except Exception as e:
            logger.error(f"Unexpected error updating frontmatter for {file_path}: {e}", exc_info=True)
            # Wrap unexpected errors
            raise IOError(f"Unexpected error updating {file_path}") from e

# Add __init__.py if it doesn't exist
# (This part is manual or requires a separate tool call if needed)
# For now, assuming it exists or will be created manually. 