---
lang: en
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2026-06-07 00:06:48
title: Accounting Overview
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T22:24:11+00:00
translation_source_body_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_source_metadata_hash: c45673cd9d7565ec3ec199693ebf58ec02b3be3bece492c55c65a074f4b82a20
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:04:57+00:00
---
# Accounting Overview

Our accounting system is based on what's known as "plaintext accounting."
All data and transactions are written into a text file in a human-readable format.

Here's what a transaction looks like in this format:
```
2023-01-09 document Expenses:Office:Miscellaneous "Receipts Expenses/Entered/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Office Lamp" #open #scanned ^2023_004

    Expenses:Office:Miscellaneous      64.95 EUR

    Liabilities:Person:Marc-Bielert
```

# To-Do

Donations should always be clearly tracked, either through a separate account or tags.
This is important for the [Activity Reports](../_inbox/Tätigkeitsberichte.md) that we have to create annually. #todo
