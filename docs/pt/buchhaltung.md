---
lang: pt
translation_id: buchhaltung
publish: true
tags:
  - moc
created: 2025-01-19 16:47:55
update: 2026-06-07 00:06:48
title: Buchhaltung Übersicht
authors:
  - Marc Bielert
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/buchhaltung.md
translation_source_hash: be60078ea723f4aec6db8f350c8a5a5597cfee74d578fecbf75f55a97077189f
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T18:31:00+00:00
---
# Visão Geral da Contabilidade

A nossa contabilidade baseia-se na chamada "contabilidade em texto simples" (Plaintext Accounting).
Todos os dados / transações são escritos num ficheiro de texto num formato facilmente legível por humanos.

Uma transação neste formato tem o seguinte aspeto:
```
2023-01-09 document Despesas:Escritório:Outros "Recibos Despesas/Registados/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Lâmpada de escritório" #aberto #digitalizado ^2023_004

    Despesas:Escritório:Outros              64.95 EUR

    Passivos:Pessoa:Marc-Bielert
```

# A Fazer

As doações devem ser sempre rastreadas claramente, seja através de uma conta separada ou de etiquetas (tags).
Isto é importante para os [Relatórios de Atividades](../_inbox/Tätigkeitsberichte.md) que temos de elaborar anualmente. #aFazer
