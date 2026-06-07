---
lang: nl
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
translation_updated: 2026-06-06T23:15:47+00:00
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
