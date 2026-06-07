---
lang: cs
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
translation_updated: 2026-06-07T18:31:01+00:00
---
# Přehled účetnictví

Naše účetnictví je založeno na tzv. "Plaintext Accounting" (účetnictví v prostém textu).
Všechna data / transakce se zapisují do textového souboru v lidsky čitelné podobě.

Transakce v tomto formátu vypadá takto:
```
2023-01-09 document Výdaje:Kancelář:Ostatní "Doklady/Výdaje/Zadané/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Kancelářská lampa" #open #scanned ^2023_004

    Výdaje:Kancelář:Ostatní                                    64,95 EUR

    Závazky:Osoba:Marc-Bielert
```

# Úkoly

Dary by měly být vždy jasně sledovány, buď prostřednictvím samostatného účtu, nebo tagů.
To je důležité pro [zprávy o činnosti](../_inbox/Tätigkeitsberichte.md), které musíme každoročně vytvářet. #todo
