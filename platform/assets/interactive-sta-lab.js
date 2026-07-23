/**
 * Interactive STA lab chrome.
 * Learner edits levels / values / path / cone / exceptions; Check scores learner state.
 * Reveal golden is optional study aid — not the path to pass.
 */
import {
  GOLDENS,
  PROP_GOLDENS,
  TINY_TIMING,
  cloneTiming,
  levelize,
  near,
  withCycle,
} from "./sta-core.js";
import {
  createChallengeLab,
  drawTimingGraph,
  el,
  hitPin,
  metricsBlock,
} from "./sta-ui.js";

export function emptyLevels(timing = TINY_TIMING) {
  return Object.fromEntries(timing.pins.map((p) => [p.id, null]));
}

export function cloneLevels(lv) {
  return lv ? { ...lv } : {};
}

export function levelsComplete(lv, timing = TINY_TIMING) {
  return timing.pins.every((p) => lv?.[p.id] != null && Number.isFinite(lv[p.id]));
}

export function levelsMatchGolden(lv, golden = GOLDENS.levels) {
  if (!lv) return false;
  return Object.keys(golden).every((id) => lv[id] === golden[id]);
}

export function valuesNear(a, b, eps = 1e-6) {
  if (!a || !b) return false;
  const keys = Object.keys(b);
  return keys.every((k) => a[k] != null && near(a[k], b[k], eps));
}

/**
 * Create an interactive STA lab.
 *
 * opts.mode:
 *  - "levels"   — assign levels (+/-) or Run levelize
 *  - "values"   — edit pin numeric tags (arrival / required / slack)
 *  - "path"     — click pins to build a path
 *  - "cone"     — click pins to mark a fanout cone; optional delay bump
 *  - "exceptions" — disable arcs + multicycle cycles
 *
 * opts:
 *  - starterHtml, challenges[], valueLabel ("A" | "R" | "S" | …)
 *  - initialTiming / getTiming()
 *  - initialLevels / initialValues / initialPath / initialMarked
 *  - revealLevels / revealValues / revealPath / revealMarked
 *  - extraActions(ctx, api), extraMetrics(api), onAfterChange, onChallengeSetup
 *  - getDrawOpts(api), getTags(api)
 *  - allowCycleToggle (levels mode)
 *  - selectedArcKey for exceptions
 */
