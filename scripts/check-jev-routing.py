#!/usr/bin/env python3
"""Regression check for global Jev and TypeSafe discovery and routing."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import time


HOME = Path.home()
REPO = HOME / ".dotfiles-karan"
AGENTS_SOURCE = REPO / "home/.config/agents/AGENTS.md"
CURSOR_RULE_SOURCE = REPO / "home/.cursor/rules/jev-review.mdc"
SHARED_SKILLS = HOME / ".agents/skills"


def fail(message: str) -> None:
    raise AssertionError(message)


def require_text(path: Path, fragments: list[str]) -> None:
    text = path.read_text()
    for fragment in fragments:
        if fragment not in text:
            fail(f"{path}: missing {fragment!r}")


def require_target(path: Path, target: Path) -> None:
    if not path.is_symlink():
        fail(f"{path}: expected symlink")
    if path.resolve() != target.resolve():
        fail(f"{path}: resolves to {path.resolve()}, expected {target.resolve()}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receive(process: subprocess.Popen[str], request_id: int, timeout: int = 120) -> dict:
    deadline = time.time() + timeout
    assert process.stdout is not None
    while time.time() < deadline:
        ready, _, _ = select.select([process.stdout], [], [], min(1, deadline - time.time()))
        if not ready:
            continue
        line = process.stdout.readline()
        if not line:
            break
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("id") == request_id:
            return message
    fail(f"codex app-server: no response for request {request_id}")
    return {}


def send(process: subprocess.Popen[str], message: dict) -> None:
    assert process.stdin is not None
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()


def check_codex_discovery(cwds: list[str]) -> list[dict]:
    process = subprocess.Popen(
        ["codex", "app-server", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    try:
        send(
            process,
            {
                "id": 0,
                "method": "initialize",
                "params": {
                    "clientInfo": {"name": "check-jev-routing", "version": "1"},
                    "capabilities": {"experimentalApi": True},
                },
            },
        )
        receive(process, 0)
        send(process, {"method": "initialized", "params": {}})
        send(
            process,
            {
                "id": 1,
                "method": "skills/list",
                "params": {"cwds": cwds, "forceReload": True},
            },
        )
        response = receive(process, 1)
    finally:
        process.terminate()

    if response.get("error"):
        fail(f"codex skills/list: {response['error']}")
    groups = response.get("result", {}).get("data", [])
    if len(groups) != len(cwds):
        fail(f"codex skills/list: expected {len(cwds)} groups, got {len(groups)}")
    expected_paths = {
        "jev": str(SHARED_SKILLS / "jev/SKILL.md"),
        "typesafe-ai": str(SHARED_SKILLS / "typesafe-ai/SKILL.md"),
    }
    summaries = []
    for group in groups:
        errors = group.get("errors", [])
        if errors:
            fail(f"{group.get('cwd')}: discovery errors: {errors}")
        matches = {
            skill["name"]: skill
            for skill in group.get("skills", [])
            if skill.get("name") in expected_paths and skill.get("enabled")
        }
        if set(matches) != set(expected_paths):
            fail(f"{group.get('cwd')}: missing user Jev/TypeSafe skills")
        for name, expected in expected_paths.items():
            skill = matches[name]
            if skill.get("path") != expected or skill.get("scope") != "user":
                fail(f"{group.get('cwd')}: wrong {name} discovery record: {skill}")
        summaries.append(
            {
                "cwd": group.get("cwd"),
                "skills": len(group.get("skills", [])),
                "errors": len(errors),
            }
        )
    return summaries


def main() -> None:
    require_text(
        AGENTS_SOURCE,
        [
            "Jev is an optional review adviser.",
            "Never send it deterministic checks",
            "Never print, persist,",
        ],
    )
    require_text(
        CURSOR_RULE_SOURCE,
        [
            "only for ambiguous semantic judgments during review",
            "supporting evidence, never verdicts",
            "Never print, persist,",
        ],
    )

    for path in [AGENTS_SOURCE, CURSOR_RULE_SOURCE]:
        text = path.read_text()
        if "TYPESAFE_API_KEY=" in text or "Authorization: Bearer" in text:
            fail(f"{path}: possible credential literal")

    for relative in [
        ".claude/CLAUDE.md",
        ".codex/AGENTS.md",
        ".config/opencode/AGENTS.md",
        ".grok/AGENTS.md",
    ]:
        require_target(HOME / relative, AGENTS_SOURCE)
    require_target(HOME / ".cursor/rules/jev-review.mdc", CURSOR_RULE_SOURCE)

    jev_owner = SHARED_SKILLS / "jev"
    typesafe_owner = SHARED_SKILLS / "typesafe-ai"
    for root in [".claude/skills", ".cursor/skills", ".config/opencode/skills", ".grok/skills"]:
        require_target(HOME / root / "jev", jev_owner)
    for root in [".cursor/skills", ".config/opencode/skills", ".grok/skills"]:
        require_target(HOME / root / "typesafe-ai", typesafe_owner)

    official = sorted(
        (HOME / ".claude/plugins/cache/typesafe-ai/typesafe").glob(
            "*/skills/typesafe-ai/SKILL.md"
        )
    )
    if not official:
        fail("Claude TypeSafe plugin skill not found")
    if digest(typesafe_owner / "SKILL.md") not in {digest(path) for path in official}:
        fail("shared TypeSafe skill differs from installed official plugin")

    summaries = check_codex_discovery([str(Path.cwd()), str(HOME)])
    print(json.dumps({"ok": True, "codex": summaries}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
