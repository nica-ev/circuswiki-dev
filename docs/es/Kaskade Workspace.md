---
lang: es
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
translation_updated: 2026-06-07T14:07:00+00:00
---
>[!info]- Introducción
>Crecí con Kaskade. Antes de que existiera YouTube, antes de que pudiéramos encontrar todo en Internet, esta revista fue una de las primeras fuentes de información regulares que tuve sobre malabarismo, circo y espectáculos.
>Cuando la revista cesó su publicación en 2013, sentí que era el fin de una era, al menos para mí.
>Durante varios años, las revistas estuvieron disponibles para descargar en formato PDF. Desde aproximadamente 2017, la página dejó de estar en línea.
>A menudo recordaba pequeños talleres, tutoriales o artículos que me inspiraron en aquel entonces. Ahora, años después, cuando quise releer algo, ya no había forma de hacerlo.
>
>Afortunadamente, con la ayuda de la Wayback Machine (The Internet Archive), encontré un punto de control de 2017 con las descargas completas (esto no siempre es así, especialmente porque eran alrededor de 3 GB de PDFs), completas con las ediciones alemana, inglesa y francesa.
>
>Al revisarlas, me di cuenta de que, si bien había muchos artículos y tutoriales geniales escondidos en las revistas, en la actualidad es poco probable que alguien revise 112 revistas que son meras fotocopias. Bueno, a menos que tengas un interés nostálgico =P
>
>Sin embargo, dado que es una pena perder ese conocimiento, quise intentar digitalizarlo con la tecnología actual para que siga siendo útil hoy en día.

>[!info]- ¿Cómo se transcribieron las revistas?
>Primero, eliminé de los PDF todas las páginas que no contenían textos relevantes.
>
>Para la transcripción (o OCR) en sí, utilicé un modelo de lenguaje multimodal de Google.
>Uso ```Gemini 2.0 Pro Experimental 02-05``` con el prompt:
>```
>The attached PDF is a photocopy of a magazine. Extract all text, keep the document structure intact as much as possible, also extract single images and have them correctly in context.
>```
>junto con el PDF de la revista escaneada.
>Configuración: Temperatura 0.1 (importante para evitar alucinaciones).
>
>El resultado se limpia con ```gemini-2.0-flash-exp``` y el siguiente prompt (así como el texto adjunto que hemos extraído):
>```
>The following text is extracted with OCR from an old magazin. Your task is to clean this up. Remove artifacts (like page-numbering, unneccessary linebreaks) or unneeded parts but keep the structure, articles etc. intact. Use a proper Markdown formatting to structure the text correctly.
>
>Text:
>```
>
>El resultado se revisa y corrige manualmente una vez más.
>
>>[!Danger]+ Importante:
>>El enfoque estaba en la extracción de artículos, talleres, entrevistas, etc.
>>He descartado contribuciones como anuncios clasificados, etc.
>>La extracción y limpieza de los textos se realizó con LLMs, por lo que siempre existe la posibilidad de que los textos no se hayan transcrito 1:1 o que el contenido difiera ligeramente del original. Intenté mantener la tasa de error lo más baja posible comparando fragmentos de texto de forma selectiva.

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

# Artículos

<!-- QueryToSerialize: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->
<!-- SerializedQuery: TABLE authors, type, sub-type, source FROM "docs" WHERE contains(file.tags, "kaskade") AND (type != "Magazin") -->

| Archivo                                                                           | autores                                           | tipo     | subtipo | fuente      |
| --------------------------------------------------------------------------------- | ------------------------------------------------- | -------- | ------- | ----------- |
| [Die Säulen-Seite](docs/de/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/de/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artículo | -       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/de/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artículo | -       | Kaskade 001 |
| [Schummeln!](docs/de/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Schwerkraft - na und!](docs/de/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artículo | -       | Kaskade 001 |
| [Zirkus gesucht!](docs/de/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artículo | -       | Kaskade 001 |
| [Die Säulen-Seite](docs/en/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/en/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artículo | -       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/en/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artículo | -       | Kaskade 001 |
| [Schummeln!](docs/en/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Schwerkraft - na und!](docs/en/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artículo | -       | Kaskade 001 |
| [Zirkus gesucht!](docs/en/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artículo | -       | Kaskade 001 |
| [Die Säulen-Seite](docs/pl/Die Säulen-Seite.md)                                 | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Eine neue Zeitschrift für Europa](docs/pl/Eine neue Zeitschrift für Europa.md) | <ul><li>Gabi Keaton</li><li>Paul Keaton</li></ul> | Artículo | -       | Kaskade 001 |
| [Lächeln überwindet Schwerkraft](docs/pl/Lächeln überwindet Schwerkraft.md)     | <ul><li>Toby Philpott</li></ul>                   | Artículo | -       | Kaskade 001 |
| [Schummeln!](docs/pl/Schummeln!.md)                                             | <ul><li>Dr. P. Luftiko</li></ul>                  | Tutorial | Pelotas | Kaskade 001 |
| [Schwerkraft - na und!](docs/pl/Schwerkraft - na und!.md)                       | <ul><li>Christoph Schmitt</li></ul>               | Artículo | -       | Kaskade 001 |
| [Zirkus gesucht!](docs/pl/Zirkus gesucht!.md)                                   | <ul><li>Kattrin & Uli</li></ul>                   | Artículo | -       | Kaskade 001 |

<!-- SerializedQuery END -->

---

>[!info]- Ediciones mal nombradas / combinadas (002 - 004)
>
>Kaskade 002:
>En el PDF original en alemán, las ediciones 2+3 están juntas.
>
>Kaskade 003:
>En el PDF original en alemán, aquí se encuentra la edición 004.
>
>Kaskade 004:
>Aquí falta la portada. Aún no he podido averiguar a qué pertenece...
>Parece una copia de la edición 009, sin portada.
>
>Corrección:
>He dividido el PDF de Kaskade 002 (original) en 002 y 003.
>He renombrado Kaskade 003 (original) a Kaskade 004.
>Y he eliminado Kaskade 004 (original).
