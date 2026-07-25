# Mac Setup - terminals, shell, agents

Applied 2026-07-25. Adapted from https://github.com/kunchenguid/dotfiles

Everything below is now stored in a git repo at `~/.dotfiles-karan`.
Your live config files are symlinks into it, so editing `~/.zshrc` edits the repo
file. They cannot drift apart.

---

# 1. Daily workflow

## Starting work

Open a terminal tab and type:

```sh
fm
```

That is the whole thing. `fm` does three steps you used to do by hand:

| Old way | Now |
|---|---|
| `cd ~/karan-agent-workspace` | done by `fm` |
| check whether herdr is running | done by `fm` |
| launch the agent | done by `fm` |

It greets you as Captain Karan, shows the current git branch, and starts
FirstMate. Works from WezTerm, Ghostty, or cmux.

You do NOT need to type `herdr` separately if a herdr session is already
running - `fm` detects it and will not nest a session inside a session.

## The three commands, and when to use which

| Command | What it starts | Permission prompts |
|---|---|---|
| `fm` | FirstMate, in the workspace | Yes - supervised, gates on merges |
| `cc` | plain Claude Code, wherever you are | **No - all prompts disabled** |
| `co` | plain Codex, wherever you are | **No - full auto** |

`fm` is the normal way in. `cc` and `co` are escape hatches: they let an agent
write files, run commands, and delete things without asking first. Two
keystrokes, no safety net. Use them only when you are watching closely and the
work is disposable.

---

# 2. Keyboard shortcuts

## WezTerm (the terminal app itself)

| Keys | Does |
|---|---|
| `Cmd+T` | new tab |
| `Cmd+N` | new window |
| `Cmd+W` | close tab |
| `Cmd+1`, `Cmd+2` ... | jump to tab 1, 2 ... |
| `Cmd+Shift+R` | reload the WezTerm config after editing it |
| `Cmd+K` | clear the screen |
| `Cmd+F` | search the scrollback |
| `Cmd+plus` / `Cmd+minus` | text bigger / smaller |

## Two pane systems - important

There are TWO independent pane systems running, with different leader keys:

| | WezTerm's own | herdr's |
|---|---|---|
| Leader | `Ctrl+A` | `Ctrl+B` |
| Split right | `Ctrl+A` then `Shift+\|` | `Ctrl+B` then `%` |
| Split down | `Ctrl+A` then `-` | `Ctrl+B` then `"` |
| Move | `Ctrl+A` then `h/j/k/l` | `Ctrl+B` then `h/j/k/l` |
| New tab | `Ctrl+A` then `c` | `Ctrl+B` then `c` |
| Zoom pane full-screen | `Ctrl+A` then `z` | not available |
| Send a literal Ctrl+A | `Ctrl+A` twice | - |

Movement is `h/j/k/l` in both, so the habit transfers. Only the leader differs.

**Use `Ctrl+B` (herdr) for anything agent-related.** herdr is what FirstMate uses
to open worker panes and what it can see. WezTerm's own panes are invisible to it.

`Ctrl+A` then `z` (zoom) is the one genuinely useful extra - it expands the
current pane to fill the window, press again to restore. Good for reading long
output without closing a split.

## herdr (panes and workspaces inside the terminal)

herdr uses a **prefix key**. This is the important idea for a beginner:

> You press `Ctrl+B`, **let go**, then press one more key.
> The second key is the actual command.

`Ctrl+B` on its own does nothing visible. It just means "the next key is a
herdr command, not text". This is how tmux works too, so learning it once
covers both.

Written `prefix + h` below = press `Ctrl+B`, release, press `h`.

### Moving between panes - the vim-style part

A pane is one split section of the window. Movement uses four letters sitting in
a row under your right hand on a QWERTY keyboard:

```
        k          k = up
      ↑
  h ←   → l        h = left      l = right
      ↓
        j          j = down
```

| Keys | Moves focus |
|---|---|
| `prefix + h` | left |
| `prefix + j` | down |
| `prefix + k` | up |
| `prefix + l` | right |

Why these letters instead of arrow keys? They come from the vim editor. Your
fingers already rest on them, so you never move your hand to reach the arrows.
It feels wrong for about a day, then it is faster. You do not need to know vim
itself to use this - it is just four direction keys.

Memory hook: `h` is the leftmost of the four, `l` is the rightmost, `j` points
down like the descender on the letter j, `k` is the one left over for up.

### Splitting and tabs

| Keys | Does |
|---|---|
| `prefix + "` | split horizontally (new pane below) |
| `prefix + %` | split vertically (new pane to the right) |
| `prefix + c` | create a new tab |
| `prefix + &` | close the current tab |
| `prefix + w` | workspace picker - list and jump between workspaces |
| `prefix + g` | go to a specific pane or tab |
| `prefix + y` | enter copy mode (see below) |

