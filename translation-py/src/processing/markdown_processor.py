# translation-py/src/processing/markdown_processor.py

from typing import List, Tuple, Dict, Any, Optional
import markdown_it
from markdown_it.token import Token
from ..utils.types import TranslationMap, TextSegment # Uncommented import
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
        for token in tokens:
            if token.type == 'text':
                text += token.content
            elif token.type == 'softbreak':
                text += ' ' # Treat softbreaks as spaces
            elif token.type == 'hardbreak':
                text += '\n' # Preserve hardbreaks
            # Ignore code_inline, html_inline etc. by not adding their content
        return text.strip()

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
        ignore_level = -1 # Track level inside code blocks

        while i < len(tokens):
            token = tokens[i]
            # print(f"Processing Token: Level:{token.level} Type:{token.type} Tag:{token.tag} Content:'{token.content[:20]}...'") # Debug

            # --- Code Block Skipping --- 
            if token.type == 'fence':
                # Skip this token
                i += 1
                continue
            if token.type == 'code_block':
                 # Skip this token
                 i += 1
                 continue
            # --- End Code Block Skipping ---

            # Handle nesting for path and context
            while token_stack and token.level <= token_stack[-1].level:
                 token_stack.pop()
            
            is_block_opening = token.type.endswith('_open')
            is_inline = token.type == 'inline'

            # --- Block Element Processing --- 
            segment_text: Optional[str] = None
            segment_type: Optional[str] = None
            segment_path: Optional[str] = None
            advance_by = 1 # How many tokens to advance 'i' by default

            if is_block_opening:
                token_stack.append(token)
                # Logic for specific block types that contain inline content directly
                if token.type == 'heading_open':
                    level = token.tag[1]
                    segment_type = f'heading_{level}'
                    # Next token should be inline content
                    if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                        segment_text = self._extract_inline_text(tokens[i+1].children or [])
                        # Skip the inline token and the closing tag
                        advance_by = 3 
                    else: 
                        advance_by = 2 # Skip open and close if no inline

                # Paragraphs, List Items, Blockquotes often contain inline content within their tags
                # OR they contain nested blocks (like paragraphs inside list items/blockquotes)
                elif token.type == 'paragraph_open':
                    parent_token = token_stack[-2] if len(token_stack) > 1 else None
                    if parent_token and parent_token.type == 'list_item_open':
                         segment_type = 'paragraph_in_list' # Maybe refine later
                    elif parent_token and parent_token.type == 'blockquote_open':
                         segment_type = 'paragraph_in_blockquote'
                    else:
                         segment_type = 'paragraph'
                    
                    # Extract inline content until paragraph_close
                    if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                        segment_text = self._extract_inline_text(tokens[i+1].children or [])
                        advance_by = 3 # Skip open, inline, close
                    else:
                         advance_by = 2 # Skip open, close
                
                # Special handling for list items - extract direct inline text
                # Note: markdown-it often puts paragraphs inside list items even for simple text.
                # The paragraph logic above handles the paragraph_in_list case.
                # This part is tricky and might need adjustment based on how markdown-it structures complex lists.
                elif token.type == 'list_item_open':
                   # Check for immediate inline content *before* a potential nested paragraph
                   # This addresses cases like "- Item *text*" where inline is direct child of li
                   if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                       # Check if the next block isn't paragraph_open
                       if not (i + 2 < len(tokens) and tokens[i+2].type == 'paragraph_open'):
                            segment_type = 'list_item' # Treat as direct list item text
                            segment_text = self._extract_inline_text(tokens[i+1].children or [])
                            # Need to find list_item_close, could be far away
                            j = i + 1
                            li_close_found = False
                            while j < len(tokens):
                                if tokens[j].level == token.level and tokens[j].type == 'list_item_close':
                                    advance_by = (j - i) + 1
                                    li_close_found = True
                                    break
                                j += 1
                            if not li_close_found:
                                advance_by = 2 # Fallback: assume just open/inline?

            # --- Segment Creation --- 
            if segment_text and segment_type:
                segment_path = get_element_path(token_stack)
                translation_map.addSegment(TextSegment(segment_text, segment_type, segment_path))
                # print(f"  Added Segment: Type={segment_type}, Path={segment_path}, Text={segment_text}") # Debug
            
            # Advance index
            i += advance_by

            # Pop from stack if we just advanced past a closing tag implicitly
            if advance_by > 1 and is_block_opening and token_stack:
                 # We need to check if the closing tag was indeed at i(original)+advance_by-1
                 expected_close_index = (i - advance_by) + advance_by -1 
                 if expected_close_index < len(tokens):
                      closing_token = tokens[expected_close_index]
                      expected_close_type = token.type.replace('_open', '_close')
                      if closing_token.type == expected_close_type and closing_token.level == token.level:
                           if token_stack[-1] == token:
                               token_stack.pop()
            elif token.type.endswith('_close') and token_stack: # Explicit close handling
                 if token_stack[-1].type == token.type.replace('_close', '_open'):
                      token_stack.pop()

        # TODO: Add extraction logic for other element types (Task 7.4, etc.)

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