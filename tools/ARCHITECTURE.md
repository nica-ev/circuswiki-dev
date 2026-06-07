# Tools Architecture

## Goal

The tooling layer should be a small, explicit platform around the Markdown vault. It should keep content durable, generated output disposable, and multilingual behavior consistent across staging, translation, navigation, runtime JavaScript, and Zensical configs.

## Boundaries

`tools/config/`
: Source configuration for local tooling. `languages.json` is the canonical language/site registry.

`tools/core/`
: Shared helpers for paths, language metadata, and future site config validation.

`tools/translation/`
: Markdown/frontmatter-safe translation workflow, metadata inspection, batch planning, and API calls.

`tools/navigation/`
: Canonical navigation model, Zensical nav rendering, and navigation-label translation.

`tools/dev_console/`
: Local HTTP adapter and static UI. It should expose APIs and render state, not own domain logic.

`site-assets/`
: Static assets copied into each staged language root. Runtime assets should derive language/site data from generated files where possible.

## Current Constraints

- Python scripts are intentionally kept in their current locations until moving them reduces a concrete duplication or boundary problem.
- The dev console stays on `http.server` and vanilla JS for now.
- Zensical configs remain checked-in TOML files, but duplicated fields should be validated or synchronized from the registry over time.
- Obsidian integration is optional and should be isolated behind a future adapter module.

## Near-Term Refactor Path

1. Centralize language metadata in `tools/config/languages.json` and `tools/core/languages.py`.
2. Replace duplicated language/config lists in Python and PowerShell tools.
3. Add validation for docs folders, Zensical configs, and alternate link coverage.
4. Make CLI and UI source/target language selection explicit beyond `de -> en` defaults.
5. Split dev-console route handling by domain only when route growth makes it necessary.
6. Extend focused tests for pure translation, staging, metadata, and registry behavior.
