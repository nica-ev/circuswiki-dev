---
lang: cs
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
translation_updated: 2026-06-07T19:14:09+00:00
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

Každá složka s prefixem _ je systémová složka

# ```_attachments```  
Všechny obrázky, PDF soubory a další přílohy

- především pro udržení pořádku
- pro oddělení obrazových a textových dat
- pro zjednodušení pozdější organizace při velkém množství dat
- pro zjednodušení pozdějších automatizací

❗Tuto složku momentálně Git ignoruje, je potřeba ještě promyslet, jak budeme nakládat s obrazovými daty. To znamená, že obrazová data jsou v současné době dostupná pouze lokálně (a samozřejmě na výsledném webu), ale nejsou součástí repozitáře. #todo

# ```_canvas```
Canvas je funkce Obsidianu, která je vhodná pro myšlenkové mapy a podobné věci. 
Jelikož toto používáme pouze v rámci Obsidianu, jsou data oddělená.
