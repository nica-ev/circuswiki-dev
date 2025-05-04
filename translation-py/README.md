# Markdown Content Translator (Python)

This tool facilitates the translation of Markdown files using various LLM APIs (like DeepL, OpenAI, etc.).

## Features

- (To be added)

## Setup

- (To be added)

## Usage

- (To be added)

## Usage Examples

Basic usage from the command line:

```bash
python src/cli.py --settings ../config/settings.txt --env ../config/translate.env
```

## Limitations

### Inline Formatting Preservation

**Current Status:** The current version of the Markdown reconstruction process **does not** preserve inline formatting elements (like **bold**, *italic*, `code spans`, or [links](...) within text) during translation.

**Reason:** The reconstruction algorithm currently replaces entire inline text segments within block elements (like paragraphs or list items) with the translated text. This simplification ensures block-level structure is maintained but sacrifices the granularity needed to reapply inline formatting to the translated content.

**Example:**

**Original Markdown:**
```markdown
This is a paragraph with **bold text** and an *italic word*.
```

**Extracted Segments:**
1. `This is a paragraph with `
2. `bold text`
3. ` and an `
4. `italic word`
5. `.`

**Simulated Translation (French):**
1. `Ceci est un paragraphe avec `
2. `texte en gras`
3. ` et un `
4. `mot en italique`
5. `.`

**Current Reconstructed Markdown (Incorrect Formatting):**
```markdown
Ceci est un paragraphe avec texte en gras et un mot en italique.
```
*(Note: The bold and italic formatting is lost.)*

**Target Reconstructed Markdown (Future State):**
```markdown
Ceci est un paragraphe avec **texte en gras** et un *mot en italique*.
```

**Resolution:** This limitation is tracked in [Task 10, Subtask 4](tasks/task_10.md#subtask-4-implement-special-element-preservation-logic) and will be addressed by implementing a more sophisticated reassembly mechanism that handles inline elements correctly. Until subtask 10.4 is completed, users should expect inline formatting within translated segments to be lost.

## Development Setup

- (To be added) 