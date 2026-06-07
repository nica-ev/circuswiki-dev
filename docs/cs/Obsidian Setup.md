---
lang: cs
translation_id: obsidian-setup
publish: true
tags: 
title: Obsidian Setup
created: 2025-01-23 01:38:52
update: 2026-06-06 21:43:04
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Obsidian Setup.md
translation_source_hash: 12599e90e70b1c7a59227815d654a7076285e589ef224bbe86222277b9b386e6
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T19:07:07+00:00
---
Obsidian je extrémně přizpůsobitelný, což může být pro nováčky problém.
Poskytujeme základní nastavení, které lze použít tak, jak je, včetně pluginů a motivů, a také jejich jemně doladěná nastavení.
Jedná se o základní nastavení, které lze dále upravit podle osobních preferencí každého.
Poskytujeme pouze funkční řešení – které zde zdokumentujeme a vysvětlíme.

## Použité termíny
**Trezor (Vault)** – kolekce markdown souborů a obrázků, které tvoří znalostní bázi

## Pluginy

- Advanced Canvas
- BRAT
- Better Wordcount
- Clear Unused Images
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
Poskytuje přístup k mnoha novým funkcím a možnostem stylizace pro Canvas.

### BRAT
Potřebný k instalaci neoficiálních pluginů / pluginů, které nejsou registrovány v ekosystému Obsidianu, konkrétně:
- Dataview Serializer
- Sortable

### Better Word Count
Používá se hlavně pro svou schopnost zobrazit počet slov/znaků v označeném textu.
Je viditelný ve stavovém řádku.

### Beautitab
Čistě kosmetický, poskytuje přizpůsobitelnou stránku "prázdného nového panelu".

### Clear unused Images
Jak název napovídá, pomáhá s organizací trezoru identifikací nepoužívaných obrázků.

❗Vyloučil jsem podsložku ```/site/```, aby se ne vždy mazaly obrázky z vytvořené webové stránky (což není problém, spíše nepříjemnost).

❗Buďte opatrní při používání příkazu pro vymazání příloh – ten vždy smaže ```mkdocs.yml``` a ```license.``` --> pokud se to stane, soubory jsou ve složce .trash a lze je obnovit. Ale je snadné to přehlédnout.

### Dataview
Umožňuje dotazy podobné SQL na trezoru.

### Dataview Serializer
Převádí výsledky Dataview na markdown.
Pomáhá s opětovným použitím výsledků dotazů Dataview v samotných poznámkách.

### Emoji Toolbar
No, poskytuje snadný přístup k emotikonům.
**Klávesová zkratka nastavena na: ALT-E**
😍

### Linter
Čistí markdown soubory a data frontmatter.
Pomáhá udržovat konzistentní formu.

### Note Toolbar
Umožňuje přizpůsobitelné panely nástrojů v horní části poznámky, které lze definovat na úrovni složky/souboru.

### Tag Wrangler
Poskytuje další možnosti pro práci se značkami.
- přejmenování značek
Pomáhá s organizací trezoru.

### Templater
Umožňuje přizpůsobitelné šablony, které lze vložit ručně nebo na základě podmínek (např. při vytváření poznámky).

### Status Bar Organizer
Umožňuje skrýt položky ze stavového řádku.

### Sortable
Umožňuje řazení tabulek (jak markdown, tak dataview tabulek) kliknutím na jejich záhlaví.

### Workspaces Plus
Umožňuje snadné rychlé přepínání ze stavového řádku.

## Souborový systém trezoru

[Souborový systém trezoru](Vault%20File%20System.md){ .md-button }
