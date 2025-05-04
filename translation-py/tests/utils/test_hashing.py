import pytest
import hashlib
from typing import Dict, Any, Set
from unittest.mock import patch

# Assuming src is in PYTHONPATH or project is structured correctly for imports
# This might need adjustment if tests run from within translation-py
from src.utils.hashing import calculate_yaml_hash, TECHNICAL_FIELDS

# Mock implementation of normalize_yaml for testing purposes
# In a real scenario, this would import from yaml_utils or use a library
def mock_normalize_yaml(data: Dict[str, Any]) -> str:
    """Mock normalization: Sorts keys and converts to a simple string representation."""
    if not data:
        return "{}"
    # Simple string conversion, sorting keys for consistency
    items = [f"{k}:{v}" for k, v in sorted(data.items())]
    return "{" + ",".join(items) + "}"

@pytest.fixture
def mock_normalize():
    """Fixture to mock the normalize_yaml function."""
    # Patch the function *where it's looked up* (within the hashing module)
    # This path might also need adjustment depending on test execution context
    with patch('src.utils.hashing.normalize_yaml', side_effect=mock_normalize_yaml) as mock_func:
        yield mock_func

def test_calculate_yaml_hash_excludes_technical_fields(mock_normalize):
    """Verify that standard technical fields are excluded."""
    frontmatter = {
        'title': 'Test Document',
        'date': '2023-01-01',
        'content_hash': 'abc123hash', # Technical
        'yaml_hash': 'def456hash',     # Technical
        'lang': 'en',                 # Technical
        'path': '/path/to/doc',       # Technical
        'url': '/url/to/doc',         # Technical
        'last_updated': 'timestamp',  # Technical
        'custom_field': 'value1'
    }
    
    # Expected input to the (mocked) normalize_yaml function
    expected_normalized_input = {
        'title': 'Test Document',
        'date': '2023-01-01',
        'custom_field': 'value1'
    }
    
    # Calculate expected hash based on the mocked normalization
    normalized_str = mock_normalize_yaml(expected_normalized_input)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    assert calculate_yaml_hash(frontmatter) == expected_hash
    # Verify normalize_yaml was called with the correctly filtered dict
    mock_normalize.assert_called_once_with(expected_normalized_input)

def test_calculate_yaml_hash_order_independence(mock_normalize):
    """Verify hash consistency regardless of initial field order (relies on normalize)."""
    frontmatter1 = {'title': 'Test', 'author': 'John', 'date': '2023-01-01'}
    frontmatter2 = {'date': '2023-01-01', 'author': 'John', 'title': 'Test'}
    # Exclude technical fields just in case they sneak in
    frontmatter3 = {'date': '2023-01-01', 'yaml_hash': 'oldhash', 'author': 'John', 'title': 'Test'} 

    hash1 = calculate_yaml_hash(frontmatter1)
    hash2 = calculate_yaml_hash(frontmatter2)
    hash3 = calculate_yaml_hash(frontmatter3)
    
    assert hash1 == hash2
    assert hash1 == hash3 # Should be the same as it excludes yaml_hash

def test_calculate_yaml_hash_none_input(mock_normalize):
    """Verify handling of None input."""
    expected_hash = hashlib.sha256(b"").hexdigest() # Hash of empty string
    assert calculate_yaml_hash(None) == expected_hash
    mock_normalize.assert_not_called() # Normalize shouldn't be called for None

def test_calculate_yaml_hash_empty_dict(mock_normalize):
    """Verify handling of an empty dictionary."""
    frontmatter = {}
    expected_normalized_input = {}
    normalized_str = mock_normalize_yaml(expected_normalized_input)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    assert calculate_yaml_hash(frontmatter) == expected_hash
    mock_normalize.assert_called_once_with(expected_normalized_input)
    
def test_calculate_yaml_hash_invalid_type():
    """Verify TypeError is raised for non-dict (and non-None) input."""
    with pytest.raises(TypeError, match="Frontmatter must be a dictionary or None"):
        calculate_yaml_hash("this is a string")
        
    with pytest.raises(TypeError, match="Frontmatter must be a dictionary or None"):
        calculate_yaml_hash([1, 2, 3]) # A list

def test_calculate_yaml_hash_additional_exclude_fields(mock_normalize):
    """Verify exclusion of additional fields."""
    frontmatter = {
        'title': 'Test Document',
        'custom_technical': 'tech_value', # To be excluded via additional
        'normal_field': 'value',
        'content_hash': 'abc' # Standard technical
    }
    additional_exclude: Set[str] = {'custom_technical'}
    
    expected_normalized_input = {
        'title': 'Test Document',
        'normal_field': 'value'
    }
    
    normalized_str = mock_normalize_yaml(expected_normalized_input)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()
    
    assert calculate_yaml_hash(frontmatter, additional_exclude_fields=additional_exclude) == expected_hash
    mock_normalize.assert_called_once_with(expected_normalized_input)

def test_calculate_yaml_hash_non_string_keys(mock_normalize):
    """Verify that non-string keys are currently excluded (as per implementation)."""
    frontmatter = {
        'title': 'Test Document',
        123: 'numeric_key_value',
        ('a', 'b'): 'tuple_key_value',
        'normal_field': 'value'
    }
    
    expected_normalized_input = {
        'title': 'Test Document',
        'normal_field': 'value'
    }

    normalized_str = mock_normalize_yaml(expected_normalized_input)
    expected_hash = hashlib.sha256(normalized_str.encode('utf-8')).hexdigest()

    assert calculate_yaml_hash(frontmatter) == expected_hash
    mock_normalize.assert_called_once_with(expected_normalized_input)
    
def test_all_technical_fields_defined():
     """Ensure the TECHNICAL_FIELDS set is not empty and contains expected types."""
     assert isinstance(TECHNICAL_FIELDS, set)
     assert len(TECHNICAL_FIELDS) > 0
     assert all(isinstance(field, str) for field in TECHNICAL_FIELDS)
     # Check a few known fields are present
     assert 'content_hash' in TECHNICAL_FIELDS
     assert 'yaml_hash' in TECHNICAL_FIELDS
     assert 'lang' in TECHNICAL_FIELDS 