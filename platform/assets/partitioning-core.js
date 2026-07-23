/**
 * partitioning-core.js — bipartition / multiway helpers for learn_partitioning labs.
 * Reuses cutsize, KL, FM, spectral, hyperedgeCut from clustering-core.js.
 */
import {
  BAD_SEED,
  TINY_GRAPH,
  TINY_HYPERGRAPH,
  adjacency,
  cutsize,
  fiducciaMattheyses,
  greedyPairMerge,
  hyperedgeCut,
  hyperedgesToPairEdges,
  partsString,
  spectralBisection,
} from "./clustering-core.js";

export { BAD_SEED, TINY_GRAPH, TINY_HYPERGRAPH, cutsize, hyperedgeCut, hyperedgesToPairEdges, partsString };

/** Deterministic LCG for reproducible "random" bipartitions. */
export function mulberry32(seed) {
  let t = seed >>> 0;
  return function next() {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

/** Part → total size (default size 1). */
export function partSizes(assignment, sizes = null) {
  const out = {};
  for (const [n, p] of Object.entries(assignment)) {
    const s = sizes?.[n] ?? 1;
    out[p] = (out[p] || 0) + s;
  }
  return out;
}

/**
 * Balance for a bipartition: ratio = min/max ∈ (0,1], imbalance = |s0-s1|/total.
 * Returns null fields if not exactly two parts.
 */
export function balanceMetrics(assignment, sizes = null) {
  const ps = partSizes(assignment, sizes);
  const labs = Object.keys(ps).sort();
  if (labs.length !== 2) {
    return { parts: ps, labels: labs, ratio: null, imbalance: null, sizes: null };
  }
  const s0 = ps[labs[0]];
  const s1 = ps[labs[1]];
  const total = s0 + s1;
  const lo = Math.min(s0, s1);
  const hi = Math.max(s0, s1);
  return {
    parts: ps,
    labels: labs,
    sizes: [s0, s1],
    ratio: lo / hi,
    imbalance: Math.abs(s0 - s1) / total,
  };
}

/** Golden balanced bipartition on TINY_GRAPH (cut 3). */
export const GOLDEN_BIPART = { A: "0", B: "0", C: "0", D: "1", E: "1" };

/**
 * Random bipartition aiming for roughly half the nodes on each side.
 * Seed 7 on TINY_GRAPH yields AE|BCD (same shape as BAD_SEED) — cut 12.
 */
export function randomBipartition(nodes, seed = 7) {
  const rng = mulberry32(seed);
  const shuffled = [...nodes].sort((a, b) => {
    const ra = rng();
    const rb = rng();
    return ra - rb || (a < b ? -1 : 1);
  });
  const half = Math.floor(nodes.length / 2);
  const left = new Set(shuffled.slice(0, half));
  return Object.fromEntries(nodes.map((n) => [n, left.has(n) ? "0" : "1"]));
}

/**
 * Greedy initial bipartition: start with heaviest edge on side 0,
 * then place remaining nodes to the side that adds less cut weight.
 */
export function greedyInitialBipartition(nodes, edges) {
  if (nodes.length < 2) return Object.fromEntries(nodes.map((n) => [n, "0"]));
  const sorted = [...edges].sort(
    (a, b) => b.w - a.w || (a.u < b.u ? -1 : 1) || (a.v < b.v ? -1 : 1)
  );
  const { u: u0, v: v0 } = sorted[0];
  const asn = Object.fromEntries(nodes.map((n) => [n, null]));
  asn[u0] = "0";
  asn[v0] = "0";
  const adj = adjacency(edges);
  const rest = nodes.filter((n) => asn[n] == null).sort();
  // Seed side 1 with the unplaced node of highest affinity to the other side later;
  // first place one node on side 1 for balance.
  if (rest.length) {
    const first = rest[0];
    asn[first] = "1";
    rest.shift();
  }
  for (const n of rest) {
    let add0 = 0;
    let add1 = 0;
    for (const [nbr, w] of Object.entries(adj[n] || {})) {
      if (asn[nbr] === "0") add0 += w;
      else if (asn[nbr] === "1") add1 += w;
    }
    // Prefer the side where more weight is already internal (less cut added).
    asn[n] = add0 >= add1 ? "0" : "1";
  }
  return asn;
}

/**
 * Grow a bipartition from a seed node: BFS by heaviest neighbor until half filled.
 */
export function growBipartition(nodes, edges, seedNode) {
  const adj = adjacency(edges);
  const target = Math.floor(nodes.length / 2);
  const left = new Set([seedNode]);
  while (left.size < target) {
    let best = null;
    for (const u of left) {
      for (const [v, w] of Object.entries(adj[u] || {})) {
        if (left.has(v)) continue;
        if (!best || w > best.w || (w === best.w && v < best.v)) best = { v, w };
      }
    }
    if (!best) {
      const leftover = nodes.find((n) => !left.has(n));
      if (!leftover) break;
      left.add(leftover);
    } else {
      left.add(best.v);
    }
  }
  return Object.fromEntries(nodes.map((n) => [n, left.has(n) ? "0" : "1"]));
}

/** Induced subgraph on a node subset (edge endpoints both inside). */
export function inducedSubgraph(nodes, edges, sizes) {
  const set = new Set(nodes);
  return {
    nodes: [...nodes],
    edges: edges.filter((e) => set.has(e.u) && set.has(e.v)),
    sizes: Object.fromEntries(nodes.map((n) => [n, sizes?.[n] ?? 1])),
  };
}

/**
 * Recursive bisection to targetK parts.
 * Always bisects the largest part via spectral; returns assignment + history.
 */
export function recursiveBisection(nodes, edges, sizes, targetK = 3) {
  const sz = sizes || Object.fromEntries(nodes.map((n) => [n, 1]));
  let nextLabel = 0;
  let assignment = Object.fromEntries(nodes.map((n) => [n, String(nextLabel)]));
  nextLabel = 1;
  const history = [{ step: 0, event: "start", parts: partsString(assignment), cut: cutsize(assignment, edges) }];

  function largestPart() {
    const groups = {};
    for (const n of nodes) {
      const p = assignment[n];
      (groups[p] ||= []).push(n);
    }
    let bestLab = null;
    let bestNodes = [];
    for (const [lab, mem] of Object.entries(groups)) {
      if (
        mem.length > bestNodes.length ||
        (mem.length === bestNodes.length && (bestLab == null || lab < bestLab))
      ) {
        bestLab = lab;
        bestNodes = mem;
      }
    }
    return { lab: bestLab, members: bestNodes.sort() };
  }

  let step = 1;
  while (new Set(Object.values(assignment)).size < targetK) {
    const { lab, members } = largestPart();
    if (members.length < 2) break;
    const sub = inducedSubgraph(members, edges, sz);
    const { assignment: bip } = spectralBisection(sub.nodes, sub.edges, sub.sizes);
    const newLab = String(nextLabel++);
    for (const n of members) {
      if (bip[n] === "1") assignment[n] = newLab;
      else assignment[n] = lab;
    }
    history.push({
      step,
      event: `bisect part ${lab}`,
      split: members.join(""),
      parts: partsString(assignment),
      cut: cutsize(assignment, edges),
      k: new Set(Object.values(assignment)).size,
    });
    step++;
  }
  return { assignment, history };
}

/**
 * Flat multiway literacy: assign nodes to k buckets by spectral recursive result,
 * or a simple round-robin baseline for contrast.
 */
export function roundRobinMultiway(nodes, k) {
  const sorted = [...nodes].sort();
  return Object.fromEntries(sorted.map((n, i) => [n, String(i % k)]));
}

/**
 * Terminal propagation: fixed terminals keep their side; free nodes take the
 * side of the neighboring terminal (or assigned) with highest affinity weight.
 * Iterates until stable (small graphs).
 */
export function terminalPropagation(nodes, edges, terminals) {
  // terminals: { node: "0"|"1", ... }
  const asn = Object.fromEntries(nodes.map((n) => [n, terminals[n] != null ? String(terminals[n]) : null]));
  const adj = adjacency(edges);
  const free = nodes.filter((n) => asn[n] == null).sort();
  let changed = true;
  let iters = 0;
  const history = [];
  while (changed && iters < 20) {
    changed = false;
    iters++;
    for (const n of free) {
      let w0 = 0;
      let w1 = 0;
      for (const [nbr, w] of Object.entries(adj[n] || {})) {
        if (asn[nbr] === "0") w0 += w;
        else if (asn[nbr] === "1") w1 += w;
      }
      if (w0 === 0 && w1 === 0) continue;
      const next = w0 >= w1 ? "0" : "1";
      if (asn[n] !== next) {
        asn[n] = next;
        changed = true;
      }
    }
    history.push({
      iter: iters,
      assignment: { ...asn },
      cut: cutsize(
        Object.fromEntries(nodes.map((n) => [n, asn[n] ?? "?"])),
        edges.filter((e) => asn[e.u] != null && asn[e.v] != null)
      ),
    });
  }
  // Any still-null free node: put on smaller side
  for (const n of free) {
    if (asn[n] != null) continue;
    const s0 = nodes.filter((u) => asn[u] === "0").length;
    const s1 = nodes.filter((u) => asn[u] === "1").length;
    asn[n] = s0 <= s1 ? "0" : "1";
  }
  return { assignment: asn, history, iters, terminals: { ...terminals } };
}

/**
 * Multilevel V-cycle with explicit stages for literacy labs.
 * coarsen (greedy→2) → partition (identity on coarse) → project → FM refine.
 */
export function multilevelVCycle(nodes, edges, sizes, coarseK = 2) {
  const { assignment: coarse, mergeLog } = greedyPairMerge(nodes, edges, sizes, coarseK);
  const labs = [...new Set(Object.values(coarse))].sort();
  const stages = {
    coarsen: { assignment: { ...coarse }, labels: labs, mergeLog },
  };

  let projected;
  if (labs.length === 2) {
    projected = Object.fromEntries(nodes.map((n) => [n, coarse[n] === labs[0] ? "0" : "1"]));
  } else {
    projected = Object.fromEntries(nodes.map((n, i) => [n, String(i % 2)]));
  }
  stages.project = {
    assignment: { ...projected },
    cut: cutsize(projected, edges),
    parts: partsString(projected),
  };

  const { assignment: refined, history: fmHist } = fiducciaMattheyses(nodes, edges, projected);
  stages.refine = {
    assignment: { ...refined },
    cut: cutsize(refined, edges),
    parts: partsString(refined),
    fmHistory: fmHist,
  };

  const finalAsn = Object.fromEntries(nodes.map((n) => [n, `P${refined[n]}`]));
  stages.final = {
    assignment: finalAsn,
    cut: cutsize(finalAsn, edges),
    parts: partsString(finalAsn),
  };

  return { stages, assignment: finalAsn };
}

/** Hypergraph bipartition via clique-expansion + FM from a seed. */
export function hypergraphBipartition(nodes, hedges, initial) {
  const edges = hyperedgesToPairEdges(hedges);
  const { assignment, history } = fiducciaMattheyses(nodes, edges, initial);
  return {
    assignment,
    history,
    hyperCut: hyperedgeCut(assignment, hedges),
    pairCut: cutsize(assignment, edges),
  };
}
