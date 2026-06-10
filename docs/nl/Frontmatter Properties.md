---
lang: nl
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter Eigenschappen
description: Hoe gebruiken we frontmatter in markdown-bestanden
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T23:15:47+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:34+00:00
---
We gebruiken het volgende frontmatter-formaat

| Eigenschap | Datatype    | Standaard | Uitleg                                                                                             |
| ---------- | ----------- | --------- | -------------------------------------------------------------------------------------------------- |
| created    | Datum + Tijd | auto      | Wanneer het bestand is aangemaakt<br>wordt automatisch ingevuld                                    |
| update     | Datum + Tijd | auto      | Wanneer het bestand voor het laatst is gewijzigd,<br>wordt automatisch ingevuld                   |
| publish    | Boolean     | false     | Bepaalt of een bestand wordt gepubliceerd als onderdeel van de website                              |
| tags       | tags        | -         | Hier gedefinieerde tags worden ook op de website weergegeven                                       |
| title      | string      | -         | De titel wordt op de website als kop boven de eigenlijke inhoud weergegeven,                     |
| authors    | lijst       | -         | een lijst van de makers van de inhoud van deze pagina                                              |
