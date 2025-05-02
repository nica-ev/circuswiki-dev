---
created: 2025-01-23 04:17:46
update: 2025-01-23 04:57:00
---

Zeigt alle Notizen die keine Verlinkung aufweisen, aber Teil des PKM sind, Notizen aus den Verzeichnissen Seedbox, Person, Templates und SyncConflict werden ignoriert.

```dataview 
List 
from "docs"
where length(file.outlinks) = 0
where length(file.inlinks) = 0
```
