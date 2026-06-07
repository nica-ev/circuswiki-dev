---
lang: it
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
translation_updated: 2026-06-06T23:05:13+00:00
---
>[!info]- Introduzione
>Sono cresciuto con "Kaskade". Prima che esistesse YouTube, prima che potessimo trovare tutto su Internet, questa rivista è stata una delle prime fonti di informazione regolari che ho avuto sul giocoleria, sul circo e sugli spettacoli.
>Quando la rivista è stata interrotta nel 2013, mi è sembrata la fine di un'era, almeno per me.
>Per diversi anni le riviste sono state ancora disponibili per il download in formato PDF; dal 2017 circa il sito è andato offline.
>Mi sono spesso ricordato di piccoli workshop, tutorial o articoli che mi avevano ispirato all'epoca. Ora, anni dopo, quando volevo rileggere qualcosa, non c'era più modo.
>
>Fortunatamente, utilizzando la Wayback Machine (The Internet Archive), ho trovato un punto di salvataggio del 2017 con i download completi (non è sempre così, soprattutto perché si trattava di circa 3 GB di PDF), completi di edizioni tedesca, inglese e francese.
>
>Riguardandoli, mi sono reso conto che, sebbene ci fossero molti ottimi articoli e tutorial nascosti nelle riviste, oggi difficilmente qualcuno sfoglierebbe 112 riviste semplicemente fotocopiate. Beh, a meno che non si abbia un interesse nostalgico =P
>
>Dato che sarebbe un peccato perdere queste conoscenze, ho voluto provare a digitalizzare il tutto utilizzando la tecnologia attuale in modo che sia ancora utile oggi.

>[!info]- Come sono state trascritte le riviste
>Per prima cosa ho rimosso da ogni pagina del PDF quelle che non contenevano testi rilevanti.
>
>Per la trascrizione vera e propria (o OCR) ho utilizzato un modello linguistico multimodale di Google.
>Utilizzo ```Gemini 2.0 Pro Experimental 02-05``` con il prompt:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>insieme al PDF con la rivista scansionata.
>Impostazioni: Temperatura 0.1 (Importante per evitare allucinazioni)
>
>L'output viene ripulito con ```gemini-2.0-flash-exp``` e il seguente prompt (insieme al testo allegato che abbiamo estratto):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>Il risultato viene poi rivisto e corretto manualmente.
>
>>[!Danger]+ Importante:
>>L'obiettivo era estrarre articoli, workshop, interviste, ecc.
>>Ho scartato contributi come annunci economici, ecc.
>>L'estrazione e la pulizia dei testi sono state eseguite con LLM, quindi esiste sempre la possibilità che i testi non siano stati trascritti 1:1 o che il contenuto differisca leggermente dall'originale. Ho cercato di mantenere la percentuale di errore il più bassa possibile confrontando a campione parti di testo.

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

# Articoli

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| File                                                                              | authors                                           | type     | sub-type | source      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | -------- | ----------- |
| [La pagina dei pilastri](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Una nuova rivista per l'Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Articolo  | \-       | Kaskade 001 |
| [Sorridere vince la gravità](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Articolo  | \-       | Kaskade 001 |
| [Barare!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Gravità - e allora!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Articolo  | \-       | Kaskade 001 |
| [Cerchiamo un circo!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Articolo  | \-       | Kaskade 001 |
| [La pagina dei pilastri](docs/en/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Una nuova rivista per l'Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Articolo  | \-       | Kaskade 001 |
| [Sorridere vince la gravità](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Articolo  | \-       | Kaskade 001 |
| [Barare!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Gravità - e allora!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Articolo  | \-       | Kaskade 001 |
| [Cerchiamo un circo!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Articolo  | \-       | Kaskade 001 |
| [La pagina dei pilastri](docs/pl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Una nuova rivista per l'Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Articolo  | \-       | Kaskade 001 |
| [Sorridere vince la gravità](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Articolo  | \-       | Kaskade 001 |
| [Barare!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Palle    | Kaskade 001 |
| [Gravità - e allora!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Articolo  | \-       | Kaskade 001 |
| [Cerchiamo un circo!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Articolo  | \-       | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Edizioni nominate erroneamente / aggregate (002 - 004)
>
>Kaskade 002:
>Nel PDF originale tedesco, le edizioni 2 e 3 sono unite.
>
>Kaskade 003:
>Nel PDF originale tedesco, qui si trova l'edizione 004.
>
>Kaskade 004:
>Qui manca la copertina, non sono ancora riuscito a capire a cosa appartenga...
>Sembra una copia dell'edizione 009, senza copertina.
>
>Correzione:
>Ho diviso il PDF di Kaskade 002 (originale) in 002 e 003.
>Ho rinominato Kaskade 003 (originale) in Kaskade 004.
>E ho eliminato Kaskade 004 (originale).
