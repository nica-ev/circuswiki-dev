---
created: 2026-06-07 21:04:37
update: 2026-06-07 21:31:46
---

# CircusWiki Tooling Architecture Review

Created: 2026-06-07
Status: discussion draft
Scope: `tools/`, `site-assets/`, multilingual Zensical configs, local dev console, translation/navigation tooling, and future Obsidian integration.

## Executive Summary

CircusWiki tooling has outgrown the original prototype shape. The core direction is sound: Markdown and metadata remain the durable source of truth, Zensical remains the static-site renderer, and the local dev console is becoming the operational bridge for translation, navigation, health checks, and future Obsidian workflows.

The main architectural risk is not any single bug. The risk is duplicated configuration and unclear boundaries as more language/site/tool features are added.

The next step should be a controlled refactor toward a small local tooling platform:

- one language/site registry
- explicit domain modules for translation, site build/staging, navigation, and Obsidian integration
- a thin local web server that exposes APIs but does not own domain behavior
- a modular browser UI served into Obsidian Webviewer or a normal browser
- documented agent/tool workflow under `tools/`
- lightweight but real quality gates

This should be done incrementally. A large rewrite would create more risk than it removes.

## Review Inputs

Reviewed current repository files:

- `README.md`
- `AGENTS.md`
- `_system/translation-architecture.md`
- `tools/stage_multilang.py`
- `tools/translation/workflow.py`
- `tools/navigation/workflow.py`
- `tools/dev_console/server.py`
- `tools/dev_console/static/app.js`
- `tools/dev_console/static/index.html`
- `tools/dev_console/static/styles.css`
- `tools/configure_site_base.py`
- `tools/augment_sitemaps.py`
- `tools/build_multilang.ps1`
- `tools/serve_multilang.ps1`
- `tools/serve_multilang_site.py`
- `tools/translation_cli.py`
- `zensical*.toml`

Compared against attached reference repo docs:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `README.md`

## Current Strengths

### Good project principles

The root documentation correctly prioritizes durable content over presentation tooling. This is the right foundation for a multilingual Obsidian-compatible knowledge commons.

### Plain-text operational model

The repository remains understandable with basic tools: Markdown, TOML, Python scripts, PowerShell wrappers, JSON navigation model, and static assets. This is good for long-term maintenance.

### Plan-first translation workflow

Batch translation planning is a strong safety pattern. It bounds cost and makes source/target/reason visible before calling an API.

### Translation metadata model is directionally correct

The architecture note correctly separates:

- default site language
- file language
- canonical source language
- translation status/provenance

That distinction is essential now that non-German originals and many target languages are expected.

### Static fallback layer is the right deployment strategy

Generating fallback pages and a translation map keeps GitHub Pages static while avoiding avoidable 404s. This should be preserved.

### Navigation model is a useful concept

`tools/navigation/nav.json` is a good move toward a canonical multilingual navigation model instead of treating each Zensical config as independent hand-maintained state.

## Main Findings

### Finding 1: Language configuration is duplicated across too many files

Severity: high

The language list and related metadata currently appear in multiple places:

- `tools/stage_multilang.py`
- `tools/translation/workflow.py`
- `tools/navigation/workflow.py`
- `tools/configure_site_base.py`
- `tools/augment_sitemaps.py`
- `site-assets/javascripts/language-switcher.js`
- every `zensical*.toml` alternate block
- `tools/build_multilang.ps1`
- `README.md`

This already caused a real issue: `sk` was configured as a language but initially missing from `LANGUAGE_NAMES`, which affected UI labels and prompt rendering.

Recommended fix: introduce a single language/site registry and make all tool layers consume it.

### Finding 2: The dev console is now an application, but is still structured like a prototype script

Severity: high

`tools/dev_console/server.py` is currently a thin HTTP server plus direct route dispatcher. That is acceptable while small, but the UI now covers:

- single-file translation
- vault health matrix
- metadata repair
- batch planning and execution
- navigation scanning
- navigation model generation
- navigation translation
- preview/apply

The server should become an adapter layer. Domain logic should stay in separate modules with typed request/response-like structures where practical.

Recommended fix: split API routing from domain orchestration. Keep `http.server` for now unless limitations appear.

### Finding 3: Translation workflow still contains legacy German-to-English assumptions

Severity: high

The group-based batch planner is moving in the right direction, but older CLI and single-file endpoints still default to `de -> en` and list `docs/de/` sources. That is documented as a prototype limitation, but the tool is now being used for many languages.

Recommended fix: make source/target selection explicit in CLI and UI, while preserving convenient defaults.

### Finding 4: Zensical configs are manually expanded language artifacts

Severity: medium-high

Each language has a full TOML config. Some duplication is inherent because Zensical uses separate configs, but repeated fields and alternate blocks should be generated or normalized from a registry.

