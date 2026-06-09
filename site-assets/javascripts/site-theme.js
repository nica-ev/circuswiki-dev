(function() {
  var LEFT_NAV_KEY = "circuswiki:left-nav-collapsed";
  var RIGHT_NAV_KEY = "circuswiki:right-nav-collapsed";

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

  function storedPanelState(key) {
    try {
      return window.localStorage.getItem(key) === "true";
    } catch (error) {
      return false;
    }
  }

  function storePanelState(key, collapsed) {
    try {
      window.localStorage.setItem(key, collapsed ? "true" : "false");
    } catch (error) {
      // The layout still works for this page if storage is unavailable.
    }
  }

  function panelConfig(side) {
    if (side === "right") {
      return {
        key: RIGHT_NAV_KEY,
        bodyClass: "cw-nav-right-collapsed",
        selector: '.md-sidebar--secondary[data-md-type="toc"]',
        collapseLabel: "Hide table of contents",
        expandLabel: "Show table of contents",
        collapseIcon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-panel-right-close" viewBox="0 0 24 24" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18M8 9l3 3-3 3"/></svg>',
        expandIcon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-panel-right-open" viewBox="0 0 24 24" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18M10 15l-3-3 3-3"/></svg>',
      };
    }

    return {
      key: LEFT_NAV_KEY,
      bodyClass: "cw-nav-left-collapsed",
      selector: '.md-sidebar--primary[data-md-type="navigation"]',
      collapseLabel: "Hide navigation",
      expandLabel: "Show navigation",
      collapseIcon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-panel-left-close" viewBox="0 0 24 24" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18M16 15l-3-3 3-3"/></svg>',
      expandIcon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-panel-left-open" viewBox="0 0 24 24" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18M14 9l3 3-3 3"/></svg>',
    };
  }

  function setPanelCollapsed(side, collapsed) {
    var config = panelConfig(side);
    document.body.classList.toggle(config.bodyClass, collapsed);

    document.querySelectorAll('.cw-panel-toggle[data-cw-panel="' + side + '"]').forEach(function (button) {
      button.setAttribute("aria-expanded", collapsed ? "false" : "true");
      button.setAttribute("title", collapsed ? config.expandLabel : config.collapseLabel);
      button.setAttribute("aria-label", collapsed ? config.expandLabel : config.collapseLabel);
      button.innerHTML = collapsed ? config.expandIcon : config.collapseIcon;
    });
  }

  function togglePanel(side) {
    var config = panelConfig(side);
    var collapsed = !document.body.classList.contains(config.bodyClass);
    storePanelState(config.key, collapsed);
    setPanelCollapsed(side, collapsed);
  }

  function makePanelButton(side, type) {
    var config = panelConfig(side);
    var button = document.createElement("button");
    button.className = "cw-panel-toggle cw-panel-toggle--" + side + " cw-panel-toggle--" + type;
    button.type = "button";
    button.setAttribute("data-cw-panel", side);
    button.addEventListener("click", function () {
      togglePanel(side);
    });
    return button;
  }

  function ensurePanelToggle(side) {
    var config = panelConfig(side);
    var sidebar = document.querySelector(config.selector);
    var inner = sidebar ? sidebar.querySelector(".md-sidebar__inner") : null;

    if (!inner) {
      return;
    }

    if (!inner.querySelector('.cw-panel-toggle--panel[data-cw-panel="' + side + '"]')) {
      inner.insertBefore(makePanelButton(side, "panel"), inner.firstChild);
    }
  }

  function ensureEdgeToggle(side) {
    if (document.querySelector('.cw-panel-toggle--edge[data-cw-panel="' + side + '"]')) {
      return;
    }

    document.body.appendChild(makePanelButton(side, "edge"));
  }

  function ensurePanelToggles() {
    ["left", "right"].forEach(function (side) {
      var config = panelConfig(side);
      ensurePanelToggle(side);
      ensureEdgeToggle(side);
      setPanelCollapsed(side, storedPanelState(config.key));
    });
  }

  setPanelCollapsed("left", storedPanelState(LEFT_NAV_KEY));
  setPanelCollapsed("right", storedPanelState(RIGHT_NAV_KEY));

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      markHeroPage();
      ensurePanelToggles();
    });
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      markHeroPage();
      ensurePanelToggles();
    });
  }
})();
