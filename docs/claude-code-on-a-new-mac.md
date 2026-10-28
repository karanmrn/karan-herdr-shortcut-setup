# Claude Code on a new Mac

This guide explains how Claude Code (`cc`) runs on the main Mac. Use it to set
up a second Mac, such as a MacBook Air, the same way.

The facts come from this repository, `~/.claude/settings.json`, the installed
plugins under `~/.claude/plugins`, and the
[desktop-agent-workflows skill](../home/.claude/skills/desktop-agent-workflows/SKILL.md).
Read the [setup guide](setup-guide.md) for terminals, keyboard shortcuts and
the FirstMate roles.

---

## 1. The big picture

Three layers work together:

| Layer | What it is | Where it lives |
|---|---|---|
| Harness | The agent program, such as Claude Code or Codex | Homebrew, npm |
| Instructions and skills | Shared rules and playbooks that every harness reads | This repo, `~/.agents/skills` |
| FirstMate | A coordinator that runs a crew of agents in Herdr | `~/karan-agent-workspace` |

You talk to one Claude Code session, FirstMate. FirstMate starts workers in
Herdr tabs. Each worker gets its own git worktree. See
[section 6 of the setup guide](setup-guide.md#6-firstmate-and-crewmates---how-the-agents-fit-together).

---

## 2. What to install

These harnesses and tools are installed and configured on the main Mac.

| Tool | Install on the main Mac | Notes |
|---|---|---|
| Claude Code | `brew install --cask claude-code@latest` | The `claude` command |
| Codex | `npm install -g @openai/codex` | npm prefix is `~/.local` |
| Herdr | `brew install herdr` | Terminal workspaces for agents |
| GitHub CLI | `brew install gh` | Run `gh auth login` once |
| WezTerm | `brew install --cask wezterm` | Main terminal app |
| cliproxyapi | `brew install cliproxyapi` | Local model proxy on port 8317 |
| Starship, zsh plugins | in the `Brewfile` | Prompt and shell |

Other harnesses also have shared instructions linked by `install.sh`:
opencode (`~/.opencode/bin`) and grok (`~/.grok/bin`). Install them only if you
use them.

The AXI command-line tools are in `~/.local/bin`: `gh-axi`, `chrome-devtools-axi`,
`quota-axi` and `tasks-axi`. `treehouse` (worktree pool) is also there.
`no-mistakes` (the PR validation pipeline) lives in `~/.no-mistakes/bin`.
FirstMate offers to install the tools that it needs, after you approve.

`jq` comes with macOS at `/usr/bin/jq`. The status line and the model
launchers need it.

To restore every Homebrew package from the main Mac, run
`brew bundle install --file=Brewfile`. This step is optional. It never removes
a package.

---

## 3. What install.sh does for Claude Code

`install.sh` makes symlinks from your home folder into this repo. It backs up
anything that it replaces to `<name>.pre-dotfiles-YYYYMMDD-HHMMSS`. It is safe to
run more than once.

| Link in your home folder | Repo file |
|---|---|
| `~/.claude/CLAUDE.md` | `home/.config/agents/AGENTS.md` |
| `~/.codex/AGENTS.md` | `home/.config/agents/AGENTS.md` |
| `~/.config/opencode/AGENTS.md` | `home/.config/agents/AGENTS.md` |
| `~/.grok/AGENTS.md` | `home/.config/agents/AGENTS.md` |
| `~/.config/agents/AGENTS.md` | `home/.config/agents/AGENTS.md` |
| `~/.claude/statusline.sh` | `home/.claude/statusline.sh` |
| `~/.claude/skills/desktop-agent-workflows` | `home/.claude/skills/desktop-agent-workflows` |
| `~/.claude/skills/openrouter` | `home/.claude/skills/openrouter` |
| `~/.cursor/rules/jev-review.mdc` | `home/.cursor/rules/jev-review.mdc` |
| `~/.local/bin/openrouter` | `home/.local/bin/openrouter` |
| `~/.zshrc`, `~/.zshenv` | `home/.zshrc`, `home/.zshenv` |

One file, `AGENTS.md`, gives Claude Code, Codex, opencode and grok the same
engineering rules. Edit it once and every harness reads the change.

`install.sh` also adds one hook line to `~/.zprofile`. That line loads
`home/firstmate-env.zsh`, which sets `FM_WORKSPACE`, `FM_HOME` and `FM_BACKEND`.
The hook expects the repo at `~/.dotfiles-karan`. Clone it there.

`install.sh` does not write `~/.claude/settings.json`. Section 5 tells you what
to set by hand.

---

## 4. Skills

A skill is a folder with a `SKILL.md` playbook. The shared `AGENTS.md` tells
each agent where to look, in this order:

1. Project skills in `<repo>/.agents/skills/`.
2. Shared skills in `~/.agents/skills/`.
3. The harness or plugin catalogue.

On the main Mac, `~/.agents/skills/` holds the catalogue, about 300 skills.
Most entries in `~/.claude/skills/` are symlinks into `~/.agents/skills/`, so
Claude Code and Codex see the same skills.

The `skills` CLI installs these skills from GitHub, for example
`npx skills add <owner>/<repo>`. It records each source in
`~/.agents/.skill-lock.json`. The largest sources are:

| Source | Examples |
|---|---|
| `backnotprop/pstack` | `architect`, `council` |
| `mattpocock/skills` | `tdd`, `grilling`, `codebase-design` |
| `addyosmani/agent-skills` | `code-review-and-quality`, `context-engineering` |
| `obra/superpowers` | `brainstorming`, `systematic-debugging` |
| `emilkowalski/skills` | `animate`, `emil-design-eng` |
| `kunchenguid/*` | `no-mistakes`, `quota-axi`, `tasks-axi`, `vision` |

To copy the catalogue, copy `~/.agents/.skill-lock.json` from the main Mac.
Then install each source again with the `skills` CLI.

This repo publishes two skills of its own:

- `desktop-agent-workflows` explains the terminals, launchers, Herdr and FirstMate.
- `openrouter` explains the local model proxy and OpenRouter integrations.

On the main Mac these two skills are real folders in `~/.agents/skills/`. A new
Mac gets them from `install.sh` as links into this repo.

The FirstMate workspace brings its own skills in
`~/karan-agent-workspace/.agents/skills/`.

---

## 5. Claude Code settings

Set these in `~/.claude/settings.json` on the new Mac. The main Mac uses them.

### Status line

```json
"statusLine": { "type": "command", "command": "bash ~/.claude/statusline.sh", "padding": 0 }
```

The script shows model, folder, branch, context, cost and provider quota. It
calls `quota-axi` in the background.

### Environment and permissions

- `env.ENABLE_TOOL_SEARCH` is set.
- `permissions.defaultMode` is `auto`.
- `skipDangerousModePermissionPrompt` is `true`, because `cc` runs
  `claude --dangerously-skip-permissions`.

### Plugins

Add these marketplaces under `extraKnownMarketplaces`, then install plugins
with `/plugin` inside Claude Code.

| Marketplace | Source | Plugin | Enabled |
|---|---|---|---|
| `caveman` | `JuliusBrussee/caveman` | `caveman` | yes |
| `openai-codex` | `openai/codex-plugin-cc` | `codex` | yes |
| `compact-adviser` | `kunchenguid/compact-adviser` | `compact-adviser` | no |
| `typesafe-ai` | `typesafe-ai/skills` | `typesafe` | no |
| `mattpocock` | `mattpocock/skills` | `mattpocock-skills` | no |
| `ecc` | `affaan-m/everything-claude-code` | `ecc` | no |
| `compound-engineering-plugin` | `EveryInc/compound-engineering-plugin` | `compound-engineering` | no |

### MCP servers

These MCP servers are in the user scope of `~/.claude.json`. Add them with
`claude mcp add`. Each one signs in on first use. No token is stored in this
repo.

| Server | Type |
|---|---|
| `posthog` | HTTP |
| `tinyfish` | HTTP |
| `superlogical` | HTTP |
| `mempalace` | local command `~/.local/bin/mempalace-mcp` |

The claude.ai connectors (for example Gmail, Slack, Notion and Vercel) come
from your claude.ai account. They appear when you sign in.

### Hooks

Hooks run on Claude Code events. Other programs install them. Do not copy them
by hand.

| Hook | Installed by | What it does |
|---|---|---|
| `~/.claude/hooks/herdr-agent-state.sh` | `herdr integration install` | Tells Herdr the agent state |
| `chrome-devtools-axi` on `SessionStart` | added for the `chrome-devtools-axi` CLI | Prints the browser session state |
| `orca/agent-hooks/claude-hook.sh` on most events | the Orca app | Reports agent events to Orca |
| `~/.fermat/hooks/*.mjs` | the Fermat app | Does nothing unless a Fermat session is active |

FirstMate adds its own hooks inside each worker worktree in
`.claude/settings.local.json`. You do not set those.

---

## 6. FirstMate and Herdr

FirstMate is the repo `karanmrn/firstmate`, a fork of `kunchenguid/firstmate`.
It is not an app. The cloned repo is the coordinator.

```sh
gh repo clone karanmrn/firstmate ~/karan-agent-workspace
```

How the captain uses it:

1. Open WezTerm and start Herdr with `herdr`.
2. Type `fm`. It changes to `~/karan-agent-workspace` and starts Claude Code.
3. Talk to FirstMate. It plans and sends tasks to crewmates.
4. Each crewmate runs in its own Herdr tab and git worktree.
5. FirstMate reports finished pull requests to you. You decide merges.

`config/backend` in the workspace selects `herdr`. The Herdr prefix key is
Ctrl+B. See the [Herdr shortcuts](setup-guide.md#herdr-panes-and-workspaces-inside-the-terminal).

FirstMate state, such as briefs, status files and task data, stays in the
workspace. It is not part of this repo.

---

## 7. Keys and secrets

No key, token or password goes in this repo. `.gitignore` blocks `*.env`,
`secrets/` and key files.

| Secret | Where it lives | Read by |
|---|---|---|
| `TINYFISH_API_KEY` | macOS Keychain item `tinyfish-api-key` | `~/.zshrc` |
| `TYPESAFE_API_KEY` | environment or Keychain | Jev and TypeSafe skills |
| Proxy token `ANTHROPIC_AUTH_TOKEN` | `~/.config/secrets/claudex.env`, mode 600 | `claudex`, `aim`, `openrouter` |
| Fleet keys | `~/karan-agent-workspace/data/keys.env`, mode 600 | FirstMate and crewmates |
| Anthropic API key for `claude-pubmaxx` | OpenCode `auth.json` | `claude-pubmaxx` |

`data/keys.env` is one `NAME=value` per line. The FirstMate repo ignores the
`data/` folder, so the file is never committed.

To store the TinyFish key in Keychain, run this command. It asks for the value.

```sh
security add-generic-password -a "$USER" -s tinyfish-api-key -w
```

Clone FirstMate as section 6 shows before creating `data/keys.env`.
Create `claudex.env` and `keys.env` by hand on the new Mac. Then run
`chmod 600` on each file. Do not send their contents through chat, email or a
pull request.

---

## 8. First hour on the MacBook Air

1. Install Homebrew, then run `brew install gh git node`.
2. Run `gh auth login`.
3. Clone this repo: `gh repo clone karanmrn/karan-herdr-shortcut-setup ~/.dotfiles-karan`.
4. Run `~/.dotfiles-karan/install.sh`. Read the `backup` lines it prints.
5. Run `brew install --cask claude-code@latest wezterm` and `brew install herdr starship zsh-autosuggestions zsh-syntax-highlighting`.
6. Run `npm config set prefix ~/.local`, then `npm install -g @openai/codex`.
7. Open a new WezTerm tab. Check that `type cc fm aim` finds all three.
8. Run `claude` once and sign in.
9. Edit `~/.claude/settings.json` as section 5 shows: status line, marketplaces, plugins.
10. Add the MCP servers from section 5 with `claude mcp add`.
11. Install the shared skills into `~/.agents/skills` with the `skills` CLI.
12. Clone FirstMate: `gh repo clone karanmrn/firstmate ~/karan-agent-workspace`.
13. Store keys as section 7 shows: Keychain item, `claudex.env`, `keys.env`.
14. Run `herdr integration install claude`. Repeat with `codex` if you use Codex in Herdr.
15. Start `herdr`, then type `fm`. Ask FirstMate to check its toolchain.

When FirstMate answers and lists its tools, the new Mac matches the main Mac.
