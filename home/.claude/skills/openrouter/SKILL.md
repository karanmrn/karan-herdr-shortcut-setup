---
name: openrouter
description: List, ask, compare and launch OpenRouter models from the shell. Use when the user types /openrouter, asks which models exist or what they cost, wants one answer from a named non-Claude model, wants two models compared on one prompt, or wants to start a coding session on another model.
license: MIT
---

# OpenRouter

`scripts/openrouter` (in this skill's folder) calls `https://openrouter.ai/api/v1` directly. It needs only `python3`. Below, `openrouter` means that script.

**Every `ask` and `compare` spends credit on the user's OpenRouter account.** `list` and `launch` are free. Before a paid call, check the price with `list`. Add `--max-tokens` to put a limit on the reply. Use a `:free` model when the task permits.

## Key

The CLI reads `OPENROUTER_API_KEY` from the environment. If that is empty, it reads the file named by `OPENROUTER_KEY_FILE`. The file holds the bare key or a `.env` line `OPENROUTER_API_KEY=<key>`.

The key is a secret. Keep it out of commands, output, logs and commits. Refer to it only as `$OPENROUTER_API_KEY`.

## Commands

```bash
openrouter list [filter]                     # id, context, $/M in, $/M out, free marker
openrouter ask <model> "<prompt>"            # streams the reply; tokens and cost go to stderr
openrouter ask <model> - < handoff.md        # "-" reads the prompt from stdin
openrouter compare <m1> <m2> "<prompt>"      # both replies side by side
openrouter launch <model> [--tool claude|codex|env]   # prints the session command
```

Run `openrouter <command> --help` for all flags.

## Procedure

1. Run `list` with a filter. Show the user a short, relevant subset, not hundreds of rows.
2. If the user named a task, recommend two or three models. Give one line each on why, with the price.
3. For one answer now, run `ask`. Tell the user the cost from the stderr line.
4. To choose between models, run `compare` on one representative prompt.
5. For a coding session, run `launch` and give the user the printed command.

A running session keeps its model. `launch` only prints a command that starts a **new** session. The user runs it in another terminal.

## Launch notes

- Claude Code talks to OpenRouter's Anthropic-compatible endpoint. It warns that it does not know the model's context window. The session still works.
- Codex CLI uses the Responses API through `-c` overrides. Codex sends its full system prompt and project instructions, so even a short task can use many prompt tokens.
- A model without tool calling cannot drive a coding agent. `launch` prints a warning for such a model.
- OpenCode reads models from its own catalog, which can lag OpenRouter. Run `opencode models openrouter` to see what it accepts.

## Errors

| Message | Cause |
|---|---|
| `no API key` | Set `OPENROUTER_API_KEY` or `OPENROUTER_KEY_FILE`. |
| `HTTP 401` | The key is not valid or was revoked. |
| `HTTP 402` | The account or the key has no credit left. Tell the user. Do not retry. |
| `unknown model` | The id changed or the model was retired. Run `list` with a filter. |
