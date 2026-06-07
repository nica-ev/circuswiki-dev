---
lang: cs
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
translation_updated: 2026-06-07T18:59:02+00:00
---
>[!info]- Úvod
>Vyrostl jsem s časopisem Kaskáda. Než existoval YouTube, než jsme na internetu našli všechno – tento časopis byl jedním z prvních pravidelných zdrojů informací, které jsem získal o žonglování, cirkusu a představeních.
>Když byl časopis v roce 2013 ukončen, připadalo mi to jako konec jedné éry – alespoň pro mě.
>Několik let byly časopisy dostupné ke stažení ve formátu PDF, přibližně od roku 2017 šla stránka offline.
>Často jsem si vzpomínal na malé workshopy, tutoriály nebo články, které mě tehdy inspirovaly. Když jsem si o několik let později chtěl něco znovu přečíst – už to nebylo možné.
>
>S pomocí Wayback Machine (The Internet Archive) jsem naštěstí našel zálohu z roku 2017 s kompletními soubory ke stažení (což není vždy samozřejmostí, zvláště když šlo o přibližně 3 GB PDF) – kompletní s německým, anglickým a francouzským vydáním.
>
>Při procházení jsem si uvědomil, že ačkoli bylo v časopisech ukryto mnoho skvělých článků a tutoriálů – v dnešní době by si asi málokdo prohlížel 112 časopisů, které jsou pouze zkopírované. No, pokud nemá nostalgický zájem =P
>
>Protože je ale škoda znalostí, chtěl jsem se pokusit pomocí současné techniky vše digitalizovat tak, aby to bylo i dnes smysluplně využitelné.

>[!info]- Jak byly časopisy přepsány
>Nejprve jsem z PDF odstranil všechny stránky, které neobsahovaly relevantní texty.
>
>Pro samotný přepis (nebo OCR) jsem použil multimodální jazykový model od Googlu.
>Používám ```Gemini 2.0 Pro Experimental 02-05``` s promptem
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>a také PDF se skenovaným časopisem.
>Nastavení: Teplota 0.1 (Důležité pro zamezení halucinací)
>
>Výstup je čištěn pomocí ```gemini-2.0-flash-exp``` a následujícího promptu (spolu s přiloženým textem, který jsme extrahovali):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Výsledek je pak ještě ručně zkontrolován a opraven.
>
>>[!Danger]+ Důležité:
>>Zaměření bylo na extrakci článků, workshopů, rozhovorů atd.
>>Příspěvky jako např. inzeráty atd. jsem zamítl.
>>Extrakce a čištění textů proběhlo pomocí LLM, takže vždy existuje možnost, že texty nebyly přepsány 1:1 nebo se obsah mírně liší od originálu. Snažil jsem se minimalizovat chybovost tím, že jsem namátkově porovnával textové úseky.

<!-- QueryToSerialize: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
<!-- SerializedQuery: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
- [Kaskáda 001](docs/de/Kaskade 001.md)
- [Kaskáda 002](docs/de/Kaskade 002.md)
- [Kaskáda 003](docs/de/Kaskade 003.md)
- [Kaskáda 004](docs/de/Kaskade 004.md)
- [Kaskáda 005](docs/de/Kaskade 005.md)
- [Kaskáda 001](docs/en/Kaskade 001.md)
- [Kaskáda 002](docs/en/Kaskade 002.md)
- [Kaskáda 003](docs/en/Kaskade 003.md)
- [Kaskáda 004](docs/en/Kaskade 004.md)
- [Kaskáda 005](docs/en/Kaskade 005.md)
- [Kaskáda 001](docs/pl/Kaskade 001.md)
- [Kaskáda 002](docs/pl/Kaskade 002.md)
- [Kaskáda 003](docs/pl/Kaskade 003.md)
- [Kaskáda 004](docs/pl/Kaskade 004.md)
- [Kaskáda 005](docs/pl/Kaskade 005.md)

<!-- SerializedQuery END -->

---

# Články

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Soubor                                                                            | autoři                                        | typ      | podtyp | zdroj      |
| --------------------------------------------------------------------------------- | --------------------------------------------- | -------- | ------ | ----------- |
| [Stránka o sloupech](docs/de/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Nový časopis pro Evropu](docs/de/Eine neue Zeitschrift für Europa.md)         | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článek   | -      | Kaskáda 001 |
| [Úsměv překonává gravitaci](docs/de/Lächeln überwindet Schwerkraft.md)       | <ul><li>Toby Philpott</li></ul>                 | Článek   | -      | Kaskáda 001 |
| [Podvádět!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Gravitace - a co!](docs/de/Schwerkraft - na und!.md)                         | <ul><li>Christoph Schmitt</li></ul>             | Článek   | -      | Kaskáda 001 |
| [Hledá se cirkus!](docs/de/Zirkus gesucht!.md)                                 | <ul><li>Kattrin & Uli</li></ul>                 | Článek   | -      | Kaskáda 001 |
| [Stránka o sloupech](docs/en/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Nový časopis pro Evropu](docs/en/Eine neue Zeitschrift für Europa.md)         | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článek   | -      | Kaskáda 001 |
| [Úsměv překonává gravitaci](docs/en/Lächeln überwindet Schwerkraft.md)       | <ul><li>Toby Philpott</li></ul>                 | Článek   | -      | Kaskáda 001 |
| [Podvádět!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Gravitace - a co!](docs/en/Schwerkraft - na und!.md)                         | <ul><li>Christoph Schmitt</li></ul>             | Článek   | -      | Kaskáda 001 |
| [Hledá se cirkus!](docs/en/Zirkus gesucht!.md)                                 | <ul><li>Kattrin & Uli</li></ul>                 | Článek   | -      | Kaskáda 001 |
| [Stránka o sloupech](docs/pl/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Nový časopis pro Evropu](docs/pl/Eine neue Zeitschrift für Europa.md)         | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Článek   | -      | Kaskáda 001 |
| [Úsměv překonává gravitaci](docs/pl/Lächeln überwindet Schwerkraft.md)       | <ul><li>Toby Philpott</li></ul>                 | Článek   | -      | Kaskáda 001 |
| [Podvádět!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>              | Tutoriál | Míče   | Kaskáda 001 |
| [Gravitace - a co!](docs/pl/Schwerkraft - na und!.md)                         | <ul><li>Christoph Schmitt</li></ul>             | Článek   | -      | Kaskáda 001 |
| [Hledá se cirkus!](docs/pl/Zirkus gesucht!.md)                                 | <ul><li>Kattrin & Uli</li></ul>                 | Článek   | -      | Kaskáda 001 |

<!-- SerializedQuery END -->

---

>[!info]- Nesprávně pojmenovaná / sloučená vydání (002 - 004)
>
>Kaskáda 002:
>V původním německém PDF jsou vydání 2 a 3 sloučena.
>
>Kaskáda 003:
>V původním německém PDF je zde vydání 004.
>
>Kaskáda 004:
>Zde chybí titulní strana, ještě jsem nezjistil, k čemu patří...
>Vypadá jako kopie vydání 009, bez titulní strany.
>
>Oprava:
>Rozdělil jsem PDF Kaskády 002 (originál) na 002 a 003.
>Přejmenoval jsem Kaskádu 003 (originál) na Kaskádu 004.
>A smazal Kaskádu 004 (originál).
