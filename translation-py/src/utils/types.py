from typing import List, Optional
from enum import Enum # Import Enum

# Define SegmentType Enum
class SegmentType(Enum):
    TEXT = "text"                     # Plain text within standard Markdown blocks
    YAML = "yaml"                     # Text from YAML frontmatter field
    HTML_CONTENT = "html_content"     # Text content within an HTML tag
    HTML_ATTRIBUTE = "html_attribute" # Text content of an HTML tag attribute
    IMAGE_ALT = "image_alt"           # Alt text of an image
    WIKILINK_ALIAS = "wikilink_alias" # Alias part of an Obsidian-style wikilink

class TextSegment:
    """Represents a segment of translatable text and its context."""
    def __init__(self, text: str, segment_type: SegmentType, path: str):
        self.text: str = text
        self.type: SegmentType = segment_type 
        self.path: str = path      # Identifier for location (e.g., token path)
        # Add other fields if needed, like original text, metadata, etc.

    def __repr__(self):
        return f"TextSegment(type='{self.type.value}', path='{self.path}', text='{self.text[:50]}...')"

    def __eq__(self, other):
        # Basic equality check for testing purposes
        if not isinstance(other, TextSegment):
            return NotImplemented
        return (
            self.text == other.text and
            self.type == other.type # Path comparison might be tricky, skip for basic tests?
            # self.path == other.path
        )

class TranslationMap:
    """Stores extracted text segments."""
    def __init__(self):
        self.segments: List[TextSegment] = []

    def addSegment(self, segment: TextSegment):
        """Adds a text segment to the map."""
        self.segments.append(segment)

    def get_segments(self) -> List[TextSegment]:
        """Returns the list of segments."""
        return self.segments

    def __repr__(self):
        return f"TranslationMap(segments=[{len(self.segments)} segments])" 