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