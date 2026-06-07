(function() {
  function pageHasTag(tag) {
    var tags = document.querySelectorAll(".md-tags .md-tag");
    for (var i = 0; i < tags.length; i += 1) {
      if ((tags[i].textContent || "").trim().toLowerCase() === tag) {
        return true;
      }
    }
    return false;
  }

  function markHeroPage() {
    document.body.classList.toggle("circuswiki-hero", pageHasTag("moc"));
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(markHeroPage);
  } else {
    document.addEventListener("DOMContentLoaded", markHeroPage);
  }
})();
