---
lang: es
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Propiedades de Frontmatter
description: Cómo usamos Frontmatter en los archivos Markdown
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T14:03:08+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:35+00:00
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
