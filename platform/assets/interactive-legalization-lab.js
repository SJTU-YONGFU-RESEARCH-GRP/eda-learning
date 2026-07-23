/**
 * Interactive legalization lab chrome.
 * Learner moves cells on the site/row grid; Check scores learner positions.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  CELLS,
  CHIP_H,
  CHIP_W,
  FIXED_MACROS,
  FLOAT_PLACEMENT,
  GOLDEN_PLACEMENT,
  GOLDENS,
  OVERLAP_PLACEMENT,
  ROW_H,
  ROW_YS,
  SITE_W,
  WIDTHS,
  abacusLegalize,
  cellWidth,
  clonePositions,
  detailedLegalize,
  drawLegalization,
  globalLegalize,
  greedySnap,
  isLegal,
  legalizeCost,
  legalityReport,
  overlapRemoval,
  snapX,
  snapY,
  tetrisLegalize,
  totalDisplacement,
  totalHpwl,
} from "./legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

/**
 * Invert drawLegalization mapping: canvas click → continuous chip coords
 * (lower-left origin, same as core).
 */
export function canvasToChip(canvas, clientX, clientY) {
  const rect = canvas.getBoundingClientRect();
  const W = canvas.clientWidth || rect.width || 640;
  const H = canvas.clientHeight || rect.height || 480;
  const pad = 28;
  const scaleX = (W - 2 * pad) / CHIP_W;
  const scaleY = (H - 2 * pad) / CHIP_H;
  const mx = clientX - rect.left;
  const my = clientY - rect.top;
  return {
    x: (mx - pad) / scaleX,
    y: (H - pad - my) / scaleY,
    scaleX,
    scaleY,
  };
}

/**
 * Hit-test which cell rectangle contains the click (top-most / last in CELLS order).
 */
export function hitLegalCell(positions, canvas, clientX, clientY, cells = CELLS) {
  const { x, y } = canvasToChip(canvas, clientX, clientY);
  for (let i = cells.length - 1; i >= 0; i--) {
    const id = cells[i];
    const p = positions[id];
    if (!p) continue;
    const w = cellWidth(id);
    if (x >= p.x && x < p.x + w && y >= p.y && y < p.y + ROW_H) return id;
  }
  return null;
}

/**
 * Create an interactive legalization lab.
 *
 * opts:
 *  - initialPositions (default OVERLAP_PLACEMENT)
 *  - revealPositions (default GOLDEN_PLACEMENT or Abacus result)
 *  - originPositions — for displacement (default = initial)
 *  - lockedIds: cells that cannot move (macros)
 *  - snapToSites: if true (default), place snaps x to site and y to row
 *  - allowFloat: if true, place without snap (greedy-snap lab)
 *  - starterHtml, challenges, extraActions(ctx, api), extraMetrics(api)
 *  - fixedMacros: map for legality/algorithm helpers
 */