### Copy mode - scrolling and copying text with the keyboard

`prefix + y` enters copy mode. Once inside, these keys are fixed and cannot be
reconfigured:

| Keys | Does |
|---|---|
| `v` or `Space` | start selecting |
| `y` or `Enter` | copy the selection and exit |
| `q` or `Esc` | cancel and exit |
| `h` `j` `k` `l` | move the cursor while selecting |

Useful when you want to copy a long error message without reaching for the
mouse.

### Shell keys

| Keys | Does |
|---|---|
| `Ctrl+F` | accept the grey suggested command |
| `Ctrl+C` | cancel the running command |
| `Ctrl+R` | search your command history |
| `Ctrl+A` / `Ctrl+E` | jump to start / end of the line |
| `Ctrl+U` | clear the whole line |
| `Ctrl+L` | clear the screen |

The **grey text** that appears as you type is a suggestion from your history.
`Ctrl+F` accepts it. Ignore it and keep typing to dismiss it.

Commands turn **green** when the shell recognises them and **red** when it does
not - a typo check before you press Enter.

---

# 3. Shell aliases

| Alias | Full command |
|---|---|
| `..` | `cd ..` |
| `add` | `git add .` |
| `push` | `git push` |
| `pull` | `git pull` |
| `m` | `git switch main` |
| `cc` | `claude --dangerously-skip-permissions` |
| `co` | `codex --sandbox workspace-write --ask-for-approval never` |
| `fm` | FirstMate in the workspace (a function) |
| `claudex` | Claude on `gpt-5.6-sol` via the local proxy |
| `aim <model>` | Claude on any proxied model, no picker |
| `openrouter` | fuzzy picker over all ~349 proxied models |

Note on `co`: codex 0.145 removed the old `--full-auto` flag. The two flags above
are the same behaviour - write access limited to the working directory, no
approval prompts.

Note on `add`: it stages **everything** changed, not just one file. Check
`git status` first if the tree is messy.

---

# 4. The prompt

Starship. One line of information, then the cursor line:

```
~/karan-agent-workspace  main  1.2s
❯
```

- current directory
- git branch and whether it is dirty
- how long the last command took
- `❯` is **purple** when the last command succeeded, **red** when it failed

That colour is your error signal - no need to check exit codes.

---

# 5. The terminal look

**rose-pine-moon** in both WezTerm and Ghostty: dark base with a purple-grey
cast, muted rose and gold accents. Not black. Windows are ~94% opaque with a
blur, so the wallpaper shows through slightly. No title bar.

| | WezTerm | Ghostty |
|---|---|---|
| Colours | rose-pine-moon | rose-pine-moon |
| Font | JetBrainsMono Nerd Font 14 | Hack Nerd Font 15 |
| Opacity | 0.94 | 0.8 |

Colours match. Fonts deliberately differ - both are Nerd Fonts (they include
icon glyphs), so either renders CLI tool icons correctly.

A navy scheme (`#07111f` background, `#8bdcff` cursor) was tried and rejected in
favour of rose-pine-moon. If it is ever wanted back, replace the
`config.color_scheme` line in `wezterm.lua` with a `config.colors = { ... }` block.

**cmux is not covered.** Its config format has no terminal theme or font
setting, so set its appearance in cmux Settings directly.

### Tuning

| Want | Change |
|---|---|
| less transparent | raise `window_background_opacity` toward `1.0` |
| solid window | set it to `1.0`, delete the blur line |
| bigger text | raise `font_size` |
| title bar back | `window_decorations = "TITLE | RESIZE"` |
| more scrollback | raise `scrollback_lines` (currently 10000) |

WezTerm reloads config live; `Cmd+Shift+R` forces it.

---

# 6. FirstMate and crewmates - how the agents fit together

This is the part worth understanding properly.

## The roles

**You are the captain.** You talk to exactly one agent.

**FirstMate is that agent.** It does not write product code. It reads code,
plans, delegates, supervises, and reports back to you.

**Crewmates are workers FirstMate creates.** Each one gets its own isolated copy
of the project, does one task, and reports its result to FirstMate - never to
you.

```
      You (captain)
           |
       FirstMate            <- the only agent you talk to
       /    |    \
   crew   crew   crew       <- workers, one task each, isolated copies
```

## Can FirstMate send a task to a crewmate?

**Yes - that is its entire job.** FirstMate creates a crewmate, hands it written
instructions, and can send it follow-up messages while it works. That is the
normal flow, not a special feature.

What it does NOT do:

- Crewmates never talk to you directly. Everything comes back through FirstMate.
- A crewmate does not create its own crewmates.
- FirstMate does not read another crewmate's chat window to check on it - it
  reads the status each worker reports.

