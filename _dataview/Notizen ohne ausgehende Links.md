---
created: 2025-01-23 04:17:46
update: 2025-01-23 22:03:24
---

Notizen die keine ausgehenden Links haben, zu denen aber gelinkt wird. Verzeichnisse Seedbox, Person, Templates, SyncConflict werden ignoriert.

```dataview 
List 
from "docs"
where length(file.outlinks) = 0
where length(file.inlinks) > 0
```