/**
 * Interactive graph / bipartition lab chrome.
 * Learner flips, swaps, and assigns nodes; Check scores learner state.
 * Reveal golden is optional study aid — not the path to pass.
 */
import { fitGraphLayout } from "./canvas-hires.js";
import {
  BAD_SEED,
  TINY_GRAPH,
  cloneGraph,
  cutsize,
  partsString,
  starterLayout,
} from "./clustering-core.js";
import { createChallengeLab, drawGraph, el, metricsBlock } from "./clustering-ui.js";

/** Unlabeled bipartition seed (all null) — learner must assign. */
export function emptyAssignment(nodes = TINY_GRAPH.nodes) {
  return Object.fromEntries(nodes.map((n) => [n, null]));
}

/** Clone an assignment map. */
export function cloneAssignment(asn) {
  return asn ? { ...asn } : {};
}

/** Hit-test node under canvas click (screen coords after fitGraphLayout). */
export function hitNode(canvas, clientX, clientY, layout = starterLayout(), radius = 20) {
  const rect = canvas.getBoundingClientRect();
  const w = canvas.clientWidth || rect.width || 640;
  const h = canvas.clientHeight || rect.height || 480;
  const { layout: screen, nodeR } = fitGraphLayout(layout, w, h);
  const mx = clientX - rect.left;
  const my = clientY - rect.top;
  const r = Math.max(radius, nodeR + 4);
  let best = null;
  let bestD = r * r;
  for (const [id, p] of Object.entries(screen)) {
    const dx = mx - p.x;
    const dy = my - p.y;
    const d = dx * dx + dy * dy;
    if (d <= bestD) {
      bestD = d;
      best = id;
    }
  }
  return best;
}

function sideCount(asn) {
  const s0 = Object.values(asn).filter((v) => v === "0").length;
  const s1 = Object.values(asn).filter((v) => v === "1").length;
  return { s0, s1, n: Object.keys(asn).length };
}

/**
 * Create an interactive graph lab.
 *
 * opts:
 *  - starterHtml
 *  - initialAssignment (default BAD_SEED)
 *  - revealAssignment (golden)
 *  - lockedNodes: string[] cannot flip/assign
 *  - lockedSides: { node: "0"|"1" } forced on load/reset
 *  - graph / getGraph()
 *  - cutFn(asn, graph) override cutsize (e.g. hyperedgeCut)
 *  - layout
 *  - actionSet: "bipart" | "none"  (default bipart)
 *  - challenges[]  check(ctx, api) must use learner state
 *  - extraActions(ctx, api)
 *  - extraMetrics(api)
 *  - onChallengeSetup(ctx, api, ch)
 *  - onAfterChange(ctx, api)
 *  - highlightPairs() optional
 *  - drawAssignment(api) optional override displayed assignment
 */
