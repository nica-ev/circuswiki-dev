---
lang: uk
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: Файлова система Vault
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:33:02+00:00
translation_source_body_hash: 3bc0110134e109236bc99536708bc16f7b492cf3d0fbb5e05bf12deef33d3de2
translation_source_metadata_hash: 13ffbb1a33178e1e6ce6e25ff0b126ea5894fe439a76f260c0dca0356812d043
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T19:10:40+00:00
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

Кожна папка з префіксом _ є системною папкою.

# ```_attachments```
Усі зображення, PDF-файли та інші вкладення.

- головним чином для підтримки порядку
- для розділення даних зображень і тексту
- для спрощення подальшої організації при великих обсягах даних
- для спрощення подальших автоматизацій

❗Наразі цей каталог ігнорується Git. Потрібно ще обміркувати, як ми будемо працювати з даними зображень. Це означає, що дані зображень наразі доступні лише локально (і, звісно, на кінцевій вебсторінці), але вони не є частиною репозиторію. #todo

# ```_canvas```
Canvas — це функція Obsidian, яка добре підходить для створення ментальних карт та подібного.
Оскільки ми використовуємо це лише в межах Obsidian, дані зберігаються окремо.
