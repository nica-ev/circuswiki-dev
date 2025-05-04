import pytest
from src.html_config import HtmlProcessingConfig
import logging

# Basic test configurations
CONFIG_EXTRACT_ALL = {
    'extract_content_tags': ['p', 'div', 'span'],
    'extract_attribute_tags': {'a': ['title'], 'img': ['alt']},
    'preserve_tags': ['code', 'pre'],
    'default_tag_behavior': 'extract' 
}

CONFIG_PRESERVE_ALL = {
    'extract_content_tags': [],
    'extract_attribute_tags': {},
    'preserve_tags': ['p', 'div', 'span', 'a', 'img'],
    'default_tag_behavior': 'preserve'
}

CONFIG_DEFAULT_PRESERVE = {
    'extract_content_tags': ['p'],
    'extract_attribute_tags': {'img': ['alt']},
    'preserve_tags': ['code'],
    'default_tag_behavior': 'preserve' # Default
}

CONFIG_OVERLAP = {
    'extract_content_tags': ['p', 'div'],
    'extract_attribute_tags': {'div': ['title']}, # div also in preserve
    'preserve_tags': ['code', 'div']
}

CONFIG_INVALID_DEFAULT = {
    'default_tag_behavior': 'invalid_option'
}

# --- Tests --- 

def test_config_initialization():
    config = HtmlProcessingConfig(CONFIG_EXTRACT_ALL)
    assert isinstance(config.extract_content_tags, set)
    assert 'p' in config.extract_content_tags
    assert isinstance(config.extract_attribute_tags, dict)
    assert 'a' in config.extract_attribute_tags
    assert isinstance(config.extract_attribute_tags['a'], set)
    assert 'title' in config.extract_attribute_tags['a']
    assert 'code' in config.preserve_tags
    assert config.default_tag_behavior == 'extract'

def test_config_empty_init():
    config = HtmlProcessingConfig({})
    assert config.extract_content_tags == set()
    assert config.extract_attribute_tags == {}
    assert config.preserve_tags == set()
    assert config.default_tag_behavior == 'preserve' # Default behavior

def test_validation_overlap(caplog):
    """Check that preserve takes precedence over extraction rules."""
    caplog.set_level(logging.WARNING)
    config = HtmlProcessingConfig(CONFIG_OVERLAP)
    assert 'div' not in config.extract_content_tags # Should be removed
    assert 'div' not in config.extract_attribute_tags # Should be removed
    assert 'div' in config.preserve_tags # Should remain
    assert 'code' in config.preserve_tags
    assert 'p' in config.extract_content_tags
    assert "overlap" in caplog.text.lower()

def test_validation_invalid_default(caplog):
    """Check that invalid default behavior defaults to preserve."""
    caplog.set_level(logging.WARNING)
    config = HtmlProcessingConfig(CONFIG_INVALID_DEFAULT)
    assert config.default_tag_behavior == 'preserve'
    assert "invalid default_tag_behavior" in caplog.text.lower()

# Tests for helper methods
@pytest.mark.parametrize("config_data, tag, expected", [
    (CONFIG_EXTRACT_ALL, 'p', True),
    (CONFIG_EXTRACT_ALL, 'div', True),
    (CONFIG_EXTRACT_ALL, 'code', False), # Preserved
    (CONFIG_EXTRACT_ALL, 'unknown', True), # Default extract
    (CONFIG_DEFAULT_PRESERVE, 'p', True),
    (CONFIG_DEFAULT_PRESERVE, 'div', False), # Default preserve
    (CONFIG_DEFAULT_PRESERVE, 'code', False), # Preserved
])
def test_should_extract_content(config_data, tag, expected):
    config = HtmlProcessingConfig(config_data)
    assert config.should_extract_content(tag) == expected

@pytest.mark.parametrize("config_data, tag, expected", [
    (CONFIG_EXTRACT_ALL, 'p', False),
    (CONFIG_EXTRACT_ALL, 'code', True),
    (CONFIG_PRESERVE_ALL, 'div', True),
    (CONFIG_PRESERVE_ALL, 'unknown', False),
])
def test_should_preserve_tag(config_data, tag, expected):
    config = HtmlProcessingConfig(config_data)
    assert config.should_preserve_tag(tag) == expected

@pytest.mark.parametrize("config_data, tag, expected_attrs", [
    (CONFIG_EXTRACT_ALL, 'a', {'title'}),
    (CONFIG_EXTRACT_ALL, 'img', {'alt'}), # Note: title not in config
    (CONFIG_EXTRACT_ALL, 'p', set()),
    (CONFIG_EXTRACT_ALL, 'code', set()), # Preserved tag
    (CONFIG_PRESERVE_ALL, 'a', set()), # Preserved tag
    (CONFIG_DEFAULT_PRESERVE, 'img', {'alt'}),
    (CONFIG_DEFAULT_PRESERVE, 'a', set()),
])
def test_get_extractable_attributes(config_data, tag, expected_attrs):
    config = HtmlProcessingConfig(config_data)
    assert config.get_extractable_attributes(tag) == expected_attrs 