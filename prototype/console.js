"use strict";
const $ = selector => document.querySelector(selector);
const priorities = ["P1", "P2", "P3", "P4"];
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let state = {tickets: [], accounts: [], teams: [], mode: "suggestions"};
let selected = null;

async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({...body, actor: $("#operator").value.trim() || "demo-operator"})
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Local service unavailable");
  return result;
}
function toast(message) {
  $("#toast").textContent = message;
  $("#toast").classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => $("#toast").classList.remove("show"), 3500);
}
function ticket() { return state.tickets.find(t => t.id === selected); }
function left(t) { return Date.parse(t.triage.sla_deadline) - Date.now(); }
function formatTime(ms) {
  if (ms <= 0) return "SLA breached";
  const minutes = Math.floor(ms / 60000), hours = Math.floor(minutes / 60);
  return hours ? `${hours} h ${minutes % 60} min left` : `${minutes} min ${Math.floor(ms / 1000) % 60} s left`;
}
function badge(priority) { return `<span class="sev ${escapeHtml(priority)}">${escapeHtml(priority || "Abstains")}</span>`; }
function updateClocks() {
  for (const t of state.tickets) {
    document.querySelectorAll(`[data-clock="${t.id}"]`).forEach(el => { el.textContent = formatTime(left(t)); });
    const bar = document.querySelector(`[data-bar="${t.id}"]`);
    if (bar) {
      const fraction = Math.max(0, left(t) / (t.triage.sla_minutes * 60000));
      bar.style.width = `${Math.min(100, fraction * 100)}%`;
      bar.style.background = left(t) <= 0 || fraction < 0.25 ? "var(--p1)" : fraction < 0.5 ? "var(--p2)" : "var(--ok)";
    }
  }
}
function render() {
  $("#mode").textContent = state.mode === "suggestions" ? "L1 · suggestions only" : "Assisted · raises enabled";
  const sorted = [...state.tickets].sort((a, b) => left(a) - left(b));
  $("#queue").innerHTML = sorted.map(t => `<button class="ticket" data-id="${t.id}" aria-current="${t.id === selected}">
    <div class="row">${badge(t.triage.effective_priority)}<span class="id">${t.id}</span><span class="clock" data-clock="${t.id}"></span></div>
    <div class="title">${escapeHtml(t.title)}</div><div class="acct">${escapeHtml(t.triage.account)} · ${escapeHtml(t.triage.tier)}</div>
    <div class="state">${escapeHtml(t.status.replaceAll("_", " "))}</div><div class="bar"><span data-bar="${t.id}"></span></div></button>`).join("") || '<p class="empty">No tickets yet.</p>';
  document.querySelectorAll(".ticket").forEach(button => { button.onclick = () => { selected = button.dataset.id; render(); }; });
  const t = ticket();
  if (!t) { $("#copilot").innerHTML = ""; updateClocks(); return; }
  const a = t.triage;
  // CALM-01 returns the chosen non-P1 class score; the initial label is kept
  // separately. Do not display that score as if it belonged to the initial P1.
  const scoredClass = a.evidence.some(e => e.rule === "CALM-01") ? a.proposed_severity : (a.classifier_severity || a.proposed_severity);
  $("#detail").innerHTML = `<div class="meta">${t.id} · ${escapeHtml(a.account)} · customer declared ${badge(a.declared_priority)}</div>
    <h2>${escapeHtml(t.title)}</h2><p class="explanation">Opened ${escapeHtml(new Date(a.created_at).toLocaleString())}; the SLA always starts at this timestamp.</p>
    <div class="msg">${escapeHtml(a.redacted_text)}</div><p class="redact-note">${a.redaction.count} item(s) masked before local analysis and storage. Best-effort demo redaction.</p>
    <p class="explanation">Contract ${a.contract_verified ? "verified against synthetic account record" : "UNKNOWN — fallback clock is provisional"}. Model ${escapeHtml(a.model_version)}.</p>`;
  const hidden = t.taken_over;
  $("#copilot").innerHTML = `<h3>Triage copilot</h3>
    <div class="proposal"><div class="big">${badge(a.effective_priority)}<strong>Effective priority</strong></div>
    ${a.auto_raised ? '<p class="raised">Raised automatically by the assisted policy when the ticket was created.</p>' : ""}
    ${hidden ? '<p class="taken">Engineer has taken over. Automatic proposal hidden; manual controls remain available.</p>' : `
      <p>Model/rule suggestion: ${badge(a.proposed_severity)}</p><p>${escapeHtml(a.reason)}</p>
      ${a.evidence.map(e => `<div class="raised"><strong>${escapeHtml(e.rule)}</strong> · ${escapeHtml(e.source)}<br>“${escapeHtml(e.quote)}”</div>`).join("")}
      <p class="explanation">${a.classifier_score === null ? "No classifier score available." : `Model score for class ${escapeHtml(scoredClass)}: ${Math.round(a.classifier_score * 100)}%.`} ${escapeHtml(a.score_note)}</p>`}
    <dl><dt>SLA clock</dt><dd data-clock="${t.id}"></dd><dt>Team</dt><dd>${escapeHtml(a.team)}</dd><dt>Human verification</dt><dd>${t.human_checked ? "Recorded" : "Not recorded"}</dd></dl>
    ${a.review_reasons.length ? `<div class="held"><strong>Human review</strong><ul>${a.review_reasons.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul></div>` : ""}</div>
    ${hidden ? "" : `<div class="similar"><h4>Reusable sources · same customer or generic KB</h4>
      ${a.similar.map(s => `<details><summary><strong>${escapeHtml(s.id)}</strong> ${escapeHtml(s.title)}</summary><p>${escapeHtml(s.text)}</p>
        <p class="explanation">Similarity ${s.score.toFixed(2)} · ${escapeHtml(s.version)} · ${escapeHtml(s.source)}<br>${escapeHtml(s.review_status)}</p></details>`).join("") || '<p class="held">No source found. No troubleshooting suggestion; hand over to an engineer.</p>'}</div>`}
    <div class="manual"><h4>Engineer controls</h4><div class="actions"><button class="btn primary" id="review">Verify / change priority or team</button>
      <button class="btn" id="take" ${hidden ? "disabled" : ""}>Take over</button>
      <button class="btn" id="accept" ${t.status === "accepted" || ((a.requires_human || hidden || state.mode === "suggestions") && !t.human_checked) ? "disabled" : ""}>${t.status === "accepted" ? "Triage accepted" : "Accept triage"}</button></div>
      <p class="rule">Only an engineer can lower priority, with a reason. Diagnosis, remediation and customer contact remain human-only.</p></div>`;
  $("#review").onclick = openReview;
  $("#take").onclick = () => act("take_over");
  $("#accept").onclick = () => act("accept");
  updateClocks();
}
async function refresh() {
  state = await api("/api/state");
  if (!state.tickets.some(t => t.id === selected)) selected = state.tickets[0]?.id || null;
  $("#account").innerHTML = state.accounts.map(a => `<option value="${escapeHtml(a.id)}">${escapeHtml(a.name)} · ${escapeHtml(a.tier)}</option>`).join("") + '<option value="unknown">Unknown account (human only)</option>';
  render();
}
async function act(action, extra = {}) {
  try { await api("/api/action", {ticket_id: selected, action, ...extra}); await refresh(); toast("Engineer action recorded"); }
  catch (error) { toast(error.message); }
}
function openReview() {
  const a = ticket().triage;
  $("#reviewPriority").innerHTML = priorities.map(p => `<option ${p === a.effective_priority ? "selected" : ""}>${p}</option>`).join("");
  $("#reviewTeam").innerHTML = state.teams.map(team => `<option ${team === a.team ? "selected" : ""}>${escapeHtml(team)}</option>`).join("");
  $("#reviewReason").value = ""; $("#reviewError").textContent = "";
  $("#reviewDlg").showModal(); $("#reviewReason").focus();
}
$("#reviewForm").onsubmit = async event => {
  event.preventDefault();
  try {
    await api("/api/action", {ticket_id: selected, action: "change", priority: $("#reviewPriority").value,
      team: $("#reviewTeam").value, reason: $("#reviewReason").value});
    $("#reviewDlg").close(); await refresh(); toast("Engineer decision saved; acceptance is now available");
  } catch (error) { $("#reviewError").textContent = error.message; }
};
$("#newTicket").onclick = () => {
  const local = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  $("#created").value = local; $("#newError").textContent = ""; $("#newDlg").showModal(); $("#title").focus();
};
$("#newForm").onsubmit = async event => {
  event.preventDefault();
  const button = $("#newForm button[type=submit]"); button.disabled = true;
  try {
    const form = Object.fromEntries(new FormData(event.target));
    form.created_at = new Date($("#created").value).toISOString();
    const created = await api("/api/triage", form);
    selected = created.id;
    await refresh();
    $("#newDlg").close(); event.target.reset();
  } catch (error) { $("#newError").textContent = error.message; }
  finally { button.disabled = false; }
};
$("#loadDemo").onclick = async () => {
  try { await api("/api/demo", {}); await refresh(); toast("Six synthetic demo tickets loaded"); }
  catch (error) { toast(error.message); }
};
$("#switch").onclick = () => {
  $("#switchDescription").textContent = state.mode === "suggestions" ?
    "Enable assisted mode for NEW tickets: contextual safety rules or a classifier score ≥ 0.70 may raise priority. Existing tickets stay unchanged." :
    "Switch every NEW ticket to suggestions only: no automatic priority change. Existing tickets and engineer decisions stay unchanged; acceptance needs human verification.";
  $("#switchReason").value = ""; $("#switchError").textContent = ""; $("#switchDlg").showModal();
};
$("#switchForm").onsubmit = async event => {
  event.preventDefault();
  try {
    await api("/api/switch", {mode: state.mode === "suggestions" ? "assisted" : "suggestions", reason: $("#switchReason").value});
    $("#switchDlg").close(); await refresh(); toast("Global operating mode saved");
  } catch (error) { $("#switchError").textContent = error.message; }
};
$("#audit").onclick = async () => {
  try {
    const audit = await api("/api/audit");
    const url = URL.createObjectURL(new Blob([JSON.stringify(audit, null, 2)], {type: "application/json"}));
    const link = document.createElement("a"); link.href = url; link.download = "triage-audit.json"; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (error) { toast(error.message); }
};
document.querySelectorAll("[data-close]").forEach(b => { b.onclick = () => document.getElementById(b.dataset.close).close(); });
refresh().catch(error => {
  $("#fatal").hidden = false;
  $("#fatal").textContent = `Local API unavailable. Start the Python server, then open http://127.0.0.1:8765. ${error.message}`;
});
setInterval(updateClocks, 1000);
