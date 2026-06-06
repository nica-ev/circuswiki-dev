---
created: 2025-05-02 21:56:19
update: 2026-06-06 20:05:53
---

# CircusWiki

CircusWiki is a Markdown-based knowledge base for circus pedagogy, circus arts, movement games, education, and related topics.

The repository is now treated as a clean rebuild:

- content is authored as an Obsidian vault
- public site generation uses Zensical
- old MkDocs Material, Cursor, Task Master, and translation-tooling code has been removed

## Structure

```text
.
|-- docs/          Published Markdown content and shared assets
|   |-- de/        German source pages
|   |-- en/        English pages
|   `-- img/       Shared media assets
|-- site-assets/   Shared generated-site assets copied into each language build
|-- tools/         Local build/staging scripts
|-- .obsidian/     Obsidian vault configuration
|-- _templates/    Obsidian templates
|-- _dataview/     Dataview helper notes and queries
|-- _canvas/       Obsidian canvas files
|-- _inbox/        Drafts, raw notes, and working material
|-- _system/       Vault maintenance notes
|-- zensical.toml     Zensical German/default site configuration
|-- zensical.en.toml  Zensical English site configuration
`-- zensical.pl.toml  Zensical Polish site configuration
```

Language folders use matching relative paths so translations can preserve page context:

```text
docs/de/spiele/example.md
docs/en/spiele/example.md
```

Public URLs do not expose German as a language layer. German is the default root, English is below `/en/`:

```text
/circuswiki/spiele/example/
/circuswiki/en/spiele/example/
/circuswiki/pl/spiele/example/
```

Polish (`pl`) is scaffolded as a third language so multilingual tooling is not
accidentally designed around exactly two languages.

The build creates an ignored `.build/` staging directory so Zensical can see each language as its own root while source content stays organized in `docs/de/` and `docs/en/`. Shared generated-site assets from `site-assets/` are copied into each staged language root.

The language selector is configured with root links, then adjusted in the browser to preserve the current path across languages.

## Local Setup

Create a Python environment and install Zensical:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Preview the German/default site only:

```powershell
python tools/stage_multilang.py
zensical serve
```

This is useful for quick checks, but it serves only `zensical.toml`. The English
site from `zensical.en.toml` is not available through this command.

Preview the compiled multilingual site:

```powershell
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1
```

Open:

```text
http://127.0.0.1:8000/circuswiki/
```

Use this command when checking the language switcher, English pages, or the
same URL shape used on GitHub Pages. It builds all language configs first, then serves
the generated `site/` directory with `/circuswiki/` mapped locally.

Available options:

```powershell
# Use another port if 8000 is busy
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -Port 8765

# Serve the existing site/ output without rebuilding
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -NoBuild

# Bind to all network interfaces for device testing on the local network
powershell -ExecutionPolicy Bypass -File tools/serve_multilang.ps1 -HostAddress 0.0.0.0
```

Expected local URLs:

```text
http://127.0.0.1:8000/circuswiki/
http://127.0.0.1:8000/circuswiki/en/
http://127.0.0.1:8000/circuswiki/pl/
```

Build all language sites:

```powershell
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

## GitHub Pages

The repository includes an Actions-based Pages workflow in `.github/workflows/pages.yml`.
It builds the ignored `site/` directory and uploads it as a GitHub Pages artifact.

The build base path is environment driven:

```powershell
$env:CIRCUSWIKI_SITE_BASE_PATH = "/circuswiki-dev/"
$env:CIRCUSWIKI_SITE_URL = "https://nica-ev.github.io/circuswiki-dev/"
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

If these variables are not set, the build defaults to the main public URL shape:

```text
/circuswiki/
/circuswiki/en/
/circuswiki/pl/
```

For this dev repository, the Pages workflow uses:

```text
https://nica-ev.github.io/circuswiki-dev/
https://nica-ev.github.io/circuswiki-dev/en/
https://nica-ev.github.io/circuswiki-dev/pl/
```

GitHub Pages must be enabled for the repository with "GitHub Actions" as the
Pages source. After that, pushes to `main` or manual workflow runs deploy the
compiled multilingual site.

## Translation Console

The repo includes a local web console for translation workflow experiments and health checks:

Translation architecture notes, including canonical source-language rules and
future fallback behavior, live in `_system/translation-architecture.md`.

```powershell
powershell -ExecutionPolicy Bypass -File tools/dev_console.ps1
```

Open:

```text
http://127.0.0.1:8787
```

The current prototype console can:

- list German source pages from `docs/de/`
- inspect the matching English target path in `docs/en/`
- report missing, outdated, or inconsistent translations
- translate one selected Markdown file through an OpenAI-compatible API

German is the current default site language, but not a permanent source-language
rule. Future translation tooling should translate from each page's canonical
original language as defined by metadata.

During multilingual staging, missing language versions are generated as static
fallback pages. For example, if a German page has no English translation yet,
`/circuswiki/en/example/` should still resolve and show a visible "translation
missing" message with a link to the available source/fallback version.

The console's Vault Health tab includes a deterministic metadata repair tool.
It only fixes values that can be inferred safely, such as `lang`,
`translation_id`, `translation_status`, `translation_source_lang`, and
`translation_source`. It intentionally leaves stale hashes, missing model names,
and missing timestamps visible until translation or review happens.

The Batch Translate tab uses a required plan-first workflow. Planning does not
call the translation API; it only selects candidate files, applies `max_files`,
counts source characters, and shows the candidate list. Running the plan then
processes only those planned files and shows progress file by file.

API credentials are read from local environment variables and are not stored in the repo:

```powershell
$env:OPENROUTER_API_KEY = "..."
$env:OPENROUTER_MODEL = "google/gemini-2.0-flash-001"
```

Optional:

```powershell
$env:OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
```

The same workflow is available from the command line:

```powershell
python tools/translation_cli.py health
python tools/translation_cli.py inspect "docs/de/index.md"
python tools/translation_cli.py translate "docs/de/index.md" --dry-run
python tools/translation_cli.py translate "docs/de/index.md"
```

Translation writes only target files. It splits Markdown into frontmatter and body, sends only the body to the model, then updates these target frontmatter properties deterministically:

```yaml
lang: en
translation_id: ...
translation_source: docs/de/example.md
translation_source_hash: ...
translation_model: ...
translation_status: machine-translated
translation_updated: ...
```

Unknown frontmatter fields are preserved instead of re-dumped.

## Notes

- Obsidian setup is part of the repository and should not be removed during site cleanup.
- Site pages live in language folders below `docs/`.
- Shared images live in `docs/img/`.
- Generated staging and output belong in `.build/` and `site/`; both are ignored by Git.
- The old MkDocs workflow was intentionally removed; this repo does not aim for backward compatibility.
- API keys belong in local environment variables or `.env`, never in committed files.

## License

Content is licensed under CC BY-SA 4.0 unless stated otherwise.
