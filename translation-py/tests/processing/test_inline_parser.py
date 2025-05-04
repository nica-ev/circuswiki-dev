# translation-py/tests/processing/test_inline_parser.py
import pytest
# Use relative import based on running pytest from translation-py directory
from src.processing.inline_parser import InlineParser, InlineToken, InlineTokenType

class TestInlineParser:

    @pytest.fixture
    def parser(self):
        return InlineParser()

    def test_parse_plain_text(self, parser):
        text = "This is plain text."
        tokens = parser.parse(text)
        assert len(tokens) == 1
        assert tokens[0].type == InlineTokenType.TEXT
        assert tokens[0].content == "This is plain text."

    def test_parse_simple_code_span(self, parser):
        text = "Some `code` here."
        tokens = parser.parse(text)
        assert len(tokens) == 3
        assert tokens[0].type == InlineTokenType.TEXT
        assert tokens[0].content == "Some "
        assert tokens[1].type == InlineTokenType.CODE_INLINE
        assert tokens[1].content == "code" # Content inside backticks
        assert tokens[2].type == InlineTokenType.TEXT
        assert tokens[2].content == " here."

    # --- Start with basic, non-nested formatting ---

    # @pytest.mark.skip(reason="Requires state machine for emphasis/strong")
    def test_parse_simple_emphasis(self, parser):
        text = "Some *italic* text."
        tokens = parser.parse(text)
        # Expected: TEXT, EMPHASIS_OPEN, TEXT, EMPHASIS_CLOSE, TEXT
        # Current basic impl might just produce TEXT tokens around the *
        assert len(tokens) == 5, f"Expected 5 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Some "
        assert tokens[1].type == InlineTokenType.EMPHASIS_OPEN
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == "italic"
        assert tokens[3].type == InlineTokenType.EMPHASIS_CLOSE
        assert tokens[4].type == InlineTokenType.TEXT and tokens[4].content == " text."

    # @pytest.mark.skip(reason="Requires state machine for emphasis/strong")
    def test_parse_simple_strong(self, parser):
        text = "Some **bold** text."
        tokens = parser.parse(text)
        # Expected: TEXT, STRONG_OPEN, TEXT, STRONG_CLOSE, TEXT
        # Current basic impl might just produce TEXT tokens around the **
        assert len(tokens) == 5, f"Expected 5 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Some "
        assert tokens[1].type == InlineTokenType.STRONG_OPEN
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == "bold"
        assert tokens[3].type == InlineTokenType.STRONG_CLOSE
        assert tokens[4].type == InlineTokenType.TEXT and tokens[4].content == " text."

    # --- Add more tests incrementally as parser logic evolves --- 

    def test_parse_simple_link(self, parser):
        text = "A [link text](http://example.com) here."
        tokens = parser.parse(text)
        # Expected: TEXT, LINK_OPEN, LINK_TEXT, LINK_CLOSE, LINK_DESTINATION, TEXT
        assert len(tokens) == 6, f"Expected 6 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "A "
        assert tokens[1].type == InlineTokenType.LINK_OPEN and tokens[1].content == "["
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == "link text" # Treat link text as TEXT for now
        assert tokens[3].type == InlineTokenType.LINK_CLOSE and tokens[3].content == "]"
        assert tokens[4].type == InlineTokenType.LINK_DESTINATION and tokens[4].content == "http://example.com"
        assert tokens[5].type == InlineTokenType.TEXT and tokens[5].content == " here."

    def test_parse_link_with_title(self, parser):
        text = "[link](url \"title\")"
        tokens = parser.parse(text)
        # Expected: LINK_OPEN, LINK_TEXT, LINK_CLOSE, LINK_DESTINATION, LINK_TITLE
        assert len(tokens) == 5, f"Expected 5 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.LINK_OPEN
        assert tokens[1].type == InlineTokenType.TEXT and tokens[1].content == "link"
        assert tokens[2].type == InlineTokenType.LINK_CLOSE
        assert tokens[3].type == InlineTokenType.LINK_DESTINATION and tokens[3].content == "url"
        assert tokens[4].type == InlineTokenType.LINK_TITLE and tokens[4].content == "title"

    # --- Tests for Images, WikiLinks, Attributes, Nesting etc. to follow ---

    def test_parse_simple_image(self, parser):
        text = "An ![alt text](image.png) here."
        tokens = parser.parse(text)
        # Expected: TEXT, IMAGE_OPEN, IMAGE_ALT (as TEXT?), IMAGE_CLOSE, LINK_DESTINATION, TEXT
        assert len(tokens) == 6, f"Expected 6 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "An "
        assert tokens[1].type == InlineTokenType.IMAGE_OPEN and tokens[1].content == "!["
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == "alt text" # Treat alt text as TEXT
        assert tokens[3].type == InlineTokenType.IMAGE_CLOSE and tokens[3].content == "]"
        assert tokens[4].type == InlineTokenType.LINK_DESTINATION and tokens[4].content == "image.png"
        assert tokens[5].type == InlineTokenType.TEXT and tokens[5].content == " here."

    def test_parse_image_with_title(self, parser):
        text = "![alt](path/img.jpg \"Image Title\")"
        tokens = parser.parse(text)
        # Expected: IMAGE_OPEN, IMAGE_ALT (as TEXT?), IMAGE_CLOSE, LINK_DESTINATION, LINK_TITLE
        assert len(tokens) == 5, f"Expected 5 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.IMAGE_OPEN
        assert tokens[1].type == InlineTokenType.TEXT and tokens[1].content == "alt"
        assert tokens[2].type == InlineTokenType.IMAGE_CLOSE
        assert tokens[3].type == InlineTokenType.LINK_DESTINATION and tokens[3].content == "path/img.jpg"
        assert tokens[4].type == InlineTokenType.LINK_TITLE and tokens[4].content == "Image Title"

    def test_parse_wikilink_simple(self, parser):
        text = "Link to [[Target Page]]."
        tokens = parser.parse(text)
        # Expected: TEXT, WIKILINK_OPEN, WIKILINK_TARGET, WIKILINK_CLOSE, TEXT
        assert len(tokens) == 5, f"Expected 5 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Link to "
        assert tokens[1].type == InlineTokenType.WIKILINK_OPEN and tokens[1].content == "[["
        assert tokens[2].type == InlineTokenType.WIKILINK_TARGET and tokens[2].content == "Target Page"
        assert tokens[3].type == InlineTokenType.WIKILINK_CLOSE and tokens[3].content == "]]"
        assert tokens[4].type == InlineTokenType.TEXT and tokens[4].content == "."

    def test_parse_wikilink_with_alias(self, parser):
        text = "Another [[Real Target|Alias Text]]."
        tokens = parser.parse(text)
        # Expected: TEXT, WIKILINK_OPEN, WIKILINK_TARGET, WIKILINK_SEPARATOR, WIKILINK_ALIAS, WIKILINK_CLOSE, TEXT
        assert len(tokens) == 7, f"Expected 7 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Another "
        assert tokens[1].type == InlineTokenType.WIKILINK_OPEN
        assert tokens[2].type == InlineTokenType.WIKILINK_TARGET and tokens[2].content == "Real Target"
        assert tokens[3].type == InlineTokenType.WIKILINK_SEPARATOR and tokens[3].content == "|"
        assert tokens[4].type == InlineTokenType.WIKILINK_ALIAS and tokens[4].content == "Alias Text"
        assert tokens[5].type == InlineTokenType.WIKILINK_CLOSE
        assert tokens[6].type == InlineTokenType.TEXT and tokens[6].content == "."

    def test_parse_attribute_simple(self, parser):
        text = "Text with { .class } attribute."
        tokens = parser.parse(text)
        # Expected: TEXT, ATTRIBUTE, TEXT
        assert len(tokens) == 3, f"Expected 3 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Text with "
        # For now, ATTRIBUTE token contains the raw inner content
        assert tokens[1].type == InlineTokenType.ATTRIBUTE and tokens[1].content == " .class "
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == " attribute."

    def test_parse_attribute_key_value(self, parser):
        text = "Another { key=value name=\"quoted name\" } example."
        tokens = parser.parse(text)
        assert len(tokens) == 3, f"Expected 3 tokens, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Another "
        assert tokens[1].type == InlineTokenType.ATTRIBUTE and tokens[1].content == " key=value name=\"quoted name\" "
        assert tokens[2].type == InlineTokenType.TEXT and tokens[2].content == " example."

    def test_parse_attribute_escaped_braces(self, parser):
        text = "Text with \\{escaped\\} content."
        tokens = parser.parse(text)
        # Expected: TEXT token containing the literal brace
        assert len(tokens) == 1, f"Expected 1 token, got {len(tokens)}: {tokens}"
        assert tokens[0].type == InlineTokenType.TEXT and tokens[0].content == "Text with {escaped} content."

