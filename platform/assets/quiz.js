/**
 * Formative quiz player for lab pages.
 * Mount: DDVQuiz.mount(rootEl, quiz, { nextHref, nextLabel, onPass })
 * Types: multiple_choice | mcq | true_false | short | short_answer
 */
(function () {
  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  function normalizeType(type) {
    if (type === "mcq" || type === "multiple_choice") return "multiple_choice";
    if (type === "short" || type === "short_answer") return "short_answer";
    return type || "multiple_choice";
  }

  function mount(root, quiz, opts) {
    if (!root || !quiz || !Array.isArray(quiz.items) || !quiz.items.length) {
      if (root) {
        root.hidden = true;
        root.innerHTML = "";
      }
      return;
    }

    opts = opts || {};
    root.hidden = false;
    const passing = quiz.passing_score != null ? quiz.passing_score : 0.67;
    const results = {};
    const nextHref = opts.nextHref || "";
    const nextLabel = opts.nextLabel || "Next lab";

    root.innerHTML = "";
    root.classList.add("quiz-section");
    root.id = root.id || "quiz";

    const title = document.createElement("h2");
    title.textContent = quiz.title || "Check your understanding";
    root.appendChild(title);

    const note = document.createElement("p");
    note.className = "lead";
    note.textContent =
      "Formative self-check — check each answer as you go. Explanations appear after you submit.";
    root.appendChild(note);

    quiz.items.forEach((item, idx) => {
      const type = normalizeType(item.type);
      const box = document.createElement("div");
      box.className = "quiz-item";
      box.dataset.id = item.id || `q${idx + 1}`;

      const prompt = document.createElement("p");
      prompt.className = "prompt";
      prompt.textContent = `${idx + 1}. ${item.prompt || ""}`;
      box.appendChild(prompt);

      if (type === "multiple_choice") {
        const choices = document.createElement("div");
        choices.className = "quiz-choices";
        (item.choices || []).forEach((choice, ci) => {
          const label = document.createElement("label");
          const input = document.createElement("input");
          input.type = "radio";
          input.name = box.dataset.id;
          input.value = String(ci);
          label.appendChild(input);
          label.appendChild(document.createTextNode(choice));
          choices.appendChild(label);
        });
        box.appendChild(choices);
      } else if (type === "true_false") {
        const choices = document.createElement("div");
        choices.className = "quiz-choices";
        ["True", "False"].forEach((labelText, ci) => {
          const label = document.createElement("label");
          const input = document.createElement("input");
          input.type = "radio";
          input.name = box.dataset.id;
          input.value = ci === 0 ? "true" : "false";
          label.appendChild(input);
          label.appendChild(document.createTextNode(labelText));
          choices.appendChild(label);
        });
        box.appendChild(choices);
      } else if (type === "short_answer") {
        const ta = document.createElement("textarea");
        ta.className = "quiz-short";
        ta.placeholder = "Your answer…";
        box.appendChild(ta);
      }

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn-secondary";
      btn.textContent = "Check answer";
      btn.addEventListener("click", () => checkItem(item, box, type));
      box.appendChild(btn);

      const result = document.createElement("div");
      result.className = "quiz-result";
      box.appendChild(result);

      root.appendChild(box);
    });

    const summary = document.createElement("div");
    summary.className = "quiz-summary";
    summary.dataset.role = "summary";
    root.appendChild(summary);

    const actions = document.createElement("div");
    actions.className = "quiz-actions";
    const submitAll = document.createElement("button");
    submitAll.type = "button";
    submitAll.className = "btn btn-primary";
    submitAll.textContent = "Score quiz";
    submitAll.addEventListener("click", showSummary);
    actions.appendChild(submitAll);
    root.appendChild(actions);

    function getAnswer(item, box, type) {
      if (type === "short_answer") {
        const ta = box.querySelector("textarea");
        return (ta && ta.value ? ta.value : "").trim();
      }
      const selected = box.querySelector(`input[name="${box.dataset.id}"]:checked`);
      if (!selected) return null;
      if (type === "multiple_choice") return parseInt(selected.value, 10);
      if (type === "true_false") return selected.value === "true";
      return null;
    }

    function expectedMcq(item) {
      if (typeof item.answer_index === "number") return item.answer_index;
      if (typeof item.answer === "number") return item.answer;
      return null;
    }

    function checkItem(item, box, type) {
      const result = box.querySelector(".quiz-result");
      const ans = getAnswer(item, box, type);
      if (ans === null || ans === "") {
        result.className = "quiz-result show partial";
        result.textContent = "Select or enter an answer first.";
        return;
      }

      let correct = false;
      if (type === "multiple_choice") {
        correct = ans === expectedMcq(item);
      } else if (type === "true_false") {
        correct = ans === !!item.answer;
      } else if (type === "short_answer") {
        if (item.answer && typeof item.answer === "string") {
          correct = ans.toLowerCase() === item.answer.toLowerCase();
        } else {
          correct = ans.length > 8;
        }
      }

      results[box.dataset.id] = correct;
      result.className = "quiz-result show " + (correct ? "ok" : "bad");

      let html = correct ? "<strong>Correct.</strong> " : "<strong>Not quite.</strong> ";
      if (item.explain) html += escapeHtml(item.explain);
      if (type === "short_answer" && item.sample_answer) {
        html += `<br><br><strong>Sample answer:</strong> ${escapeHtml(item.sample_answer)}`;
      }
      result.innerHTML = html;
    }

    function showSummary() {
      quiz.items.forEach((item, idx) => {
        const id = item.id || `q${idx + 1}`;
        const box = root.querySelector(`.quiz-item[data-id="${id}"]`);
        if (box && results[id] === undefined) {
          checkItem(item, box, normalizeType(item.type));
        }
      });

      const total = quiz.items.length;
      let checked = 0;
      let correct = 0;
      quiz.items.forEach((item, idx) => {
        const id = item.id || `q${idx + 1}`;
        if (results[id] !== undefined) {
          checked += 1;
          if (results[id]) correct += 1;
        }
      });

      const pct = checked ? correct / checked : 0;
      const passed = checked === total && pct >= passing;
      const el = root.querySelector('[data-role="summary"]');
      el.className = "quiz-summary show";

      let html =
        `<strong>Score:</strong> ${correct} / ${total}` +
        (checked === total
          ? ` (${Math.round(pct * 100)}%) — ` +
            (passed
              ? "Nice work — you met the passing threshold."
              : "Review this lab and try again.")
          : " — Answer every question for a full score.");

      if (passed && nextHref) {
        html += `<div class="quiz-actions"><a class="btn btn-primary" href="${escapeAttr(nextHref)}">${escapeHtml(nextLabel)}</a></div>`;
      }
      el.innerHTML = html;
      el.scrollIntoView({ behavior: "smooth", block: "nearest" });

      if (passed && typeof opts.onPass === "function") opts.onPass({ correct, total, pct });
      if (passed && window.DDV && typeof window.DDV.gtagEvent === "function") {
        window.DDV.gtagEvent("quiz_pass", { score: correct, total: total });
      }
    }
  }

  window.DDVQuiz = { mount };
})();
