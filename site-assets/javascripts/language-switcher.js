function rewriteLanguageLinks() {
  var base = "/circuswiki/";
  var englishRoot = base + "en/";
  var path = window.location.pathname;
  var context = "";

  if (path.indexOf(englishRoot) === 0) {
    context = path.slice(englishRoot.length);
  } else if (path.indexOf(base) === 0) {
    context = path.slice(base.length);
  } else {
    context = path.replace(/^\/+/, "");
  }

  if (context === "en" || context === "en/") {
    context = "";
  }

  document.querySelectorAll('a[hreflang="de"]').forEach(function(link) {
    link.href = base + context;
  });

  document.querySelectorAll('a[hreflang="en"]').forEach(function(link) {
    link.href = englishRoot + context;
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(rewriteLanguageLinks);
} else {
  document.addEventListener("DOMContentLoaded", rewriteLanguageLinks);
}
