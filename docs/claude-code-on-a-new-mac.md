# Claude Code on a new Mac

This guide explains how Claude Code (`cc`) runs on the main Mac. Use it to set
up a second Mac, such as a MacBook Air, the same way.

The facts come from this repository, `~/.claude/settings.json`, the installed
plugins under `~/.claude/plugins`, the FirstMate home in `~/karan-agent-workspace`,
and the
[desktop-agent-workflows skill](../home/.claude/skills/desktop-agent-workflows/SKILL.md).
They were last checked on the main Mac (the Mac Studio) on 6 Nov 2026.
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
| LM Studio | `brew install --cask lm-studio` | Local models, see [section 7](#7-models) |
| Starship, zsh plugins | in the `Brewfile` | Prompt and shell |

Other harnesses also have shared instructions linked by `install.sh`:
opencode (`~/.opencode/bin`) and grok (`~/.grok/bin`). Install them only if you
use them. The main Mac also has `cursor-agent`, `pi` and `hermes` in
`~/.local/bin`. Kimi is not installed on the main Mac.

The AXI command-line tools are in `~/.local/bin`: `gh-axi`, `chrome-devtools-axi`,
`quota-axi` and `tasks-axi`. `treehouse` (worktree pool) is also there.
`no-mistakes` (the PR validation pipeline) lives in `~/.no-mistakes/bin`.
FirstMate offers to install the tools that it needs, after you approve.

The main Mac no longer runs `cliproxyapi`, the local model proxy on port 8317.
It stays in the `Brewfile` because this repo never removes a package. You do
not need it on a new Mac. See [section 7](#7-models) for the commands that
still expect it.

`jq` comes with macOS at `/usr/bin/jq`. The status line and the model
launchers need it.

To restore every Homebrew package from the main Mac, run
`brew bundle install --file=Brewfile`. This step is optional. It never removes
a package.

---

## 3. What install.sh does for Claude Code

See the [README installation instructions](../README.md#install-on-a-new-mac)
for backup behaviour and common usage. The Claude Code setup includes these
links:

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

The `openrouter` links come from an older setup that used the local proxy.
On the main Mac, `~/.claude/skills/openrouter` now points to the kstack copy in
`~/.agents/skills/openrouter`. See [section 7](#7-models).

`install.sh` also adds one hook line to `~/.zprofile`. That line loads
`home/firstmate-env.zsh`, which sets `FM_WORKSPACE`, `FM_HOME` and `FM_BACKEND`.
The hook expects the repo at `~/.dotfiles-karan`. Clone it there.

`install.sh` does not write `~/.claude/settings.json`. Section 5 tells you what
to set by hand.

---

## 4. Skills

A skill is a folder with a `SKILL.md` playbook. The
[shared agent instructions](../home/.config/agents/AGENTS.md#engineering-skills)
define the skill lookup order.

### The skill policy

The fleet uses a lean skill policy. It keeps the skills from five families,
plus a short list of approved extras:

| Family | Source repo |
|---|---|
| Addy Osmani | `addyosmani/agent-skills` |
| pstack | `backnotprop/pstack` |
| tstack | `t3dotgg/tstack` |
| Matt Pocock | `mattpocock/skills` |
| Kun Chen | `kunchenguid/*`, for example `no-mistakes`, `quota-axi`, `tasks-axi` |

[kstack](https://github.com/karanmrn/kstack) is the published pack of these
five families. It also holds the fleet's own workflow skills, such as
`openrouter`, `delegate-to-model` and `supervise-agent-fleet`.

`asd-ste100` is one approved extra. It sets the response style, see
[Response style](#response-style). The duplicate skills from
`kunchenguid/grok-ship` are removed. Three grok-ship skills that have no
duplicate stay installed: `ahoy`, `14-day-stale-pr-close` and
`vision-md-triage-verdict`.

### Install the skills

The `skills` CLI installs skills from GitHub into `~/.agents/skills/` and
records each source in `~/.agents/.skill-lock.json`. The `-g` flag makes the
installation available across projects. See the
[CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add).

Install kstack, then the style skill:

```sh
npx skills add -g karanmrn/kstack
npx skills add -g danyuchn/asd-ste100-skill
```

To see the skills before you install them, add `--list`. When the CLI asks for
agents, select every harness that you use.

### Where each harness finds the skills

`~/.agents/skills/` is the one real copy. Each harness has a skills folder
with a symlink per skill into `~/.agents/skills/`:

| Harness | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| opencode | `~/.config/opencode/skills/` |
| pi | `~/.pi/agent/skills/` |
| grok | `~/.grok/skills/` |
| hermes | `~/.hermes/skills/` |

If you install kimi, link its skills folder in the same way.

### Skills from this repo and from FirstMate

This repo publishes `desktop-agent-workflows`. It explains the terminals,
launchers, Herdr and FirstMate. `install.sh` links it into `~/.claude/skills/`.

The FirstMate workspace brings its own skills in
`~/karan-agent-workspace/.agents/skills/`.

---

## 5. Claude Code settings

Set these in `~/.claude/settings.json` on the new Mac. The main Mac uses them.

### Status line

```json
{
  "statusLine": { "type": "command", "command": "bash ~/.claude/statusline.sh", "padding": 0 }
}
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
| `caveman` | `JuliusBrussee/caveman` | `caveman` | no |
| `openai-codex` | `openai/codex-plugin-cc` | `codex` | yes |
| `compact-adviser` | `kunchenguid/compact-adviser` | `compact-adviser` | no |
| `typesafe-ai` | `typesafe-ai/skills` | `typesafe` | no |
| `mattpocock` | `mattpocock/skills` | `mattpocock-skills` | no |
| `ecc` | `affaan-m/everything-claude-code` | `ecc` | no |
| `compound-engineering-plugin` | `EveryInc/compound-engineering-plugin` | `compound-engineering` | no |

Only `codex` is enabled. The other plugins are installed but turned off in
`enabledPlugins`.

### Response style

Agents answer in plain English that follows the `asd-ste100` skill
(Simplified Technical English). The rule is in the
[shared agent instructions](../home/.config/agents/AGENTS.md#response-style-simplified-technical-english),
so every harness gets it through `install.sh`.

This style replaces the caveman style. Keep the caveman plugin turned off:

```json
{
  "enabledPlugins": { "caveman@caveman": false }
}
```

### MCP servers

These MCP servers are in the user scope of `~/.claude.json`. The commands
below use `--scope user` so every project can use them. See the
[Claude Code MCP guide](https://code.claude.com/docs/en/mcp#user-scope).
No token is stored in this repo.

| Server and setup instructions | Connection |
|---|---|
| [PostHog](https://posthog.com/docs/model-context-protocol) | HTTP: `https://mcp.posthog.com/mcp` |
| [TinyFish](https://docs.tinyfish.ai/mcp-integration) | HTTP: `https://agent.tinyfish.ai/mcp` |
| [Superlogical](https://www.superlogical.com/rex/docs/beta/community-mcp) | HTTP: `https://www.superlogical.com/rex/community-mcp` |
| [MemPalace](https://mempalaceofficial.com/guide/getting-started#installation) | Local command: `~/.local/bin/mempalace-mcp` |

Register the HTTP servers:

```sh
claude mcp add --scope user --transport http posthog https://mcp.posthog.com/mcp
claude mcp add --scope user --transport http tinyfish https://agent.tinyfish.ai/mcp
claude mcp add --scope user --transport http superlogical https://www.superlogical.com/rex/community-mcp
```

Open `/mcp` inside Claude Code to authenticate each HTTP server.
Superlogical requires membership in the Rex Beta Discord server.

For MemPalace, follow the linked installation instructions before registering
the local executable. They cover the Python prerequisite and installation
with `uv tool install mempalace`. Then run:

```sh
claude mcp add --scope user --transport stdio mempalace "$HOME/.local/bin/mempalace-mcp"
```

If your installer uses another directory, replace the executable path with
the absolute path from `command -v mempalace-mcp`. Local MemPalace requires
no account sign-in.

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
It is not an app. The cloned repo is the coordinator, and its folder is the
FirstMate home.

```sh
gh repo clone karanmrn/firstmate ~/karan-agent-workspace
```

`gh repo clone` adds the parent repo as the `upstream` remote. The main Mac
merges upstream changes into the fork. To check the remotes, run
`git -C ~/karan-agent-workspace remote -v`.

How the captain uses it:

1. Open WezTerm and start Herdr with `herdr`.
2. Type `fm`. It changes to `~/karan-agent-workspace` and starts Claude Code.
3. Talk to FirstMate. It plans and sends tasks to crewmates.
4. Each crewmate runs in its own Herdr pane, in a git worktree from the
   treehouse pool.
5. FirstMate reports finished pull requests to you. You decide merges.

The parts:

| Part | What it does | Check on the Mac |
|---|---|---|
| Herdr | Runs FirstMate and each crewmate in panes. `config/backend` in the home selects `herdr`. | `herdr --version` |
| treehouse | Keeps a pool of reusable git worktrees, one per crewmate, under `~/.treehouse/`. | `treehouse --version` |
| no-mistakes | Validates a branch before it becomes a PR: review, tests, lint, push and CI. One daemon serves every lane. | `no-mistakes daemon status` |
| Herdr integrations | Hooks that tell Herdr the agent state. | `herdr integration status` |

Only FirstMate manages the no-mistakes daemon. Do not stop, restart or update
it while a pipeline run is active.

The Herdr prefix key is Ctrl+B. See the
[Herdr shortcuts](setup-guide.md#herdr-panes-and-workspaces-inside-the-terminal).

FirstMate state, such as briefs, status files and task data, stays in the
workspace. It is not part of this repo.

---

## 7. Models

### Crewmates run on Claude Opus 5.5

`config/crew-dispatch.json` in the FirstMate home chooses the harness and model
for each crewmate. On the main Mac, every rule and the default use the same
route:

```json
{ "harness": "claude", "model": "claude-opus-5-5" }
```

To check the routes, run:

```sh
jq -c '[.rules[].use, .default] | unique' ~/karan-agent-workspace/config/crew-dispatch.json
```

The output must be `[{"harness":"claude","model":"claude-opus-5-5"}]`, one route.

### OpenRouter

The `/openrouter` skill comes from kstack. Its script,
`~/.agents/skills/openrouter/scripts/openrouter`, calls
`https://openrouter.ai/api/v1` directly. It needs only `python3`. It does not
use `cli-proxy-api`.

| Command | Cost |
|---|---|
| `openrouter list [filter]` | free |
| `openrouter launch <model>` | free, prints a command for a new session |
| `openrouter ask <model> "<prompt>"` | spends OpenRouter credit |
| `openrouter compare <m1> <m2> "<prompt>"` | spends OpenRouter credit |

The script reads `OPENROUTER_API_KEY` from the environment. If that is empty, it
reads the file named by `OPENROUTER_KEY_FILE`. The key lives in
`data/keys.env`, see [section 8](#8-keys-and-secrets).

To check the script without a key, run:

```sh
python3 ~/.agents/skills/openrouter/scripts/openrouter list opus
```

The `openrouter` command on `PATH` (`~/.local/bin/openrouter`, linked by
`install.sh`) is the older launcher. It and the `claudex` and `aim` shell
functions need the local proxy and `~/.config/secrets/claudex.env`. The main
Mac has neither, so these three commands do not work there. Use the kstack
script instead.

### LM Studio and local models

LM Studio 0.4.28 is installed from the Homebrew cask. Its command-line tool is
`lms`, in `~/.lmstudio/bin`. The main Mac has two local chat models:

| Model | Download command |
|---|---|
| Qwen3.8-27B | `lms get qwen/qwen3.8-27b` |
| Qwen3.6-35B-A3B | `lms get qwen/qwen3.6-35b-a3b` |

Together they use about 38 GB of disk space. To see the installed models, run
`lms ls`.

`~/.lmstudio` holds the models, settings and `lms`. Keep it. Do not delete it
during a disk clean-up.

---

## 8. Keys and secrets

Follow the [README secret-storage instructions](../README.md#secrets-are-not-in-this-repo)
for the TinyFish key and the `claude-pubmaxx` API key. Additional credentials
used by the agent tools are:

| Secret | Where it lives | Read by |
|---|---|---|
| `TYPESAFE_API_KEY` | `data/keys.env`, environment or Keychain | Jev and TypeSafe skills |
| `OPENROUTER_API_KEY` | `data/keys.env` | the `/openrouter` skill |
| Other fleet keys | `~/karan-agent-workspace/data/keys.env`, mode 600 | FirstMate and crewmates |

`data/keys.env` is one `NAME=value` per line. The FirstMate repo ignores the
`data/` folder, so the file is never committed. To see which keys are set
without their values, run:

```sh
cut -d= -f1 ~/karan-agent-workspace/data/keys.env
```

Clone FirstMate as section 6 shows before creating `data/keys.env`.
Create `keys.env` by hand on the new Mac. Then run `chmod 600` on the file.
Do not send credentials through chat, email or a pull request. Write key names
in documents, never key values.

---

## 9. Daily update

The daily update script is `scripts/update-all.sh` in the
[mac-studio-setup](https://github.com/karanmrn/mac-studio-setup) repo. On the
main Mac the clone is `~/mac-studio-setup`.

```sh
gh repo clone karanmrn/mac-studio-setup ~/mac-studio-setup
~/mac-studio-setup/scripts/update-all.sh
```

The script updates Homebrew packages, npm globals, the self-updating CLIs,
skills, gstack, Claude Code plugins and FirstMate. It writes its log to
`~/karan-agent-workspace/data/deck/update-all.log`, not to the terminal.

The script does not update no-mistakes while `no-mistakes axi status` reports a
running pipeline, because the update would stop that run.

On the main Mac, the LaunchAgent `com.firstmate.update-all` runs a script every
day at 06:30. It runs the copy in
`~/karan-agent-workspace/data/deck/update-all.sh`, not the repo copy. That copy
does not skip the no-mistakes update. Point a new Mac's LaunchAgent at the repo
copy.

---

## 10. First hour on the MacBook Air

1. Install Homebrew, then run `brew install gh git node`.
2. Run `gh auth login`.
3. Clone this repo: `gh repo clone karanmrn/karan-herdr-shortcut-setup ~/.dotfiles-karan`.
4. Run `~/.dotfiles-karan/install.sh`. Read the `backup` lines it prints.
5. Run `brew install --cask claude-code@latest wezterm lm-studio` and `brew install herdr starship zsh-autosuggestions zsh-syntax-highlighting`.
6. Run `npm config set prefix ~/.local`, then `npm install -g @openai/codex`.
7. Open a new WezTerm tab. Check that `type cc fm` finds both.
8. Run `claude` once and sign in.
9. Edit `~/.claude/settings.json` as section 5 shows: status line, marketplaces, plugins, caveman off.
10. Follow section 5 to install MemPalace, register all four MCP servers in user scope, and authenticate the HTTP servers.
11. Install kstack and `asd-ste100` as section 4 shows.
12. Clone FirstMate: `gh repo clone karanmrn/firstmate ~/karan-agent-workspace`.
13. Store keys as section 8 shows: Keychain item and `keys.env`.
14. Run `herdr integration install claude`. Repeat with `codex` if you use Codex in Herdr.
15. Download the local models with `lms get`, as section 7 shows.
16. Clone `mac-studio-setup` and run the daily update once, as section 9 shows.
17. Start `herdr`, then type `fm`. Ask FirstMate to check its toolchain and its crew routing.

Ask FirstMate to identify any missing tools, skills or authentication before
starting project work. A reply alone does not confirm that the setups match.
