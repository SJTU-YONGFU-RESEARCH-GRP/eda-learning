/**
 * Interactive placement lab chrome.
 * Learner moves cells; Check scores learner positions / metrics.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  hpwl,
  totalHpwl,
} from "./placement-core.js";
import { createChallengeLab, drawPlacement, el, metricsBlock } from "./placement-ui.js";

const DEFAULT_WORLD = { worldMin: -0.5, worldMax: 8.5 };

/**
 * Invert drawPlacement mapping: canvas client click → world coords.
 */
export function canvasToWorld(canvas, clientX, clientY, opts = {}) {
  const rect = canvas.getBoundingClientRect();
  const w = canvas.clientWidth || rect.width || 640;
  const h = canvas.clientHeight || rect.height || 480;
  const pad = 28;
  const worldMin = opts.worldMin ?? DEFAULT_WORLD.worldMin;
  const worldMax = opts.worldMax ?? DEFAULT_WORLD.worldMax;
  const span = worldMax - worldMin;
  const scale = Math.min((w - 2 * pad) / span, (h - 2 * pad) / span);
  const ox = (w - span * scale) / 2;
  const oy = (h - span * scale) / 2;
  const mx = clientX - rect.left;
  const my = clientY - rect.top;
  return {
    x: worldMin + (mx - ox) / scale,
    y: worldMax - (my - oy) / scale,
    scale,
  };
}

/**
 * Hit-test nearest cell within pixel radius of click (default ~16px).
 */
export function hitCell(positions, canvas, clientX, clientY, opts = {}) {
  const world = canvasToWorld(canvas, clientX, clientY, opts);
  const cells = opts.cells || CELLS;
  const maxPx = opts.hitRadiusPx ?? 16;
  const maxWorld = maxPx / Math.max(world.scale, 1e-9);
  let best = null;
  let bestD = maxWorld;
  for (const id of cells) {
    const p = positions[id];
    if (!p) continue;
    const d = Math.hypot(p.x - world.x, p.y - world.y);
    if (d <= bestD) {
      bestD = d;
      best = id;
    }
  }
  return best;
}

function snapCoord(v, snap) {
  if (!snap || snap <= 0) return v;
  return Math.round(v / snap) * snap;
}

/**
 * Create an interactive placement lab.
 *
 * opts:
 *  - initialPositions (default STARTER_PLACEMENT)
 *  - revealPositions (default GOLDEN_PLACEMENT)
 *  - lockedIds: cells that cannot move
 *  - snap: coordinate snap (default 1)
 *  - drawOpts / getDrawOpts(api)
 *  - starterHtml, starterExtraHtml
 *  - challenges[] — check(ctx, api) must use learner positions
 *  - extraActions(ctx, api)
 *  - extraMetrics(api) → string[]
 *  - onAfterChange(ctx, api)
 *  - onLoadStarter(api)
 *  - showPerNetMetrics (default true)
 */
