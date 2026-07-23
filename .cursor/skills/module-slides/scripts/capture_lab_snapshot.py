#!/usr/bin/env python3
"""Capture a browser lab screenshot for module-slides Track B slides.

Examples:
  # From a lab module (reads Primary lab from README, or --lab):
  python capture_lab_snapshot.py courses/learn_unix/module03-path-abs-rel

  # Explicit lab id + local tools server:
  python capture_lab_snapshot.py --lab path-abs-rel --out courses/learn_unix/module03-path-abs-rel/assets

  # Live site:
  python capture_lab_snapshot.py --lab vfs-terminal --base https://universal-verification-methodology.github.io/learning/tools

  # Tools index (intro modules):
  python capture_lab_snapshot.py --lab index --module-dir courses/learn_unix/module00-intro
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

DEFAULT_LOCAL = "http://127.0.0.1:8080/tools"
DEFAULT_LIVE = "https://universal-verification-methodology.github.io/learning/tools"


def _lab_from_readme(module_dir: Path) -> str | None:
    readme = module_dir / "README.md"
    if not readme.is_file():
        return None
    text = readme.read_text(encoding="utf-8")
    m = re.search(r"Primary lab:\s*`([a-z0-9-]+)`", text)
    if m:
        return m.group(1)
    m = re.search(r"lab:\s*`([a-z0-9-]+)`", text, re.I)
    if m:
        return m.group(1)
    return None


def _tool_url(base: str, lab_id: str) -> str:
    base = base.rstrip("/")
    if lab_id in ("index", "tools", "tools-index"):
        return f"{base}/index.html"
    return f"{base}/{lab_id}/index.html"


def _ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "Playwright is required for snapshots.\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        ) from exc


def capture(
    *,
    url: str,
    out_path: Path,
    width: int,
    height: int,
    wait_ms: int,
    full_page: bool,
    selector: str | None,
) -> Path:
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url, wait_until="networkidle", timeout=60_000)
        # Let client-side labs paint starter UI
        page.wait_for_timeout(wait_ms)
        if selector:
            loc = page.locator(selector).first
            try:
                loc.wait_for(state="visible", timeout=15_000)
                loc.screenshot(path=str(out_path))
            except Exception:
                # Lab chrome differs; still capture the viewport.
                page.screenshot(path=str(out_path), full_page=full_page)
        else:
            page.screenshot(path=str(out_path), full_page=full_page)
        browser.close()
    return out_path


def _patch_outline_image_slide(
    module_dir: Path,
    image_rel: str,
    *,
    title: str,
) -> None:
    """Ensure outline.yaml has a Track B image slide pointing at the snapshot."""
    try:
        import yaml
    except ImportError:
        return
    outline_path = module_dir / "outline.yaml"
    if not outline_path.is_file():
        return
    data = yaml.safe_load(outline_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "slides" not in data:
        return
    slides = data["slides"]
    if not isinstance(slides, list):
        return

    # Update existing lab snapshot slide, or insert after first title/concept
    for spec in slides:
        if not isinstance(spec, dict):
            continue
        if spec.get("type") == "image" and str(spec.get("image", "")).startswith("assets/lab"):
            spec["image"] = image_rel
            spec["title"] = title
            spec.setdefault(
                "notes",
                "Here is the browser lab with its starter example loaded. "
                "Use this view to orient yourself before you try the challenges.",
            )
            outline_path.write_text(
                yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            return

    insert_at = 1
    for i, spec in enumerate(slides):
        if isinstance(spec, dict) and spec.get("type") == "title":
            insert_at = i + 1
            break
    slides.insert(
        insert_at,
        {
            "type": "image",
            "title": title,
            "image": image_rel,
            "caption": "Browser lab — starter view",
            "notes": (
                "Here is the browser lab with its starter example loaded. "
                "Pause and look at the layout — you will use this same screen on Track B."
            ),
        },
    )
    outline_path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "module_dir",
        nargs="?",
        type=Path,
        help="courses/<course>/moduleNN-slug (optional if --lab + --out)",
    )
    parser.add_argument("--lab", help="Lab id under platform/tools/<id>/ (or 'index')")
    parser.add_argument(
        "--base",
        default=DEFAULT_LOCAL,
        help=f"Tools base URL (default: {DEFAULT_LOCAL}). Use live: {DEFAULT_LIVE}",
    )
    parser.add_argument("--out", type=Path, help="Output directory (default: <module>/assets)")
    parser.add_argument(
        "--name",
        default="lab-starter.png",
        help="Filename under assets/ (default: lab-starter.png)",
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--wait-ms", type=int, default=1500, help="Extra settle time after load")
    parser.add_argument("--full-page", action="store_true", help="Full-page screenshot")
    parser.add_argument(
        "--selector",
        help="Optional CSS selector to crop (e.g. main, #path-root)",
    )
    parser.add_argument(
        "--patch-outline",
        action="store_true",
        help="Insert/update an image slide in outline.yaml",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry count if the page is not ready (default: 2)",
    )
    args = parser.parse_args(argv)

    module_dir = args.module_dir.resolve() if args.module_dir else None
    lab_id = args.lab
    if not lab_id and module_dir:
        lab_id = _lab_from_readme(module_dir)
    if not lab_id:
        raise SystemExit("Need --lab or a module README with Primary lab: `id`")

    out_dir = args.out
    if out_dir is None:
        if module_dir is None:
            raise SystemExit("Need --out when module_dir is omitted")
        out_dir = module_dir / "assets"
    out_dir = out_dir.resolve()
    out_path = out_dir / args.name

    url = _tool_url(args.base, lab_id)
    _ensure_playwright()

    last_err: Exception | None = None
    for attempt in range(args.retries + 1):
        try:
            capture(
                url=url,
                out_path=out_path,
                width=args.width,
                height=args.height,
                wait_ms=args.wait_ms + attempt * 1000,
                full_page=args.full_page,
                selector=args.selector,
            )
            last_err = None
            break
        except Exception as exc:  # noqa: BLE001 — surface final error
            last_err = exc
            time.sleep(0.5)
    if last_err is not None:
        raise SystemExit(
            f"Snapshot failed for {url}\n"
            f"  {last_err}\n"
            f"Hint: start the site with:\n"
            f"  python -m http.server 8080 --directory platform\n"
            f"Or pass --base {DEFAULT_LIVE}"
        ) from last_err

    print(f"Wrote {out_path} from {url}")

    if args.patch_outline and module_dir:
        rel = f"assets/{args.name}"
        title = (
            "Tools index"
            if lab_id in ("index", "tools", "tools-index")
            else f"Browser lab — {lab_id}"
        )
        _patch_outline_image_slide(module_dir, rel, title=title)
        print(f"Patched {module_dir / 'outline.yaml'} with image slide → {rel}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
