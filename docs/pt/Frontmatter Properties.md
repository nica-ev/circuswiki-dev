---
lang: pt
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
translation_updated: 2026-06-07T18:45:36+00:00
---
Utilizamos o seguinte formato de frontmatter

| Propriedade | Tipo de Dado | Padrão | Explicação                                                                                                                            |
| ----------- | ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| created     | Data e Hora  | auto   | Quando o arquivo foi criado<br>é inserido automaticamente                                                                             |
| update      | Data e Hora  | auto   | Quando o arquivo foi modificado pela última vez,<br>é inserido automaticamente                                                       |
| publish     | Booleano     | false  | Decide se um arquivo será publicado como parte do site                                                                                |
| tags        | tags         | -      | As tags definidas aqui também serão exibidas no site                                                                                 |
| title       | string       | -      | O título será exibido no site como um cabeçalho antes do conteúdo principal                                                           |
| authors     | lista        | -      | Uma lista dos autores do conteúdo desta página                                                                                        |
