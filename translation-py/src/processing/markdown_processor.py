# translation-py/src/processing/markdown_processor.py

from typing import List, Tuple, Dict, Any, Optional
import markdown_it
from markdown_it.token import Token
from ..utils.types import TranslationMap, TextSegment # Uncommented import
import re # Add import for regex
import copy # For deep copying tokens if needed
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
# Import the custom plugin
from .md_plugins.wikilinks import wikilinks_plugin
# Import the new attributes plugin
from .md_plugins.attributes import attributes_plugin

def get_element_path(token_stack: List[Token], table_context: Optional[Dict] = None) -> str:
    """Generates a path based on token stack, including table context if available."""
    path_parts = []
    for t in token_stack:
        # Basic path part based on type and level
        part = f"{t.type}_{t.level}"
        # Enhance path part with table context if it matches current token
        if table_context and table_context.get('current_token_ref') == t:
            if 'table_index' in table_context:
                part = f"table_{table_context['table_index']}"
            if 'row_index' in table_context:
                part += f" > tr_{table_context['row_index']}"
            if 'cell_index' in table_context and 'cell_type' in table_context:
                 part += f" > {table_context['cell_type']}_{table_context['cell_index']}"
        path_parts.append(part)
    return ' > '.join(path_parts)

class MarkdownProcessor:
    """Processes Markdown content to extract translatable segments."""

    def __init__(self):
        # Initialize markdown-it parser, enable table, use wikilinks and attributes plugins
        self.md = markdown_it.MarkdownIt()\
            .enable('table')\
            .use(wikilinks_plugin)\
            .use(attributes_plugin) # Enable attributes plugin
        # Potentially enable other specific rules or add plugins here if necessary

    def _extract_inline_text(self, tokens: List[Token]) -> str:
        """
        Extracts and concatenates text content from a list of inline tokens,
        handling standard markdown, wikilinks, and skipping attributes.
        """
        text = ""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # print(f"    Inline Token: {token.type}, Level: {token.level}, Tag: {token.tag}, Content: '{token.content[:20]}...'") # Debug
            if token.type == 'text':
                text += token.content
            elif token.type == 'softbreak':
                text += ' ' # Treat softbreaks as spaces
            elif token.type == 'hardbreak':
                text += '\n' # Preserve hardbreaks
            elif token.type == 'link_open':
                # Find link_close, extract text from children in between
                j = i + 1
                link_children = []
                nesting_level = 1 # Handle nested links? Maybe not needed if children are flat.
                while j < len(tokens):
                    inner_token = tokens[j]
                    # Basic nesting check - might need refinement for complex cases
                    if inner_token.type == 'link_open': nesting_level += 1
                    elif inner_token.type == 'link_close': 
                        nesting_level -= 1
                        if nesting_level == 0:
                            # Recursively extract text from children within the link
                            text += self._extract_inline_text(link_children)
                            i = j # Position i to the link_close token
                            break
                    if nesting_level > 0: # Only add children if inside the main link
                        link_children.append(inner_token)
                    j += 1
                # If link_close not found, we might have an issue, but loop will advance `i`
            elif token.type == 'image':
                # Alt text is in token.content for image tokens
                # Alt text is considered translatable
                text += token.content
            # --- NEW: Handle WikiLink Alias --- 
            elif token.type == 'wikilink_alias':
                text += token.content # Add the alias text
            # --- End WikiLink Handling ---
            # Skip tokens that don't contribute to translatable text:
            elif token.type in ['em_open', 'em_close', 'strong_open', 'strong_close',
                                'code_inline', 'html_inline', 'link_close',
                                # Skip wikilink parts
                                'wikilink_open', 'wikilink_target',
                                'wikilink_separator', 'wikilink_close',
                                # --- NEW: Skip attribute parts ---
                                'attribute_open', 'attribute_content', 'attribute_close']:
                pass # Explicitly skip these types
            else:
                 # Potentially log unknown/unhandled inline types
                 # print(f"Unhandled inline token type: {token.type}")
                 pass 
                 
            i += 1
            
        # No final strip here, let the main extractor handle block-level stripping
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
        table_context: Optional[Dict] = None # Context for table row/col
        table_count = 0 # Track number of tables encountered

        while i < len(tokens):
            token = tokens[i]
            # print(f"Processing Token: Level:{token.level} Type:{token.type} Tag:{token.tag} Content:'{token.content[:20]}...'", table_context) # Debug

            # --- Code Block Skipping --- 
            if token.type == 'fence' or token.type == 'code_block':
                i += 1
                continue
            # --- End Code Block Skipping ---

            # --- Table Context Management --- 
            if token.type == 'table_open':
                table_count += 1
                table_context = {'table_index': table_count, 'row_index': 0, 'cell_index': 0, 'in_header': False, 'current_token_ref': token}
            elif token.type == 'table_close' and table_context:
                table_context = None # Clear context when leaving table
            elif table_context:
                 table_context['current_token_ref'] = token # Update token ref for path generation
                 if token.type == 'thead_open':
                     table_context['in_header'] = True
                     table_context['row_index'] = 0 # Reset row index for header
                 elif token.type == 'tbody_open':
                     table_context['in_header'] = False
                     table_context['row_index'] = 0 # Reset row index for body
                 elif token.type == 'tr_open':
                     table_context['row_index'] += 1
                     table_context['cell_index'] = 0 # Reset cell index for new row
                 elif token.type == 'th_open' or token.type == 'td_open':
                     table_context['cell_index'] += 1
                     table_context['cell_type'] = token.tag # 'th' or 'td'
            # --- End Table Context Management ---

            # --- Stack Management --- 
            # Adjust stack based on current token level relative to stack top
            while token_stack and token.level <= token_stack[-1].level:
                 # Pop if current level is same or lower, unless it's the same table context
                 if not table_context or token_stack[-1].type not in ['table_open', 'thead_open', 'tbody_open', 'tr_open', 'th_open', 'td_open']:
                      # print(f"  Popping {token_stack[-1].type} (Level {token_stack[-1].level}) due to {token.type} (Level {token.level})", table_context) # Debug
                      token_stack.pop()
                 else:
                     break # Don't pop table elements unnecessarily

            is_block_opening = token.type.endswith('_open')
            is_block_closing = token.type.endswith('_close')

            # --- Block Element Processing --- 
            segment_text: Optional[str] = None
            segment_type: Optional[str] = None
            segment_path: Optional[str] = None
            advance_by = 1 

            if is_block_opening:
                # Always push opening blocks onto the stack
                token_stack.append(token)
                # print(f"  Pushed {token.type} (Level {token.level}), Stack: {[t.type for t in token_stack]}", table_context) # Debug

                # Logic for specific block types that contain inline content directly
                if token.type in ['heading_open', 'paragraph_open', 'th_open', 'td_open']:
                    if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                        segment_text = self._extract_inline_text(tokens[i+1].children or [])
                        segment_text = re.sub(r'\s+', ' ', segment_text).strip() 
                        
                        # Determine segment type
                        if token.type == 'heading_open':
                            level = token.tag[1]
                            segment_type = f'heading_{level}'
                        elif token.type == 'th_open':
                            segment_type = 'table_header_cell'
                        elif token.type == 'td_open':
                            segment_type = 'table_data_cell'
                        elif token.type == 'paragraph_open':
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
                        # Empty paragraph, heading, or table cell
                        segment_text = '' 
                        if token.type == 'heading_open': segment_type = f'heading_{token.tag[1]}'
                        elif token.type == 'paragraph_open': segment_type = 'paragraph'
                        elif token.type == 'th_open': segment_type = 'table_header_cell'
                        elif token.type == 'td_open': segment_type = 'table_data_cell'
                        advance_by = 2 # Skip open and close if no inline
                
                # Other opening tags are pushed, but content is handled by nested elements (like paragraph_in_list)

            # --- Segment Creation --- 
            if segment_text is not None and segment_type and segment_text: # Ensure non-empty text
                segment_path = get_element_path(token_stack, table_context) # Use table context for path if available
                translation_map.addSegment(TextSegment(segment_text, segment_type, segment_path))
                # print(f"  Added Segment: Type={segment_type}, Path={segment_path}, Text={segment_text}", table_context) # Debug
            
            # Advance index
            current_i = i 
            i += advance_by

            # --- Updated Stack Management (Post-Advance) --- 
            # Pop from stack if we just advanced past the closing tag for the opening token
            if advance_by > 1 and is_block_opening:
                 expected_close_index = current_i + advance_by - 1 
                 if expected_close_index < len(tokens):
                      closing_token = tokens[expected_close_index]
                      expected_close_type = token.type.replace('_open', '_close')
                      if closing_token.type == expected_close_type and closing_token.level == token.level:
                           if token_stack and token_stack[-1] == token:
                               # print(f"  Implicit Pop {token_stack[-1].type} (Level {token_stack[-1].level}) after advancing past block", table_context) # Debug
                               token_stack.pop()
            # Handle explicit closing tags that weren't implicitly handled by advancing
            elif is_block_closing and token_stack: 
                 if token_stack[-1].type == token.type.replace('_close', '_open'):
                      # print(f"  Explicit Pop {token_stack[-1].type} (Level {token_stack[-1].level}) on seeing close tag", table_context) # Debug
                      token_stack.pop()
            # --- End Stack Management ---

        # TODO: Add extraction logic for other element types (Task 7.4, etc.)
        # TODO: Add extraction logic for table elements (Task 7.5)
        # TODO: Add extraction logic for specific syntax (WikiLinks, etc. - later tasks)

        return translation_map

    def reassemble_markdown(self, original_markdown: str, translated_segments: Dict[str, str]) -> str:
        """
        Reconstructs Markdown content using translated text segments by modifying tokens
        and using the built-in renderer.
        
        Args:
            original_markdown: The original Markdown string.
            translated_segments: A dictionary mapping segment paths to translated text.
        
        Returns:
            The reconstructed Markdown string with translations applied.
        """
        tokens: List[Token] = self.md.parse(original_markdown)
        token_stack: List[Token] = []
        table_context: Optional[Dict] = None
        table_count = 0
        i = 0

        # First pass: Modify tokens in place based on translations
        while i < len(tokens):
            token = tokens[i]
            advance_by = 1

            # --- Manage Context (Stack & Table) --- 
            # (Similar logic to extraction for table context and stack management)
            if token.type == 'table_open':
                table_count += 1
                table_context = {'table_index': table_count, 'row_index': 0, 'cell_index': 0, 'in_header': False, 'current_token_ref': token}
            elif token.type == 'table_close' and table_context:
                table_context = None
            elif table_context:
                 table_context['current_token_ref'] = token
                 if token.type == 'thead_open': table_context['in_header'] = True; table_context['row_index'] = 0
                 elif token.type == 'tbody_open': table_context['in_header'] = False; table_context['row_index'] = 0
                 elif token.type == 'tr_open': table_context['row_index'] += 1; table_context['cell_index'] = 0
                 elif token.type == 'th_open' or token.type == 'td_open': table_context['cell_index'] += 1; table_context['cell_type'] = token.tag
            
            # Manage stack (simplified)
            while token_stack and token.level <= token_stack[-1].level:
                 if not table_context or token_stack[-1].type not in ['table_open', 'thead_open', 'tbody_open', 'tr_open', 'th_open', 'td_open']:
                      token_stack.pop()
                 else:
                     break 

            is_block_opening = token.type.endswith('_open')
            is_block_closing = token.type.endswith('_close')

            if is_block_opening:
                token_stack.append(token)
                # Handle blocks that contain inline content directly
                if token.type in ['heading_open', 'paragraph_open', 'th_open', 'td_open']:
                    if i + 1 < len(tokens) and tokens[i+1].type == 'inline':
                        inline_token = tokens[i+1]
                        # Generate path for this segment
                        current_path = get_element_path(token_stack, table_context)
                        translated_text = translated_segments.get(current_path)

                        if translated_text is not None:
                            # Modify the inline token's content/children
                            # Simple approach: Replace content of the first text child found? 
                            # Or better: rebuild children based on translated text (complex).
                            # For now, let's replace the *inline token's content* directly.
                            # This relies on the renderer using this field, might lose internal formatting.
                            inline_token.content = translated_text
                            # Clear children? Renderer might use content OR children.
                            # inline_token.children = [Token(type='text', tag='', nesting=0, content=translated_text, level=inline_token.level+1, attrs=None, map=None, info='', meta=None, block=False, hidden=False)]
                            # The above might be safer if renderer prioritizes children.

                        advance_by = 3 # Skip inline and close tag
                        # Pop stack after processing block
                        if token_stack and token_stack[-1] == token: token_stack.pop()
                    else:
                        # Empty block 
                        advance_by = 2
                        if token_stack and token_stack[-1] == token: token_stack.pop()
            
            # Pop stack on explicit close tags
            elif is_block_closing and token_stack and token_stack[-1].type == token.type.replace('_close', '_open'):
                  token_stack.pop()

            i += advance_by

        # Second pass: Render the modified token stream
        env = {}
        return self.md.renderer.render(tokens, self.md.options, env)

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