---
lang: uk
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
translation_updated: 2026-06-07T14:33:02+00:00
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
