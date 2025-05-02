## Product Design Document: Markdown Content Translator

**1. Introduction**

This document outlines the design for a command-line tool that automates the translation of Markdown (`.md`) files. The tool scans a specified source directory, identifies original content files, parses them to isolate translatable text while preserving Markdown structure (like code blocks, links, etc.), sends the text to a configurable Language Model (LLM) API (initially DeepL, with potential for others) for translation, and reconstructs the translated content into new Markdown files in a specified output directory. Change detection using content hashing ensures only new or modified files are translated. Configuration is managed through external files for directories, languages, API keys, and operational modes.

**2. Goals**

*   **Automated Translation:** Provide a scriptable way to translate collections of Markdown files.
*   **Structure Preservation:** Maintain Markdown formatting, including code blocks, links, lists, headers, and YAML frontmatter, during the translation process.
*   **Efficient Updates:** Only translate files that are new or whose content has changed since the last translation, using a content hash comparison.
*   **Configurability:** Allow users to easily configure input/output directories, target languages, and API endpoints/providers via external files.
*   **Extensibility:** Design with the possibility of supporting multiple LLM translation providers (e.g., DeepL, OpenAI, Gemini, OpenRouter).
*   **Secure Credential Management:** Keep API keys separate from the main configuration and codebase.
*   **Testability:** Include a test/dry-run mode to simulate the process without incurring API costs.

**3. Non-Goals**

*   A graphical user interface (GUI).
*   Real-time translation or interactive editing features.
*   Support for file formats other than Markdown.
*   Complex version control integration beyond hash checking.
*   Management of translation memory or terminology databases (beyond what the LLM API might inherently do).

**4. User Stories**

*   **As a documentation maintainer,** I want to automatically translate my project's English Markdown documentation into German and Spanish, so I can reach a wider audience without manual copy-pasting.
*   **As a developer,** I want to configure the tool to use my DeepL API key and specify source/target directories, so I can integrate translation into my content pipeline.
*   **As a content creator,** I want the tool to skip files that haven't changed since the last run, so I don't waste time or API credits re-translating content.
*   **As a developer,** I want to run the tool in a test mode that mimics the file processing and parsing logic but doesn't call the actual translation API, so I can debug the workflow without cost.
*   **As a maintainer,** I want the tool to correctly handle code blocks, inline code, and URLs within my Markdown files, ensuring they are not translated.
*   **As a documentation maintainer,** I want the tool to translate the title and description fields in my YAML frontmatter, so the translated pages have localized metadata.
*   **As a content creator using Obsidian,** I want the tool to preserve my [[WikiLinks]] and not attempt to translate the link target, but I want the alias in [[LinkTarget|This Alias]] to be translated.

**5. Functional Requirements**

*   **FR1: Configuration Loading:**
    *   The tool MUST read settings.txt to determine INPUT_DIR, OUTPUT_DIR, TARGET_LANGUAGES (list), TEST_MODE (boolean), YAML_TRANSLATE_FIELDS (comma-separated list of YAML keys whose string values should be translated), and API_PROVIDER.
    *   The tool MUST read translate.env to load necessary API keys (e.g., DEEPL_API_KEY).
*   **FR2: Directory Scanning:**
    *   The tool MUST recursively scan the `INPUT_DIR` for all files ending with the `.md` extension.
*   **FR3: File Processing:**
    *   For each `.md` file found:
        *   **FR3.1:** Parse the YAML frontmatter into a data structure (e.g., a dictionary).
        *   **FR3.2:** Check if the `orig` flag is `true`. If not, skip the file.
        *   **FR3.3:** Calculate Hashes:
            *   **`content_hash`**: Calculate a hash of the file's main content (everything *after* the closing `---` of the frontmatter, potentially normalized). Use a consistent algorithm (e.g., SHA-256).
            *   **`yaml_hash`**: Calculate a hash based on the content of the parsed YAML frontmatter (excluding the `content_hash`, `yaml_hash` and `updated` fields themselves). This ensures changes to *any* metadata field are detected. `updated`isnt crucial so there is no need to trigger a translation.
        *   **FR3.4:** Compare calculated hashes (`content_hash`, `yaml_hash`) with the corresponding values stored in the source file's frontmatter.
        *   **FR3.5:** Identify YAML fields needing translation: Check keys in the parsed frontmatter against the `YAML_TRANSLATE_FIELDS` list from settings. Store the string values of matching keys for potential later translation.
        *   **FR3.6:** Determine Action Based on Hashes:
            *   If `content_hash` is missing or differs from the stored `content_hash`: Proceed to full content extraction, translation, and reconstruction (FR4, FR5, FR6, FR7). This handles changes in the main Markdown body.
            *   If `yaml_hash` is missing or differs from the stored `yaml_hash`: Proceed to YAML processing and translation update (subset of FR5, FR7). This handles changes only within the frontmatter.
        *   **FR3.7:** If both calculated hashes match the stored hashes, skip processing for this file entirely.
