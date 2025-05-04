import pytest
import hashlib
# Adjust import based on running tests from root or translation-py dir
# Assuming tests run via `python -m pytest translation-py/tests`
from src.utils.hashing import calculate_yaml_hash, TECHNICAL_FIELDS

# Placeholder/Example normalize_yaml for testing if the real one isn't easily importable yet
# In a real scenario, ensure the actual normalize_yaml is used.
import yaml
def normalize_yaml(data: dict) -> str:
    """Placeholder: Sorts keys and dumps to string. Used for testing calculate_yaml_hash."""
    return yaml.dump(data, sort_keys=True, allow_unicode=True)

def test_calculate_yaml_hash_excludes_technical_fields():
    """Verify that technical fields are excluded before hashing."""
    frontmatter = {
        'title': 'Test Document',
        'date': '2023-01-01',
        'content_hash': 'abc123',  # Should be excluded
        'yaml_hash': 'def456',     # Should be excluded
        'lang': 'en',               # Should be excluded
        'path': '/path/to/doc',    # Should be excluded
        'author': 'Test Author'
    }
    
    expected_input_to_normalize = {
        'title': 'Test Document',
        'date': '2023-01-01',
        'author': 'Test Author'
    }
    
    # Use the placeholder normalize_yaml defined in this file
    normalized_str = normalize_yaml(expected_input_to_normalize)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    # Test the actual function (expect failure due to stub)
    assert calculate_yaml_hash(frontmatter) == expected_hash
    # assert calculate_yaml_hash(frontmatter) is None 

def test_calculate_yaml_hash_order_independence():
    """Verify hash is consistent regardless of initial field order."""
    frontmatter1 = {'title': 'Test', 'author': 'John', 'date': '2023-01-01'}
    frontmatter2 = {'date': '2023-01-01', 'title': 'Test', 'author': 'John'}
    
    # Test the actual function (expect failure due to stub)
    hash1 = calculate_yaml_hash(frontmatter1)
    hash2 = calculate_yaml_hash(frontmatter2)
    assert hash1 is not None # Will fail first
    assert hash1 == hash2
    # assert calculate_yaml_hash(frontmatter1) is None
    # assert calculate_yaml_hash(frontmatter2) is None

def test_calculate_yaml_hash_no_technical_fields():
    """Verify hashing works correctly when no technical fields are present."""
    frontmatter = {
        'title': 'Another Test',
        'category': 'Examples'
    }
    # Use the placeholder normalize_yaml defined in this file
    normalized_str = normalize_yaml(frontmatter)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    # Test the actual function (expect failure due to stub)
    assert calculate_yaml_hash(frontmatter) == expected_hash
    # assert calculate_yaml_hash(frontmatter) is None

def test_calculate_yaml_hash_empty_input():
    """Verify behavior with empty input dictionary."""
    frontmatter = {}
    # Use the placeholder normalize_yaml defined in this file
    normalized_str = normalize_yaml(frontmatter)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    # Test the actual function (expect failure due to stub)
    assert calculate_yaml_hash(frontmatter) == expected_hash
    # assert calculate_yaml_hash(frontmatter) is None

# Potential edge case: Input is not a dictionary (should ideally raise TypeError or handle gracefully)
def test_calculate_yaml_hash_invalid_input():
    """Verify function handles non-dict input gracefully."""
    with pytest.raises(TypeError): # Or specific custom error
        calculate_yaml_hash("not a dict") # This should fail until type check implemented 