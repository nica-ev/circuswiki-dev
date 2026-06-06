---
lang: pl
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
translation_source_hash: ae8f36f6540d80a5be5070905e4aa7251d85170462ef6b36f1c6440762b237f2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T20:19:41+00:00
---
>[!info]- Wprowadzenie
>Dorastałem z „Kaskadą”. Zanim pojawił się YouTube, zanim mogliśmy znaleźć wszystko w Internecie – to czasopismo było jednym z pierwszych regularnych źródeł informacji, jakie trafiły w moje ręce na temat żonglerki, cyrku i występów.
>Kiedy w 2013 roku czasopismo zostało zamknięte, poczułem, że to koniec pewnej ery – przynajmniej dla mnie.
>Przez kilka lat czasopisma były dostępne do pobrania w formacie PDF, ale około 2017 roku strona została wyłączona.
>Często przypominałem sobie małe warsztaty, tutoriale lub artykuły, które mnie wtedy inspirowały. Kiedy po latach chciałem coś ponownie przeczytać – nie było już takiej możliwości.
>
>Dzięki Wayback Machine (The Internet Archive) na szczęście znalazłem punkt kontrolny z 2017 roku z kompletnymi plikami do pobrania (nie zawsze tak jest, zwłaszcza że było to około 3 GB plików PDF) – w tym wydania niemieckie, angielskie i francuskie.
>
>Przeglądając je, zdałem sobie sprawę, że chociaż w czasopismach ukrytych było wiele wspaniałych artykułów i tutoriali – to w dzisiejszych czasach mało kto przeglądałby 112 czasopism, które są jedynie kserokopiami. No cóż, chyba że ktoś ma sentymentalne zainteresowania =P
>
>Ponieważ szkoda byłoby zmarnować tę wiedzę, postanowiłem spróbować wykorzystać obecną technologię do zdigitalizowania tego wszystkiego w sposób, który będzie użyteczny również dzisiaj.

>[!info]- Jak transkrybowano czasopisma
>Najpierw usunąłem z PDF wszystkie strony, które nie zawierały istotnych tekstów.
>
>Do właściwej transkrypcji (lub OCR) użyłem multimodalnego modelu językowego Google.
>Używam ```Gemini 2.0 Pro Experimental 02-05``` z promptem:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>oraz PDF ze zeskanowanym czasopismem.
>Ustawienia: Temperatura 0.1 (Ważne, aby uniknąć halucynacji)
>
>Wynik jest czyszczony za pomocą ```gemini-2.0-flash-exp``` i następującego promptu (wraz z dołączonym tekstem, który wyodrębniliśmy):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Wynik jest następnie ponownie przeglądany i poprawiany ręcznie.
>
>>[!Danger]+ Ważne:
>>Skupiono się na wyodrębnianiu artykułów, warsztatów, wywiadów itp.
>>Ogłoszenia drobne itp. zostały odrzucone.
>>Ekstrakcja i czyszczenie tekstów odbywało się za pomocą LLM, dlatego zawsze istnieje możliwość, że teksty nie zostały przetranskrybowane 1:1 lub treść nieznacznie odbiega od oryginału. Starałem się zminimalizować wskaźnik błędów, porównując fragmenty tekstu wyrywkowo.

<!-- QueryToSerialize: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
<!-- SerializedQuery: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
- [Kaskada 002](docs/de/Kaskade 002.md)
- [Kaskade 001](docs/de/Kaskade 001.md)
- [Kaskada 003](docs/de/Kaskade 003.md)
- [Kaskade 004](docs/de/Kaskade 004.md)
- [Kaskada 005](docs/de/Kaskade 005.md)

<!-- SerializedQuery END -->

---

# Artykuły

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Plik                                                                              | autorzy                                           | typ      | podtyp | źródło      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | ------ | ----------- |
| [Die Säulen-Seite](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Piłki  | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artykuł  | \-     | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artykuł  | \-     | Kaskade 001 |
| [Schummeln!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Piłki  | Kaskade 001 |
| [Schwerkraft - na und!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artykuł  | \-     | Kaskade 001 |
| [Zirkus gesucht!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artykuł  | \-     | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Błędnie nazwane / połączone wydania (002 - 004)
>
>Kaskada 002:
>W oryginalnym niemieckim pliku PDF wydania 2 i 3 są połączone.
>
>Kaskada 003:
>W oryginalnym niemieckim pliku PDF znajduje się tutaj wydanie 004.
>
>Kaskada 004:
>Brakuje tutaj strony tytułowej, nie udało mi się jeszcze ustalić, do czego ona należy...
>Wygląda jak kopia wydania 009, bez strony tytułowej.
>
>Poprawka:
>Podzieliłem plik PDF Kaskady 002 (oryginalny) na 002 i 003.
>Przemianowałem Kaskadę 003 (oryginalną) na Kaskadę 004.
>Oraz usunąłem Kaskadę 004 (oryginalną).
