/**
 * Interactive clock tree synthesis lab — learner placement + tree build + Check.
 */
import {
  CELLS,
  PLACEMENT,
  CLOCK_SOURCE,
  canvasToPoint,
  drawClockTree,
  hitSink,
  hTree,
  mmmTree,
  zeroSkewMerge,
  insertBuffers,
  sequentialCts,
  skew,
  latency,
  tappingPoints,
  skewBoundOk,
  bufferedLatencies,
  sinkPoints,
  clonePositions,
  GOLDENS,
} from "./clock-tree-core.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

export function createInteractiveClockTreeLab(root, opts = {}) {
  const seed = () => clonePositions(opts.initialPositions || PLACEMENT);
  const skewBound = opts.skewBound ?? GOLDENS.skewBoundDefault;
  const maxWireLen = opts.maxWireLen ?? GOLDENS.maxWireLenDefault;

  let positions = seed();
  let tree = null;
  let treeMode = null;
  let selectedId = (opts.cells || CELLS)[0] || "A";

  const api = {
    getPositions: () => positions,
    setPositions: (p) => {
      positions = clonePositions(p);
      tree = null;
      treeMode = null;
    },
    getTree: () => tree,
    setTree: (t, mode = "custom") => {
      tree = t;
      treeMode = mode;
    },
    getTreeMode: () => treeMode,
    getSelected: () => selectedId,
    setSelected: (id) => {
      selectedId = id;
    },
    getSkew: () => (tree ? skew(tree, positions) : Infinity),
    getLatency: (id) => (tree ? latency(tree, id, positions) : Infinity),
    getSinks: () => sinkPoints(positions),
    getSource: () => ({ ...CLOCK_SOURCE }),
    getSkewBound: () => skewBound,
    getMaxWireLen: () => maxWireLen,
    buildHTree: () => {
      tree = hTree(positions);
      treeMode = "h-tree";
      if (typeof opts.onAfterBuild === "function") opts.onAfterBuild(api);
    },
    buildMMM: () => {
      tree = mmmTree(positions);
      treeMode = "mmm";
      if (typeof opts.onAfterBuild === "function") opts.onAfterBuild(api);
    },
    zeroSkewMergeDemo: () => {
      tree = zeroSkewMerge(positions);
      treeMode = "zero-skew";
      if (typeof opts.onAfterBuild === "function") opts.onAfterBuild(api);
    },
    insertBuffers: () => {
      if (!tree) tree = hTree(positions);
      tree = insertBuffers(tree, maxWireLen);
      treeMode = treeMode ? `${treeMode}+buf` : "buffered";
      if (typeof opts.onAfterBuild === "function") opts.onAfterBuild(api);
    },
    sequentialCts: () => {
      tree = sequentialCts(positions, opts.ctsOrder || CELLS);
      treeMode = "sequential";
      if (typeof opts.onAfterBuild === "function") opts.onAfterBuild(api);
    },
    clearTree: () => {
      tree = null;
      treeMode = null;
    },
    tappingPoints: () => (tree ? tappingPoints(tree) : []),
    skewBoundOk: () => (tree ? skewBoundOk(tree, skewBound, positions) : false),
    bufferedLatencies: () => (tree ? bufferedLatencies(tree, positions) : {}),
  };

  function moveSelectedTo(wx, wy) {
    if (!positions[selectedId]) return;
    positions = {
      ...positions,
      [selectedId]: {
        x: Math.max(0, Math.min(CHIP_MAX_X, wx)),
        y: Math.max(0, Math.min(CHIP_MAX_Y, wy)),
      },
    };
    tree = null;
    treeMode = null;
  }

  function nudge(dx, dy) {
    const p = positions[selectedId];
    if (!p) return;
    moveSelectedTo(p.x + dx, p.y + dy);
  }

  const CHIP_MAX_X = 11.5;
  const CHIP_MAX_Y = 7.5;

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Move sinks, build a clock tree, then <strong>Check</strong>.",
    starterHtml:
      opts.starterHtml ||
      `<p><strong>Your workspace:</strong> twelve-by-eight chip with clock source at (${CLOCK_SOURCE.x},${CLOCK_SOURCE.y}).
      Build H-tree, MMM, zero-skew merge, insert buffers, or sequential CTS. Challenges score <em>your</em> tree skew.</p>`,
    loadStarter() {
      positions = seed();
      tree = null;
      treeMode = null;
      selectedId = (opts.cells || CELLS)[0] || "A";
      if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        positions = seed();
        tree = null;
        treeMode = null;
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
          text: "Build H-tree",
          onClick: () => { api.buildHTree(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Build MMM",
          onClick: () => { api.buildMMM(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Zero-skew merge demo",
          onClick: () => { api.zeroSkewMergeDemo(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Insert buffers",
          onClick: () => { api.insertBuffers(); ctx.rerender(); },
        }),
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Sequential CTS",
          onClick: () => { api.sequentialCts(); ctx.rerender(); },
        })
      );
      if (typeof opts.extraActions === "function") btns.push(...(opts.extraActions(ctx, api) || []));
      return btns;
    },
    renderWorkspace(ctx) {
      drawClockTree(ctx.canvas, {
        positions,
        tree: tree || { source: CLOCK_SOURCE, sinks: sinkPoints(positions), edges: [], steiners: [], buffers: [] },
        selectedSink: selectedId,
        highlight: [selectedId],
        showSkew: true,
      });
      ctx.canvas.onclick = (ev) => {
        const hit = hitSink(positions, ctx.canvas, ev.clientX, ev.clientY);
        if (hit && !ev.shiftKey) {
          selectedId = hit;
          ctx.rerender();
          return;
        }
        const world = canvasToPoint(ctx.canvas, ev.clientX, ev.clientY);
        moveSelectedTo(world.x, world.y);
        ctx.rerender();
      };
      const lines = [
        `selected sink: ${selectedId} @ (${positions[selectedId].x.toFixed(1)},${positions[selectedId].y.toFixed(1)})`,
        `tree: ${tree?.edges?.length ? treeMode || "built" : "(none — click Build)"}`,
        `skew: ${tree?.edges?.length ? api.getSkew().toFixed(2) : "—"}`,
        `latency ${selectedId}: ${tree?.edges?.length ? api.getLatency(selectedId).toFixed(2) : "—"}`,
        `skew bound: ${skewBound} · max wire: ${maxWireLen}`,
      ];
      if (typeof opts.extraMetrics === "function") lines.push(...opts.extraMetrics(api));
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
    },
  });

  return api;
}

export { el, metricsBlock };
