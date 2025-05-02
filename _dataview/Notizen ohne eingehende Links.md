# Notizen ohne eingehende Links

Notizen die keine eingehenden Links haben, von denen aber aus verlinkt wird. Verzeichnisse Seedbox, Person, Templates, SyncConflict werden ignoriert.

```dataview 
List 
from "docs"
where length(file.outlinks) > 0
where length(file.inlinks) = 0
```