---
lang: en
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter Properties
description: Wie nutzen wir Frontmatter in den Markdown Dateien
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 89bf9ebe8a05134ed70a2642fb5ea6f7381a70cc3e71447f3520e49a039f1264
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T19:22:58+00:00
---
We use the following frontmatter format:

| Property | Data Type   | Default | Explanation                                                                                             |
| -------- | ----------- | ------- | ------------------------------------------------------------------------------------------------------- |
| created  | Date + Time | auto    | When the file was created<br>automatically entered                                                      |
| update   | Date + Time | auto    | When the file was last modified,<br>automatically entered                                               |
| publish  | Boolean     | false   | Determines whether a file is published as part of the website                                           |
| tags     | tags        | -       | Tags defined here will also be displayed on the website                                                 |
| title    | string      | -       | The title will be displayed on the website as a heading before the actual content,                      |
| authors  | list        | -       | a list of the creators of the content on this page                                                      |
