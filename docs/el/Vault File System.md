---
lang: el
translation_id: vault-file-system
created: 2025-01-21 18:09:55
update: 2025-01-25 02:06:00
publish: true
tags: 
title: Vault File System
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Vault File System.md
translation_source_hash: d418e7c5944943e87dc15e652b5d223265fb03145f2906ae04de273b545ebae4
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T13:55:54+00:00
---
```code
/_attachments/        
/_canvas/             
/_dataview/           
/_inbox/
/_sonstiges/
/_templates/
/docs/
/site/
license
mkdocs.yml
readme.md
```

Κάθε φάκελος με το πρόθεμα _ είναι φάκελος συστήματος

# ```_attachments```  
Όλες οι εικόνες, τα PDF και άλλα συνημμένα αρχεία

- κυρίως για να διατηρείται η τάξη
- για να διαχωρίζονται τα δεδομένα εικόνας και κειμένου
- για να απλοποιηθεί η μελλοντική οργάνωση σε μεγάλες ποσότητες δεδομένων
- για να απλοποιηθούν οι μελλοντικές αυτοματοποιήσεις

❗Αυτή τη στιγμή, αυτός ο φάκελος αγνοείται από το Git. Χρειάζεται περαιτέρω σκέψη για το πώς θα διαχειριστούμε τα δεδομένα εικόνας. Αυτό σημαίνει ότι τα δεδομένα εικόνας είναι προς το παρόν διαθέσιμα μόνο τοπικά (και φυσικά στην τελική ιστοσελίδα), αλλά δεν αποτελούν μέρος του αποθετηρίου αυτή τη στιγμή. #todo

# ```_canvas```
Το Canvas είναι ένα χαρακτηριστικό του Obsidian, το οποίο είναι κατάλληλο για mind maps και παρόμοια. 
Δεδομένου ότι το χρησιμοποιούμε μόνο εντός του Obsidian, τα δεδομένα είναι διαχωρισμένα
