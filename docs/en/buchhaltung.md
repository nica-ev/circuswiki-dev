---
lang: en
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
translation_updated: 2026-06-06T19:19:57+00:00
---
# Accounting Overview

Our accounting system is based on "plaintext accounting."
All data and transactions are written into a text file in a human-readable format.

A transaction in this format looks like this:
```
2023-01-09 document Expenses:Office:Miscellaneous "Receipts Expenses/Entered/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Office Lamp" #open #scanned ^2023_004

    Expenses:Office:Miscellaneous      64.95 EUR

    Liabilities:Person:Marc-Bielert
```

# To-Do

Donations should always be clearly tracked, either through a separate account or tags.
This is important for the [Activity Reports](../_inbox/Tätigkeitsberichte.md) that we have to create annually. #todo
