/**
 * Static timing analysis core — timing graph, arrival/required, slack, path, incremental.
 * Goldens must match courses/learn_sta/common/ (graph.py + propagate.py).
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

/** Graph-construction goldens */
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

/**
 * Propagation goldens on TINY_TIMING with arrival(in)=0, setup required(out)=period.
 * Hold required(out)=0 (same-edge lite).
 */
export const PROP_GOLDENS = {
  period: 10.0,
  arrival: {
    in: 0,
    "u1/A": 0,
    "u1/Y": 1.2,
    "u2/A": 1.5,
    "u2/Y": 3.0,
    out: 3.2,
  },
  requiredSetup: {
    out: 10.0,
    "u2/Y": 9.8,
    "u2/A": 8.3,
    "u1/Y": 8.0,
    "u1/A": 6.8,
    in: 6.8,
  },
  setupSlackOut: 6.8, // 10 - 3.2
  holdSlackOut: 3.2, // 3.2 - 0
  criticalPath: ["in", "u1/A", "u1/Y", "u2/A", "u2/Y", "out"],
  // After bumping u1/A→u1/Y delay 1.2 → 2.0:
  incremental: {
    editFrom: "u1/A",
    editTo: "u1/Y",
    newDelay: 2.0,
    arrivalOut: 4.0,
    setupSlackOut: 6.0,
    invalidated: ["u1/Y", "u2/A", "u2/Y", "out"],
  },
  // False-path disables the whole chain endpoint for setup:
  falsePath: {
    arcs: [["u1/Y", "u2/A"]],
    setupSlackOut: null, // not timed
  },
  // Multicycle setup=2 → required = 2*period
  multicycle: {
    setupCycles: 2,
    requiredOut: 20.0,
    setupSlackOut: 16.8,
  },
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

export function near(a, b, eps = 1e-9) {
  return Math.abs(a - b) < eps;
}

export function round6(x) {
  return Math.round(x * 1e6) / 1e6;
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
  return [...pinIds(t)].sort(
    (a, b) => levels[a] - levels[b] || (a < b ? -1 : a > b ? 1 : 0)
  );
}

export function pathDelaySum(t) {
  return round6(t.arcs.reduce((s, a) => s + a.delay, 0));
}

export function cellDelaySum(t) {
  return round6(
    t.arcs.filter((a) => a.kind === "cell").reduce((s, a) => s + a.delay, 0)
  );
}

export function withCycle(t = TINY_TIMING) {
  const c = cloneTiming(t);
  c.arcs.push({ from: "out", to: "in", delay: 0.1, kind: "net" });
  c.name = `${c.name || "tiny"}_cyclic`;
  return c;
}

function preds(t, pin, disabled) {
  return t.arcs.filter(
    (a) => a.to === pin && !disabled.has(`${a.from}|${a.to}`)
  );
}

function succs(t, pin, disabled) {
  return t.arcs.filter(
    (a) => a.from === pin && !disabled.has(`${a.from}|${a.to}`)
  );
}

/**
 * @param {object} t
 * @param {object} [opts]
 * @param {Record<string,number>} [opts.arrivalAt] — seed arrivals (default sources=0)
 * @param {Set<string>|string[]} [opts.disableArcs] — "from|to"
 */
export function propagateArrival(t, opts = {}) {
  const order = topoOrder(t);
  if (!order) return null;
  const disabled = new Set(opts.disableArcs || []);
  const arr = {};
  for (const p of sources(t)) arr[p] = opts.arrivalAt?.[p] ?? 0;
  if (opts.arrivalAt) {
    for (const [p, v] of Object.entries(opts.arrivalAt)) arr[p] = v;
  }
  for (const p of order) {
    if (arr[p] != null) continue;
    const incoming = preds(t, p, disabled);
    if (!incoming.length) {
      arr[p] = opts.arrivalAt?.[p] ?? 0;
      continue;
    }
    let best = -Infinity;
    for (const a of incoming) {
      if (arr[a.from] == null) continue;
      best = Math.max(best, arr[a.from] + a.delay);
    }
    arr[p] = best === -Infinity ? 0 : round6(best);
  }
  return arr;
}

/**
 * Backward required for setup. Sink required = period * setupCycles (default 1).
 * Hold lite: use requiredAt sinks = 0 via opts.
 */
export function propagateRequired(t, opts = {}) {
  const order = topoOrder(t);
  if (!order) return null;
  const disabled = new Set(opts.disableArcs || []);
  const period = t.clock?.period ?? 10;
  const cycles = opts.setupCycles ?? 1;
  const snk = sinks(t);
  const req = {};
  for (const p of snk) {
    if (opts.requiredAt?.[p] != null) req[p] = opts.requiredAt[p];
    else if (opts.mode === "hold") req[p] = 0;
    else req[p] = round6(period * cycles);
  }
  if (opts.requiredAt) {
    for (const [p, v] of Object.entries(opts.requiredAt)) req[p] = v;
  }
  for (let i = order.length - 1; i >= 0; i--) {
    const p = order[i];
    if (req[p] != null) continue;
    const outgoing = succs(t, p, disabled);
    if (!outgoing.length) continue;
    let best = Infinity;
    for (const a of outgoing) {
      if (req[a.to] == null) continue;
      best = Math.min(best, req[a.to] - a.delay);
    }
    if (best !== Infinity) req[p] = round6(best);
  }
  return req;
}

export function setupSlack(arr, req, pin) {
  if (arr?.[pin] == null || req?.[pin] == null) return null;
  return round6(req[pin] - arr[pin]);
}

export function holdSlack(arr, reqHold, pin) {
  if (arr?.[pin] == null || reqHold?.[pin] == null) return null;
  return round6(arr[pin] - reqHold[pin]);
}

/** Trace critical (worst) path into `pin` using arrival tags. */
export function criticalPathTo(t, arr, pin) {
  if (!arr || arr[pin] == null) return null;
  const path = [pin];
  let cur = pin;
  const guard = pinIds(t).length + 2;
  for (let i = 0; i < guard; i++) {
    const incoming = t.arcs.filter((a) => a.to === cur);
    if (!incoming.length) break;
    let best = null;
    for (const a of incoming) {
      if (arr[a.from] == null) continue;
      const cand = round6(arr[a.from] + a.delay);
      if (near(cand, arr[cur]) && (best == null || arr[a.from] >= arr[best.from])) {
        best = a;
      }
    }
    if (!best) break;
    path.push(best.from);
    cur = best.from;
  }
  return path.reverse();
}

/** Downstream cone including start pin (BFS on successors). */
export function fanoutCone(t, startPin) {
  const seen = new Set([startPin]);
  const q = [startPin];
  while (q.length) {
    const u = q.shift();
    for (const a of t.arcs) {
      if (a.from === u && !seen.has(a.to)) {
        seen.add(a.to);
        q.push(a.to);
      }
    }
  }
  return [...seen];
}

/**
 * Edit one arc delay, invalidate fanout of the arc's `to`, recompute arrivals on the cone.
 */
export function incrementalArrival(t, edit, baseArr) {
  const tt = cloneTiming(t);
  const arc = tt.arcs.find((a) => a.from === edit.from && a.to === edit.to);
  if (!arc) throw new Error(`missing arc ${edit.from}→${edit.to}`);
  arc.delay = edit.delay;
  const invalidated = fanoutCone(tt, edit.to);
  const arr = { ...baseArr };
  for (const p of invalidated) delete arr[p];
  const order = topoOrder(tt);
  const disabled = new Set();
  for (const p of order) {
    if (!invalidated.includes(p) && arr[p] != null) continue;
    if (sources(tt).includes(p) && arr[p] == null) arr[p] = 0;
    const incoming = preds(tt, p, disabled);
    if (!incoming.length) {
      if (arr[p] == null) arr[p] = 0;
      continue;
    }
    let best = -Infinity;
    for (const a of incoming) {
      if (arr[a.from] == null) continue;
      best = Math.max(best, arr[a.from] + a.delay);
    }
    arr[p] = best === -Infinity ? 0 : round6(best);
  }
  return { timing: tt, arrival: arr, invalidated };
}

export function analyzeSetup(t, opts = {}) {
  const arr = propagateArrival(t, opts);
  const req = propagateRequired(t, { ...opts, mode: "setup" });
  if (!arr || !req) return null;
  const snk = sinks(t)[0];
  const slack = setupSlack(arr, req, snk);
  return {
    arrival: arr,
    required: req,
    slackAtSink: slack,
    path: slack == null ? null : criticalPathTo(t, arr, snk),
    sink: snk,
  };
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
