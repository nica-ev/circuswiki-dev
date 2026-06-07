---
created: 2026-06-06 18:48:28
update: 2026-06-06 19:18:00
---

# AGENTS.md

Instructions for coding agents working in this repository.

## Project Scope

CircusWiki is a Markdown-based knowledge commons for circus pedagogy, movement pedagogy, inclusive practice, games, organizational documentation, and related material.

The repository scope includes both:

- the content itself, primarily under `docs/`
- the surrounding working infrastructure, including the Obsidian vault setup, local tools, translation tooling, static site generation, staging scripts, generated-site assets, and project documentation

Do not treat this as only a website repository. The raw Markdown/YAML content and the local authoring workflow are core project assets.

## Current Architecture

This repo is a clean rebuild of the older setup.

- Content is authored as an Obsidian-compatible vault.
- Public site generation uses Zensical.
- The previous MkDocs Material, MkDocs Publisher, Cursor, and Task Master based workflow is not the active implementation.
- Do not reintroduce old MkDocs/Cursor/Task Master tooling unless explicitly asked.
- Generated staging and build output belong in `.build/` and `site/`; both are ignored by Git.

Relevant paths:

- `docs/de/`: German source pages
- `docs/en/`: English translated pages
- `docs/img/`: shared media assets
- `site-assets/`: assets copied into generated language builds
- `tools/`: local build, staging, translation, and dev-console scripts
- `.obsidian/`: Obsidian vault configuration and part of the project
- `_templates/`: Obsidian templates
- `_dataview/`: Dataview helper notes and queries
- `_canvas/`: Obsidian canvas files
- `_inbox/`: drafts, raw material, and working notes
- `_system/`: vault maintenance notes
- `zensical.toml`: German/default site config
- `zensical.en.toml`: English site config

German is the default public language root. English is published below `/en/`.
Polish (`pl`) is scaffolded as the third language to keep tooling generalized beyond two languages.

```text
/circuswiki/example/
/circuswiki/en/example/
/circuswiki/pl/example/
```

Language folders should preserve matching relative paths:

```text
docs/de/spiele/example.md
docs/en/spiele/example.md
```

## Project Philosophy

The technical manual currently lives at `_inbox/CircusWiki - Technical Manual.md`. It still contains older MkDocs-era details, but its durable principles remain valid:

- Content is the core value of the project.
- Markdown, YAML metadata, and assets are the persistent knowledge base.
- Presentation tools are secondary and replaceable.
- Keep content and presentation separated.
- Prefer open, plain-text, version-controlled formats.
- Preserve decentralization and long-term resilience through Git.
- Support multilingual access as a high-priority goal.
- Preserve meaningful internal linking and metadata-driven discovery.
- Avoid unnecessary complexity in content structure; folders are mostly technical, while links and metadata carry knowledge structure.

When the manual conflicts with current repo implementation, prefer the current implementation documented in `README.md` and the actual code.

## Content Editing Rules

- Preserve YAML frontmatter unless a task explicitly requires changing it.
- Do not bulk-reformat Markdown content without a clear reason.
- Preserve Obsidian-style constructs such as wikilinks, callouts, embeds, Dataview blocks, and canvas-related references.
- Prefer minimal, targeted edits to content files.
- Keep shared images and media in `docs/img/` unless an existing file clearly uses another convention.
- Be careful with non-English content. Do not translate, normalize, or rewrite prose unless explicitly asked.
- Do not delete drafts, inbox notes, templates, Dataview notes, or Obsidian configuration as cleanup. They are part of the working system.

## Translation Tooling

Read `_system/translation-architecture.md` before changing translation metadata, translation discovery, fallback behavior, or language-switching behavior.

Translation tooling currently lives in:

- `tools/translation/`
- `tools/translation_cli.py`
- `tools/dev_console/`
- `tools/dev_console.ps1`

The local translation console starts with:

```powershell
powershell -ExecutionPolicy Bypass -File tools/dev_console.ps1
```

Then open:

```text
http://127.0.0.1:8787
```

The current prototype translation workflow:

- lists German Markdown source files from `docs/de/`
- maps target files to matching paths under `docs/en/`
- inspects translation metadata and source hashes
- sends only the Markdown body to an OpenAI-compatible API
- writes translated output only to target files
- preserves unknown frontmatter fields

