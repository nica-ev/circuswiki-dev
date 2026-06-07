---
lang: el
translation_id: kaskade-workspace
created: 2025-01-21 18:09:55
update: 2025-05-03 23:22:16
publish: draft
tags:
  - moc
  - dynamic
title: Transkripte des Kaskade Magazines
description: 
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Kaskade Workspace.md
translation_source_hash: a7bb0dd4700febf2eceb0bf6831cf1c6ab4a4da17f8bad159eaa666c8eceebd3
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T13:47:02+00:00
---
>[!info]- Εισαγωγή
>Μεγάλωσα με το "Kaskade". Πριν υπήρχε το YouTube, πριν μπορούσαμε να βρούμε τα πάντα στο διαδίκτυο – αυτό το περιοδικό ήταν από τις πρώτες τακτικές πηγές πληροφοριών που έφτασαν στα χέρια μου σχετικά με το αντικείμενο του ζογκλερικού, του τσίρκου, των παραστάσεων.
>Όταν το περιοδικό σταμάτησε να εκδίδεται το 2013, ένιωσα σαν το τέλος μιας εποχής – τουλάχιστον για μένα.
>Για αρκετά χρόνια, τα τεύχη του περιοδικού ήταν διαθέσιμα για λήψη σε μορφή PDF, αλλά περίπου από το 2017 η ιστοσελίδα τέθηκε εκτός λειτουργίας.
>Συχνά θυμόμουν μικρά εργαστήρια, οδηγούς ή άρθρα που με είχαν εμπνεύσει τότε. Όταν, χρόνια αργότερα, θέλησα να διαβάσω κάτι ξανά – δεν υπήρχε πλέον τρόπος.
>
>Με τη βοήθεια του Wayback Machine (The Internet Archive), ευτυχώς βρήκα ένα σημείο ελέγχου από το 2017 με τις πλήρεις λήψεις (αυτό δεν συμβαίνει πάντα, ειδικά αφού ήταν περίπου 3 GB PDF) – πλήρες με γερμανική, αγγλική και γαλλική έκδοση.
>
>Κατά την επισκόπηση, συνειδητοποίησα ότι ενώ υπήρχαν πολλά υπέροχα άρθρα και οδηγοί κρυμμένα στα περιοδικά – στη σημερινή εποχή, δύσκολα θα ξεφύλλιζε κανείς 112 περιοδικά που είναι απλώς φωτοτυπημένα. Λοιπόν, εκτός αν έχει κανείς νοσταλγικό ενδιαφέρον =P
>
>Επειδή όμως είναι κρίμα να χαθεί η γνώση, θέλησα να προσπαθήσω, με τη βοήθεια της σύγχρονης τεχνολογίας, να ψηφιοποιήσω τα πάντα με τέτοιο τρόπο ώστε να είναι χρήσιμα και σήμερα.

>[!info]- Πώς έγινε η μεταγραφή των περιοδικών
>Αρχικά, αφαίρεσα όλες τις σελίδες από τα PDF που δεν περιείχαν σχετικά κείμενα.
>
>Για την πραγματική μεταγραφή (ή OCR) χρησιμοποίησα ένα πολυτροπικό γλωσσικό μοντέλο της Google.
>Χρησιμοποιώ το ```Gemini 2.0 Pro Experimental 02-05``` με το prompt
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>καθώς και το PDF με το σαρωμένο περιοδικό.
>Ρυθμίσεις: Temperature 0.1 (Σημαντικό για την αποφυγή παραισθήσεων)
>
>Η έξοδος καθαρίζεται με το ```gemini-2.0-flash-exp``` και το ακόλουθο prompt (καθώς και το συνημμένο κείμενο που εξάγαμε):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Το αποτέλεσμα ελέγχεται ξανά χειροκίνητα και διορθώνεται.
>
>>[!Danger]+ Σημαντικό:
>>Η εστίαση ήταν στην εξαγωγή άρθρων, εργαστηρίων, συνεντεύξεων κ.λπ.
>>Ανακοινώσεις όπως π.χ. αγγελίες κ.λπ. απορρίφθηκαν.
>>Η εξαγωγή και ο καθαρισμός των κειμένων έγιναν με LLMs, επομένως υπάρχει πάντα η πιθανότητα τα κείμενα να μην έχουν μεταγραφεί 1:1 ή το περιεχόμενο να αποκλίνει ελαφρώς από το πρωτότυπο. Προσπάθησα να διατηρήσω το ποσοστό σφάλματος όσο το δυνατόν χαμηλότερο, συγκρίνοντας τυχαία τμήματα κειμένου.

