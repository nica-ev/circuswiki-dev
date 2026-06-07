---
lang: cs
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
translation_updated: 2026-06-07T18:45:37+00:00
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
