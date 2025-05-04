"""
Markdown Processor using markdown-it-py.

This module provides a class to parse Markdown text into an Abstract Syntax Tree (AST)
represented as a list of tokens, using the markdown-it-py library.
"""

import logging
import re
import yaml
from typing import Optional, List, Dict, Any, Tuple
from markdown_it import MarkdownIt

class MarkdownProcessor:
    """
    Parses Markdown text into an AST (token stream) using markdown-it-py.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initializes the MarkdownProcessor.

        Args:
            config: Optional configuration dictionary. Currently unused.
        """
        self.md = MarkdownIt()
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("MarkdownProcessor initialized.")
        # TODO: Configure markdown-it based on self.config if needed

    def extract_frontmatter(self, text: str) -> Tuple[Dict[str, Any], str]:
        """
        Extracts YAML frontmatter (between '---' delimiters) from the start 
        of the text.

        Args:
            text: The input string, potentially containing frontmatter.

        Returns:
            A tuple containing: 
            - A dictionary with the parsed frontmatter (empty if no valid 
              frontmatter was found).
            - The remaining text content after the frontmatter block 
              (or the original text if no frontmatter was found).
        """
        if not isinstance(text, str):
            self.logger.error("Input for extract_frontmatter must be a string.")
            # Or raise TypeError, but returning original seems safer if called internally
            return {}, text 

        # Regex to find YAML frontmatter at the start of the string
        # - Matches '---' at the start (^---)
        # - Followed by optional whitespace (\s*)
        # - Captures everything until the next '---' line (.*?)
        # - Requires the closing '---' line (\n---\s*\n)
        # - Captures the rest of the content (.*)
        # Flags: DOTALL (. matches newline), MULTILINE (^ matches start of lines)
        pattern = r'^---\s*\n(.*?)\n---\s*\n?(.*)$' 
        match = re.match(pattern, text, re.DOTALL | re.MULTILINE)

        if not match:
            self.logger.debug("No frontmatter found.")
            return {}, text # No frontmatter found

        yaml_part = match.group(1).strip()
        # Use strip() on content_part to remove leading/trailing whitespace/newlines
        content_part = match.group(2).strip() 

        if not yaml_part:
            self.logger.debug("Empty frontmatter block found.")
            return {}, content_part # Empty frontmatter block

        try:
            frontmatter = yaml.safe_load(yaml_part)
            if isinstance(frontmatter, dict):
                self.logger.debug("Successfully extracted frontmatter.")
                return frontmatter, content_part
            else:
                # Handle case where YAML is valid but not a dictionary (e.g., a list)
                self.logger.warning(
                    f"Parsed frontmatter is not a dictionary (type: {type(frontmatter)}). "
                    f"Treating as no frontmatter."
                )
                # Return original text because the structure doesn't match expected frontmatter format
                return {}, text 
        except yaml.YAMLError as e:
            # Handle YAML parsing errors
            self.logger.warning(f"Could not parse YAML frontmatter: {e}")
            # Return original text as frontmatter is invalid
            return {}, text
        except Exception as e:
            # Catch any other unexpected errors during loading
            self.logger.exception(f"Unexpected error parsing YAML frontmatter: {e}")
            return {}, text
            
    def parse(self, text: Optional[str]) -> List[Dict[str, Any]]:
        """
        Parses the given Markdown text into a list of tokens (AST).

        Args:
            text: The Markdown text to parse.

        Returns:
            A list of dictionaries, where each dictionary represents a token
            in the markdown-it-py AST structure.

        Raises:
            TypeError: If the input text is None.
            Exception: Re-raises exceptions encountered during parsing after logging.
        """
        if text is None:
            self.logger.error("Input text cannot be None")
            raise TypeError("Input text cannot be None")

        if not text:
            # Return empty list for empty string input
            return []

        try:
            # Use markdown-it-py's parse method
            tokens = self.md.parse(text)
            self.logger.debug(f"Successfully parsed text into {len(tokens)} tokens.")
            return tokens
        except Exception as e:
            # Log any unexpected parsing errors and re-raise
            self.logger.exception(f"Error parsing Markdown text: {e}")
            raise

    def process(self, text: Optional[str]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Processes the full Markdown text, extracting frontmatter and parsing the 
        remaining content into an AST.

        Args:
            text: The full input string, potentially containing frontmatter.

        Returns:
            A tuple containing:
            - A dictionary with the parsed frontmatter (empty if none found or invalid).
            - A list of tokens representing the AST of the content part.
            
        Raises:
            TypeError: If the input text is None.
        """
        if text is None:
            self.logger.error("Input text cannot be None for processing.")
            raise TypeError("Input text cannot be None")

        if not text: # Handle empty string input
            self.logger.info("Processing empty string, returning empty results.")
            return ({}, [])

        self.logger.info("Starting to process text...")
        frontmatter, content_text = self.extract_frontmatter(text)

        if frontmatter:
            self.logger.info(f"Extracted frontmatter: {list(frontmatter.keys())}")
        else:
            self.logger.info("No valid frontmatter found.")
            # If extraction failed, content_text is the original text

        self.logger.info("Parsing content into AST...")
        ast_tokens = self.parse(content_text)
        self.logger.info(f"Generated AST with {len(ast_tokens)} tokens.")

        return frontmatter, ast_tokens

    # --- AST Traversal Methods ---

    def find_nodes_by_type(self, ast: List[Dict[str, Any]], node_type: str) -> List[Dict[str, Any]]:
        """
        Finds all nodes (tokens) in the AST list that match the given type.

        Args:
            ast: The list of tokens representing the AST.
            node_type: The 'type' string to match (e.g., 'heading_open', 'inline').

        Returns:
            A list containing all matching node dictionaries.
        """
        if not ast:
            return []
        return [node for node in ast if node.get('type') == node_type]

    def get_node_text_content(self, ast: List[Dict[str, Any]], node_index: int) -> str:
        """
        Extracts the combined text content from an 'inline' node's children.

        This is useful for getting the rendered text of elements like paragraphs
        or headings, which are represented by an 'inline' token containing 
        child tokens for text, emphasis, links, etc.

        Args:
            ast: The list of tokens representing the AST.
            node_index: The index of the 'inline' node in the AST list.

        Returns:
            The combined text content of the inline node's children, or an
            empty string if the node is not 'inline', has no children, or 
            the index is invalid.
            
        Raises:
            IndexError: If node_index is out of bounds for the ast list.
        """
        if not ast or node_index < 0 or node_index >= len(ast):
            self.logger.warning(f"Invalid index {node_index} or empty AST provided.")
            # Raise IndexError if out of bounds, consistent with list behavior
            if node_index < 0 or node_index >= len(ast):
                 raise IndexError("Node index out of range")
            return "" # Return empty if AST itself is empty but index is 0

        node = ast[node_index]

        # Only extract text from 'inline' nodes which contain renderable content
        if node.get('type') != 'inline':
            self.logger.debug(f"Node at index {node_index} is not type 'inline', returning empty text.")
            return ""

        children = node.get('children')
        if not children:
            # Return the node's own content if no children (e.g., simple text node within inline)
            # Although usually inline nodes *should* have children if they represent complex text
            return node.get('content', '') 

        # Concatenate the 'content' from all child tokens
        text_parts = [child.get('content', '') for child in children if child.get('content')]
        return "".join(text_parts)

# Basic logging setup if the module is run directly (for testing/example)
# In a real application, logging would be configured centrally.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    processor = MarkdownProcessor()
    sample_md = "# Test Header\n\nThis is *important* paragraph content.\n\n- List item 1\n- List item 2\n\n```python\nprint('hello')\n```"
    
    logger.info("Parsing sample Markdown...")
    try:
        ast_result = processor.parse(sample_md)
        logger.info(f"Parsing successful. Got {len(ast_result)} tokens.")
        # Optionally print the AST for inspection
        # import json
        # print(json.dumps(ast_result, indent=2))
    except Exception as e:
        logger.error(f"Sample parsing failed: {e}")

    logger.info("Testing None input...")
    try:
        processor.parse(None)
    except TypeError as e:
        logger.info(f"Caught expected TypeError: {e}")
    except Exception as e:
        logger.error(f"Unexpected error parsing None: {e}")

    logger.info("Testing empty string input...")
    try:
        empty_ast = processor.parse("")
        logger.info(f"Parsing empty string successful. Got {len(empty_ast)} tokens.")
    except Exception as e:
        logger.error(f"Unexpected error parsing empty string: {e}") 