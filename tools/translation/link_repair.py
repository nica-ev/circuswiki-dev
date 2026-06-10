from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable


MARKDOWN_LINK_RE = re.compile(
    r"(!?\[[^\]]*\]\()"
    r"(?P<inner><[^>]+>|[^)]*)"
    r"(\))"
)
WIKILINK_RE = re.compile(r"(!?\[\[)(?P<body>[^\]]+)(\]\])")
LOCAL_MARKDOWN_TARGET_RE = re.compile(
    r"^(?![a-z][a-z0-9+.-]*:|#|/|mailto:)(?P<path>[^#?]+?\.md)(?P<suffix>[#?].*)?$",
    re.IGNORECASE,
)
LOCAL_REPAIRABLE_TARGET_RE = re.compile(
    r"^(?![a-z][a-z0-9+.-]*:|#|/|mailto:)"
    r"(?P<path>[^#?]+?\.(?:md|png|jpe?g|gif|svg|webp|avif|pdf|mp3|mp4|wav|ogg))"
    r"(?P<suffix>[#?].*)?$",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class LinkRepairDiagnostic:
    kind: str
    link_type: str
    message: str
    source_target: str = ""
    translated_target: str = ""


@dataclass(frozen=True)
class LinkRepairResult:
    body: str
    changed: bool
    repair_count: int
    diagnostics: list[LinkRepairDiagnostic]

    def to_dict(self) -> dict[str, object]:
        return {
            "body": self.body,
            "changed": self.changed,
            "repair_count": self.repair_count,
            "diagnostics": [asdict(item) for item in self.diagnostics],
        }


@dataclass(frozen=True)
class MarkdownLink:
    raw_target: str
    normalized_target: str
    start: int
    end: int
    prefix: str
    suffix: str


@dataclass(frozen=True)
class Wikilink:
    raw_target: str
    start: int
    end: int
    prefix: str
    alias: str
    suffix: str


def repair_link_targets(source_body: str, translated_body: str) -> LinkRepairResult:
    markdown_result = repair_markdown_link_targets(source_body, translated_body)
    wikilink_result = repair_wikilink_targets(source_body, markdown_result.body)
    diagnostics = [*markdown_result.diagnostics, *wikilink_result.diagnostics]
    repair_count = markdown_result.repair_count + wikilink_result.repair_count
    return LinkRepairResult(
        body=wikilink_result.body,
        changed=wikilink_result.body != translated_body,
        repair_count=repair_count,
        diagnostics=diagnostics,
    )


def repair_markdown_link_targets(source_body: str, translated_body: str) -> LinkRepairResult:
    source_links = extract_markdown_links(source_body)
    translated_links = extract_markdown_links(translated_body)
    diagnostics = sequence_diagnostics("markdown", source_links, translated_links)
    if len(source_links) != len(translated_links):
        repaired = translated_body
        repair_count = 0
    else:
        repaired = replace_markdown_targets(translated_body, source_links, translated_links)
        repair_count = sum(
            1
            for source, translated in zip(source_links, translated_links)
            if source.raw_target != translated.raw_target
        )
    return LinkRepairResult(
        body=repaired,
        changed=repaired != translated_body,
        repair_count=repair_count,
        diagnostics=diagnostics,
    )


def repair_wikilink_targets(source_body: str, translated_body: str) -> LinkRepairResult:
    source_links = extract_wikilinks(source_body)
    translated_links = extract_wikilinks(translated_body)
    diagnostics = sequence_diagnostics("wikilink", source_links, translated_links)
    if len(source_links) != len(translated_links):
        repaired = translated_body
        repair_count = 0
    else:
        repaired = replace_wikilink_targets(translated_body, source_links, translated_links)
        repair_count = sum(
            1
            for source, translated in zip(source_links, translated_links)
            if source.raw_target != translated.raw_target
        )
    return LinkRepairResult(
        body=repaired,
        changed=repaired != translated_body,
        repair_count=repair_count,
        diagnostics=diagnostics,
    )


def extract_markdown_links(body: str) -> list[MarkdownLink]:
    fence_spans = fenced_code_spans(body)
    links: list[MarkdownLink] = []
    for match in MARKDOWN_LINK_RE.finditer(body):
        if inside_any_span(match.start(), fence_spans):
            continue
        parsed = markdown_target_span(match.group("inner"), match.start("inner"))
        if not parsed:
            continue
        raw_target, target_start, target_end = parsed
        normalized = normalize_markdown_target(raw_target)
        if not is_local_repairable_target(raw_target):
            continue
        links.append(
            MarkdownLink(
                raw_target=raw_target,
                normalized_target=normalized,
                start=target_start,
                end=target_end,
                prefix=match.group(1),
                suffix=match.group(3),
            )
        )
    return links


def extract_wikilinks(body: str) -> list[Wikilink]:
    fence_spans = fenced_code_spans(body)
    links: list[Wikilink] = []
    for match in WIKILINK_RE.finditer(body):
        if inside_any_span(match.start(), fence_spans):
            continue
        body_text = match.group("body")
        target = wikilink_target(body_text)
        if not target:
            continue
        links.append(
            Wikilink(
                raw_target=target,
                start=match.start("body"),
                end=match.start("body") + len(target),
                prefix=match.group(1),
                alias=wikilink_alias(body_text),
                suffix=match.group(3),
            )
        )
    return links


def replace_markdown_targets(
    translated_body: str,
    source_links: list[MarkdownLink],
    translated_links: list[MarkdownLink],
) -> str:
    output = translated_body
    for source, translated in reversed(list(zip(source_links, translated_links))):
        if source.raw_target == translated.raw_target:
            continue
        output = output[: translated.start] + source.raw_target + output[translated.end :]
    return output


def replace_wikilink_targets(
    translated_body: str,
    source_links: list[Wikilink],
    translated_links: list[Wikilink],
) -> str:
    output = translated_body
    for source, translated in reversed(list(zip(source_links, translated_links))):
        if source.raw_target == translated.raw_target:
            continue
        output = output[: translated.start] + source.raw_target + output[translated.end :]
    return output


def sequence_diagnostics(
    link_type: str,
    source_links: Iterable[MarkdownLink | Wikilink],
    translated_links: Iterable[MarkdownLink | Wikilink],
) -> list[LinkRepairDiagnostic]:
    source_list = list(source_links)
    translated_list = list(translated_links)
    diagnostics: list[LinkRepairDiagnostic] = []
    if len(source_list) != len(translated_list):
        diagnostics.append(
            LinkRepairDiagnostic(
                kind="link_count_mismatch",
                link_type=link_type,
                message=(
                    f"Source has {len(source_list)} local {link_type} link(s), "
                    f"translation has {len(translated_list)}."
                ),
            )
        )
        return diagnostics

    for source, translated in zip(source_list, translated_list):
        if source.raw_target == translated.raw_target:
            continue
        diagnostics.append(
            LinkRepairDiagnostic(
                kind="target_repaired",
                link_type=link_type,
                message="Local link target differs from source and was restored.",
                source_target=source.raw_target,
                translated_target=translated.raw_target,
            )
        )
    return diagnostics


def restore_internal_link_targets(source_body: str, translated_body: str) -> str:
    return repair_link_targets(source_body, translated_body).body


def restore_markdown_link_targets(source_body: str, translated_body: str) -> str:
    return repair_markdown_link_targets(source_body, translated_body).body


def restore_wikilink_targets(source_body: str, translated_body: str) -> str:
    return repair_wikilink_targets(source_body, translated_body).body


def is_local_markdown_target(target: str) -> bool:
    return bool(LOCAL_MARKDOWN_TARGET_RE.match(normalize_markdown_target(target)))


def is_local_repairable_target(target: str) -> bool:
    return bool(LOCAL_REPAIRABLE_TARGET_RE.match(normalize_markdown_target(target)))


def markdown_target_span(inner: str, inner_start: int) -> tuple[str, int, int] | None:
    stripped = inner.strip()
    if not stripped:
        return None

    leading = len(inner) - len(inner.lstrip())
    target_start = inner_start + leading
    if stripped.startswith("<"):
        closing = stripped.find(">")
        if closing == -1:
            return None
        raw_target = stripped[: closing + 1]
        return raw_target, target_start, target_start + len(raw_target)

    raw_target = strip_markdown_link_title(stripped)
    if not raw_target:
        return None
    return raw_target, target_start, target_start + len(raw_target)


def strip_markdown_link_title(inner: str) -> str:
    title_match = re.search(r"\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\))\s*$", inner)
    if not title_match:
        return inner.rstrip()
    return inner[: title_match.start()].rstrip()


def normalize_markdown_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        return target[1:-1].strip()
    return target


def wikilink_target(body: str) -> str:
    return body.split("|", 1)[0].strip()


def wikilink_alias(body: str) -> str:
    if "|" not in body:
        return ""
    return "|" + body.split("|", 1)[1]


def fenced_code_spans(body: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    in_fence = False
    start = 0
    offset = 0
    for line in body.splitlines(keepends=True):
        line_start = offset
        line_end = offset + len(line)
        if FENCE_RE.match(line):
            if in_fence:
                spans.append((start, line_end))
                in_fence = False
            else:
                start = line_start
                in_fence = True
        offset = line_end
    if in_fence:
        spans.append((start, len(body)))
    return spans


def inside_any_span(position: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= position < end for start, end in spans)
