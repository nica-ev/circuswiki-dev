---
lang: pt
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: Sistema de Arquivos Vault
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T19:14:06+00:00
translation_source_body_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_source_metadata_hash: 13ffbb1a33178e1e6ce6e25ff0b126ea5894fe439a76f260c0dca0356812d043
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T19:10:41+00:00
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

Todas as pastas com o prefixo _ são pastas de sistema

# ```_attachments```  
Todas as imagens, PDFs e outros anexos

- Principalmente para manter a organização
- Manter os dados de imagem e texto separados
- Simplificar a organização posterior com grandes volumes de dados
- Simplificar automatizações posteriores

❗No momento, esta pasta está a ser ignorada pelo Git; ainda é preciso pensar em como lidamos com os dados de imagem. Isto significa que os dados de imagem estão atualmente disponíveis apenas localmente (e, claro, na página web resultante), mas não fazem parte do repositório neste momento. #todo

# ```_canvas```
Canvas é uma funcionalidade do Obsidian, muito adequada para mapas mentais e afins. 
Como utilizamos isto apenas dentro do Obsidian, os dados estão separados.