*   **FR4: Markdown Parsing & Content Extraction:**
    *   **FR4.1:** Utilize a Markdown parser capable of generating a detailed Abstract Syntax Tree (AST) or a token stream (e.g., markdown-it-py is recommended for its extensibility). The parser MUST be configured to handle common extensions (like tables, footnotes) and pass through raw HTML blocks without modification.
    *   **FR4.2:** Traverse the AST/token stream. Identify and extract text segments that are safe for translation. This includes:
        *   Paragraph content
        *   List item content
        *   Table cell content (excluding formatting)
        *   Header content
        *   Emphasis/Strong text content
        *   Link text (the part in [text](url))
        *   Image alt text (the part in ![alt text](url))
        *   Aliases in specific non-standard links (e.g., the Alias part of [[LinkTarget|Alias]]) if custom parsing rules are implemented (see FR4.4).
    *   **FR4.3:** Identify and explicitly mark segments/nodes that MUST NOT be translated. This includes:
            *   Code blocks (fenced and indented)
            *   Inline code ( )
            *   URLs (in links, images, or autolinks)
            *   HTML tags and content within HTML blocks.
            *   Specific non-standard syntax structures like the entirety of [[LinkTarget]] or the target and attributes part of [[LinkTarget|Alias]].{attribute}.
            *   YAML frontmatter section (handled separately).
    *   **FR4.4:** (Potential Extension): Implement custom parsing rules or plugins for the chosen parser (e.g., using markdown-it-py plugins) to specifically recognize and handle non-standard syntax like Obsidian's [[LinkTarget|Alias]]. This rule should isolate the Alias part for translation while preserving the rest of the structure ([[LinkTarget|...]]). If custom rules are not implemented, the entire [[...]] block should be treated as non-translatable (FR4.3).
    *   **FR4.5:** Aggregate the extracted translatable text segments from both the Markdown body (FR4.2) and the designated YAML fields (FR3.5) into a list for the translation service. Maintain mapping to know where each translated segment belongs (e.g., paragraph X, list item Y, YAML key Z).
*   **FR5: Translation Execution:**
    *   For each `TARGET_LANGUAGE` specified in `settings.txt`:
        *   **FR5.1:** If TEST_MODE is true, simulate translation by returning the original text segments. Skip API calls.
        *   **FR5.2:** If TEST_MODE is false, send the aggregated list of translatable text segments (from Markdown body and YAML fields) to the configured LLM API.
        *   **FR5.3:** Handle potential API errors gracefully (e.g., log the error, skip the file for that language).
*   **FR6: Markdown Reconstruction:**
    *   **FR6.1:** Using the mapping from FR4.5, replace the original text segments in the AST/token stream representation and the stored YAML data structure with the corresponding translated segments received from the API (or simulated text).
    *   **FR6.2:** Reconstruct the full Markdown content from the modified AST/token stream, ensuring that non-translated elements (code, HTML, URLs, preserved non-standard syntax) and original formatting are perfectly maintained.
*   **FR7: Output File Generation:**
    *   **FR7.1:** Construct the output file path (e.g., OUTPUT_DIR/<lang_code>/<relative_path_from_input_dir>/<filename>.md). 
    *   **FR7.2:** Create necessary subdirectories within OUTPUT_DIR.
    *   **FR7.3:** Create the YAML frontmatter for the translated file:
        * Include translated values for keys listed in YAML_TRANSLATE_FIELDS (taken from the modified YAML data structure in FR6.1).
        * Include untranslated values for other keys copied from the original frontmatter (unless they are technical fields).
        * Set lang to the TARGET_LANGUAGE code (e.g., DE, ES).
        * Set `orig` to `false`.
        * Include the `content_hash` and `yaml_hash` from the source file it was generated from, for reference.
    *   **FR7.4:** Write the generated frontmatter and the reconstructed, translated Markdown content (from FR6.2) to the output file.
    *   **FR7.5:** Handle YAML-Only Updates: If only the `yaml_hash` changed (per FR3.6), instead of generating a completely new file, the tool MUST read the existing translated file for the target language, update *only* its YAML frontmatter (translating required fields, copying others as per FR7.3), and rewrite the file. The existing Markdown body remains unchanged.

