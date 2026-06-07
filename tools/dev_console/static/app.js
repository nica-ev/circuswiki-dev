let state = {
  config: null,
  pages: [],
  selected: null,
  details: null,
  vaultHealth: null,
  activeTab: "file-test",
  batchPlan: null,
  navigationScan: null,
  navigationPreview: null,
  matrixWindow: { start: 0, end: 0 },
  matrixDrag: null,
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
  state.config = config;
  $("model").value = config.default_model;
  $("prompt").value = config.default_prompt;
  renderFileLanguageOptions(config);
}

async function loadHealth() {
  const sourceLang = fileSourceLang();
  const targetLang = fileTargetLang();
  const health = await api(`/api/health?source_lang=${encodeURIComponent(sourceLang)}&target_lang=${encodeURIComponent(targetLang)}`);
  $("metric-total").textContent = health.total;
  $("metric-translated").textContent = health.translated;
  $("metric-needs").textContent = health.needs_translation;
  $("metric-issues").textContent = health.with_issues;
  state.pages = health.pages;
  renderPages();
}

async function loadPages() {
  const sourceLang = fileSourceLang();
  const result = await api(`/api/pages?source_lang=${encodeURIComponent(sourceLang)}`);
  state.pages = result.pages.map((source) => ({ source }));
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
    button.textContent = page.source.replace(`docs/${fileSourceLang()}/`, "");
    button.title = page.source;
    button.addEventListener("click", () => selectPage(page.source));
    $("pages").appendChild(button);
  });
}

