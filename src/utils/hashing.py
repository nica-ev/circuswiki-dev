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

def compare_hashes(old_hashes: Optional[Dict[str, str]], 
                   new_hashes: Dict[str, str]) -> Dict[str, bool]:
    """
    Compare old and new hashes to detect changes.

    Args:
        old_hashes: Dictionary with stored 'content_hash' and 'yaml_hash' keys, or None if none stored.
        new_hashes: Dictionary with newly calculated 'content_hash' and 'yaml_hash' keys.

    Returns:
        Dictionary with 'content_changed' and 'yaml_changed' boolean flags.
    """
    # Handle first-run scenario or missing old hashes
    if not old_hashes:
        # If no old hashes, assume change if new hashes exist
        content_changed = bool(new_hashes.get('content_hash'))
        yaml_changed = bool(new_hashes.get('yaml_hash'))
        return {'content_changed': content_changed, 'yaml_changed': yaml_changed}

    # Compare content hash
    content_changed = old_hashes.get('content_hash') != new_hashes.get('content_hash')
    
    # Compare yaml hash
    yaml_changed = old_hashes.get('yaml_hash') != new_hashes.get('yaml_hash')
    
    return {'content_changed': content_changed, 'yaml_changed': yaml_changed}

def process_document_and_get_hashes(content: str, 
                                    frontmatter: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Placeholder demonstrating hash calculation and in-memory storage integration.
    
    Args:
        content: The main body content of the document.
        frontmatter: The YAML frontmatter dictionary (can be None).

    Returns:
        The potentially modified frontmatter dictionary including the calculated hashes.
        Returns an empty dictionary if input frontmatter was None and content was empty.
    """
    # Calculate new hashes
    new_content_hash = calculate_content_hash(content)
    new_yaml_hash = calculate_yaml_hash(frontmatter) # Handles None frontmatter

    # Simulate storing hashes in frontmatter (in-memory)
    updated_frontmatter = {}
    if frontmatter is not None:
         # Use deepcopy if modifying frontmatter in place is not desired downstream
         # For now, let's modify a copy
         updated_frontmatter = frontmatter.copy() 
         
    # Add/update hashes in the frontmatter dictionary
    # We might use a nested structure like _system.hashes later, but flat for now.
    updated_frontmatter['content_hash'] = new_content_hash
    updated_frontmatter['yaml_hash'] = new_yaml_hash
    
    # In a real workflow, you might compare with old hashes here
    # old_hashes = {'content_hash': frontmatter.get('content_hash'), 
    #               'yaml_hash': frontmatter.get('yaml_hash')} # Extract potentially existing hashes
    # changes = compare_hashes(old_hashes, {'content_hash': new_content_hash, 'yaml_hash': new_yaml_hash})
    # print(f"Detected changes: {changes}") # Example logging

    return updated_frontmatter

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

#     # Example for compare_hashes
#     old = {'content_hash': 'abc', 'yaml_hash': 'def'}
#     new = {'content_hash': 'abc', 'yaml_hash': 'xyz'}
#     print(f"Compare (YAML change): {compare_hashes(old, new)}")
#     print(f"Compare (No change): {compare_hashes(old, old)}")
#     print(f"Compare (Content change): {compare_hashes(old, {'content_hash': '123', 'yaml_hash': 'def'})}")
#     print(f"Compare (Initial): {compare_hashes(None, new)}")
    
#     # Example for process_document_and_get_hashes
#     sample_content = "This is the main content.\\nIt has two lines."
#     sample_fm = {'title': 'Test Doc', 'author': 'Me'}
#     processed_fm = process_document_and_get_hashes(sample_content, sample_fm)
#     print(f"Processed Frontmatter: {processed_fm}")
    
#     processed_fm_no_fm = process_document_and_get_hashes(sample_content, None)
#     print(f"Processed with None FM: {processed_fm_no_fm}")

#     processed_fm_no_content = process_document_and_get_hashes("", {'title': 'Empty Content'})
#     print(f"Processed with Empty Content: {processed_fm_no_content}") 