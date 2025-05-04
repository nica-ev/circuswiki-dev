# Tests for AST Visitor 

import pytest
from typing import List, Dict, Any, Optional
from unittest.mock import MagicMock, patch
# Assuming Task 6 is done
from src.processing.markdown_processor import MarkdownProcessor
from src.processing.ast_visitor import MarkdownAstVisitor
from markdown_it.token import Token # Assuming Token type
from src.processing.segments import TextSegment, CodeBlockSegment, LinkSegment

# --- Test Visitor Subclass ---

class SimpleVisitor(MarkdownAstVisitor):
    """A simple visitor to record visited node types and content."""
    def __init__(self):
        super().__init__()
        self.visited_log: List[str] = [] # Combined log of type and content
        self.default_visited_types: List[str] = []

    def visit_text(self, node: Token) -> Optional[bool]:
        content = getattr(node, 'content', '')
        self.visited_log.append(f"text: {content}")
        return True

    def visit_paragraph_open(self, node: Token) -> Optional[bool]:
        self.visited_log.append("paragraph_open")
        return True
        
    def visit_paragraph_close(self, node: Token) -> Optional[bool]:
        self.visited_log.append("paragraph_close")
        return True

    def visit_heading_open(self, node: Token) -> Optional[bool]:
        tag = getattr(node, 'tag', '?')
        self.visited_log.append(f"heading_open: {tag}")
        return True
        
    def visit_heading_close(self, node: Token) -> Optional[bool]:
        tag = getattr(node, 'tag', '?')
        self.visited_log.append(f"heading_close: {tag}")
        return True
        
    def visit_inline(self, node: Token) -> Optional[bool]:
        self.visited_log.append("inline")
        # Crucially, allow children of inline nodes to be visited by returning True
        return True 

    def visit_bullet_list_open(self, node: Token) -> Optional[bool]:
        self.visited_log.append("bullet_list_open")
        return True
        
    def visit_bullet_list_close(self, node: Token) -> Optional[bool]:
        self.visited_log.append("bullet_list_close")
        return True
        
    def visit_list_item_open(self, node: Token) -> Optional[bool]:
        self.visited_log.append("list_item_open")
        return True
        
    def visit_list_item_close(self, node: Token) -> Optional[bool]:
        self.visited_log.append("list_item_close")
        return True

    def visit_default(self, node: Token) -> Optional[bool]:
        node_type = getattr(node, 'type', 'unknown')
        self.visited_log.append(f"default: {node_type}") # Log default visits too
        self.default_visited_types.append(node_type)
        return True

# --- Test Fixtures ---

@pytest.fixture(scope="module")
def processor():
    """Provides a MarkdownProcessor instance."""
    # Check if MarkdownProcessor exists and handle potential import error
    try:
        return MarkdownProcessor()
    except ImportError:
        pytest.skip("MarkdownProcessor (Task 6) not available/implemented.")
    except Exception as e:
         pytest.fail(f"Failed to initialize MarkdownProcessor: {e}")

@pytest.fixture
def simple_ast(processor):
    """AST for simple markdown: # Heading\n\nParagraph text."""
    markdown = "# Heading\n\nParagraph text."
    return processor.parse(markdown)

@pytest.fixture
def complex_ast(processor):
    """AST for more complex markdown: # H1\n\nPara 1\n\n* Item 1\n* Item 2"""
    markdown = "# H1\n\nPara 1\n\n* Item 1\n* Item 2"
    return processor.parse(markdown)

# --- Test Cases ---

def test_visitor_instantiation():
    """Test that the visitor classes can be instantiated."""
    base_visitor = MarkdownAstVisitor()
    test_visitor = SimpleVisitor()
    assert isinstance(base_visitor, MarkdownAstVisitor)
    assert isinstance(test_visitor, SimpleVisitor)

def test_visit_called_on_ast(simple_ast):
    """Verify the visit method processes nodes."""
    visitor = SimpleVisitor()
    visitor.visit(simple_ast)
    assert len(visitor.visited_log) > 0
    # Expected: heading_open, inline, text, heading_close, paragraph_open, inline, text, paragraph_close
    assert len(visitor.visited_log) == 8

def test_specific_visit_methods_called(simple_ast):
    """Check that specific visit_<type> methods are dispatched correctly."""
    visitor = SimpleVisitor()
    visitor.visit(simple_ast)
    # Check log for expected entries from specific visitors
    assert "heading_open: h1" in visitor.visited_log
    assert "paragraph_open" in visitor.visited_log
    assert "text: Heading" in visitor.visited_log
    assert "text: Paragraph text." in visitor.visited_log
    assert "inline" in visitor.visited_log # Visited via specific method

def test_default_visitor_called(simple_ast):
    """Check that visit_default is called for types without specific methods."""
    visitor = SimpleVisitor()
    visitor.visit(simple_ast)
    # We added specific handlers for inline, _close tags now.
    # Check if any *other* types fell through to default.
    # For this simple AST, there shouldn't be any defaults called if handlers are comprehensive.
    assert visitor.default_visited_types == [] 

def test_traversal_order(complex_ast):
    """Verify the sequence of visited node types/content."""
    visitor = SimpleVisitor()
    visitor.visit(complex_ast)
    expected_log = [
        'heading_open: h1', 'inline', 'text: H1', 'heading_close: h1',
        'paragraph_open', 'inline', 'text: Para 1', 'paragraph_close',
        'bullet_list_open',
        'list_item_open', 'paragraph_open', 'inline', 'text: Item 1', 'paragraph_close', 'list_item_close',
        'list_item_open', 'paragraph_open', 'inline', 'text: Item 2', 'paragraph_close', 'list_item_close',
        'bullet_list_close'
    ]
    assert visitor.visited_log == expected_log

def test_visit_empty_ast():
    """Test visiting an empty AST list."""
    visitor = SimpleVisitor()
    visitor.visit([])
    assert visitor.visited_log == []

def test_visit_ast_with_no_type_node():
    """Test robustness against nodes missing the 'type' key."""
    visitor = SimpleVisitor()
    # Create dummy Token objects for testing
    malformed_ast = [
        Token(type=None, tag='h1', nesting=1, content='No Type'), # type is None
        Token(type='paragraph_open', tag='p', nesting=1) # Valid node
    ]
    visitor.visit(malformed_ast)
    # Should log a warning and skip the node with type=None
    # The log will show the 'paragraph_open' from the specific visitor
    assert visitor.visited_log == ['paragraph_open']
    assert visitor.default_visited_types == [] 