---
lang: pt
translation_id: frontmatter-properties
created: 2025-01-21 18:09:55
update: 2025-01-25 02:07:04
publish: true
tags: 
title: Propriedades do Frontmatter
description: Como usamos o Frontmatter em arquivos Markdown
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/Frontmatter Properties.md
translation_source_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T18:45:36+00:00
translation_source_body_hash: 2e30831383593168acdb0184b17d6967214f93b5e052c4e649cbab6fd46ba0aa
translation_source_metadata_hash: 134e1df473510011b7c4bdb6bf2f3f47be26193c9f2618b69e370d8eb38bb00d
translation_metadata_model: google/gemini-2.5-flash-lite
translation_metadata_status: machine-translated
translation_metadata_updated: 2026-06-10T18:47:36+00:00
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
