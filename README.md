# karan dotfiles

Mac setup: terminals, shell, prompt, and the FirstMate entry point.
Plain files and symlinks - no nix, no package manager takeover.

Setting up a new Mac? Start with [Install with an agent](INSTALL-WITH-AN-AGENT.md).

For background, read [Claude Code on a new Mac](docs/claude-code-on-a-new-mac.md).
It covers:

- the harnesses, plugins, MCP servers and hooks
- the [skill policy and kstack](docs/claude-code-on-a-new-mac.md#4-skills)
- the [response style](docs/claude-code-on-a-new-mac.md#response-style), with caveman off
- [FirstMate, Herdr, treehouse and no-mistakes](docs/claude-code-on-a-new-mac.md#6-firstmate-and-herdr)
- [models](docs/claude-code-on-a-new-mac.md#7-models): Opus-only crew routing, `/openrouter` and LM Studio
- [keys](docs/claude-code-on-a-new-mac.md#8-keys-and-secrets) and the [daily update](docs/claude-code-on-a-new-mac.md#9-daily-update)

Inspired by [kunchenguid/dotfiles](https://github.com/kunchenguid/dotfiles), but
deliberately **not** declarative. That repo's `homebrew.onActivation.cleanup = "zap"`
uninstalls anything not on its list. This repo never removes a package.

## What's here

```
home/.zshenv                       noninteractive shell PATH
home/.zshrc                        shell: aliases, prompt, fm entry point
home/.config/wezterm/wezterm.lua   WezTerm: rose-pine-moon look
home/.config/ghostty/config        Ghostty: same look
home/.config/herdr/config.toml     herdr: tmux-style keybindings (ctrl+b prefix)
home/.config/starship.toml         prompt format
home/.claude/skills/               Claude Code skills published from this Mac
Brewfile                           full Homebrew state (brew bundle install)
Brewfile.formulae                  top-level formulae only
Brewfile.casks                     casks only
install.sh                         symlinks the above into place
```

## Install on a new Mac

These steps target an Apple silicon Mac with a fresh user account. The installer
links configuration files. It does not install software, sign in to services,
or copy private data. Review the optional package list before installing it.

1. Install the Xcode command-line tools with `xcode-select --install`.
2. Install Homebrew from [brew.sh](https://brew.sh/). Follow its instructions
   to add `/opt/homebrew/bin/brew` to your shell.
3. Install GitHub CLI with `brew install gh`. Run `gh auth login` and sign in.
4. Clone this repository and install its configuration:

   ```sh
   gh repo clone karanmrn/karan-herdr-shortcut-setup ~/.dotfiles-karan
   ~/.dotfiles-karan/install.sh
   ```

5. Review `~/.dotfiles-karan/Brewfile`. To restore the recorded package list,
   run `brew bundle install --file="$HOME/.dotfiles-karan/Brewfile"`. This can
   download many unrelated tools. It does not remove packages.
6. Clone FirstMate with `gh repo clone karanmrn/firstmate ~/karan-agent-workspace`.
   Follow its setup instructions for dependencies and local fleet configuration.
7. Sign in separately to Claude Code, Codex, GitHub, and any other services you
   use. Restore needed keys through the appropriate service or Keychain. Never
   copy authentication files or keys into this repository.
8. Open WezTerm and grant any macOS permissions requested by the tools you use.
   Install the Herdr agent integrations as described in the
   [new Mac guide](docs/claude-code-on-a-new-mac.md#6-firstmate-and-herdr).
9. The Studio uses the reviewr Herdr plugin. To restore it on the new Mac, run
   `herdr plugin install persiyanov/herdr-reviewr --ref aede1794248fbfc3fc8f45ff77977a718aadbef0`.
   The plugin builds its own executable. Review its source before installing it.
10. Open a new terminal, start Herdr, and run `fm` inside it. Check the sidebar,
    keyboard shortcuts, and agent integrations on the new machine.

The Brewfile is a Studio snapshot from 24 November 2026. Cursor extensions were
excluded because the local Cursor CLI could not find an IDE installation.
The package list does not include every tool installed outside Homebrew, npm,
or uv. The guide lists additional tools and sign-in steps. Herdr session
snapshots, logs, plugin state, runner registrations, and credentials are local
machine data and are not copied.

`install.sh` backs up replaced files, directories, and symlinks to
`<file>.pre-dotfiles-YYYYMMDD-HHMMSS`, then creates symlinks. It adds a login
hook once and links the FirstMate environment independently of the checkout
location. Existing profile content remains in place. Run the installer again
after pulling updates. Quote glob patterns that must reach a command unchanged.

## The look

See the [terminal appearance guide](docs/setup-guide.md#5-the-terminal-look)
for WezTerm and Ghostty settings. Herdr uses Catppuccin with automatic theme
switching disabled.

cmux is not covered - it has no terminal theme key in its config schema, so set
its appearance in cmux Settings directly.

## Secrets are not in this repo

Fleet keys live in `~/karan-agent-workspace/data/keys.env` (mode 600), one
`NAME=value` per line. See
[Keys and secrets](docs/claude-code-on-a-new-mac.md#8-keys-and-secrets).

`~/.config/secrets/claudex.env` held `ANTHROPIC_AUTH_TOKEN` for `claudex`,
`aim` and the older `openrouter` launcher. These commands need the local
proxy, which the main Mac no longer runs. Create the file only if you run
that proxy. It is intentionally outside this repo and must never be committed.
Put an `export ANTHROPIC_AUTH_TOKEN='your-local-proxy-token'` assignment in
it, replace the placeholder with your token, then run
`chmod 600 ~/.config/secrets/claudex.env`.

`claude-pubmaxx` reads an Anthropic API key from OpenCode's local
`~/.local/share/opencode/auth.json`. Connect an Anthropic API key in OpenCode
before using the command. Keep that file outside this repo.

The shell loads `TINYFISH_API_KEY` from the macOS Keychain item
`tinyfish-api-key` for the current user when the variable is empty. It preserves
an existing value and leaves the variable unset if retrieval fails.

To store the TinyFish key, run this command. Enter the value at the prompt.

```sh
security add-generic-password -a "$USER" -s tinyfish-api-key -w
```

## Aliases

| Alias | Command |
|---|---|
| `..` | `cd ..` |
| `add` | `git add .` |
| `push` | `git push` |
| `pull` | `git pull` |
| `m` | `git switch main` |
| `cc` | `claude --dangerously-skip-permissions` |
| `co` | `codex --sandbox workspace-write --ask-for-approval never` |

`cc` and `co` disable agent permission prompts. `co` retains the workspace-write
sandbox. Use these commands only when you intend those permission settings.

## fm

`fm` enters `FM_WORKSPACE` and starts Claude Code with any supplied arguments.
It works from any terminal and does not create a nested Herdr session.

`home/firstmate-env.zsh` supplies defaults through the interactive `.zshrc`
and login `.zprofile` hooks. It preserves nonempty environment overrides:

| Variable | Default |
|---|---|
| `FM_WORKSPACE` | `~/karan-agent-workspace` |
| `FM_HOME` | the value of `FM_WORKSPACE` |
| `FM_BACKEND` | `herdr` |

## claude-pubmaxx

`claude-pubmaxx <prompt>` starts Claude Code in print mode in
`/Users/karanmanoharan/code/projects/pubmaxx` with `claude-sonnet-5-5`.
It uses the Anthropic API directly and consumes Console API credits.
It clears conflicting authentication and cloud-provider settings inside a
subshell. See [Secrets](#secrets-are-not-in-this-repo) for its credential source.