export function createInteractivePlacementLab(root, opts = {}) {
  const locked = new Set(opts.lockedIds || []);
  const snap = opts.snap ?? 1;
  const seed = () => clonePositions(opts.initialPositions || STARTER_PLACEMENT);
  const revealSeed = () => clonePositions(opts.revealPositions || GOLDEN_PLACEMENT);

  let positions = seed();
  let selectedId = (opts.cells || CELLS)[0] || "A";
  let revealed = false;

  const api = {
    getPositions: () => positions,
    setPositions: (p) => {
      positions = clonePositions(p);
    },
    getSelected: () => selectedId,
    setSelected: (id) => {
      selectedId = id;
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    getHpwl: () => totalHpwl(opts.nets || NETS, positions),
    getNetHpwl: (i) => hpwl((opts.nets || NETS)[i], positions),
    getLocked: () => locked,
  };

  function moveSelectedTo(wx, wy) {
    if (locked.has(selectedId)) return;
    if (!positions[selectedId]) return;
    positions = {
      ...positions,
      [selectedId]: {
        x: snapCoord(wx, snap),
        y: snapCoord(wy, snap),
      },
    };
    revealed = false;
  }

  function nudge(dx, dy) {
    if (locked.has(selectedId)) return;
    const p = positions[selectedId];
    if (!p) return;
    positions = {
      ...positions,
      [selectedId]: { x: p.x + dx, y: p.y + dy },
    };
    revealed = false;
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Move cells in the workspace, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      (opts.starterHtml ||
        `<p><strong>Your workspace:</strong> click a cell to select, click empty canvas to move it.
        Nudge with arrows. Challenges check <strong>your</strong> positions (starter HPWL ${GOLDENS.starterHpwl},
        compact golden ${GOLDENS.goldenHpwl}). <em>Reveal golden</em> is optional study help.</p>`) +
      (opts.starterExtraHtml || ""),
    loadStarter() {
      positions = seed();
      revealed = false;
      selectedId = (opts.cells || CELLS)[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        positions = seed();
        revealed = false;
        selectedId = (opts.cells || CELLS)[0] || "A";
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
      const cells = opts.cells || CELLS;
      const btns = [];

      for (const id of cells) {
        const lockedMark = locked.has(id) ? " 🔒" : "";
        btns.push(
          el("button", {
            className: "btn " + (selectedId === id ? "btn-primary" : "btn-secondary"),
            type: "button",
            text: `${id}${lockedMark}`,
            onClick: () => {
              selectedId = id;
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
            nudge(-(snap || 1), 0);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "→",
          onClick: () => {
            nudge(snap || 1, 0);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↑",
          onClick: () => {
            nudge(0, snap || 1);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↓",
          onClick: () => {
            nudge(0, -(snap || 1));
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Reset to starter",
          onClick: () => {
            positions = seed();
            revealed = false;
            if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: revealed ? "Hide golden" : "Reveal golden (study)",
          onClick: () => {
            if (revealed) {
              positions = seed();
              revealed = false;
            } else {
              positions = revealSeed();
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
      const nets = opts.nets || NETS;
      const cells = opts.cells || CELLS;
      const drawOpts =
        typeof opts.getDrawOpts === "function"
          ? opts.getDrawOpts(api)
          : { ...(opts.drawOpts || {}) };

      drawPlacement(ctx.canvas, cells, positions, nets, {
        ...drawOpts,
        highlightCells: [...(drawOpts.highlightCells || []), selectedId],
      });

      ctx.canvas.onclick = (ev) => {
        const hit = hitCell(positions, ctx.canvas, ev.clientX, ev.clientY, {
          cells,
          worldMin: drawOpts.worldMin,
          worldMax: drawOpts.worldMax,
        });
        if (hit && !ev.shiftKey) {
          selectedId = hit;
          ctx.rerender();
          return;
        }
        const world = canvasToWorld(ctx.canvas, ev.clientX, ev.clientY, drawOpts);
        moveSelectedTo(world.x, world.y);
        ctx.rerender();
        if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
      };

      const tot = totalHpwl(nets, positions);
      const lines = [
        `selected: ${selectedId}${locked.has(selectedId) ? " (locked)" : ""}`,
        `total HPWL: ${tot}`,
        revealed ? "view: revealed golden (study)" : "view: your placement",
        "tip: click cell to select · click canvas to move · arrows nudge",
      ];
      if (opts.showPerNetMetrics !== false) {
        for (let i = 0; i < nets.length; i++) {
          lines.push(`  net${i} [${nets[i].join(",")}]: ${hpwl(nets[i], positions)}`);
        }
      }
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

/** Soft compare of two placements (coords within eps). */
export function positionsNear(a, b, eps = 0.05) {
  const ids = Object.keys(b);
  if (Object.keys(a).length !== ids.length) return false;
  return ids.every(
    (id) => a[id] && Math.abs(a[id].x - b[id].x) <= eps && Math.abs(a[id].y - b[id].y) <= eps
  );
}

export {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  el,
  metricsBlock,
  totalHpwl,
  hpwl,
};
