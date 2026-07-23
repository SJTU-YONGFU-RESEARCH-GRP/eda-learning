/**
 * Tiny placement instance for browser labs (6 cells, 6 nets).
 * Coordinates are integer-friendly; HPWL is half-perimeter of the net bbox.
 *
 * Starter (bad) total HPWL = 52; golden-ish compact = 14.
 */

export const CELLS = ["A", "B", "C", "D", "E", "F"];

/** Nets as arrays of cell ids. */
export const NETS = [
  ["A", "B"], // 0
  ["C", "D"], // 1
  ["A", "C"], // 2
  ["B", "D"], // 3
  ["A", "B", "C", "D"], // 4 — 4-pin
  ["E", "F"], // 5
];

/** Criticality weights (net 4 is timing-critical). */
export const NET_WEIGHTS = [1, 1, 1, 1, 5, 1];

/** Spread-out / high-wirelength seed. */
export const STARTER_PLACEMENT = {
  A: { x: 0, y: 0 },
  B: { x: 8, y: 0 },
  C: { x: 0, y: 8 },
  D: { x: 8, y: 8 },
  E: { x: 4, y: 4 },
  F: { x: 0, y: 4 },
};

/** Compact lower-HPWL reference. */
export const GOLDEN_PLACEMENT = {
  A: { x: 2, y: 2 },
  B: { x: 4, y: 2 },
  C: { x: 2, y: 4 },
  D: { x: 4, y: 4 },
  E: { x: 3, y: 3 },
  F: { x: 1, y: 3 },
};

/** Triple overlap at (4,4) for legalization demos. */
export const OVERLAP_PLACEMENT = {
  A: { x: 4, y: 4 },
  B: { x: 4, y: 4 },
  C: { x: 4, y: 4 },
  D: { x: 7, y: 1 },
  E: { x: 1, y: 7 },
  F: { x: 7, y: 7 },
};

/** Pad cells held fixed during analytical / quadratic solves. */
export const FIXED_PADS = ["A", "D"];

/**
 * Numeric goldens for challenges (deterministic defaults of the algos below).
 *
 * | Metric | Starter | Golden / after algo |
 * |--------|---------|---------------------|
 * | HPWL | 52 | golden 14 |
 * | Timing HPWL | 116 | golden 30 |
 * | Force-directed | 52 | ≈18.7 |
 * | Quadratic (pads A,D) | 52 | 48 |
 * | Analytical lite | 52 | ≈48.1 |
 * | SA (seed 42) | 52 | ≈49.6 (best) |
 */
export const GOLDENS = {
  starterHpwl: 52,
  goldenHpwl: 14,
  starterTimingHpwl: 116,
  goldenTimingHpwl: 30,
  cliqueHpwlGolden4pin: 16,
  starHpwlGolden4pinFromA: 8,
  density2x2Cap1StarterOverflow: 2,
  density2x2Cap1GoldenOverflow: 2,
  density2x2Cap2GoldenOverflow: 1,
  forceHpwlAfter: 18.7,
  quadraticHpwlAfter: 48,
  analyticalHpwlAfter: 48.1,
  saHpwlAfter: 49.6,
  saAccepted: 44,
  saRejected: 16,
  spreadMinPairDist: 0.5,
};

export function clonePositions(pos) {
  const out = {};
  for (const [id, p] of Object.entries(pos)) out[id] = { x: p.x, y: p.y };
  return out;
}

/** Half-perimeter wirelength of one net. */
export function hpwl(net, positions) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const id of net) {
    const p = positions[id];
    if (!p) continue;
    if (p.x < minX) minX = p.x;
    if (p.x > maxX) maxX = p.x;
    if (p.y < minY) minY = p.y;
    if (p.y > maxY) maxY = p.y;
  }
  if (!Number.isFinite(minX)) return 0;
  return maxX - minX + (maxY - minY);
}

export function totalHpwl(nets = NETS, positions) {
  return nets.reduce((s, n) => s + hpwl(n, positions), 0);
}

/** Sum of pairwise HPWL (clique model). */
export function cliqueHpwl(net, positions) {
  let s = 0;
  for (let i = 0; i < net.length; i++) {
    for (let j = i + 1; j < net.length; j++) {
      s += hpwl([net[i], net[j]], positions);
    }
  }
  return s;
}

