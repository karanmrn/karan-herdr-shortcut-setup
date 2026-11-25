# Set up a new Mac with an agent

The Mac Studio keeps running the fleet. The MacBook is a remote control by default.
Do not start a second fleet on the same projects. Do not copy fleet state, sessions,
logs, runner registrations, or credentials from the Studio.

After the clone in step 3, paste this prompt into Claude Opus:

> Read INSTALL-WITH-AN-AGENT.md in this repo and set up this Mac; stop and ask me at each STOP point

The person must complete steps 1 to 3 if an agent is not available yet. The
agent then checks those steps and continues. Run commands as the MacBook user.
A STOP requires the person to act before the agent continues. Never ask them to
paste a password, token, or key into the agent session. Do not print secrets.
Record failures and missing items in the final report. Do not claim an exact
match when an item has not been checked.

## 1. Prepare macOS and developer tools

**STOP:** Ask the person to finish macOS setup, sign in to Apple ID, connect to
the internet, and install updates. Ask them to approve permission prompts when
macOS displays them. Do not approve prompts on their behalf.

Run:

```sh
uname -m
xcode-select -p || xcode-select --install
```

Expected: `arm64` and a command-line tools path. If the installer opens, wait
for the person to finish it, then run `xcode-select -p` again. If the Mac is
not Apple silicon or the tools still fail, stop and report the output.

## 2. Install Homebrew and GitHub CLI

Install Homebrew using the current command at https://brew.sh/ if it is absent.
Review that command before running it. A password or installation prompt needs
the person. Then run:

```sh
eval "$(/opt/homebrew/bin/brew shellenv)"
brew --version
brew install gh git node
```

Expected: Homebrew prints its version and the packages install. If a command
fails, read its error, correct the prerequisite, and retry. Stop if it still
fails. Start a new terminal after the dotfiles are installed in step 4.

**STOP:** Ask the person to sign in to GitHub in the browser when prompted:

```sh
gh auth login
gh auth status
```

Expected: `gh auth status` reports a logged-in GitHub account. If it does not,
ask the person to repeat the login. Do not request their authentication code.

## 3. Clone the dotfiles

```sh
gh repo clone karanmrn/karan-herdr-shortcut-setup ~/.dotfiles-karan
git -C ~/.dotfiles-karan remote -v
```

Expected: the clone succeeds and the remote identifies the requested repository.
If the directory already exists, inspect its remote and local changes first. Do
not overwrite it. If access fails, check `gh auth status` and ask the person
to resolve access.

## 4. Install configuration and packages

```sh
~/.dotfiles-karan/install.sh
npm config set prefix "$HOME/.local"
brew bundle install --file="$HOME/.dotfiles-karan/Brewfile"
brew install --cask ghostty
```

The installer backs up replaced paths with a `pre-dotfiles` suffix. Review its
output. The Brewfile is a Studio snapshot and can download many packages. It
also contains npm and uv entries. A failure is not proof that later entries
installed. Read the error, fix the dependency, and rerun the bundle. Do not
delete backup files. Verify in a new terminal:

```sh
readlink ~/.zshrc
readlink ~/.config/agents/AGENTS.md
brew bundle check --file="$HOME/.dotfiles-karan/Brewfile"
```

Expected: the links point into `~/.dotfiles-karan` and the bundle check passes.
Report every package that remains missing. Do not infer full Studio parity from
this snapshot. The snapshot excludes tools installed by other methods.

## 5. Install harnesses and sign in

The Brewfile includes Claude Code, Codex, Pi and Grok. Check them:

```sh
command -v claude codex pi grok
claude --version
codex --version
```

If Codex is missing, run `npm install -g @openai/codex`. If Claude is missing,
run `brew install --cask claude-code@latest`. Check the commands again. Report
any package that still fails.

**STOP:** Ask the person to run `claude` and `codex` and complete each login.
Do not enter credentials for them. Check `claude auth status` and
`codex login status`. If either is not authenticated, ask the person to retry.

**STOP:** Ask the person to run `vercel login` and `supabase login` themselves.
Check `vercel whoami` and `supabase projects list`. A successful project list
can be empty. If a login or access check fails, report it and ask the person
to resolve account access. Do not capture or print tokens.

