# Placeholder for segment tests 

import pytest
# Assume root 'src' is on path due to editable install
from src.processing.segments import (
    TextSegment,
    TranslationMap,
    SegmentType,
    PositionInfo,
    NodeBreadcrumb
)

# --- Basic Tests (Phase 1 - Python) ---

@pytest.fixture
def mock_ast_node():
    # Simple mock for AST node placeholder
    return {"type": "paragraph", "content": "mock"}

@pytest.fixture
def basic_position():
    return PositionInfo(start_offset=0, end_offset=10, node_path=[], breadcrumbs=[])

@pytest.fixture
def sample_segment(mock_ast_node, basic_position):
    return TextSegment(
        id="seg1",
        content="Sample text",
        ast_node=mock_ast_node,
        segment_type=SegmentType.PARAGRAPH,
        position=basic_position
    )

def test_text_segment_creation(sample_segment):
    """Test basic TextSegment creation."""
    assert sample_segment.id == "seg1"
    assert sample_segment.content == "Sample text"
    assert sample_segment.segment_type == SegmentType.PARAGRAPH
    assert sample_segment.ast_node == {"type": "paragraph", "content": "mock"}
    assert sample_segment.position.start_offset == 0

def test_translation_map_add_get(sample_segment):
    """Test adding a segment to TranslationMap and retrieving it."""
    trans_map = TranslationMap()
    
    # Before adding, get_segment should return None 
    assert trans_map.get_segment("seg1") is None 
    
    # Add the segment
    trans_map.add_segment(sample_segment)
    
    # After adding, get_segment should return the segment
    assert trans_map.get_segment("seg1") == sample_segment
    assert trans_map.get_segment("nonexistent") is None

def test_position_info_storage(mock_ast_node):
    """Test that complex PositionInfo is stored correctly."""
    breadcrumbs = [
        NodeBreadcrumb(node_type='document', index=0),
        NodeBreadcrumb(node_type='paragraph', index=2, attributes={'class': 'intro'})
    ]
    position = PositionInfo(
        start_offset=45,
        end_offset=62,
        node_path=['0', '2', '0'],
        breadcrumbs=breadcrumbs
    )
    segment = TextSegment(
        id="seg_pos",
        content="Text with position",
        ast_node=mock_ast_node,
        segment_type=SegmentType.TEXT,
        position=position
    )
    
    trans_map = TranslationMap()
    trans_map.add_segment(segment)
    retrieved = trans_map.get_segment("seg_pos")
    
    assert retrieved is not None
    assert retrieved.position.start_offset == 45
    assert retrieved.position.end_offset == 62
    assert retrieved.position.node_path == ['0', '2', '0']
    assert retrieved.position.breadcrumbs == breadcrumbs
    assert retrieved.position.breadcrumbs[1].attributes == {'class': 'intro'}

def test_translation_map_get_all_ordered(sample_segment, mock_ast_node, basic_position):
    """Test that getAllSegments returns segments in insertion order."""
    trans_map = TranslationMap()
    
    segment2 = TextSegment(
        id="seg2", content="Second", ast_node=mock_ast_node, 
        segment_type=SegmentType.TEXT, position=basic_position
    )
    segment3 = TextSegment(
        id="seg3", content="Third", ast_node=mock_ast_node, 
        segment_type=SegmentType.TEXT, position=basic_position
    )
    
    # Add out of order ID-wise
    trans_map.add_segment(sample_segment) # id=seg1
    trans_map.add_segment(segment3)       # id=seg3
    trans_map.add_segment(segment2)       # id=seg2
    
    all_segments = trans_map.get_all_segments() # Needs implementation
    
    assert len(all_segments) == 3
    assert all_segments[0].id == "seg1"
    assert all_segments[1].id == "seg3"
    assert all_segments[2].id == "seg2"

def test_translation_map_nesting(mock_ast_node, basic_position):
    """Test parent-child relationships and retrieval methods."""
    trans_map = TranslationMap()

    parent = TextSegment(
        id="parent1", content="Parent", ast_node=mock_ast_node, 
        segment_type=SegmentType.PARAGRAPH, position=basic_position
    )
    child1 = TextSegment(
        id="child1", content="Child 1", ast_node=mock_ast_node, 
        segment_type=SegmentType.TEXT, position=basic_position, parent_id="parent1"
    )
    child2 = TextSegment(
        id="child2", content="Child 2", ast_node=mock_ast_node, 
        segment_type=SegmentType.TEXT, position=basic_position, parent_id="parent1"
    )
    unrelated = TextSegment(
        id="unrelated", content="Unrelated", ast_node=mock_ast_node, 
        segment_type=SegmentType.PARAGRAPH, position=basic_position
    )
    
    trans_map.add_segment(parent)
    trans_map.add_segment(child1)
    trans_map.add_segment(child2)
    trans_map.add_segment(unrelated)

    # Test get_child_segments (needs implementation)
    child_segments = trans_map.get_child_segments("parent1")
    assert len(child_segments) == 2
    assert child_segments[0].id == "child1"
    assert child_segments[1].id == "child2"
    assert len(trans_map.get_child_segments("child1")) == 0 # Child has no children
    assert len(trans_map.get_child_segments("nonexistent")) == 0

    # Test get_nested_segments (needs implementation)
    nested_segments = trans_map.get_nested_segments()
    assert len(nested_segments) == 2
    assert nested_segments[0].id == "parent1"
    assert nested_segments[1].id == "unrelated"

    # Check if child_ids were added to parent
    retrieved_parent = trans_map.get_segment("parent1")
    assert retrieved_parent is not None
    assert retrieved_parent.child_ids == ["child1", "child2"]

def test_translation_map_duplicate_id(sample_segment):
    """Test that adding a segment with a duplicate ID raises an error."""
    trans_map = TranslationMap()
    trans_map.add_segment(sample_segment) # id="seg1"
    
    duplicate_segment = TextSegment(
        id="seg1", # Same ID
        content="Duplicate content",
        ast_node=sample_segment.ast_node,
        segment_type=SegmentType.TEXT,
        position=sample_segment.position
    )
    
    with pytest.raises(ValueError, match="already exists"):
        trans_map.add_segment(duplicate_segment)