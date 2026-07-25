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

link ".zshrc"
link ".config/wezterm/wezterm.lua"
link ".config/ghostty/config"
link ".config/herdr/config.toml"
link ".config/starship.toml"
link ".config/agents/AGENTS.md"
link ".claude/statusline.sh"
link ".local/bin/openrouter"

echo
echo "Done. Open a new terminal tab to pick up shell changes."
echo "Optional: brew bundle install --file=$REPO/Brewfile"
echo
echo "Not handled here (by design):"
echo "  - ~/.config/secrets/claudex.env  recreate by hand, never commit"
echo "  - cmux appearance               set in cmux Settings"