The Studio also uses other harnesses. Follow the publisher links in
[the harness table](docs/claude-code-on-a-new-mac.md#2-what-to-install) for
Oh My Pi, Devin, Hermes, T3 Code and Muse. Check each command in that table.
Report any unavailable installer, login, or missing command as incomplete.
Do not claim these tools are installed because the Brewfile passed.

## 6. Install skills and configure Claude

```sh
npx skills add -g karanmrn/kstack
npx skills add -g danyuchn/asd-ste100-skill
```

Select the harnesses in use when prompted. Expected: the installer reports
success. Check `~/.agents/skills` and each selected harness's skills directory.
Check for `SKILL.md` in the installed kstack skills and `asd-ste100`. If a
skill is absent, inspect the installer output and retry. Report remaining gaps.
Do not remove or replace custom skills without the person's instruction.

Configure the status line, plugins, MCP servers and hooks using
[Claude Code settings](docs/claude-code-on-a-new-mac.md#5-claude-code-settings).
Merge settings into existing JSON. Do not overwrite existing settings. Verify
with `claude plugin list` and `claude mcp list`. Report unavailable plugins or
servers. **STOP:** Ask the person to complete each service authentication in
Claude's `/mcp` interface. Never copy authentication files from the Studio.

## 7. Clone FirstMate and restore keys

```sh
gh repo clone karanmrn/firstmate ~/karan-agent-workspace
git -C ~/karan-agent-workspace remote -v
```

Expected: the remote identifies `karanmrn/firstmate`. If the directory exists,
inspect it and its remote. Do not overwrite or reset it. If cloning fails,
check GitHub access and report the error.

**STOP:** Ask the person to restore only needed keys from 1Password or Keychain.
They must create `~/karan-agent-workspace/data/keys.env` privately if needed.
They must never put keys in this repository or the conversation. After they
finish, check permissions without reading values:

```sh
test ! -e ~/karan-agent-workspace/data/keys.env || stat -f '%Lp %N' ~/karan-agent-workspace/data/keys.env
```

Expected: an existing file has mode `600`. Ask the person to run `chmod 600`
on it if needed. An absent file means no fleet keys have been restored. Report
that as incomplete if the person needs them. See
[Keys and secrets](docs/claude-code-on-a-new-mac.md#8-keys-and-secrets).

## 8. Check terminals and the remote-control session

```sh
herdr --version
herdr integration status
ls -d /Applications/WezTerm.app /Applications/Ghostty.app
```

Expected: Herdr reports a version and integration status. Both apps exist. If
a tool is missing, inspect the bundle output and install it. For missing Herdr
integrations, run `herdr integration install claude` and, if used,
`herdr integration install codex`. Check integration status again.

**STOP:** Ask the person to open WezTerm and Ghostty and approve any macOS
permissions. Check that each opens and reads its linked configuration. Ask the
person to check the appearance and shortcuts against the Studio. Report any
visual check they cannot make.

For remote control, connect to the Studio using the person's existing approved
remote access. Inspect the Studio for an existing FirstMate session first. If none exists, ask
the person to start one on the Studio. In its terminal, enter `herdr` and then
`fm`, as described in
[FirstMate and Herdr](docs/claude-code-on-a-new-mac.md#6-firstmate-and-herdr).
Do not start a new local fleet on the MacBook. If remote access or an existing
session is unavailable, stop and ask the person how to connect. Do not create
a replacement fleet. Confirm the session's host before giving it project work.

## 9. Install the daily update script

```sh
gh repo clone karanmrn/mac-studio-setup ~/mac-studio-setup
test -x ~/mac-studio-setup/scripts/update-all.sh
```

Expected: the clone succeeds and the script is executable. If the directory
exists, inspect its remote and changes before continuing. If the check fails,
report the error. Read the script before running it. It updates packages,
skills and FirstMate, and writes a log. Run it only when the person authorises
the updates and no local pipeline is active:

```sh
~/mac-studio-setup/scripts/update-all.sh
tail -n 50 ~/karan-agent-workspace/data/deck/update-all.log
```

Expected: the log ends with `done`. Inspect the entire new log section for
errors and skipped steps. The script can continue after failures, so `done`
alone is not proof of success. Report each failure. The script is available for
manual daily use. A scheduled LaunchAgent is not installed by these commands.

## 10. Final checklist

Run and report each check, including failures and items requiring the person:

```sh
uname -m
brew bundle check --file="$HOME/.dotfiles-karan/Brewfile"
gh auth status
claude auth status
codex login status
vercel whoami
supabase projects list
herdr --version
herdr integration status
command -v claude codex pi grok vercel supabase
ls -d /Applications/WezTerm.app /Applications/Ghostty.app
readlink ~/.zshrc
readlink ~/.config/agents/AGENTS.md
test -x ~/mac-studio-setup/scripts/update-all.sh
```

Also report the FirstMate remote, installed skills, Claude plugin and MCP
status, key-file permissions, and the person's terminal appearance check. State
whether the remote Studio session was actually reached. List every unchecked
Studio setting, missing tool, login, permission, key, and package. The checks
prove only the listed items. They do not prove that both Macs are identical.
