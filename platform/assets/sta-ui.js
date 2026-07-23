/**
 * STA canvas helpers + re-export of challenge chrome from clustering-ui.
 */
import { fitHiDpiCanvas, LAB_CANVAS_CSS_HEIGHT } from "./canvas-hires.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";

export { createChallengeLab, el, metricsBlock };

const KIND_FILL = {
  port: "#2a6f6a",
  cell_in: "#3d5a80",
  cell_out: "#6b4c9a",
  default: "#4a5568",
};

/**
 * Compute pin screen positions for a timing DAG (same layout as drawTimingGraph).
 * @returns {Record<string,{x:number,y:number,pin:object}>}
 */
export function pinPositions(canvas, timing, levels = null) {
  const w = canvas.clientWidth || 640;
  const h = canvas.clientHeight || LAB_CANVAS_CSS_HEIGHT;
  const pins = timing.pins;
  const byLevel = {};
  for (const p of pins) {
    const lv = levels ? levels[p.id] ?? 0 : pins.indexOf(p);
    if (!byLevel[lv]) byLevel[lv] = [];
    byLevel[lv].push(p);
  }
  const levelKeys = Object.keys(byLevel)
    .map(Number)
    .sort((a, b) => a - b);
  const maxLv = levelKeys.length ? levelKeys[levelKeys.length - 1] : 0;
  const padX = 48;
  const padY = 36;
  const pos = {};
  for (const lv of levelKeys) {
    const col = byLevel[lv];
    const x =
      maxLv === 0 ? w / 2 : padX + ((w - 2 * padX) * lv) / Math.max(maxLv, 1);
    col.forEach((p, i) => {
      const y =
        col.length === 1
          ? h / 2
          : padY + ((h - 2 * padY) * i) / Math.max(col.length - 1, 1);
      pos[p.id] = { x, y, pin: p };
    });
  }
  return pos;
}

/** Hit-test pin under canvas click. */
export function hitPin(canvas, timing, clientX, clientY, levels = null, radius = 18) {
  const rect = canvas.getBoundingClientRect();
  const mx = clientX - rect.left;
  const my = clientY - rect.top;
  const pos = pinPositions(canvas, timing, levels);
  let best = null;
  let bestD = radius * radius;
  for (const [id, p] of Object.entries(pos)) {
    const dx = mx - p.x;
    const dy = my - p.y;
    const d = dx * dx + dy * dy;
    if (d <= bestD) {
      bestD = d;
      best = id;
    }
  }
  return best;
}

/**
 * Draw a levelized timing DAG left→right by level.
 *
 * @param {HTMLCanvasElement} canvas
 * @param {object} timing
 * @param {object} [opts]
 * @param {Record<string,number>|null} [opts.levels]
 * @param {string[]} [opts.highlightPins]
 * @param {string[]} [opts.highlightArcs] — "from|to"
 * @param {Record<string,number|string>} [opts.tags] — pin → label under L#
 * @param {boolean} [opts.showDelay=true]
 */
export function drawTimingGraph(canvas, timing, opts = {}) {
  const { ctx, w, h } = fitHiDpiCanvas(canvas);
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#f7faf9";
  ctx.fillRect(0, 0, w, h);

  const levels = opts.levels || null;
  const highlightPins = new Set(opts.highlightPins || []);
  const highlightArcs = new Set(opts.highlightArcs || []);
  const tags = opts.tags || {};
  const showDelay = opts.showDelay !== false;
  const pos = pinPositions(canvas, timing, levels);

  // Arcs
  for (const a of timing.arcs) {
    const A = pos[a.from];
    const B = pos[a.to];
    if (!A || !B) continue;
    const key = `${a.from}|${a.to}`;
    const hi = highlightArcs.has(key);
    ctx.beginPath();
    ctx.moveTo(A.x, A.y);
    ctx.lineTo(B.x, B.y);
    ctx.strokeStyle = hi ? "#c45c26" : a.kind === "cell" ? "#6b4c9a" : "#94a3b8";
    ctx.lineWidth = hi ? 3 : a.kind === "cell" ? 2.5 : 1.5;
    if (a.kind === "net" && !hi) ctx.setLineDash([5, 4]);
    else ctx.setLineDash([]);
    ctx.stroke();
    ctx.setLineDash([]);

    // arrow head
    const ang = Math.atan2(B.y - A.y, B.x - A.x);
    const tipX = B.x - 14 * Math.cos(ang);
    const tipY = B.y - 14 * Math.sin(ang);
    ctx.beginPath();
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(
      tipX - 8 * Math.cos(ang - 0.4),
      tipY - 8 * Math.sin(ang - 0.4)
    );
    ctx.lineTo(
      tipX - 8 * Math.cos(ang + 0.4),
      tipY - 8 * Math.sin(ang + 0.4)
    );
    ctx.closePath();
    ctx.fillStyle = hi ? "#c45c26" : a.kind === "cell" ? "#6b4c9a" : "#94a3b8";
    ctx.fill();

    if (showDelay) {
      const mx = (A.x + B.x) / 2;
      const my = (A.y + B.y) / 2 - 8;
      ctx.fillStyle = "#334155";
      ctx.font = "11px ui-monospace, monospace";
      ctx.textAlign = "center";
      ctx.fillText(String(a.delay), mx, my);
    }
  }

  // Pins
  for (const p of timing.pins) {
    const P = pos[p.id];
    if (!P) continue;
    const hi = highlightPins.has(p.id);
    const r = hi ? 16 : 13;
    ctx.beginPath();
    ctx.arc(P.x, P.y, r, 0, Math.PI * 2);
    ctx.fillStyle = KIND_FILL[p.kind] || KIND_FILL.default;
    ctx.fill();
    if (hi) {
      ctx.strokeStyle = "#c45c26";
      ctx.lineWidth = 3;
      ctx.stroke();
    }
    ctx.fillStyle = "#0f172a";
    ctx.font = "11px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(p.id, P.x, P.y + r + 14);
    if (levels) {
      ctx.fillStyle = "#64748b";
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText(`L${levels[p.id]}`, P.x, P.y + 4);
    }
    if (tags[p.id] != null && tags[p.id] !== "") {
      ctx.fillStyle = "#0f172a";
      ctx.font = "10px ui-monospace, monospace";
      ctx.fillText(String(tags[p.id]), P.x, P.y - r - 4);
    }
  }
}
