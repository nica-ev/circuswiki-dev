"""Markdown-it-py plugin for parsing Obsidian-style WikiLinks: [[target]] or [[target|alias]]."""

import re
from typing import Optional

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token

# Regex to capture WikiLinks, handling potential escaping and ensuring proper closing.
# Group 1: Target (anything not | or ])
# Group 2: Optional pipe and alias (?:\|([^]]+))
#    Group 3: Alias (anything not ])
WIKILINK_RE = re.compile(r"""
    \[\[              # Opening double brackets
    (?!\[)             # Avoid matching [[[link]]]
    (                   # Group 1: Target
        [^\|\]+?      # One or more characters not | or ], non-greedy
    )
    (?:                 # Optional non-capturing group for pipe and alias
        \|              # Pipe separator
        (               # Group 2: Alias
            [^\|\]]*?  # ZERO or more characters not | or ], non-greedy (* instead of +)
        )
    )?                  # Alias part is optional
    \]\]              # Closing double brackets
""", re.VERBOSE)

# Simpler Regex for initial testing: Matches [[ followed by anything except ]] up to the closing ]]
WIKILINK_RE_SIMPLE = re.compile(r"\[\[([^]]+?)\]\]")

def wikilink_rule(state: StateInline, silent: bool):
    """Inline rule for parsing WikiLinks."""
    if not state.src.startswith('[[', state.pos):
        return False

    # Use the simpler regex
    match = WIKILINK_RE_SIMPLE.match(state.src, state.pos)
    if not match:
        # Debug: Log if no match found where expected
        # print(f"WikiLink RE failed at pos {state.pos} on: {state.src[state.pos:state.pos+20]}")
        return False

    # If matched, extract the inner content
    inner_content = match.group(1).strip()
    target = inner_content
    alias = None

    # Basic split for alias (can be refined later)
    if '|' in inner_content:
        parts = inner_content.split('|', 1)
        target = parts[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else '' # Handle [[target|]] case

    if silent:
        return True

    # Push tokens (similar logic as before)
    token = state.push('wikilink_open', '', 1)
    token.markup = '[['

    token = state.push('wikilink_target', '', 0)
    token.content = target
    token.hidden = True

    if alias is not None: # Check if alias was present (even if empty string)
        token = state.push('wikilink_separator', '', 0)
        token.markup = '|'
        token.hidden = True
        
        token = state.push('wikilink_alias', '', 0)
        token.content = alias # Alias can be empty

    token = state.push('wikilink_close', '', -1)
    token.markup = ']]'

    state.pos = match.end()
    return True

def wikilinks_plugin(md: MarkdownIt):
    """Enable WikiLink parsing rule."""
    # Try inserting before 'emphasis' as it might interact with single brackets
    md.inline.ruler.before('emphasis', 'wikilink', wikilink_rule)
    # Alternatively, could try md.inline.ruler.push if conflicts arise
    # md.inline.ruler.push('wikilink', wikilink_rule) 