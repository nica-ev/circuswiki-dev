---
lang: hu
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
translation_updated: 2026-06-06T22:54:48+00:00
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

Minden aláhúzásjellel kezdődő mappa egy rendszermappa.

# ```_attachments```
Minden kép, PDF és egyéb melléklet.

- elsősorban a rend fenntartása érdekében
- a képi és szöveges adatok elkülönítése
- a későbbi, nagy adatmennyiségekkel való egyszerűbb kezelés érdekében
- a későbbi automatizálások egyszerűsítése érdekében

❗Jelenleg ezt a mappát a Git figyelmen kívül hagyja, még gondolkodni kell azon, hogyan kezeljük a képi adatokat. Ez azt jelenti, hogy a képi adatok jelenleg csak lokálisan érhetők el (és természetesen a végeredményként létrejövő weboldalon), de jelenleg nem részei a repositorynak. #todo

# ```_canvas```
A Canvas az Obsidian egyik funkciója, amely alkalmas elmetérképekhez és hasonló dolgokhoz.
Mivel ezt csak az Obsidianon belül használjuk, az adatok külön vannak tárolva.
