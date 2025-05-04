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
    # 1. Normalize line endings to LF (\n)
    content_lf = re.sub(r'\r\n|\r', '\n', content)

    # 2. Reduce multiple blank lines (more than two consecutive \n) to a single blank line (two \n)
    # Operate on content_lf before stripping lines
    content_reduced_blanks = re.sub(r'\n{3,}', '\n\n', content_lf)

    # 3. Trim leading/trailing whitespace from each line
    lines = content_reduced_blanks.split('\n')
    stripped_lines = [line.strip() for line in lines]
    # Remove potential fully blank lines resulting from stripping lines containing only whitespace
    non_blank_lines = [line for line in stripped_lines if line]
    content_stripped = '\n'.join(non_blank_lines)

    # 4. Normalize Unicode characters to NFC form
    normalized_content = unicodedata.normalize('NFC', content_stripped)

    return normalized_content


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