---
lang: it
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
translation_updated: 2026-06-06T22:58:31+00:00
---
# Panoramica della Contabilità

La nostra contabilità si basa sul cosiddetto "Plaintext Accounting".
Tutti i dati / transazioni vengono scritti in un file di testo in un formato facilmente leggibile dall'uomo.

Ecco come appare una transazione in questo formato:
```
2023-01-09 document Spese:Ufficio:Altro "Ricevute Spese/Registrate/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Lampada da ufficio" #open #scanned ^2023_004

    Spese:Ufficio:Altro              64.95 EUR

    Passività:Persona:Marc-Bielert
```

# Da Fare

Le donazioni dovrebbero sempre essere tracciate chiaramente, o tramite un conto separato o tramite tag.
Questo è importante per i [Rapporti sulle attività](../_inbox/Tätigkeitsberichte.md) che dobbiamo creare annualmente. #todo
