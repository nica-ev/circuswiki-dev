---
created: 2025-05-26 23:03:50
update: 2025-05-27 23:50:55
publish: false
tags: 
title: 
description: 
authors: 
selected-folder: /
selected-template: _templates/Frontmatter Scheme - Games.md
filter-key: tags
filter-value: spiele
recursive-scan: true
---

# title
This is a DataviewJS Tool that helps compare the frontmatter of md.files with a template file and can append missing metadata if needed.

```dataviewjs
// =======================
// 🛠 Helper Functions
// =======================

function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

async function getStoredSelections() {
    const file = app.vault.getAbstractFileByPath(dv.current().file.path);
    let folder = "";
    let template = "";
    let filterKey = "";
    let filterValue = "";
    let recursiveScan = false;

    await app.fileManager.processFrontMatter(file, (fm) => {
        folder = fm["selected-folder"] || "";
        template = fm["selected-template"] || "";
        filterKey = fm["filter-key"] || "";
        filterValue = fm["filter-value"] || "";
        recursiveScan = fm["recursive-scan"] || false;
    });

    return { folder, template, filterKey, filterValue, recursiveScan };
}

// Modified storeSelections to be called only on button click
async function storeSelections(folder, template, filterKey, filterValue, recursiveScan) {
    const file = app.vault.getAbstractFileByPath(dv.current().file.path);
    await app.fileManager.processFrontMatter(file, (fm) => {
        fm["selected-folder"] = folder;
        fm["selected-template"] = template;
        fm["filter-key"] = filterKey;
        fm["filter-value"] = filterValue;
        fm["recursive-scan"] = recursiveScan;
    });
}

async function clearSelections() {
    const file = app.vault.getAbstractFileByPath(dv.current().file.path);

    await app.fileManager.processFrontMatter(file, (fm) => {
        delete fm["selected-folder"];
        delete fm["selected-template"];
        delete fm["filter-key"];
        delete fm["filter-value"];
        delete fm["recursive-scan"];
    });
}

// =======================
// 🧩 Build UI Elements
// =======================

const container = this.container;
container.empty();

dv.header(2, "🧩 Template metadata/property checker");

// Folder Selection
container.createEl("div", { text: "Folder to check:" });
const folderInputWrapper = container.createDiv();
folderInputWrapper.style.position = "relative";
folderInputWrapper.style.marginBottom = "1em";
const folderInput = folderInputWrapper.createEl("input", { attr: { placeholder: "Type folder path..." } });
folderInput.style.cssText = "width: 100%; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--interactive-accent); box-sizing: border-box;";
const folderDropdown = folderInputWrapper.createDiv();
folderDropdown.style.cssText = "position: absolute; top: 100%; left: 0; right: 0; border: 1px solid var(--interactive-accent); border-top: none; background-color: var(--background-primary); max-height: 150px; overflow-y: auto; z-index: 10; display: none;";

// Recursive Scan Toggle
const recursiveScanWrapper = container.createDiv();
recursiveScanWrapper.style.marginBottom = "1em";
const recursiveScanToggle = recursiveScanWrapper.createEl("input", { type: "checkbox" });
const recursiveScanLabel = recursiveScanWrapper.createEl("label", { text: "Scan subdirectories recursively" });
recursiveScanLabel.style.marginLeft = "0.5em";

// Template Selection
container.createEl("div", { text: "Template file:" });
const templateInputWrapper = container.createDiv();
templateInputWrapper.style.position = "relative";
templateInputWrapper.style.marginBottom = "1em";
const templateInput = templateInputWrapper.createEl("input", { attr: { placeholder: "Type template filename..." } });
templateInput.style.cssText = "width: 100%; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--interactive-accent); box-sizing: border-box;";
const templateDropdown = templateInputWrapper.createDiv();
templateDropdown.style.cssText = "position: absolute; top: 100%; left: 0; right: 0; border: 1px solid var(--interactive-accent); border-top: none; background-color: var(--background-primary); max-height: 150px; overflow-y: auto; z-index: 10; display: none;";

// YAML Property Filter
container.createEl("div", { text: "Filter by YAML property (optional):" });
const filterInputWrapper = container.createDiv();
filterInputWrapper.style.display = "flex";
filterInputWrapper.style.gap = "1em";
filterInputWrapper.style.marginBottom = "1em";

const filterKeyInput = filterInputWrapper.createEl("input", { attr: { placeholder: "Property key..." } });
filterKeyInput.style.cssText = "flex-grow: 1; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--interactive-accent); box-sizing: border-box;";

const filterValueInput = filterInputWrapper.createEl("input", { attr: { placeholder: "Property value..." } });
filterValueInput.style.cssText = "flex-grow: 1; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--interactive-accent); box-sizing: border-box;";


const statusDiv = container.createDiv();
statusDiv.style.margin = "0.5em 0 1em 0";

// New "Update Selection" button
const updateButton = container.createEl("button", { text: "🔄 Update Selection" });
updateButton.style.cssText = "padding: 8px 12px; border: 1px solid var(--interactive-accent); border-radius: 6px; background-color: var(--interactive-accent); color: var(--text-on-accent); cursor: pointer; margin-top: 1em;";

const fixButton = container.createEl("button", { text: "🔁 Append missing metadata and tags" });
fixButton.style.cssText = "padding: 8px 12px; border: 1px solid var(--interactive-accent); border-radius: 6px; background-color: var(--interactive-accent); color: var(--text-on-accent); cursor: pointer; margin-top: 1em; margin-left: 1em;";


const resetButton = container.createEl("button", { text: "🧹 Reset selections" });
resetButton.style.cssText = "padding: 8px 12px; border: 1px solid var(--interactive-accent); border-radius: 6px; background-color: var(--background-secondary); color: var(--text-normal); cursor: pointer; margin-top: 1em; margin-left: 1em;";

container.appendChild(updateButton);
container.appendChild(fixButton);
container.appendChild(resetButton);
container.appendChild(statusDiv);

// State variables used by the Dataview query (only updated on button click)
let selectedFolder = "";
let selectedTemplate = "";
let filterKey = "";
let filterValue = "";
let recursiveScan = false;

let resultRows = [];

// Removed the shouldRenderOnLoad flag

// =======================
// 🌳 Data sources
// =======================

const folders = app.vault.getAllLoadedFiles()
    .filter(f => f instanceof obsidian.TFolder)
    .map(f => f.path)
    .sort();

const mdFiles = app.vault.getMarkdownFiles().map(f => f.path).sort();

// =======================
// 🔎 Folder Input Logic
// =======================

function updateFolderDropdown(filter) {
    folderDropdown.empty();
    if (!filter) {
        folderDropdown.style.display = "none";
        return;
    }

    const matches = folders.filter(f => f.toLowerCase().includes(filter.toLowerCase()));
    if (matches.length === 0) {
        folderDropdown.style.display = "none";
        return;
    }

    for (const match of matches) {
        const optionDiv = folderDropdown.createDiv({ text: match });
        optionDiv.style.padding = "6px 8px";
        optionDiv.style.cursor = "pointer";
        optionDiv.style.borderBottom = "1px solid var(--interactive-accent)";
        optionDiv.onmouseover = () => optionDiv.style.backgroundColor = "var(--interactive-accent)";
        optionDiv.onmouseout = () => optionDiv.style.backgroundColor = "transparent";

        optionDiv.onclick = async () => {
            folderInput.value = match;
            folderDropdown.style.display = "none";
        };
    }

    folderDropdown.style.display = "block";
}

// =======================
// 🔎 Template Input Logic
// =======================

function updateTemplateDropdown(filter) {
    templateDropdown.empty();
    if (!filter) {
        templateDropdown.style.display = "none";
        return;
    }

    const matches = mdFiles.filter(f => f.toLowerCase().includes(filter.toLowerCase()));
    if (matches.length === 0) {
        templateDropdown.style.display = "none";
        return;
    }

    for (const match of matches) {
        const optionDiv = templateDropdown.createDiv({ text: match });
        optionDiv.style.padding = "6px 8px";
        optionDiv.style.cursor = "pointer";
        optionDiv.style.borderBottom = "1px solid var(--interactive-accent)";
        optionDiv.onmouseover = () => optionDiv.style.backgroundColor = "var(--interactive-accent)";
        optionDiv.onmouseout = () => optionDiv.style.backgroundColor = "transparent";

        optionDiv.onclick = async () => {
            templateInput.value = match;
            templateDropdown.style.display = "none";
        };
    }

    templateDropdown.style.display = "block";
}

// =======================
// 🔁 Event Bindings
// =======================

document.addEventListener("click", (e) => {
    if (!folderInputWrapper.contains(e.target)) folderDropdown.style.display = "none";
    if (!templateInputWrapper.contains(e.target)) templateDropdown.style.display = "none";
});

// Debounced input handlers to update dropdowns, NO frontmatter storage
folderInput.addEventListener("input", debounce(async (e) => {
    updateFolderDropdown(e.target.value);
}, 200));

templateInput.addEventListener("input", debounce(async (e) => {
    updateTemplateDropdown(e.target.value);
}, 200));

// Filter and toggle handlers also do NOT store to frontmatter
filterKeyInput.addEventListener("input", debounce(async (e) => {
    // No action needed here other than allowing input
}, 300));

filterValueInput.addEventListener("input", debounce(async (e) => {
    // No action needed here other than allowing input
}, 300));

recursiveScanToggle.addEventListener("change", async (e) => {
    // No action needed here other than allowing toggle
});

// Event listener for the "Update Selection" button
updateButton.onclick = async () => {
    // Update the state variables used by the Dataview query from input values
    selectedFolder = folderInput.value.trim();
    selectedTemplate = templateInput.value.trim();
    filterKey = filterKeyInput.value.trim();
    filterValue = filterValueInput.value.trim();
    recursiveScan = recursiveScanToggle.checked;

    // Store the now-finalized selections to frontmatter
    // This frontmatter change will trigger Dataview's re-render
    await storeSelections(selectedFolder, selectedTemplate, filterKey, filterValue, recursiveScan);

    // Removed the explicit call to scanAndRender() here!
    // Dataview's reactivity will handle the re-render after frontmatter update.

    // Optionally, provide immediate feedback to the user
    statusDiv.setText("Selections updated. Re-rendering...");
};


resetButton.onclick = async () => {
    await clearSelections();
    // Reset state variables
    selectedFolder = "";
    selectedTemplate = "";
    filterKey = "";
    filterValue = "";
    recursiveScan = false;

    folderInput.value = "";
    templateInput.value = "";
    filterKeyInput.value = "";
    filterValueInput.value = "";
    recursiveScanToggle.checked = false;

    // No need to reset shouldRenderOnLoad flag

    dv.paragraph("Selections cleared. Please choose folder and template again.");
    scanAndRender(); // Re-render to show empty state (will be empty due to cleared state)
};

// =======================
// 🔎 Scan and Render Logic
// =======================

async function scanAndRender() {
    // Removed the conditional check based on shouldRenderOnLoad

    statusDiv.setText("Scanning notes...");

    // Clear previous results by clearing the container element
    // This ensures that the new output replaces the old one.
    container.findAll(".dataview.table-view").forEach(el => el.remove());
    container.findAll("p").forEach(el => {
        // Only remove paragraphs that are part of the Dataview output,
        // not the initial instruction paragraph.
        if (!el.textContent.startsWith("Start typing folder and template names above") &&
            !el.textContent.startsWith("Selections loaded. Click 'Update Selection'")) { // Also exclude the loaded message
             el.remove();
        }
    });
    container.findAll("h3").forEach(el => el.remove());


    if (!selectedFolder) {
        statusDiv.setText("Please select a folder from the suggestions.");
        dv.paragraph("No data to show.");
        return;
    }
    if (!selectedTemplate) {
        statusDiv.setText("Please select a template from the suggestions.");
        dv.paragraph("No data to show.");
        return;
    }

    const template = dv.page(selectedTemplate);
    if (!template) {
        statusDiv.setText(`Template not found: ${selectedTemplate}`);
        return;
    }

    const requiredKeys = Object.keys(template).filter(k => !k.startsWith("file") && k !== "tags");
    const requiredTags = Array.isArray(template.tags) ? template.tags : [];

    let pages;
    if (recursiveScan) {
        // Exclude the current file from the recursive scan
        pages = dv.pages(`"${selectedFolder}"`).where(p => p.file.path !== dv.current().file.path);
    } else {
        // Exclude the current file from the non-recursive scan
        pages = dv.pages().where(p => p.file.folder === selectedFolder && p.file.path !== dv.current().file.path);
    }

    // Apply YAML property filter if key and value are provided
    if (filterKey) {
        if (filterValue) {
            // Filter for pages where the property exists
            pages = pages.where(p => p[filterKey] !== undefined);

            // Now, refine the filter based on the property type and value
            pages = pages.where(p => {
                const propertyValue = p[filterKey];
                if (Array.isArray(propertyValue)) {
                    // If the property is a list, check if it includes the filterValue
                    // Case-insensitive comparison for list items
                    return propertyValue.some(item =>
                        typeof item === 'string' && item.toLowerCase() === filterValue.toLowerCase()
                    );
                } else if (typeof propertyValue === 'string') {
                    // If it's a string, perform case-insensitive comparison
                    return propertyValue.toLowerCase() === filterValue.toLowerCase();
                }
                 else {
                    // For other types (numbers, booleans), check for direct equality
                    return propertyValue === filterValue;
                }
            });
        } else {
             // If only key is provided, filter for notes that have the key
             pages = pages.where(p => p[filterKey] !== undefined);
        }
    }

    resultRows = [];

    for (const page of pages) {
        const missingKeys = requiredKeys.filter(k => page[k] === undefined);
        const currentTags = Array.isArray(page.tags) ? page.tags : [];
        const missingTags = requiredTags.filter(t => !currentTags.includes(t));

        if (missingKeys.length > 0 || missingTags.length > 0) {
            resultRows.push({
                note: page.file.link,
                path: page.file.path,
                missingKeys,
                missingTags
            });
        }
    }

    dv.header(3, "📋 Notes missing metadata or tags");
    if (resultRows.length === 0) {
        dv.paragraph("✅ All notes have complete metadata and tags.");
    } else {
        dv.table(
            ["Note", "Missing keys", "Missing tags"],
            resultRows.map(r => [
                r.note,
                r.missingKeys.length ? r.missingKeys.join(", ") : "—",
                r.missingTags.length ? r.missingTags.join(", ") : "—"
            ])
        );
        dv.paragraph(`🔍 Number of notes with missing metadata or tags: **${resultRows.length}**`);
    }

    statusDiv.setText("");
}

// =======================
// 🔘 Button click to fix metadata/tags
// =======================

fixButton.onclick = async () => {
    if (resultRows.length === 0) {
        statusDiv.setText("No notes to update.");
        return;
    }

    statusDiv.setText("🔄 Updating metadata and tags...");

    const template = dv.page(selectedTemplate);
    if (!template) {
        statusDiv.setText(`Template not found: ${selectedTemplate}`);
        return;
    }

    let updatedCount = 0;

    for (const { path, missingKeys, missingTags } of resultRows) {
        const file = app.vault.getAbstractFileByPath(path);
        if (!file || !file.path) continue;

        await app.fileManager.processFrontMatter(file, (frontmatter) => {
            for (const key of missingKeys) {
                if (frontmatter[key] === undefined) {
                     frontmatter[key] = template[key] !== undefined ? template[key] : "";
                }
            }

            if (!Array.isArray(frontmatter.tags)) {
                frontmatter.tags = [...(Array.isArray(template.tags) ? template.tags : [])];
            } else {
                for (const tag of missingTags) {
                    if (!frontmatter.tags.includes(tag)) {
                        frontmatter.tags.push(tag);
                    }
                }
            }
        });

        updatedCount++;
    }

    statusDiv.setText(`✅ Done! Updated **${updatedCount}** notes. Refreshing results...`);
    await scanAndRender(); // Explicitly re-render after fixing
};

// =======================
// 🏁 Load Saved Values on Start
// =======================

(async () => {
    const stored = await getStoredSelections();
    // Load stored values directly into input fields and toggle
    folderInput.value = stored.folder;
    templateInput.value = stored.template;
    filterKeyInput.value = stored.filterKey;
    filterValueInput.value = stored.filterValue;
    recursiveScanToggle.checked = stored.recursiveScan;

    // If stored selections exist, update the state variables and perform initial scan
    if (folderInput.value.trim() && templateInput.value.trim()) {
        // Update the state variables used by the Dataview query from input values
        selectedFolder = folderInput.value.trim();
        selectedTemplate = templateInput.value.trim();
        filterKey = filterKeyInput.value.trim();
        filterValue = filterValueInput.value.trim();
        recursiveScan = recursiveScanToggle.checked;

        // Explicitly call scanAndRender() on initial load if selections exist
        await scanAndRender();
    } else {
        // If no selections are loaded, the initial message is shown
        dv.paragraph("Start typing folder and template names above, then click 'Update Selection' to scan notes.");
    }
})();
```

# hello

