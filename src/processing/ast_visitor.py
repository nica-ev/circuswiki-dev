# AST Visitor Implementation 
from typing import List, Any, Type, Optional
import logging
# Assuming markdown-it-py Token type, may need actual import if available
from markdown_it.token import Token # Hypothetical import

class MarkdownAstVisitor:
    """Base class for traversing a markdown-it-py AST (list of Tokens)."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def visit(self, ast: List[Token]) -> None:
        """Start traversal of the AST (list of Tokens)."""
        self.logger.debug(f"Starting AST traversal with {len(ast)} tokens.")
        for node in ast:
            self._visit_node(node)
        self.logger.debug("AST traversal finished.")

    def _visit_node(self, node: Token) -> None:
        """Visit a single token and dispatch to specific methods."""
        node_type = getattr(node, 'type', None)
        if not node_type:
            self.logger.warning(f"Node missing 'type' attribute: {node}")
            return

        method_name = f"visit_{node_type}"
        visitor_method = getattr(self, method_name, self.visit_default)
        
        self.logger.debug(f"Visiting node type '{node_type}' with method '{visitor_method.__name__}'")
        # Execute the specific visitor method first
        should_continue = visitor_method(node)

        # If the visitor method didn't return False, check for children
        if should_continue is not False and node.children:
            self.logger.debug(f"Visiting {len(node.children)} children of node type '{node_type}'")
            # Visit children after processing the parent node itself
            for child in node.children:
                 self._visit_node(child) # Recursive call

    def visit_default(self, node: Token) -> Optional[bool]: # Allow returning bool
        """Default visitor method called if specific visitor is not found."""
        self.logger.debug(f"No specific visitor for type '{getattr(node, 'type', 'unknown')}', using default.")
        # By default, allow children traversal if they exist
        return True

    # --- Add specific visit methods as needed by subclasses ---
    # Example:
    # def visit_paragraph_open(self, node: Dict[str, Any]) -> None:
    #     pass
    # 
    # def visit_text(self, node: Dict[str, Any]) -> None:
    #     pass
    # 
    # def visit_heading_open(self, node: Dict[str, Any]) -> None:
    #     pass 