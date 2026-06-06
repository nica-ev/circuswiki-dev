function translationStatusLabel(status) {
  return {
    "original": "Original page",
    "machine-translated": "Machine translation",
    "needs-review": "Translation needs review",
    "missing-translation": "Translation missing",
  }[status] || "Translation status";
}

function translationStatusMessage(group, language, entry) {
  var sourceLang = group.source_lang || "";
  var sourceLabel = sourceLang ? sourceLang.toUpperCase() : "source";
  var currentLabel = language ? language.toUpperCase() : "current language";

  if (entry.status === "original") {
    return "This is the original " + currentLabel + " version of this page.";
  }

  if (entry.status === "machine-translated") {
    var message = "This page was machine-translated from " + sourceLabel + ".";
    if (entry.model) {
      message += " Model: " + entry.model + ".";
    }
    return message;
  }

  if (entry.status === "needs-review") {
    return "This translation exists, but its metadata or source alignment still needs review.";
  }

  if (entry.status === "missing-translation" || entry.fallback) {
    return "A dedicated " + currentLabel + " translation does not exist yet. This page is a fallback placeholder.";
  }

  return "Translation metadata is incomplete for this page.";
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
    "  display: grid;",
    "  grid-template-columns: auto 1fr;",
    "  gap: 0.55rem 0.75rem;",
    "  align-items: center;",
    "  margin: 0 0 1.25rem;",
    "  padding: 0.7rem 0.85rem;",
    "  border: 1px solid var(--md-default-fg-color--lightest);",
    "  border-left: 0.22rem solid var(--md-accent-fg-color);",
    "  border-radius: 0.45rem;",
    "  background: var(--md-default-bg-color);",
    "  color: var(--md-default-fg-color);",
    "  font-size: 0.68rem;",
    "  line-height: 1.35;",
    "}",
    ".translation-status__badge {",
    "  display: inline-flex;",
    "  align-items: center;",
    "  width: max-content;",
    "  padding: 0.14rem 0.45rem;",
    "  border-radius: 999px;",
    "  background: var(--md-accent-fg-color--transparent);",
    "  color: var(--md-accent-fg-color);",
    "  font-weight: 700;",
    "  letter-spacing: 0.02em;",
    "  text-transform: uppercase;",
    "}",
    ".translation-status__message {",
    "  margin: 0;",
    "}",
    ".translation-status--original { border-left-color: #2e7d32; }",
    ".translation-status--machine-translated { border-left-color: #f57c00; }",
    ".translation-status--needs-review,",
    ".translation-status--missing-translation { border-left-color: #c62828; }",
    "@media (max-width: 44rem) {",
    "  .translation-status { grid-template-columns: 1fr; }",
    "}",
  ].join("\\n");
  document.head.appendChild(style);
}

function renderTranslationStatus() {
  var content = document.querySelector("article.md-content__inner");
  if (!content) {
    return;
  }

  loadTranslationMap(currentLanguageAssetBase()).then(function(map) {
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

    var message = document.createElement("p");
    message.className = "translation-status__message";
    message.textContent = translationStatusMessage(
      current.group,
      current.language,
      current.entry
    );

    banner.appendChild(badge);
    banner.appendChild(message);
    content.insertBefore(banner, content.firstChild);
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(renderTranslationStatus);
} else {
  document.addEventListener("DOMContentLoaded", renderTranslationStatus);
}
