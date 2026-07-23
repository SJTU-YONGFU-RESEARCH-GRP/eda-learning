/**
 * Placement canvas + re-exports of challenge chrome from clustering-ui.
 */
import { fitHiDpiCanvas } from "./canvas-hires.js";
import { createChallengeLab, el, metricsBlock } from "./clustering-ui.js";
import { CELLS, NETS } from "./placement-core.js";

const PALETTE = ["#2a6f6a", "#c45c26", "#3d5a80", "#6b4c9a", "#b08900", "#4a7c59"];

export { createChallengeLab, el, metricsBlock };

function cellColor(id) {
  const i = CELLS.indexOf(id);
  return PALETTE[i >= 0 ? i % PALETTE.length : 0];
}

/**
 * Draw cells + net bounding boxes / edges on a canvas.
 * World coords roughly [0,8]×[0,8] mapped into the canvas with padding.
 *
 * @param {HTMLCanvasElement} canvas
 * @param {string[]} cells
 * @param {Record<string,{x:number,y:number}>} positions
 * @param {string[][]} nets
 * @param {object} [opts]
 * @param {boolean} [opts.showNets=true]
 * @param {boolean} [opts.showBBox=true]
 * @param {number} [opts.grid=2] — draw nxn density grid (0 to hide)
 * @param {Set<string>|string[]} [opts.highlightNets] — net indices or "0","4"
 * @param {string[]} [opts.highlightCells]
 */
export function drawPlacement(canvas, cells, positions, nets, opts = {}) {
  const { ctx, w, h } = fitHiDpiCanvas(canvas);
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#f7faf9";
  ctx.fillRect(0, 0, w, h);

  const pad = 28;
  const worldMin = opts.worldMin ?? -0.5;
  const worldMax = opts.worldMax ?? 8.5;
  const span = worldMax - worldMin;
  const scale = Math.min((w - 2 * pad) / span, (h - 2 * pad) / span);
  const ox = (w - span * scale) / 2;
  const oy = (h - span * scale) / 2;

  function map(p) {
    return {
      x: ox + (p.x - worldMin) * scale,
      y: oy + (worldMax - p.y) * scale, // y-up in world
    };
  }

  // density grid
  const grid = opts.grid ?? 2;
  if (grid > 0) {
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1;
    for (let i = 0; i <= grid; i++) {
      const t = worldMin + (span * i) / grid;
      const a = map({ x: t, y: worldMin });
      const b = map({ x: t, y: worldMax });
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
      const c = map({ x: worldMin, y: t });
      const d = map({ x: worldMax, y: t });
      ctx.beginPath();
      ctx.moveTo(c.x, c.y);
      ctx.lineTo(d.x, d.y);
      ctx.stroke();
    }
  }

  const netList = nets || NETS;
  const hiNets = new Set(
    (opts.highlightNets || []).map((x) => String(x))
  );
  const hiCells = new Set(opts.highlightCells || []);
  const showNets = opts.showNets !== false;
  const showBBox = opts.showBBox !== false;

  if (showNets || showBBox) {
    netList.forEach((net, idx) => {
      const pts = net.map((id) => positions[id]).filter(Boolean);
      if (pts.length < 2) return;
      const hot = hiNets.has(String(idx));
      if (showBBox) {
        let minX = Infinity;
        let maxX = -Infinity;
        let minY = Infinity;
        let maxY = -Infinity;
        for (const p of pts) {
          minX = Math.min(minX, p.x);
          maxX = Math.max(maxX, p.x);
          minY = Math.min(minY, p.y);
          maxY = Math.max(maxY, p.y);
        }
        const tl = map({ x: minX, y: maxY });
        const br = map({ x: maxX, y: minY });
        ctx.strokeStyle = hot ? "#b45309" : "#cbd5e1";
        ctx.lineWidth = hot ? 2 : 1;
        ctx.setLineDash(hot ? [] : [4, 3]);
        ctx.strokeRect(tl.x, tl.y, br.x - tl.x, br.y - tl.y);
        ctx.setLineDash([]);
      }
      if (showNets) {
        // star from first pin
        const hub = map(pts[0]);
        ctx.strokeStyle = hot ? "#c45c26" : "#94a3b8";
        ctx.lineWidth = hot ? 2.5 : 1.5;
        for (let i = 1; i < pts.length; i++) {
          const q = map(pts[i]);
          ctx.beginPath();
          ctx.moveTo(hub.x, hub.y);
          ctx.lineTo(q.x, q.y);
          ctx.stroke();
        }
      }
    });
  }

  const list = cells || CELLS;
  for (const id of list) {
    const p = positions[id];
    if (!p) continue;
    const m = map(p);
    const r = hiCells.has(id) ? 15 : 13;
    ctx.beginPath();
    ctx.arc(m.x, m.y, r, 0, Math.PI * 2);
    ctx.fillStyle = cellColor(id);
    ctx.fill();
    ctx.strokeStyle = hiCells.has(id) ? "#b45309" : "#0f172a";
    ctx.lineWidth = hiCells.has(id) ? 2.5 : 1.5;
    ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.font = "bold 12px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(id, m.x, m.y);
  }
  ctx.textAlign = "start";
  ctx.textBaseline = "alphabetic";
}

export { PALETTE, cellColor };
