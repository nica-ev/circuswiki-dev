---
lang: el
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
translation_updated: 2026-06-07T13:33:06+00:00
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
