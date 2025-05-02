---
created: 2025-04-29 22:36:03
update: 2025-04-30 00:28:23
publish: false
tags: 
title: 
description: 
authors:
---
# CircusWiki Metadata Schema

This document defines the standard YAML front matter metadata fields used across CircusWiki content files (`.md`). Consistent metadata is crucial for organization, search, filtering, and potential automated processing.

## Core Metadata Fields (Mandatory for All Content)

These fields **must** be present in the YAML front matter of every content file intended for publication or management within the wiki.

| Field         | Type             | Mandatory | Description                                                                 | Example                                   |
| :------------ | :--------------- | :-------- | :-------------------------------------------------------------------------- | :---------------------------------------- |
| `publish`     | Boolean          | Yes       | Controls visibility on the published website (`true` = visible, `false` = hidden). | `publish: true`                           |
| `tags`        | List of Strings  | Yes       | Keywords for broad categorization and search filtering. Use lowercase.        | `tags: [game, warmup, coordination]`      |
| `created`     | String           | Yes       | Timestamp (ISO 8601 preferred) when the content was initially created.    | `created: 2024-05-16 10:30:00`            |
| `updated`     | String           | Yes       | Timestamp (ISO 8601 preferred) when the content was last significantly updated. | `updated: 2024-05-17 15:00:00`            |
| `title`       | String           | Yes       | The primary title of the content page, used for display and navigation.     | `title: "Introduction to Juggling"`       |
| `description` | String           | Yes       | A brief (1-2 sentence) summary of the content for search results and previews. | `description: "Basic 3-ball cascade."` |
| `authors`     | List of Strings  | Yes       | Names of the primary author(s) or significant contributors to the content.  | `authors: ["Jane Doe", "John Smith"]`   |

## Content-Type Specific Metadata

Different types of content benefit from additional, specific metadata fields.

### Pedagogical Games

These fields are used for files describing pedagogical games, exercises, or activities.

| Field           | Type             | Mandatory | Description                                                                              | Example                                  |
| :-------------- | :--------------- | :-------- | :--------------------------------------------------------------------------------------- | :--------------------------------------- |
| `category`      | List of Strings  | Yes       | Specific game categories (e.g., icebreaker, tag, circle game). Use lowercase.             | `category: [fangen, kennenlernen]`       |
| `Schwierigkeit` | String           | Yes       | Difficulty level, typically using predefined terms (e.g., `einfach`, `mittel`, `schwer`). | `Schwierigkeit: mittel`                  |
| `Material`      | String / List    | No        | Required materials. Can be a single string or a list if multiple items are needed.       | `Material: Bälle` or `Material: [cones, balls]` |
| `Spieldauer`    | String           | No        | Estimated duration in minutes, often expressed as a range.                                | `Spieldauer: 10-15`                      |
| `source`        | String           | No        | Origin or source of the game/activity. Use `unbekannt` if unknown.                       | `source: "Traditional"` or `source: NICA` |
| `group-min`     | Integer          | No        | Minimum recommended number of participants.                                              | `group-min: 5`                           |
| `group-max`     | Integer          | No        | Maximum recommended number of participants.                                              | `group-max: 20`                          |

*(Note: The exact allowed values for fields like `category` and `Schwierigkeit` should ideally be maintained and potentially listed here or linked to a separate vocabulary list as the wiki grows.)*

## Optional Utility Fields

These fields can be added to any content file for specific internal purposes.

| Field  | Type   | Mandatory | Description                                                                    | Example               |
| :----- | :----- | :-------- | :----------------------------------------------------------------------------- | :-------------------- |
| `todo` | String | No        | Internal notes for editors regarding tasks or improvements needed for this file. | `todo: Add diagrams` |

---

**Schema Evolution:** This schema is intended to evolve. As new content types are added or organizational needs change, this document will be updated. Community feedback on the schema is welcome via Issues or Discussions on the GitHub repository.