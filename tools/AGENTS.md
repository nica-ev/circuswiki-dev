# Tools Agent Instructions

These instructions apply to changes under `tools/`, `site-assets/`, multilingual Zensical configs, and local tooling documentation.

## Current Direction

CircusWiki tooling should remain a small local platform around plain-text content:

- Markdown/YAML content in `docs/` is the source of truth.
- Zensical remains the static-site renderer.
- `.build/` and `site/` are disposable generated output.
- The dev console is an adapter UI/server; domain behavior belongs in modules.
- Language and site metadata must come from `tools/config/languages.json` through `tools/core/languages.py`.

## Working Rules

- Read the root `README.md` and relevant source before making implementation claims.
- Prefer small changes that reduce active duplication.
- Do not reintroduce MkDocs, Cursor, or Task Master tooling unless explicitly requested.
- Preserve frontmatter/body separation and Obsidian Markdown constructs.
- Do not hardcode `/circuswiki/` in runtime JavaScript; use build-time environment variables or derive paths from loaded assets.
- Do not add language lists directly to scripts when the registry can provide them.
- Keep browser mode usable without Obsidian integration.
- Translation CLI and translation endpoints must require explicit source/target languages for operational actions.

## Checks

Minimum checks for tooling changes:

```powershell
powershell -ExecutionPolicy Bypass -File tools/check.ps1
python tools/sync_configs.py
```

For staging or multilingual URL changes, also run:

```powershell
python tools/stage_multilang.py
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
powershell -ExecutionPolicy Bypass -File tools/check.ps1 -FullBuild
```