## Why isolated copies matter

Each crewmate works in its own separate copy of the project. Two workers can
change the same project at the same time without overwriting each other. Nothing
touches your main copy until work is finished and approved.

## What needs your approval

FirstMate will not, without you saying so:

- merge a pull request
- throw away work that is not saved
- do anything destructive, irreversible, or security-related

It handles routine things itself and comes to you for the real decisions.

## Second mates

A **second mate** is a FirstMate with its own separate area, for a distinct
domain of work. You do not have one - with a single project you do not need one.

---

# 5b. Running any model - the local proxy

`cli-proxy-api` runs as a background service on `127.0.0.1:8317` and serves
**~349 models**: all 345 OpenRouter models plus your Codex ones. Config lives at
`/opt/homebrew/etc/cliproxyapi.conf`.

This is completely independent of herdr and FirstMate. It works from any plain
terminal.

```sh
openrouter                    # fuzzy picker over every model (fzf)
openrouter deepseek           # jump straight to one
openrouter grok-4.5           # Grok, via OpenRouter
openrouter --list             # print all names
openrouter --refresh          # re-fetch after OpenRouter adds models
aim gemini-3.6-flash          # same, no picker
```

Inside Claude, `/openrouter` lists models and recommends ones for a given task.
It cannot switch the current session's model - that is fixed once a session
starts - so it hands you the command to start a new one.

## Which model for what

| Job | Try |
|---|---|
| Bulk edits, mechanical refactors | `deepseek-chat`, `qwen` variants |
| Long-context reading | `gemini-3.6-flash` |
| Reasoning-heavy analysis | `deepseek-r1` |
| Free / throwaway | anything suffixed `:free` |

These bill to **OpenRouter**, not to the Claude or Codex quotas - useful when
either is running low.

## What is NOT available

- **Cursor**: no public API exists. The Ultra subscription only works inside
  Cursor's own apps. No key would change this.
- **Grok via your subscription**: the Grok CLI uses OAuth, not an API key. Grok
  models are reachable through OpenRouter instead (already working). A direct
  xAI channel would need a separately billed key from console.x.ai.

## Status line

The bar under the prompt shows: model, folder, git branch, context used, session
cost, and remaining quota per provider. Script: `~/.claude/statusline.sh`.

Quota is cached for 5 minutes and refreshed in the background, because
`quota-axi` takes ~2s and the status line must stay fast.

Compaction is set to fire at **14%** of the 1M context window, which is ~140k
tokens (`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` in `~/.claude/settings.json`).

---

# 6b. Closing the terminal, sessions, and memory

## Does closing WezTerm end the session?

**No.** herdr runs as a background server with a persistent session called
`default`. Closing the terminal window only disconnects the *view*, like hanging
up a video call while the meeting continues.

```
WezTerm window   ← just a viewer. Closing it changes nothing.
      │
herdr server     ← keeps running in the background, holds the session
      │
   the panes     ← agents keep running inside them
```

When you come back: open WezTerm and type `herdr`. It reattaches to the same
session, same panes, same agents, exactly as you left them. Work that was running
while you were out kept running.

Check what is alive at any time:

```sh
herdr session list     # sessions and whether they are running
herdr pane list        # panes, which agent is in each, and its status
```

## Three different kinds of memory - this is the part worth understanding

They are separate, and they behave very differently.

### 1. Context window - the conversation, and it is finite

The agent can only "see" a limited amount of text at once - the conversation so
far, plus files it has read. This is the **context window**.

When it fills up, **compaction** happens: the older part of the conversation is
replaced with a summary, and work continues. Nothing stops, but fine detail from
early on becomes a summary rather than the exact words.

Consequence: in a very long session, precise early details can blur. If something
matters, it should be written to a file, not left sitting in the conversation.

### 2. Session - resumable, but a separate thing from the terminal

The conversation is stored on disk, so it can be resumed later even after the
agent process exits:

```sh
claude --continue     # resume the most recent conversation here
claude --resume       # pick from a list of past conversations
```

Note the difference:

- **herdr session** = the pane and the process staying alive
- **agent session** = the conversation transcript being resumable

You can lose one and keep the other.

### 3. Durable records - what actually survives everything

FirstMate does not rely on remembering the conversation. It writes to disk:

| What | Where |
|---|---|
| Your preferences | `data/captain.md` |
| Which projects exist | `data/projects.md` |
| Task queue and history | `data/backlog.md` |
| Worker instructions | `data/<id>/brief.md` |
| Investigation findings | `data/<id>/report.md` |
| Live worker state | `state/` |
| Lessons learned | `data/learnings.md` |

This is why a restart is a **non-event**. On start, FirstMate reads these files
and reconstructs what is happening from disk, not from memory of the chat. A
worker mid-task, a pending decision, an unfinished investigation - all recorded.

