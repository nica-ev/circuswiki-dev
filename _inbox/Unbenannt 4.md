---
created: 2025-05-27 22:28:42
update: 2025-05-27 22:30:32
publish: false
tags: 
title: 
description: 
authors: 
selected-mode: folder
selected-folder: ""
selected-template: ""
selected-tag: ""
selected-property: ""
include-subfolders: true
---

```dataviewjs
// =======================
// 🛠 Constants & Helpers
// =======================

const STYLES = {
    input: "width: 100%; padding: 6px 8px; margin-bottom: 1em; border-radius: 4px; border: 1px solid var(--interactive-accent);",
    button: "padding: 8px 12px; border: 1px solid var(--interactive-accent); border-radius: 6px; cursor: pointer; margin-top: 1em;",
    primaryButton: "background-color: var(--interactive-accent); color: var(--text-on-accent);",
    secondaryButton: "background-color: var(--background-secondary); color: var(--text-normal); margin-left: 1em;",
    label: "font-weight: bold;",
    summaryBox: "background-color: var(--background-secondary); padding: 12px; border-radius: 6px; margin: 1em 0; border-left: 4px solid var(--interactive-accent);",
    successMessage: "color: var(--color-green); font-weight: bold; padding: 12px; background-color: var(--background-secondary); border-radius: 6px; margin: 1em 0;",
    table: "width: 100%; border-collapse: collapse; margin: 1em 0;",
    tableHeader: "border: 1px solid var(--background-modifier-border); padding: 8px; text-align: left; background-color: var(--background-secondary);",
    tableCell: "border: 1px solid var(--background-modifier-border); padding: 8px;",
};

// Cache data
let cachedData = null;
const getData = () => cachedData || (cachedData = {
    folders: app.vault.getAllLoadedFiles().filter(f => f instanceof obsidian.TFolder).map(f => f.path).sort(),
    mdFiles: app.vault.getMarkdownFiles().map(f => f.path).sort(),
    allTags: [...new Set(dv.pages().flatMap(p => p.tags || []))].map(t => t.replace(/^#/, "")).sort(),
    allProperties: [...new Set(dv.pages().flatMap(p => Object.keys(p).filter(k => !k.startsWith("file") && k !== "tags")))].sort()
});

// Path helpers
const normalizePath = (name) => {
    if (!name) return "";
    if (name.endsWith('.md')) return name;
    return getData().mdFiles.find(f => f.replace(/\.md$/, '') === name) || name + '.md';
};

const stripExt = (path) => path.replace(/\.md$/, '');

// Storage
const KEYS = { mode: "selected-mode", folder: "selected-folder", template: "selected-template", tag: "selected-tag", property: "selected-property", includeSubfolders: "include-subfolders" };
const defaults = { mode: "folder", folder: "", template: "", tag: "", property: "", includeSubfolders: true };

const withFrontMatter = async (fn) => {
    const file = app.vault.getAbstractFileByPath(dv.current().file.path);
    if (file) await app.fileManager.processFrontMatter(file, fn);
};

const load = async () => {
    const selections = {...defaults};
    await withFrontMatter(fm => {
        Object.entries(KEYS).forEach(([k, v]) => {
            if (fm[v] !== undefined) selections[k] = k === 'includeSubfolders' ? fm[v] !== false : fm[v];
        });
    });
    return selections;
};

const save = async (sel) => withFrontMatter(fm => Object.entries(KEYS).forEach(([k, v]) => fm[v] = sel[k]));
const clear = async () => withFrontMatter(fm => Object.values(KEYS).forEach(k => delete fm[k]));

// UI Builder with save on blur/change
const createInput = (container, {label, placeholder, id, options, visible = true, onUpdate}) => {
    const wrapper = container.createDiv();
    wrapper.style.display = visible ? "block" : "none";
    
    wrapper.createEl("div", { text: label, attr: { style: STYLES.label } });
    const input = wrapper.createEl("input", { attr: { placeholder, list: id } });
    input.style.cssText = STYLES.input;
    
    const datalist = wrapper.createEl("datalist", { attr: { id } });
    options.forEach(opt => datalist.createEl("option", { value: opt }));
    
    // Filter options on input
    input.addEventListener('input', e => {
        const val = e.target.value.toLowerCase();
        [...datalist.children].forEach(o => o.style.display = o.value.toLowerCase().includes(val) ? '' : 'none');
        if (onUpdate) onUpdate(e.target.value.trim());
    });
    
    // Save on blur (when clicking outside)
    input.addEventListener('blur', () => save(state));
    
    // Save on selecting from datalist
    input.addEventListener('change', () => save(state));
    
    return { wrapper, input };
};

const btn = (container, text, primary = true) => {
    const b = container.createEl("button", { text });
    b.style.cssText = STYLES.button + (primary ? STYLES.primaryButton : STYLES.secondaryButton);
    return b;
};

// =======================
// 🧩 Build UI
// =======================

const container = this.container;
container.empty();
dv.header(2, "🧩 Template metadata/property checker");

const data = getData();
let state = {...defaults};
let results = [];

// Mode selector
container.createEl("div", { text: "Mode:", attr: { style: STYLES.label } });
const modeSelect = container.createEl("select");
["folder", "tag", "property"].forEach(m => modeSelect.createEl("option", { value: m, text: m[0].toUpperCase() + m.slice(1) }));
modeSelect.style.marginBottom = "1em";

// Mode inputs
const inputs = {
    folder: createInput(container, { 
        label: "Folder to check:", 
        placeholder: "Type folder path...", 
        id: "folder-list", 
        options: data.folders,
        onUpdate: v => state.folder = v
    }),
    tag: createInput(container, { 
        label: "Tag to check:", 
        placeholder: "Type tag (without #)", 
        id: "tag-list", 
        options: data.allTags, 
        visible: false,
        onUpdate: v => state.tag = v
    }),
    property: createInput(container, { 
        label: "Property to check:", 
        placeholder: "Type property name...", 
        id: "property-list", 
        options: data.allProperties, 
        visible: false,
        onUpdate: v => state.property = v
    })
};

// Subfolder checkbox
const sfWrap = inputs.folder.wrapper.createDiv();
sfWrap.style.cssText = "margin-bottom: 1em; display: flex; align-items: center; gap: 8px;";
const subfoldersCheck = sfWrap.createEl("input", { attr: { type: "checkbox", checked: true } });
sfWrap.createEl("label", { text: "Include subfolders", attr: { style: "cursor: pointer;" } });

container.createEl("hr");

// Template input
const templateInput = createInput(container, { 
    label: "Template file:", 
    placeholder: "Type template filename...", 
    id: "template-list", 
    options: data.mdFiles.map(stripExt),
    onUpdate: v => state.template = normalizePath(v)
}).input;

const status = container.createDiv({ attr: { style: "margin: 0.5em 0 1em 0;" } });

// Buttons
const searchBtn = btn(container, "🔍 Search");
const updateBtn = btn(container, "🔁 Append missing metadata and tags");
const resetBtn = btn(container, "🧹 Reset selections", false);

container.createEl("hr");
const resultsDiv = container.createDiv();

// =======================
// 🔁 Logic
// =======================

const updateUI = () => Object.entries(inputs).forEach(([m, {wrapper}]) => wrapper.style.display = state.mode === m ? "block" : "none");

// Mode change saves immediately
modeSelect.onchange = async () => { 
    state.mode = modeSelect.value; 
    updateUI(); 
    await save(state);
};

// Checkbox saves immediately
subfoldersCheck.onchange = async e => {
    state.includeSubfolders = e.target.checked;
    await save(state);
};

// Search - no saving, just search
const search = () => {
    const template = dv.page(normalizePath(state.template));
    if (!state.template || !template) return status.setText("❌ Please select a valid template file.");
    if (!state[state.mode]) return status.setText(`❌ Please specify a ${state.mode}.`);
    
    status.setText("🔄 Scanning notes...");
    
    const reqKeys = Object.keys(template).filter(k => !k.startsWith("file") && k !== "tags");
    const reqTags = template.tags || [];
    
    const getPages = {
        folder: () => {
            const f = state.folder;
            return state.includeSubfolders 
                ? dv.pages().where(p => p.file.path.startsWith(f))
                : dv.pages().where(p => {
                    const fp = f.endsWith('/') ? f : f + '/';
                    const rel = p.file.path.startsWith(fp) ? p.file.path.substring(fp.length) : null;
                    return rel && !rel.includes('/');
                });
        },
        tag: () => dv.pages().where(p => (p.tags || []).includes(state.tag)),
        property: () => dv.pages().where(p => state.property in p)
    };
    
    const pages = getPages[state.mode]();
    results = [];
    let complete = 0;
    
    for (const p of pages) {
        const mKeys = reqKeys.filter(k => !(k in p));
        const mTags = reqTags.filter(t => !(p.tags || []).includes(t));
        
        if (mKeys.length || mTags.length) results.push({ note: p.file, mKeys, mTags });
        else complete++;
    }
    
    // Clear and render
    resultsDiv.innerHTML = '';
    resultsDiv.createEl("h3", { text: "📋 Search Results" });
    
    const summary = resultsDiv.createDiv();
    summary.style.cssText = STYLES.summaryBox;
    summary.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 8px;">Summary:</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px;">
            <div>📝 Total: ${pages.length}</div>
            <div style="color: var(--color-green);">✅ Complete: ${complete}</div>
            <div style="color: var(--color-orange);">⚠️ Incomplete: ${results.length}</div>
        </div>`;
    
    if (!results.length) {
        resultsDiv.createEl("p", { text: "All notes have complete metadata and tags!", attr: { style: STYLES.successMessage } });
    } else {
        resultsDiv.createEl("h4", { text: `📋 Incomplete notes (${results.length})`, attr: { style: "margin-top: 1.5em; color: var(--color-orange);" } });
        
        const table = resultsDiv.createEl("table", { attr: { style: STYLES.table } });
        const header = table.createEl("tr");
        ["Note", "Missing keys", "Missing tags"].forEach(h => header.createEl("th", { text: h, attr: { style: STYLES.tableHeader } }));
        
        results.forEach(({note, mKeys, mTags}) => {
            const row = table.createEl("tr");
            
            const cell = row.createEl("td", { attr: { style: STYLES.tableCell } });
            cell.createEl("a", { text: stripExt(note.name), attr: { href: note.path, class: "internal-link" } })
                .onclick = e => { e.preventDefault(); app.workspace.openLinkText(note.path, '', false); };
            
            row.createEl("td", { text: mKeys.length ? mKeys.join(", ") : "—", attr: { style: STYLES.tableCell } });
            row.createEl("td", { text: mTags.length ? mTags.join(", ") : "—", attr: { style: STYLES.tableCell } });
        });
    }
    
    status.setText("✅ Search completed.");
};

