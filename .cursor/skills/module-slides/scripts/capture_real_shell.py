#!/usr/bin/env python3
"""Capture a real-shell (Track A) session frame for module-slides.

Runs try-these commands in WSL/bash under the module examples dir and writes
a terminal-framed PNG (plus .txt transcript of the session).

Example:
  python capture_real_shell.py courses/learn_unix/module01-vfs-terminal
  python capture_real_shell.py courses/learn_unix/module01-vfs-terminal \\
      --example-subdir navigation \\
      --commands "pwd,ls -la,cd sample_repo,ls,cd ..,pwd"

  # When wrappers would pollute builtins like history:
  python capture_real_shell.py courses/learn_unix/module14-shell-history \\
      --example-subdir history --session-text assets/real-shell.txt
"""

from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_COMMANDS = ["pwd", "ls -la", "cd sample_repo", "ls", "cd ..", "pwd"]


def _ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "Playwright required: pip install playwright && playwright install chromium"
        ) from exc


def _to_posix_path(path: Path) -> str:
    resolved = path.resolve()
    s = resolved.as_posix()
    if len(s) >= 2 and s[1] == ":":
        drive = s[0].lower()
        rest = s[2:].lstrip("/")
        return f"/mnt/{drive}/{rest}"
    return s


def _printf_literal(command: str) -> str:
    """Escape for use inside double-quoted printf so $? / $! are not expanded early."""
    return (
        command.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("`", "\\`")
        .replace("$", "\\$")
    )


def _run_bash(script: str) -> str:
    runners: list[list[str]] = []
    if shutil.which("wsl"):
        runners.append(["wsl", "-e", "bash", "-lc", script])
    if shutil.which("bash"):
        runners.append(["bash", "-lc", script])

    errors: list[str] = []
    for cmd in runners:
        try:
            proc = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            return proc.stdout.strip() + "\n"
        except (OSError, subprocess.CalledProcessError) as exc:
            err = getattr(exc, "stderr", "") or str(exc)
            errors.append(f"{cmd[0]}: {err.strip() or exc}")
            continue
    raise SystemExit("Could not run real shell session:\n  " + "\n  ".join(errors))


def _run_real_shell_session(example_dir: Path, commands: list[str]) -> str:
    posix = _to_posix_path(example_dir)
    script = "\n".join(
        [
            "set -e",
            f"cd '{posix}'",
            "echo '# real shell session (Track A)'",
            "echo",
            *[
                "\n".join(
                    [
                        f'printf "%s\\n" "$ {_printf_literal(c)}"',
                        c,
                        "echo",
                    ]
                )
                for c in commands
            ],
        ]
    )
    return _run_bash(script)


def _run_bash_script_file(script_path: Path, example_dir: Path | None = None) -> str:
    """Run a prepared bash script; stdout becomes the framed session text.

    Use when per-command wrappers would pollute tools like ``history`` (module 14).
    """
    posix_script = _to_posix_path(script_path)
    parts = ["set -e", f"bash '{posix_script}'"]
    if example_dir is not None:
        posix_cd = _to_posix_path(example_dir)
        parts = ["set -e", f"cd '{posix_cd}'", f"bash '{posix_script}'"]
    return _run_bash("\n".join(parts))


def _frame_session_text(
    session: str,
    *,
    out_path: Path,
    title: str,
    width: int,
    height: int,
) -> Path:
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "real-shell.html"
        html_path.write_text(_terminal_html(session, title=title), encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
            page.wait_for_timeout(300)
            page.locator("#shot").screenshot(path=str(out_path))
            browser.close()
    out_path.with_suffix(".txt").write_text(session, encoding="utf-8")
    return out_path


def _terminal_html(session_text: str, *, title: str) -> str:
    safe = html.escape(session_text)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  html, body {{ margin: 0; background: #0f1419; }}
  .frame {{
    width: 1100px; margin: 24px auto; border-radius: 12px; overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,.45); border: 1px solid #2a3340;
    font-family: "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  }}
  .bar {{
    background: #1b2330; color: #9aa7b8; padding: 10px 14px; font-size: 13px;
    display: flex; gap: 8px; align-items: center;
  }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
  .dot.r {{ background: #ff5f56; }} .dot.y {{ background: #ffbd2e; }} .dot.g {{ background: #27c93f; }}
  .body {{
    background: #0b121a; color: #d7e0ea; padding: 18px 20px 28px;
    font-size: 15px; line-height: 1.45; white-space: pre-wrap;
  }}
  .label {{ color: #6f879e; margin-bottom: 10px; }}
</style></head>
<body>
  <div class="frame" id="shot">
    <div class="bar">
      <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
      <span>{html.escape(title)}</span>
    </div>
    <div class="body"><div class="label"># Track A — real Unix</div>{safe}</div>
  </div>
</body></html>
"""


def capture_real_shell_frame(
    *,
    example_dir: Path,
    out_path: Path,
    commands: list[str],
    title: str,
    width: int,
    height: int,
) -> Path:
    session = _run_real_shell_session(example_dir, commands)
    return _frame_session_text(
        session, out_path=out_path, title=title, width=width, height=height
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module_dir", type=Path)
    parser.add_argument(
        "--example-subdir",
        default="navigation",
        help="Subfolder under examples/ (default: navigation)",
    )
    parser.add_argument(
        "--commands",
        default=",".join(DEFAULT_COMMANDS),
        help="Comma-separated commands to run (cwd = example dir)",
    )
    parser.add_argument(
        "--bash-script",
        type=Path,
        default=None,
        help="Run this bash script instead of --commands (stdout = session frame)",
    )
    parser.add_argument(
        "--session-text",
        type=Path,
        default=None,
        help="Frame an existing session transcript (.txt) instead of running commands",
    )
    parser.add_argument("--name", default="real-shell.png", help="Output under assets/")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=900)
    args = parser.parse_args(argv)

    module_dir = args.module_dir.resolve()
    example_dir = module_dir / "examples" / args.example_subdir

    _ensure_playwright()
    out_path = module_dir / "assets" / args.name
    title = f"wsl — {module_dir.name}/examples/{args.example_subdir}"
    print(f"Capturing real shell session -> {out_path}")

    if args.session_text is not None:
        text_path = args.session_text
        if not text_path.is_file():
            text_path = module_dir / args.session_text
        if not text_path.is_file():
            raise SystemExit(f"Missing session text: {args.session_text}")
        session = text_path.read_text(encoding="utf-8")
        if not session.endswith("\n"):
            session += "\n"
        _frame_session_text(
            session, out_path=out_path, title=title, width=args.width, height=args.height
        )
    elif args.bash_script is not None:
        script_path = args.bash_script
        if not script_path.is_file():
            script_path = module_dir / args.bash_script
        if not script_path.is_file():
            raise SystemExit(f"Missing bash script: {args.bash_script}")
        session = _run_bash_script_file(
            script_path.resolve(),
            example_dir if example_dir.is_dir() else None,
        )
        _frame_session_text(
            session, out_path=out_path, title=title, width=args.width, height=args.height
        )
    else:
        if not example_dir.is_dir():
            raise SystemExit(f"Missing example dir: {example_dir}")
        commands = [
            c.strip().encode("utf-8").decode("unicode_escape")
            if "\\n" in c or "\\t" in c
            else c.strip()
            for c in args.commands.split(",")
            if c.strip()
        ]
        if not commands:
            raise SystemExit("Need at least one command in --commands")
        capture_real_shell_frame(
            example_dir=example_dir,
            out_path=out_path,
            commands=commands,
            title=title,
            width=args.width,
            height=args.height,
        )
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
