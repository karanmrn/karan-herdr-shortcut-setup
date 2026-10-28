# Global agent instructions

Shared by Claude Code, Codex, opencode, and grok via symlink.

Source of truth: `~/.dotfiles-karan/home/.config/agents/AGENTS.md`

---

## Writing

- Never use the em dash. Use a plain dash instead.
- Never add your agent name as a commit co-author.
- Never manually modify CHANGELOG.md or any file marked auto-generated.

## Technical judgment

- When making technical decisions, do not give much weight to development cost.
  Prefer quality, simplicity, robustness, scalability, and long-term maintainability.
- For one-off or infrequent operational work, start with the simplest direct
  end-to-end path. Do not build wrappers, control planes, policy layers, custom
  verifiers, or automation unless the direct path exposes a concrete blocker or
  repeated need that justifies it.

## Bug fixing

- Always start by reproducing the bug end-to-end, as closely to how a real user
  would hit it as possible. This confirms you found the real cause, so the fix
  actually works.

## Quality bar

- When end-to-end testing a product, be picky about the UI and obsessed with
  pixel perfection. If something clearly looks off, get it fixed even when it is
  unrelated to the current task.
- Apply the same standard to lint errors, test failures, and test flakiness. If
  you see one, get it fixed even when it is not caused by current work.

## Swarm safety

- Before using dynamic workflows, ultra code, or any feature that immediately
  spawns a large swarm of subagents, explain the tradeoffs and ask for explicit
  approval.

---

## Engineering skills

Read the matching SKILL.md before applying a playbook. Prefer project skills in
`.agents/skills/`, then shared skills in `~/.agents/skills/`, then the active
harness or plugin catalog. Resolve symlinks before updating an installed skill.
Project AGENTS.md and explicit user scope govern how a playbook is applied.

| Skill | When |
| --- | --- |
| `to-spec` | Publish an agreed specification when issue creation is requested |
| `implement-spec` | Execute an existing specification |
| `tdd` | Implement a feature or bug fix |
| `diagnosing-bugs` | Reproduce and diagnose broken or slow behaviour |
| `new-feature` | Create isolation when the harness has not supplied it |
| `codebase-design` | Resolve duplication, ownership or module boundaries |
| `code-review` | Review a diff and trace its reachable behaviour |
| `jev` | Advise on an ambiguous semantic review judgment |
| `verification-before-completion` | Verify evidence before claiming success |
| `domain-modeling` | Define domain terminology and decisions |
| `technical-writing` | Write developer documentation |
| `unslop` | Check prose before delivering it |

Load only the playbooks needed for the task. If a named skill is absent, search
the installed catalog once and report the missing dependency. Do not install a
whole collection to recover one skill. Preserve custom skills during updates;
quarantine proven duplicates outside discovery roots with a restore manifest.

Jev is an optional review adviser. Use it only when observed evidence leaves an
ambiguous semantic judgment. Never send it deterministic checks such as builds,
types, lint, tests, exact policy matches, file equality, or schema validation.
Its typed answer and probability are supporting evidence, never a verdict, gate,
or reason to waive verification. Missing credentials must not block review.

Read `jev` and `typesafe-ai` before a call. Use `TYPESAFE_API_KEY` only when it is
already available through the environment or Keychain. Never print, persist,
log, paste, or commit the secret.

---

## Response style (Simplified Technical English)

Use the `asd-ste100` skill for plans, implementation updates, instructions and
reports to the user. Read `~/.codex/skills/asd-ste100/SKILL.md` before applying it.
This preference replaces the previous caveman style.

- Use complete sentences with explicit subjects, verbs and articles.
- Use plain words and active voice. Keep technical names exact.
- Give one instruction per sentence. Keep descriptions to one clear idea.
- Prefer at most 20 words per instruction and 25 words per description.
- Preserve facts, uncertainty, conditions and exceptions when simplifying text.
- Do not use semicolons or an em dash.
- Use numbered steps for procedures with three or more actions.
- Keep creative and marketing copy in the product's established voice.
- Do not claim certified ASD-STE100 dictionary compliance.
