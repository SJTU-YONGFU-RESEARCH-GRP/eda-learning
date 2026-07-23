/**
 * Shared canvas + challenge chrome for clustering labs.
 * Pattern matches digital_learning tools: starter example + challenge catalog.
 */
import {
  PALETTE,
  clusterColor,
  cutsize,
  starterLayout,
} from "./clustering-core.js";

export function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "className") node.className = v;
    else if (k === "text") node.textContent = v;
    else if (k === "html") node.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") {
      node.addEventListener(k.slice(2).toLowerCase(), v);
    } else if (v === false || v == null) {
      /* skip */
    } else if (v === true) {
      node.setAttribute(k, "");
    } else {
      node.setAttribute(k, v);
    }
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

export function drawGraph(canvas, graph, opts = {}) {
  const ctx = canvas.getContext("2d");
  const layout = opts.layout || starterLayout();
  const assignment = opts.assignment || null;
  const highlightPairs = new Set(opts.highlightPairs || []);
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth || 420;
  const h = canvas.clientHeight || 300;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#f7faf9";
  ctx.fillRect(0, 0, w, h);

  for (const e of graph.edges) {
    const a = layout[e.u];
    const b = layout[e.v];
    if (!a || !b) continue;
    const key = e.u < e.v ? `${e.u}|${e.v}` : `${e.v}|${e.u}`;
    const hot = highlightPairs.has(key);
    const cut =
      assignment && assignment[e.u] != null && assignment[e.u] !== assignment[e.v];
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.strokeStyle = hot ? "#b45309" : cut ? "#9f1239" : "#94a3b8";
    ctx.lineWidth = hot ? 3.5 : cut ? 2.5 : 2;
    ctx.stroke();
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;
    ctx.fillStyle = "#334155";
    ctx.font = "12px ui-monospace, Menlo, Consolas, monospace";
    ctx.fillText(String(e.w), mx + 4, my - 4);
  }

  for (const n of graph.nodes) {
    const p = layout[n];
    if (!p) continue;
    const cid = assignment ? assignment[n] : n;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 16, 0, Math.PI * 2);
    ctx.fillStyle = clusterColor(cid, PALETTE);
    ctx.fill();
    ctx.strokeStyle = "#0f172a";
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.font = "bold 13px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(n, p.x, p.y);
  }
  ctx.textAlign = "start";
  ctx.textBaseline = "alphabetic";
}

export function metricsBlock(lines) {
  const pre = el("pre", { className: "metrics-pre" });
  pre.textContent = lines.join("\n");
  return pre;
}

/**
 * @param {HTMLElement} root
 * @param {object} opts
 * @param {string} opts.starterHtml - HTML for starter-note (reference example)
 * @param {Array} opts.challenges - [{id,title,level,prompt,hint,setup,check}]
 * @param {() => void} opts.loadStarter - restore worked reference example
 * @param {(ctx) => void} opts.renderWorkspace - draw graph/metrics into panels
 * @param {(ctx) => HTMLElement[]} [opts.extraActions] - tool-specific buttons
 */