export function createInteractiveStaLab(root, opts = {}) {
  const mode = opts.mode || "levels";
  const valueLabel = opts.valueLabel || "V";

  function baseTiming() {
    if (typeof opts.getTiming === "function") return cloneTiming(opts.getTiming());
    return cloneTiming(opts.initialTiming || TINY_TIMING);
  }

  let timing = baseTiming();
  let selected = timing.pins[0]?.id || "in";
  let selectedArc = opts.initialArc || "u1/A|u1/Y";
  let levels = cloneLevels(
    opts.initialLevels !== undefined ? opts.initialLevels : emptyLevels(timing)
  );
  let values = { ...(opts.initialValues || {}) };
  let path = [...(opts.initialPath || [])];
  let marked = new Set(opts.initialMarked || []);
  let disabledArcs = new Set(opts.initialDisabled || []);
  let setupCycles = opts.initialSetupCycles ?? 1;
  let revealed = false;
  let cyclic = false;
  const meta = opts.initialMeta ? { ...opts.initialMeta } : {};

  const api = {
    getTiming: () => timing,
    setTiming: (t) => {
      timing = cloneTiming(t);
    },
    getSelected: () => selected,
    setSelected: (id) => {
      selected = id;
    },
    getSelectedArc: () => selectedArc,
    setSelectedArc: (k) => {
      selectedArc = k;
    },
    getLevels: () => levels,
    setLevels: (lv) => {
      levels = cloneLevels(lv);
    },
    getValues: () => values,
    setValues: (v) => {
      values = { ...v };
    },
    setValue: (pin, n) => {
      values = { ...values, [pin]: n };
    },
    getPath: () => path,
    setPath: (p) => {
      path = [...p];
    },
    getMarked: () => marked,
    setMarked: (s) => {
      marked = new Set(s);
    },
    getDisabledArcs: () => disabledArcs,
    setDisabledArcs: (s) => {
      disabledArcs = new Set(s);
    },
    getSetupCycles: () => setupCycles,
    setSetupCycles: (n) => {
      setupCycles = n;
    },
    isRevealed: () => revealed,
    setRevealed: (v) => {
      revealed = !!v;
    },
    isCyclic: () => cyclic,
    getMeta: () => meta,
    setMeta: (m) => Object.assign(meta, m),
    near,
    GOLDENS,
    PROP_GOLDENS,
  };

  function resetWorkspace() {
    timing = baseTiming();
    cyclic = false;
    selected = timing.pins[0]?.id || "in";
    levels = cloneLevels(
      opts.initialLevels !== undefined ? opts.initialLevels : emptyLevels(timing)
    );
    values = { ...(opts.initialValues || {}) };
    path = [...(opts.initialPath || [])];
    marked = new Set(opts.initialMarked || []);
    disabledArcs = new Set(opts.initialDisabled || []);
    setupCycles = opts.initialSetupCycles ?? 1;
    revealed = false;
    for (const k of Object.keys(meta)) delete meta[k];
    if (opts.initialMeta) Object.assign(meta, opts.initialMeta);
    if (typeof opts.onLoadStarter === "function") opts.onLoadStarter(api);
  }

  function layoutLevels() {
    if (levels && levelsComplete(levels, timing)) return levels;
    return levelize(timing);
  }

  createChallengeLab(root, {
    starterButtonLabel: "Reset workspace",
    workspaceBeforeActions: true,
    idlePromptHtml:
      "Pick a challenge and click <strong>Start</strong>. Edit the workspace, then <strong>Check</strong>. Reveal golden is study-only.",
    starterHtml:
      (opts.starterHtml ||
        `<p><strong>Your workspace:</strong> click pins on the graph to select; use the actions below.
        Challenges check <strong>your</strong> state. <em>Reveal golden (study)</em> is optional.</p>`) +
      (opts.starterExtraHtml || ""),
    loadStarter() {
      resetWorkspace();
    },
    challenges: (opts.challenges || []).map((ch) => ({
      ...ch,
      setup: (ctx) => {
        resetWorkspace();
        if (typeof ch.setup === "function") ch.setup(ctx, api);
        else if (typeof opts.onChallengeSetup === "function")
          opts.onChallengeSetup(ctx, api, ch);
      },
      check: (ctx) => {
        if (typeof ch.check === "function") return !!ch.check(ctx, api);
        return false;
      },
    })),
    extraActions(ctx) {
      const btns = [];

      // Compact pin picker (avoids a button flood that pushes the graph off-screen)
      const pinSel = el("select", {
        className: "lab-pin-select",
        style: "min-width:7rem;padding:0.35rem 0.5rem;border-radius:6px;border:1px solid var(--line);",
        onChange: (ev) => {
          selected = ev.target.value;
          ctx.rerender();
        },
      });
      for (const p of timing.pins) {
        const opt = el("option", { value: p.id, text: p.id });
        if (p.id === selected) opt.selected = true;
        pinSel.append(opt);
      }
      btns.push(
        el("label", {
          style: "display:inline-flex;align-items:center;gap:0.35rem;font-size:0.9rem;",
        }, [
          el("span", { text: "Pin" }),
          pinSel,
        ])
      );

      if (mode === "levels") {
        btns.push(
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Level −",
            onClick: () => {
              const cur = levels[selected];
              levels = {
                ...levels,
                [selected]: cur == null ? 0 : Math.max(0, cur - 1),
              };
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Level +",
            onClick: () => {
              const cur = levels[selected];
              levels = { ...levels, [selected]: cur == null ? 0 : cur + 1 };
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Clear levels",
            onClick: () => {
              levels = emptyLevels(timing);
              revealed = false;
              ctx.rerender();
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Run levelize",
            onClick: () => {
              const lv = levelize(timing);
              levels = lv ? { ...lv } : emptyLevels(timing);
              meta.levelizeOk = lv != null;
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          })
        );
        if (opts.allowCycleToggle !== false) {
          btns.push(
            el("button", {
              className: "btn btn-ghost",
              type: "button",
              text: cyclic ? "Remove cycle edge" : "Add cycle edge",
              onClick: () => {
                if (cyclic) {
                  timing = baseTiming();
                  cyclic = false;
                } else {
                  timing = withCycle(baseTiming());
                  cyclic = true;
                }
                levels = emptyLevels(timing);
                meta.levelizeOk = undefined;
                revealed = false;
                ctx.rerender();
                if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
              },
            })
          );
        }
      }

      if (mode === "values") {
        const step = opts.valueStep ?? 0.1;
        btns.push(
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: `${valueLabel} −`,
            onClick: () => {
              const cur = values[selected];
              const next = cur == null ? 0 : Math.round((cur - step) * 1000) / 1000;
              values = { ...values, [selected]: next };
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: `${valueLabel} +`,
            onClick: () => {
              const cur = values[selected];
              const next = cur == null ? 0 : Math.round((cur + step) * 1000) / 1000;
              values = { ...values, [selected]: next };
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Clear values",
            onClick: () => {
              values = {};
              revealed = false;
              ctx.rerender();
            },
          })
        );
      }

      if (mode === "path") {
        btns.push(
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Clear path",
            onClick: () => {
              path = [];
              revealed = false;
              ctx.rerender();
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Pop last",
            onClick: () => {
              path = path.slice(0, -1);
              revealed = false;
              ctx.rerender();
            },
          })
        );
      }

      if (mode === "cone") {
        btns.push(
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: "Clear marks",
            onClick: () => {
              marked = new Set();
              revealed = false;
              ctx.rerender();
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Toggle mark",
            onClick: () => {
              if (marked.has(selected)) marked.delete(selected);
              else marked.add(selected);
              marked = new Set(marked);
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          })
        );
      }

      if (mode === "exceptions") {
        const arcSel = el("select", {
          className: "lab-arc-select",
          style: "min-width:10rem;padding:0.35rem 0.5rem;border-radius:6px;border:1px solid var(--line);",
          onChange: (ev) => {
            selectedArc = ev.target.value;
            ctx.rerender();
          },
        });
        for (const a of timing.arcs) {
          const key = `${a.from}|${a.to}`;
          const opt = el("option", {
            value: key,
            text: `${a.from}→${a.to} (${a.delay})`,
          });
          if (key === selectedArc) opt.selected = true;
          arcSel.append(opt);
        }
        btns.push(
          el("label", {
            style: "display:inline-flex;align-items:center;gap:0.35rem;font-size:0.9rem;",
          }, [
            el("span", { text: "Arc" }),
            arcSel,
          ])
        );
        btns.push(
          el("button", {
            className: "btn btn-secondary",
            type: "button",
            text: disabledArcs.has(selectedArc) ? "Enable arc" : "Disable arc (false)",
            onClick: () => {
              if (disabledArcs.has(selectedArc)) disabledArcs.delete(selectedArc);
              else disabledArcs.add(selectedArc);
              disabledArcs = new Set(disabledArcs);
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Cycles −",
            onClick: () => {
              setupCycles = Math.max(1, setupCycles - 1);
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          }),
          el("button", {
            className: "btn btn-ghost",
            type: "button",
            text: "Cycles +",
            onClick: () => {
              setupCycles = setupCycles + 1;
              revealed = false;
              ctx.rerender();
              if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
            },
          })
        );
      }

      btns.push(
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: "Reset to starter",
          onClick: () => {
            resetWorkspace();
            ctx.rerender();
          },
        }),
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: revealed ? "Hide golden" : "Reveal golden (study)",
          onClick: () => {
            if (revealed) {
              resetWorkspace();
            } else {
              if (opts.revealLevels) levels = cloneLevels(opts.revealLevels);
              if (opts.revealValues) values = { ...opts.revealValues };
              if (opts.revealPath) path = [...opts.revealPath];
              if (opts.revealMarked) marked = new Set(opts.revealMarked);
              if (opts.revealDisabled) disabledArcs = new Set(opts.revealDisabled);
              if (opts.revealSetupCycles != null) setupCycles = opts.revealSetupCycles;
              if (typeof opts.onRevealGolden === "function") opts.onRevealGolden(api);
              revealed = true;
            }
            ctx.rerender();
          },
        })
      );

      if (typeof opts.extraActions === "function") {
        btns.push(...(opts.extraActions(ctx, api) || []));
      }
      return btns;
    },
    renderWorkspace(ctx) {
      const drawLevels = mode === "levels" ? (levelsComplete(levels, timing) ? levels : null) : layoutLevels();
      const drawOpts =
        typeof opts.getDrawOpts === "function"
          ? opts.getDrawOpts(api)
          : { ...(opts.drawOpts || {}) };

      let tags = {};
      if (typeof opts.getTags === "function") tags = opts.getTags(api) || {};
      else if (mode === "values") {
        for (const [p, v] of Object.entries(values)) tags[p] = `${valueLabel}:${v}`;
      } else if (mode === "levels" && levels) {
        for (const [p, v] of Object.entries(levels)) {
          if (v != null) tags[p] = `L?${v}`;
        }
      }

      const hiPins = [
        selected,
        ...(drawOpts.highlightPins || []),
        ...(mode === "path" ? path : []),
        ...(mode === "cone" ? [...marked] : []),
      ];
      const hiArcs =
        mode === "path" && path.length >= 2
          ? path.slice(0, -1).map((p, i) => `${p}|${path[i + 1]}`)
          : mode === "exceptions"
            ? [...disabledArcs]
            : drawOpts.highlightArcs || [];

      drawTimingGraph(ctx.canvas, timing, {
        levels: drawOpts.levels !== undefined ? drawOpts.levels : drawLevels,
        tags: { ...tags, ...(drawOpts.tags || {}) },
        highlightPins: hiPins,
        highlightArcs: hiArcs,
        showDelay: drawOpts.showDelay !== false,
      });

      ctx.canvas.onclick = (ev) => {
        const hit = hitPin(ctx.canvas, timing, ev.clientX, ev.clientY, drawLevels);
        if (!hit) return;
        selected = hit;
        if (mode === "path") {
          path = [...path, hit];
          revealed = false;
        } else if (mode === "cone") {
          if (marked.has(hit)) marked.delete(hit);
          else marked.add(hit);
          marked = new Set(marked);
          revealed = false;
        }
        ctx.rerender();
        if (typeof opts.onAfterChange === "function") opts.onAfterChange(ctx, api);
      };

      const lines = [
        `selected: ${selected}`,
        revealed ? "view: revealed golden (study)" : "view: your workspace",
      ];
      if (mode === "levels") {
        const assigned = timing.pins.filter((p) => levels?.[p.id] != null).length;
        lines.push(`levels assigned: ${assigned}/${timing.pins.length}`);
        lines.push(`acyclic: ${levelize(timing) != null}`);
        lines.push(`pins: ${timing.pins.length} · arcs: ${timing.arcs.length}`);
      }
      if (mode === "values") {
        lines.push(`values set: ${Object.keys(values).length}`);
        if (values[selected] != null) lines.push(`  ${selected} ${valueLabel}=${values[selected]}`);
      }
      if (mode === "path") {
        lines.push(`path (${path.length}): ${path.join(" → ") || "(empty)"}`);
      }
      if (mode === "cone") {
        lines.push(`marked: ${[...marked].sort().join(", ") || "(none)"}`);
      }
      if (mode === "exceptions") {
        lines.push(`setup cycles: ${setupCycles}`);
        lines.push(`disabled: ${[...disabledArcs].join(", ") || "(none)"}`);
        lines.push(`selected arc: ${selectedArc}`);
      }
      if (typeof opts.extraMetrics === "function") {
        lines.push(...opts.extraMetrics(api));
      }
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(metricsBlock(lines));
      if (typeof opts.renderExtra === "function") opts.renderExtra(ctx, api);
    },
  });

  return api;
}
