(function () {
  var SORT_NONE = "none";
  var SORT_ASC = "ascending";
  var SORT_DESC = "descending";
  var SORT_LABEL = "Sort table by this column";

  function toArray(collection) {
    return Array.prototype.slice.call(collection || []);
  }

  function normalizeText(value) {
    return (value || "").replace(/\s+/g, " ").trim();
  }

  function parseComparableNumber(value) {
    var text = normalizeText(value).replace(/\u00a0/g, " ").replace(",", ".");

    if (!text || /^[-–—]$/.test(text)) {
      return null;
    }

    var match = text.match(/-?\d+(?:\.\d+)?/);
    if (!match) {
      return null;
    }

    return Number(match[0]);
  }

  function originalIndex(row) {
    return Number(row.getAttribute("data-cw-original-row") || 0);
  }

  function cellText(row, columnIndex) {
    var cell = row.cells[columnIndex];
    return normalizeText(cell ? cell.textContent : "");
  }

  function compareCellText(left, right) {
    var leftEmpty = left === "" || /^[-–—]$/.test(left);
    var rightEmpty = right === "" || /^[-–—]$/.test(right);

    if (leftEmpty && rightEmpty) {
      return 0;
    }

    if (leftEmpty) {
      return 1;
    }

    if (rightEmpty) {
      return -1;
    }

    var leftNumber = parseComparableNumber(left);
    var rightNumber = parseComparableNumber(right);

    if (leftNumber !== null && rightNumber !== null && leftNumber !== rightNumber) {
      return leftNumber - rightNumber;
    }

    return left.localeCompare(right, undefined, {
      numeric: true,
      sensitivity: "base",
    });
  }

  function nextSortState(current) {
    if (current === SORT_ASC) {
      return SORT_DESC;
    }

    if (current === SORT_DESC) {
      return SORT_NONE;
    }

    return SORT_ASC;
  }

  function headerCells(table) {
    if (!table.tHead || !table.tHead.rows.length) {
      return [];
    }

    return toArray(table.tHead.rows[table.tHead.rows.length - 1].cells).filter(function (cell) {
      return cell.tagName.toLowerCase() === "th";
    });
  }

  function updateHeaderState(table, activeHeader, state) {
    headerCells(table).forEach(function (header) {
      header.setAttribute("aria-sort", SORT_NONE);
      header.classList.remove("cw-sort-ascending", "cw-sort-descending");
    });

    if (activeHeader && state !== SORT_NONE) {
      activeHeader.setAttribute("aria-sort", state);
      activeHeader.classList.add(state === SORT_ASC ? "cw-sort-ascending" : "cw-sort-descending");
    }
  }

  function sortRows(table, columnIndex, state) {
    var tbody = table.tBodies[0];
    if (!tbody) {
      return;
    }

    var rows = toArray(tbody.rows);

    rows.sort(function (leftRow, rightRow) {
      if (state === SORT_NONE) {
        return originalIndex(leftRow) - originalIndex(rightRow);
      }

      var result = compareCellText(cellText(leftRow, columnIndex), cellText(rightRow, columnIndex));
      if (state === SORT_DESC) {
        result *= -1;
      }

      return result || originalIndex(leftRow) - originalIndex(rightRow);
    });

    rows.forEach(function (row) {
      tbody.appendChild(row);
    });
  }

  function activateHeader(table, header) {
    var nextState = nextSortState(header.getAttribute("aria-sort"));

    updateHeaderState(table, header, nextState);
    sortRows(table, header.cellIndex, nextState);
  }

  function prepareHeader(table, header) {
    header.classList.add("cw-sortable-header");
    header.setAttribute("aria-sort", SORT_NONE);
    header.setAttribute("tabindex", "0");

    if (!header.getAttribute("title")) {
      header.setAttribute("title", SORT_LABEL);
    }

    header.addEventListener("click", function (event) {
      if (event.target.closest("a, button, input, select, textarea")) {
        return;
      }

      activateHeader(table, header);
    });

    header.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }

      event.preventDefault();
      activateHeader(table, header);
    });
  }

  function prepareTable(table) {
    if (table.getAttribute("data-cw-sortable-ready") === "true") {
      return;
    }

    var tbody = table.tBodies[0];
    var headers = headerCells(table);

    if (!tbody || tbody.rows.length < 2 || !headers.length) {
      return;
    }

    if (!table.getAttribute("class")) {
      table.setAttribute("data-cw-plain-table", "true");
    }

    table.setAttribute("data-cw-sortable-ready", "true");
    table.classList.add("cw-sortable-table");

    toArray(tbody.rows).forEach(function (row, index) {
      row.setAttribute("data-cw-original-row", String(index));
    });

    headers.forEach(function (header) {
      prepareHeader(table, header);
    });
  }

  function initTableSorting() {
    document.querySelectorAll(".md-typeset table").forEach(prepareTable);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initTableSorting);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTableSorting);
  } else {
    initTableSorting();
  }
})();
