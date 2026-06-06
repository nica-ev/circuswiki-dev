---
lang: pl
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2025-01-23 05:44:55
title: Buchhaltung Übersicht
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: 7e7515fc48e5a6c76a28064818db4443942ef404101f5517cd02e9fcb355be41
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T20:08:59+00:00
---
# Księgowość – Przegląd

Nasza księgowość opiera się na tzw. „księgowości w czystym tekście” (ang. Plaintext Accounting).
Wszystkie dane / transakcje zapisuje się w pliku tekstowym w formacie czytelnym dla człowieka.

Tak wygląda transakcja w tym formacie:
```
2023-01-09 document Wydatki:Biuro:Inne "Paragony Wydatki/Zapisane/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Lampa biurowa" #open #scanned ^2023_004

    Wydatki:Biuro:Inne                                                64.95 EUR

    Zobowiązania:Osoba:Marc-Bielert
```

# Do zrobienia

Darowizny powinny być zawsze jasno śledzone, albo poprzez osobne konto, albo przez tagi.
Jest to ważne dla [raportów z działalności](../_inbox/Tätigkeitsberichte.md), które musimy sporządzać co roku. #todo
