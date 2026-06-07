---
lang: sk
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
translation_updated: 2026-06-07T19:14:10+00:00
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

Každý priečinok s predponou _ je systémový priečinok.

# ```_attachments```
Všetky obrázky, PDF súbory a iné prílohy.

- hlavne na udržanie poriadku
- na oddelenie obrazových a textových dát
- na zjednodušenie neskoršej organizácie pri veľkom objeme dát
- na zjednodušenie neskorších automatizácií

❗V súčasnosti tento priečinok Git ignoruje, ešte je potrebné zvážiť, ako budeme pracovať s obrazovými dátami. To znamená, že obrazové dáta sú momentálne dostupné iba lokálne (a samozrejme na výslednej webovej stránke), ale momentálne nie sú súčasťou úložiska. #todo

# ```_canvas```
Canvas je funkcia Obsidianu, ktorá je vhodná na myšlienkové mapy a podobné veci.
Keďže toto používame iba v rámci Obsidianu, dáta sú oddelené.
