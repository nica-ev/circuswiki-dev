---
lang: it
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Proprietà del Frontmatter
description: Come utilizzare il Frontmatter nei file Markdown
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T23:01:25+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:33+00:00
---
Utilizziamo il seguente formato di frontmatter

| Proprietà | Tipo di dato | Predefinito | Spiegazione                                                                                                                               |
| --------- | ------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| created   | Data e ora   | auto        | Quando il file è stato creato<br>viene inserito automaticamente                                                                            |
| update    | Data e ora   | auto        | Quando il file è stato modificato l'ultima volta,<br>viene inserito automaticamente                                                        |
| publish   | Booleano     | false       | Decide se un file deve essere pubblicato come parte del sito web                                                                           |
| tags      | tag          | -           | I tag definiti qui verranno visualizzati anche sul sito web                                                                               |
| title     | string       | -           | Il titolo viene visualizzato sul sito web come intestazione prima del contenuto effettivo,                                                |
| authors   | lista        | -           | un elenco degli autori del contenuto di questa pagina                                                                                     |
