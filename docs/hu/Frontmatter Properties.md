---
lang: hu
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
translation_updated: 2026-06-06T22:39:23+00:00
---
A következő frontmatter formátumot használjuk:

| Tulajdonság | Adattípus   | Alapérték | Magyarázat                                                                                             |
| ----------- | ----------- | --------- | ------------------------------------------------------------------------------------------------------ |
| created     | Dátum + Idő | auto      | Mikor jött létre a fájl<br>automatikusan bejegyzésre kerül                                              |
| update      | Dátum + Idő | auto      | Mikor lett utoljára módosítva a fájl,<br>automatikusan bejegyzésre kerül                                 |
| publish     | Boolean     | false     | Eldönti, hogy egy fájl közzétételre kerül-e a weboldal részeként                                        |
| tags        | tagek       | -         | Az itt definiált tagek a weboldalon is megjelennek                                                    |
| title       | string      | -         | A cím a weboldalon címsorként jelenik meg a tényleges tartalom előtt,                                   |
| authors     | lista       | -         | az oldal tartalmának szerzői listája                                                                   |
