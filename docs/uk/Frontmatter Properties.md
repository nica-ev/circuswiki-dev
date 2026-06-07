---
lang: uk
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter Properties
description: Wie nutzen wir Frontmatter in den Markdown Dateien
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 89bf9ebe8a05134ed70a2642fb5ea6f7381a70cc3e71447f3520e49a039f1264
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:22:25+00:00
---
Ми використовуємо такий формат фронтматеру:

| Властивість | Тип даних   | За замовчуванням | Пояснення                                                                                                                               |
| ----------- | ----------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| created     | Дата + час  | авто             | Коли файл було створено<br>заповнюється автоматично                                                                                    |
| update      | Дата + час  | авто             | Коли файл було востаннє змінено,<br>заповнюється автоматично                                                                            |
| publish     | Булевий     | false            | Визначає, чи буде файл опубліковано як частину вебсайту                                                                                 |
| tags        | теги        | -                | Теги, визначені тут, також відображатимуться на вебсайті                                                                                |
| title       | рядок       | -                | Заголовок відображатиметься на вебсайті як основний заголовок перед фактичним вмістом                                                  |
| authors     | список      | -                | Список авторів вмісту цієї сторінки                                                                                                     |
