/**
 * Interactive floorplanning lab chrome.
 * Learner places/moves modules; Check scores learner state.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  GOLDEN_PACK,
  OUTLINE,
  TINY_MODULES,
  cloneModules,
  clonePack,
  deadspace,
  density,
  drawFloorplan,
  isLegalPacking,
  legalityReport,
  moduleAreaSum,
  outlineArea,
} from "./floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

/** Packing with no placements — learner must place. */
export function emptyPack() {
  return {};
}

/** Unplaced module list from sizes. */
export function unplacedIds(modules = TINY_MODULES) {
  return modules.map((m) => m.id);
}

/**
 * Map canvas click → outline grid cell (lower-left coords).
 */
export function canvasToCell(canvas, clientX, clientY, outline = OUTLINE) {
  const rect = canvas.getBoundingClientRect();
  const cw = canvas.clientWidth || rect.width;
  const ch = canvas.clientHeight || rect.height;
  const pad = 28;
  const scale = Math.min((cw - pad * 2) / outline.w, (ch - pad * 2) / outline.h);
  const ox = pad + ((cw - pad * 2) - outline.w * scale) / 2;
  const oy = pad + ((ch - pad * 2) - outline.h * scale) / 2;
  const mx = clientX - rect.left;
  const my = clientY - rect.top;
  const x = Math.floor((mx - ox) / scale);
  const yFromTop = (my - oy) / scale;
  const y = Math.floor(outline.h - yFromTop);
  return { x, y };
}

/**
 * Hit-test which placed module contains cell (x,y) as lower-left click point,
 * or any cell under the pointer in module interior.
 */
export function hitModule(pack, cell, outline = OUTLINE) {
  const { x, y } = cell;
  if (x < 0 || y < 0 || x >= outline.w || y >= outline.h) return null;
  const ids = Object.keys(pack);
  for (let i = ids.length - 1; i >= 0; i--) {
    const id = ids[i];
    const r = pack[id];
    if (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) return id;
  }
  return null;
}

/**
 * Create an interactive floorplan lab.
 *
 * opts:
 *  - title / lead already in HTML
 *  - starterHtml
 *  - challenges[]  (check must use learner pack via getPack())
 *  - getModules() optional
 *  - lockedIds: string[] modules that cannot move (macros)
 *  - initialPack: starting pack (default {})
 *  - allowSoftToggle: show reshape A buttons
 *  - extraActions(ctx)
 *  - onAfterChange(ctx)
 *  - pins / setPins for pin labs — optional via hooks
 */
