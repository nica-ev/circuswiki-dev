---
lang: cs
translation_id: blog/posts/games-the-data-side
created: 2025-01-21 18:09:55
update: 2025-05-03 22:54:41
date: 2025-03-18T02:14:00
publish: true
tags: 
title: Games - The Data Side
description: How game descriptions were standardized and made more dynamic using metadata and Obsidian plugins.
authors:
  - Marc Bielert
categories: 
  - development
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/blog/posts/Games - The Data Side.md
translation_source_hash: 3353b31192222fa2f6b149173311038624bdeac5d127157c14a2f4a801a4d7df
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T18:29:52+00:00
---
# **Hry – Datová stránka**
**Jak byly popisy her standardizovány a zefektivněny pomocí metadat a pluginů Obsidianu.**

Pokud jde o správu obsahu, klíčová je konzistence. Pro první velkou část tohoto projektu jsem se pustil do her – asi 170 z nich, každá s vlastním jedinečným formátem, stylem a přístupností. Problém? Mnoho z těchto popisů spoléhalo na pevně zakódované, statické odkazy, což ztěžovalo přidávání nových her nebo úpravu struktury.

Tak jsem si vyhrnul rukávy a pustil se do práce.
<!-- more -->
## Krok 1: Sjednocený formát
Prvním úkolem bylo stanovit jednotný formát pro všechny popisy her. Inspiraci jsem čerpal z "Tasifan Spielebuch" (Kniha her Tasifan), dobře organizovaného zdroje pro popisy her. Aby byly věci ještě uživatelsky přívětivější, přidal jsem krátká shrnutí, takže všechny podstatné detaily jsou viditelné na první pohled – dokonce i v náhledu.

Ale skutečnou revolucí? Metadata.

## Krok 2: Kouzlo metadat
Nyní jsou všechny klíčové informace – velikost skupiny, materiály, doba trvání a další – uloženy jako metadata v horní části každého souboru Markdown ve formátu nazývaném YAML (nebo frontmatter). To nejen udržuje věci organizované, ale také umožňuje opětovné použití dat v celém systému.

Aby bylo snazší najít tu správnou hru, implementoval jsem jednoduchou, ale účinnou logiku:
1. **Vyberte kategorii**: Jaký typ hry hledáte? Hru na zklidnění? Hru na honěnou? Něco pro budování týmu? Vytvořil jsem sadu kategorií pro začátek, ale tyto lze podle potřeby upravit nebo rozšířit.
2. **Prohlédněte si tabulku**: Jakmile si vyberete kategorii, uvidíte tabulku se všemi hrami, které do ní spadají. Tabulka je řaditelná – stačí kliknout na záhlaví a uspořádat podle délky, obtížnosti nebo jiných kritérií.

A tady je to nejlepší: mnoho her se objevuje ve více kategoriích, takže nikdy nejste omezeni pouze na jeden způsob hledání toho, co potřebujete.

## Ne tak docela dynamické tabulky
Skutečné kouzlo se odehrává se dvěma pluginy Obsidianu: **Dataview** a **Dataview Serializer**.

Dataview mi umožňuje vytvářet dynamické seznamy a tabulky pomocí dotazů podobných databázím. Háček? Tyto tabulky fungují pouze v Obsidianu, protože podkladové soubory Markdown nejsou upraveny.

Vstupuje Dataview Serializer. Tento plugin převádí tyto dynamické tabulky do statického formátu Markdown a zapisuje je přímo do souboru. Když je web sestaven pomocí MkDocs, tabulky jsou statické, ale byly v podstatě generovány dynamicky offline.

Tyto dotazy mohou být poměrně složité a umožňují mi vyhledávat nebo zobrazovat konkrétní části wiki – například všechny popisy her nebo články napsané konkrétním autorem. A protože se automaticky aktualizují (prostřednictvím kroku serializace), přidávání nových informací a budování navigovatelné struktury je hračka.

Ale není to všechno sluníčko a duha. Proces není plně automatický. Dataview Serializer může přepsat soubor pouze v případě, že je otevřen v Obsidianu. Prozatím je to zvládnutelné – označil jsem každou stránku dynamickou tabulkou nebo seznamem, což usnadňuje jejich procházení. Ale pokud se počet těchto stránek výrazně zvýší, možná budu muset přehodnotit přístup.

## Nástroje a jazykové modely
Původní popisy her byly směsicí z hlediska formátování a kvality. Abych zefektivnil proces, obrátil jsem se na jazykové modely (LLM). Vytvořil jsem specifický prompt, doplněný o příklad formátování, abych zajistil, že samotný obsah nebude změněn (žádné zbytečné přepisování). Přesto jsem každý výsledek ručně zkontroloval a provedl drobné úpravy tam, kde to bylo nutné.

Zde je ponaučení: při správném použití jsou tyto nástroje *neuvěřitelně* mocné. Klíčem je být přesný a záměrný v tom, jak formulujete své úkoly.

Finální změny se týkají především formátování – jak jsou informace a popisy her prezentovány. Metadata však byla zadána ručně. Jelikož jsem stejně musel vše dvakrát zkontrolovat, ruční zadání bylo v tomto případě rychlejší.

Je to však pomalý proces. Při práci na částečný úvazek zvládnu asi 10–15 her denně. Pokrok je stálý, ale bude to chvíli trvat.

## Výzvy do budoucna
Jednou z možných překážek jsou překlady. Dotazy by musely být upraveny tak, aby vyhledávaly jazykově specifické verze her nebo značek. Prozatím to lze řešit ručně, ale pokud se systém rozšíří, může být nutná automatizace.

Překlad je složité téma a budu se mu věnovat podrobněji jindy.

## Proč se s tím obtěžovat?
Krátká odpověď? Škálovatelnost.

Tento systém je navržen tak, aby rostl. Standardizací formátu, využitím metadat a použitím dynamických nástrojů jsem vytvořil základ, který zvládne více obsahu, aniž by se stal neohrabaným.

## Co je nového?
Funkce vyhledávání dostala několik vylepšení:
- **Automatické doplňování**: Při psaní se vyhledávání navrhuje dotazy, které vracejí nejvíce výsledků. To není založeno na chování uživatelů – vyhledávání nesledujeme – ale na statickém indexu vyhledávání vygenerovaném při sestavování webu.
- **Uložená vyhledávání**: Klikněte na malou ikonu vedle vyhledávacího pole a váš dotaz (a výsledky) se uloží do URL. Uložte si jej do záložek a pokaždé získáte stejné výsledky.

Je to malá funkce, ale může se stát neuvěřitelně užitečnou, jak se wiki rozrůstá a pokrývá rozmanitější témata.
