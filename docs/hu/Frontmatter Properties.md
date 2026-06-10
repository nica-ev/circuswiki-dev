---
lang: hu
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter tulajdonságok
description: Hogyan használjuk a Frontmattert a Markdown fájlokban
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T22:39:23+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:32+00:00
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