export function createInteractiveGraphLab(root, opts = {}) {
  const locked = new Set(opts.lockedNodes || []);
  const lockedSides = { ...(opts.lockedSides || {}) };
  const layout = opts.layout || starterLayout();
  const actionSet = opts.actionSet || "bipart";

  let graph =
    typeof opts.getGraph === "function"
      ? opts.getGraph()
      : cloneGraph(opts.graph || TINY_GRAPH);

  function baseSeed() {
    const seed = cloneAssignment(opts.initialAssignment || BAD_SEED);
    for (const [n, s] of Object.entries(lockedSides)) seed[n] = String(s);
    return seed;
  }

  let assignment = baseSeed();
  let selected = graph.nodes[0] || "A";
  let swapPartner = null;
  let revealed = false;
  const meta = opts.initialMeta ? { ...opts.initialMeta } : {};

  const cutFn =
    typeof opts.cutFn === "function"
      ? opts.cutFn
      : (asn, g) => cutsize(asn, g.edges);

  const api = {
    getAssignment: () => assignment,
    setAssignment: (a) => {
      assignment = cloneAssignment(a);
      for (const [n, s] of Object.entries(lockedSides)) {
        if (locked.has(n) || lockedSides[n] != null) assignment[n] = String(s);
      }
    },
    getSelected: () => selected,
    setSelected: (id) => {
      selected = id;
    },
    getSwapPartner: () => swapPartner,
    setSwapPartner: (id) => {
      swapPartner = id;
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    getGraph: () => graph,
    setGraph: (g) => {
      graph = cloneGraph(g);
    },
    getMeta: () => meta,
    setMeta: (patch) => {
      Object.assign(meta, patch || {});
    },
    resetMeta: () => {
      for (const k of Object.keys(meta)) delete meta[k];
      if (opts.initialMeta) Object.assign(meta, opts.initialMeta);
    },
    partsString: () => partsString(assignment),
    cutsize: () => cutFn(assignment, graph),
    flipNode,
    swapNodes,
    assignSide,
    clearToSeed,
  };

  function flipNode(id = selected) {
    if (!id || locked.has(id)) return false;
    const cur = assignment[id];
    assignment = {
      ...assignment,
      [id]: cur === "0" ? "1" : cur === "1" ? "0" : "0",
    };
    revealed = false;
    return true;
  }

  function assignSide(side, id = selected) {
    if (!id || locked.has(id)) return false;
    assignment = { ...assignment, [id]: String(side) };
    revealed = false;
    return true;
  }

  function swapNodes(a = selected, b = swapPartner) {
    if (!a || !b || a === b) return false;
    if (locked.has(a) || locked.has(b)) return false;
    const next = { ...assignment };
    const tmp = next[a];
    next[a] = next[b];
    next[b] = tmp;
    assignment = next;
    revealed = false;
    return true;
  }

  function clearToSeed() {
    assignment = baseSeed();
    revealed = false;
    swapPartner = null;
    api.resetMeta();
    if (typeof opts.onClear === "function") opts.onClear(api);
  }

  function applyLocked() {
    for (const [n, s] of Object.entries(lockedSides)) {
      assignment = { ...assignment, [n]: String(s) };
    }
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      opts.idlePromptHtml ||
      "Pick a challenge and click <strong>Start</strong>. Edit the partition in the workspace, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      (opts.starterHtml ||
        `<p><strong>Your workspace:</strong> click a node to select it, then Flip / Assign / Swap.
        Challenges check <em>your</em> assignment — Reveal golden is optional study help.</p>`) +
      (opts.starterExtraHtml || ""),
    loadStarter() {
      if (typeof opts.getGraph === "function") graph = opts.getGraph();
      else graph = cloneGraph(opts.graph || TINY_GRAPH);
      clearToSeed();
      selected = graph.nodes[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        if (typeof opts.getGraph === "function") graph = opts.getGraph();
        else graph = cloneGraph(opts.graph || TINY_GRAPH);
        clearToSeed();
        if (typeof ch.setup === "function") ch.setup(ctx, api);
        else if (typeof opts.onChallengeSetup === "function") opts.onChallengeSetup(ctx, api, ch);
      },
      check: (ctx) => {
        if (typeof ch.check === "function") return !!ch.check(ctx, api);
        return false;
      },
    })),
    extraActions(ctx) {
      const btns = [];

      if (actionSet === "bipart") {
        btns.push(
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: `Flip ${selected}${locked.has(selected) ? " 🔒" : ""}`,
            onClick: () => {
              flipNode(selected);
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Assign 0",
            onClick: () => {
              assignSide("0");
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Assign 1",
            onClick: () => {
              assignSide("1");
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: swapPartner ? `Swap ${selected}↔${swapPartner}` : "Swap (pick partner)",
            onClick: () => {
              if (!swapPartner) {
                ctx.setStatus("idle", "Shift+click another node as swap partner");
                return;
              }
              swapNodes(selected, swapPartner);
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Clear to seed",
            onClick: () => {
              clearToSeed();
              ctx.rerender();
            },
          })
        );
      }

      if (opts.revealAssignment) {
        btns.push(
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: revealed ? "Hide golden" : "Reveal golden (study)",
            onClick: () => {
              if (revealed) {
                clearToSeed();
              } else {
                assignment = cloneAssignment(opts.revealAssignment);
                applyLocked();
                revealed = true;
              }
              ctx.rerender();
            },
          })
        );
      }

      if (typeof opts.extraActions === "function") {
        btns.push(...(opts.extraActions(ctx, api) || []));
      }
      return btns;
    },
    renderWorkspace(ctx) {
      const displayAsn =
        typeof opts.drawAssignment === "function"
          ? opts.drawAssignment(api)
          : assignment;
      const highlightPairs =
        typeof opts.highlightPairs === "function" ? opts.highlightPairs(api) : opts.highlightPairs || [];
      const selectedNodes = [selected, swapPartner].filter(Boolean);

      drawGraph(ctx.canvas, graph, {
        layout,
        assignment: displayAsn,
        highlightPairs,
        selectedNodes,
      });

      ctx.canvas.onclick = (ev) => {
        const hit = hitNode(ctx.canvas, ev.clientX, ev.clientY, layout);
        if (!hit) return;
        if (ev.shiftKey) {
          swapPartner = hit === selected ? null : hit;
        } else {
          selected = hit;
        }
        ctx.rerender();
      };

      const cut = cutFn(assignment, graph);
      const parts = partsString(
        Object.fromEntries(
          Object.entries(assignment).filter(([, v]) => v != null && v !== "?")
        )
      );
      const { s0, s1, n } = sideCount(assignment);
      const lines = [
        `selected: ${selected}${locked.has(selected) ? " (locked)" : ""}` +
          (swapPartner ? ` · swap partner: ${swapPartner}` : ""),
        `parts: ${parts || "—"}`,
        `cutsize: ${Number.isFinite(cut) ? cut : "—"}`,
        `balance: ${s0} vs ${s1} (n=${n})`,
        revealed ? "view: revealed golden (study)" : "view: your assignment",
        "tip: click node to select · Shift+click sets swap partner",
      ];
      if (typeof opts.extraMetrics === "function") {
        lines.push(...(opts.extraMetrics(api) || []));
      }
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
      if (typeof opts.renderExtra === "function") opts.renderExtra(ctx, api);
    },
  });

  return api;
}

/** Challenge helpers */
export function asnEquals(a, b) {
  const keys = new Set([...Object.keys(a || {}), ...Object.keys(b || {})]);
  for (const k of keys) {
    if (String(a?.[k]) !== String(b?.[k])) return false;
  }
  return true;
}

export function sameParts(api, expected) {
  return partsString(api.getAssignment()) === expected;
}

export function cutIs(api, n) {
  return api.cutsize() === n;
}

export function unlabeledOk(asn) {
  return Object.values(asn).every((v) => v === "0" || v === "1");
}

// balanceRatio may not exist on core — compute locally if needed
function _balanceRatio(asn) {
  const vals = Object.values(asn).filter((v) => v === "0" || v === "1");
  const s0 = vals.filter((v) => v === "0").length;
  const s1 = vals.filter((v) => v === "1").length;
  if (!s0 || !s1) return null;
  return Math.min(s0, s1) / Math.max(s0, s1);
}

export { partsString, cutsize, BAD_SEED, el, metricsBlock, _balanceRatio as balanceRatio };