*   **FR8: Source File Update:**
    *   After calculating the hashes for a source file (`FR3.3`), regardless of whether translation occurred, update its frontmatter to store the newly calculated `content_hash` and `yaml_hash` values. This ensures the source file always reflects the latest state used for comparison.


**6. Non-Functional Requirements**

*   **NFR1: Performance:** The tool should process a moderate number of files (e.g., 100 files) in a reasonable timeframe, with the primary bottleneck expected to be the external API calls. Consider potential for batching API requests if the provider supports it. The two-hash system helps avoid unnecessary API calls for YAML-only changes.
*   **NFR2: Reliability:** The tool should handle common errors like file not found, invalid Markdown, network issues, and API errors gracefully, logging issues without crashing.
*   **NFR3: Maintainability:** The codebase should be well-structured, potentially separating concerns like file handling, configuration, parsing, API interaction, and reconstruction into different modules or classes. The logic differentiating full updates from YAML-only updates should be clear.
*   **NFR4: Security:** API keys must not be hardcoded or checked into version control. Loading from a `.env` file is the minimum requirement.

**7. Technical Design & Architecture**

*   **Language:** Python 3.x is recommended due to its strong libraries for file handling, text processing, API requests, and Markdown parsing.
*   **Key Libraries:**
    *   `python-dotenv`: For loading `.env` files.
    *   `PyYAML` or `ruamel.yaml`: For parsing and updating YAML frontmatter (preserving comments/style if possible with `ruamel.yaml`).
    *   `markdown-it-py`: Strongly recommended due to its plugin architecture, which is ideal for handling standard Markdown, extensions, HTML, and potentially adding rules for non-standard syntax like Obsidian links.
    *   `requests` or `httpx`: For making HTTP calls to translation APIs.
    *   Official `deepl-python` library (if available and suitable) or direct API calls.
    *   `hashlib`: For calculating content hashes.
    *   `os` / `pathlib`: For file system operations.
*   **Core Components:**
    *   `ConfigLoader`: Reads `settings.txt` and `translate.env`.
    *   `FileManager`: Scans directories, reads/writes files, updates source file hashes.
    *   `MarkdownProcessor`:
        *   Uses a Markdown parser library.
        *   Extracts frontmatter.
        *   Calculates content hash.
        *   Walks the AST/token stream to identify translatable vs. non-translatable nodes.
        *   Reconstructs Markdown from the (modified) AST/token stream.
    *   `TranslationService`:
        *   Abstracts the interaction with the LLM API.
        *   Contains logic for specific providers (e.g., `DeepLTranslator`, potentially `OpenAITranslator`).
        *   Handles API key injection and request formatting.
        *   Implements the `TEST_MODE` logic.
*   **Workflow:**
    1.  Load configuration (`ConfigLoader`).
    2.  Initialize `FileManager` and `TranslationService`.
    3.  `FileManager` scans `INPUT_DIR` recursively for `.md` files.
    4.  For each file:
        a.  `FileManager` reads file content.
        b.  `MarkdownProcessor` extracts frontmatter and content.
        c.  `FileProcessor` checks `orig` flag. Skip if false.
        d.  `FileProcessor` calculates `content_hash` and `yaml_hash`.
        e.  `FileProcessor` compares calculated hashes with stored hashes from frontmatter.
        f.  If `content_hash` differs (or missing):
            i.  `FileProcessor` parses content, extracts translatable Markdown segments + specified YAML fields.
            ii. For each `TARGET_LANGUAGE`:
                1. `TranslationService` requests translation for all segments.
                2. `FileProcessor` reconstructs full Markdown document with translated text.
                3. `FileManager` writes the new translated file (including full frontmatter).
        g.  Else if `yaml_hash` differs (or missing):
            i.  `FileProcessor` extracts only specified YAML fields for translation.
            ii. For each `TARGET_LANGUAGE`:
                1. `TranslationService` requests translation *only* for the YAML fields.
                2. `FileManager` reads existing translated file, updates its YAML frontmatter with new translated/copied values, and rewrites it.
        h.  `FileManager` updates `content_hash` and `yaml_hash` in the source file's frontmatter.
    5. Log completion or errors.