export function createChallengeLab(root, opts) {
  const challenges = opts.challenges || [];
  const state = {
    challengeOn: false,
    challengeId: challenges[0]?.id || "",
    challengeHint: false,
    clearedIds: [],
    statusKind: "idle",
    statusText: "Idle",
  };

  const ctx = {
    state,
    canvas: null,
    metrics: null,
    actions: null,
    setStatus() {},
    getChallenge() {
      return challenges.find((c) => c.id === state.challengeId) || challenges[0];
    },
    rerender: () => render(),
  };

  function challengeById(id) {
    return challenges.find((c) => c.id === id) || challenges[0];
  }

  function nextId() {
    const i = challenges.findIndex((c) => c.id === state.challengeId);
    return challenges[(i + 1) % challenges.length].id;
  }

  function startChallenge(id) {
    const ch = challengeById(id || state.challengeId);
    state.challengeId = ch.id;
    state.challengeOn = true;
    state.challengeHint = false;
    setStatus("idle", "Challenge armed — act, then Check");
    if (typeof ch.setup === "function") ch.setup(ctx);
    render();
  }

  function loadStarter() {
    state.challengeOn = false;
    state.challengeHint = false;
    setStatus("idle", "Starter loaded (reference)");
    opts.loadStarter(ctx);
    render();
  }

  function setStatus(kind, text) {
    state.statusKind = kind;
    state.statusText = text;
    const statusEl = root.querySelector("#lab-status");
    if (statusEl) {
      statusEl.className = `challenge-status ${kind}`;
      statusEl.textContent = text;
    }
  }

  function checkNow() {
    if (!state.challengeOn) {
      setStatus("idle", "Load a challenge with Start");
      return;
    }
    const ch = challengeById(state.challengeId);
    const ok = typeof ch.check === "function" ? !!ch.check(ctx) : false;
    if (ok) {
      if (!state.clearedIds.includes(ch.id)) state.clearedIds.push(ch.id);
      setStatus("pass", "PASS");
    } else {
      setStatus("fail", "Not yet — try again or show hint");
    }
    render();
  }

  function render() {
    const ch = challengeById(state.challengeId);
    const cleared = state.clearedIds.filter((id) => challenges.some((c) => c.id === id)).length;
    const options = challenges
      .map((c) => {
        const mark = state.clearedIds.includes(c.id) ? "✓ " : "";
        const sel = c.id === state.challengeId ? " selected" : "";
        return `<option value="${c.id}"${sel}>${mark}[${c.level}] ${c.title}</option>`;
      })
      .join("");

    root.innerHTML = "";
    const note = el("div", { className: "starter-note" });
    note.innerHTML =
      opts.starterHtml +
      `<p><button type="button" class="btn btn-secondary" id="lab-starter">Load starter example</button></p>`;

    const challengeBox = el("div", { className: "challenge" });
    challengeBox.innerHTML = `
      <div class="chal-head">
        <h2>Challenges</h2>
        <span class="chal-progress">${cleared} / ${challenges.length} cleared</span>
      </div>
      <div class="chal-pick">
        <label for="lab-chal-sel">Pick one</label>
        <select id="lab-chal-sel">${options}</select>
      </div>
      <p class="chal-prompt">${state.challengeOn ? escapeHtml(ch.prompt) : "Pick a challenge and click <strong>Start</strong>. The starter example above stays available as a reference — reload it anytime."}</p>
      ${
        state.challengeOn && state.challengeHint
          ? `<p class="chal-hint"><strong>Hint:</strong> ${escapeHtml(ch.hint || "")}</p>`
          : ""
      }
      <div class="tool-actions" id="lab-chal-actions">
        <button type="button" class="btn btn-secondary" id="lab-chal-start">${state.challengeOn ? "Restart" : "Start"}</button>
        <button type="button" class="btn btn-ghost" id="lab-chal-hint" ${state.challengeOn ? "" : "disabled"}>${state.challengeHint ? "Hide hint" : "Show hint"}</button>
        <button type="button" class="btn btn-primary" id="lab-chal-check" ${state.challengeOn ? "" : "disabled"}>Check</button>
        <button type="button" class="btn btn-ghost" id="lab-chal-next" ${state.clearedIds.includes(state.challengeId) ? "" : "disabled"}>Next challenge</button>
        <button type="button" class="btn btn-ghost" id="lab-chal-stop" ${state.challengeOn ? "" : "disabled"}>Stop checking</button>
        <span class="challenge-status ${state.statusKind}" id="lab-status">${escapeHtml(state.statusText)}</span>
      </div>
    `;

    const actions = el("div", { className: "tool-actions lab-extra-actions" });
    const layout = el("div", { className: "tool-layout split-wide" });
    const left = el("div", { className: "panel" }, [
      el("div", { className: "panel-head" }, [el("h2", { text: "Graph" })]),
      el("div", { className: "panel-body" }, [
        el("canvas", {
          className: "cluster-canvas",
          style: "width:100%;height:300px;border-radius:8px;border:1px solid var(--line);",
        }),
      ]),
    ]);
    const right = el("div", { className: "panel" }, [
      el("div", { className: "panel-head" }, [el("h2", { text: "Reference / metrics" })]),
      el("div", { className: "panel-body metrics-body" }),
    ]);
    layout.append(left, right);
    root.append(note, challengeBox, actions, layout);

    ctx.canvas = root.querySelector("canvas");
    ctx.metrics = root.querySelector(".metrics-body");
    ctx.actions = actions;
    ctx.setStatus = setStatus;

    if (typeof opts.extraActions === "function") {
      for (const btn of opts.extraActions(ctx) || []) actions.append(btn);
    }

    root.querySelector("#lab-starter").onclick = () => loadStarter();
    root.querySelector("#lab-chal-sel").onchange = (e) => {
      state.challengeId = e.target.value;
      if (state.challengeOn) startChallenge(state.challengeId);
      else render();
    };
    root.querySelector("#lab-chal-start").onclick = () => startChallenge(state.challengeId);
    root.querySelector("#lab-chal-hint").onclick = () => {
      state.challengeHint = !state.challengeHint;
      render();
    };
    root.querySelector("#lab-chal-check").onclick = () => checkNow();
    root.querySelector("#lab-chal-next").onclick = () => startChallenge(nextId());
    root.querySelector("#lab-chal-stop").onclick = () => {
      state.challengeOn = false;
      state.challengeHint = false;
      render();
    };

    opts.renderWorkspace(ctx);
  }

  // First visit: load starter reference automatically
  opts.loadStarter(ctx);
  render();
  return ctx;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export { cutsize, PALETTE };
