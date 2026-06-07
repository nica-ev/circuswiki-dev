---
lang: uk
translation_id: kaskade-workspace
created: 2025-01-21 18:09:55
update: 2025-05-03 23:22:16
publish: draft
tags:
  - moc
  - dynamic
title: Transkripte des Kaskade Magazines
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Kaskade Workspace.md
translation_source_hash: a7bb0dd4700febf2eceb0bf6831cf1c6ab4a4da17f8bad159eaa666c8eceebd3
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:27:21+00:00
---
>[!info]- Вступ
>Я виріс на журналі "Kaskade". Ще до появи YouTube, до того, як ми могли знайти все в Інтернеті — цей журнал був одним із перших регулярних джерел інформації про жонглювання, цирк, шоу, до яких я мав доступ.
>Коли журнал припинив виходити у 2013 році, це відчувалося як кінець епохи — принаймні для мене.
>Кілька років журнали були доступні для завантаження у форматі PDF, але приблизно з 2017 року сайт став недоступним.
>Я часто згадував невеликі майстер-класи, навчальні посібники чи статті, які надихали мене тоді. Коли через роки я захотів щось перечитати — можливості вже не було.
>
>На щастя, за допомогою Wayback Machine (The Internet Archive) я знайшов точку збереження з 2017 року з повними завантаженнями (це не завжди вдається, особливо враховуючи, що це було близько 3 ГБ PDF-файлів) — повністю з німецьким, англійським та французьким виданнями.
>
>Переглядаючи їх, я зрозумів, що хоча в журналах було багато чудових статей та навчальних посібників — у наш час навряд чи хтось буде переглядати 112 журналів, які просто відксерокопійовані. Ну, хіба що з ностальгічних міркувань =P
>
>Але оскільки шкода втрачати ці знання, я хотів спробувати використати сучасні технології, щоб оцифрувати все це так, щоб воно було корисним і сьогодні.

>[!info]- Як були транскрибовані журнали
>Спочатку я видалив усі сторінки з PDF, які не містили релевантних текстів.
>
>Для власне транскрибування (або OCR) я використовував мультимодальну мовну модель від Google.
>Я використовую ```Gemini 2.0 Pro Experimental 02-05``` з таким запитом:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>та PDF зі сканованим журналом.
>Налаштування: Temperature 0.1 (Важливо, щоб уникнути галюцинацій)
>
>Результат очищується за допомогою ```gemini-2.0-flash-exp``` та такого запиту (а також доданого тексту, який ми витягли):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Результат потім ще раз переглядається вручну та виправляється.
>
>>[!Danger]+ Важливо:
>>Основна увага була зосереджена на вилученні статей, майстер-класів, інтерв'ю тощо.
>>Публікації, такі як, наприклад, приватні оголошення тощо, я відкинув.
>>Вилучення та очищення текстів проводилося за допомогою LLM, тому завжди існує ймовірність, що тексти не були транскрибовані 1:1 або зміст дещо відрізняється від оригіналу. Я намагався мінімізувати кількість помилок, порівнюючи фрагменти тексту вибірково.

<!-- QueryToSerialize: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
<!-- SerializedQuery: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
- [Kaskade 001](docs/de/Kaskade 001.md)
- [Kaskade 002](docs/de/Kaskade 002.md)
- [Kaskade 003](docs/de/Kaskade 003.md)
- [Kaskade 004](docs/de/Kaskade 004.md)
- [Kaskade 005](docs/de/Kaskade 005.md)
- [Kaskade 001](docs/en/Kaskade 001.md)
- [Kaskade 002](docs/en/Kaskade 002.md)
- [Kaskade 003](docs/en/Kaskade 003.md)
- [Kaskade 004](docs/en/Kaskade 004.md)
- [Kaskade 005](docs/en/Kaskade 005.md)
- [Kaskade 001](docs/pl/Kaskade 001.md)
- [Kaskade 002](docs/pl/Kaskade 002.md)
- [Kaskade 003](docs/pl/Kaskade 003.md)
- [Kaskade 004](docs/pl/Kaskade 004.md)
- [Kaskade 005](docs/pl/Kaskade 005.md)
- [Kaskade 001](docs/hu/Kaskade 001.md)
- [Kaskade 002](docs/hu/Kaskade 002.md)
- [Kaskade 003](docs/hu/Kaskade 003.md)
- [Kaskade 004](docs/hu/Kaskade 004.md)
- [Kaskade 005](docs/hu/Kaskade 005.md)
- [Kaskade 001](docs/it/Kaskade 001.md)
- [Kaskade 002](docs/it/Kaskade 002.md)
- [Kaskade 003](docs/it/Kaskade 003.md)
- [Kaskade 004](docs/it/Kaskade 004.md)
- [Kaskade 005](docs/it/Kaskade 005.md)
- [Kaskade 001](docs/nl/Kaskade 001.md)
- [Kaskade 002](docs/nl/Kaskade 002.md)
- [Kaskade 003](docs/nl/Kaskade 003.md)
- [Kaskade 004](docs/nl/Kaskade 004.md)
- [Kaskade 005](docs/nl/Kaskade 005.md)
- [Kaskade 001](docs/el/Kaskade 001.md)
- [Kaskade 002](docs/el/Kaskade 002.md)
- [Kaskade 003](docs/el/Kaskade 003.md)
- [Kaskade 004](docs/el/Kaskade 004.md)
- [Kaskade 005](docs/el/Kaskade 005.md)
- [Kaskade 001](docs/es/Kaskade 001.md)
- [Kaskade 002](docs/es/Kaskade 002.md)
- [Kaskade 003](docs/es/Kaskade 003.md)
- [Kaskade 004](docs/es/Kaskade 004.md)
- [Kaskade 005](docs/es/Kaskade 005.md)

<!-- SerializedQuery END -->

---

# Статті

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| File                                                                              | authors                                           | type     | sub-type | source      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | -------- | ----------- |
| [Die Säulen-Seite](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/en/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/pl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/hu/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/hu/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/hu/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/hu/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/hu/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/hu/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/it/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/it/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/it/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/it/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/it/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/it/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/nl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/nl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/nl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/nl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/nl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/nl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/el/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/el/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/el/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/el/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/el/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/el/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/es/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/es/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/es/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Schummeln!](docs/es/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Schwerkraft - na und!](docs/es/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Zirkus gesucht!](docs/es/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Die Säulen-Seite](docs/uk/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bälle    | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/uk/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Неправильно названі / об'єднані випуски (002 - 004)
>
>Kaskade 002:
>В оригінальному німецькому PDF випуски 2 та 3 об'єднані.
>
>Kaskade 003:
>В оригінальному німецькому PDF тут знаходиться випуск 004.
>
>Kaskade 004:
>Тут відсутня титульна сторінка, я ще не з'ясував, до чого вона належить...
>Виглядає як копія випуску 009, без титульної сторінки.
>
>Виправлення:
>Я розділив PDF Kaskade 002 (оригінал) на 002 та 003.
>Перейменував Kaskade 003 (оригінал) на Kaskade 004.
>А також видалив Kaskade 004 (оригінал).