**8. Configuration Details**

*   **`settings.txt` (Example - Key-Value format):**
    ```ini
    INPUT_DIR=./docs
    OUTPUT_DIR=./translated_docs
    # Comma-separated list of DeepL target language codes
    TARGET_LANGUAGES=DE,FR,ES
    # Comma-separated list of YAML keys whose values should be translated
    YAML_TRANSLATE_FIELDS=title,description,seo_title
    # API Provider identifier (e.g., DeepL, OpenAI) - for future extension
    API_PROVIDER=DeepL
    # Set to true to skip actual API calls
    TEST_MODE=false
    ```
    *(Alternatively, JSON or YAML could be used for `settings.txt`)*


*   **`translate.env` (Example):**
    ```bash
    # DeepL API Key (use Free or Pro key)
    DEEPL_API_KEY=your_deepl_api_key_here
    # OPENAI_API_KEY=your_openai_key_here # Example for future extension
    ```
    *This file MUST be added to `.gitignore`.*

**9. Error Handling**

*   Log errors to standard error or a dedicated log file.
*   File I/O errors (permissions, not found): Log and skip the affected file.
*   Configuration errors (missing keys, invalid values): Log and exit gracefully.
*   Parsing errors (invalid Markdown/YAML): Log and skip the affected file.
*   API errors (network, authentication, rate limits, invalid requests): Log the error, potentially retry (with backoff) for transient errors, and skip the file/language combination if persistent.

**10. Future Considerations / Open Questions**

*   **API Batching:** Investigate if selected APIs (like DeepL) support translating multiple text segments in a single request for efficiency.
*   **More Sophisticated Parsing:** Handle edge cases in Markdown (e.g., HTML embedded in Markdown, complex nested structures).
*   **Pluralization/Context:** Standard LLM calls translate segments in isolation. Context might be lost. Could prompts be engineered to provide more context? (Likely complex).
*   **API Provider Abstraction:** Formalize the interface for `TranslationService` to make adding new providers (OpenAI, Gemini, etc.) easier.
*   **Progress Indication:** For large sets of files, provide progress feedback (e.g., files processed, estimated time).
*   **Caching:** Optionally cache successful translations (source text + target lang -> translated text) to avoid re-translation costs if the *exact same* segment appears in multiple files (could be complex to manage invalidation).
*   **Orphaned File Detection:** Consider adding a separate mode or utility script to scan the `OUTPUT_DIR` and identify translated files whose corresponding `orig:true` source file no longer exists or is marked `orig:false`. This helps manage cleanup.
*   **Forced YAML Re-evaluation:** Implement a command-line flag (e.g., `--force-yaml-update`) that skips the hash check and forces the tool to re-process the YAML frontmatter (FR7.5) for all source files. This is useful if the `YAML_TRANSLATE_FIELDS` setting changes or to ensure consistency.
*   **YAML Hash Granularity:** The current design hashes the whole frontmatter (minus hashes). If performance becomes an issue due to frequent non-translatable YAML changes triggering updates, consider making the `yaml_hash` *only* cover fields listed in `YAML_TRANSLATE_FIELDS`. This would revert to the behavior where non-translatable YAML changes aren't automatically propagated.
*   **Non-Standard Syntax Handling:** Define the priority and approach for supporting various non-standard syntaxes. Should it rely on markdown-it-py plugins? Is a configuration needed to enable/disable specific syntax support?
*   **HTML Content Translation:** Currently passing through HTML. Is there ever a case where text within HTML tags needs translation? This adds significant complexity (requires HTML parsing). Assume "no" for now.
*   **Context Preservation:** How critical is preserving context between adjacent text segments sent to the LLM? Could concatenating smaller adjacent blocks (e.g., multiple paragraphs) before sending improve translation quality, even if it complicates reconstruction slightly? Requires investigation based on LLM behavior.
