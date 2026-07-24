import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
let beforeRip = null;

createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Route L-HV, note overflow, click Rip-up reroute.
    Golden: rip-up can reduce total on hot corridors.</p>`,
  onAfterRoute(api) {
    if (beforeRip == null && api.getRoutes().length) beforeRip = api.getOverflow().total;
  },
  extraMetrics(api) {
    const lines = [];
    if (beforeRip != null) lines.push(`before rip: ${beforeRip.toFixed(2)}`);
    return lines;
  },
  challenges: [
    { id: "l-route", title: "Route L-HV first", level: "Intro",
      prompt: "Route L-HV before rip-up.",
      setup: (_c, api) => { beforeRip=null; api.routeLHV(); beforeRip=api.getOverflow().total; },
      check: (_c, api) => api.getRoutes().length > 0 },
    { id: "has-ov", title: "Overflow before rip", level: "Intro",
      prompt: "Spread L-HV has overflow > 0.",
      setup: (_c, api) => { api.routeLHV(); beforeRip=api.getOverflow().total; },
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "rip-btn", title: "Run rip-up", level: "Practice",
      prompt: "Click Rip-up reroute.",
      setup: (_c, api) => { api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getRoutes().length > 0 },
    { id: "not-worse", title: "Rip ≤ before", level: "Practice",
      prompt: "After rip-up, total overflow ≤ before.",
      setup: (_c, api) => {
        api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getOverflow().total <= beforeRip + 0.01 },
    { id: "improve", title: "Rip improves or clears", level: "Challenge",
      prompt: "Rip-up strictly lowers total or clears overflow.",
      setup: (_c, api) => {
        api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getOverflow().total < beforeRip || api.getOverflow().total === 0 },
    { id: "max-drop", title: "Max ≤ 1 after rip", level: "Challenge",
      prompt: "After rip-up, max overflow ≤ 1.",
      check: (_c, api) => {
        if (!api.getRoutes().length) api.routeLHV();
        api.ripupReroute();
        return api.getOverflow().max <= 1; } },
    { id: "golden", title: "Rip helper ok", level: "Intro",
      prompt: "GOLDENS documents rip-up can improve overflow.",
      check: () => GOLDENS.ripupImproves === true },
    { id: "six-nets", title: "Six nets after rip", level: "Intro",
      prompt: "Still six net routes after rip-up.",
      setup: (_c, api) => { api.routeLHV(); api.ripupReroute(); },
      check: (_c, api) => api.getRoutes().length === 6 },
  ],
});
