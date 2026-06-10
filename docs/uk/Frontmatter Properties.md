---
lang: uk
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Властивості Frontmatter
description: Як використовувати Frontmatter у файлах Markdown
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:22:25+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:35+00:00
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
