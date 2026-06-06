---
lang: pl
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: Vault File System
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: d418e7c5944943e87dc15e652b5d223265fb03145f2906ae04de273b545ebae4
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T20:24:44+00:00
---
```code
/_attachments/        
/_canvas/             
/_dataview/           
/_inbox/
/_sonstiges/
/_templates/
/docs/
/site/
license
mkdocs.yml
readme.md
```

Każdy folder z prefiksem _ jest folderem systemowym

# ```_attachments```  
Wszystkie obrazy, pliki PDF i inne załączniki

- głównie w celu utrzymania porządku
- oddzielenia danych graficznych od tekstowych
- ułatwienia późniejszej organizacji przy dużych ilościach danych
- uproszczenia późniejszych automatyzacji

❗Obecnie ten folder jest ignorowany przez Git. Wymaga to dalszych przemyśleń, jak będziemy postępować z danymi graficznymi. Oznacza to, że dane graficzne są obecnie dostępne tylko lokalnie (i oczywiście na stronie internetowej), ale nie są częścią repozytorium. #todo

# ```_canvas```
Canvas to funkcja Obsidian, która dobrze nadaje się do tworzenia map myśli i podobnych struktur.
Ponieważ korzystamy z niej tylko w obrębie Obsidian, dane są odseparowane.
