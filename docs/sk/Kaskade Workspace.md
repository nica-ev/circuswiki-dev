---
lang: sk
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
translation_updated: 2026-06-07T18:59:11+00:00
---
>[!info]- Úvod
>Vyrastal som s časopisom Kaskade. Predtým, než existoval YouTube, predtým, než sme na internete našli čokoľvek – tento časopis bol jedným z prvých pravidelných zdrojov informácií, ktoré som dostal do rúk o žonglovaní, cirkuse a predstaveniach.
>Keď časopis v roku 2013 skončil, bol to pre mňa koniec jednej éry.
>Niekoľko rokov boli časopisy dostupné na stiahnutie ako PDF, ale približne od roku 2017 je stránka offline.
>Často som si spomínal na malé workshopy, návody alebo články, ktoré ma vtedy inšpirovali. Keď som si o niekoľko rokov neskôr chcel niečo znova prečítať – už nebola žiadna možnosť.
>
>S pomocou Wayback Machine (The Internet Archive) som našiel zálohu z roku 2017 s kompletnými stiahnutiami (čo nie je vždy samozrejmé, najmä keď išlo o približne 3 GB PDF súborov) – kompletnú s nemeckým, anglickým a francúzskym vydaním.
>
>Pri prezeraní som si uvedomil, že hoci sa v časopisoch skrývalo množstvo skvelých článkov a návodov, v dnešnej dobe by si už asi málokto pozrel 112 časopisov, ktoré sú len prekopiírované. No, pokiaľ nemá nostalgický záujem =P
>
>Keďže je škoda prísť o tieto vedomosti, chcel som sa pokúsiť pomocou súčasnej techniky všetko zdigitalizovať tak, aby to bolo zmysluplne využiteľné aj dnes.

>[!info]- Ako boli časopisy prepísané
>Najprv som zo všetkých PDF odstránil strany, ktoré neobsahovali relevantné texty.
>
>Na samotné prepisovanie (alebo OCR) som použil multimodálny jazykový model od spoločnosti Google.
>Používam ```Gemini 2.0 Pro Experimental 02-05``` s promptom
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>a tiež PDF so skenovaným časopisom.
>Nastavenia: Teplota 0.1 (Dôležité na zabránenie halucináciám)
>
>Výstup sa vyčistí pomocou ```gemini-2.0-flash-exp``` a nasledujúceho promptu (ako aj pripojeného textu, ktorý sme extrahovali):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Výsledok sa potom ešte manuálne skontroluje a opraví.
>
>>[!Danger]+ Dôležité:
>>Zameranie bolo na extrakciu článkov, workshopov, rozhovorov atď.
>>Príspevky ako napr. drobné inzercie som zamietol.
>>Extrakcia a čistenie textov prebiehalo pomocou LLM, preto existuje vždy možnosť, že texty neboli transkribované 1:1 alebo sa obsah mierne líši od originálu. Snažil som sa minimalizovať chybovosť tým, že som náhodne porovnával textové úseky.

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

<!-- SerializedQuery END -->

---

# Články

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Súbor                                                                         | autori                                | typ      | podtyp | zdroj      |
| ----------------------------------------------------------------------------- | ------------------------------------- | -------- | ------ | ----------- |
| [Die Säulen-Seite](docs/de/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článok   | -      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/de/Lächeln überwindet Schwerkraft.md)  | <ul><li>Toby Philpott</li></ul>      | Článok   | -      | Kaskade 001 |
| [Schummeln!](docs/de/Schummeln!.md)                                          | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Schwerkraft - na und!](docs/de/Schwerkraft - na und!.md)                    | <ul><li>Christoph Schmitt</li></ul>  | Článok   | -      | Kaskade 001 |
| [Zirkus gesucht!](docs/de/Zirkus gesucht!.md)                                | <ul><li>Kattrin & Uli</li></ul>      | Článok   | -      | Kaskade 001 |
| [Die Säulen-Seite](docs/en/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článok   | -      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/en/Lächeln überwindet Schwerkraft.md)  | <ul><li>Toby Philpott</li></ul>      | Článok   | -      | Kaskade 001 |
| [Schummeln!](docs/en/Schummeln!.md)                                          | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Schwerkraft - na und!](docs/en/Schwerkraft - na und!.md)                    | <ul><li>Christoph Schmitt</li></ul>  | Článok   | -      | Kaskade 001 |
| [Zirkus gesucht!](docs/en/Zirkus gesucht!.md)                                | <ul><li>Kattrin & Uli</li></ul>      | Článok   | -      | Kaskade 001 |
| [Die Säulen-Seite](docs/pl/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článok   | -      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/pl/Lächeln überwindet Schwerkraft.md)  | <ul><li>Toby Philpott</li></ul>      | Článok   | -      | Kaskade 001 |
| [Schummeln!](docs/pl/Schummeln!.md)                                          | <ul><li>Dr. P. Luftiko</li></ul>     | Návod    | Lopty  | Kaskade 001 |
| [Schwerkraft - na und!](docs/pl/Schwerkraft - na und!.md)                    | <ul><li>Christoph Schmitt</li></ul>  | Článok   | -      | Kaskade 001 |
| [Zirkus gesucht!](docs/pl/Zirkus gesucht!.md)                                | <ul><li>Kattrin & Uli</li></ul>      | Článok   | -      | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Nesprávne pomenované / zlúčené vydania (002 - 004)
>
>Kaskade 002:
>V pôvodnom nemeckom PDF sú vydania 2 a 3 spojené.
>
>Kaskade 003:
>V pôvodnom nemeckom PDF sa tu nachádza vydanie 004.
>
>Kaskade 004:
>Tu chýba titulná strana, ešte som nezistil, k čomu patrí...
>Vyzerá ako kópia vydania 009, bez titulnej strany.
>
>Oprava:
>PDF Kaskade 002 (originál) som rozdelil na 002 a 003.
>Kaskade 003 (originál) som premenoval na Kaskade 004.
>A Kaskade 004 (originál) som zmazal.
