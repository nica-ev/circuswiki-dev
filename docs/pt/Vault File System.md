---
lang: pt
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
translation_updated: 2026-06-07T19:14:06+00:00
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
