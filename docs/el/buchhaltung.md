---
lang: el
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2026-06-07 00:06:48
title: Επισκόπηση Λογιστικής
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T13:33:06+00:00
translation_source_body_hash: 66a642a774547843fee7c0bdb1ce18206708a6fbca5073d4ab4150c381925c2e
translation_source_metadata_hash: c45673cd9d7565ec3ec199693ebf58ec02b3be3bece492c55c65a074f4b82a20
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:05:00+00:00
---
# Επισκόπηση Λογιστικής

Η λογιστική μας βασίζεται στην λεγόμενη "Λογιστική Απλού Κειμένου" (Plaintext Accounting).
Όλα τα δεδομένα / συναλλαγές γράφονται σε ένα αρχείο κειμένου σε μια μορφή ευανάγνωστη από τον άνθρωπο.

Έτσι μοιάζει μια συναλλαγή σε αυτή τη μορφή:
```
2023-01-09 document Ausgaben:Buero:Sonstiges "Belege Ausgaben/Eingetragen/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Buerolampe" #open #scanned ^2023_004

    Ausgaben:Buero:Sonstiges              64.95 EUR

    Verbindlichkeiten:Person:Marc-Bielert
```

# Εργασίες προς Εκτέλεση (Todo)

Οι δωρεές θα πρέπει πάντα να παρακολουθούνται με σαφήνεια, είτε μέσω ενός ξεχωριστού λογαριασμού, είτε μέσω ετικετών (tags).
Αυτό είναι σημαντικό για τις [Εκθέσεις Δραστηριοτήτων](../_inbox/Tätigkeitsberichte.md) που πρέπει να δημιουργούμε ετησίως. #todo
