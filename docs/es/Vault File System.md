---
lang: es
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: Sistema de archivos Vault
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:11:33+00:00
translation_source_body_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_source_metadata_hash: 13ffbb1a33178e1e6ce6e25ff0b126ea5894fe439a76f260c0dca0356812d043
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T19:10:39+00:00
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

Cada carpeta con el prefijo _ es una carpeta del sistema

# ```_attachments```  
Todas las imágenes, PDFs y otros archivos adjuntos

- principalmente para mantener el orden
- para mantener separados los datos de imágenes y texto
- para simplificar la organización posterior con grandes volúmenes de datos
- para simplificar automatizaciones posteriores

❗En este momento, esta carpeta es ignorada por Git; aún se necesita reflexionar sobre cómo gestionaremos los datos de imágenes. Esto significa que los datos de imágenes solo están disponibles localmente por el momento (y, por supuesto, en la página web resultante), pero actualmente no forman parte del repositorio. #todo

# ```_canvas```
Canvas es una función de Obsidian, muy adecuada para mapas mentales y similares.
Dado que solo utilizamos esto dentro de Obsidian, los datos están separados.
