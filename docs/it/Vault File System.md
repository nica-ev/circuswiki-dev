---
lang: it
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: File System Vault
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T23:09:32+00:00
translation_source_body_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_source_metadata_hash: 13ffbb1a33178e1e6ce6e25ff0b126ea5894fe439a76f260c0dca0356812d043
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T19:10:37+00:00
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

Ogni cartella con il prefisso _ è una cartella di sistema

# ```_attachments```  
Tutte le immagini, i PDF e altri allegati

- principalmente per mantenere l'ordine
- per mantenere separati i dati di immagini e testo
- per semplificare l'organizzazione futura con grandi quantità di dati
- per semplificare le future automazioni

❗Al momento questa cartella viene ignorata da Git, è ancora necessario riflettere su come gestire i dati delle immagini. Ciò significa che i dati delle immagini sono attualmente disponibili solo localmente (e naturalmente nel sito web risultante), ma al momento non fanno parte del repository. #todo

# ```_canvas```
Canvas è una funzionalità di Obsidian, adatta per mappe mentali e simili.
Poiché lo utilizziamo solo all'interno di Obsidian, i dati sono separati.
