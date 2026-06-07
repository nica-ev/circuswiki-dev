---
lang: hu
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
translation_updated: 2026-06-06T22:45:15+00:00
---
>[!info]- Bevezetés
>A Kaskade magazinnal nőttem fel. Még mielőtt létezett volna a Youtube, mielőtt mindent megtalálhattunk volna az interneten – ez a magazin volt az egyik első rendszeres információs forrásom az ugrálás, a cirkusz és a show-k témájában.
>Amikor a magazin 2013-ban megszűnt, vége volt egy korszaknak – legalábbis számomra.
>Több éven át a magazinok PDF-ben még letölthetők voltak, de kb. 2017 óta az oldal offline.
>Gyakran emlékeztem kis workshopokra, oktatóanyagokra vagy cikkekre, amelyek akkoriban inspiráltak. Amikor évekkel később újra el akartam olvasni valamit – erre már nem volt lehetőség.
>
>A Wayback Machine (The Internet Archive) segítségével szerencsére találtam egy 2017-es mentést a teljes letöltésekkel (ez nem mindig van így, különösen, mivel kb. 3 GB PDF-ről van szó) – teljes német, angol és francia kiadásokkal.
>
>Átnézve észrevettem, hogy bár sok nagyszerű cikk és oktatóanyag volt elrejtve a magazinokban – a mai világban valószínűleg senki sem nézne át 112, csak fénymásolt magazint. Hát, hacsak nincs valakinek nosztalgikus érdeklődése =P
>
>Mivel kár lenne az információkért, megpróbáltam a jelenlegi technológia segítségével digitalizálni az egészet úgy, hogy ma is értelmesen használható legyen.

>[!info]- Hogyan transzkribálták a magazinokat?
>Először eltávolítottam az összes olyan oldalt a PDF-ből, amely nem tartalmazott releváns szöveget.
>
>A tényleges transzkribáláshoz (vagy OCR-hez) a Google egyik multimodális nyelvi modelljét használtam.
>A ```Gemini 2.0 Pro Experimental 02-05```-t használom a következő prompttal:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>valamint a beolvasott magazin PDF-jét.
>Beállítások: Temperature 0.1 (Fontos a téves következtetések elkerülése érdekében)
>
>Az outputot a ```gemini-2.0-flash-exp``` és a következő prompt (valamint a mellékelt, általunk kinyert szöveg) segítségével tisztítom:
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Az eredményt ezután még egyszer manuálisan átnézem és javítom.
>
>>[!Danger]+ Fontos:
>>A hangsúly a cikkek, workshopok, interjúk stb. kinyerésén volt.
>>Az olyan bejegyzéseket, mint pl. apróhirdetések stb. elvetettem.
>>A szövegek kinyerése és tisztítása LLM-ekkel történt, így mindig fennáll annak a lehetősége, hogy a szövegek nem 1:1-ben lettek átírva, vagy a tartalom kissé eltér az eredetitől. Igyekeztem a hibaszázalékot a lehető legalacsonyabb szinten tartani azáltal, hogy mintavételszerűen összehasonlítottam szövegrészeket.

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

<!-- SerializedQuery END -->

---

# Cikkek

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

<!-- SerializedQuery END -->

---

>[!info]- Rosszul elnevezett / összefoglalt kiadások (002 - 004)
>
>Kaskade 002:
>A német eredeti PDF-ben a 2. és 3. kiadás össze van vonva.
>
>Kaskade 003:
>A német eredeti PDF-ben itt a 004-es kiadás található.
>
>Kaskade 004:
>Itt hiányzik a címlap, még nem tudtam kideríteni, mihez tartozik...
>Úgy néz ki, mint a 009-es kiadás másolata, címlap nélkül.
>
>Javítás:
>A Kaskade 002 (eredeti) PDF-et kettéosztottam 002-re és 003-ra.
>A Kaskade 003 (eredeti) átnevezve Kaskade 004-re.
>A Kaskade 004 (eredeti) pedig törölve lett.
