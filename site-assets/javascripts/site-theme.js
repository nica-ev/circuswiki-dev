(function() {
  var LEFT_NAV_KEY = "circuswiki:left-nav-collapsed";
  var RIGHT_NAV_KEY = "circuswiki:right-nav-collapsed";
  var THEME_KEY = "circuswiki:theme";
  var THEME_VALUES = ["auto", "light", "dark", "contrast"];

  function storedTheme() {
    try {
      var value = window.localStorage.getItem(THEME_KEY) || "auto";
      return THEME_VALUES.indexOf(value) === -1 ? "auto" : value;
    } catch (error) {
      return "auto";
    }
  }

  function storeTheme(value) {
    try {
      window.localStorage.setItem(THEME_KEY, value);
    } catch (error) {
      // The theme still applies for this page if storage is unavailable.
    }
  }

  function resolvedTheme(value) {
    if (value === "auto") {
      return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    return value;
  }

  function applyTheme(value) {
    var selected = THEME_VALUES.indexOf(value) === -1 ? "auto" : value;
    document.documentElement.setAttribute("data-cw-theme-choice", selected);
    document.documentElement.setAttribute("data-cw-theme", resolvedTheme(selected));

    document.querySelectorAll(".cw-theme-menu__item").forEach(function (item) {
      var active = item.getAttribute("data-cw-theme-value") === selected;
      item.classList.toggle("cw-theme-menu__item--active", active);
      item.setAttribute("aria-checked", active ? "true" : "false");
    });
  }

  function closeThemeMenus() {
    document.querySelectorAll(".cw-theme-control").forEach(function (control) {
      control.classList.remove("cw-theme-control--open");
      var button = control.querySelector(".cw-theme-button");
      if (button) {
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function ensureThemeMenu() {
    var header = document.querySelector(".md-header__inner");
    if (!header || header.querySelector(".cw-theme-control")) {
      applyTheme(storedTheme());
      return;
    }

    var control = document.createElement("div");
    control.className = "cw-theme-control";
    control.innerHTML = [
      '<button class="md-header__button md-icon cw-theme-button" type="button" aria-label="Theme wechseln" aria-haspopup="true" aria-expanded="false">',
      '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-palette" viewBox="0 0 24 24" aria-hidden="true"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 22C6.477 22 2 17.97 2 13 2 7.477 6.477 3 12 3s10 4.03 10 9c0 2.21-1.79 4-4 4h-1.5a2.5 2.5 0 0 0-2.5 2.5c0 1.933-1.067 3.5-2 3.5Z"/></svg>',
      "</button>",
      '<div class="cw-theme-menu" role="menu" aria-label="Theme">',
      '<button class="cw-theme-menu__item" type="button" role="menuitemradio" data-cw-theme-value="auto">Auto</button>',
      '<button class="cw-theme-menu__item" type="button" role="menuitemradio" data-cw-theme-value="light">Light</button>',
      '<button class="cw-theme-menu__item" type="button" role="menuitemradio" data-cw-theme-value="dark">Dark</button>',
      '<button class="cw-theme-menu__item" type="button" role="menuitemradio" data-cw-theme-value="contrast">Contrast</button>',
      "</div>",
    ].join("");

    var button = control.querySelector(".cw-theme-button");
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = !control.classList.contains("cw-theme-control--open");
      closeThemeMenus();
      control.classList.toggle("cw-theme-control--open", open);
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });

    control.querySelectorAll(".cw-theme-menu__item").forEach(function (item) {
      item.addEventListener("click", function () {
        var value = item.getAttribute("data-cw-theme-value");
        storeTheme(value);
        applyTheme(value);
        closeThemeMenus();
      });
    });

    var languageOption = header.querySelector(".md-header__option");
    var searchToggle = header.querySelector('label[for="__search"]');
    if (languageOption) {
      header.insertBefore(control, languageOption);
    } else if (searchToggle) {
      header.insertBefore(control, searchToggle);
    } else {
      header.appendChild(control);
    }

    applyTheme(storedTheme());
  }

  function ensureSearchButton() {
    document.querySelectorAll(".md-search > .md-search__button").forEach(function (button) {
      if (button.classList.contains("cw-search-button")) {
        return;
      }

      var label = (button.textContent || "").trim() || "Search";
      button.classList.add("cw-search-button", "md-header__button", "md-icon");
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide lucide-search" viewBox="0 0 24 24" aria-hidden="true"><path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/></svg>';
    });
  }

  document.addEventListener("click", function (event) {
    if (!event.target.closest(".cw-theme-control")) {
      closeThemeMenus();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeThemeMenus();
    }
  });

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
  applyTheme(storedTheme());

  if (window.matchMedia) {
    var darkPreference = window.matchMedia("(prefers-color-scheme: dark)");
    var handlePreferenceChange = function () {
      if (storedTheme() === "auto") {
        applyTheme("auto");
      }
    };

    if (darkPreference.addEventListener) {
      darkPreference.addEventListener("change", handlePreferenceChange);
    } else if (darkPreference.addListener) {
      darkPreference.addListener(handlePreferenceChange);
    }
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      ensureThemeMenu();
      ensureSearchButton();
      markHeroPage();
      ensurePanelToggles();
    });
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      ensureThemeMenu();
      ensureSearchButton();
      markHeroPage();
      ensurePanelToggles();
    });
  }
})();
