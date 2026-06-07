---
lang: es
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
translation_updated: 2026-06-07T14:11:33+00:00
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
