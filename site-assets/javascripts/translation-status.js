function translationStatusLabel(status) {
  return {
    "original": "original",
    "machine-translated": "machine translated",
    "needs-review": "needs review",
    "missing-translation": "translation missing",
  }[status] || "Translation status";
}

function translationStatusDetails(group, language, entry) {
  var sourceLang = entry.source_lang || group.source_lang || "";
  var sourceEntry = group.languages && sourceLang ? group.languages[sourceLang] : null;
  var sourcePath = entry.source || (sourceEntry && sourceEntry.path) || "";
  var authors = entry.authors && entry.authors.length ? entry.authors.join(", ") : "";
  var lines = [
    "Status: " + translationStatusLabel(entry.status),
    "Language: " + (language || entry.source_lang || "unknown"),
  ];

  if (entry.path) {
    lines.push("File: " + entry.path);
  }

  if (authors) {
    lines.push("Author: " + authors);
  }

  if (sourceLang) {
    lines.push("Source language: " + sourceLang);
  }

  if (sourcePath) {
    lines.push("Source file: " + sourcePath);
  }

  if (entry.model) {
    lines.push("Model: " + entry.model);
  }

  if (entry.updated) {
    lines.push("Updated: " + entry.updated);
  }

  if (entry.fallback) {
    lines.push("This is a fallback page; a dedicated translation is missing.");
  }

  return lines.join("\n");
}

function findCurrentTranslationEntry(map, path) {
  if (!map || !map.groups) {
    return null;
  }

  var normalizedCurrent = normalizedPath(path);
  var groupKeys = Object.keys(map.groups);

  for (var i = 0; i < groupKeys.length; i += 1) {
    var group = map.groups[groupKeys[i]];
    var languages = group.languages || {};
    var languageKeys = Object.keys(languages);

    for (var j = 0; j < languageKeys.length; j += 1) {
      var language = languageKeys[j];
      var entry = languages[language];
      if (entry && normalizedPath(entry.url) === normalizedCurrent) {
        return { group: group, language: language, entry: entry };
      }
    }
  }

  return null;
}

function injectTranslationStatusStyles() {
  if (document.getElementById("translation-status-styles")) {
    return;
  }

  var style = document.createElement("style");
  style.id = "translation-status-styles";
  style.textContent = [
    ".translation-status {",
    "  display: flex;",
    "  align-items: center;",
    "  margin: 0 0 0.45rem;",
    "  padding: 0;",
    "  font-size: 0.58rem;",
    "  line-height: 1;",
    "}",
    ".translation-status__badge {",
    "  display: inline-flex;",
    "  align-items: center;",
    "  width: max-content;",
    "  padding: 0.18rem 0.55rem;",
    "  border: 1px solid rgba(47, 111, 94, 0.42);",
    "  border-radius: 999px;",
    "  background: rgba(47, 111, 94, 0.1);",
    "  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.48), 0 0.08rem 0.28rem rgba(30, 38, 33, 0.08);",
    "  color: var(--cw-green, #2f6f5e);",
    "  font-weight: 700;",
    "  letter-spacing: 0.06em;",
    "  text-transform: uppercase;",
    "  cursor: help;",
    "}",
    ".translation-status--original .translation-status__badge {",
    "  border-color: rgba(47, 111, 94, 0.34);",
    "  color: var(--cw-green, #2f6f5e);",
    "}",
    ".translation-status--machine-translated .translation-status__badge {",
    "  border-color: rgba(217, 155, 54, 0.62);",
    "  background: rgba(217, 155, 54, 0.16);",
    "  color: #8a5d12;",
    "}",
    ".translation-status--needs-review .translation-status__badge,",
    ".translation-status--missing-translation .translation-status__badge {",
    "  border-color: rgba(185, 70, 50, 0.58);",
    "  background: rgba(185, 70, 50, 0.12);",
    "  color: var(--cw-red, #b94632);",
    "}",
  ].join("\n");
  document.head.appendChild(style);
}

function renderTranslationStatus() {
  var content = document.querySelector("article.md-content__inner");
  if (!content) {
    return;
  }

  loadTranslationMap(currentLanguageRootPath()).then(function(map) {
    var current = findCurrentTranslationEntry(map, window.location.pathname);
    if (!current) {
      return;
    }

    injectTranslationStatusStyles();

    var existing = content.querySelector(":scope > .translation-status");
    if (existing) {
      existing.remove();
    }

    var banner = document.createElement("aside");
    var status = current.entry.status || "unknown";
    banner.className = "translation-status translation-status--" + status;
    banner.setAttribute("aria-label", "Translation status");

    var badge = document.createElement("span");
    badge.className = "translation-status__badge";
    badge.textContent = translationStatusLabel(status);
    badge.title = translationStatusDetails(current.group, current.language, current.entry);
    badge.setAttribute("aria-label", badge.title);

    banner.appendChild(badge);
    content.insertBefore(banner, content.firstChild);
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(renderTranslationStatus);
} else {
  document.addEventListener("DOMContentLoaded", renderTranslationStatus);
}
