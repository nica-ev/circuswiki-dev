# translation-py/tests/processing/test_markdown_processor.py

import pytest
from src.processing.markdown_processor import MarkdownProcessor, TextSegment, TranslationMap
from typing import Dict

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

# New class for inline element tests
class TestMarkdownProcessorInlineElements:

    @pytest.fixture
    def processor(self):
        return MarkdownProcessor()

    def test_extract_italic(self, processor):
        markdown = "This has *italic* text."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # The _extract_inline_text helper should concatenate the text
        assert segments[0].text == "This has italic text."

    def test_extract_bold(self, processor):
        markdown = "This has **bold** text."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "This has bold text."

    def test_extract_nested_emphasis(self, processor):
        markdown = "Mixed **bold and *italic*** text."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # markdown-it-py renders <strong><em>, so extracted text is concatenated
        assert segments[0].text == "Mixed bold and italic text."
        
    def test_extract_nested_emphasis_alternative(self, processor):
        markdown = "More ***bold italic*** mixed."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "More bold italic mixed."

    def test_extract_link_text(self, processor):
        markdown = "Here is a [link text](http://example.com)."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # Expecting only the link text to be part of the segment
        assert segments[0].text == "Here is a link text."

    def test_extract_image_alt_text(self, processor):
        markdown = "An image: ![Alt text here](/path/to/image.jpg)"
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # Expecting alt text to be extracted along with surrounding text
        assert segments[0].text == "An image: Alt text here"

    def test_ignore_inline_code(self, processor):
        markdown = "Text with `inline code` should ignore code."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # Expecting inline code content to be excluded
        assert segments[0].text == "Text with should ignore code."

    def test_ignore_link_url(self, processor):
        markdown = "Another [link](http://ignore.this/url)."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Another link."

    def test_ignore_image_src(self, processor):
        markdown = "Image ![alt text](/ignore/this/path.png) source."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Image alt text source."

    def test_mixed_inline_elements(self, processor):
        markdown = "A para with *italic*, **bold**, `code`, [link](url), and ![img alt](src)."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # Expected: text + italic + text + bold + text + (skipped code) + text + link_text + text + img_alt + text
        expected = "A para with italic, bold, , link, and img alt."
        assert segments[0].text == expected

    # --- WikiLink Tests (Subtask 7.7) ---
    
    def test_extract_wikilink_simple_no_alias(self, processor):
        # Decision: Do not extract target if no alias is present.
        markdown = "Link to [[Another Page]]."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Link to ." # Target is not extracted

    def test_extract_wikilink_alias(self, processor):
        markdown = "Link with [[Target Page|Display Alias]]."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Link with Display Alias." # Alias is extracted
        
    def test_extract_wikilink_alias_empty(self, processor):
        # Behavior for empty alias might depend on desired handling/plugin logic
        # Assuming empty alias means extract nothing for now.
        markdown = "Link with [[Target Page|]]."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Link with ." 
        
    def test_wikilink_ignored_in_code(self, processor):
        markdown = "Code `[[ignore this|alias]]` block."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Code block." # Code content ignored
        assert "alias" not in segments[0].text
        
    def test_mixed_content_with_wikilinks(self, processor):
        markdown = "Text, [[Target1|Alias1]], more text, [[Target2]], final."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Text, Alias1, more text, , final." # Only alias extracted

    # --- Attribute Tests (Subtask 7.8) ---
    def test_attribute_block_ignored_simple_class(self, processor):
        markdown = "Text before { .my-class } after text."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Text before after text."

    def test_attribute_block_ignored_key_value(self, processor):
        markdown = "More text { key=value another=\"quoted val\" } here."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "More text here."

    def test_attribute_block_in_code_is_code(self, processor):
        markdown = "This is code `with an { .attribute } inside`."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # The content of code_inline is ignored by the extractor
        assert segments[0].text == "This is code ."

    def test_attribute_block_near_other_inline(self, processor):
        markdown = "Some *italic*{.attr}**bold** text."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Some italicbold text."

    def test_attribute_block_with_escaped_braces_ignored(self, processor):
        # Assuming escaped braces should not trigger attribute parsing
        markdown = "Text with \\{escaped\\} braces."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        # Escaped braces are typically rendered as literal braces by markdown-it
        assert segments[0].text == "Text with {escaped} braces."

    def test_attribute_block_unterminated(self, processor):
        # Expect the unterminated block to be treated as text
        markdown = "Text with an { incomplete attribute."
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert len(segments) == 1
        assert segments[0].type == 'paragraph'
        assert segments[0].text == "Text with an { incomplete attribute."

