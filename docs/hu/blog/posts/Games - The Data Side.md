---
lang: hu
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
translation_updated: 2026-06-06T22:34:34+00:00
---
# **Játékok – Az Adatoldal**
**Hogyan tették egységessé és dinamikusabbá a játékleírásokat metaadatok és Obsidian bővítmények segítségével.**

Amikor a tartalomkezelésről van szó, a következetesség kulcsfontosságú. A projekt első nagyobb részében a játékokkal foglalkoztam – nagyjából 170-nel, mindegyik sajátos formátummal, stílussal és hozzáférhetőséggel. A probléma? Sok leírás keményen kódolt, statikus linkekre támaszkodott, ami rémálommá tette új játékok hozzáadását vagy a struktúra módosítását.

Tehát felgyűrtem az ingujjam, és munkához láttam.
<!-- more -->
## 1. Lépés: Egységes Formátum
Az elsődleges feladat az egységes formátum kialakítása volt az összes játékleíráshoz. Ehhez a „Tasifan Spielebuch” (Tasifan Játékkönyv) inspirált, amely egy jól strukturált forrás a játékleírásokhoz. A felhasználóbarátság növelése érdekében rövid összefoglalókat is hozzáadtam, így minden lényeges részlet egy pillantással látható – még előnézetben is.

De az igazi áttörést a metaadatok jelentették.

## 2. Lépés: Metaadat Varázslat
Mostantól minden kulcsfontosságú információ – csoportméret, anyagok, időtartam és még sok más – metaadatként tárolódik minden Markdown fájl tetején, YAML (vagy frontmatter) formátumban. Ez nemcsak a rendszerezést segíti, hanem az adatok újrafelhasználhatóságát is biztosítja az egész rendszerben.

A megfelelő játék megtalálásának megkönnyítése érdekében egy egyszerű, de hatékony logikát vezettem be:
1. **Válassz kategóriát**: Milyen típusú játékot keresel? Levezető játékot? Fogócskát? Csapatépítő játékot? Kezdetnek létrehoztam néhány kategóriát, de ezek igény szerint módosíthatók vagy bővíthetők.
2. **Böngészd az táblázatot**: Miután kiválasztottad a kategóriát, egy táblázat jelenik meg, amely felsorolja az összes odaillő játékot. A táblázat rendezhető – csak kattints a fejlécokra az időtartam, nehézség vagy más kritériumok szerint rendezéshez.

És itt jön a lényeg: sok játék több kategóriába is bekerült, így soha nem korlátozódsz csak egyetlen keresési módra.

## Nem Teljesen Dinamikus Táblázatok
Az igazi varázslat két Obsidian bővítménnyel történik: a **Dataview** és a **Dataview Serializer** segítségével.

A Dataview lehetővé teszi dinamikus listák és táblázatok létrehozását adatbázisszerű lekérdezésekkel. A csavar? Ezek a táblázatok csak az Obsidianon belül működnek, mert az alapul szolgáló Markdown fájlok nem módosulnak.

Itt jön képbe a Dataview Serializer. Ez a bővítmény ezeket a dinamikus táblázatokat statikus Markdown formátummá alakítja, és közvetlenül a fájlba írja őket. Amikor az oldalt az MkDocs segítségével építik fel, a táblázatok statikusak, de lényegében offline módon, dinamikusan generálódtak.

Ezek a lekérdezések meglehetősen összetettek lehetnek, lehetővé téve a wiki bizonyos részeinek keresését vagy megjelenítését – például az összes játékleírást vagy egy adott szerző által írt cikket. És mivel automatikusan frissülnek (a szerializáló lépésen keresztül), az új információk hozzáadása és egy navigálható struktúra felépítése gyerekjáték.

De nem minden fenékig tejfel. A folyamat nem teljesen automatikus. A Dataview Serializer csak akkor tudja újraírni egy fájlt, ha az meg van nyitva az Obsidianban. Jelenleg ez kezelhető – minden oldalt elláttam egy dinamikus táblázattal vagy listával, így könnyű végigmenni rajtuk. De ha ezeknek az oldalaknak a száma jelentősen megnő, lehet, hogy át kell gondolnom az megközelítést.

## Eszközök és Nyelvi Modellek
Az eredeti játékleírások vegyes képet mutattak formátum és minőség tekintetében. A folyamat egyszerűsítése érdekében nyelvi modellekhez (LLM) fordultam. Készítettem egy specifikus promptot, példa formátummal, hogy biztosítsam a tartalom változatlanságát (nem voltak szükségtelen átírások). Ennek ellenére minden eredményt manuálisan felülvizsgáltam, és kisebb módosításokat végeztem, ahol szükséges volt.

A tanulság: helyesen használva ezek az eszközök *hihetetlenül* erőteljesek. A kulcs az, hogy precízen és céltudatosan fogalmazzuk meg a feladatokat.

A végső változtatások többnyire a formázásra vonatkoznak – hogyan jelennek meg az információk és a játékleírások. A metaadatokat azonban mind kézzel vittem be. Mivel úgyis mindent kétszer kellett ellenőriznem, ebben az esetben a kézi bevitel volt a gyorsabb.

Ez azonban lassú folyamat. Részmunkaidőben dolgozva naponta nagyjából 10-15 játékkal tudok foglalkozni. A haladás egyenletes, de még sok időbe telik.

## Kihívások Előttünk
Egy lehetséges akadály a fordítás. A keresési lekérdezéseket adaptálni kellene a játékok vagy címkék nyelvspecifikus verzióinak megtalálásához. Jelenleg ezt manuálisan lehet kezelni, de ha a rendszer növekszik, szükségessé válhat az automatizálás.

A fordítás összetett téma, és ezzel egy másik alkalommal mélyebben foglalkozom.

## Miért Erőfeszítsek?
A rövid válasz? Skálázhatóság.

Ez a rendszer növekedésre lett tervezve. A formátum standardizálásával, a metaadatok kihasználásával és a dinamikus eszközök használatával olyan alapot teremtettem, amely több tartalmat is képes kezelni anélkül, hogy kezelhetetlenné válna.

## Mi Újság Még?
A keresőfunkció kapott néhány fejlesztést:
- **Automatikus kiegészítés**: Gépelés közben a kereső olyan lekérdezéseket javasol, amelyek a legtöbb találatot eredményezik. Ez nem felhasználói viselkedésen alapul – nem követjük a kereséseket –, hanem az oldal felépítésekor generált statikus keresési indexen.
- **Mentett keresések**: Kattints a keresősáv melletti kis ikonra, és a lekérdezésed (és az eredmények) elmentődnek az URL-ben. Könyvjelzőzd meg, és minden alkalommal ugyanazokat az eredményeket kapod.

Ez egy kis funkció, de rendkívül hasznossá válhat, ahogy a wiki növekszik és egyre több és változatosabb témát fed le.
