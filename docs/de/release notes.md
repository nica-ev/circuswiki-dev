---
lang: de
translation_id: release-notes
created: 2025-01-21 18:09:55
update: 2025-03-11 02:46:28
publish: true
tags: 
title: Release Notes
description: 
authors:
  - Marc Bielert
translation_status: original
translation_source_lang: de
---
>[!info]
>Diese Release Notes geben nur einen groben Überblick, kleine Änderungen (wie z.b. einzelne neue Seiten, Änderungen an bestehendem Content) werden nicht alle aufgeführt. Diese können aber in der Historie des Repositories genau nachvollzogen werden.

>[!info]- **Version:** v0.04 - **Release Datum**: 9. Juni 2026
>**Content**
>- Mehrsprachige Inhalte stark erweitert: Inhalte liegen nun strukturiert unter `docs/<sprache>`.
>- Neue und aktualisierte Übersetzungen für viele Spielbeschreibungen und Projektseiten hinzugefügt.
>- Polnische Workshop-Materialien importiert und in die mehrsprachige Inhaltsstruktur integriert.
>- Inhalts- und Metadatenstruktur für Spiele weiter vereinheitlicht.
>
>**Technical**
>- Website-Generator von MkDocs/MkDocs Material auf Zensical umgestellt.
>- Neue mehrsprachige Build- und Staging-Struktur eingeführt.
>- Deutsch bleibt die Standardsprache ohne Sprachprefix; weitere Sprachen werden unter Sprachcodes veröffentlicht, z. B. `/en/`, `/pl/`, `/es/`.
>- Zentrale Sprachkonfiguration über `tools/config/languages.json` eingeführt.
>- GitHub-Pages-Deployment für die neue Zensical-Struktur aktualisiert.
>- Lokale Übersetzungswerkzeuge und Dev Console stark erweitert: Health Checks, Batch-Planung, Übersetzungsstatus, Graph-Ansichten, Navigationstools, Link-Reparatur und Cleanup-Workflows.
>- Sprachumschalter, Übersetzungsstatus-Anzeigen und Fallback-Seiten für fehlende Übersetzungen ergänzt.
>- Tabellen im finalen Site-Output verbessert: sortierbare Tabellen, bessere Darstellung dichter Tabellen und optional einklappbare Seitenbereiche.
>
>**Fixed**
>- Interne Links und Markdown-Links in übersetzten Seiten werden zuverlässiger erhalten und repariert.
>- Mehrsprachige Navigation und URL-Struktur wurden stabilisiert.
>- Responsive Verhalten der Navigation wurde verbessert, insbesondere im Zusammenspiel mit Zensicals mobilem Hamburger-Menü.

>[!info]- **Version:** v0.03 - **Release Datum**: 11. März 2025
>**Content**
>- fehlende Spielebeschreibungen hinzugefügt
>
>**Technical**
>- Favicon + Logo hinzugefügt
>- Redesign UI
>- Navigation ersten Grades ist nun im Header der Seite, während Kontextabhängig die rechte Navigationsleiste angepasst wird
>- Tabellen können durch Klick auf die Header sortiert werden
>
>**Fixed**
>- Tags funktionieren wieder

>[!info]- **Version:** v0.02 - **Release Datum**: 26. Februar 2025
>**Technical**
>- Blog Funktion
>- Analytics (Google)
>- Cookie Banner
>- Feedback widget (bottom of each page)

>[!info]- **Version:** v0.01 - **Release Datum** 15. Januar 2025
>**Content**
>- 150 Spielebeschreibungen hinzugefügt
>- Grundbeschreibung der Dokumentation
>
>**Technical**
>- Basis Setup für Mkdocs and Mkdocs-materials
>- Obsidian Support mit Mkdocs-publisher (erlaubt das nutzen von Obsidian Markdown wie z.b. Markdownlinks, Callout Boxes)

