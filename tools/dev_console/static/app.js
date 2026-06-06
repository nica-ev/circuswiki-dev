let state = {
  pages: [],
  selected: null,
  details: null,
  vaultHealth: null,
  activeTab: "file-test",
  batchPlan: null,
};

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const text = await response.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch (error) {
    const preview = text.slice(0, 120).replace(/\s+/g, " ");
    throw new Error(
      `Expected JSON from ${path}, got ${response.status} ${response.statusText}: ${preview}`
    );
  }

  if (!response.ok) {
    throw new Error(data?.error || response.statusText);
  }
  return data;
}

function log(value) {
  $("log").textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

function healthLog(value) {
  $("health-details").textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

async function loadConfig() {
  const config = await api("/api/config");
  $("model").value = config.default_model;
  $("prompt").value = config.default_prompt;
}

async function loadHealth() {
  const health = await api("/api/health");
  $("metric-total").textContent = health.total;
  $("metric-translated").textContent = health.translated;
  $("metric-needs").textContent = health.needs_translation;
  $("metric-issues").textContent = health.with_issues;
  state.pages = health.pages;
  renderPages();
}

async function loadVaultHealth() {
  const health = await api("/api/vault-health");
  state.vaultHealth = health;
  $("metric-matrix").textContent = `${health.totals.green}/${health.totals.yellow}/${health.totals.red}`;
  renderBatchLanguageOptions();
  renderVaultHealth();
}

function renderPages() {
  const filter = $("filter").value.toLowerCase();
  const pages = state.pages.filter((page) =>
    page.source.toLowerCase().includes(filter)
  );
  $("pages").innerHTML = "";

  pages.forEach((page) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "page";
    if (state.selected === page.source) {
      button.classList.add("active");
    }
    button.textContent = page.source.replace("docs/de/", "");
    button.title = page.source;
    button.addEventListener("click", () => selectPage(page.source));
    $("pages").appendChild(button);
  });
}

async function selectPage(path) {
  state.selected = path;
  renderPages();
  state.details = await api(`/api/page?path=${encodeURIComponent(path)}`);
  renderDetails();
}

function renderDetails() {
  const page = state.details;
  if (!page) {
    $("details").innerHTML = "";
    return;
  }

  const issues = page.issues.length
    ? page.issues.map((issue) => `<span class="issue">${escapeHtml(issue)}</span>`).join("")
    : '<span class="ok">none</span>';

  $("details").innerHTML = `
    <dt>Source</dt><dd>${escapeHtml(page.source)}</dd>
    <dt>Target</dt><dd>${escapeHtml(page.target)}</dd>
    <dt>ID</dt><dd>${escapeHtml(page.translation_id)}</dd>
    <dt>Hash</dt><dd>${escapeHtml(page.source_hash.slice(0, 12))}</dd>
    <dt>Target Exists</dt><dd>${page.target_exists ? "yes" : "no"}</dd>
    <dt>Needs Work</dt><dd>${page.needs_translation ? "yes" : "no"}</dd>
    <dt>Issues</dt><dd>${issues}</dd>
  `;
}

async function runTranslation(dryRun) {
  if (!state.selected) {
    log("Select a source page first.");
    return;
  }

  setBusy(true);
  log(dryRun ? "Running dry run..." : "Translating file...");
  try {
    const result = await api("/api/translate", {
      method: "POST",
      body: JSON.stringify({
        path: state.selected,
        model: $("model").value.trim(),
        prompt: $("prompt").value.trim(),
        dry_run: dryRun,
      }),
    });
    log(result);
    await loadHealth();
    await loadVaultHealth();
    await selectPage(state.selected);
  } catch (error) {
    log(error.message);
  } finally {
    setBusy(false);
  }
}

async function runMetadataRepair() {
  if (!state.vaultHealth) {
    await loadVaultHealth();
  }

  const candidates = repairCandidates();
  const progress = $("repair-progress");
  const status = $("repair-status");
  progress.max = candidates.length;
  progress.value = 0;

  if (!candidates.length) {
    status.textContent = "No yellow existing files to repair.";
    return;
  }

  setBusy(true);
  const results = [];
  try {
    for (let index = 0; index < candidates.length; index += 1) {
      const item = candidates[index];
      status.textContent = `Repairing ${index + 1}/${candidates.length}: ${item.path}`;
      const result = await api("/api/repair-metadata", {
        method: "POST",
        body: JSON.stringify({ path: item.path }),
      });
      results.push(result);
      progress.value = index + 1;
    }
    status.textContent = `Repair complete: ${results.filter((item) => item.changed).length} changed, ${results.length} processed.`;
    healthLog(results);
    await loadVaultHealth();
  } catch (error) {
    status.textContent = "Repair stopped.";
    healthLog(error.message);
  } finally {
    setBusy(false);
  }
}

async function createBatchPlan() {
  const targetLang = $("batch-target").value;
  const maxFiles = Number($("batch-max-files").value);
  if (!targetLang) {
    batchLog("Select a target language.");
    return;
  }
  if (!Number.isInteger(maxFiles) || maxFiles < 1) {
    batchLog("max_files must be at least 1.");
    return;
  }

  setBusy(true);
  $("batch-run").disabled = true;
  $("batch-status").textContent = "Planning...";
  try {
    const plan = await api("/api/batch-plan", {
      method: "POST",
      body: JSON.stringify({
        target_lang: targetLang,
        max_files: maxFiles,
      }),
    });
    state.batchPlan = plan;
    renderBatchPlan();
    $("batch-run").disabled = plan.candidates.length === 0;
    $("batch-status").textContent = `Plan ready: ${plan.planned_count}/${plan.total_candidates} candidates selected.`;
  } catch (error) {
    state.batchPlan = null;
    batchLog(error.message);
    $("batch-status").textContent = "Planning failed.";
  } finally {
    setBusy(false);
    $("batch-run").disabled = !state.batchPlan || state.batchPlan.candidates.length === 0;
  }
}

async function runBatchTranslation() {
  const plan = state.batchPlan;
  if (!plan || !plan.candidates.length) {
    batchLog("Create a non-empty plan first.");
    return;
  }

  const progress = $("batch-progress");
  progress.max = plan.candidates.length;
  progress.value = 0;
  setBusy(true);
  const results = [];

  try {
    for (let index = 0; index < plan.candidates.length; index += 1) {
      const item = plan.candidates[index];
      $("batch-status").textContent = `Translating ${index + 1}/${plan.candidates.length}: ${item.translation_id}`;
      const result = await api("/api/batch-translate-file", {
        method: "POST",
        body: JSON.stringify({
          source_path: item.source_path,
          source_lang: item.source_lang,
          target_lang: item.target_lang,
          model: $("model").value.trim(),
          prompt: $("prompt").value.trim(),
        }),
      });
      results.push(result);
      progress.value = index + 1;
      batchLog(results);
    }
    $("batch-status").textContent = `Batch complete: ${results.length} translated.`;
    await loadHealth();
    await loadVaultHealth();
  } catch (error) {
    $("batch-status").textContent = "Batch stopped.";
    batchLog({
      error: error.message,
      completed: results.length,
      total: plan.candidates.length,
      results,
    });
  } finally {
    setBusy(false);
    $("batch-run").disabled = !state.batchPlan || state.batchPlan.candidates.length === 0;
  }
}

function renderBatchLanguageOptions() {
  const select = $("batch-target");
  const current = select.value || "en";
  const languages = state.vaultHealth?.languages || [];
  select.innerHTML = languages
    .map((language) => `<option value="${escapeHtml(language)}">${escapeHtml(language)}</option>`)
    .join("");
  if (languages.includes(current)) {
    select.value = current;
  }
}

function renderBatchPlan() {
  const plan = state.batchPlan;
  if (!plan) {
    $("batch-summary").innerHTML = "";
    $("batch-list").innerHTML = "";
    return;
  }

  $("batch-summary").innerHTML = `
    <span class="pill">Target: <strong>${escapeHtml(plan.target_lang)}</strong></span>
    <span class="pill">Planned: <strong>${plan.planned_count}</strong></span>
    <span class="pill">Candidates: <strong>${plan.total_candidates}</strong></span>
    <span class="pill">Chars: <strong>${plan.total_source_chars}</strong></span>
    <span class="pill">Limit: <strong>${plan.max_files}</strong></span>
  `;

  const table = $("batch-list");
  table.innerHTML = `
    <thead>
      <tr>
        <th>#</th>
        <th>ID</th>
        <th>Source</th>
        <th>Target</th>
        <th>Chars</th>
        <th>Reason</th>
      </tr>
    </thead>
    <tbody>
      ${plan.candidates.map((item, index) => `
        <tr>
          <td>${index + 1}</td>
          <td>${escapeHtml(item.translation_id)}</td>
          <td>${escapeHtml(item.source_lang)}</td>
          <td>${escapeHtml(item.target_lang)}</td>
          <td>${item.source_chars}</td>
          <td>${escapeHtml(item.reason)}</td>
        </tr>
      `).join("")}
    </tbody>
  `;
  batchLog(plan);
}

function batchLog(value) {
  $("batch-log").textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

function repairCandidates() {
  const seen = new Set();
  const candidates = [];
  for (const row of state.vaultHealth?.rows || []) {
    for (const language of state.vaultHealth.languages) {
      const cell = row.cells[language];
      if (cell.status !== "yellow" || !cell.exists || !cell.path) {
        continue;
      }
      if (seen.has(cell.path)) {
        continue;
      }
      seen.add(cell.path);
      candidates.push({
        path: cell.path,
        translation_id: row.translation_id,
        language,
      });
    }
  }
  return candidates;
}

function renderVaultHealth() {
  const health = state.vaultHealth;
  if (!health) {
    return;
  }

  $("health-summary").innerHTML = `
    <span class="pill">Notes: <strong>${health.total_notes}</strong></span>
    <span class="pill green">Green: <strong>${health.totals.green}</strong></span>
    <span class="pill yellow">Yellow: <strong>${health.totals.yellow}</strong></span>
    <span class="pill red">Red: <strong>${health.totals.red}</strong></span>
    <span class="pill">Languages: <strong>${health.languages.join(", ")}</strong></span>
  `;

  const query = $("health-filter").value.toLowerCase();
  const statusFilter = $("health-status").value;
  const rows = health.rows.filter((row) => matchesHealthFilter(row, query, statusFilter));

  const table = $("health-matrix");
  table.innerHTML = "";
  const thead = document.createElement("thead");
  const header = document.createElement("tr");
  header.innerHTML = `
    <th class="sticky-col lang-col">lang</th>
    ${rows.map((row, index) => `<th class="note-index" title="${escapeHtml(row.translation_id)}">${index + 1}</th>`).join("")}
  `;
  thead.appendChild(header);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  health.languages.forEach((language) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<th class="sticky-col lang-col">${escapeHtml(language)}</th>`;

    rows.forEach((row) => {
      const cell = row.cells[language];
      const td = document.createElement("td");
      const button = document.createElement("button");
      button.type = "button";
      button.className = `status-cell ${cell.status}`;
      button.title = `${language} | ${row.translation_id} | ${cell.issues.length ? cell.issues.join(", ") : "ok"}`;
      button.setAttribute("aria-label", button.title);
      button.addEventListener("click", () => {
        healthLog({
          translation_id: row.translation_id,
          title: row.title,
          source_lang: row.source_lang,
          language,
          ...cell,
        });
      });
      td.appendChild(button);
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
}

function matchesHealthFilter(row, query, statusFilter) {
  const cells = Object.values(row.cells);
  if (statusFilter !== "all" && !cells.some((cell) => cell.status === statusFilter)) {
    return false;
  }
  if (!query) {
    return true;
  }
  const haystack = [
    row.translation_id,
    row.title,
    row.relative_path,
    row.source_lang,
    ...cells.flatMap((cell) => [cell.path, cell.relative_path, ...cell.issues]),
  ].join(" ").toLowerCase();
  return haystack.includes(query);
}

function switchTab(tabName) {
  state.activeTab = tabName;
  document.querySelectorAll(".tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `tab-${tabName}`);
  });
  if (tabName === "vault-health" && !state.vaultHealth) {
    loadVaultHealth().catch((error) => healthLog(error.message));
  }
}

function setBusy(isBusy) {
  $("dry-run").disabled = isBusy;
  $("translate").disabled = isBusy;
  $("refresh").disabled = isBusy;
  $("refresh-health").disabled = isBusy;
  $("repair-health").disabled = isBusy;
  $("batch-plan").disabled = isBusy;
  if (isBusy) {
    $("batch-run").disabled = true;
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => switchTab(button.dataset.tab));
});

$("filter").addEventListener("input", renderPages);
$("refresh").addEventListener("click", () => {
  loadHealth().catch((error) => log(error.message));
  loadVaultHealth().catch((error) => healthLog(error.message));
});
$("refresh-health").addEventListener("click", () => {
  loadVaultHealth().catch((error) => healthLog(error.message));
});
$("repair-health").addEventListener("click", () => {
  runMetadataRepair().catch((error) => healthLog(error.message));
});
$("batch-plan").addEventListener("click", () => {
  createBatchPlan().catch((error) => batchLog(error.message));
});
$("batch-run").addEventListener("click", () => {
  runBatchTranslation().catch((error) => batchLog(error.message));
});
$("health-filter").addEventListener("input", renderVaultHealth);
$("health-status").addEventListener("change", renderVaultHealth);
$("dry-run").addEventListener("click", () => runTranslation(true));
$("translate").addEventListener("click", () => runTranslation(false));

loadConfig()
  .then(loadHealth)
  .then(loadVaultHealth)
  .catch((error) => {
    log(error.message);
    healthLog(error.message);
  });
