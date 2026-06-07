---
lang: sk
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
translation_updated: 2026-06-07T18:31:03+00:00
---
# Prehľad účtovníctva

Naše účtovníctvo je založené na tzv. „plaintext accounting“ (účtovníctvo v čistom texte).
Všetky údaje / transakcie sa zapisujú do textového súboru v ľahko čitateľnom formáte.

Takto vyzerá transakcia v tomto formáte:
```
2023-01-09 document Výdavky:Kancelária:Ostatné "Doklady Výdavky/Zadané/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Kancelárska lampa" #open #scanned ^2023_004

    Výdavky:Kancelária:Ostatné                                    64.95 EUR

    Záväzky:Osoba:Marc-Bielert
```

# Úlohy

Dary by sa mali vždy jasne sledovať, buď prostredníctvom samostatného účtu, alebo tagov.
Toto je dôležité pre [správy o činnosti](../_inbox/Tätigkeitsberichte.md), ktoré musíme každoročne vypracúvať. #todo
