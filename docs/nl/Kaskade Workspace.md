---
lang: nl
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
translation_updated: 2026-06-06T23:20:02+00:00
---
>[!info]- Introductie
>Ik ben opgegroeid met Kaskade. Voordat YouTube bestond, voordat we alles op internet konden vinden – was dit tijdschrift een van de eerste regelmatige informatiebronnen die ik kreeg over jongleren, circus en shows.
>Toen het tijdschrift in 2013 stopte, voelde dat als het einde van een tijdperk – althans voor mij.
>Meerdere jaren waren de tijdschriften nog als pdf te downloaden, maar sinds ongeveer 2017 is de website offline gegaan.
>Ik heb vaak teruggedacht aan kleine workshops, tutorials of artikelen die me destijds inspireerden. Toen ik jaren later iets wilde teruglezen – kon dat niet meer.
>
>Met behulp van de Wayback Machine (The Internet Archive) heb ik gelukkig nog een controlepunt uit 2017 gevonden met de complete downloads (dit is niet altijd het geval, zeker omdat het ongeveer 3 GB aan pdf's waren) – compleet met Duitse, Engelse en Franse edities.
>
>Tijdens het doorbladeren merkte ik dat er weliswaar veel geweldige artikelen en tutorials in de tijdschriften verborgen zaten, maar dat in deze tijd waarschijnlijk niemand meer 112 tijdschriften, die slechts gekopieerd zijn, zou doorbladeren. Nou ja, tenzij je nostalgische interesses hebt =P
>
>Omdat het zonde is van de kennis, wilde ik proberen met behulp van huidige technologie alles zo te digitaliseren dat het ook vandaag nog zinvol bruikbaar is.

>[!info]- Hoe de tijdschriften zijn getranscribeerd
>Eerst heb ik alle pagina's uit de pdf verwijderd die geen relevante teksten bevatten.
>
>Voor het eigenlijke transcriberen (of OCR) heb ik een multimodale taalmodel van Google gebruikt.
>Ik gebruik ```Gemini 2.0 Pro Experimental 02-05``` met de prompt
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>en de pdf met het gescande tijdschrift.
>Instellingen: Temperatuur 0.1 (Belangrijk om hallucinaties te voorkomen)
>
>De output wordt opgeschoond met ```gemini-2.0-flash-exp``` en de volgende prompt (evenals de bijgevoegde tekst die we hebben geëxtraheerd):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Het resultaat wordt dan nogmaals handmatig bekeken en gecorrigeerd.
>
>>[!Danger]+ Belangrijk:
>>De focus lag op het extraheren van artikelen, workshops, interviews etc.
>>Berichten zoals bijvoorbeeld kleine advertenties etc. heb ik verworpen.
>>Het extraheren en opschonen van de teksten is met LLM's uitgevoerd, dus er bestaat altijd de mogelijkheid dat teksten niet 1:1 zijn getranscribeerd of dat de inhoud licht afwijkt van het origineel. Ik heb geprobeerd de foutmarge zo klein mogelijk te houden door steekproefsgewijs tekstgedeelten te vergelijken.

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

# Artikelen

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Bestand                                                                           | auteurs                                           | type     | sub-type | bron        |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | -------- | ----------- |
| [De Zuilen-Pagina](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Een nieuw tijdschrift voor Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lachen overwint zwaartekracht](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Valsspelen!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Zwaartekracht - nou en!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Circus gezocht!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [De Zuilen-Pagina](docs/en/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Een nieuw tijdschrift voor Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lachen overwint zwaartekracht](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Valsspelen!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Zwaartekracht - nou en!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Circus gezocht!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [De Zuilen-Pagina](docs/pl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Een nieuw tijdschrift voor Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artikel  | \-       | Kaskade 001 |
| [Lachen overwint zwaartekracht](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artikel  | \-       | Kaskade 001 |
| [Valsspelen!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Ballen   | Kaskade 001 |
| [Zwaartekracht - nou en!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artikel  | \-       | Kaskade 001 |
| [Circus gezocht!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artikel  | \-       | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Verkeerd benoemde / samengevoegde edities (002 - 004)
>
>Kaskade 002:
>In de Duitse originele pdf zijn edities 2+3 samengevoegd.
>
>Kaskade 003:
>In de Duitse originele pdf is hier de editie 004 te vinden.
>
>Kaskade 004:
>Hier ontbreekt het titelblad, ik heb nog niet kunnen achterhalen waar dit bij hoort...
>Het lijkt op een kopie van editie 009, zonder titelblad.
>
>Correctie:
>Ik heb de pdf van Kaskade 002 (origineel) gesplitst in 002 en 003.
>Kaskade 003 (origineel) hernoemd naar Kaskade 004.
>En Kaskade 004 (origineel) verwijderd.
