---
lang: es
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
translation_updated: 2026-06-07T14:00:17+00:00
---
# Resumen de Contabilidad

Nuestra contabilidad se basa en la llamada "contabilidad en texto plano".
Todos los datos / transacciones se escriben en un archivo de texto en un formato fácilmente legible por humanos.

Así se ve una transacción en este formato:
```
2023-01-09 document Gastos:Oficina:Otros "Recibos Gastos/Registrados/2023_004.jpg" ^2023_004

2023-01-09 ! "Hornbach" "Lámpara de oficina" #open #scanned ^2023_004

    Gastos:Oficina:Otros              64.95 EUR

    Pasivos:Persona:Marc-Bielert
```

# Tareas Pendientes

Las donaciones siempre deben registrarse claramente, ya sea a través de una cuenta separada o mediante etiquetas.
Esto es importante para los [Informes de Actividades](../_inbox/Tätigkeitsberichte.md) que debemos elaborar anualmente. #todo
