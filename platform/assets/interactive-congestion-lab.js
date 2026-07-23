/**
 * Interactive congestion lab chrome.
 * Learner moves cells; Check scores demand/overflow from learner positions.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  CAPACITY,
  CELLS,
  CONGESTED_SEED,
  PLACEMENT,
  cellGcell,
  clonePositions,
  congestionMap,
  drawCongestion,
  hitCell,
  canvasToChip,
  overflowMetrics,
  placementFeedbackLite,
  rudyDemand,
  totalHpwl,
} from "./congestion-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

/**
 * opts:
 *  - initialPositions (default CONGESTED_SEED)
 *  - revealPositions (default PLACEMENT)
 *  - capacity, demandFn, heatMode
 *  - starterHtml, challenges, extraActions(ctx, api), extraMetrics(api)
 */
export function createInteractiveCongestionLab(root, opts = {}) {
  const capacity = opts.capacity ?? CAPACITY;
  const demandFn = opts.demandFn || rudyDemand;
  const seed = () => clonePositions(opts.initialPositions || CONGESTED_SEED);
  const revealSeed = () => clonePositions(opts.revealPositions || PLACEMENT);

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
    getDemand: () => demandFn(positions),
    getCongestion: () => congestionMap(demandFn(positions), capacity),
    getOverflow: () => overflowMetrics(demandFn(positions), capacity),
    getHpwl: () => totalHpwl(positions),
    getCapacity: () => capacity,
    cellGcell: (x, y) => cellGcell(x, y),
  };

  function moveSelectedTo(wx, wy) {
    if (!positions[selectedId]) return;
    positions = {
      ...positions,
      [selectedId]: {
        x: Math.max(0, Math.min(11.5, wx)),
        y: Math.max(0, Math.min(7.5, wy)),
      },
    };
    revealed = false;
  }

  function nudge(dx, dy) {
    const p = positions[selectedId];
    if (!p) return;
    moveSelectedTo(p.x + dx, p.y + dy);
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Move cells, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      opts.starterHtml ||
      `<p><strong>Your workspace:</strong> click a cell to select, click empty canvas to move it.
      Challenges score <em>your</em> demand / overflow on the 4×2 GCell grid.</p>`,
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
    })),
    extraActions(ctx) {
      const btns = [];
      for (const id of opts.cells || CELLS) {
        btns.push(
          el("button", {
            className: "btn " + (selectedId === id ? "btn-primary" : "btn-secondary"),
            type: "button",
            text: id,
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
            nudge(-0.5, 0);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "→",
          onClick: () => {
            nudge(0.5, 0);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↑",
          onClick: () => {
            nudge(0, 0.5);
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: "↓",
          onClick: () => {
            nudge(0, -0.5);
            ctx.rerender();
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
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Run feedback",
          onClick: () => {
            positions = placementFeedbackLite(positions, capacity);
            revealed = false;
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
      const demand = demandFn(positions);
      const cong = congestionMap(demand, capacity);
      drawCongestion(ctx.canvas, {
        positions,
        heat: opts.heatMode === "demand" ? demand : cong,
        heatMode: opts.heatMode === "demand" ? "demand" : "cong",
        capacity,
        highlight: [selectedId],
        showNets: opts.showNets !== false,
      });

      ctx.canvas.onclick = (ev) => {
        const hit = hitCell(positions, ctx.canvas, ev.clientX, ev.clientY);
        if (hit && !ev.shiftKey) {
          selectedId = hit;
          ctx.rerender();
          return;
        }
        const world = canvasToChip(ctx.canvas, ev.clientX, ev.clientY);
        moveSelectedTo(world.x, world.y);
        ctx.rerender();
      };

      const ov = overflowMetrics(demand, capacity);
      const gc = cellGcell(positions[selectedId].x, positions[selectedId].y);
      const lines = [
        `selected: ${selectedId} @ GCell (${gc.i},${gc.j})`,
        `HPWL: ${totalHpwl(positions).toFixed(1)}`,
        `overflow total: ${ov.total.toFixed(2)} · max: ${ov.max.toFixed(2)} · count: ${ov.count}`,
        `capacity: ${capacity}`,
        revealed ? "view: revealed golden (study)" : "view: your placement",
      ];
      if (typeof opts.extraMetrics === "function") lines.push(...opts.extraMetrics(api));
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
    },
  });

  return api;
}

export { el, metricsBlock };
