import pytest
import yaml
# Use relative path import for testing within the subproject
from src.utils.yaml_utils import normalize_yaml

# Expected canonical output format (indent=2, default_flow_style=False)
# Note: PyYAML's dump adds a trailing newline

def test_simple_dict_ordering():
    dict1 = {'b': 2, 'a': 1, 'c': 3}
    dict2 = {'c': 3, 'a': 1, 'b': 2}
    expected_output = """a: 1
b: 2
c: 3
"""
    assert normalize_yaml(dict1) == expected_output
    assert normalize_yaml(dict2) == expected_output

def test_nested_dict_ordering():
    dict1 = {'b': {'y': 2, 'x': 1}, 'a': 0}
    dict2 = {'a': 0, 'b': {'x': 1, 'y': 2}}
    expected_output = """a: 0
b:
  x: 1
  y: 2
"""
    assert normalize_yaml(dict1) == expected_output
    assert normalize_yaml(dict2) == expected_output

def test_dict_with_list():
    # Lists should maintain order, but dicts within lists should be sorted
    data = {
        'c': [3, 1, 2],
        'a': [
            {'y': 2, 'x': 1},
            {'z': 3}
        ]
    }
    expected_output = """a:
- x: 1
  y: 2
- z: 3
c:
- 3
- 1
- 2
"""
    assert normalize_yaml(data) == expected_output

def test_various_data_types():
    data = {
        'string': "hello",
        'integer': 123,
        'float': 45.67,
        'boolean_true': True,
        'boolean_false': False,
        'none_value': None,
        'unicode_string': "你好世界" # Example Unicode
    }
    # Note: yaml.dump handles None as 'null', True/False as 'true'/'false'
    # Updated expectation: Unicode string without quotes, allow_unicode=True behavior
    expected_output = """boolean_false: false
boolean_true: true
float: 45.67
integer: 123
none_value: null
string: hello
unicode_string: 你好世界
"""
    assert normalize_yaml(data) == expected_output

def test_empty_dict():
    data = {}
    # Updated expectation: Include trailing newline added by yaml.dump
    expected_output = "{}\n" # PyYAML outputs {} followed by newline
    assert normalize_yaml(data) == expected_output

def test_dict_with_none_values_as_dict():
    # Test case where a nested value is None, but represented as a dict key
    data = {'a': 1, 'b': None}
    expected_output = """a: 1
b: null
"""
    assert normalize_yaml(data) == expected_output 