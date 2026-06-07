---
lang: uk
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
translation_updated: 2026-06-07T14:18:57+00:00
---
# Огляд бухгалтерії

Наша бухгалтерія базується на так званому "Plaintext Accounting" (бухгалтерія у простому тексті).
Усі дані / транзакції записуються у текстовий файл у форматі, який легко читається людиною.

Ось як виглядає транзакція у цьому форматі:
```
2023-01-09 document Витрати:Офіс:Інше "Квитанції Витрати/Внесено/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Офісна лампа" #open #scanned ^2023_004

    Витрати:Офіс:Інше                                             64.95 EUR

    Зобов'язання:Особа:Marc-Bielert
```

# Завдання

Пожертви завжди слід чітко відстежувати, або через окремий рахунок, або за допомогою тегів.
Це важливо для [звітів про діяльність](../_inbox/Tätigkeitsberichte.md), які ми повинні складати щорічно. #todo
