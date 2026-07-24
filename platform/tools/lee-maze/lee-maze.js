import {
  GOLDENS, PLACEMENT, leeMaze, isBlocked
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
const blocked = new Set();
for (let x = 5; x < 7; x++) for (let y = 2; y < 4; y++) blocked.add(`${x},${y}`);

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Lee maze routes around blockage. Detour (4,1)→(7,1) length ≈ ${GOLDENS.leeDetourLen}.</p>`,
  extraMetrics() {
    const path = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
    return [`detour len: ${path ? path.length : 0}`];
  },
  challenges: [
    { id: "detour-len", title: "Detour length", level: "Intro",
      prompt: "Lee (4,1)→(7,1) around blockage has documented length.",
      check: () => {
        const p = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
        return p && p.length === GOLDENS.leeDetourLen; } },
    { id: "avoid-block", title: "Avoids blockage", level: "Intro",
      prompt: "Detour path avoids blocked cells.",
      check: () => {
        const p = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
        return p && p.every(pt => !isBlocked(pt.x, pt.y)); } },
    { id: "route-lee", title: "Route Lee", level: "Practice",
      prompt: "Click Route Lee on spread starter.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "lee-finite", title: "Lee overflow finite", level: "Practice",
      prompt: "After Lee route, overflow metrics are finite.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "six-nets", title: "Six nets routed", level: "Practice",
      prompt: "Lee routes all six nets.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => api.getRoutes().filter(r => r.segments?.length).length === 6 },
    { id: "total-le2", title: "Total ≤ 2", level: "Challenge",
      prompt: "Move cells; Lee route with total overflow ≤ 2.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 2 },
    { id: "zero-lee", title: "Clear overflow", level: "Challenge",
      prompt: "Achieve total overflow 0 with Lee routing.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total === 0 },
    { id: "same-pin", title: "Same pin trivial", level: "Intro",
      prompt: "Lee from A pin to itself returns one point.",
      check: () => {
        const p = leeMaze({ x: 1, y: 1 }, { x: 1, y: 1 }, blocked);
        return p && p.length === 1; } },
  ],
});
