# CircusWiki Tools

Local tooling supports multilingual staging, translation workflow experiments, navigation management, and static site builds.

## Main Commands

```powershell
python tools/stage_multilang.py
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1
powershell -ExecutionPolicy Bypass -File tools/dev_console.ps1
powershell -ExecutionPolicy Bypass -File tools/check.ps1
python tools/sync_configs.py
```

Translation CLI:

```powershell
python tools/translation_cli.py health --source-lang de --target-lang en
python tools/translation_cli.py inspect "docs/de/index.md" --source-lang de --target-lang en
python tools/translation_cli.py translate "docs/de/index.md" --source-lang de --target-lang en --dry-run
```

Registry validation:

```powershell
python -m tools.core.languages
```

Tests:

```powershell
python -m unittest discover tools/tests
```

Combined checks:

```powershell
powershell -ExecutionPolicy Bypass -File tools/check.ps1
powershell -ExecutionPolicy Bypass -File tools/check.ps1 -FullBuild
```

Zensical config sync is dry-run by default:

```powershell
python tools/sync_configs.py
python tools/sync_configs.py --write
```

The sync command derives `site_url`, `docs_dir`, `site_dir`, theme language, and
alternate language entries from `tools/config/languages.json`. It respects
`CIRCUSWIKI_SITE_BASE_PATH` and `CIRCUSWIKI_SITE_URL`, or explicit `--base-path`
and `--base-url` arguments.

## Language Registry

The configured language list lives in `tools/config/languages.json`. Python tools should access it through `tools/core/languages.py` instead of duplicating language codes, names, fallback behavior, or Zensical config paths.

The registry currently owns:

- default language
- common fallback language
- language code order
- English and native language names
- Zensical config file per language
- root/default language marker

## Dev Console API Summary

The local console is served by `tools/dev_console/server.py`.

Current endpoint contracts:

- `GET /api/config`: returns registry languages, UI initial source/target selections, default model, default prompt template, and rendered default prompt.
- `GET /api/pages?source_lang=<code>`: returns source Markdown paths for the explicit source language. Missing `source_lang` returns `400`.
- `GET /api/health?source_lang=<code>&target_lang=<code>`: returns the file-pair health summary for the explicit language pair. Missing language parameters return `400`.
- `GET /api/page?path=<repo-path>&source_lang=<code>&target_lang=<code>`: inspects one explicit source/target pair. Missing `path`, `source_lang`, or `target_lang` returns `400`.
- `GET /api/vault-health`: returns the multilingual translation matrix using canonical source detection per translation group.
- `POST /api/translate`: translates one file. JSON body requires `path`, `source_lang`, and `target_lang`; optional fields are `model`, `prompt`, and `dry_run`.
- `POST /api/repair-metadata`: deterministic metadata repair for one file. JSON body requires `path`.
- `POST /api/batch-plan`: plans batch candidates without API calls. JSON body uses `target_lang`, `max_files`, optional `source_lang` (`all` allowed), optional `reason`, optional `max_source_chars`, and optional `path_filter`.
- `POST /api/batch-translate-file`: translates one planned batch item. JSON body uses `source_path`, `source_lang`, `target_lang`, and optional `model`/`prompt`.
- `GET /api/navigation/scan`: inspects Zensical navigation and canonical navigation model state.
- `POST /api/navigation/init`: creates the canonical navigation model from an explicit source language. JSON body requires `language`.
- `POST /api/navigation/preview`: renders the supplied model without writing files. JSON body requires `model`.
- `POST /api/navigation/apply`: writes the supplied model and regenerates Zensical nav blocks. JSON body requires `model`.
- `POST /api/navigation/translate-labels`: translates navigation labels for one target language. JSON body requires `model`, `source_lang`, and `target_lang`.
- `POST /api/navigation/translate-all-labels`: translates navigation labels from an explicit source language to all other configured languages. JSON body requires `model` and `source_lang`.
- `GET /api/obsidian/status`: reports optional Obsidian CLI availability.

The console currently uses lightweight explicit endpoint contracts rather than
a dedicated schema framework. Add a schema layer only when request/response
objects become large enough that duplicated validation is causing bugs.

The server should remain thin. Translation, navigation, build, and Obsidian behavior should stay in domain modules.

The dev console serves `index.html` with mtime-based query strings for `styles.css`
and `app.js`, so normal refreshes should pick up local UI changes.
