---
lang: en
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter Properties
description: How to use frontmatter in Markdown files
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T19:22:58+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:31+00:00
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
