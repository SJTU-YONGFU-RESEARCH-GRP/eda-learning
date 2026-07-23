/**
 * Small UX helpers for the module-slides site (+ optional GA4 video events).
 */
(function () {
  function gtagEvent(name, params) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, params || {});
  }

  // If a video source 404s, show the placeholder instead of a blank player.
  // When GA4 is present, also send play / progress / complete events.
  document.querySelectorAll(".video-wrap").forEach((wrap) => {
    const video = wrap.querySelector("video");
    const placeholder = wrap.querySelector(".video-placeholder");
    if (!video || !placeholder) return;

    video.addEventListener("error", () => {
      video.style.display = "none";
      placeholder.hidden = false;
    });

    const pagePath = location.pathname;
    const milestones = { 25: false, 50: false, 75: false, 90: false };
    let started = false;

    video.addEventListener("play", () => {
      if (started) return;
      started = true;
      gtagEvent("video_start", {
        page_path: pagePath,
        video_url: video.currentSrc || "",
      });
    });

    video.addEventListener("timeupdate", () => {
      const duration = video.duration;
      if (!duration || !isFinite(duration)) return;
      const pct = (video.currentTime / duration) * 100;
      for (const mark of [25, 50, 75, 90]) {
        if (pct >= mark && !milestones[mark]) {
          milestones[mark] = true;
          gtagEvent("video_progress", {
            page_path: pagePath,
            percent: mark,
            video_url: video.currentSrc || "",
          });
        }
      }
    });

    video.addEventListener("ended", () => {
      gtagEvent("video_complete", {
        page_path: pagePath,
        video_url: video.currentSrc || "",
      });
    });
  });

  // Remember open/closed state for slides/transcript panels on this page.
  document.querySelectorAll("details.panel[data-persist]").forEach((panel) => {
    const key = `module-slides:${location.pathname}:${panel.dataset.persist}`;
    try {
      const saved = localStorage.getItem(key);
      if (saved === "1") panel.open = true;
      if (saved === "0") panel.open = false;
    } catch (_) {
      /* ignore */
    }
    panel.addEventListener("toggle", () => {
      try {
        localStorage.setItem(key, panel.open ? "1" : "0");
      } catch (_) {
        /* ignore */
      }
    });
  });
})();