**The practical rule:** conversation is temporary, files are permanent. Anything
that matters should end up in a file. That is what this document is.

## Safe ways to leave

| Situation | Do this |
|---|---|
| Stepping away, work is running | Just close the window. Everything continues. |
| Going away and want batched updates | Type `/afk` first - FirstMate handles routine things itself and batches what needs you |
| Truly done for the day | Close the window; or `herdr session stop default` to end the session entirely |
| Coming back | Open WezTerm, type `herdr`, then carry on |

Do **not** quit WezTerm expecting it to stop work - it will not. Work continues
in the background.

---

# 7. Your pubmax copies - READ THIS

You have **three** working copies of the same private repo
`github.com/karanmrn/pubmax`:

| Location | Branch | Uncommitted | Role |
|---|---|---|---|
| `~/karan-agent-workspace/projects/pubmax` | `main` | 0 files | **the one agents use** |
| `~/Documents/pubmax` | `docs/dag-handoff` | **16 files** | your manual editor copy |
| `~/conductor/repos/pubmax` | `feat/lane-to-plan-metric` | 0 files | older, probably stale |

**The problem:** those 16 uncommitted files in `~/Documents/pubmax` exist only on
your disk. Agents cannot see them. If you ask for work on that code, a worker
will start from `main` and not know your changes exist - and you can end up with
two versions of the same work.

**The fix:** commit and push from `~/Documents/pubmax` when you finish something.
Once it is on GitHub, agents pick it up.

```sh
cd ~/Documents/pubmax
git status          # look before you commit
add                 # stage everything (alias for git add .)
git commit -m "your message"
push
```

Rule of thumb: **pushed = visible to agents. Unpushed = invisible.**

---

# 8. Security

The Anthropic token that used to sit in plain text inside `~/.zshrc` now lives
in `~/.config/secrets/claudex.env`, readable only by you (mode 600), loaded only
when `claudex` runs. It is gitignored and not in the dotfiles repo.

**Still recommended:** rotate that token. It was in a plain file for a while. To
replace it, edit that one file - nothing else changes.

---

# 9. The dotfiles repo

`~/.dotfiles-karan`, a git repo, currently **local only** (not on GitHub).

```
home/.zshrc                        shell
home/.config/wezterm/wezterm.lua   WezTerm look + leader keybindings
home/.config/ghostty/config        Ghostty look
home/.config/herdr/config.toml     herdr keybindings
home/.config/starship.toml         prompt
home/.config/agents/AGENTS.md      shared agent instructions
Brewfile                           all taps/formulae/casks
install.sh                         symlinks everything into place
```

## Shared agent instructions

`~/.config/agents/AGENTS.md` is one file, symlinked into three agents:

| Agent | Reads |
|---|---|
| Codex | `~/.codex/AGENTS.md` -> shared file |
| opencode | `~/.config/opencode/AGENTS.md` -> shared file |
| grok | `~/.grok/AGENTS.md` -> shared file |
| Claude | its own `~/.claude/CLAUDE.md` (standards mirrored) |

Edit the shared file once and all three change. Claude keeps a separate file
because it also holds Claude-only skill routing (`ideate`, `graphify`), which
means nothing to the others.

It contains the engineering standards merged from Kun's setup, plus the caveman
response style that used to live only in the opencode file.

**Skills do NOT cross harnesses.** Skills are a Claude Code feature living in
`~/.claude/skills/`. Codex, grok, and opencode cannot see them. Only written
instructions are portable, which is what the shared file is for.

On a new Mac: clone it, run `./install.sh`, optionally
`brew bundle install --file=Brewfile`. Done.

`install.sh` backs up any file it would overwrite and **never uninstalls
packages**. That last point is deliberate: Kun's nix version sets Homebrew
cleanup to `zap`, which uninstalls anything not on his list. His list is 3
items; this machine has 125. Running his version would have removed ~115
packages. That is why the nix layer was skipped.

## Undo anything

```sh
# restore the pre-setup shell
rm ~/.zshrc && mv ~/.zshrc.pre-dotfiles-20260725-115800 ~/.zshrc

# remove the terminal look
rm ~/.config/wezterm/wezterm.lua ~/.config/ghostty/config

# remove herdr keybindings (back to defaults)
rm ~/.config/herdr/config.toml
```

Backups from the install are `~/.zshrc.pre-dotfiles-*` and
`~/.zshrc.backup-20260725`.

---

# 10. Not applied

| Thing | Why |
|---|---|
| Neovim config | You do not use it |
| Nix / nix-darwin | Would have uninstalled ~115 Homebrew packages |
| cmux theme | No theme setting exists in its config format |
| Other projects registered | Only pubmax, by your decision |
