---
lang: hu
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2026-06-07 00:06:48
title: Buchhaltung Übersicht
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: be60078ea723f4aec6db8f350c8a5a5597cfee74d578fecbf75f55a97077189f
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T22:35:01+00:00
---
# Könyvelés áttekintése

A könyvelésünk az úgynevezett "plaintext accounting" (szöveges könyvelés) elven alapul.
Minden adatot / tranzakciót egy szöveges fájlba írunk, ember által jól olvasható formátumban.

Egy tranzakció így néz ki ebben a formátumban:
```
2023-01-09 dokumentum Kiadások:Iroda:Egyéb "Bizonylatok/Kiadások/Bejegyezve/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Irodai lámpa" #nyitott #beolvasva ^2023_004

    Kiadások:Iroda:Egyéb              64.95 EUR

    Kötelezettségek:Személy:Marc-Bielert
```

# Teendők

Az adományokat mindig egyértelműen kell nyomon követni, akár külön számlán, akár tagekkel.
Ez fontos a [tevékenységi jelentések](../_inbox/Tätigkeitsberichte.md) szempontjából, amelyeket évente el kell készítenünk. #teendő
