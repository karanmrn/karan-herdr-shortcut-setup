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

`install.sh` backs up anything it would overwrite to `<file>.pre-dotfiles`,
then symlinks. Because they are symlinks, editing `~/.zshrc` edits the file in
this repo - the two never drift.

## The look

rose-pine-moon everywhere: dark base with a purple-grey cast, muted rose and
gold accents. Hack Nerd Font 15pt, 80% window opacity with heavy blur.

cmux is not covered - it has no terminal theme key in its config schema, so set
its appearance in cmux Settings directly.

## Secrets are not in this repo

`~/.config/secrets/claudex.env` holds the Anthropic token for the `claudex`
function (mode 600). It is intentionally outside this repo and must never be
committed. On a new machine, recreate it by hand.

## Aliases

| Alias | Command |
|---|---|
| `..` | `cd ..` |
| `add` | `git add .` |
| `push` | `git push` |
| `pull` | `git pull` |
| `m` | `git switch main` |
| `cc` | `claude --dangerously-skip-permissions` |
| `co` | `codex --full-auto` |

`cc` and `co` disable agent permission prompts. Deliberate escape hatches - know
what they do.

## fm

`fm` cds into the FirstMate workspace and starts it. Works from any terminal.
Detects an existing herdr session and does not nest inside one.