// Buttons
searchBtn.onclick = search;  // Just search, no saving

updateBtn.onclick = async () => {
    if (!results.length) return status.setText("❌ No notes to update. Please search first.");
    
    status.setText("🔄 Updating notes...");
    const template = dv.page(normalizePath(state.template));
    let count = 0;
    
    for (const {note, mKeys, mTags} of results) {
        const file = app.vault.getAbstractFileByPath(note.path);
        if (!file) continue;
        
        await app.fileManager.processFrontMatter(file, fm => {
            mKeys.forEach(k => fm[k] = "");
            if (mTags.length) fm.tags = [...new Set([...(fm.tags || []), ...mTags])];
        });
        count++;
    }
    
    status.setText(`✅ Updated ${count} notes.`);
    results = [];
    resultsDiv.innerHTML = '';
};

resetBtn.onclick = async () => {
    await clear();
    state = {...defaults};
    
    Object.values(inputs).forEach(({input}) => input.value = "");
    templateInput.value = "";
    modeSelect.value = "folder";
    subfoldersCheck.checked = true;
    updateUI();
    
    resultsDiv.innerHTML = '';
    results = [];
    status.setText("✅ Selections cleared.");
};

// Init
(async () => {
    state = await load();
    
    modeSelect.value = state.mode;
    Object.entries(inputs).forEach(([m, {input}]) => input.value = state[m]);
    templateInput.value = stripExt(state.template);
    subfoldersCheck.checked = state.includeSubfolders;
    
    updateUI();
})();
```
