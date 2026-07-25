#!/usr/bin/env bash
# Claude Code status line: model / dir [branch] | ctx | tokens | cost | quota
# Input: JSON on stdin from Claude Code. Must stay fast - runs on every render.

input=$(cat)

# One-time capture of the raw payload so the available fields can be inspected.
DUMP="$HOME/.claude/statusline-input.json"
[ -f "$DUMP" ] || printf '%s' "$input" > "$DUMP" 2>/dev/null

j() { printf '%s' "$input" | jq -r "$1 // empty" 2>/dev/null; }

# ---- model, directory, branch ----
model=$(j '.model.display_name'); : "${model:=Claude}"
cwd=$(j '.workspace.current_dir'); : "${cwd:=.}"
dir=$(basename "$cwd")

out="$model"
[ -n "$dir" ] && [ "$dir" != "/" ] && out="$out / $dir"

if git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null)
  [ -n "$branch" ] && [ "$branch" != "HEAD" ] && out="$out [$branch]"
fi

# ---- context window ----
# Field names have varied across versions; try each and use the first that exists.
pct=$(j '.context_window.used_percentage')
[ -z "$pct" ] && pct=$(j '.context.used_percentage')
[ -z "$pct" ] && pct=$(j '.usage.context_used_percentage')

used=$(j '.context_window.used_tokens')
[ -z "$used" ] && used=$(j '.context.used_tokens')
[ -z "$used" ] && used=$(j '.usage.input_tokens')

total=$(j '.context_window.total_tokens')
[ -z "$total" ] && total=$(j '.context.total_tokens')

fmt_tokens() {  # 152000 -> 152k
  awk -v n="$1" 'BEGIN{ if (n>=1000000) printf "%.1fM", n/1000000;
                        else if (n>=1000) printf "%.0fk", n/1000;
                        else printf "%d", n }'
}

ctx=""
if [ -n "$pct" ]; then
  ctx=$(awk -v p="$pct" 'BEGIN{printf "%.0f%%", p}')
  [ -n "$used" ] && ctx="$ctx ($(fmt_tokens "$used"))"
elif [ -n "$used" ] && [ -n "$total" ]; then
  ctx=$(awk -v u="$used" -v t="$total" 'BEGIN{ if (t>0) printf "%.0f%%", (u/t)*100 }')
  ctx="$ctx ($(fmt_tokens "$used")/$(fmt_tokens "$total"))"
elif [ -n "$used" ]; then
  ctx="$(fmt_tokens "$used")"
fi
[ -n "$ctx" ] && out="$out | ctx $ctx"

# ---- session cost ----
cost=$(j '.cost.total_cost_usd')
[ -n "$cost" ] && out="$out | \$$(awk -v c="$cost" 'BEGIN{printf "%.2f", c}')"

# ---- quota (cached; quota-axi takes ~2s so never call it inline) ----
CACHE="$HOME/.claude/quota-cache.txt"
MAXAGE=300  # seconds

cache_age=999999
if [ -f "$CACHE" ]; then
  now=$(date +%s)
  mtime=$(stat -f %m "$CACHE" 2>/dev/null || echo 0)
  cache_age=$(( now - mtime ))
fi

# Refresh in the background when stale. Never blocks the status line.
if [ "$cache_age" -gt "$MAXAGE" ]; then
  {
    q=$(quota-axi --json 2>/dev/null)
    printf '%s' "$q" | jq -r '
      [ .providers[]
        | select(.state.status == "ok" or (.windows | length) > 0)
        | . as $p
        | ($p.windows | map(select(.percentRemaining != null)) | sort_by(.percentRemaining) | first) as $w
        | select($w != null)
        | "\($p.label) \($w.percentRemaining)%"
      ] | join("  ")
    ' 2>/dev/null > "$CACHE".tmp && mv "$CACHE".tmp "$CACHE"
  } >/dev/null 2>&1 &
fi

if [ -f "$CACHE" ]; then
  quota=$(cat "$CACHE" 2>/dev/null)
  [ -n "$quota" ] && out="$out | $quota"
fi

printf '%s' "$out"

# ---- caveman plugin suffix (preserve existing behaviour) ----
cav="$HOME/.claude/plugins/cache/caveman/caveman/0d95a81d35a9/src/hooks/caveman-statusline.sh"
if [ -x "$cav" ]; then
  cav_out=$("$cav" 2>/dev/null)
  [ -n "$cav_out" ] && printf ' %s' "$cav_out"
fi
