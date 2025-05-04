import pytest
from translation_py.src.processing.change_detection import (
    compare_hashes, determine_action, ChangeDetectionResult, ActionType
)

# --- Fixtures ---

@pytest.fixture
def current_hashes():
    return {'content': 'hash_content_v2', 'yaml': 'hash_yaml_v2'}

@pytest.fixture
def frontmatter_v1():
    return {
        'title': 'Old Title',
        'other': 'value',
        '_system': {
            'hashes': {
                'content': 'hash_content_v1',
                'yaml': 'hash_yaml_v1'
            }
        }
    }

@pytest.fixture
def frontmatter_v2_content_changed():
    return {
        'title': 'Old Title',
        'other': 'value',
        '_system': {
            'hashes': {
                'content': 'hash_content_v1', # Content differs from current_hashes
                'yaml': 'hash_yaml_v2'      # YAML matches current_hashes
            }
        }
    }

@pytest.fixture
def frontmatter_v2_yaml_changed():
    return {
        'title': 'New Title', # Assume this changes YAML hash
        'other': 'value',
        '_system': {
            'hashes': {
                'content': 'hash_content_v2', # Content matches current_hashes
                'yaml': 'hash_yaml_v1'      # YAML differs from current_hashes
            }
        }
    }

@pytest.fixture
def frontmatter_v2_no_change():
    return {
        'title': 'New Title',
        'other': 'value',
        '_system': {
            'hashes': {
                'content': 'hash_content_v2', # Matches current_hashes
                'yaml': 'hash_yaml_v2'      # Matches current_hashes
            }
        }
    }

@pytest.fixture
def frontmatter_no_hashes():
    return {
        'title': 'No Hashes Here',
        'other': 'value'
    }

@pytest.fixture
def frontmatter_no_system():
    return {
        'title': 'No System Key',
        'other': 'value'
    }

@pytest.fixture
def frontmatter_empty():
    return {}


# --- Tests for compare_hashes ---

def test_compare_hashes_no_change(current_hashes, frontmatter_v2_no_change):
    result = compare_hashes(current_hashes, frontmatter_v2_no_change)
    assert isinstance(result, ChangeDetectionResult)
    assert not result.content_changed
    assert not result.yaml_changed
    assert result.hashes_match
    assert result.old_hashes == frontmatter_v2_no_change['_system']['hashes']
    assert result.new_hashes == current_hashes

def test_compare_hashes_content_change(current_hashes, frontmatter_v2_content_changed):
    result = compare_hashes(current_hashes, frontmatter_v2_content_changed)
    assert result.content_changed
    assert not result.yaml_changed
    assert not result.hashes_match

def test_compare_hashes_yaml_change(current_hashes, frontmatter_v2_yaml_changed):
    result = compare_hashes(current_hashes, frontmatter_v2_yaml_changed)
    assert not result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match

def test_compare_hashes_both_change(current_hashes, frontmatter_v1):
    result = compare_hashes(current_hashes, frontmatter_v1)
    assert result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match

def test_compare_hashes_no_stored_hashes(current_hashes, frontmatter_no_hashes):
    result = compare_hashes(current_hashes, frontmatter_no_hashes)
    # Missing stored hashes implies change
    assert result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match
    assert result.old_hashes == {}

def test_compare_hashes_no_system_key(current_hashes, frontmatter_no_system):
    result = compare_hashes(current_hashes, frontmatter_no_system)
    assert result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match
    assert result.old_hashes == {}

def test_compare_hashes_empty_frontmatter(current_hashes, frontmatter_empty):
    result = compare_hashes(current_hashes, frontmatter_empty)
    assert result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match
    assert result.old_hashes == {}

def test_compare_hashes_none_frontmatter(current_hashes):
    result = compare_hashes(current_hashes, None)
    assert result.content_changed
    assert result.yaml_changed
    assert not result.hashes_match
    assert result.old_hashes == {}

def test_compare_hashes_missing_one_stored_hash(current_hashes):
    frontmatter = {
        '_system': {
            'hashes': {
                'content': 'hash_content_v2' # YAML hash missing
            }
        }
    }
    result = compare_hashes(current_hashes, frontmatter)
    assert not result.content_changed # Content matches
    assert result.yaml_changed       # Missing YAML implies change
    assert not result.hashes_match

# --- Tests for determine_action ---

def test_determine_action_no_change():
    result = ChangeDetectionResult(content_changed=False, yaml_changed=False)
    action = determine_action(result)
    assert action == ActionType.SKIP

def test_determine_action_content_change():
    result = ChangeDetectionResult(content_changed=True, yaml_changed=False)
    action = determine_action(result)
    assert action == ActionType.FULL_TRANSLATION

def test_determine_action_yaml_change():
    result = ChangeDetectionResult(content_changed=False, yaml_changed=True)
    action = determine_action(result)
    assert action == ActionType.YAML_UPDATE

def test_determine_action_both_change():
    # Content change takes precedence
    result = ChangeDetectionResult(content_changed=True, yaml_changed=True)
    action = determine_action(result)
    assert action == ActionType.FULL_TRANSLATION

# --- Test Logging (Manual Inspection or with caplog fixture) ---

def test_determine_action_logging_skip(caplog):
    result = ChangeDetectionResult(content_changed=False, yaml_changed=False,
                                   new_hashes={'content': 'h1', 'yaml': 'h2'})
    determine_action(result)
    assert "Action: SKIP" in caplog.text
    assert "Reason: Hashes match" in caplog.text
    assert "Content Hash: h1" in caplog.text
    assert "YAML Hash: h2" in caplog.text

def test_determine_action_logging_content_change(caplog):
    result = ChangeDetectionResult(content_changed=True, yaml_changed=False,
                                   old_hashes={'content': 'old_c', 'yaml': 'old_y'},
                                   new_hashes={'content': 'new_c', 'yaml': 'old_y'}) # YAML matches old
    determine_action(result)
    assert "Action: FULL_TRANSLATION" in caplog.text
    assert "Reason: Content hash changed" in caplog.text
    assert "Old Content Hash: old_c" in caplog.text
    assert "New Content Hash: new_c" in caplog.text
    assert "Old YAML Hash: old_y" in caplog.text
    assert "New YAML Hash: old_y" in caplog.text


def test_determine_action_logging_yaml_change(caplog):
    result = ChangeDetectionResult(content_changed=False, yaml_changed=True,
                                   old_hashes={'content': 'old_c', 'yaml': 'old_y'},
                                   new_hashes={'content': 'old_c', 'yaml': 'new_y'}) # Content matches old
    determine_action(result)
    assert "Action: YAML_UPDATE" in caplog.text
    assert "Reason: YAML hash changed, content hash matches" in caplog.text
    assert "Old Content Hash: old_c" in caplog.text
    assert "New Content Hash: old_c" in caplog.text
    assert "Old YAML Hash: old_y" in caplog.text
    assert "New YAML Hash: new_y" in caplog.text 