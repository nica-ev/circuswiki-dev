var translationMapPromise = null;
var LANGUAGE_CODES = ["de", "en", "pl", "hu", "it", "nl"];

function currentScriptPath(scriptName) {
  var scripts = document.getElementsByTagName("script");
  for (var i = 0; i < scripts.length; i += 1) {
    var src = scripts[i].src || "";
    if (src.indexOf("/javascripts/" + scriptName) !== -1) {
      return new URL(src, window.location.href).pathname;
    }
  }
  return window.location.pathname;
}

function siteRootPath() {
  var scriptPath = currentScriptPath("language-switcher.js");
  var root = scriptPath.replace(/javascripts\/language-switcher\.js$/, "");
  root = root.replace(new RegExp("(?:" + LANGUAGE_CODES.join("|") + ")\\/$"), "");
  if (!root.startsWith("/")) {
    root = "/" + root;
  }
  return root.endsWith("/") ? root : root + "/";
}

function currentLanguageRootPath() {
  var scriptPath = currentScriptPath("language-switcher.js");
  return scriptPath.replace(/javascripts\/language-switcher\.js$/, "");
}

function normalizedPath(value) {
  return value.replace(/\/+$/, "") || "/";
}

function loadTranslationMap(base) {
  if (!translationMapPromise) {
    translationMapPromise = fetch(base + "javascripts/translation-map.json")
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Missing translation map");
        }
        return response.json();
      })
      .catch(function() {
        return null;
      });
  }
  return translationMapPromise;
}

function findCurrentGroup(map, path) {
  if (!map || !map.groups) {
    return null;
  }

  var normalizedCurrent = normalizedPath(path);
  var groups = Object.keys(map.groups).map(function(key) {
    return map.groups[key];
  });

  for (var i = 0; i < groups.length; i += 1) {
    var languages = groups[i].languages || {};
    var languageKeys = Object.keys(languages);
    for (var j = 0; j < languageKeys.length; j += 1) {
      var entry = languages[languageKeys[j]];
      if (entry && normalizedPath(entry.url) === normalizedCurrent) {
        return groups[i];
      }
    }
  }

  return null;
}

function rewriteLanguageLinks() {
  var base = siteRootPath();
  var path = window.location.pathname;
  var context = "";

  for (var i = 0; i < LANGUAGE_CODES.length; i += 1) {
    var language = LANGUAGE_CODES[i];
    if (language === "de") {
      continue;
    }
    var languageRoot = base + language + "/";
    if (path.indexOf(languageRoot) === 0) {
      context = path.slice(languageRoot.length);
      break;
    }
  }

  if (!context && path.indexOf(base) === 0) {
    context = path.slice(base.length);
  }

  if (!context && path.indexOf(base) !== 0) {
    context = path.replace(/^\/+/, "");
  }

  if (LANGUAGE_CODES.some(function(language) {
    return context === language || context === language + "/";
  })) {
    context = "";
  }

  LANGUAGE_CODES.forEach(function(language) {
    var languageRoot = language === "de" ? base : base + language + "/";
    document.querySelectorAll('a[hreflang="' + language + '"]').forEach(function(link) {
      link.href = languageRoot + context;
    });
  });

  loadTranslationMap(currentLanguageRootPath()).then(function(map) {
    var group = findCurrentGroup(map, path);
    if (!group || !group.languages) {
      return;
    }

    document.querySelectorAll("a[hreflang]").forEach(function(link) {
      var language = link.getAttribute("hreflang");
      var entry = group.languages[language];
      if (entry && entry.url) {
        link.href = entry.url;
        if (entry.fallback) {
          link.title = "Translation missing. Opens a fallback page.";
        }
      }
    });
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(rewriteLanguageLinks);
} else {
  document.addEventListener("DOMContentLoaded", rewriteLanguageLinks);
}
