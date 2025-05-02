---
created: 2025-03-17 01:07:58
update: 2025-03-25 23:27:29
publish: false
tags: 
title: 
description: 
authors:
---

```dataview 
Table Schwierigkeit, group-min, group-max, todo FROM #spiele WHERE category
```

## Categories

```dataview
TABLE length(rows) AS Count FROM "" FLATTEN category AS cat GROUP BY cat SORT cat ASC
```