This German-to-English assumption is temporary. German is the current default public site language, not a permanent rule for canonical source language. Long-term tooling should translate from each page's original source language as defined by metadata.

Multilingual staging generates static fallback pages for known missing translations and writes `javascripts/translation-map.json`. Do not remove this fallback layer when changing build or language-switching behavior.

Translation metadata currently includes:

```yaml
lang: en
translation_id: ...
translation_source: docs/de/example.md
translation_source_lang: de
translation_source_hash: ...
translation_model: ...
translation_status: machine-translated
translation_updated: ...
```

API keys must never be committed. Use environment variables or a local `.env` file:

```powershell
$env:OPENROUTER_API_KEY = "..."
$env:OPENROUTER_MODEL = "google/gemini-2.0-flash-001"
$env:OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
```

The code also accepts `OPENAI_API_KEY` and `OPENAI_BASE_URL` for OpenAI-compatible endpoints.

The default translation prompt is defined in `tools/translation/workflow.py` in `default_prompt()`.

## Development Workflow

Use PowerShell-compatible commands by default on Windows.

Common setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Preview German/default site only:

```powershell
python tools/stage_multilang.py
zensical serve
```

This serves only `zensical.toml` and does not run multilingual post-build steps.
Do not use it to verify `/circuswiki/en/`, fallback pages, or hover previews.
Hover previews depend on the augmented generated sitemap.

Preview compiled multilingual site with the deployed `/circuswiki/` URL prefix:

```powershell
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1
```

Use the multilingual preview command when testing language switching, translated pages, fallback pages, hover previews, or final GitHub Pages URL shape. It builds all language configs first, augments the generated sitemaps, and serves the generated `site/` directory.

Useful variants:

```powershell
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -Port 8765
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -NoBuild
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -HostAddress 0.0.0.0
```

Expected local URLs:

```text
http://127.0.0.1:8000/circuswiki/
http://127.0.0.1:8000/circuswiki/en/
http://127.0.0.1:8000/circuswiki/pl/
http://127.0.0.1:8000/circuswiki/hu/
http://127.0.0.1:8000/circuswiki/it/
http://127.0.0.1:8000/circuswiki/nl/
```

Build all language sites:

```powershell
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

GitHub Pages deployment:

- `.github/workflows/pages.yml` builds `site/` and deploys it through Actions-based GitHub Pages.
- The checked-in default URL shape remains `/circuswiki/` for the main/public repo.
- The dev repo workflow sets `CIRCUSWIKI_SITE_BASE_PATH=/circuswiki-dev/` and `CIRCUSWIKI_SITE_URL=https://nica-ev.github.io/circuswiki-dev/`.
- Do not hardcode `/circuswiki/` in runtime JS or staging logic. Use `CIRCUSWIKI_SITE_BASE_PATH` for build-time URLs and derive runtime asset roots from loaded script URLs.

Translation CLI:

```powershell
python tools/translation_cli.py health
python tools/translation_cli.py inspect "docs/de/index.md"
python tools/translation_cli.py translate "docs/de/index.md" --dry-run
python tools/translation_cli.py translate "docs/de/index.md"
```

For Python syntax checks:

```powershell
python -m compileall tools
```

## Agent Operating Rules

- Read `README.md` first for current setup.
- Check relevant source files before making implementation claims.
- Assume the working tree may contain user changes. Do not revert unrelated changes.
- Use `rg` for searching when available.
- Prefer small, reviewable changes.
- Keep generated files out of commits unless the user explicitly asks for generated output.
- Do not commit secrets, API keys, local machine paths, virtual environments, caches, `.build/`, or `site/`.
- Do not migrate old tooling back in from historical docs unless the user explicitly asks for it.
- If changing translation behavior, verify both console and CLI entry points where applicable.
- If changing site structure, consider language path parity between `docs/de/` and `docs/en/`.
- If changing content-processing code, preserve Markdown frontmatter/body separation and Obsidian syntax.

## Documentation Priority

Use these sources in this order when deciding what is current:

1. Actual code and config in this repository.
2. `README.md`.
3. `AGENTS.md`.
4. `_inbox/CircusWiki - Technical Manual.md` for project philosophy and historical context.
5. Older docs mentioning MkDocs/Cursor only as historical context unless explicitly revived by the user.
