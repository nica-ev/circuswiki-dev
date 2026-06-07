---
lang: es
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Frontmatter Properties
description: Wie nutzen wir Frontmatter in den Markdown Dateien
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 89bf9ebe8a05134ed70a2642fb5ea6f7381a70cc3e71447f3520e49a039f1264
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:03:08+00:00
---
Utilizamos el siguiente formato de metadatos (frontmatter):

| Propiedad | Tipo de dato | Predeterminado | Explicación                                                                                                                               |
| --------- | ------------ | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| created   | Fecha y hora | automático     | Cuándo se creó el archivo.<br>Se introduce automáticamente.                                                                                |
| update    | Fecha y hora | automático     | Cuándo se modificó el archivo por última vez.<br>Se introduce automáticamente.                                                            |
| publish   | Booleano     | falso          | Decide si un archivo se publicará como parte de la página web.                                                                             |
| tags      | etiquetas    | -              | Las etiquetas definidas aquí también se mostrarán en la página web.                                                                       |
| title     | cadena       | -              | El título se mostrará en la página web como encabezado antes del contenido principal.                                                      |
| authors   | lista        | -              | Una lista de los autores del contenido de esta página.                                                                                    |