/** Star HPWL: sum of HPWL from hub to every other pin. */
export function starHpwl(net, positions, hub) {
  const h = hub ?? net[0];
  let s = 0;
  for (const id of net) {
    if (id === h) continue;
    s += hpwl([h, id], positions);
  }
  return s;
}

export function timingWeightedHpwl(nets = NETS, positions, weights = NET_WEIGHTS) {
  let s = 0;
  for (let i = 0; i < nets.length; i++) {
    s += (weights[i] ?? 1) * hpwl(nets[i], positions);
  }
  return s;
}

function neighborsOf(nets = NETS) {
  const adj = {};
  for (const id of CELLS) adj[id] = new Set();
  for (const net of nets) {
    for (let i = 0; i < net.length; i++) {
      for (let j = i + 1; j < net.length; j++) {
        adj[net[i]].add(net[j]);
        adj[net[j]].add(net[i]);
      }
    }
  }
  return adj;
}

/**
 * Force-directed place: partial spring pull along net edges + weak center pull.
 * Uses small alpha so a few iters improve HPWL without total collapse.
 */
export function forceDirectedPlace(positions, opts = {}) {
  const nets = opts.nets || NETS;
  const iters = opts.iters ?? 5;
  const alpha = opts.alpha ?? 0.12;
  const centerPull = opts.centerPull ?? 0.02;
  const fixed = new Set(opts.fixed || []);
  const pos = clonePositions(positions);
  const adj = neighborsOf(nets);
  const cx = 4;
  const cy = 4;

  for (let t = 0; t < iters; t++) {
    const next = clonePositions(pos);
    for (const id of CELLS) {
      if (fixed.has(id)) continue;
      const nbs = [...adj[id]];
      if (!nbs.length) continue;
      let sx = 0;
      let sy = 0;
      for (const nb of nbs) {
        sx += pos[nb].x;
        sy += pos[nb].y;
      }
      const tx = sx / nbs.length;
      const ty = sy / nbs.length;
      next[id].x = pos[id].x + alpha * (tx - pos[id].x) + centerPull * (cx - pos[id].x);
      next[id].y = pos[id].y + alpha * (ty - pos[id].y) + centerPull * (cy - pos[id].y);
    }
    for (const id of CELLS) {
      pos[id].x = next[id].x;
      pos[id].y = next[id].y;
    }
  }
  return pos;
}

/**
 * Quadratic-place lite: Gauss–Seidel average of neighbors; pads stay fixed.
 */
export function quadraticPlace(positions, opts = {}) {
  const nets = opts.nets || NETS;
  const iters = opts.iters ?? 6;
  const fixed = new Set(opts.fixed || FIXED_PADS);
  const blend = opts.blend ?? 0.55; // retain some of prior coord (avoids collapse)
  const pos = clonePositions(positions);
  const adj = neighborsOf(nets);

  for (let t = 0; t < iters; t++) {
    for (const id of CELLS) {
      if (fixed.has(id)) continue;
      const nbs = [...adj[id]];
      if (!nbs.length) continue;
      let sx = 0;
      let sy = 0;
      for (const nb of nbs) {
        sx += pos[nb].x;
        sy += pos[nb].y;
      }
      const ax = sx / nbs.length;
      const ay = sy / nbs.length;
      pos[id].x = blend * ax + (1 - blend) * pos[id].x;
      pos[id].y = blend * ay + (1 - blend) * pos[id].y;
    }
  }
  return pos;
}

/**
 * Analytical lite: force/quadratic wirelength stage, then density-repulsion spreading.
 * Goal: cut HPWL vs starter while easing bin overflow vs a pure force collapse.
 */
