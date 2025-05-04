import hashlib
from typing import Dict, Any, Optional, Set
# Assuming yaml_utils.py exists in the same directory and has normalize_yaml
# This will be resolved when subtask 5.1 is completed.
# For now, ensure a placeholder exists or subtask 5.1 is done.
from .yaml_utils import normalize_yaml 

# Define technical fields that should be excluded from hash calculation
TECHNICAL_FIELDS: Set[str] = {'content_hash', 'yaml_hash', 'lang', 'path', 'url', 'last_updated'}

def calculate_content_hash(content: str) -> str:
    """
    Calculate SHA-256 hash for the given content string.
    
    Args:
        content: The string content to hash.
        
    Returns:
        Hexadecimal digest of SHA-256 hash.
    """
    if content is None:
        content = "" # Treat None as empty string for hashing
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def calculate_yaml_hash(frontmatter: Optional[Dict[str, Any]],
                        additional_exclude_fields: Optional[Set[str]] = None) -> str:
    """
    Calculate SHA-256 hash for normalized YAML frontmatter, excluding technical fields.
    
    Args:
        frontmatter: Dictionary containing frontmatter fields. Can be None.
        additional_exclude_fields: Optional set of additional fields to exclude.
        
    Returns:
        Hexadecimal digest of SHA-256 hash. Returns hash of empty string if frontmatter is None.
        
    Raises:
        TypeError: If frontmatter is not a dictionary (and not None).
    """
    if frontmatter is None:
        # Consistent hashing for None input
        return hashlib.sha256(b"").hexdigest() 
        
    if not isinstance(frontmatter, dict):
        raise TypeError("Frontmatter must be a dictionary or None")
    
    # Determine fields to exclude
    exclude_fields = TECHNICAL_FIELDS.copy()
    if additional_exclude_fields:
        # Ensure additional_exclude_fields is treated as a set
        if isinstance(additional_exclude_fields, set):
             exclude_fields.update(additional_exclude_fields)
        else:
            # Attempt to convert if iterable, otherwise raise error or warning?
            # For simplicity, let's assume it's provided as a set if not None.
            # Consider adding more robust type checking if needed.
             pass # Or log a warning

    # Create filtered copy of frontmatter, handling potential non-string keys gracefully
    filtered_frontmatter = {}
    for k, v in frontmatter.items():
        if isinstance(k, str) and k not in exclude_fields:
            filtered_frontmatter[k] = v
        elif not isinstance(k, str):
             # Decide how to handle non-string keys: include, exclude, raise error?
             # For now, excluding non-string keys to avoid normalization issues.
             pass # Or log a warning
             
    # Normalize and hash
    # Ensure normalize_yaml handles empty dict correctly
    normalized_yaml_str = normalize_yaml(filtered_frontmatter) 
    return hashlib.sha256(normalized_yaml_str.encode('utf-8')).hexdigest()

# Example usage (optional, for testing)
# if __name__ == '__main__':
#     test_fm = {'title': 'Test Doc', 'author': 'Me', 'content_hash': 'abc', 'lang': 'en'}
#     print(f"Technical Fields: {TECHNICAL_FIELDS}")
#     yaml_hash = calculate_yaml_hash(test_fm)
#     print(f"YAML Hash: {yaml_hash}")

#     test_fm_none = None
#     yaml_hash_none = calculate_yaml_hash(test_fm_none)
#     print(f"YAML Hash for None: {yaml_hash_none}")
    
#     try:
#         calculate_yaml_hash("not a dict")
#     except TypeError as e:
#         print(f"Caught expected error: {e}") 