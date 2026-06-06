---
lang: pl
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
translation_updated: 2026-06-06T20:08:36+00:00
---
# **Gry – Aspekt Danych**
**Jak opisy gier zostały ustandaryzowane i uczynione bardziej dynamicznymi dzięki metadanym i wtyczkom Obsidian.**

Jeśli chodzi o zarządzanie treścią, kluczowa jest spójność. W pierwszej dużej części tego projektu zająłem się grami – około 170 z nich, każda z własnym, unikalnym formatem, stylem i dostępnością. Problem? Wiele z tych opisów opierało się na zakodowanych na stałe, statycznych linkach, co sprawiało, że dodawanie nowych gier lub dostosowywanie struktury było koszmarem.

Więc podwinąłem rękawy i zabrałem się do pracy.
<!-- more -->
## Krok 1: Jednolity Format
Pierwszym krokiem było ustalenie spójnego formatu dla wszystkich opisów gier. Inspirację czerpałem z „Tasifan Spielebuch” (Księgi Gier Tasifan), dobrze zorganizowanego źródła opisów gier. Aby uczynić rzeczy jeszcze bardziej przyjaznymi dla użytkownika, dodałem krótkie podsumowania, dzięki czemu wszystkie kluczowe szczegóły są widoczne na pierwszy rzut oka – nawet w podglądzie.

Ale prawdziwą rewolucją? Metadane.

## Krok 2: Magia Metadanych
Teraz wszystkie kluczowe informacje – liczba graczy, materiały, czas trwania i inne – są przechowywane jako metadane na górze każdego pliku Markdown w formacie zwanym YAML (lub frontmatter). To nie tylko utrzymuje porządek, ale także sprawia, że dane są wielokrotnego użytku w całym systemie.

Aby ułatwić znalezienie odpowiedniej gry, wdrożyłem prostą, ale skuteczną logikę:
1. **Wybierz kategorię**: Jakiego rodzaju gry szukasz? Gra wyciszająca? Gra w berka? Coś do budowania zespołu? Stworzyłem zestaw kategorii na początek, ale można je dostosowywać lub rozszerzać w miarę potrzeb.
2. **Przeglądaj tabelę**: Po wybraniu kategorii zobaczysz tabelę zawierającą wszystkie pasujące gry. Tabela jest sortowalna – wystarczy kliknąć nagłówki, aby uporządkować według czasu trwania, trudności lub innych kryteriów.

A oto najlepsze: wiele gier pojawia się w wielu kategoriach, więc nigdy nie jesteś ograniczony tylko jednym sposobem na znalezienie tego, czego potrzebujesz.

## Tabele Nie-Do-Końca-Dynamiczne
Prawdziwa magia dzieje się dzięki dwóm wtyczkom Obsidian: **Dataview** i **Dataview Serializer**.

Dataview pozwala mi tworzyć dynamiczne listy i tabele za pomocą zapytań podobnych do bazodanowych. Haczyk? Te tabele działają tylko w Obsidian, ponieważ bazowe pliki Markdown nie są modyfikowane.

Tu wkracza Dataview Serializer. Ta wtyczka konwertuje te dynamiczne tabele do statycznego formatu Markdown i zapisuje je bezpośrednio w pliku. Kiedy strona jest budowana za pomocą MkDocs, tabele są statyczne, ale zostały zasadniczo wygenerowane dynamicznie offline.

Te zapytania mogą być dość złożone, pozwalając mi wyszukiwać lub wyświetlać określone części wiki – takie jak wszystkie opisy gier lub artykuły napisane przez konkretnego autora. A ponieważ aktualizują się automatycznie (poprzez krok serializacji), dodawanie nowych informacji i budowanie nawigacyjnej struktury jest dziecinnie proste.

Ale nie wszystko jest idealne. Proces nie jest w pełni zautomatyzowany. Dataview Serializer może nadpisać plik tylko wtedy, gdy jest on otwarty w Obsidian. Na razie jest to wykonalne – oznaczyłem każdą stronę z dynamiczną tabelą lub listą, co ułatwia ich przeglądanie. Ale jeśli liczba tych stron znacznie wzrośnie, być może będę musiał przemyśleć podejście.

## Narzędzia i Modele Językowe
Oryginalne opisy gier były mieszanką pod względem formatowania i jakości. Aby usprawnić proces, zwróciłem się do modeli językowych (LLM). Stworzyłem specyficzny prompt, wraz z przykładowym formatowaniem, aby zapewnić, że sama treść nie zostanie zmieniona (bez niepotrzebnych przepisów). Mimo to, ręcznie przeglądałem każdy wynik i wprowadzałem drobne poprawki tam, gdzie były potrzebne.

Oto wnioski: przy prawidłowym użyciu te narzędzia są *niezwykle* potężne. Kluczem jest precyzja i celowość w formułowaniu zadań.

Ostateczne zmiany dotyczą głównie formatowania – sposobu prezentacji informacji i opisów gier. Metadane natomiast były wprowadzane ręcznie. Ponieważ i tak musiałem wszystko dwukrotnie sprawdzić, zrobienie tego ręcznie było w tym przypadku szybsze.

Jest to jednak powolny proces. Pracując w niepełnym wymiarze godzin, udaje mi się przetworzyć około 10-15 gier dziennie. Postęp jest stały, ale zajmie to trochę czasu.

## Wyzwania na Przyszłość
Jedną z potencjalnych przeszkód są tłumaczenia. Zapytania wyszukiwania musiałyby zostać dostosowane, aby znaleźć wersje gier lub tagów specyficzne dla danego języka. Na razie można sobie z tym poradzić ręcznie, ale jeśli system się rozrośnie, automatyzacja może być konieczna.

Tłumaczenie to złożony temat, do którego wrócę innym razem.

## Po Co Się W To Zagłębiać?
Krótka odpowiedź? Skalowalność.

Ten system jest zaprojektowany tak, aby mógł się rozwijać. Standaryzując format, wykorzystując metadane i stosując dynamiczne narzędzia, stworzyłem fundament, który może obsłużyć więcej treści bez stawania się nieporęcznym.

## Co Jeszcze Nowego?
Funkcja wyszukiwania doczekała się kilku ulepszeń:
- **Autouzupełnianie**: Podczas pisania wyszukiwanie sugeruje zapytania, które dają najwięcej trafień. Nie opiera się to na zachowaniu użytkownika – nie śledzimy wyszukiwań – ale na statycznym indeksie wyszukiwania generowanym podczas budowania strony.
- **Zapisane wyszukiwania**: Kliknij małą ikonę obok paska wyszukiwania, a Twoje zapytanie (i wyniki) zostaną zapisane w adresie URL. Dodaj je do zakładek, a za każdym razem uzyskasz te same wyniki.

To mała funkcja, ale może okazać się niezwykle przydatna w miarę rozwoju wiki i obejmowania coraz bardziej zróżnicowanych tematów.
