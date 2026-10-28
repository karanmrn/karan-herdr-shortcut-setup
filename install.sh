#!/usr/bin/env bash
# Symlink this repo's config files into place.
# Backs up anything it would overwrite. Never deletes packages.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

link() {
  local src="$REPO/home/$1" dest="$HOME/$1"

  if [ ! -e "$src" ]; then
    echo "skip   $1 (not in repo)"
    return
  fi

  # already the correct symlink
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    echo "ok     $1"
    return
  fi

  mkdir -p "$(dirname "$dest")"

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    mv "$dest" "$dest.pre-dotfiles-$STAMP"
    echo "backup $1 -> $1.pre-dotfiles-$STAMP"
  fi

  ln -s "$src" "$dest"
  echo "link   $1"
}

link ".zshenv"
link ".zshrc"
link ".config/wezterm/wezterm.lua"
link ".config/ghostty/config"
link ".config/herdr/config.toml"
link ".config/starship.toml"
link ".config/agents/AGENTS.md"
link ".cursor/rules/jev-review.mdc"
link ".claude/statusline.sh"
link ".local/bin/openrouter"

FIRSTMATE_ENV_MARKER="# firstmate global env (dotfiles-karan)"
ZPROFILE="$HOME/.zprofile"
touch "$ZPROFILE"
if ! grep -qF "$FIRSTMATE_ENV_MARKER" "$ZPROFILE" 2>/dev/null; then
  {
    echo ""
    echo "$FIRSTMATE_ENV_MARKER"
    echo "[ -f \"\$HOME/.dotfiles-karan/home/firstmate-env.zsh\" ] && source \"\$HOME/.dotfiles-karan/home/firstmate-env.zsh\""
  } >>"$ZPROFILE"
  echo "append .zprofile (firstmate global env)"
else
  echo "ok     .zprofile firstmate hook"
fi

link_global_agents() {
  local src="$REPO/home/.config/agents/AGENTS.md"
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    echo "ok     $dest"
    return
  fi
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    mv "$dest" "$dest.pre-dotfiles-$STAMP"
    echo "backup $(basename "$dest") in $(dirname "$dest")"
  fi
  ln -sf "$src" "$dest"
  echo "link   $dest"
}

link_global_agents "$HOME/.claude/CLAUDE.md"
link_global_agents "$HOME/.codex/AGENTS.md"
link_global_agents "$HOME/.config/opencode/AGENTS.md"
link_global_agents "$HOME/.grok/AGENTS.md"

echo
echo "Done. Open a new terminal tab to pick up shell changes."
echo "Optional: brew bundle install --file=$REPO/Brewfile"
echo
echo "Not handled here (by design):"
echo "  - ~/.config/secrets/claudex.env  recreate by hand, never commit"
echo "  - cmux appearance               set in cmux Settings"