export function createInteractiveFloorplanLab(root, opts = {}) {
  const locked = new Set(opts.lockedIds || []);
  let moduleSizes = cloneModules();
  if (typeof opts.getModules === "function") {
    moduleSizes = opts.getModules().map((m) => ({ ...m }));
  }

  const modules = () => moduleSizes;

  let pack = clonePack(opts.initialPack || {});
  let selectedId = moduleSizes[0]?.id || "A";
  let revealed = false;
  let pins = Array.isArray(opts.initialPins) ? opts.initialPins.map((p) => ({ ...p })) : [];

  const api = {
    getPack: () => pack,
    setPack: (p) => {
      pack = clonePack(p);
    },
    getSelected: () => selectedId,
    setSelected: (id) => {
      selectedId = id;
    },
    getPins: () => pins,
    setPins: (p) => {
      pins = (p || []).map((x) => ({ ...x }));
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    getModules: modules,
    setModuleSize: (id, w, h) => {
      moduleSizes = moduleSizes.map((m) => (m.id === id ? { ...m, w, h } : m));
      if (pack[id]) pack = { ...pack, [id]: { ...pack[id], w, h } };
    },
  };

  function placeSelectedAt(x, y) {
    const mods = modules();
    const m = mods.find((t) => t.id === selectedId);
    if (!m) return;
    if (locked.has(selectedId) && pack[selectedId]) return;
    pack = { ...pack, [selectedId]: { x, y, w: m.w, h: m.h, ...(pack[selectedId]?.macro ? { macro: true } : {}) } };
    if (pack[selectedId].macro) pack[selectedId].macro = true;
  }

  function removeSelected() {
    if (locked.has(selectedId)) return;
    const next = { ...pack };
    delete next[selectedId];
    pack = next;
  }

  function nudge(dx, dy) {
    const r = pack[selectedId];
    if (!r || locked.has(selectedId)) return;
    pack = {
      ...pack,
      [selectedId]: { ...r, x: r.x + dx, y: r.y + dy },
    };
  }

  function clearUnlocked() {
    const next = {};
    for (const [id, r] of Object.entries(pack)) {
      if (locked.has(id)) next[id] = { ...r };
    }
    pack = next;
    revealed = false;
  }

  function reshapeA(w, h) {
    const a = moduleSizes.find((m) => m.id === "A");
    if (!a || !a.soft) return;
    api.setModuleSize("A", w, h);
  }

  function resetModules() {
    moduleSizes = cloneModules();
    if (typeof opts.getModules === "function") {
      moduleSizes = opts.getModules().map((m) => ({ ...m }));
    }
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Place or edit in the workspace, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      (opts.starterHtml ||
        `<p><strong>Your workspace:</strong> select a module, click the outline grid to place it.
        Nudge with arrows. <em>Reveal golden</em> is optional study help — challenges check <strong>your</strong> packing.</p>`) +
      (opts.starterExtraHtml || ""),
    loadStarter() {
      resetModules();
      pack = clonePack(opts.initialPack || {});
      pins = Array.isArray(opts.initialPins) ? opts.initialPins.map((p) => ({ ...p })) : [];
      revealed = false;
      selectedId = modules()[0]?.id || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        // Reset to seed workspace — never auto-load golden
        resetModules();
        pack = clonePack(opts.initialPack || {});
        pins = Array.isArray(opts.initialPins) ? opts.initialPins.map((p) => ({ ...p })) : [];
        revealed = false;
        if (typeof ch.setup === "function") ch.setup(ctx, api);
        else if (typeof opts.onChallengeSetup === "function") opts.onChallengeSetup(ctx, api, ch);
      },
      check: (ctx) => {
        if (typeof ch.check === "function") return !!ch.check(ctx, api);
        return false;
      },
      hint: ch.hint,
      prompt: ch.prompt,
    })),
    extraActions(ctx) {
      const btns = [];

      // Module palette
      for (const m of modules()) {
        const lockedMark = locked.has(m.id) ? " 🔒" : "";
        btns.push(
          el("button", {
            className: "btn " + (selectedId === m.id ? "btn-primary" : "btn-secondary"),
            type: "button",
            text: `${m.id} (${m.w}×${m.h})${lockedMark}`,
            onClick: () => {
              selectedId = m.id;
              ctx.rerender();
            },
          })
        );
      }

      btns.push(
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "←",
          onClick: () => {
            nudge(-1, 0);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "→",
          onClick: () => {
            nudge(1, 0);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↑",
          onClick: () => {
            nudge(0, 1);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↓",
          onClick: () => {
            nudge(0, -1);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Remove",
          onClick: () => {
            removeSelected();
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Clear",
          onClick: () => {
            clearUnlocked();
            ctx.rerender();
          },
        })
      );

      if (opts.allowSoftToggle) {
        btns.push(
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "A → 3×2",
            onClick: () => {
              reshapeA(3, 2);
              ctx.rerender();
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "A → 2×3",
            onClick: () => {
              reshapeA(2, 3);
              ctx.rerender();
            },
          })
        );
      }

      btns.push(
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: revealed ? "Hide golden" : "Reveal golden (study)",
          onClick: () => {
            if (revealed) {
              pack = clonePack(opts.initialPack || {});
              revealed = false;
            } else {
              pack = clonePack(opts.revealPack || GOLDEN_PACK);
              revealed = true;
            }
            ctx.rerender();
          },
        })
      );

      if (typeof opts.extraActions === "function") {
        btns.push(...(opts.extraActions(ctx, api) || []));
      }
      return btns;
    },
    renderWorkspace(ctx) {
      const outline = opts.outline || OUTLINE;
      drawFloorplan(ctx.canvas, {
        outline,
        pack,
        pins,
      });

      // Click to select / place
      ctx.canvas.onclick = (ev) => {
        const cell = canvasToCell(ctx.canvas, ev.clientX, ev.clientY, outline);
        const hit = hitModule(pack, cell, outline);
        if (hit && !ev.shiftKey) {
          selectedId = hit;
          ctx.rerender();
          return;
        }
        // Place selected lower-left at clicked cell
        if (cell.x < 0 || cell.y < 0 || cell.x >= outline.w || cell.y >= outline.h) return;
        placeSelectedAt(cell.x, cell.y);
        revealed = false;
        ctx.rerender();
        if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
      };

      const rep = Object.keys(pack).length ? legalityReport(pack, outline) : { legal: null, reason: "empty" };
      const placed = Object.keys(pack).sort().join(",") || "—";
      const lines = [
        `selected: ${selectedId}${locked.has(selectedId) ? " (locked)" : ""}`,
        `placed: ${placed}`,
        `legal: ${rep.legal}`,
        `reason: ${rep.reason}`,
        `moduleArea: ${moduleAreaSum(modules())}`,
        `outlineArea: ${outlineArea(outline)}`,
        `deadspace: ${deadspace(outline, modules())}`,
        `density: ${density(outline, modules()).toFixed(4)}`,
        revealed ? "view: revealed golden (study)" : "view: your packing",
        "tip: click grid to place · click block to select · Shift+click places on top",
      ];
      if (typeof opts.extraMetrics === "function") {
        lines.push(...opts.extraMetrics(api));
      }
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
      if (typeof opts.renderExtra === "function") opts.renderExtra(ctx, api);
    },
  });

  return api;
}

/** Helpers for challenge authors */
export function packHasAll(pack, ids = ["A", "B", "C", "D", "E"]) {
  return ids.every((id) => pack[id]);
}

export function packsEqualPositions(a, b) {
  const ids = Object.keys(b);
  if (Object.keys(a).length !== ids.length) return false;
  return ids.every(
    (id) => a[id] && a[id].x === b[id].x && a[id].y === b[id].y && a[id].w === b[id].w && a[id].h === b[id].h
  );
}

export { isLegalPacking, GOLDEN_PACK, OUTLINE, TINY_MODULES, el, metricsBlock };
