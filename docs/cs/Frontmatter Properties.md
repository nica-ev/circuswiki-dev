---
lang: cs
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Vlastnosti Frontmatter
description: Jak používat Frontmatter v Markdown souborech
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T18:45:37+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:37+00:00
---
Používáme následující formát frontmatteru

| Vlastnost | Datový typ    | Výchozí hodnota | Vysvětlení                                                                                             |
| ----------- | ----------- | --------------- | ------------------------------------------------------------------------------------------------------ |
| created     | Datum a čas | automaticky     | Kdy byl soubor vytvořen<br>se zadává automaticky                                                       |
| update      | Datum a čas | automaticky     | Kdy byl soubor naposledy změněn,<br>se zadává automaticky                                              |
| publish     | Boolean     | false           | Rozhoduje, zda bude soubor publikován jako součást webu                                                |
| tags        | tagy        | -               | Zde definované tagy se zobrazí i na webu                                                               |
| title       | string      | -               | Název se na webu zobrazí jako nadpis před vlastním obsahem                                            |
| authors     | seznam      | -               | seznam autorů obsahu této stránky                                                                       |
