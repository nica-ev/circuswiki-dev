"""
Tests for the MarkdownProcessor class.
"""
import pytest
from markdown_it import MarkdownIt
from src.processing.markdown_processor import MarkdownProcessor
import logging
import yaml

class TestMarkdownProcessor:
    """
    Test suite for the MarkdownProcessor class.
    """

    def test_initialization(self):
        """Test that the processor initializes correctly."""
        processor = MarkdownProcessor()
        assert isinstance(processor, MarkdownProcessor)
        assert isinstance(processor.md, MarkdownIt)
        self.logger.info("MarkdownProcessor initialized successfully in test.") # Added logging

    def test_basic_parsing_returns_ast(self):
        """Test basic parsing returns a non-empty list of tokens."""
        markdown_text = "# Heading\n\nThis is a paragraph."
        processor = MarkdownProcessor()
        ast = processor.parse(markdown_text)
        
        assert isinstance(ast, list)
        assert len(ast) > 0
        # Check for specific token types
        token_types = [token['type'] for token in ast]
        assert 'heading_open' in token_types
        assert 'heading_close' in token_types
        assert 'paragraph_open' in token_types
        assert 'paragraph_close' in token_types
        self.logger.info(f"Basic parsing test successful, got {len(ast)} tokens.") # Added logging

    def test_parse_empty_string(self):
        """Test parsing an empty string returns an empty list."""
        processor = MarkdownProcessor()
        ast = processor.parse("")
        assert isinstance(ast, list)
        assert len(ast) == 0
        self.logger.info("Empty string parsing test successful.") # Added logging

    def test_parse_none_input(self):
        """Test parsing None raises a TypeError."""
        processor = MarkdownProcessor()
        with pytest.raises(TypeError, match="Input text cannot be None"):
            processor.parse(None)
        self.logger.info("None input parsing test successful (raised TypeError).") # Added logging

    # Optional: Add more tests for different markdown features
    def test_parsing_list(self):
        """Test parsing a simple markdown list."""
        markdown_text = "- Item 1\n- Item 2"
        processor = MarkdownProcessor()
        ast = processor.parse(markdown_text)
        assert isinstance(ast, list)
        token_types = [token['type'] for token in ast]
        assert 'bullet_list_open' in token_types
        assert 'list_item_open' in token_types
        assert 'list_item_close' in token_types
        assert 'bullet_list_close' in token_types
        self.logger.info("List parsing test successful.") # Added logging

    def test_parsing_code_block(self):
        """Test parsing a fenced code block."""
        markdown_text = "```python\ndef hello():\n    print(\"Hello\")\n```"
        processor = MarkdownProcessor()
        ast = processor.parse(markdown_text)
        assert isinstance(ast, list)
        token_types = [token['type'] for token in ast]
        assert 'fence' in token_types
        fence_token = next(token for token in ast if token['type'] == 'fence')
        assert fence_token['info'] == 'python'
        assert fence_token['content'] == "def hello():\n    print(\"Hello\")\n"
        self.logger.info("Code block parsing test successful.") # Added logging

    # --- Tests for extract_frontmatter --- 

    def test_extract_frontmatter_valid(self):
        """Test extracting valid YAML frontmatter."""
        processor = MarkdownProcessor()
        markdown_text = "---\ntitle: Test Document\nauthor: John Doe\ndate: 2023-01-01\n---\n# Actual Content\nThis is the body."
        expected_fm = {'title': 'Test Document', 'author': 'John Doe', 'date': '2023-01-01'}
        expected_content = "# Actual Content\nThis is the body."
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("Valid frontmatter extraction test successful.")

    def test_extract_frontmatter_no_frontmatter(self):
        """Test text with no frontmatter."""
        processor = MarkdownProcessor()
        markdown_text = "# Content Only\nNo frontmatter here."
        expected_fm = {}
        expected_content = markdown_text # Original content should be returned
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("No frontmatter extraction test successful.")

    def test_extract_frontmatter_malformed_yaml(self):
        """Test handling of malformed YAML (should return original text)."""
        processor = MarkdownProcessor()
        markdown_text = "---\ntitle: Test: Colon Error \ndate: 2023-01-01\n---\nContent Below"
        expected_fm = {}
        expected_content = markdown_text # Original content on error
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("Malformed YAML extraction test successful.")

    def test_extract_frontmatter_empty_block(self):
        """Test handling of an empty frontmatter block."""
        processor = MarkdownProcessor()
        markdown_text = "---\n---\n# Content Starts Here"
        expected_fm = {}
        expected_content = "# Content Starts Here"
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("Empty frontmatter block test successful.")

    def test_extract_frontmatter_no_close_delimiter(self):
        """Test handling of missing closing delimiter."""
        processor = MarkdownProcessor()
        markdown_text = "---\ntitle: No Close\nActual Content"
        expected_fm = {}
        expected_content = markdown_text # Original content
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("No close delimiter test successful.")

    def test_extract_frontmatter_not_a_dict(self):
        """Test handling when frontmatter parses to non-dict (e.g., list)."""
        processor = MarkdownProcessor()
        markdown_text = "---\n- item1\n- item2\n---\nContent After List"
        expected_fm = {}
        expected_content = markdown_text # Original content
        
        frontmatter, content = processor.extract_frontmatter(markdown_text)
        
        assert frontmatter == expected_fm
        assert content == expected_content
        self.logger.info("Non-dict frontmatter test successful.")

# Add logger initialization for tests (optional but good practice)
logging.basicConfig(level=logging.INFO)
TestMarkdownProcessor.logger = logging.getLogger('TestMarkdownProcessor') 