export function analyticalPlace(positions, opts = {}) {
  const densIters = opts.iters ?? 12;
  const densW = opts.densityWeight ?? 0.55;
  const fixed = new Set(opts.fixed || FIXED_PADS);

  // Wirelength stage (tends to cluster)
  let pos = forceDirectedPlace(positions, {
    iters: opts.forceIters ?? 6,
    alpha: 0.14,
    centerPull: 0.025,
    fixed: [...fixed],
  });
  pos = quadraticPlace(pos, {
    iters: opts.quadIters ?? 3,
    fixed: [...fixed],
    blend: 0.45,
  });

  // Density / spreading stage
  for (let t = 0; t < densIters; t++) {
    const bins = densityBins(pos, { nx: 2, ny: 2, x0: 0, y0: 0, x1: 8, y1: 8 });
    const force = {};
    for (const id of CELLS) force[id] = { x: 0, y: 0 };
    for (const id of CELLS) {
      if (fixed.has(id)) continue;
      const p = pos[id];
      let bx = Math.floor(((p.x - 0) / 8) * 2);
      let by = Math.floor(((p.y - 0) / 8) * 2);
      if (!Number.isFinite(bx) || !Number.isFinite(by)) continue;
      bx = Math.max(0, Math.min(1, bx));
      by = Math.max(0, Math.min(1, by));
      const count = bins.counts[by][bx];
      if (count <= 1) continue;
      const binCx = (bx + 0.5) * 4;
      const binCy = (by + 0.5) * 4;
      let dx = p.x - binCx;
      let dy = p.y - binCy;
      if (Math.abs(dx) + Math.abs(dy) < 1e-6) {
        dx = ((id.charCodeAt(0) * 3) % 5) - 2;
        dy = ((id.charCodeAt(0) * 7) % 5) - 2;
      }
      const len = Math.hypot(dx, dy) || 1;
      force[id].x += densW * (dx / len) * (count - 1) * 0.4;
      force[id].y += densW * (dy / len) * (count - 1) * 0.4;
    }
    for (const id of CELLS) {
      if (fixed.has(id)) continue;
      pos[id].x += force[id].x;
      pos[id].y += force[id].y;
    }
    // Light reconnect so spreading does not explode HPWL
    pos = forceDirectedPlace(pos, {
      iters: 1,
      alpha: 0.06,
      centerPull: 0.01,
      fixed: [...fixed],
    });
  }
  return pos;
}

/** Mulberry32 — deterministic PRNG. */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function rand() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Simulated annealing placement: few random axis jogs; accept/reject on HPWL.
 * Defaults tuned so seed=42 improves the starter instance.
 */
export function saPlace(positions, opts = {}) {
  const nets = opts.nets || NETS;
  const moves = opts.moves ?? 60;
  const t0 = opts.t0 ?? 3;
  const cool = opts.cool ?? 0.94;
  const step = opts.step ?? 1.0;
  const seed = opts.seed ?? 42;
  const rand = mulberry32(seed);
  let pos = clonePositions(positions);
  let cur = totalHpwl(nets, pos);
  let best = clonePositions(pos);
  let bestHpwl = cur;
  let T = t0;
  let accepted = 0;
  let rejected = 0;
  const history = [{ hpwl: cur, T }];

  for (let m = 0; m < moves; m++) {
    const id = CELLS[Math.floor(rand() * CELLS.length)];
    const trial = clonePositions(pos);
    const axis = rand() < 0.5 ? "x" : "y";
    const delta = (rand() < 0.5 ? -1 : 1) * step * (0.5 + rand());
    trial[id] = { x: pos[id].x, y: pos[id].y };
    trial[id][axis] = pos[id][axis] + delta;
    // keep loosely in [−1, 9]
    trial[id].x = Math.max(-1, Math.min(9, trial[id].x));
    trial[id].y = Math.max(-1, Math.min(9, trial[id].y));
    const next = totalHpwl(nets, trial);
    const d = next - cur;
    if (d <= 0 || rand() < Math.exp(-d / Math.max(T, 1e-9))) {
      pos = trial;
      cur = next;
      accepted++;
      if (cur < bestHpwl) {
        bestHpwl = cur;
        best = clonePositions(pos);
      }
    } else {
      rejected++;
    }
    T *= cool;
    if (m % 10 === 9) history.push({ hpwl: cur, T });
  }
  return {
    positions: best,
    hpwl: bestHpwl,
    accepted,
    rejected,
    history,
    finalHpwl: cur,
  };
}

/**
 * Bin density on a regular grid. Default 2×2 over [0,8]×[0,8].
 * @returns {{ counts: number[][], overflow: number, capacity: number, nx, ny }}
 */
