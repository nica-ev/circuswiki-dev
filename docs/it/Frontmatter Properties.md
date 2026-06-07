---
lang: it
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
translation_updated: 2026-06-06T23:01:25+00:00
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
