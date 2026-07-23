/**
 * Formative quiz player for the module-slides HTML site.
 * Expects #quiz-root and a sibling script#quiz-data with JSON content.
 * Optional data-next-href / data-next-label on #quiz-root for post-pass CTA.
 */
(function () {
  const root = document.getElementById("quiz-root");
  const dataEl = document.getElementById("quiz-data");
  if (!root || !dataEl) return;

  let quiz;
  try {
    quiz = JSON.parse(dataEl.textContent);
  } catch (e) {
    root.innerHTML = "<p>Could not load quiz data.</p>";
    return;
  }

  const passing = quiz.passing_score ?? 0.7;
  const results = {};
  const nextHref = root.dataset.nextHref || "";
  const nextLabel = root.dataset.nextLabel || "Next part";

  function render() {
    root.innerHTML = "";

    const title = document.createElement("h2");
    title.textContent = quiz.title || "Check your understanding";
    root.appendChild(title);

    const note = document.createElement("p");
    note.className = "lead";
    note.textContent =
      "Formative self-check — check each answer as you go. Explanations appear after you submit.";
    root.appendChild(note);

    quiz.items.forEach((item, idx) => {
      const box = document.createElement("div");
      box.className = "quiz-item";
      box.dataset.id = item.id;

      const prompt = document.createElement("p");
      prompt.className = "prompt";
      prompt.textContent = `${idx + 1}. ${item.prompt}`;
      box.appendChild(prompt);

      if (item.type === "mcq") {
        const choices = document.createElement("div");
        choices.className = "quiz-choices";
        item.choices.forEach((choice, ci) => {
          const label = document.createElement("label");
          const input = document.createElement("input");
          input.type = "radio";
          input.name = item.id;
          input.value = String(ci);
          label.appendChild(input);
          label.appendChild(document.createTextNode(choice));
          choices.appendChild(label);
        });
        box.appendChild(choices);
      } else if (item.type === "true_false") {
        const choices = document.createElement("div");
        choices.className = "quiz-choices";
        ["True", "False"].forEach((labelText, ci) => {
          const label = document.createElement("label");
          const input = document.createElement("input");
          input.type = "radio";
          input.name = item.id;
          input.value = ci === 0 ? "true" : "false";
          label.appendChild(input);
          label.appendChild(document.createTextNode(labelText));
          choices.appendChild(label);
        });
        box.appendChild(choices);
      } else if (item.type === "short") {
        const ta = document.createElement("textarea");
        ta.className = "quiz-short";
        ta.placeholder = "Your answer…";
        ta.dataset.id = item.id;
        box.appendChild(ta);
      }

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn-secondary";
      btn.textContent = "Check answer";
      btn.addEventListener("click", () => checkItem(item, box));
      box.appendChild(btn);

      const result = document.createElement("div");
      result.className = "quiz-result";
      box.appendChild(result);

      root.appendChild(box);
    });

    const summary = document.createElement("div");
    summary.id = "quiz-summary";
    summary.className = "quiz-summary";
    root.appendChild(summary);

    const actions = document.createElement("div");
    actions.className = "quiz-actions";

    const submitAll = document.createElement("button");
    submitAll.type = "button";
    submitAll.className = "btn";
    submitAll.textContent = "Score quiz";
    submitAll.addEventListener("click", showSummary);
    actions.appendChild(submitAll);

    root.appendChild(actions);
  }

  function getAnswer(item, box) {
    if (item.type === "short") {
      const ta = box.querySelector("textarea");
      return (ta?.value || "").trim();
    }
    const selected = box.querySelector(`input[name="${item.id}"]:checked`);
    if (!selected) return null;
    if (item.type === "mcq") return parseInt(selected.value, 10);
    if (item.type === "true_false") return selected.value === "true";
    return null;
  }

  function checkItem(item, box) {
    const result = box.querySelector(".quiz-result");
    const ans = getAnswer(item, box);
    if (ans === null || ans === "") {
      result.className = "quiz-result show partial";
      result.textContent = "Select or enter an answer first.";
      return;
    }

    let correct = false;
    if (item.type === "mcq") {
      correct = ans === item.answer_index;
    } else if (item.type === "true_false") {
      correct = ans === item.answer;
    } else if (item.type === "short") {
      correct = ans.length > 10;
    }

    results[item.id] = correct;
    result.className = "quiz-result show " + (correct ? "ok" : "bad");

    let html = correct ? "<strong>Correct.</strong> " : "<strong>Not quite.</strong> ";
    if (item.explain) html += escapeHtml(item.explain);
    if (item.type === "short" && item.sample_answer) {
      html += `<br><br><strong>Sample answer:</strong> ${escapeHtml(item.sample_answer)}`;
    }
    result.innerHTML = html;
  }

  function showSummary() {
    quiz.items.forEach((item) => {
      const box = root.querySelector(`.quiz-item[data-id="${item.id}"]`);
      if (box && results[item.id] === undefined) {
        checkItem(item, box);
      }
    });

    const total = quiz.items.length;
    let checked = 0;
    let correct = 0;
    quiz.items.forEach((item) => {
      if (results[item.id] !== undefined) {
        checked += 1;
        if (results[item.id]) correct += 1;
      }
    });

    const summary = document.getElementById("quiz-summary");
    summary.className = "quiz-summary show";
    const pct = checked ? correct / checked : 0;
    const passed = checked === total && pct >= passing;

    let html =
      `<strong>Score:</strong> ${correct} / ${total}` +
      (checked === total
        ? ` (${Math.round(pct * 100)}%) — ` +
          (passed
            ? "Nice work — you met the passing threshold."
            : "Review this part and try again.")
        : " — Answer every question for a full score.");

    if (passed && nextHref) {
      html += `<div class="quiz-actions"><a class="btn" href="${escapeAttr(nextHref)}">${escapeHtml(nextLabel)}</a></div>`;
    }

    summary.innerHTML = html;
    summary.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  render();
})();