export function densityBins(positions, opts = {}) {
  const nx = opts.nx ?? 2;
  const ny = opts.ny ?? 2;
  const x0 = opts.x0 ?? 0;
  const y0 = opts.y0 ?? 0;
  const x1 = opts.x1 ?? 8;
  const y1 = opts.y1 ?? 8;
  const capacity = opts.capacity ?? 1;
  const bw = (x1 - x0) / nx;
  const bh = (y1 - y0) / ny;
  const counts = Array.from({ length: ny }, () => Array(nx).fill(0));

  for (const p of Object.values(positions)) {
    if (!p || !Number.isFinite(p.x) || !Number.isFinite(p.y)) continue;
    let bx = Math.floor((p.x - x0) / bw);
    let by = Math.floor((p.y - y0) / bh);
    if (!Number.isFinite(bx) || !Number.isFinite(by)) continue;
    if (bx < 0) bx = 0;
    if (by < 0) by = 0;
    if (bx >= nx) bx = nx - 1;
    if (by >= ny) by = ny - 1;
    counts[by][bx]++;
  }

  let overflow = 0;
  for (let y = 0; y < ny; y++) {
    for (let x = 0; x < nx; x++) {
      overflow += Math.max(0, counts[y][x] - capacity);
    }
  }
  return { counts, overflow, capacity, nx, ny, bw, bh };
}

/** Min pairwise Euclidean distance among cells. */
export function minPairDistance(positions) {
  const ids = Object.keys(positions);
  let min = Infinity;
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      const a = positions[ids[i]];
      const b = positions[ids[j]];
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if (d < min) min = d;
    }
  }
  return min;
}

/**
 * Spread cells lite: push overlapping / near pairs apart.
 */
export function spreadCells(positions, opts = {}) {
  const minDist = opts.minDist ?? 0.5;
  const iters = opts.iters ?? 40;
  const strength = opts.strength ?? 0.5;
  const pos = clonePositions(positions);

  for (let t = 0; t < iters; t++) {
    for (let i = 0; i < CELLS.length; i++) {
      for (let j = i + 1; j < CELLS.length; j++) {
        const a = CELLS[i];
        const b = CELLS[j];
        const dx = pos[b].x - pos[a].x;
        const dy = pos[b].y - pos[a].y;
        const dist = Math.hypot(dx, dy);
        if (dist >= minDist) continue;
        const push = (minDist - dist) * strength;
        const ux = dist < 1e-9 ? Math.cos((i + j) * 1.7) : dx / dist;
        const uy = dist < 1e-9 ? Math.sin((i + j) * 1.7) : dy / dist;
        pos[a].x -= ux * push * 0.5;
        pos[a].y -= uy * push * 0.5;
        pos[b].x += ux * push * 0.5;
        pos[b].y += uy * push * 0.5;
      }
    }
  }

  // Deterministic pairwise repair until all pairs meet minDist
  for (let pass = 0; pass < 20; pass++) {
    let ok = true;
    for (let i = 0; i < CELLS.length; i++) {
      for (let j = i + 1; j < CELLS.length; j++) {
        const a = CELLS[i];
        const b = CELLS[j];
        const dx = pos[b].x - pos[a].x;
        const dy = pos[b].y - pos[a].y;
        const dist = Math.hypot(dx, dy);
        if (dist >= minDist - 1e-9) continue;
        ok = false;
        const need = (minDist - (dist < 1e-12 ? 0 : dist)) / 2;
        const ux = dist < 1e-12 ? Math.cos((i * 5 + j) * 0.9) : dx / dist;
        const uy = dist < 1e-12 ? Math.sin((i * 5 + j) * 0.9) : dy / dist;
        pos[a].x -= ux * need;
        pos[a].y -= uy * need;
        pos[b].x += ux * need;
        pos[b].y += uy * need;
      }
    }
    if (ok) break;
  }
  return pos;
}

/** Round HPWL-ish metrics for display / soft compares. */
export function round1(n) {
  return Math.round(n * 10) / 10;
}

/** Soft numeric compare for challenge checks. */
export function near(a, b, eps = 0.15) {
  return Math.abs(a - b) <= eps;
}
