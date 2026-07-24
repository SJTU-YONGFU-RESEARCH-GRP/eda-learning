import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
let beforeRip = null;

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Route layered, note overflow, click Rip-up detailed.
    Golden: rip-up can reduce total on hot tracks.</p>`,
  extraMetrics(api) {
    const lines = [];
    if (beforeRip != null) lines.push(`before rip: ${beforeRip.toFixed(2)}`);
    return lines;
  },
  challenges: [
    { id: "layer-first", title: "Route layered first", level: "Intro",
      prompt: "Route layered before rip-up.",
      setup: (_c, api) => { beforeRip = null; api.routeLayered(); beforeRip = api.getOverflow().total; },
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "has-ov", title: "Overflow before rip", level: "Intro",
      prompt: "Spread layered has overflow > 0.",
      setup: (_c, api) => { api.routeLayered(); beforeRip = api.getOverflow().total; },
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "rip-btn", title: "Run rip-up", level: "Practice",
      prompt: "Click Rip-up detailed.",
      setup: (_c, api) => { api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "not-worse", title: "Rip ≤ before", level: "Practice",
      prompt: "After rip-up, total overflow ≤ before.",
      setup: (_c, api) => {
        api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getOverflow().total <= beforeRip + 0.01 },
    { id: "improve", title: "Rip improves", level: "Challenge",
      prompt: "Rip-up strictly lowers total or clears overflow.",
      setup: (_c, api) => {
        api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getOverflow().total < beforeRip || api.getOverflow().total === 0 },
    { id: "golden", title: "Rip helper ok", level: "Intro",
      prompt: "GOLDENS documents rip-up can improve overflow.",
      check: () => GOLDENS.ripupImproves === true },
    { id: "six-nets", title: "Six nets after rip", level: "Intro",
      prompt: "Still six net routes after rip-up.",
      setup: (_c, api) => { api.routeLayered(); api.ripupDetailed(); },
      check: (_c, api) => api.getRoutes().length === 6 },
    { id: "max-drop", title: "Max ≤ 1 after rip", level: "Challenge",
      prompt: "After rip-up, max overflow ≤ 1.",
      check: (_c, api) => {
        if (!api.getRoutes().some(r => r.segments?.length)) api.routeLayered();
        api.ripupDetailed();
        return api.getOverflow().max <= 1; } },
  ],
});