Recommended fix: create a config generation/sync tool that owns:

- language list
- language names
- URL path segments
- config path
- docs dir
- site dir
- alternate links
- theme language

Navigation blocks can continue to be generated by the navigation model.

### Finding 5: Runtime JavaScript duplicates the language list

Severity: medium-high

`site-assets/javascripts/language-switcher.js` hardcodes `LANGUAGE_CODES`. That makes runtime behavior easy to forget when adding languages.

Recommended fix: either generate this list from the translation map at runtime or emit a small `language-config.json` into staged assets.

Preferred approach: make `language-switcher.js` derive language codes from `translation-map.json` when available, with a minimal fallback for first-load/root-path detection.

### Finding 6: There are no real tests for core transformation behavior

Severity: medium

Current checks are mostly:

- `python -m compileall tools`
- full staging/build
- manual browser verification

This catches syntax and build failures, but not regressions in:

- frontmatter preservation
- source-language detection
- fallback selection
- translation candidate planning
- link restoration
- callout conversion
- language registry propagation

Recommended fix: add focused Python tests for pure functions before deeper refactors.

### Finding 7: Obsidian integration is not yet a first-class boundary

Severity: medium

The stated goal is a local webserver viewed through Obsidian Webviewer and bridged to Obsidian through `obsidian` CLI. This is not yet represented in the architecture.

Recommended fix: add a dedicated `tools/obsidian/` adapter layer before adding CLI calls throughout the server/UI.

The adapter should own:

- CLI availability checks
- opening webviewer URLs
- opening notes/files
- revealing files if supported
- running commands/search if supported
- returning structured errors suitable for the UI

### Finding 8: Tooling docs are root-centered, not tools-centered

Severity: medium

The root `AGENTS.md` and `README.md` are useful but increasingly broad. The attached repo's `Tools/AGENTS.md`, `Tools/README.md`, and `Tools/ARCHITECTURE.md` pattern is a better fit for future agent work.

Recommended fix: add `tools/README.md`, `tools/ARCHITECTURE.md`, and `tools/AGENTS.md` once the target architecture is agreed.

### Finding 9: API/UI contracts are implicit

Severity: medium

The frontend depends on JSON shapes returned by backend functions, but there is no schema or contract documentation. This is manageable today, but changes like `target_lang: all` already show why the contract matters.

Recommended fix: document endpoints and response fields in `tools/README.md`, and consider small dataclasses/normalizers for backend responses.

### Finding 10: Generated files and source files are mostly separated correctly

Severity: low

`.build/` and `site/` are ignored and should remain generated. The architecture should keep all generated output disposable.

## Target Architecture

Keep the current technology choices unless a concrete constraint appears:

- Python for server/domain tooling
- vanilla HTML/CSS/JS for the local console
- PowerShell wrappers for Windows ergonomics
- Zensical for static site generation
- Obsidian CLI adapter for integration

Proposed structure:

```text
tools/
  AGENTS.md
  README.md
  ARCHITECTURE.md
  ARCHITECTURE_REVIEW.md
  config/
    languages.json
    site.json
  core/
    paths.py
    languages.py
    site_config.py
  server/
    app.py
    routes_translation.py
    routes_navigation.py
    routes_obsidian.py
  ui/
    index.html
    app.js
    styles.css
  translation/
    workflow.py
    markdown.py
    metadata.py
  navigation/
    workflow.py
    nav.json
  site/
    stage_multilang.py
    configure_site_base.py
    augment_sitemaps.py
  obsidian/
    cli.py
  tests/
    test_languages.py
    test_translation_planning.py
    test_metadata.py
    test_stage_links.py
```

This is a direction, not an immediate move-all-files task. Move only when it reduces active duplication.

## Proposed Central Registry

A registry should be the first structural refactor.

Example shape:

```json
{
  "default_language": "de",
  "common_fallback_language": "en",
  "languages": [
    { "code": "de", "name": "German", "nativeName": "Deutsch", "root": true, "zensical": "zensical.toml" },
    { "code": "en", "name": "English", "nativeName": "English", "zensical": "zensical.en.toml" },
    { "code": "pl", "name": "Polish", "nativeName": "Polski", "zensical": "zensical.pl.toml" },
    { "code": "pt", "name": "Portuguese", "nativeName": "Português", "zensical": "zensical.pt.toml" },
    { "code": "cs", "name": "Czech", "nativeName": "Česky", "zensical": "zensical.cs.toml" },
    { "code": "sk", "name": "Slovak", "nativeName": "Slovenčina", "zensical": "zensical.sk.toml" }
  ]
}
```

The Python API should provide helpers like:

- `language_codes()`
- `language_name(code)`
- `native_language_name(code)`
- `default_language()`
- `common_fallback_language()`
- `zensical_config_path(code)`
- `docs_path(code)`
- `site_path(code)`
- `language_url(base, code)`

