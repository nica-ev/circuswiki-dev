from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum

# --- Basic Types (Phase 1 - Python) ---

@dataclass
class NodeBreadcrumb:
    node_type: str
    index: int
    attributes: Optional[Dict[str, Any]] = None

@dataclass
class PositionInfo:
    start_offset: int
    end_offset: int
    node_path: List[str] = field(default_factory=list)
    breadcrumbs: List[NodeBreadcrumb] = field(default_factory=list)

class SegmentType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    LIST_ITEM = 'listItem'
    CODE_BLOCK = 'code'
    INLINE_CODE = 'inlineCode'
    BOLD = 'strong'
    ITALIC = 'emphasis'
    LINK = 'link'
    IMAGE = 'image'
    TEXT = 'text'
    # Add more as needed

@dataclass
class TextSegment:
    id: str
    content: str
    ast_node: Any # Placeholder for the actual AST node type
    segment_type: SegmentType
    position: PositionInfo
    parent_id: Optional[str] = None
    child_ids: List[str] = field(default_factory=list)

class TranslationMap:
    def __init__(self):
        self._segments: Dict[str, TextSegment] = {}
        self._ordered_ids: List[str] = []

    def add_segment(self, segment: TextSegment) -> None:
        """Adds a segment to the map and updates parent if needed."""
        if segment.id in self._segments:
            raise ValueError(f"Segment with ID {segment.id} already exists.")
        self._segments[segment.id] = segment
        self._ordered_ids.append(segment.id)

        # If this segment has a parent, add its ID to the parent's child_ids
        if segment.parent_id:
            parent = self._segments.get(segment.parent_id)
            if parent:
                # Ensure child_ids list exists
                if parent.child_ids is None: # Should not happen with dataclass default_factory
                    parent.child_ids = [] 
                if segment.id not in parent.child_ids:
                    parent.child_ids.append(segment.id)
            # else: Handle case where parent_id is specified but parent doesn't exist yet? 
            #     Or assume parent is always added first. For now, assume parent exists.

    def get_segment(self, id: str) -> Optional[TextSegment]:
        """Retrieves a segment by its ID."""
        # Basic implementation for Phase 1
        return self._segments.get(id)

    def get_all_segments(self) -> List[TextSegment]:
        """Returns all segments in the order they were added."""
        return [self._segments[id] for id in self._ordered_ids if id in self._segments]

    def get_child_segments(self, parent_id: str) -> List[TextSegment]:
        """Returns the direct children of a given parent segment ID."""
        parent = self.get_segment(parent_id)
        if not parent or not parent.child_ids:
            return []
        # Retrieve child segments, filter out any potential misses (shouldn't happen ideally)
        children = [self.get_segment(child_id) for child_id in parent.child_ids]
        return [child for child in children if child is not None]

    def get_nested_segments(self) -> List[TextSegment]:
        """Returns only the top-level segments (those without a parent_id)."""
        return [segment for segment in self.get_all_segments() if segment.parent_id is None]

    # Other methods will be added later 