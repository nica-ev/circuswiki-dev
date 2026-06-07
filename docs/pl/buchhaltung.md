---
lang: pl
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
translation_updated: 2026-06-06T22:30:37+00:00
---
# Przegląd Księgowości

Nasza księgowość opiera się na tzw. „księgowości w czystym tekście” (Plaintext Accounting).
Wszystkie dane / transakcje zapisuje się w pliku tekstowym w formacie łatwym do odczytania przez człowieka.

Tak wygląda transakcja w tym formacie:
```
2023-01-09 document Wydatki:Biuro:Inne "Paragony Wydatki/Wprowadzone/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Lampa biurowa" #open #scanned ^2023_004

    Wydatki:Biuro:Inne                 64.95 EUR

    Zobowiązania:Osoba:Marc-Bielert
```

# Do Zrobienia

Darowizny powinny być zawsze jasno śledzone, albo poprzez osobne konto, albo za pomocą tagów.
Jest to ważne dla [raportów z działalności](../_inbox/Tätigkeitsberichte.md), które musimy sporządzać corocznie. #todo