The frontend should receive the registry through an API or generated JSON, not maintain its own list.

## Proposed Obsidian Bridge

The Obsidian bridge should be isolated behind one module and one API route group.

Initial capabilities:

- `GET /api/obsidian/status`
- `POST /api/obsidian/open-webviewer` with URL
- `POST /api/obsidian/open-note` with vault-relative path
- `POST /api/obsidian/reveal-file` if supported

Design rules:

- Do not call `obsidian` CLI directly from unrelated modules.
- All calls return structured JSON with `ok`, `command`, `stdout`, `stderr`, and `error` fields.
- UI should show actionable errors when Obsidian CLI is missing or not connected.
- Browser mode must remain usable without Obsidian.

## Recommended Phases

### Phase 0: Stabilize current changes

Goal: finish current language/batch work safely.

Tasks:

- Keep the dropdown-based `All target languages` option.
- Remove accidental checkbox-only edits.
- Restart/hard-refresh instructions for dev console changes.
- Run `python -m compileall tools` and targeted batch-plan smoke checks.

### Phase 1: Documentation and agent workflow

Goal: make future tool work predictable.

Tasks:

- Add `tools/AGENTS.md` as the mandatory entry point for tooling changes.
- Add `tools/README.md` with commands, runtime model, and API summary.
- Add `tools/ARCHITECTURE.md` with target boundaries and current constraints.
- Keep root `AGENTS.md` as repository-wide policy.

### Phase 2: Central language registry

Goal: remove the highest-risk duplication.

Tasks:

- Add `tools/config/languages.json`.
- Add `tools/core/languages.py`.
- Replace duplicated language lists in Python scripts.
- Generate or validate Zensical alternate blocks from the registry.
- Expose language registry to dev console and runtime site JS.
- Add tests for language registry propagation.

### Phase 3: Translation domain cleanup

Goal: make source-language handling explicit and robust.

Tasks:

- Extract translation group discovery into a shared module.
- Use the same group model in staging and translation workflow.
- Update CLI to support `--source-lang`, `--target-lang`, and group-based planning.
- Preserve existing convenience defaults but stop hardcoding German in the backend contract.
- Add tests for source-language detection and batch candidate selection.

### Phase 4: Dev console modularization

Goal: keep UI/server growth manageable.

Tasks:

- Split server routes by domain.
- Split `app.js` into modules if staying vanilla JS.
- Document API response contracts.
- Add cache-busting for static JS/CSS during local development, or document hard-refresh clearly.

### Phase 5: Obsidian bridge

Goal: support the intended Webviewer workflow without coupling every tool to Obsidian.

Tasks:

- Add `tools/obsidian/cli.py`.
- Add `/api/obsidian/*` routes.
- Add UI affordances to open preview/dev-console in Obsidian Webviewer.
- Keep all features usable in a normal browser.

### Phase 6: Quality gates

Goal: catch regressions before manual browser/build checks.

Tasks:

- Add lightweight Python tests for pure logic.
- Add a single command wrapper for checks.
- Consider `ruff` after the code layout stabilizes.
- Do not add a JS build system unless frontend complexity requires it.

## Suggested Quality Gates

Current minimum:

```powershell
python -m compileall tools
python tools/stage_multilang.py
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

Near-term target:

```powershell
python -m compileall tools
python -m pytest tools/tests
python tools/stage_multilang.py
```

Full release/deployment check:

```powershell
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

## Open Decisions

1. Should the dev console remain Python `http.server` plus vanilla JS for now?

Recommendation: yes. Keep it simple until routing/state requirements exceed it.

1. Should Zensical configs be generated entirely or partially synchronized?

Recommendation: start with partial synchronization. Generate/sync alternate blocks, site URLs, docs dirs, site dirs, and language config. Keep hand-readable TOML files.

1. Should `tools/` files be physically moved now?

Recommendation: no. Add docs and central registry first. Move files only when it reduces a specific duplication or boundary problem.

1. Should Obsidian CLI be required?

Recommendation: no. Treat Obsidian as an optional integration layer. Browser mode must continue to work.

1. Should frontend use a framework?

Recommendation: no for now. Modular vanilla JS is enough. Add a framework only if state complexity becomes the limiting factor.

## Immediate Next Actions

Recommended next implementation slice after this review is accepted:

1. Add `tools/AGENTS.md`, `tools/README.md`, and `tools/ARCHITECTURE.md` based on this review and the attached repo patterns.
2. Add `tools/config/languages.json` and `tools/core/languages.py`.
3. Replace duplicated language definitions in Python code.
4. Add a validation command that checks all configured languages have docs folders, Zensical configs, language names, native names, and alternate entries.
5. Only after that, consider moving server/UI files into clearer directories.
