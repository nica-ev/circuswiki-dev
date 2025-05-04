from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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

# Add __init__.py if it doesn't exist
# (This part is manual or requires a separate tool call if needed)
# For now, assuming it exists or will be created manually. 