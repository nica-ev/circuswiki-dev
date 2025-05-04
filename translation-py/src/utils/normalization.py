import re
import yaml
import unicodedata
import hashlib # Added for hashing
from collections.abc import Mapping # Use Mapping for type hint


def normalize_markdown_content(content: str) -> str:
    """Normalizes Markdown content for consistent hashing.

    Args:
        content: The raw Markdown content string.

    Returns:
        The normalized Markdown content string.
    """
    if not isinstance(content, str):
        raise TypeError("Input content must be a string.")

    # 1. Normalize line endings to LF
    content = re.sub(r'\r\n|\r', '\n', content)

    # 2. Normalize Unicode to NFC form
    content = unicodedata.normalize('NFC', content)

    # 3. Process lines: Trim whitespace from each, reduce blank lines
    lines = content.split('\n')
    normalized_lines = []
    in_blank_sequence = False
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line: # It's a blank line
            if not in_blank_sequence:
                normalized_lines.append("") # Add one blank line
                in_blank_sequence = True
        else:
            # Add the line *after* stripping leading/trailing whitespace
            normalized_lines.append(stripped_line) 
            in_blank_sequence = False

    # 4. Join lines back
    content_processed_lines = '\n'.join(normalized_lines)

    # 5. Trim leading/trailing whitespace from the entire result *only*
    # This handles potential blank lines at the very start/end after processing
    final_content = content_processed_lines.strip()

    return final_content


def _sort_dict_recursively(d):
    """Helper function to recursively sort dictionaries by key."""
    if isinstance(d, Mapping):
        return {k: _sort_dict_recursively(v) for k, v in sorted(d.items())}
    elif isinstance(d, list):
        # Also sort items within lists if they are mappings
        return [_sort_dict_recursively(item) for item in d]
    else:
        return d

def normalize_yaml_frontmatter(frontmatter: dict) -> dict:
    """Normalizes YAML frontmatter dictionary for consistent hashing by sorting keys.

    Args:
        frontmatter: The YAML frontmatter as a Python dictionary.

    Returns:
        A new dictionary with all keys recursively sorted.
    """
    if not isinstance(frontmatter, Mapping):
        # Or raise an error, depending on desired strictness
        return frontmatter
    return _sort_dict_recursively(frontmatter)


def calculate_content_hash(markdown_content: str) -> str:
    """Calculates the SHA-256 hash of normalized Markdown content.

    Args:
        markdown_content: The raw Markdown content string.

    Returns:
        The hexadecimal SHA-256 hash digest.
    """
    # 1. Normalize the content
    normalized_content = normalize_markdown_content(markdown_content)

    # 2. Encode the normalized string to bytes (UTF-8 is standard)
    content_bytes = normalized_content.encode('utf-8')

    # 3. Calculate SHA-256 hash
    hash_object = hashlib.sha256(content_bytes)

    # 4. Return the hexadecimal representation of the hash
    return hash_object.hexdigest()

# Placeholder/Example for YAML normalization (from Subtask 5.5)
def normalize_yaml(data: dict) -> str:
    """Placeholder/Example: Normalize a dictionary to a consistent YAML representation."""
    # Simple sort keys for consistency
    return yaml.dump(data, sort_keys=True) 