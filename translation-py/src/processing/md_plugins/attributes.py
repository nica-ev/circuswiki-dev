"""Markdown-it-py plugin for parsing Obsidian-style attributes: { .class key=value }."""

import re
from typing import Optional

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token

# More robust Regex: Starts with {, ends with }, allows nested braces if escaped.
# Avoids matching if immediately inside code span (tricky to do perfectly with regex alone).
ATTRIBUTE_RE = re.compile(r"""
    (?<!`)           # Negative lookbehind: Not preceded by a backtick
    \{              # Opening brace
    (               # Group 1: Content
        (?:         # Non-capturing group for content parts
            [^\\{}]+ # Character is not a backslash or brace
            |       # OR
            \\.     # Any escaped character (including \{ and \})
        )*?         # Zero or more times, non-greedy
    )
    \}              # Closing brace
    (?!`)           # Negative lookahead: Not followed by a backtick (helps avoid matching closing brace of code)
""", re.VERBOSE)

def attribute_rule(state: StateInline, silent: bool):
    """Inline rule for parsing Obsidian-style attributes { ... }."""
    # Quick check for starting brace
    if not state.src.startswith('{', state.pos):
        return False

    # Check for escaped brace \{
    if state.pos > 0 and state.src[state.pos - 1] == '\\':
        return False
        
    # Check if we might be inside code - this is markdown-it specific
    # We access the pending text in the state's pending buffer
    if state.pending and state.pending.endswith('`'):
         # Heuristic: if the text right before { was a backtick, assume we are inside code.
         # This isn't perfect but better than the previous check.
         return False
         
    match = ATTRIBUTE_RE.match(state.src, state.pos)
    if not match:
        return False

    attr_content = match.group(1) # Don't strip here, preserve raw content

    if silent:
        return True

    # Push tokens
    token = state.push('attribute_open', '', 1) 
    token.markup = '{'
    token.hidden = True

    token = state.push('attribute_content', '', 0) 
    token.content = attr_content # Store raw content
    token.markup = match.group(0) # Store the full raw match
    token.hidden = True

    token = state.push('attribute_close', '', -1) 
    token.markup = '}'
    token.hidden = True

    state.pos = match.end()
    return True

def attributes_plugin(md: MarkdownIt):
    """Enable attribute parsing rule."""
    # Run after escape rule, but before emphasis.
    # Let's try inserting before 'emphasis' again, like we did for wikilinks.
    md.inline.ruler.before('emphasis', 'obsidian_attributes', attribute_rule)
 