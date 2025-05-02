---
created: 2025-02-25 15:48:07
update: 2025-03-11 00:29:34
---

# Notizen ohne Verlinkung außer von/zu einem MOC

Zeigt alle Notizen die keine Verlinkung aufweisen außer von/zu einem MOC. Verzeichnisse Seedbox, Person, Template und SyncConflict werden ignoriert.

```dataviewjs
dv.list(dv.pages('"docs"').where( p => p.file.outlinks.filter(l => l.path.endsWith(".md")).every( l => { const linkedPage = dv.page(l.path); return linkedPage && linkedPage.file && linkedPage.file.tags.includes("#moc"); } ) && p.file.inlinks.filter(l => l.path.endsWith(".md")).every( l => { const linkedPage = dv.page(l.path); return linkedPage && linkedPage.file && linkedPage.file.tags.includes("#moc"); } ) && !p.file.path.startsWith("_templates") && !p.file.path.startsWith("_sonstiges") ).file.link )
```