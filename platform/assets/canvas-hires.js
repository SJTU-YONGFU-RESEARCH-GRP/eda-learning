/**
 * Shared HiDPI canvas setup for browser labs.
 * Backing-store pixels = CSS size × devicePixelRatio (capped); draw in CSS pixels.
 */

/** Default CSS height for lab / walkthrough canvases (was 300). */
export const LAB_CANVAS_CSS_HEIGHT = 480;

/** Fallback CSS size when clientWidth/Height is 0 (hidden / not laid out yet). */
export const LAB_CANVAS_FALLBACK = { w: 640, h: LAB_CANVAS_CSS_HEIGHT };

/** Cap DPR so large canvases stay responsive on 3× displays. */
export const LAB_CANVAS_MAX_DPR = 3;

/**
 * Size the canvas backing store for crisp drawing on HiDPI screens.
 * @param {HTMLCanvasElement} canvas
 * @param {{w?:number,h?:number}} [fallback]
 * @returns {{ctx:CanvasRenderingContext2D,w:number,h:number,dpr:number}}
 */
export function fitHiDpiCanvas(canvas, fallback = LAB_CANVAS_FALLBACK) {
  const dpr = Math.min(window.devicePixelRatio || 1, LAB_CANVAS_MAX_DPR);
  const w = Math.max(1, Math.floor(canvas.clientWidth || fallback.w || 640));
  const h = Math.max(
    1,
    Math.floor(canvas.clientHeight || fallback.h || LAB_CANVAS_CSS_HEIGHT),
  );
  const bw = Math.floor(w * dpr);
  const bh = Math.floor(h * dpr);
  if (canvas.width !== bw || canvas.height !== bh) {
    canvas.width = bw;
    canvas.height = bh;
  }
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, w, h, dpr };
}

/**
 * Fit a design-space node layout into the canvas with padding.
 * Design coords (e.g. starterLayout) are scaled uniformly and centered.
 *
 * @param {Record<string,{x:number,y:number}>} layout
 * @param {number} w — CSS width
 * @param {number} h — CSS height
 * @param {{pad?:number,nodeMargin?:number}} [opts]
 * @returns {{
 *   layout: Record<string,{x:number,y:number}>,
 *   scale: number,
 *   nodeR: number,
 *   fontPx: number,
 *   edgeW: number,
 * }}
 */
export function fitGraphLayout(layout, w, h, opts = {}) {
  const pad = opts.pad ?? 36;
  const nodeMargin = opts.nodeMargin ?? 22;
  const pts = Object.values(layout);
  if (!pts.length) {
    return { layout: {}, scale: 1, nodeR: 16, fontPx: 13, edgeW: 2 };
  }
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const p of pts) {
    minX = Math.min(minX, p.x);
    minY = Math.min(minY, p.y);
    maxX = Math.max(maxX, p.x);
    maxY = Math.max(maxY, p.y);
  }
  minX -= nodeMargin;
  minY -= nodeMargin;
  maxX += nodeMargin;
  maxY += nodeMargin;
  const bw = Math.max(maxX - minX, 1);
  const bh = Math.max(maxY - minY, 1);
  const scale = Math.min((w - 2 * pad) / bw, (h - 2 * pad) / bh);
  const ox = pad + ((w - 2 * pad) - bw * scale) / 2;
  const oy = pad + ((h - 2 * pad) - bh * scale) / 2;
  const out = {};
  for (const [k, p] of Object.entries(layout)) {
    out[k] = {
      x: ox + (p.x - minX) * scale,
      y: oy + (p.y - minY) * scale,
    };
  }
  const nodeR = Math.max(14, Math.min(28, 16 * scale));
  const fontPx = Math.max(12, Math.min(18, 13 * scale));
  const edgeW = Math.max(1.5, Math.min(3.5, 2 * scale));
  return { layout: out, scale, nodeR, fontPx, edgeW };
}
