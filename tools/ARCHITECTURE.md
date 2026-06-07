---
created: 2026-06-07 21:33:20
update: 2026-06-07 23:38:09
---

# Tools Architecture

## Goal

The tooling layer is a small, explicit platform around the Markdown vault. It keeps content durable, generated output disposable, and multilingual behavior consistent across staging, translation, navigation, runtime JavaScript, Zensical configs, and optional Obsidian integration.

## Boundaries

`tools/config/`
: Source configuration for local tooling. `languages.json` is the canonical language/site registry.

`tools/core/`
: Shared helpers for language metadata, paths, Zensical config references, and registry validation.

`tools/translation/`
: Markdown/frontmatter-safe translation workflow, metadata inspection, vault health, batch planning, and API calls.

`tools/navigation/`
: Canonical navigation model, Zensical nav rendering, and navigation-label translation.

`tools/dev_console/`
: Local HTTP adapter and static UI. It exposes APIs and renders state; domain behavior belongs in the domain modules above.

`tools/obsidian/`
: Optional Obsidian CLI adapter. Browser mode must remain usable when the CLI is missing.

`site-assets/`
: Static assets copied into each staged language root. Runtime assets should derive language/site data from generated files where possible.

## Current State

Implemented architecture decisions:

- Language/site metadata is centralized in `tools/config/languages.json`.
- Python tooling consumes the registry through `tools/core/languages.py`.
- Zensical configs remain checked-in TOML files and can be validated/synchronized with `tools/sync_configs.py`.
- Translation CLI and dev-console file translation require explicit source and target languages.
- Batch translation uses canonical source detection per translation group and a plan-first workflow.
- Dev-console backend routes are split by domain: translation, navigation, and Obsidian status.
- Dev-console browser helpers are split into small ES modules while keeping vanilla JS and no build step.
- Optional Obsidian CLI integration is isolated behind `tools/obsidian/` and `/api/obsidian/*`.
- Focused unit tests cover registry behavior, staging transformations, translation helpers, navigation rendering, config sync, and Obsidian status behavior.

## Constraints

- Keep Zensical as the static-site renderer unless explicitly replaced.
- Keep `.build/` and `site/` disposable and ignored by Git.
- Keep checked-in Zensical TOML files human-readable; use sync/validation rather than hidden generated config for now.
- Keep the dev console on Python `http.server` and vanilla JS until concrete limitations justify more framework/tooling.
- Do not add a frontend build system unless the UI grows beyond what modular vanilla JS can maintain.
- Config synchronization must be explicit. Validation and dry-runs are safe by default; write operations require an explicit flag.

## Current Quality Gates

Default tooling check:

```powershell
powershell -ExecutionPolicy Bypass -File tools/check.ps1
```

The default check runs Python syntax compilation, language registry validation, unit tests, and multilingual staging.

Config sync dry-run:

```powershell
python tools/sync_configs.py
```

Full static-site build check:

```powershell
powershell -ExecutionPolicy Bypass -File tools/check.ps1 -FullBuild
```

## Remaining Refactor Targets

1. Extract shared translation-group discovery so staging and translation workflow use one implementation.
2. Expand endpoint contract documentation if request/response objects continue to grow.
3. Add more tests around metadata repair edge cases and fallback page rendering.
4. Consider a lightweight schema/validation layer only when duplicated request validation becomes a real maintenance problem.
5. Keep reviewing `app.js` for domain-sized modules, but avoid splitting purely for aesthetics.
