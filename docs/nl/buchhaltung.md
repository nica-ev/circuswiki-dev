---
lang: nl
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
translation_updated: 2026-06-06T23:12:36+00:00
---
# Boekhouding Overzicht

Onze boekhouding is gebaseerd op de zogenaamde "Plaintext Accounting".
Alle gegevens / transacties worden in een tekstbestand geschreven in een goed leesbaar formaat.

Zo ziet een transactie er in dit formaat uit:
```
2023-01-09 document Uitgaven:Kantoor:Overig "Bonnen Uitgaven/Ingevoerd/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Kantoorlamp" #open #scanned ^2023_004

    Uitgaven:Kantoor:Overig              64.95 EUR

    Verplichtingen:Persoon:Marc-Bielert
```

# Todo

Donaties moeten altijd duidelijk worden bijgehouden, hetzij via een apart account, hetzij via tags.
Dit is belangrijk voor de [Activiteitenverslagen](../_inbox/Tätigkeitsberichte.md) die we jaarlijks moeten opstellen. #todo