async function selectPage(path) {
  state.selected = path;
  renderPages();
  state.details = await api(
    `/api/page?path=${encodeURIComponent(path)}&source_lang=${encodeURIComponent(fileSourceLang())}&target_lang=${encodeURIComponent(fileTargetLang())}`
  );
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
        source_lang: fileSourceLang(),
        target_lang: fileTargetLang(),
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
  const maxSourceChars = Number($("batch-max-chars").value);
  if (!targetLang) {
    batchLog("Select a target language.");
    return;
  }
  if (!Number.isInteger(maxFiles) || maxFiles < 1) {
    batchLog("max_files must be at least 1.");
    return;
  }
  if ($("batch-max-chars").value && (!Number.isInteger(maxSourceChars) || maxSourceChars < 1)) {
    batchLog("max_source_chars must be empty or at least 1.");
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
        source_lang: $("batch-source").value,
        reason: $("batch-reason").value,
        max_source_chars: $("batch-max-chars").value ? maxSourceChars : null,
        path_filter: $("batch-path-filter").value.trim(),
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
  const targetSelect = $("batch-target");
  const sourceSelect = $("batch-source");
  const reasonSelect = $("batch-reason");
  const currentTarget = targetSelect.value || "en";
  const currentSource = sourceSelect.value || "all";
  const currentReason = reasonSelect.value || "all";
  const languages = state.vaultHealth?.languages || [];
  const languageNames = state.vaultHealth?.language_names || {};
  const targetOptions = [
    '<option value="all">All target languages</option>',
    ...languages.map((language) => `<option value="${escapeHtml(language)}">${escapeHtml(languageLabel(language, languageNames[language]))}</option>`),
  ];
  const sourceOptions = [
    '<option value="all">All source languages</option>',
    ...languages.map((language) => `<option value="${escapeHtml(language)}">${escapeHtml(languageLabel(language, languageNames[language]))}</option>`),
  ];
  const reasonOptions = batchReasonOptions().map(
    (reason) => `<option value="${escapeHtml(reason)}">${escapeHtml(batchReasonLabel(reason))}</option>`
  );
  targetSelect.innerHTML = targetOptions.join("");
  sourceSelect.innerHTML = sourceOptions.join("");
  reasonSelect.innerHTML = reasonOptions.join("");
  if (currentTarget === "all" || languages.includes(currentTarget)) {
    targetSelect.value = currentTarget;
  }
  if (currentSource === "all" || languages.includes(currentSource)) {
    sourceSelect.value = currentSource;
  }
  if (batchReasonOptions().includes(currentReason)) {
    reasonSelect.value = currentReason;
  }
}

function renderFileLanguageOptions(config) {
  const languages = config.languages || [];
  const options = languages
    .map((language) => `<option value="${escapeHtml(language.code)}">${escapeHtml(languageLabel(language.code, language.name))}</option>`)
    .join("");
  $("file-source-lang").innerHTML = options;
  $("file-target-lang").innerHTML = options;
  $("file-source-lang").value = config.default_source_lang || "de";
  $("file-target-lang").value = config.default_target_lang || "en";
}

function fileSourceLang() {
  return $("file-source-lang")?.value || state.config?.default_source_lang || "de";
}

function fileTargetLang() {
  return $("file-target-lang")?.value || state.config?.default_target_lang || "en";
}

function renderBatchPlan() {
  const plan = state.batchPlan;
  if (!plan) {
    $("batch-summary").innerHTML = "";
    $("batch-list").innerHTML = "";
    return;
  }

  $("batch-summary").innerHTML = `
    <span class="pill">Target: <strong>${escapeHtml(languageLabel(plan.target_lang, plan.target_language))}</strong></span>
    <span class="pill">Planned: <strong>${plan.planned_count}</strong></span>
    <span class="pill">Candidates: <strong>${plan.total_candidates}</strong></span>
    <span class="pill">Chars: <strong>${plan.total_source_chars}</strong></span>
    <span class="pill">Limit: <strong>${plan.max_files}</strong></span>
    <span class="pill">Source policy: <strong>${escapeHtml(formatSourcePolicy(plan.source_policy))}</strong></span>
    <span class="pill">Filters: <strong>${escapeHtml(formatBatchFilters(plan.filters || {}))}</strong></span>
    ${plan.source_counts ? `<span class="pill">By source: <strong>${escapeHtml(formatLanguageCounts(plan.source_counts, state.vaultHealth?.language_names || {}))}</strong></span>` : ""}
    ${plan.target_counts ? `<span class="pill">By language: <strong>${escapeHtml(formatTargetCounts(plan.target_counts, state.vaultHealth?.language_names || {}))}</strong></span>` : ""}
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
          <td>${escapeHtml(languageLabel(item.source_lang, item.source_language))}</td>
          <td>${escapeHtml(languageLabel(item.target_lang, item.target_language))}</td>
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

function formatTargetCounts(counts, languageNames) {
  return formatLanguageCounts(counts, languageNames);
}

function formatLanguageCounts(counts, languageNames) {
  return Object.entries(counts)
    .map(([language, count]) => `${languageLabel(language, languageNames[language])}: ${count}`)
    .join(", ");
}

function formatSourcePolicy(policy) {
  if (policy === "canonical_source_per_translation_group") {
    return "Canonical source per group";
  }
  return policy || "default";
}

function batchReasonOptions() {
  return [
    "all",
    "missing_file",
    "fallback_page",
    "source_hash_mismatch",
    "missing_source_hash",
    "translation_source_lang_mismatch",
  ];
}

function batchReasonLabel(reason) {
  return {
    all: "All reasons",
    missing_file: "Missing file",
    fallback_page: "Fallback page",
    source_hash_mismatch: "Source hash mismatch",
    missing_source_hash: "Missing source hash",
    translation_source_lang_mismatch: "Source language mismatch",
  }[reason] || reason;
}

function formatBatchFilters(filters) {
  const names = state.vaultHealth?.language_names || {};
  const parts = [
    `source=${languageLabel(filters.source_lang || "all", filters.source_lang === "all" ? "All source languages" : names[filters.source_lang])}`,
    `reason=${batchReasonLabel(filters.reason || "all")}`,
  ];
  if (filters.max_source_chars) {
    parts.push(`max chars=${filters.max_source_chars}`);
  }
  if (filters.path_filter) {
    parts.push(`text="${filters.path_filter}"`);
  }
  return parts.join(", ");
}

function navLog(value) {
  $("nav-log").textContent =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

async function loadNavigationScan() {
  setBusy(true);
  navLog("Scanning navigation...");
  try {
    const scan = await api("/api/navigation/scan");
    state.navigationScan = scan;
    $("nav-model").value = JSON.stringify(scan.model, null, 2);
    renderNavigationLanguageOptions();
    renderNavigationScan();
    navLog(scan);
  } catch (error) {
    navLog(error.message);
  } finally {
    setBusy(false);
  }
}

async function initNavigationModel() {
  setBusy(true);
  navLog("Creating canonical model from German nav...");
  try {
    const result = await api("/api/navigation/init", {
      method: "POST",
      body: JSON.stringify({ language: "de" }),
    });
    $("nav-model").value = JSON.stringify(result.model, null, 2);
    state.navigationPreview = result.preview;
    renderNavigationPreview();
    await loadNavigationScan();
  } catch (error) {
    navLog(error.message);
  } finally {
    setBusy(false);
  }
}

async function translateNavigationLabels() {
  const model = currentNavigationModel();
  if (!model) {
    return;
  }
  const sourceLang = $("nav-source").value || "de";
  if (!sourceLang) {
    navLog("Select a navigation source language.");
    return;
  }

  setBusy(true);
  navLog(`Translating navigation labels from ${sourceLang} to all other configured languages...`);
  try {
    const result = await api("/api/navigation/translate-all-labels", {
      method: "POST",
      body: JSON.stringify({
        model,
        source_lang: sourceLang,
        llm_model: $("model").value.trim(),
      }),
    });
    $("nav-model").value = JSON.stringify(result.model, null, 2);
    state.navigationPreview = result.preview;
    renderNavigationPreview();
    navLog({
      source: languageLabel(result.source_lang, result.source_language),
      target_count: result.target_count,
      results: result.results.map((item) => ({
        target: languageLabel(item.target_lang, item.target_language),
        translated_count: item.translated_count,
        translations: item.translations,
      })),
    });
  } catch (error) {
    navLog(error.message);
  } finally {
    setBusy(false);
  }
}

async function previewNavigationModel() {
  const model = currentNavigationModel();
  if (!model) {
    return;
  }

  setBusy(true);
  navLog("Rendering navigation preview...");
  try {
    const preview = await api("/api/navigation/preview", {
      method: "POST",
      body: JSON.stringify({ model }),
    });
    state.navigationPreview = preview;
    renderNavigationPreview();
    navLog(preview);
  } catch (error) {
    navLog(error.message);
  } finally {
    setBusy(false);
  }
}

async function applyNavigationModel() {
  const model = currentNavigationModel();
  if (!model) {
    return;
  }

  setBusy(true);
  navLog("Previewing before apply...");
  try {
    state.navigationPreview = await api("/api/navigation/preview", {
      method: "POST",
      body: JSON.stringify({ model }),
    });
    renderNavigationPreview();
    const result = await api("/api/navigation/apply", {
      method: "POST",
      body: JSON.stringify({ model }),
    });
    navLog(result);
    await loadNavigationScan();
  } catch (error) {
    navLog(error.message);
  } finally {
    setBusy(false);
  }
}

function currentNavigationModel() {
  try {
    return JSON.parse($("nav-model").value);
  } catch (error) {
    navLog(`Invalid navigation JSON: ${error.message}`);
    return null;
  }
}

function renderNavigationLanguageOptions() {
  const select = $("nav-source");
  const scan = state.navigationScan;
  if (!scan) {
    select.innerHTML = "";
    return;
  }
  const current = select.value || "de";
  select.innerHTML = scan.languages
    .map((language) => `<option value="${escapeHtml(language)}">${escapeHtml(languageLabel(language, scan.language_names[language]))}</option>`)
    .join("");
  if (scan.languages.includes(current)) {
    select.value = current;
  }
}

function renderNavigationScan() {
  const scan = state.navigationScan;
  if (!scan) {
    $("nav-summary").innerHTML = "";
    $("nav-diagnostics").innerHTML = "";
    return;
  }

  $("nav-summary").innerHTML = `
    <span class="pill">Model: <strong>${scan.model_exists ? "exists" : "missing"}</strong></span>
    <span class="pill ${scan.has_multiple_navs ? "yellow" : "green"}">Nav variants: <strong>${scan.nav_variants.length}</strong></span>
    <span class="pill">Languages: <strong>${scan.languages.length}</strong></span>
    <span class="pill">Orphan candidates: <strong>${scan.orphan_candidate_count}</strong></span>
    <span class="pill ${scan.model_missing_targets.length ? "yellow" : "green"}">Model missing targets: <strong>${scan.model_missing_targets.length}</strong></span>
  `;

  const configCards = Object.entries(scan.configs).map(([language, config]) => `
    <article class="nav-card">
      <strong>${escapeHtml(languageLabel(language, scan.language_names[language]))}</strong>
      <span>${config.count} entries</span>
      ${config.duplicate_pages.length ? `<p>Duplicate pages: ${escapeHtml(config.duplicate_pages.join(", "))}</p>` : ""}
      ${config.missing_files.length ? `<p>Missing files: ${config.missing_files.length}</p>` : ""}
    </article>
  `).join("");

  const variants = scan.nav_variants.map((variant, index) => `
    <article class="nav-card">
      <strong>Variant ${index + 1}</strong>
      <p>${escapeHtml(variant.languages.join(", "))}</p>
    </article>
  `).join("");

  const orphans = scan.orphan_candidates.slice(0, 20).map((item) =>
    `<li>${escapeHtml(item.title)} <span class="muted-inline">${escapeHtml(item.page)}</span></li>`
  ).join("");

  $("nav-diagnostics").innerHTML = `
    ${variants}
    ${configCards}
    <article class="nav-card">
      <strong>Orphan candidates</strong>
      <ul>${orphans || "<li>none</li>"}</ul>
    </article>
  `;
}

function renderNavigationPreview() {
  const preview = state.navigationPreview;
  if (!preview) {
    $("nav-preview-output").innerHTML = "";
    return;
  }

  const changed = Object.entries(preview.changed).map(([language, isChanged]) => `
    <article class="nav-card">
      <strong>${escapeHtml(language)}</strong>
      <span class="${isChanged ? "pill yellow" : "pill green"}">${isChanged ? "will change" : "unchanged"}</span>
      <pre class="inline-code">${escapeHtml((preview.rendered[language] || "").slice(0, 900))}</pre>
    </article>
  `).join("");

  $("nav-preview-output").innerHTML = `
    <article class="nav-card">
      <strong>Preview</strong>
      <p>${preview.changed_count} config files would change.</p>
    </article>
    ${changed}
  `;
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
  const window = normalizedMatrixWindow(rows.length);
  const visibleRows = rows.slice(window.start, window.end);
  updateMatrixWindowControls(rows.length, window.start, window.end);

  const table = $("health-matrix");
  const wrapWidth = $("health-matrix").parentElement.clientWidth || 900;
  const matrixLayout = matrixLayoutSizes();
  const plotWidth = Math.max(
    matrixLayout.minPlotWidth,
    wrapWidth - matrixLayout.labelWidth
  );
  const cellWidth = visibleRows.length
    ? Math.max(2, Math.floor((plotWidth - visibleRows.length - 1) / visibleRows.length))
    : 15;
  table.style.setProperty("--matrix-cell-width", `${cellWidth}px`);
  table.innerHTML = "";
  const thead = document.createElement("thead");
  const header = document.createElement("tr");
  header.innerHTML = `
    <th class="sticky-col lang-col">lang</th>
    ${visibleRows.map((row, index) => `<th class="note-index" title="${escapeHtml(row.translation_id)}">${window.start + index + 1}</th>`).join("")}
  `;
  thead.appendChild(header);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  health.languages.forEach((language) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<th class="sticky-col lang-col">${escapeHtml(language)}</th>`;

    visibleRows.forEach((row) => {
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

function normalizedMatrixWindow(rowCount) {
  if (rowCount <= 0) {
    state.matrixWindow = { start: 0, end: 0 };
    return state.matrixWindow;
  }

  let start = Number.isInteger(state.matrixWindow.start) ? state.matrixWindow.start : 0;
  let end = Number.isInteger(state.matrixWindow.end) && state.matrixWindow.end > 0
    ? state.matrixWindow.end
    : rowCount;

  start = Math.max(0, Math.min(start, rowCount - 1));
  end = Math.max(start + 1, Math.min(end, rowCount));
  state.matrixWindow = { start, end };
  return state.matrixWindow;
}

function updateMatrixWindowControls(rowCount, start, end) {
  const startHandle = $("matrix-window-start");
  const endHandle = $("matrix-window-end");
  const selection = $("matrix-window-selection");
  const label = $("matrix-window-label");

  if (!rowCount) {
    startHandle.style.setProperty("--handle-left", "0%");
    endHandle.style.setProperty("--handle-left", "0%");
    selection.style.setProperty("--range-left", "0%");
    selection.style.setProperty("--range-width", "0%");
    label.textContent = "0/0";
    return;
  }

  const startPercent = (start / rowCount) * 100;
  const endPercent = (end / rowCount) * 100;
  startHandle.style.setProperty("--handle-left", `${startPercent}%`);
  endHandle.style.setProperty("--handle-left", `${endPercent}%`);
  selection.style.setProperty("--range-left", `${startPercent}%`);
  selection.style.setProperty("--range-width", `${endPercent - startPercent}%`);
  label.textContent = `${start + 1}-${end} / ${rowCount}`;
}

function setMatrixWindow(start, end) {
  state.matrixWindow = { start, end };
  renderVaultHealth();
}

function filteredVaultRows() {
  const health = state.vaultHealth;
  if (!health) {
    return [];
  }
  const query = $("health-filter").value.toLowerCase();
  const statusFilter = $("health-status").value;
  return health.rows.filter((row) => matchesHealthFilter(row, query, statusFilter));
}

function matrixIndexFromPointer(event) {
  const rows = filteredVaultRows();
  const rowCount = rows.length;
  if (!rowCount) {
    return 0;
  }

  const rect = $("matrix-window-range").getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
  return Math.round(ratio * rowCount);
}

function startMatrixDrag(kind, event) {
  const rows = filteredVaultRows();
  if (!rows.length) {
    return;
  }

  event.preventDefault();
  const window = normalizedMatrixWindow(rows.length);
  state.matrixDrag = {
    kind,
    pointerStart: matrixIndexFromPointer(event),
    start: window.start,
    end: window.end,
    width: window.end - window.start,
  };
  $("matrix-window-start").classList.toggle("active", kind === "start");
  $("matrix-window-end").classList.toggle("active", kind === "end");
}

function updateMatrixDrag(event) {
  const drag = state.matrixDrag;
  if (!drag) {
    return;
  }

  const rowCount = filteredVaultRows().length;
  if (!rowCount) {
    return;
  }

  const pointer = matrixIndexFromPointer(event);
  if (drag.kind === "start") {
    setMatrixWindow(Math.max(0, Math.min(pointer, drag.end - 1)), drag.end);
    return;
  }
  if (drag.kind === "end") {
    setMatrixWindow(drag.start, Math.max(drag.start + 1, Math.min(pointer, rowCount)));
    return;
  }

  const delta = pointer - drag.pointerStart;
  const nextStart = Math.max(0, Math.min(drag.start + delta, rowCount - drag.width));
  setMatrixWindow(nextStart, nextStart + drag.width);
}

function stopMatrixDrag() {
  state.matrixDrag = null;
  $("matrix-window-start").classList.remove("active");
  $("matrix-window-end").classList.remove("active");
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

function matrixLayoutSizes() {
  const styles = getComputedStyle(document.documentElement);
  return {
    labelWidth: cssPixelValue(styles.getPropertyValue("--matrix-label-width"), 82),
    minPlotWidth: cssPixelValue(styles.getPropertyValue("--matrix-min-plot-width"), 1320),
  };
}

function cssPixelValue(value, fallback) {
  const parsed = Number.parseFloat(String(value).trim());
  return Number.isFinite(parsed) ? parsed : fallback;
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
  if (tabName === "navigation" && !state.navigationScan) {
    loadNavigationScan().catch((error) => navLog(error.message));
  }
}

function setBusy(isBusy) {
  $("dry-run").disabled = isBusy;
  $("translate").disabled = isBusy;
  $("refresh").disabled = isBusy;
  $("refresh-health").disabled = isBusy;
  $("repair-health").disabled = isBusy;
  $("batch-plan").disabled = isBusy;
  $("nav-scan").disabled = isBusy;
  $("nav-init").disabled = isBusy;
  $("nav-translate").disabled = isBusy;
  $("nav-preview").disabled = isBusy;
  $("nav-apply").disabled = isBusy;
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

function languageLabel(code, name) {
  if (!code) {
    return "";
  }
  if (code === "all") {
    return name || "All target languages";
  }
  if (!name || name === code) {
    return code;
  }
  return `${name} (${code})`;
}

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => switchTab(button.dataset.tab));
});

$("filter").addEventListener("input", renderPages);
$("refresh").addEventListener("click", () => {
  loadHealth().catch((error) => log(error.message));
  loadVaultHealth().catch((error) => healthLog(error.message));
});
$("file-source-lang").addEventListener("change", () => {
  state.selected = null;
  state.details = null;
  renderDetails();
  loadHealth().catch((error) => log(error.message));
});
$("file-target-lang").addEventListener("change", () => {
  if (state.selected) {
    selectPage(state.selected).catch((error) => log(error.message));
  }
  loadHealth().catch((error) => log(error.message));
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
$("nav-scan").addEventListener("click", () => {
  loadNavigationScan().catch((error) => navLog(error.message));
});
$("nav-init").addEventListener("click", () => {
  initNavigationModel().catch((error) => navLog(error.message));
});
$("nav-translate").addEventListener("click", () => {
  translateNavigationLabels().catch((error) => navLog(error.message));
});
$("nav-preview").addEventListener("click", () => {
  previewNavigationModel().catch((error) => navLog(error.message));
});
$("nav-apply").addEventListener("click", () => {
  applyNavigationModel().catch((error) => navLog(error.message));
});
$("health-filter").addEventListener("input", () => {
  state.matrixWindow = { start: 0, end: 0 };
  renderVaultHealth();
});
$("health-status").addEventListener("change", () => {
  state.matrixWindow = { start: 0, end: 0 };
  renderVaultHealth();
});
$("matrix-window-start").addEventListener("pointerdown", (event) => startMatrixDrag("start", event));
$("matrix-window-end").addEventListener("pointerdown", (event) => startMatrixDrag("end", event));
$("matrix-window-selection").addEventListener("pointerdown", (event) => startMatrixDrag("range", event));
document.addEventListener("pointermove", updateMatrixDrag);
document.addEventListener("pointerup", stopMatrixDrag);
window.addEventListener("resize", () => {
  if (state.activeTab === "vault-health") {
    renderVaultHealth();
  }
});
$("dry-run").addEventListener("click", () => runTranslation(true));
$("translate").addEventListener("click", () => runTranslation(false));

loadConfig()
  .then(loadHealth)
  .then(loadVaultHealth)
  .catch((error) => {
    log(error.message);
    healthLog(error.message);
  });
