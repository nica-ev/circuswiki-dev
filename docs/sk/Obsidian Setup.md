---
lang: sk
translation_id: obsidian-setup
publish: true
tags: 
title: Nastavenie Obsidianu
created: 2025-01-23 01:38:52
update: 2026-06-06 21:43:04
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Obsidian Setup.md
translation_source_hash: bf9ce19d8ada1591527eaab93d628ac5f52f6502ff79e986249b1b03be05d9b0
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T19:07:11+00:00
translation_source_body_hash: bf9ce19d8ada1591527eaab93d628ac5f52f6502ff79e986249b1b03be05d9b0
translation_source_metadata_hash: 619a6953727d9e5aa408066d3e18868e9afcf59dd5179abedfb71844a72e480e
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T19:01:09+00:00
---
Obsidian je extrémne prispôsobiteľný, čo môže byť pre nováčikov problém.
Poskytujeme základné nastavenie, ktoré možno použiť tak, ako je, vrátane doplnkov a tém, ako aj ich jemne vyladených nastavení.
Toto je základné nastavenie a dá sa ďalej upraviť podľa osobných preferencií každého.
Poskytujeme len funkčné riešenie – ktoré tu zdokumentujeme a vysvetlíme.

## Použité pojmy
**Trezor (Vault)** – zbierka súborov markdown a obrázkov, ktoré tvoria vedomostnú bázu

## Doplnky (Plugins)

- Advanced Canvas
- BRAT
- Better Wordcount
- Clear unused Images
- Dataview
- Dataview Serializer
- Emoji Toolbar
- Linter
- Note Toolbar
- Tag Wrangler
- Templater
- Beautitab
- Omnisearch
- Status Bar Organizer
- Workspaces Plus
- Sortable

### Advanced Canvas
Poskytuje prístup k mnohým novým funkciám a možnostiam štýlovania pre Canvas.

### BRAT
Potrebný na inštaláciu neoficiálnych doplnkov / doplnkov, ktoré nie sú registrované v ekosystéme Obsidianu, konkrétne:
- Dataview Serializer
- Sortable

### Better Word Count
Používa sa hlavne pre svoju schopnosť zobrazovať počet slov/znakv v zvýraznenom texte.
Je viditeľný v stavovom riadku.

### Beautitab
Čisto kozmetický doplnok, poskytuje prispôsobiteľnú stránku „prázdneho nového panelu“.

### Clear unused Images
Ako naznačuje názov, pomáha pri organizácii trezora identifikáciou nepoužívaných obrázkov.

❗Vybral som podadresár ```/site/```, aby sa neustále nevymazávali obrázky z vytvorenej webovej stránky (čo nie je problém, skôr otravné).

❗Pri používaní príkazu na vymazanie príloh buďte opatrní – tento príkaz vždy vymaže ```mkdocs.yml``` a ```license.``` --> ak sa to stane, súbory sú v priečinku .trash a dajú sa obnoviť. Ale ľahko sa to prehliadne.

### Dataview
Umožňuje dotazy podobné SQL na trezor.

### Dataview Serializer
Prevedie výsledky Dataview na markdown.
Pomáha pri opätovnom použití výsledkov dotazov Dataview v samotných poznámkach.

### Emoji Toolbar
No, poskytuje ľahký prístup k emoji.
**Klávesová skratka nastavená na: ALT-E**
😍

### Linter
Vyčistí súbory markdown a dáta vo frontmatter.
Pomáha udržiavať konzistentnú formu.

### Note Toolbar
Umožňuje prispôsobiteľné panely nástrojov v hornej časti poznámky, ktoré je možné definovať na úrovni priečinka/súboru.

### Tag Wrangler
Poskytuje ďalšie možnosti práce so značkami.
- premenovanie značiek
Pomáha pri organizácii trezora.

### Templater
Umožňuje prispôsobiteľné šablóny, ktoré je možné vložiť manuálne alebo na základe podmienok (napr. pri vytváraní poznámky).

### Status Bar Organizer
Umožňuje skryť položky zo stavového riadku.

### Sortable
Umožňuje triedenie tabuliek (markdown aj dataview tabuliek) kliknutím na ich hlavičky.

### Workspaces Plus
Umožňuje jednoduché rýchle prepínanie zo stavového riadku.

## Súborový systém trezora

[Súborový systém trezora](Vault%20File%20System.md){ .md-button }
