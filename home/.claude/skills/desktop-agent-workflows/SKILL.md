---
name: desktop-agent-workflows
description: Explain Karan's desktop terminal, agent harnesses, model launchers, Herdr, and FirstMate setup. Use when he asks how his local agents run, where terminal work happens, or what recent work is about.
---

# Desktop agent workflows

## Keep the harness and model separate

The user can run a harness and select a model through that harness or its proxy. Do not infer the active model from the terminal name or from this Codex conversation.

- This Codex desktop conversation is its own harness session. A terminal command cannot change its model.
- The `openrouter` command lists models exposed by a local proxy and launches a new Claude Code terminal session with the selected model.
- `aim <model>` starts a new Claude Code terminal session through the same local proxy without the picker.
- The user commonly selects a DeepSeek model through this route. Check the current model list when an exact ID matters.
- The proxy endpoint is `http://127.0.0.1:8317`. Do not assume every listed model uses an OpenRouter provider route without checking the proxy configuration or request.
- Credentials stay in the local secret store. Never print or copy their values.

For OpenRouter application integrations, use the `openrouter` skill. Inspect the actual request and SDK before changing an application route.

## Understand the terminal entry points

The shell is zsh. WezTerm, Ghostty, and cmux provide terminal windows. Their shared theme and key settings live in the dotfiles repository.

- `fm` enters `~/karan-agent-workspace` and starts Claude Code as the FirstMate session.
- FirstMate is an agent distribution and coordinator. It uses isolated worktrees and a visible terminal backend such as Herdr. It is not a model or a harness.
- Herdr manages terminal workspaces, tabs, panes, and recognized agents. The prefix is Ctrl+B. Read the `herdr` skill before controlling a session. Herdr control requires `HERDR_ENV=1`.
- `co` launches Codex with workspace-write access and approval prompts disabled. Do not use it unless the user chose that execution mode.
- `cc` launches Claude Code with permission checks disabled. Do not use it unless the user chose that execution mode.
- `/shell` is a separate explicit command that runs the user's following text literally. Follow its own skill only when invoked.

The primary FirstMate workspace is `~/karan-agent-workspace`. Its README and AGENTS.md explain the current coordinator contract. Read them before changing FirstMate behavior.

## Recognize the user's work

The user's main product is PUBMAXX, a London value-for-money food and drinks guide. The code repository is `~/code/projects/pubmaxx`. The user often works in managed worktrees because many tasks can touch the same repository.

Recent work themes include pub discovery and maps, PubPal chat and search, price and source evidence, product copy and visuals, release checks, and preview or deployment identity. FirstMate's own agent-coordination workflow is another active area.

Treat these themes as context, not proof of current status. Before continuing a task, inspect the current thread, worktree, branch, uncommitted files, PR head, and deployment evidence that apply. Do not infer that a merge deployed, that a preview matches the latest commit, or that a local task is safe to replace. Preserve user changes and existing worktree ownership.

## Report the execution path clearly

When explaining a terminal action, state which harness starts, which model route it uses, and whether it starts a new session. Keep model IDs and local paths exact in written instructions when they matter. Never imply that changing a terminal model changes a separate Codex conversation.
