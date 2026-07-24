/**
 * Interactive detailed routing lab — learner placement + route + Check.
 */
import {
  CELLS,
  NETS,
  PLACEMENT,
  TRACK_CAPACITY,
  canvasToChip,
  drawDetailedRoute,
  hitCell,
  pinGrid,
  ripupDetailed,
  sequentialDetailed,
  terminalsFromPositions,
  totalHpwl,
  trackOverflow,
  pathTrackUsage,
} from "./detailed-routing-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

export function createInteractiveDetailedRoutingLab(root, opts = {}) {
  const cap = opts.capacity ?? TRACK_CAPACITY;
  const seed = () => structuredClone(opts.initialPositions || PLACEMENT);

  let positions = seed();
  let routes = [];
  let mode = opts.defaultMode || "astar";
  let selectedId = (opts.cells || CELLS)[0] || "A";
  let selectedNet = null;

  function recomputeRoutes(m = mode) {
    const terminals = terminalsFromPositions(positions);
    const result = sequentialDetailed(opts.nets || NETS, terminals, m, cap);
    routes = result.routes;
    return result.usage;
  }

  const api = {
    getPositions: () => positions,
    setPositions: (p) => {
      positions = structuredClone(p);
      routes = [];
    },
    getRoutes: () => routes,
    getUsage: () => {
      const u = {};
      for (const r of routes) {
        for (const [ek, c] of Object.entries(pathTrackUsage(r.segments || []))) {
          u[ek] = (u[ek] || 0) + c;
        }
      }
      return u;
    },
    getOverflow: () => trackOverflow(api.getUsage(), cap),
    getTerminals: () => terminalsFromPositions(positions),
    getMode: () => mode,
    getHpwl: () => totalHpwl(positions, opts.nets || NETS),
    getCapacity: () => cap,
    routeLee: () => {
      mode = "lee";
      recomputeRoutes("lee");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    routeLHV: () => {
      mode = "l_hv";
      recomputeRoutes("l_hv");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    routeLayered: () => {
      mode = "l_hv";
      recomputeRoutes("l_hv");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    routeAstar: () => {
      mode = "astar";
      recomputeRoutes("astar");
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    ripupDetailed: () => {
      if (!routes.length) recomputeRoutes(mode);
      const terminals = terminalsFromPositions(positions);
      routes = ripupDetailed(routes, api.getUsage(), cap, terminals, opts.nets || NETS);
      if (typeof opts.onAfterRoute === "function") opts.onAfterRoute(api);
    },
    clearRoutes: () => {
      routes = [];
    },
    pinGrid: (x, y) => pinGrid(x, y),
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
  }

  function nudge(dx, dy) {
    const p = positions[selectedId];
    if (!p) return;
    moveSelectedTo(p.x + dx, p.y + dy);
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Move cells, route, then <strong>Check</strong>.",
    starterHtml:
      opts.starterHtml ||
      `<p><strong>Your workspace:</strong> twelve-by-eight routing grid. M1 horizontal, M2 vertical.
      Route with Lee, L-HV, or A*. Challenges score <em>your</em> track overflow.</p>`,
    loadStarter() {
      positions = seed();
      routes = [];
      mode = opts.defaultMode || "astar";
      selectedNet = null;
      selectedId = (opts.cells || CELLS)[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        positions = seed();
        routes = [];
        mode = opts.defaultMode || "astar";
        selectedNet = null;
        selectedId = (opts.cells || CELLS)[0] || "A";
        if (typeof ch.setup === "function") ch.setup(ctx, api);
      },
      check: (ctx) => (typeof ch.check === "function" ? !!ch.check(ctx, api) : false),
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
        el("button", { className: "btn btn-ghost", type: "button", text: "←", onClick: () => { nudge(-0.5, 0); ctx.rerender(); } }),
        el("button", { className: "btn btn-ghost", type: "button", text: "→", onClick: () => { nudge(0.5, 0); ctx.rerender(); } }),
        el("button", { className: "btn btn-ghost", type: "button", text: "↑", onClick: () => { nudge(0, 0.5); ctx.rerender(); } }),
        el("button", { className: "btn btn-ghost", type: "button", text: "↓", onClick: () => { nudge(0, -0.5); ctx.rerender(); } }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route Lee",
          onClick: () => { api.routeLee(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route layered",
          onClick: () => { api.routeLayered(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Route A*",
          onClick: () => { api.routeAstar(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Rip-up detailed",
          onClick: () => { if (!routes.length) api.routeLayered(); api.ripupDetailed(); ctx.rerender(); },
        })
      );
      if (typeof opts.extraActions === "function") btns.push(...(opts.extraActions(ctx, api) || []));
      return btns;
    },
    renderWorkspace(ctx) {
      const usage = api.getUsage();
      drawDetailedRoute(ctx.canvas, {
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
      const ov = trackOverflow(usage, cap);
      const pg = pinGrid(positions[selectedId].x, positions[selectedId].y);
      const lines = [
        `selected: ${selectedId} @ grid (${pg.x},${pg.y})`,
        `routes: ${routes.some((r) => r.segments?.length) ? routes.filter((r) => r.segments?.length).length + " nets" : "(none — click Route)"}`,
        `overflow total: ${ov.total.toFixed(2)} · max: ${ov.max.toFixed(2)} · count: ${ov.count}`,
        `track capacity: ${cap} · mode: ${mode}`,
        `HPWL: ${totalHpwl(positions, opts.nets || NETS).toFixed(1)}`,
      ];
      if (typeof opts.extraMetrics === "function") lines.push(...opts.extraMetrics(api));
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
    },
  });

  return api;
}

export { el, metricsBlock };