export function createInteractiveLegalizationLab(root, opts = {}) {
  const locked = new Set(opts.lockedIds || []);
  const snapToSites = opts.snapToSites !== false && !opts.allowFloat;
  const seed = () => clonePositions(opts.initialPositions || OVERLAP_PLACEMENT);
  const revealSeed = () =>
    clonePositions(
      opts.revealPositions ||
        abacusLegalize(opts.initialPositions || OVERLAP_PLACEMENT, {
          fixed: opts.fixedMacros || {},
        })
    );
  const originSeed = () =>
    clonePositions(opts.originPositions || opts.initialPositions || OVERLAP_PLACEMENT);

  let positions = seed();
  let origin = originSeed();
  let selectedId = (opts.cells || CELLS)[0] || "A";
  let revealed = false;

  const fixedOpts = () => ({ fixed: opts.fixedMacros || {} });

  const api = {
    getPositions: () => positions,
    setPositions: (p) => {
      positions = clonePositions(p);
    },
    getOrigin: () => origin,
    setOrigin: (p) => {
      origin = clonePositions(p);
    },
    getSelected: () => selectedId,
    setSelected: (id) => {
      selectedId = id;
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    isLegal: () => isLegal(positions, fixedOpts()),
    legalityReport: () => legalityReport(positions, fixedOpts()),
    displacement: () => totalDisplacement(origin, positions),
    hpwl: () => totalHpwl(positions),
    cost: (lambda = 1) => legalizeCost(positions, origin, lambda),
    getLocked: () => locked,
  };

  function placeSelectedAt(wx, wy) {
    if (locked.has(selectedId)) return;
    if (!positions[selectedId]) return;
    const w = cellWidth(selectedId);
    let x = wx;
    let y = wy;
    if (snapToSites) {
      x = snapX(wx, w);
      y = snapY(wy);
    } else if (opts.allowFloat) {
      x = Math.max(0, Math.min(CHIP_W - w, wx));
      y = Math.max(0, Math.min(CHIP_H - ROW_H, wy));
    }
    positions = { ...positions, [selectedId]: { x, y } };
    revealed = false;
  }

  function nudge(dx, dy) {
    if (locked.has(selectedId)) return;
    const p = positions[selectedId];
    if (!p) return;
    const w = cellWidth(selectedId);
    let x = p.x + dx;
    let y = p.y + dy;
    if (snapToSites) {
      x = snapX(x, w);
      y = snapY(y);
    } else {
      x = Math.max(0, Math.min(CHIP_W - w, x));
      y = Math.max(0, Math.min(CHIP_H - ROW_H, y));
    }
    positions = { ...positions, [selectedId]: { x, y } };
    revealed = false;
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Move cells on the site/row grid, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      (opts.starterHtml ||
        `<p><strong>Your workspace:</strong> select a cell, click the chip to place it on a site/row.
        Challenges check <strong>your</strong> packing. <em>Reveal golden</em> is optional study help.</p>`) +
      (opts.starterExtraHtml || ""),
    loadStarter() {
      positions = seed();
      origin = originSeed();
      revealed = false;
      selectedId = (opts.cells || CELLS)[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        positions = seed();
        origin = originSeed();
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

      const stepX = snapToSites ? SITE_W : 0.5;
      const stepY = snapToSites ? ROW_H : 0.5;

      btns.push(
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "←",
          onClick: () => {
            nudge(-stepX, 0);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "→",
          onClick: () => {
            nudge(stepX, 0);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↑",
          onClick: () => {
            nudge(0, stepY);
            ctx.rerender();
            if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↓",
          onClick: () => {
            nudge(0, -stepY);
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
            origin = originSeed();
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
      const cells = opts.cells || CELLS;
      const highlight = [selectedId, ...((opts.highlight || []) )];

      drawLegalization(ctx.canvas, {
        positions,
        highlight,
      });

      ctx.canvas.onclick = (ev) => {
        const hit = hitLegalCell(positions, ctx.canvas, ev.clientX, ev.clientY, cells);
        if (hit && !ev.shiftKey) {
          selectedId = hit;
          ctx.rerender();
          return;
        }
        const chip = canvasToChip(ctx.canvas, ev.clientX, ev.clientY);
        placeSelectedAt(chip.x, chip.y);
        ctx.rerender();
        if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
      };

      const rep = legalityReport(positions, fixedOpts());
      const lines = [
        `selected: ${selectedId}${locked.has(selectedId) ? " (locked)" : ""}`,
        `legal: ${rep.legal} (${rep.reason})`,
        `disp vs origin: ${totalDisplacement(origin, positions)}`,
        `HPWL: ${totalHpwl(positions)}`,
        revealed ? "view: revealed golden (study)" : "view: your packing",
        `chip ${CHIP_W}×${CHIP_H} · rows ${ROW_YS.join(",")}`,
        "tip: click cell to select · click chip to place · arrows nudge",
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

/** Soft compare of two placements. */
export function positionsNear(a, b, eps = 1e-6) {
  const ids = Object.keys(b);
  if (Object.keys(a).length !== ids.length) return false;
  return ids.every(
    (id) => a[id] && Math.abs(a[id].x - b[id].x) <= eps && Math.abs(a[id].y - b[id].y) <= eps
  );
}

export {
  CELLS,
  CHIP_H,
  CHIP_W,
  FIXED_MACROS,
  FLOAT_PLACEMENT,
  GOLDEN_PLACEMENT,
  GOLDENS,
  OVERLAP_PLACEMENT,
  ROW_H,
  ROW_YS,
  SITE_W,
  WIDTHS,
  abacusLegalize,
  clonePositions,
  detailedLegalize,
  el,
  globalLegalize,
  greedySnap,
  isLegal,
  legalizeCost,
  legalityReport,
  metricsBlock,
  overlapRemoval,
  tetrisLegalize,
  totalDisplacement,
  totalHpwl,
};
