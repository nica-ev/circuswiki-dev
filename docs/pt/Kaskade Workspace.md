---
lang: pt
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
translation_updated: 2026-06-07T18:58:54+00:00
---
>[!info]- Introdução
>Cresci com a Kaskade. Antes de existir o YouTube, antes de podermos encontrar tudo na internet – esta revista foi uma das primeiras fontes regulares de informação que recebi sobre malabarismo, circo e espetáculos.
>Quando a revista foi descontinuada em 2013, pareceu o fim de uma era – pelo menos para mim.
>Durante vários anos, as revistas estiveram disponíveis para download em PDF. Por volta de 2017, o site saiu do ar.
>Muitas vezes lembrei-me de pequenos workshops, tutoriais ou artigos que me inspiraram na altura. Agora, anos depois, quando quis reler algo – já não havia forma de o fazer.
>
>Com a ajuda da Wayback Machine (The Internet Archive), tive a sorte de encontrar um ponto de verificação de 2017 com os downloads completos (o que nem sempre acontece, especialmente porque eram cerca de 3 GB de PDFs) – completo com edições em alemão, inglês e francês.
>
>Ao rever, percebi que, embora muitos artigos e tutoriais fantásticos estivessem escondidos nas revistas – nos dias de hoje, dificilmente alguém passaria 112 revistas, que são apenas fotocópias, a pente fino. Bem, a menos que se tenha um interesse nostálgico =P
>
>No entanto, como é uma pena que este conhecimento se perca, quis tentar usar a tecnologia atual para digitalizar tudo de forma que ainda seja útil hoje em dia.

>[!info]- Como as revistas foram transcritas
>Primeiro, removi todas as páginas do PDF que não continham textos relevantes.
>
>Para a transcrição (ou OCR) em si, usei um modelo de linguagem multimodal do Google.
>Utilizei o ```Gemini 2.0 Pro Experimental 02-05``` com o prompt:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>bem como o PDF com a revista digitalizada.
>Configurações: Temperatura 0.1 (Importante para evitar alucinações)
>
>O resultado é limpo com ```gemini-2.0-flash-exp``` e o seguinte prompt (bem como o texto anexado que extraímos):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>O resultado é então revisto e corrigido manualmente.
>
>>[!Danger]+ Importante:
>>O foco foi na extração de artigos, workshops, entrevistas, etc.
>>Contribuições como anúncios classificados, etc., foram descartadas.
>>A extração e limpeza dos textos foram realizadas com LLMs, pelo que existe sempre a possibilidade de os textos não terem sido transcritos 1:1 ou de o conteúdo diferir ligeiramente do original. Tentei manter a taxa de erro o mais baixa possível, comparando trechos de texto aleatoriamente.

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

# Artigos

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Ficheiro                                                                          | autores                                           | tipo     | subtipo | fonte       |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | ------- | ----------- |
| [Die Säulen-Seite](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artigo   | \-      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artigo   | \-      | Kaskade 001 |
| [Schummeln!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Schwerkraft - na und!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artigo   | \-      | Kaskade 001 |
| [Zirkus gesucht!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artigo   | \-      | Kaskade 001 |
| [Die Säulen-Seite](docs/en/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artigo   | \-      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artigo   | \-      | Kaskade 001 |
| [Schummeln!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Schwerkraft - na und!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artigo   | \-      | Kaskade 001 |
| [Zirkus gesucht!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artigo   | \-      | Kaskade 001 |
| [Die Säulen-Seite](docs/pl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artigo   | \-      | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artigo   | \-      | Kaskade 001 |
| [Schummeln!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Bolas   | Kaskade 001 |
| [Schwerkraft - na und!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artigo   | \-      | Kaskade 001 |
| [Zirkus gesucht!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artigo   | \-      | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Edições com nome incorreto / combinadas (002 - 004)
>
>Kaskade 002:
>No PDF original em alemão, as edições 2+3 estão juntas.
>
>Kaskade 003:
>Nesta edição, encontra-se a edição 004 no PDF original em alemão.
>
>Kaskade 004:
>Falta a página de rosto aqui, ainda não consegui descobrir a que pertence...
>Parece uma cópia da edição 009, sem página de rosto.
>
>Correção:
>Dividi o PDF da Kaskade 002 (original) em 002 e 003.
>Renomeei a Kaskade 003 (original) para Kaskade 004.
>E apaguei a Kaskade 004 (original).
