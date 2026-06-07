---
lang: es
translation_id: blog/posts/games-the-data-side
created: 2025-01-21 18:09:55
update: 2025-05-03 22:54:41
date: 2025-03-18T02:14:00
publish: true
tags: 
title: Games - The Data Side
description: How game descriptions were standardized and made more dynamic using metadata and Obsidian plugins.
authors:
  - Marc Bielert
categories: 
  - development
translation_status: machine-translated
translation_source_lang: de
translation_source: docs/de/blog/posts/Games - The Data Side.md
translation_source_hash: 3353b31192222fa2f6b149173311038624bdeac5d127157c14a2f4a801a4d7df
translation_model: google/gemini-2.5-flash-lite
translation_updated: 2026-06-07T13:59:54+00:00
---
# **Juegos - El Lado de los Datos**  
**Cómo se estandarizaron las descripciones de juegos y se hicieron más dinámicas utilizando metadatos y plugins de Obsidian.**

Cuando se trata de gestionar contenido, la coherencia es clave. Para la primera sección principal de este proyecto, me ocupé de los juegos —unos 170, cada uno con su propio formato, estilo y accesibilidad únicos. ¿El problema? Muchas de estas descripciones dependían de enlaces estáticos codificados de forma rígida, lo que hacía una pesadilla añadir nuevos juegos o ajustar la estructura.  

Así que me arremangué y me puse a trabajar.  
<!-- more -->
## Paso 1: Un Formato Unificado  
Lo primero fue establecer un formato coherente para todas las descripciones de juegos. Me inspiré en el "Tasifan Spielebuch" (Libro de Juegos Tasifan), un recurso bien organizado para descripciones de juegos. Para hacerlo aún más fácil de usar, añadí resúmenes cortos para que todos los detalles esenciales sean visibles de un vistazo, incluso en una vista previa.  

¿Pero el verdadero cambio? Los metadatos.  

## Paso 2: Magia de Metadatos  
Ahora, toda la información clave —tamaño del grupo, materiales, duración y más— se almacena como metadatos en la parte superior de cada archivo Markdown en un formato llamado YAML (o *frontmatter*). Esto no solo mantiene las cosas organizadas, sino que también hace que los datos sean reutilizables en todo el sistema.  

Para facilitar la búsqueda del juego adecuado, implementé una lógica simple pero efectiva:  
1. **Elige una categoría**: ¿Qué tipo de juego buscas? ¿Un juego de enfriamiento? ¿Un juego de persecución? ¿Algo para construir equipo? He creado un conjunto de categorías para empezar, pero estas se pueden ajustar o ampliar según sea necesario.  
2. **Explora la tabla**: Una vez que hayas elegido una categoría, verás una tabla que enumera todos los juegos que encajan. La tabla es ordenable: solo haz clic en los encabezados para organizar por duración, dificultad u otros criterios.  

Y aquí está lo mejor: muchos juegos aparecen en varias categorías, por lo que nunca te limitas a una sola forma de encontrar lo que necesitas.  

## Tablas No Tan Dinámicas  
La verdadera magia ocurre con dos plugins de Obsidian: **Dataview** y **Dataview Serializer**.  

Dataview me permite crear listas y tablas dinámicas utilizando consultas similares a las de una base de datos. ¿El inconveniente? Estas tablas solo funcionan dentro de Obsidian porque los archivos Markdown subyacentes no se modifican.  

Entra Dataview Serializer. Este plugin convierte esas tablas dinámicas en formato Markdown estático y las escribe directamente en el archivo. Cuando el sitio se compila usando MkDocs, las tablas son estáticas pero se generaron esencialmente de forma dinámica sin conexión.  

Estas consultas pueden ser bastante complejas, lo que me permite buscar o mostrar partes específicas de la wiki, como todas las descripciones de juegos o artículos escritos por un autor específico. Y como se actualizan automáticamente (a través del paso del serializador), añadir nueva información y construir una estructura navegable es pan comido.  

Pero no todo es color de rosa. El proceso no es totalmente automático. Dataview Serializer solo puede reescribir un archivo si está abierto en Obsidian. Por ahora, esto es manejable: he etiquetado cada página con una tabla o lista dinámica, lo que facilita su recorrido. Pero si el número de estas páginas crece significativamente, podría necesitar repensar el enfoque.  

## Herramientas y Modelos de Lenguaje  
Las descripciones originales de los juegos eran una mezcla en cuanto a formato y calidad. Para agilizar el proceso, recurrí a modelos de lenguaje (LLM). Elaboré un *prompt* específico, completo con formato de ejemplo, para asegurar que el contenido en sí no se alterara (sin reescrituras innecesarias). Aun así, revisé manualmente cada resultado e hice pequeños ajustes donde fue necesario.  

Aquí está la conclusión: cuando se usan correctamente, estas herramientas son *increíblemente* potentes. La clave es ser preciso e intencional en cómo se plantean las tareas.  

Los cambios finales son principalmente de formato: cómo se presenta la información y las descripciones de los juegos. Sin embargo, los metadatos se introdujeron manualmente. Dado que tuve que revisar todo de todos modos, hacerlo a mano fue más rápido en este caso.  

Sin embargo, es un proceso lento. Trabajando a tiempo parcial, gestiono entre 10 y 15 juegos al día. El progreso es constante, pero va a llevar tiempo.  

## Desafíos Futuros  
Un obstáculo potencial son las traducciones. Las consultas de búsqueda tendrían que adaptarse para encontrar versiones específicas del idioma de los juegos o etiquetas. Por ahora, esto se puede manejar manualmente, pero si el sistema crece, la automatización podría ser necesaria.  

La traducción es un tema complejo, y lo abordaré más a fondo en otro momento.  

## ¿Por Qué Molestarse?  
¿La respuesta corta? Escalabilidad.  

Este sistema está diseñado para crecer. Al estandarizar el formato, aprovechar los metadatos y utilizar herramientas dinámicas, he creado una base que puede manejar más contenido sin volverse inmanejable.  

## ¿Qué Más Hay de Nuevo?  
La función de búsqueda ha recibido algunas mejoras:  
- **Autocompletado**: A medida que escribes, la búsqueda sugiere consultas que arrojan la mayor cantidad de resultados. Esto no se basa en el comportamiento del usuario —no rastreamos las búsquedas— sino en el índice de búsqueda estático generado cuando se compila el sitio.  
- **Búsquedas guardadas**: Haz clic en un pequeño icono junto a la barra de búsqueda y tu consulta (y resultados) se guardan en la URL. Márcala como favorita y obtendrás los mismos resultados cada vez.  

Es una característica pequeña, pero podría volverse increíblemente útil a medida que la wiki crezca y cubra temas más diversos.
