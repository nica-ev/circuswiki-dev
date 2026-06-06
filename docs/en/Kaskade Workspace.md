---
lang: en
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
translation_source_hash: ae8f36f6540d80a5be5070905e4aa7251d85170462ef6b36f1c6440762b237f2
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-06T19:25:55+00:00
---
>[!info]- Introduction
>I grew up with Kaskade. Before YouTube existed, before we could find everything on the internet – this magazine was one of the first regular sources of information I got my hands on about juggling, circus, and shows.
>When the magazine ceased publication in 2013, it felt like the end of an era – at least for me.
>For several years, the magazines were still available for download as PDFs. Around 2017, the website went offline.
>I often remembered small workshops, tutorials, or articles that had inspired me back then. Now, years later, when I wanted to re-read something – there was no way to access them anymore.
>
>Fortunately, using the Wayback Machine (The Internet Archive), I found a checkpoint from 2017 with the complete downloads (this isn't always the case, especially since it was about 3 GB of PDFs) – complete with German, English, and French editions.
>
>While reviewing them, I realized that while many great articles and tutorials were hidden within the magazines, in today's world, hardly anyone would sift through 112 magazines that are merely photocopies. Well, unless you have a nostalgic interest =P
>
>However, since the knowledge is too valuable to lose, I wanted to try using current technology to digitize everything in a way that makes it useful even today.

>[!info]- How the Magazines Were Transcribed
>First, I removed all pages from the PDF that did not contain relevant text.
>
>For the actual transcription (or OCR), I used a multimodal language model from Google.
>I used ```Gemini 2.0 Pro Experimental 02-05``` with the prompt
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>along with the PDF containing the scanned magazine.
>Settings: Temperature 0.1 (Important to avoid hallucinations)
>
>The output is then cleaned up with ```gemini-2.0-flash-exp``` and the following prompt (along with the attached text we extracted):
>```
>The following text is extracted with OCR from an old magazine. Your task is to clean this up. Remove artifacts (like page-numbering, unnecessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>The result is then reviewed and corrected manually.
>
>>[!Danger]+ Important:
>>The focus was on extracting articles, workshops, interviews, etc.
>>Contributions like classified ads, etc., were discarded.
>>The extraction and cleaning of the texts were performed using LLMs, so there is always a possibility that texts were not transcribed 1:1 or that the content slightly deviates from the original. I tried to keep the error rate as low as possible by comparing text passages at random.

<!-- QueryToSerialize: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
<!-- SerializedQuery: LIST FROM "docs" WHERE contains(file.tags, "kaskade") AND (type = "Magazin") -->
- [Kaskade 002](docs/de/Kaskade 002.md)
- [Kaskade 001](docs/de/Kaskade 001.md)
- [Kaskade 003](docs/de/Kaskade 003.md)
- [Kaskade 004](docs/de/Kaskade 004.md)
- [Kaskade 005](docs/de/Kaskade 005.md)

<!-- SerializedQuery END -->

---

# Articles

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| File                                                                              | authors                                           | type     | sub-type | source      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | -------- | ----------- |
| [The Pillar Page](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Balls    | Kaskade 001 |
| [A New Magazine for Europe](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Article  | -        | Kaskade 001 |
| [Smiling Overcomes Gravity](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Article  | -        | Kaskade 001 |
| [Cheating!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Balls    | Kaskade 001 |
| [Gravity - So What!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Article  | -        | Kaskade 001 |
| [Circus Wanted!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Article  | -        | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Incorrectly Named / Combined Issues (002 - 004)
>
>Kaskade 002:
>In the original German PDF, issues 2 and 3 are combined.
>
>Kaskade 003:
>In the original German PDF, issue 004 is found here.
>
>Kaskade 004:
>The title page is missing here. I haven't figured out what it belongs to yet...
>It looks like a copy of issue 009, without a title page.
>
>Fix:
>I split the PDF of Kaskade 002 (original) into 002 and 003.
>Renamed Kaskade 003 (original) to Kaskade 004.
>And deleted Kaskade 004 (Original).
