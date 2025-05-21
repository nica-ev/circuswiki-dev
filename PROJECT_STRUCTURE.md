---
created: 2025-05-04 17:34:32
update: 2025-05-22 00:49:28
---

# Project Structure Overview

This document outlines the directory structure of the `circuswiki-dev` workspace.

## Root Directory (`circuswiki-dev`)

The root directory contains the main project components, configuration files, and potentially shared resources or documentation.

```
circuswiki-dev/
├── .git/               # Git version control data
├── .cursor/            # Cursor IDE specific files (rules, etc.)
├── .obsidian/          # Obsidian vault configuration (if used)
├── docs/               # Project documentation (rendered via MkDocs)
├── scripts/            # General utility scripts (e.g., PRD)
├── src/                # Main Python source code for the *root* project (if any)
├── tasks/              # Task management files (Task Master)
├── tests/              # Python tests for the *root* project (if any)
├── translation-py/     # Sub-project: Markdown Translation Script (see below)
├── .gitignore          # Specifies intentionally untracked files for Git
├── LICENSE             # Project license information
├── mkdocs.yml          # MkDocs configuration file
├── README.md           # Main project README
├── requirements.txt    # Python dependencies for the root project
└── ...                 # Other configuration files, directories
```

## Sub-project: Markdown Translation Script (`translation-py`)

This directory contains a distinct Python project focused specifically on the Markdown translation tool outlined in `scripts/prd.txt`.

```
translation-py/
├── src/                # Source code for the translation tool
│   ├── processing/     # Core logic for Markdown parsing, extraction, reconstruction
│   ├── services/       # Integration with external translation APIs (e.g., DeepL)
│   ├── utils/          # Helper functions (config loading, hashing, normalization)
│   └── main.py         # Entry point for the command-line tool
├── tests/              # Pytest tests specific to the translation tool
│   ├── processing/
│   ├── services/
│   └── utils/
├── .env.example        # Example environment file for API keys
├── settings.example.toml # Example configuration file (alternative to settings.txt)
├── requirements.txt    # Dependencies specific to the translation tool (if different from root)
└── README.md           # README specific to the translation tool
```

*(Note: The exact internal structure of `translation-py` might need further exploration or refinement based on existing code.)*

## Key Considerations

*   **Isolation:** The `translation-py` project is developed somewhat independently, though it resides within the main workspace.
*   **Dependencies:** It might have its own `requirements.txt`, potentially duplicating or extending the root `requirements.txt`.
*   **Imports:** Code within `translation-py` needs to import modules from its *own* `src` directory (e.g., `from src.utils import ...`). Imports from the *root* `src` directory might require careful path configuration if needed.
*   **Testing:** Running `pytest` from the root directory requires configuration (e.g., via `pyproject.toml` or `pytest.ini`) to correctly discover tests and source files in *both* the root `tests`/`src` and `translation-py/tests`/`translation-py/src` locations without import errors. 

...