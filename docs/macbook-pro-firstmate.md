# MacBook Pro FirstMate workflow

The MacBook Pro uses GPT-6.2 Sol through Codex as its FirstMate supervisor. Herdr hosts the supervisor and worker panes. The Studio workflow in the new-Mac guide uses Claude Code as supervisor. Choose the launcher that matches the machine you are setting up.

## Start the Pro workflow

Start Herdr and enter `fm` in a fresh shell pane. The Pro launcher starts Codex from the FirstMate checkout with `--model gpt-6.2-sol`. Claude Code and Cursor Agent run in worker panes when FirstMate dispatches tasks. Sign in to the respective CLIs before dispatching. OpenRouter is optional and uses an authenticated OpenCode worker when configured.

## Context and provider usage

The Pro launcher sets the Codex footer to show the model, Git branch, context used, token count, and available allowance windows. It opens a separate Provider usage pane with quota-axi. The dashboard shows provider-reported quota, credit and spend figures when available. Claude Code uses the bundled status line for context and its reported session cost. An unavailable or signed-out provider has no live figures.

## Projects

FirstMate stores project checkouts under `$FM_HOME/projects/` and the local registry in `$FM_HOME/data/projects.md`. The Pro's local shell helpers are `fm-add-project OWNER/REPO` to clone and register a project, `fm --projects` to list checkouts, and `fm --project NAME` to start with one selected. Keep private project names and authentication out of the public dotfiles.

See the [Mac setup repository](https://github.com/karanmrn/mac-studio-setup) for package installation and the portable Mac workflow.
