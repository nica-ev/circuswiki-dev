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
|-- zensical.toml  Zensical German/default site configuration
`-- zensical.en.toml  Zensical English site configuration
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
```

The build creates an ignored `.build/` staging directory so Zensical can see each language as its own root while source content stays organized in `docs/de/` and `docs/en/`. Shared generated-site assets from `site-assets/` are copied into each staged language root.

The language selector is configured with root links, then adjusted in the browser to preserve the current path across languages.

## Local Setup

Create a Python environment and install Zensical:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Preview the German default site:

```powershell
python tools/stage_multilang.py
zensical serve
```

Build both language sites:

```powershell
powershell -ExecutionPolicy Bypass -File tools/build_multilang.ps1
```

## Notes

- Obsidian setup is part of the repository and should not be removed during site cleanup.
- Site pages live in language folders below `docs/`.
- Shared images live in `docs/img/`.
- Generated staging and output belong in `.build/` and `site/`; both are ignored by Git.
- The old MkDocs workflow was intentionally removed; this repo does not aim for backward compatibility.

## License

Content is licensed under CC BY-SA 4.0 unless stated otherwise.
