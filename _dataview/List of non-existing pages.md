---
created: 2025-01-23 04:17:46
update: 2025-01-25 18:44:52
---

Notizen die erwähnt/verlinkt sind aber noch nicht existieren.

```dataviewjs 
let r = Object.entries(dv.app.metadataCache.unresolvedLinks) .filter(([k,v])=>Object.keys(v).length) .flatMap(([k,v]) => Object.keys(v).map(x=>dv.fileLink(x))) 
dv.list([...new Set(r)]) 
```

