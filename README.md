# karan dotfiles

Mac setup: terminals, shell, prompt, and the FirstMate entry point.
Plain files and symlinks - no nix, no package manager takeover.

Inspired by [kunchenguid/dotfiles](https://github.com/kunchenguid/dotfiles), but
deliberately **not** declarative. That repo's `homebrew.onActivation.cleanup = "zap"`
uninstalls anything not on its list. This repo never removes a package.

## What's here

```
home/.zshrc                        shell: aliases, prompt, fm entry point
home/.config/wezterm/wezterm.lua   WezTerm: rose-pine-moon look
home/.config/ghostty/config        Ghostty: same look
home/.config/herdr/config.toml     herdr: tmux-style keybindings (ctrl+b prefix)
home/.config/starship.toml         prompt format
Brewfile                           full Homebrew state (brew bundle install)
Brewfile.formulae                  top-level formulae only
Brewfile.casks                     casks only
install.sh                         symlinks the above into place
```

## Install on a new Mac

```sh
git clone <this-repo> ~/.dotfiles-karan
cd ~/.dotfiles-karan
./install.sh
brew bundle install --file=Brewfile   # optional: restore all packages
```

`install.sh` backs up replaced files, directories, and symlinks to
`<file>.pre-dotfiles-YYYYMMDD-HHMMSS`, then creates symlinks. Editing `~/.zshrc`
edits the file in this repo. The installer also appends a FirstMate environment
hook to `~/.zprofile` once. It preserves the existing profile content.

## The look

See the [terminal appearance guide](docs/setup-guide.md#5-the-terminal-look)
for WezTerm and Ghostty settings. Herdr uses Catppuccin with automatic theme
switching disabled.

cmux is not covered - it has no terminal theme key in its config schema, so set
its appearance in cmux Settings directly.

## Secrets are not in this repo

`~/.config/secrets/claudex.env` holds the Anthropic token for the `claudex`
function (mode 600). It is intentionally outside this repo and must never be
committed. On a new machine, recreate it by hand.

`claude-pubmaxx` reads an Anthropic API key from OpenCode's local
`~/.local/share/opencode/auth.json`. Connect an Anthropic API key in OpenCode
before using the command. Keep that file outside this repo.

The shell loads `TINYFISH_API_KEY` from the macOS Keychain item
`tinyfish-api-key` for the current user when the variable is empty. It preserves
an existing value and leaves the variable unset if retrieval fails.

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
