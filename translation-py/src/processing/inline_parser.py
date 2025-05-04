# translation-py/src/processing/inline_parser.py
import re
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

class InlineTokenType(Enum):
    TEXT = auto()
    EMPHASIS_OPEN = auto()  # *
    EMPHASIS_CLOSE = auto() # *
    STRONG_OPEN = auto()    # **
    STRONG_CLOSE = auto()   # **
    CODE_INLINE = auto()    # `code` (single token for content)
    LINK_OPEN = auto()      # [
    LINK_TEXT = auto()      # text
    LINK_CLOSE = auto()     # ]
    LINK_DESTINATION = auto() # (url)
    LINK_TITLE = auto()     # ("title") - Optional
    IMAGE_OPEN = auto()     # ![
    IMAGE_ALT = auto()      # alt
    IMAGE_CLOSE = auto()    # ]
    # IMAGE_DESTINATION and IMAGE_TITLE reuse LINK_DESTINATION/TITLE tokens? Or separate? Let's reuse for now.
    WIKILINK_OPEN = auto()  # [[
    WIKILINK_TARGET = auto()# target
    WIKILINK_SEPARATOR = auto()# |
    WIKILINK_ALIAS = auto() # alias
    WIKILINK_CLOSE = auto() # ]]
    ATTRIBUTE = auto()      # {content} (single token for now)
    HTML_INLINE = auto()    # <...>...</...> or <br/> (single token for now)
    SOFTBREAK = auto()      # Line break in source treated as space
    HARDBREAK = auto()      # Forced line break (e.g., two spaces at end)

@dataclass
class InlineToken:
    type: InlineTokenType
    content: str = ""  # Text content or raw marker/delimiter
    level: int = 0     # Nesting level for emphasis/strong
    attrs: Optional[Dict[str, Any]] = None # e.g., for links {'href': 'url', 'title': 'title'}
    # Removed children for now, focusing on flat token stream first

# Regex for standard Markdown links
LINK_RE = re.compile(r"""
    \!?              # Optional exclamation mark for images
    \[(?P<text>[^\]]*)\]  # Link text or alt text in brackets
    \(               # Opening parenthesis for destination
    (?P<dest>[^\s\)"]*)  # Destination URL (no spaces, parens, quotes)
    (?:\s+"(?P<title>[^"]*)")? # Optional title in double quotes
    \)               # Closing parenthesis
""", re.VERBOSE)

# Regex for WikiLinks
WIKILINK_RE = re.compile(r"\[\[(?P<target>[^\]\|]+?)(?:\|(?P<alias>[^\]]+))?\]\]")

# Regex for Obsidian Attributes (simple version, no nesting support)
# Matches the shortest sequence between { and } greedily.
ATTRIBUTE_RE = re.compile(r"\{(.*?)\}")

