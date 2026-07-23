/**
 * Static timing analysis core — tiny timing graph + levelization.
 * Goldens must match courses/learn_sta/common/graph.py GOLDENS.
 */

export const TINY_TIMING = {
  name: "tiny_sta_chain",
  clock: { name: "clk", period: 10.0 },
  pins: [
    { id: "in", kind: "port" },
    { id: "u1/A", kind: "cell_in", cell: "u1" },
    { id: "u1/Y", kind: "cell_out", cell: "u1" },
    { id: "u2/A", kind: "cell_in", cell: "u2" },
    { id: "u2/Y", kind: "cell_out", cell: "u2" },
    { id: "out", kind: "port" },
  ],
  arcs: [
    { from: "in", to: "u1/A", delay: 0.0, kind: "net" },
    { from: "u1/A", to: "u1/Y", delay: 1.2, kind: "cell" },
    { from: "u1/Y", to: "u2/A", delay: 0.3, kind: "net" },
    { from: "u2/A", to: "u2/Y", delay: 1.5, kind: "cell" },
    { from: "u2/Y", to: "out", delay: 0.2, kind: "net" },
  ],
};

export const GOLDENS = {
  pinCount: 6,
  arcCount: 5,
  cellArcs: 2,
  netArcs: 3,
  maxLevel: 5,
  sources: ["in"],
  sinks: ["out"],
  topo: ["in", "u1/A", "u1/Y", "u2/A", "u2/Y", "out"],
  levels: {
    in: 0,
    "u1/A": 1,
    "u1/Y": 2,
    "u2/A": 3,
    "u2/Y": 4,
    out: 5,
  },
  pathDelay: 3.2,
  cellDelaySum: 2.7,
};

export function cloneTiming(t = TINY_TIMING) {
  return JSON.parse(JSON.stringify(t));
}

export function pinIds(t) {
  return t.pins.map((p) => p.id);
}

export function sources(t) {
  const ids = new Set(pinIds(t));
  for (const a of t.arcs) ids.delete(a.to);
  return [...ids].sort();
}

export function sinks(t) {
  const ids = new Set(pinIds(t));
  for (const a of t.arcs) ids.delete(a.from);
  return [...ids].sort();
}

export function arcKindCounts(t) {
  const counts = {};
  for (const a of t.arcs) counts[a.kind] = (counts[a.kind] || 0) + 1;
  return counts;
}

/** Kahn levelization. Returns pin→level map, or null if cyclic. */
export function levelize(t) {
  const ids = pinIds(t);
  const indeg = Object.fromEntries(ids.map((p) => [p, 0]));
  const succ = {};
  for (const p of ids) succ[p] = [];
  for (const a of t.arcs) {
    if (!(a.from in indeg) || !(a.to in indeg)) {
      throw new Error(`arc endpoint missing pin: ${a.from}→${a.to}`);
    }
    indeg[a.to] += 1;
    succ[a.from].push(a.to);
  }
  const q = ids.filter((p) => indeg[p] === 0);
  const levels = Object.fromEntries(q.map((p) => [p, 0]));
  const order = [];
  while (q.length) {
    const u = q.shift();
    order.push(u);
    for (const v of succ[u]) {
      indeg[v] -= 1;
      levels[v] = Math.max(levels[v] || 0, levels[u] + 1);
      if (indeg[v] === 0) q.push(v);
    }
  }
  if (order.length !== ids.length) return null;
  return levels;
}

export function topoOrder(t) {
  const levels = levelize(t);
  if (!levels) return null;
  return [...pinIds(t)].sort((a, b) => levels[a] - levels[b] || (a < b ? -1 : a > b ? 1 : 0));
}

export function pathDelaySum(t) {
  return Math.round(t.arcs.reduce((s, a) => s + a.delay, 0) * 1e6) / 1e6;
}

export function cellDelaySum(t) {
  return (
    Math.round(
      t.arcs.filter((a) => a.kind === "cell").reduce((s, a) => s + a.delay, 0) * 1e6
    ) / 1e6
  );
}

export function withCycle(t = TINY_TIMING) {
  const c = cloneTiming(t);
  c.arcs.push({ from: "out", to: "in", delay: 0.1, kind: "net" });
  c.name = `${c.name || "tiny"}_cyclic`;
  return c;
}

export function summarize(t) {
  const levels = levelize(t);
  const kinds = arcKindCounts(t);
  return {
    pins: t.pins.length,
    arcs: t.arcs.length,
    cellArcs: kinds.cell || 0,
    netArcs: kinds.net || 0,
    sources: sources(t),
    sinks: sinks(t),
    levels,
    maxLevel: levels ? Math.max(...Object.values(levels)) : null,
    topo: topoOrder(t),
    pathDelay: pathDelaySum(t),
    cellDelaySum: cellDelaySum(t),
    acyclic: levels != null,
  };
}

export function near(a, b, eps = 1e-9) {
  return Math.abs(a - b) < eps;
}
