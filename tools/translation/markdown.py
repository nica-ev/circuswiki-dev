from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownDocument:
    frontmatter: str
    body: str
    has_frontmatter: bool


def split_markdown(text: str) -> MarkdownDocument:
    """Split Markdown into YAML frontmatter and body without parsing YAML."""
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return MarkdownDocument(frontmatter="", body=normalized, has_frontmatter=False)

    marker = "\n---\n"
    end = normalized.find(marker, 4)
    if end == -1:
        return MarkdownDocument(frontmatter="", body=normalized, has_frontmatter=False)

    frontmatter = normalized[4:end]
    body = normalized[end + len(marker) :]
    return MarkdownDocument(
        frontmatter=frontmatter,
        body=body,
        has_frontmatter=True,
    )


def join_markdown(frontmatter: str, body: str) -> str:
    return f"---\n{frontmatter.rstrip()}\n---\n{body.lstrip()}"
