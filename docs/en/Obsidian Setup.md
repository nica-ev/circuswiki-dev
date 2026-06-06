---
lang: en
translation_id: obsidian-setup
publish: true
tags: 
title: Obsidian Setup
created: 2025-01-23 01:38:52
update: 2025-03-11 02:05:46
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Obsidian Setup.md
translation_source_hash: bd30270abdfc27045080229792d0b5955c0cf91140aac9ca4859d4819bd61b16
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T19:27:35+00:00
---
Obsidian is extremely customizable, which can be a challenge for newcomers.
We provide a base setup that can be used as is, including plugins, themes, and their finely tuned settings.
This is a foundational setup and can be further adjusted to anyone's personal preferences.
We're offering a ready-to-use solution that we will document and explain here.

## Terms Used
**Vault** - a collection of markdown files and images that form the knowledge base.

## Plugins

- Advanced Canvas
- BRAT
- Better Word Count
- Clear Unused Images
- Dataview
- Dataview Serializer
- Emoji Toolbar
- Linter
- Note Toolbar
- Tag Wrangler
- Templater
- Beautitab
- Omnisearch
- Status Bar Organizer
- Workspaces Plus
- Sortable

### Advanced Canvas
Provides access to many new functionalities and styling options for Canvas.

### BRAT
Required for installing unofficial plugins or plugins not registered in Obsidian's ecosystem, specifically:
- Dataview Serializer
- Sortable

### Better Word Count
Primarily used for its ability to display the word/character count of highlighted text.
This is visible in the status bar.

### Beautitab
Purely cosmetic, it provides a customizable "empty new tab" page.

### Clear Unused Images
As the name suggests, this helps organize the vault by identifying unused images.

❗I've excluded the subfolder ```/site/``` so it doesn't delete images from the built website (which isn't a problem, more of an annoyance).

❗Be careful when using the clear attachments command, as this will always delete ```mkdocs.yml``` and the ```license.``` If this happens, the files are in the .trash folder and can be recovered, but it's easy to overlook.

### Dataview
Enables SQL-like queries on the vault.

### Dataview Serializer
Converts Dataview results into markdown.
This helps in reusing the results of Dataview queries within your actual notes.

### Emoji Toolbar
Provides easy access to emojis.
**Hotkey set to: ALT-E**
😍

### Linter
Cleans up markdown files and frontmatter data.
Helps maintain a consistent format.

### Note Toolbar
Enables customizable toolbars at the top of a note, which can be defined at the folder or file level.

### Tag Wrangler
Offers additional options for working with tags, such as renaming tags.
This aids in organizing the vault.

### Templater
Allows for customizable templates that can be inserted manually or based on conditions (like when creating a note).

### Status Bar Organizer
Allows you to hide items from the status bar.

### Sortable
Enables sorting of tables (both markdown and Dataview tables) by clicking on their headers.

### Workspaces Plus
Allows for easy quick-switching of workspaces from the status bar.

## Vault File System

[Vault File System](Vault%20File%20System.md){ .md-button }
