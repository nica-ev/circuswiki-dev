"""
Tests for the MarkdownProcessor class.
"""
import pytest
from markdown_it import MarkdownIt
from src.processing.markdown_processor import MarkdownProcessor
import logging
import yaml

# Helper function to create a simple AST for testing traversal
def create_test_ast():
    return [
        {'type': 'heading_open', 'tag': 'h1', 'level': 0, 'content': ''},
        {'type': 'inline', 'tag': '', 'level': 1, 'content': 'Heading 1', 'children': [
            {'type': 'text', 'content': 'Heading 1'}
        ]},
        {'type': 'heading_close', 'tag': 'h1', 'level': 0},
        {'type': 'paragraph_open', 'tag': 'p', 'level': 0},
        {'type': 'inline', 'tag': '', 'level': 1, 'content': 'This is a paragraph with bold text.', 'children': [
            {'type': 'text', 'content': 'This is a paragraph with '},
            {'type': 'strong_open', 'tag': 'strong'},
            {'type': 'text', 'content': 'bold'},
            {'type': 'strong_close', 'tag': 'strong'},
            {'type': 'text', 'content': ' text.'}
        ]},
        {'type': 'paragraph_close', 'tag': 'p', 'level': 0},
        {'type': 'fence', 'tag': 'code', 'level': 0, 'info': 'python', 'content': 'print("hello")\n'}
    ]

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

    # --- Tests for process method ---

    def test_process_valid_fm_and_content(self):
        """Test processing text with valid frontmatter and content."""
        processor = MarkdownProcessor()
        markdown_text = """---
title: Test
tags: [a, b]
---
# Header 1

This is content."""
        expected_fm = {'title': 'Test', 'tags': ['a', 'b']}
        
        frontmatter, ast = processor.process(markdown_text)
        
        assert frontmatter == expected_fm
        assert isinstance(ast, list)
        assert len(ast) > 0
        # Check if the first token is the heading
        assert ast[0]['type'] == 'heading_open'
        assert ast[0]['tag'] == 'h1'
        assert ast[1]['type'] == 'inline'
        assert ast[1]['content'] == 'Header 1'
        self.logger.info("Processed valid FM and content correctly.")

    def test_process_no_frontmatter(self):
        """Test processing text with no frontmatter."""
        processor = MarkdownProcessor()
        markdown_text = "# Header 1\\nJust content."
        
        frontmatter, ast = processor.process(markdown_text)
        
        assert frontmatter == {}
        assert isinstance(ast, list)
        assert len(ast) > 0
        assert ast[0]['type'] == 'heading_open'
        assert ast[1]['content'] == 'Header 1'
        assert 'paragraph_open' in [t['type'] for t in ast] # Check content exists
        self.logger.info("Processed content without FM correctly.")

    def test_process_malformed_frontmatter(self):
        """Test processing text with malformed frontmatter."""
        processor = MarkdownProcessor()
        markdown_text = """---
malformed: yaml: here
---
# Content After Malformed"""
        
        frontmatter, ast = processor.process(markdown_text)
        
        assert frontmatter == {} # Should be empty dict as extraction fails
        assert isinstance(ast, list)
        assert len(ast) > 0
        # AST should be for the *entire* original string in this case
        assert ast[0]['type'] == 'paragraph_open' # It parses '---' as thematic_break if not extracted
        assert 'malformed: yaml: here' in ast[1]['content']
        assert 'heading_open' in [t['type'] for t in ast] # H1 should still be parsed later
        self.logger.info("Processed malformed FM correctly (parsing full text).")

    def test_process_none_input(self):
        """Test processing None input."""
        processor = MarkdownProcessor()
        with pytest.raises(TypeError):
            processor.process(None)
        self.logger.info("Caught TypeError for None input correctly.")
            
    def test_process_empty_input(self):
        """Test processing an empty string."""
        processor = MarkdownProcessor()
        frontmatter, ast = processor.process("")
        assert frontmatter == {}
        assert ast == []
        self.logger.info("Processed empty string correctly.")

    # --- Tests for AST Traversal --- 

    def test_find_nodes_by_type(self):
        """Test finding nodes by their type."""
        processor = MarkdownProcessor()
        ast = create_test_ast()
        
        heading_opens = processor.find_nodes_by_type(ast, 'heading_open')
        assert len(heading_opens) == 1
        assert heading_opens[0]['tag'] == 'h1'

        inline_nodes = processor.find_nodes_by_type(ast, 'inline')
        assert len(inline_nodes) == 2
        assert inline_nodes[0]['content'] == 'Heading 1'
        assert inline_nodes[1]['content'] == 'This is a paragraph with bold text.'

        fence_nodes = processor.find_nodes_by_type(ast, 'fence')
        assert len(fence_nodes) == 1
        assert fence_nodes[0]['info'] == 'python'

        non_existent = processor.find_nodes_by_type(ast, 'non_existent_type')
        assert len(non_existent) == 0

        empty_ast_result = processor.find_nodes_by_type([], 'any_type')
        assert len(empty_ast_result) == 0
        self.logger.info("find_nodes_by_type tests passed.")

    def test_get_node_text_content_simple(self):
        """Test getting text content for a simple inline node."""
        processor = MarkdownProcessor()
        ast = create_test_ast()
        # Target the inline node for the heading (index 1)
        heading_text = processor.get_node_text_content(ast, 1)
        assert heading_text == 'Heading 1'
        self.logger.info("get_node_text_content (simple) passed.")
        
    def test_get_node_text_content_nested(self):
        """Test getting text content for a node with nested inline elements."""
        processor = MarkdownProcessor()
        ast = create_test_ast()
        # Target the inline node for the paragraph (index 5)
        paragraph_text = processor.get_node_text_content(ast, 5)
        assert paragraph_text == 'This is a paragraph with bold text.'
        self.logger.info("get_node_text_content (nested) passed.")
        
    def test_get_node_text_content_non_inline(self):
        """Test getting text content for a non-inline node (should be empty)."""
        processor = MarkdownProcessor()
        ast = create_test_ast()
        # Target the heading_open node (index 0)
        non_inline_text = processor.get_node_text_content(ast, 0)
        assert non_inline_text == ''
        # Target the fence node (index 12)
        fence_text = processor.get_node_text_content(ast, 12)
        assert fence_text == '' # Fence content is in 'content' attr, not children
        self.logger.info("get_node_text_content (non-inline) passed.")
        
    def test_get_node_text_content_out_of_bounds(self):
        """Test getting text content with an invalid index."""
        processor = MarkdownProcessor()
        ast = create_test_ast()
        with pytest.raises(IndexError):
            processor.get_node_text_content(ast, 100)
        self.logger.info("get_node_text_content (out of bounds) passed.")
            
    def test_get_node_text_content_empty_ast(self):
        """Test getting text content from an empty AST."""
        processor = MarkdownProcessor()
        with pytest.raises(IndexError): # Or should it return ''? Let's go with IndexError
            processor.get_node_text_content([], 0)
        self.logger.info("get_node_text_content (empty AST) passed.")

# Add logger initialization for tests (optional but good practice)
logging.basicConfig(level=logging.INFO)
TestMarkdownProcessor.logger = logging.getLogger('TestMarkdownProcessor') 