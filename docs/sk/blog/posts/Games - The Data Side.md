---
lang: sk
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
translation_updated: 2026-06-07T18:29:59+00:00
---
# **Hry – Dátová stránka**
**Ako boli popisy hier štandardizované a dynamickejšie vďaka metadátam a doplnkom Obsidian.**

Pokiaľ ide o správu obsahu, kľúčová je konzistencia. Pri prvej významnej časti tohto projektu som sa zameral na hry – približne 170 z nich, každá s vlastným jedinečným formátom, štýlom a prístupnosťou. Problém? Mnohé z týchto opisov sa spoliehali na pevne zakódované, statické odkazy, čo sťažovalo pridávanie nových hier alebo úpravu štruktúry.

Tak som si vyhrnul rukávy a pustil sa do práce.
<!-- more -->
## Krok 1: Jednotný formát
Prvou úlohou bolo stanoviť jednotný formát pre všetky opisy hier. Inšpiráciu som čerpal z „Tasifan Spielebuch“ (Kniha hier Tasifan), dobre organizovaného zdroja opisov hier. Aby som to ešte viac zjednodušil pre používateľa, pridal som krátke zhrnutia, takže všetky podstatné detaily sú viditeľné na prvý pohľad – dokonca aj v náhľade.

Ale skutočnou zmenou hry? Metadáta.

## Krok 2: Kúzlo metadát
Teraz sú všetky kľúčové informácie – veľkosť skupiny, materiály, trvanie a ďalšie – uložené ako metadáta v hornej časti každého súboru Markdown vo formáte nazývanom YAML (alebo frontmatter). To nielenže udržuje poriadok, ale tiež umožňuje opätovné použitie dát v celom systéme.

Aby bolo vyhľadávanie správnej hry jednoduchšie, implementoval som jednoduchú, ale účinnú logiku:
1. **Vyberte kategóriu**: Aký typ hry hľadáte? Hru na upokojenie? Hru na naháňanie? Niečo na budovanie tímu? Vytvoril som súbor kategórií na začiatok, ale tieto sa dajú podľa potreby upraviť alebo rozšíriť.
2. **Prezrite si tabuľku**: Keď si vyberiete kategóriu, zobrazí sa vám tabuľka so všetkými hrami, ktoré do nej patria. Tabuľka je zoraditeľná – stačí kliknúť na hlavičky, aby ste ju usporiadali podľa trvania, obtiažnosti alebo iných kritérií.

A tu je to najlepšie: mnohé hry sa objavujú vo viacerých kategóriách, takže nikdy nie ste obmedzení len na jeden spôsob vyhľadávania toho, čo potrebujete.

## Nie celkom dynamické tabuľky
Skutočné kúzlo sa deje s dvoma doplnkami Obsidian: **Dataview** a **Dataview Serializer**.

Dataview mi umožňuje vytvárať dynamické zoznamy a tabuľky pomocou dotazov podobných databázam. Háčik? Tieto tabuľky fungujú iba v rámci Obsidianu, pretože podkladové súbory Markdown sa nemenia.

Vstúpte do Dataview Serializer. Tento doplnok konvertuje tieto dynamické tabuľky do statického formátu Markdown a zapisuje ich priamo do súboru. Keď sa stránka zostavuje pomocou MkDocs, tabuľky sú statické, ale boli v podstate dynamicky generované offline.

Tieto dotazy môžu byť dosť zložité, čo mi umožňuje vyhľadávať alebo zobrazovať konkrétne časti wiki – ako sú všetky opisy hier alebo články napísané konkrétnym autorom. A pretože sa automaticky aktualizujú (prostredníctvom kroku serializácie), pridávanie nových informácií a budovanie navigovateľnej štruktúry je hračka.

Ale nie je to všetko len slnko a dúha. Proces nie je plne automatický. Dataview Serializer môže prepísať súbor iba vtedy, ak je otvorený v Obsidian. Zatiaľ je to zvládnuteľné – označil som každú stránku dynamickou tabuľkou alebo zoznamom, čo uľahčuje ich prechádzanie. Ale ak sa počet týchto stránok výrazne zvýši, možno budem musieť prehodnotiť prístup.

## Nástroje a jazykové modely
Pôvodné opisy hier boli zmiešané z hľadiska formátovania a kvality. Na zefektívnenie procesu som sa obrátil na jazykové modely (LLM). Vytvoril som špecifický prompt, doplnený o príklady formátovania, aby som zabezpečil, že samotný obsah nebude zmenený (žiadne zbytočné prepisovanie). Napriek tomu som každý výsledok manuálne skontroloval a v prípade potreby vykonal malé úpravy.

Tu je poučenie: pri správnom použití sú tieto nástroje *neuveriteľne* výkonné. Kľúčom je byť presný a zámerný v tom, ako formulujete svoje úlohy.

Finálne zmeny sa týkajú hlavne formátovania – ako sú informácie a opisy hier prezentované. Metadáta však boli všetky zadané manuálne. Keďže som aj tak musel všetko dvakrát skontrolovať, v tomto prípade bolo ručné zadávanie rýchlejšie.

Je to však pomalý proces. Keďže na tom pracujem na čiastočný úväzok, denne zvládnem asi 10-15 hier. Pokrok je stabilný, ale bude to chvíľu trvať.

## Výzvy vpred
Jednou z potenciálnych prekážok sú preklady. Vyhľadávacie dotazy by bolo potrebné prispôsobiť na vyhľadávanie jazykovo špecifických verzií hier alebo značiek. Zatiaľ sa to dá zvládnuť manuálne, ale ak systém narastie, môže byť potrebná automatizácia.

Preklad je komplexná téma a budem sa jej venovať podrobnejšie inokedy.

## Prečo sa s tým trápiť?
Krátka odpoveď? Škálovateľnosť.

Tento systém je navrhnutý tak, aby rástol. Štandardizáciou formátu, využitím metadát a použitím dynamických nástrojov som vytvoril základ, ktorý zvládne viac obsahu bez toho, aby sa stal neovládateľným.

## Čo je ešte nové?
Funkcia vyhľadávania dostala niekoľko vylepšení:
- **Automatické dopĺňanie**: Keď píšete, vyhľadávanie navrhuje dotazy, ktoré prinášajú najviac výsledkov. Toto nie je založené na správaní používateľa – nesledujeme vyhľadávania – ale na statickom vyhľadávacom indexe generovanom pri zostavovaní stránky.
- **Uložené vyhľadávania**: Kliknite na malú ikonu vedľa vyhľadávacieho poľa a váš dotaz (a výsledky) sa uložia do URL. Uložte si ju do záložiek a vždy dostanete rovnaké výsledky.

Je to malá funkcia, ale môže sa stať neuveriteľne užitočnou, keď wiki narastie a bude pokrývať rozmanitejšie témy.
