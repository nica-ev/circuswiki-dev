# translation-py/src/processing/markdown_processor.py

from typing import List, Tuple, Dict, Any, Optional
import markdown_it
from markdown_it.token import Token
from ..utils.types import TranslationMap, TextSegment # Uncommented import
import re # Add import for regex
# Placeholder types if real ones aren't ready
# class TranslationMap:
#     def __init__(self):
#         self.segments = []
#     def addSegment(self, segment):
#         self.segments.append(segment)
# class TextSegment:
#     def __init__(self, text, type, path):
#         self.text = text
#         self.type = type
#         self.path = path

def get_element_path(token_stack: List[Token]) -> str: # Simple path based on nesting
    # Basic path generation using token types and levels
    # This needs refinement for uniqueness and stability
    path_parts = [f"{t.type}_{t.level}" for t in token_stack]
    return ' > '.join(path_parts)

class MarkdownProcessor:
    """Processes Markdown content to extract translatable segments."""

    def __init__(self):
        # Initialize markdown-it parser
        # Consider adding options like html=True if needed for complex cases
        self.md = markdown_it.MarkdownIt()
        # Potentially enable specific rules or add plugins here if necessary

    def _extract_inline_text(self, tokens: List[Token]) -> str:
        """Extracts and concatenates text content from a list of inline tokens."""
        text = ""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # print(f"    Inline Token: {token.type}, Level: {token.level}, Tag: {token.tag}, Content: '{token.content[:20]}...'") # Debug
            if token.type == 'text':
                text += token.content
                i += 1
            elif token.type == 'softbreak':
                text += ' ' # Treat softbreaks as spaces
                i += 1
            elif token.type == 'hardbreak':
                text += '\n' # Preserve hardbreaks
                i += 1
            elif token.type == 'em_open' or token.type == 'strong_open':
                # Find matching close tag and recurse
                close_type = token.type.replace('_open', '_close')
                j = i + 1
                nesting_level = 1
                children_tokens: List[Token] = []
                while j < len(tokens):
                    inner_token = tokens[j]
                    if inner_token.type == token.type: # Nested open of same type
                        nesting_level += 1
                    elif inner_token.type == close_type:
                        nesting_level -= 1
                        if nesting_level == 0:
                            text += self._extract_inline_text(children_tokens)
                            i = j + 1 # Move past the closing tag
                            break
                    if nesting_level > 0: # Only add if still inside the tags
                         children_tokens.append(inner_token)
                    j += 1
                if nesting_level != 0: # Closing tag not found, treat opening tag as text?
                     # This case is tricky, maybe log a warning. For now, skip.
                     i += 1 
            elif token.type == 'link_open':
                # Find link_close, extract text from children in between
                j = i + 1
                children_tokens = []
                while j < len(tokens):
                    inner_token = tokens[j]
                    if inner_token.type == 'link_close':
                        text += self._extract_inline_text(children_tokens)
                        i = j + 1
                        break
                    children_tokens.append(inner_token)
                    j += 1
                if j == len(tokens): # link_close not found
                     i += 1
            elif token.type == 'image':
                # Alt text is in token.content for image tokens
                text += token.content
                i += 1
            elif token.type == 'code_inline':
                # Skip inline code content
                i += 1
            elif token.type.endswith('_close'): # Skip unmatched close tags handled by openers
                i += 1
            else:
                # Skip other inline tokens like html_inline for now
                i += 1
        # No final strip() here, as it might remove intended spaces between inline elements
        # Stripping happens when the full block segment is created
        return text 

    def extract_translatable_segments(self, markdown_content: str) -> TranslationMap:
        """
        Parses Markdown content and extracts translatable text segments.
        Focus for Task 7.3: Paragraphs, Headings, List Items, Blockquotes.

        Args:
            markdown_content: The Markdown string to process.

        Returns:
            A TranslationMap object containing the extracted segments.
        """
        tokens: List[Token] = self.md.parse(markdown_content)
        translation_map = TranslationMap()
        token_stack: List[Token] = []
        i = 0
        # ignore_level = -1 # Removed, using token types instead

        while i < len(tokens):
            token = tokens[i]
            # print(f"Processing Token: Level:{token.level} Type:{token.type} Tag:{token.tag} Content:'{token.content[:20]}...'") # Debug

            # --- Code Block Skipping --- 
            if token.type == 'fence' or token.type == 'code_block':
                i += 1
                continue
            # --- End Code Block Skipping ---

            # Handle nesting for path and context
            while token_stack and token.level <= token_stack[-1].level:
                 # print(f"  Popping {token_stack[-1].type} (Level {token_stack[-1].level}) due to {token.type} (Level {token.level})") # Debug
                 token_stack.pop()
            
            is_block_opening = token.type.endswith('_open')
            is_block_closing = token.type.endswith('_close')

            # --- Block Element Processing --- 
            segment_text: Optional[str] = None
            segment_type: Optional[str] = None
            segment_path: Optional[str] = None
            advance_by = 1 # How many tokens to advance 'i' by default

            if is_block_opening:
                token_stack.append(token)
                # print(f"  Pushed {token.type} (Level {token.level}), Stack: {[t.type for t in token_stack]}") # Debug
                # Logic for specific block types that contain inline content directly
                if token.type == 'heading_open' or token.type == 'paragraph_open':
                    # Next token should be inline content
                    if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                        # Extract text recursively from inline children
                        segment_text = self._extract_inline_text(tokens[i+1].children or [])
                        # Condense whitespace before final strip
                        segment_text = re.sub(r'\s+', ' ', segment_text).strip() 
                        # Determine segment type
                        if token.type == 'heading_open':
                            level = token.tag[1]
                            segment_type = f'heading_{level}'
                        else: # paragraph_open
                            parent_token = token_stack[-2] if len(token_stack) > 1 else None
                            if parent_token and parent_token.type == 'list_item_open':
                                segment_type = 'paragraph_in_list' 
                            elif parent_token and parent_token.type == 'blockquote_open':
                                segment_type = 'paragraph_in_blockquote'
                            else:
                                segment_type = 'paragraph'
                        # Skip the inline token and the closing tag
                        advance_by = 3 
                    else: 
                        # Empty paragraph or heading?
                        segment_text = '' 
                        segment_type = 'paragraph' if token.type == 'paragraph_open' else f'heading_{token.tag[1]}'
                        advance_by = 2 # Skip open and close if no inline

                # List items and blockquotes primarily contain other blocks (like paragraphs)
                # The logic above handles paragraphs within them.
                # We don't typically extract a single segment for the whole list item/blockquote block itself.
                # elif token.type == 'list_item_open':
                #     pass # Handled by paragraph_in_list
                # elif token.type == 'blockquote_open':
                #     pass # Handled by paragraph_in_blockquote

            # --- Segment Creation --- 
            if segment_text is not None and segment_type and segment_text: # Ensure non-empty text
                segment_path = get_element_path(token_stack) # Get path based on current stack
                translation_map.addSegment(TextSegment(segment_text, segment_type, segment_path))
                # print(f"  Added Segment: Type={segment_type}, Path={segment_path}, Text={segment_text}") # Debug
            
            # Advance index
            current_i = i # Store current index before advancing
            i += advance_by

            # --- Stack Management --- 
            # Pop from stack if we just advanced past the closing tag for the opening token
            if advance_by > 1 and is_block_opening:
                 expected_close_index = current_i + advance_by - 1 
                 if expected_close_index < len(tokens):
                      closing_token = tokens[expected_close_index]
                      expected_close_type = token.type.replace('_open', '_close')
                      if closing_token.type == expected_close_type and closing_token.level == token.level:
                           if token_stack and token_stack[-1] == token:
                               # print(f"  Implicit Pop {token_stack[-1].type} (Level {token_stack[-1].level}) after advancing past block") # Debug
                               token_stack.pop()
            # Handle explicit closing tags that weren't implicitly handled by advancing
            elif is_block_closing and token_stack: 
                 if token_stack[-1].type == token.type.replace('_close', '_open'):
                      # print(f"  Explicit Pop {token_stack[-1].type} (Level {token_stack[-1].level}) on seeing close tag") # Debug
                      token_stack.pop()
            # --- End Stack Management ---

        # TODO: Add extraction logic for other element types (Task 7.4, etc.)
        # TODO: Add extraction logic for table elements (Task 7.5)
        # TODO: Add extraction logic for specific syntax (WikiLinks, etc. - later tasks)

        return translation_map

# Example Usage (for testing/dev):
if __name__ == '__main__':
    processor = MarkdownProcessor()
    md_example = """
# Header 1

This is a paragraph with *emphasis*.

- List item 1
- List item 2

> A blockquote here.

```python
print("ignore me")
```
    """
    tmap = processor.extract_translatable_segments(md_example)
    for segment in tmap.segments:
        print(f"Type: {segment.type}, Path: {segment.path}, Text: {segment.text}") 