<!-- QueryToSerialize: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
<!-- SerializedQuery: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
- [Kaskade 001](docs/de/Kaskade 001.md)
- [Kaskade 002](docs/de/Kaskade 002.md)
- [Kaskade 003](docs/de/Kaskade 003.md)
- [Kaskade 004](docs/de/Kaskade 004.md)
- [Kaskade 005](docs/de/Kaskade 005.md)
- [Kaskade 001](docs/en/Kaskade 001.md)
- [Kaskade 002](docs/en/Kaskade 002.md)
- [Kaskade 003](docs/en/Kaskade 003.md)
- [Kaskade 004](docs/en/Kaskade 004.md)
- [Kaskade 005](docs/en/Kaskade 005.md)
- [Kaskade 001](docs/pl/Kaskade 001.md)
- [Kaskade 002](docs/pl/Kaskade 002.md)
- [Kaskade 003](docs/pl/Kaskade 003.md)
- [Kaskade 004](docs/pl/Kaskade 004.md)
- [Kaskade 005](docs/pl/Kaskade 005.md)

<!-- SerializedQuery END -->

---

# Άρθρα

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Αρχείο                                                                            | συγγραφείς                                       | τύπος    | υπο-τύπος | πηγή      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | -------- | ----------- |
| [Η Σελίδα των Πυλώνων](docs/de/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Μια νέα εφημερίδα για την Ευρώπη](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Άρθρο   | \-       | Kaskade 001 |
| [Χαμόγελο ξεπερνά τη βαρύτητα](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |
| [Εξαπάτηση!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Βαρύτητα - και λοιπόν!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Άρθρο   | \-       | Kaskade 001 |
| [Ζητείται τσίρκο!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |
| [Η Σελίδα των Πυλώνων](docs/en/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Μια νέα εφημερίδα για την Ευρώπη](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Άρθρο   | \-       | Kaskade 001 |
| [Χαμόγελο ξεπερνά τη βαρύτητα](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |
| [Εξαπάτηση!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Βαρύτητα - και λοιπόν!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Άρθρο   | \-       | Kaskade 001 |
| [Ζητείται τσίρκο!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |
| [Η Σελίδα των Πυλώνων](docs/pl/Die Säulen-Seite.md)                               | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Μια νέα εφημερίδα για την Ευρώπη](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Άρθρο   | \-       | Kaskade 001 |
| [Χαμόγελο ξεπερνά τη βαρύτητα](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |
| [Εξαπάτηση!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Οδηγός  | Μπάλες   | Kaskade 001 |
| [Βαρύτητα - και λοιπόν!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Άρθρο   | \-       | Kaskade 001 |
| [Ζητείται τσίρκο!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Άρθρο   | \-       | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Λανθασμένα ονομασμένες / συνδυασμένες εκδόσεις (002 - 004)
>
>Kaskade 002:
>Στο αρχικό γερμανικό PDF, οι εκδόσεις 2+3 είναι μαζί.
>
>Kaskade 003:
>Στο αρχικό γερμανικό PDF, εδώ βρίσκεται η έκδοση 004.
>
>Kaskade 004:
>Εδώ λείπει η σελίδα τίτλου, δεν έχω καταφέρει ακόμα να ανακαλύψω σε τι ανήκει...
>Μοιάζει με αντίγραφο της έκδοσης 009, χωρίς σελίδα τίτλου.
>
>Διόρθωση:
>Έχω χωρίσει το PDF του Kaskade 002 (πρωτότυπο) σε 002 και 003.
>Το Kaskade 003 (πρωτότυπο) μετονομάστηκε σε Kaskade 004.
>Και το Kaskade 004 (πρωτότυπο) διαγράφηκε.
