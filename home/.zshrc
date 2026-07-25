path_prepend() {
  [ -d "$1" ] || return
  case ":$PATH:" in
    *":$1:"*) ;;
    *) export PATH="$1:$PATH" ;;
  esac
}

fpath_prepend() {
  [ -d "$1" ] || return
  fpath=("$1" $fpath)
}

# bun
export BUN_INSTALL="$HOME/.bun"
path_prepend "$BUN_INSTALL/bin"

# User CLIs (pi, herdr, axi, treehouse, no-mistakes) must win over Hermes node bins
path_prepend "$HOME/.hermes/node/bin"
path_prepend "$HOME/.local/bin"

# grok
path_prepend "$HOME/.grok/bin"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# The following lines have been added by Docker Desktop to enable Docker CLI completions.
fpath_prepend "$HOME/.docker/completions"
# End of Docker CLI completions

# grok completions
fpath_prepend "$HOME/.grok/completions/zsh"

autoload -Uz compinit
compinit -C
autoload -U +X bashcompinit && bashcompinit
[ -s "$HOME/.dbt-completion.bash" ] && source "$HOME/.dbt-completion.bash"

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# Pi / agent CLIs — prefer ~/.local/bin (FirstMate toolchain) over Hermes node bins
export PATH="$HOME/.local/bin:$HOME/.hermes/node/bin:$PATH"


# Vite+ bin (https://viteplus.dev)
. "$HOME/.vite-plus/env"



# claudex: token lives in ~/.config/secrets/claudex.env (mode 600), not here
claudex() {
  local secrets="$HOME/.config/secrets/claudex.env"
  if [ ! -r "$secrets" ]; then
    print -u2 "claudex: missing $secrets"
    return 1
  fi
  (
    source "$secrets"
    if [ -z "$ANTHROPIC_AUTH_TOKEN" ]; then
      print -u2 "claudex: ANTHROPIC_AUTH_TOKEN not set in $secrets"
      exit 1
    fi
    ANTHROPIC_BASE_URL=http://127.0.0.1:8317 \
    CLAUDE_CODE_SUBAGENT_MODEL=gpt-5.6-sol \
    CLAUDE_CODE_ALWAYS_ENABLE_EFFORT=1 \
    CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY=3 \
    ENABLE_TOOL_SEARCH=false \
    claude --model gpt-5.6-sol "$@"
  )
}

# >>> grok installer >>>
export PATH="$HOME/.grok/bin:$PATH"
fpath=(~/.grok/completions/zsh $fpath)
autoload -Uz compinit && compinit -C
# <<< grok installer <<<

# opencode
export PATH=/Users/karanmanoharan/.opencode/bin:$PATH

# ---- kunchenguid/dotfiles setup (added 2026-07-25) ----
export EDITOR="nvim"

# aliases
alias ..='cd ..'
alias add='git add .'
alias push='git push'
alias pull='git pull'
alias m='git switch main'
alias cc='claude --dangerously-skip-permissions'
alias co='codex --full-auto'

# fm: FirstMate entry point. Works from WezTerm, Ghostty, or cmux.
export FM_WORKSPACE="$HOME/karan-agent-workspace"
fm() {
  if [ ! -d "$FM_WORKSPACE" ]; then
    print -u2 "fm: workspace not found at $FM_WORKSPACE"
    return 1
  fi
  cd "$FM_WORKSPACE" || return 1
  print -P "%F{magenta}Aboard, Captain Karan.%f  $(git branch --show-current 2>/dev/null)"
  if [ -n "$HERDR_ENV" ]; then
    # already inside a herdr session: land in the workspace, do not nest
    print -P "%F{240}herdr session already active - launching FirstMate here%f"
  fi
  claude "$@"
}

# zsh autosuggestions (ghost text from history); ctrl+f accepts
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
bindkey '^f' autosuggest-accept

# starship prompt
eval "$(starship init zsh)"

# syntax highlighting must be sourced last
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
# ------------------------------------------------------
