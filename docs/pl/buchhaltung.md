---
lang: pl
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2026-06-07 00:06:48
title: Przegląd księgowości
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T22:30:37+00:00
translation_source_body_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_source_metadata_hash: c45673cd9d7565ec3ec199693ebf58ec02b3be3bece492c55c65a074f4b82a20
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:04:58+00:00
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
