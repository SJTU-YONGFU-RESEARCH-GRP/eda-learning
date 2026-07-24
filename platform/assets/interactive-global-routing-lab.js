/**
 * Interactive global routing lab chrome.
 * Learner moves cells; routes score edge overflow from learner positions.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  CELLS,
  CLUSTER_SEED,
  EDGE_CAPACITY,
  NETS,
  PLACEMENT,
  cellGcell,
  clonePositions,
  drawGlobalRoute,
  edgeOverflow,
  hitCell,
  canvasToChip,
  ripupReroute,
  routeAllL,
  routeAllMaze,
  terminalsFromPositions,
  totalHpwl,
  usageFromRoutes,
} from "./global-routing-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

/**
 * opts:
 *  - initialPositions (default PLACEMENT)
 *  - revealPositions (default CLUSTER_SEED)
 *  - starterHtml, challenges, extraActions(ctx, api), extraMetrics(api)
 *  - onLoadStarter, onAfterRoute
 */
export function createInteractiveGlobalRoutingLab(root, opts = {}) {
  const cap = opts.capacity ?? EDGE_CAPACITY;
  const seed = () => clonePositions(opts.initialPositions || PLACEMENT);
  const revealSeed = () => clonePositions(opts.revealPositions || CLUSTER_SEED);

  let positions = seed();
  let routes = [];
  let prefer = "HV";
  let selectedId = (opts.cells || CELLS)[0] || "A";
  let selectedNet = null;
  let revealed = false;

  function recomputeRoutes(mode = "l") {
    const terminals = terminalsFromPositions(positions);
    if (mode === "maze") {
      routes = routeAllMaze(opts.nets || NETS, terminals, cap);
    } else {
      routes = routeAllL(opts.nets || NETS, terminals, prefer);
    }
    revealed = false;
  }

  const api = {
    getPositions: () => positions,
    setPositions: (p) => {
      positions = clonePositions(p);
      routes = [];
    },
    getRoutes: () => routes,
    setRoutes: (r) => {
      routes = r;
    },
    getUsage: () => usageFromRoutes(routes),
    getOverflow: () => edgeOverflow(usageFromRoutes(routes), cap),
    getTerminals: () => terminalsFromPositions(positions),
    getPrefer: () => prefer,
    setPrefer: (p) => {
      prefer = p === "VH" ? "VH" : "HV";
    },
    getSelected: () => selectedId,
    setSelected: (id) => {
      selectedId = id;
    },
    getSelectedNet: () => selectedNet,
    setSelectedNet: (n) => {
      selectedNet = n;
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    getHpwl: () => totalHpwl(positions, opts.nets || NETS),
    getCapacity: () => cap,
    cellGcell: (x, y) => cellGcell(x, y),
    routeLHV: () => {
      prefer = "HV";
      recomputeRoutes("l");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    routeLVH: () => {
      prefer = "VH";
      recomputeRoutes("l");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    routeMaze: () => {
      recomputeRoutes("maze");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    ripupReroute: () => {
      const terminals = terminalsFromPositions(positions);
      const usage = usageFromRoutes(routes);
      routes = ripupReroute(routes, usage, cap, terminals, opts.nets || NETS);
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    clearRoutes: () => {
      routes = [];
    },
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
    routes = [];
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
      "Pick a challenge and click <strong>Start</strong>. Move cells, route, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      opts.starterHtml ||
      `<p><strong>Your workspace:</strong> click a cell to select, click empty canvas to move it.
      Route with L-HV, L-VH, maze, or rip-up reroute. Challenges score <em>your</em> edge overflow.</p>`,
    loadStarter() {
      positions = seed();
      routes = [];
      prefer = "HV";
      revealed = false;
      selectedNet = null;
      selectedId = (opts.cells || CELLS)[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        positions = seed();
        routes = [];
        prefer = "HV";
        revealed = false;
        selectedNet = null;
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
            routes = [];
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
            routes = [];
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route L-HV",
          onClick: () => {
            api.routeLHV();
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route L-VH",
          onClick: () => {
            api.routeLVH();
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route maze",
          onClick: () => {
            api.routeMaze();
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Rip-up reroute",
          onClick: () => {
            if (!routes.length) api.routeLHV();
            api.ripupReroute();
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
      const usage = usageFromRoutes(routes);
      drawGlobalRoute(ctx.canvas, {
        positions,
        usage,
        routes,
        cap,
        highlight: [selectedId],
        selectedNet,
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

      const ov = edgeOverflow(usage, cap);
      const gc = cellGcell(positions[selectedId].x, positions[selectedId].y);
      const lines = [
        `selected: ${selectedId} @ GCell (${gc.i},${gc.j})`,
        `routes: ${routes.length ? routes.length + " nets" : "(none — click Route)"}`,
        `overflow total: ${ov.total.toFixed(2)} · max: ${ov.max.toFixed(2)} · count: ${ov.count}`,
        `edge capacity: ${cap}`,
        `HPWL: ${totalHpwl(positions, opts.nets || NETS).toFixed(1)}`,
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
