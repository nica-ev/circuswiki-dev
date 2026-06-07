# CircusWiki Tools

Local tooling supports multilingual staging, translation workflow experiments, navigation management, and static site builds.

## Main Commands

```powershell
python tools/stage_multilang.py
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1
powershell -ExecutionPolicy Bypass -File tools/dev_console.ps1
powershell -ExecutionPolicy Bypass -File tools/check.ps1
```

Translation CLI:

```powershell
python tools/translation_cli.py health
python tools/translation_cli.py inspect "docs/de/index.md"
python tools/translation_cli.py translate "docs/de/index.md" --dry-run
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

Current endpoint groups:

- `GET /api/config`: default model, default prompt, and default file-translation language settings.
- `GET /api/health`: legacy source/target health summary.
- `GET /api/vault-health`: multilingual translation matrix.
- `POST /api/translate`: translate one selected file.
- `POST /api/repair-metadata`: deterministic metadata repair for one file.
- `POST /api/batch-plan`: plan batch translation candidates without API calls.
- `POST /api/batch-translate-file`: translate one planned batch item.
- `GET /api/navigation/scan`: inspect Zensical navigation and canonical navigation model state.
- `POST /api/navigation/*`: initialize, preview, apply, or translate navigation labels.

The server should remain thin. Translation, navigation, build, and future Obsidian behavior should stay in domain modules.

The dev console serves `index.html` with mtime-based query strings for `styles.css`
and `app.js`, so normal refreshes should pick up local UI changes.