class InlineParser:
    def __init__(self):
        # We won't rely on simple regex for stateful parsing like emphasis/strong
        pass

    def parse(self, text: str) -> List[InlineToken]:
        tokens: List[InlineToken] = []
        pos = 0
        text_len = len(text)
        stack = [] # Stack to track open formatting (e.g., 'emphasis', 'strong')
        current_text = ""

        while pos < text_len:
            # Check for links/images first (as they start with [ or ![
            link_match = LINK_RE.match(text, pos)
            if link_match:
                if current_text:
                    tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                    current_text = ""

                link_type = InlineTokenType.IMAGE_OPEN if link_match.group(0).startswith('!') else InlineTokenType.LINK_OPEN
                text_content = link_match.group('text')
                dest_content = link_match.group('dest')
                title_content = link_match.group('title') # Can be None

                tokens.append(InlineToken(type=link_type, content='![' if link_type == InlineTokenType.IMAGE_OPEN else '['))
                # Recursively parse link text/alt text?
                # For now, treat as simple TEXT token
                tokens.append(InlineToken(type=InlineTokenType.TEXT, content=text_content))
                tokens.append(InlineToken(type=InlineTokenType.IMAGE_CLOSE if link_type == InlineTokenType.IMAGE_OPEN else InlineTokenType.LINK_CLOSE, content=']'))
                
                # Add destination and optional title
                tokens.append(InlineToken(type=InlineTokenType.LINK_DESTINATION, content=dest_content))
                if title_content is not None:
                    tokens.append(InlineToken(type=InlineTokenType.LINK_TITLE, content=title_content))

                pos = link_match.end() # Advance past the entire link match
                continue # Move to next iteration

            # Check for WikiLinks
            wikilink_match = WIKILINK_RE.match(text, pos)
            if wikilink_match:
                if current_text:
                    tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                    current_text = ""

                target = wikilink_match.group('target').strip()
                alias = wikilink_match.group('alias') # Can be None

                tokens.append(InlineToken(type=InlineTokenType.WIKILINK_OPEN, content='[['))
                tokens.append(InlineToken(type=InlineTokenType.WIKILINK_TARGET, content=target))

                if alias is not None:
                    alias = alias.strip()
                    tokens.append(InlineToken(type=InlineTokenType.WIKILINK_SEPARATOR, content='|'))
                    tokens.append(InlineToken(type=InlineTokenType.WIKILINK_ALIAS, content=alias))

                tokens.append(InlineToken(type=InlineTokenType.WIKILINK_CLOSE, content=']]'))
                pos = wikilink_match.end()
                continue # Move to next iteration

            # Check for Attributes (simple version)
            # Note: This needs to be carefully ordered WRT other syntax
            # Check *after* links/wikilinks which also use special chars
            attribute_match = ATTRIBUTE_RE.match(text, pos)
            if attribute_match:
                 if current_text:
                    tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                    current_text = ""
                 content = attribute_match.group(1) # Inner content
                 tokens.append(InlineToken(type=InlineTokenType.ATTRIBUTE, content=content))
                 pos = attribute_match.end()
                 continue

            # Check for strong (**)
            elif text.startswith('**', pos) and not text.startswith('***', pos):
                if stack and stack[-1] == 'strong':
                    # Close strong
                    if current_text:
                        tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                        current_text = ""
                    tokens.append(InlineToken(type=InlineTokenType.STRONG_CLOSE, content='**', level=len(stack)))
                    stack.pop()
                elif 'strong' not in stack: # Allow nesting later if needed, but simple for now
                    # Open strong
                    if current_text:
                        tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                        current_text = ""
                    tokens.append(InlineToken(type=InlineTokenType.STRONG_OPEN, content='**', level=len(stack) + 1))
                    stack.append('strong')
                else: # '**' inside existing 'strong' - treat as text for now
                    current_text += '**'
                pos += 2
                continue
            # Check for emphasis (*)
            elif text.startswith('*', pos) and not text.startswith('**', pos):
                if stack and stack[-1] == 'emphasis':
                    # Close emphasis
                    if current_text:
                        tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                        current_text = ""
                    tokens.append(InlineToken(type=InlineTokenType.EMPHASIS_CLOSE, content='*', level=len(stack)))
                    stack.pop()
                elif 'emphasis' not in stack: # Allow nesting later if needed
                     # Open emphasis
                    if current_text:
                        tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                        current_text = ""
                    tokens.append(InlineToken(type=InlineTokenType.EMPHASIS_OPEN, content='*', level=len(stack) + 1))
                    stack.append('emphasis')
                else: # '*' inside existing 'emphasis' - treat as text for now
                    current_text += '*'
                pos += 1
                continue
            # Check for code span (`)
            elif text.startswith('`', pos):
                # Simple code span handling (no nesting of backticks supported)
                end_code = text.find('`', pos + 1)
                if end_code != -1:
                    if current_text:
                        tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))
                        current_text = ""
                    content = text[pos + 1:end_code]
                    tokens.append(InlineToken(type=InlineTokenType.CODE_INLINE, content=content))
                    pos = end_code + 1
                else:
                    # Unmatched backtick, treat as text
                    current_text += text[pos]
                    pos += 1
                continue
            # Check for escaped characters
            elif text.startswith('\\', pos) and pos + 1 < text_len and text[pos+1] in ['*', '`', '[', ']', '{', '}', '\\']:
                 # Append the escaped character directly to the current text buffer
                 current_text += text[pos+1]
                 pos += 2
                 continue

            # Accumulate plain text
            # This else block should only execute if no other pattern matched at the current position
            current_text += text[pos]
            pos += 1

        # Add any remaining text
        if current_text:
            tokens.append(InlineToken(type=InlineTokenType.TEXT, content=current_text))

        # Basic check for unclosed tags (can be improved)
        if stack:
            logger.warning(f"Unclosed formatting tags found: {stack}")
            # Potentially revert tokens or handle error

        logger.info(f"InlineParser generated {len(tokens)} tokens.")
        return tokens 