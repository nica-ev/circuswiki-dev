# translation-py/tests/processing/test_markdown_processor.py

import pytest
from src.processing.markdown_processor import MarkdownProcessor, TextSegment, TranslationMap

# Helper function to check if a segment with specific text/type exists
def has_segment(segments, text, seg_type):
    for segment in segments:
        if segment.text == text and segment.type == seg_type:
            return True
    return False

# Helper function to count segments of a specific type
def count_segments(segments, seg_type):
    count = 0
    for segment in segments:
        if segment.type == seg_type:
            count += 1
    return count

# Helper to check if a segment containing text exists
def has_text(segments, text):
    for segment in segments:
        if text in segment.text:
            return True
    return False

class TestMarkdownProcessorBlockElements:

    @pytest.fixture
    def processor(self):
        return MarkdownProcessor()

    def test_extract_simple_paragraphs(self, processor):
        markdown = 'This is the first paragraph.\n\nAnd this is the second.'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'This is the first paragraph.', 'paragraph')
        assert has_segment(segments, 'And this is the second.', 'paragraph')
        assert count_segments(segments, 'paragraph') == 2
        assert len(segments) == 2 # Assuming only paragraphs are extracted for now

    def test_extract_headings_h1_h6(self, processor):
        markdown = '# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'H1', 'heading_1') # Use underscore per markdown-it types
        assert has_segment(segments, 'H2', 'heading_2')
        assert has_segment(segments, 'H3', 'heading_3')
        assert has_segment(segments, 'H4', 'heading_4')
        assert has_segment(segments, 'H5', 'heading_5')
        assert has_segment(segments, 'H6', 'heading_6')
        assert sum(1 for s in segments if s.type.startswith('heading_')) == 6
        assert len(segments) == 6 # Assuming only headings are extracted

    def test_extract_simple_unordered_list_items(self, processor):
        markdown = '- Item 1\n- Item 2\n* Item 3'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        # Expect paragraphs inside list items for simple cases
        assert has_segment(segments, 'Item 1', 'paragraph_in_list') 
        assert has_segment(segments, 'Item 2', 'paragraph_in_list')
        assert has_segment(segments, 'Item 3', 'paragraph_in_list')
        assert count_segments(segments, 'paragraph_in_list') == 3
        assert len(segments) == 3

    def test_extract_simple_ordered_list_items(self, processor):
        markdown = '1. First\n2. Second\n3. Third'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'First', 'paragraph_in_list')
        assert has_segment(segments, 'Second', 'paragraph_in_list')
        assert has_segment(segments, 'Third', 'paragraph_in_list')
        assert count_segments(segments, 'paragraph_in_list') == 3
        assert len(segments) == 3

    def test_extract_simple_blockquotes(self, processor):
        markdown = '> This is a quote.'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        # Blockquotes usually wrap paragraphs
        assert has_segment(segments, 'This is a quote.', 'paragraph_in_blockquote') # Assuming specific type
        assert count_segments(segments, 'paragraph_in_blockquote') == 1
        assert len(segments) == 1

    def test_handle_nested_lists(self, processor):
        markdown = '- Level 1\n  - Level 2\n    - Level 3'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        # Nested items are also likely paragraphs within list items
        assert has_segment(segments, 'Level 1', 'paragraph_in_list') 
        assert has_segment(segments, 'Level 2', 'paragraph_in_list')
        assert has_segment(segments, 'Level 3', 'paragraph_in_list')
        assert count_segments(segments, 'paragraph_in_list') == 3
        assert len(segments) == 3

    def test_handle_nested_blockquotes(self, processor):
        markdown = '> Outer\n>\n> > Inner'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'Outer', 'paragraph_in_blockquote')
        assert has_segment(segments, 'Inner', 'paragraph_in_blockquote') # Nested might need specific handling/path
        assert count_segments(segments, 'paragraph_in_blockquote') == 2
        assert len(segments) == 2

    def test_skip_code_blocks_entirely(self, processor):
        markdown = 'Paragraph before.\n\n```javascript\nconst code = "should be ignored";\nconsole.log(code);\n```\n\nParagraph after.'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'Paragraph before.', 'paragraph')
        assert has_segment(segments, 'Paragraph after.', 'paragraph')
        assert len(segments) == 2 # Only the two paragraphs
        assert not has_text(segments, 'should be ignored')

    def test_handle_paragraphs_within_list_items(self, processor):
        markdown = '- List item 1, first para.\n\n  List item 1, second para.\n- List item 2.'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        # Now explicitly expect paragraph_in_list type
        assert has_segment(segments, 'List item 1, first para.', 'paragraph_in_list') 
        assert has_segment(segments, 'List item 1, second para.', 'paragraph_in_list')
        assert has_segment(segments, 'List item 2.', 'paragraph_in_list') # Also a paragraph in list item
        assert len(segments) == 3 

    def test_handle_mixed_content_correctly(self, processor):
        markdown = '# Title\n\nFirst paragraph.\n\n- List item 1\n- List item 2\n\n> A blockquote here.\n\n```python\n# ignored code\nprint("hello")\n```\n\nFinal paragraph.'
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        expected_texts = [
            ('Title', 'heading_1'),
            ('First paragraph.', 'paragraph'),
            ('List item 1', 'paragraph_in_list'), # Adjusted expected type
            ('List item 2', 'paragraph_in_list'), # Adjusted expected type
            ('A blockquote here.', 'paragraph_in_blockquote'),
            ('Final paragraph.', 'paragraph')
        ]
        assert len(segments) == len(expected_texts) # Should now be 6
        for text, seg_type in expected_texts:
            assert has_segment(segments, text, seg_type)
        assert not has_text(segments, 'ignored code')
        assert not has_text(segments, 'print("hello")') 