# New class for table element tests
class TestMarkdownProcessorTableElements:

    @pytest.fixture
    def processor(self):
        return MarkdownProcessor()

    def test_simple_table(self, processor):
        markdown = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'Header 1', 'table_header_cell')
        assert has_segment(segments, 'Header 2', 'table_header_cell')
        assert has_segment(segments, 'Cell 1', 'table_data_cell')
        assert has_segment(segments, 'Cell 2', 'table_data_cell')
        assert has_segment(segments, 'Cell 3', 'table_data_cell')
        assert has_segment(segments, 'Cell 4', 'table_data_cell')
        assert len(segments) == 6
        # Optional: Verify path contains row/col info if implemented
        # e.g., assert segments[0].path.endswith('tr_1 > th_1')

    def test_table_with_inline_formatting(self, processor):
        markdown = """
| Header | Formatted Cell |
|--------|----------------|
| Row 1  | Cell with *italic* and **bold** |
| Row 2  | Cell with `code` and [link](url) |
"""
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'Header', 'table_header_cell')
        assert has_segment(segments, 'Formatted Cell', 'table_header_cell')
        assert has_segment(segments, 'Row 1', 'table_data_cell')
        assert has_segment(segments, 'Cell with italic and bold', 'table_data_cell')
        assert has_segment(segments, 'Row 2', 'table_data_cell')
        # Expecting code ignored, link text extracted
        assert has_segment(segments, 'Cell with and link', 'table_data_cell') 
        assert len(segments) == 6
        assert not has_text(segments, 'code')
        assert not has_text(segments, 'url')

    def test_table_with_empty_cells(self, processor):
        markdown = """
| Col A | Col B |
|-------|-------|
| Data  |       |
|       | Data2 |
"""
        result = processor.extract_translatable_segments(markdown)
        segments = result.segments
        assert has_segment(segments, 'Col A', 'table_header_cell')
        assert has_segment(segments, 'Col B', 'table_header_cell')
        assert has_segment(segments, 'Data', 'table_data_cell')
        assert has_segment(segments, 'Data2', 'table_data_cell')
        # Only 4 segments expected, empty cells should not produce segments
        assert len(segments) == 4 

# New class for reassembly tests
class TestMarkdownProcessorReassembly:

    @pytest.fixture
    def processor(self):
        return MarkdownProcessor()

    def _get_dummy_translations(self, processor: MarkdownProcessor, markdown: str) -> Dict[str, str]:
        """Helper to extract segments and create dummy translations."""
        segments_map = processor.extract_translatable_segments(markdown)
        translations = {}
        for segment in segments_map.segments:
            translations[segment.path] = f"{segment.text}[Translated]"
        return translations

    def test_reassemble_simple_paragraph(self, processor):
        markdown = "This is a simple paragraph."
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        expected = "This is a simple paragraph.[Translated]"
        # Note: Exact output depends heavily on reassembly implementation (e.g., newline handling)
        # We might need to adjust assertion based on how md-it renderer works or our string building.
        # Initial simple assertion:
        assert reassembled.strip() == expected.strip()

    def test_reassemble_headings(self, processor):
        markdown = "# H1\n## H2"
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        expected = "# H1[Translated]\n\n## H2[Translated]"
        assert reassembled.strip() == expected.strip() # Basic check

    def test_reassemble_list_items(self, processor):
        markdown = "- Item 1\n- Item 2"
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        expected = "- Item 1[Translated]\n- Item 2[Translated]"
        # This assumes simple list rendering. Might need adjustment.
        assert reassembled.strip().replace('\n', '') == expected.strip().replace('\n', '') # Looser check for now

    def test_reassemble_blockquote(self, processor):
        markdown = "> This is a quote."
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        expected = "> This is a quote.[Translated]"
        assert reassembled.strip() == expected.strip()

    def test_reassemble_table(self, processor):
        markdown = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        # Expected output might be tricky to get exactly right without running the impl.
        # Focus on ensuring translated text appears.
        assert "Header 1[Translated]" in reassembled
        assert "Header 2[Translated]" in reassembled
        assert "Cell 1[Translated]" in reassembled
        assert "Cell 2[Translated]" in reassembled
        assert "|----------|----------|" in reassembled # Verify structure preserved

    def test_reassemble_inline_formatting(self, processor):
        markdown = "A para with *italic*, **bold**, `code`, [link](url), and ![img alt](src)."
        translations = self._get_dummy_translations(processor, markdown)
        # Expected translation based on extraction rules:
        # Path for "A para with italic, bold, , link, and img alt.": ..._paragraph_open_0
        translations['paragraph_open_0'] = "A para with italic[Translated], bold[Translated], , link[Translated], and img alt[Translated]."
        
        reassembled = processor.reassemble_markdown(markdown, translations)
        
        # We expect the *structure* preserved, but the text content replaced based on the *block* segment
        # (since we aren't doing granular inline reassembly yet)
        # So, bold/italic markers etc. might be gone if we just replace the whole inline content.
        # Let's assert the translated block content is there, and crucially, the non-translatable bits.
        assert "A para with italic[Translated], bold[Translated], , link[Translated], and img alt[Translated]." in reassembled
        assert "`code`" in reassembled # Inline code preserved
        assert "[link](url)" in reassembled # Link structure preserved
        assert "![img alt](src)" in reassembled # Image structure preserved
        # assert "*italic*" not in reassembled # Formatting might be lost with simple inline replacement
        # assert "**bold**" not in reassembled

    def test_reassemble_mixed_content(self, processor):
        markdown = "# Title\n\nPara 1.\n\n- List 1\n\n```python\ncode\n```\n\nPara 2."
        translations = self._get_dummy_translations(processor, markdown)
        reassembled = processor.reassemble_markdown(markdown, translations)
        assert "# Title[Translated]" in reassembled
        assert "Para 1.[Translated]" in reassembled
        assert "- List 1[Translated]" in reassembled # Adjust based on list rendering
        assert "```python\ncode\n```" in reassembled # Code block preserved
        assert "Para 2.[Translated]" in reassembled 