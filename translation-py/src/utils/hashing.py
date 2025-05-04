import hashlib
import copy
# Assuming normalize_yaml is in a sibling file - uncommenting now
# This import should work correctly once normalize_yaml is implemented
# in the expected location (likely src/utils/yaml_utils.py or normalization.py)
from .yaml_utils import normalize_yaml 

TECHNICAL_FIELDS = {'content_hash', 'yaml_hash', 'lang', 'path', 'url', 'last_updated'}

def calculate_yaml_hash(frontmatter: dict) -> str | None:
    """
    Calculates the SHA-256 hash of normalized YAML frontmatter, excluding technical fields.

    Args:
        frontmatter: A dictionary representing the YAML frontmatter.

    Returns:
        The hexadecimal SHA-256 hash digest, or None if input is invalid.
        
    Raises:
        TypeError: If input is not a dictionary.
        ImportError: If yaml_utils or normalize_yaml cannot be found.
    """
    if not isinstance(frontmatter, dict):
        raise TypeError("Input frontmatter must be a dictionary.")

    # Create a deep copy to avoid modifying the original dictionary
    fm_copy = copy.deepcopy(frontmatter)

    # Filter out technical fields
    filtered_fm = {k: v for k, v in fm_copy.items() if k not in TECHNICAL_FIELDS}

    # Normalize the filtered YAML content
    # This relies on normalize_yaml being implemented correctly in yaml_utils.py
    try:
        # We need to ensure the actual normalize_yaml function is available
        # Assuming it's in yaml_utils.py as per previous steps
        normalized_yaml_str = normalize_yaml(filtered_fm) 
    except NameError: # Should be caught by ImportError on module load, but belt-and-suspenders
        print("Error: normalize_yaml function not found. Make sure yaml_utils.py is present and correct.")
        raise ImportError("normalize_yaml function not found.")
        
    if normalized_yaml_str is None: # Handle case where normalize_yaml might return None
        # Decide on behavior: return None, empty hash, or raise error?
        # Returning hash of empty string might be safest default.
        normalized_yaml_str = ""

    # Calculate SHA-256 hash
    hash_object = hashlib.sha256(normalized_yaml_str.encode('utf-8'))
    hex_dig = hash_object.hexdigest()

    return hex_dig 