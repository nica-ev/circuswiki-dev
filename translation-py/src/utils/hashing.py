import hashlib
from typing import Dict, Any, Optional, Set
# Attempt to import the real normalization function, fallback to placeholder if needed
try:
    from .yaml_utils import normalize_yaml
except ImportError:
    # Placeholder if yaml_utils is not yet available
    import yaml
    def normalize_yaml(data):
        return yaml.dump(data, sort_keys=True)

# Define technical fields that should be excluded from hash calculation
TECHNICAL_FIELDS: Set[str] = {'content_hash', 'yaml_hash', 'lang', 'path', 'url', 'last_updated'}


def calculate_content_hash(markdown_content: str) -> str:
    """
    Calculate SHA-256 hash for normalized Markdown content.
    # ... (rest of docstring) ...
    """
    # ... (implementation remains the same) ...
    if not isinstance(markdown_content, str):
        raise TypeError("Input must be a string")

    # Normalize the content first
    # Assumes normalize_markdown_content exists in normalization.py
    from .normalization import normalize_markdown_content
    normalized_content = normalize_markdown_content(markdown_content)

    # Create hash object and update with UTF-8 encoded content
    hash_obj = hashlib.sha256()
    hash_obj.update(normalized_content.encode('utf-8'))

    # Return hexadecimal representation
    return hash_obj.hexdigest()

def calculate_yaml_hash(frontmatter: Optional[Dict[str, Any]],
                        additional_exclude_fields: Optional[Set[str]] = None) -> str:
    """
    Calculate SHA-256 hash for normalized YAML frontmatter, excluding technical fields.

    Args:
        frontmatter: Dictionary containing frontmatter fields or None.
        additional_exclude_fields: Optional set of additional fields to exclude.

    Returns:
        Hexadecimal digest of SHA-256 hash.

    Raises:
        TypeError: If frontmatter is not a dictionary or None.
    """
    # Handle None input explicitly
    if frontmatter is None:
        return hashlib.sha256(b"").hexdigest() # Return hash of empty string for None

    # Check if it's a dictionary
    if not isinstance(frontmatter, dict):
        # Match the expected error message from the test
        raise TypeError("Frontmatter must be a dictionary or None")

    # Determine fields to exclude
    exclude_fields = TECHNICAL_FIELDS.copy()
    if additional_exclude_fields:
        exclude_fields.update(additional_exclude_fields)

    # Create filtered copy of frontmatter, ONLY including string keys
    filtered_fm = {
        k: v for k, v in frontmatter.items()
        if isinstance(k, str) and k not in exclude_fields
    }

    # Normalize and hash
    normalized_yaml_str = normalize_yaml(filtered_fm)
    return hashlib.sha256(normalized_yaml_str.encode('utf-8')).hexdigest() 