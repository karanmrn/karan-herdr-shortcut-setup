# Let agent commands pass unmatched patterns to the consumer.
if [[ ${CLAUDECODE:-} == 1 || -n ${CODEX_THREAD_ID:-} ]]; then
  setopt NO_NOMATCH
fi
