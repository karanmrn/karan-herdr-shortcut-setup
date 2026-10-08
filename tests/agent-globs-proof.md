# Agent unmatched-glob proof

The source baseline and remote main were `5ef6580d4b2f470ac1a34a8fa65d71526882de5b`.
The tests used `/bin/zsh` 5.9 on 8 October 2026.
The disposable worktree was `/Users/karanmanoharan/.treehouse/dotfiles-ac064d/1/dotfiles`.

## Native shell reproduction

Each shell received an explicit environment with a disposable `HOME`, system `PATH`, and `LC_ALL=C`.
Only each test's specified markers entered the shell.
The tests used native `zsh -d -c` startup, with `-l` or `-i` where specified.
`-d` suppresses global RC files after the unavoidable global zshenv startup.
The tests did not source the live `.zshrc` or any secrets.

The first test ran before `home/.zshenv` existed.

```text
python3 -B tests/test_agent_globs.py
AssertionError: 1 != 0 : zsh:1: no matches found: --include*.ts
Ran 1 test in 0.007s
FAILED (failures=1)
TEST_EXIT=1
```

The same test ran after adding the gated `.zshenv`.

```text
python3 -B tests/test_agent_globs.py
Ran 1 test in 0.009s
OK
TEST_EXIT=0
```

The probes established the shell as the cause.
Quoted `--include*.ts` reached printf with exit 0.
Explicit `NO_NOMATCH` let the unquoted argument reach printf with exit 0.
A fake `.zshrc` containing `NO_NOMATCH` did not fix noninteractive startup, which exited 1.

## Installer reproduction

The installer test ran after `.zshenv` existed, before its installer link call existed.
The destination was a regular file in a fake home.
The installer exited 0 but did not replace the destination with a symlink.

```text
python3 -B tests/test_agent_globs.py AgentGlobsTest.test_installer_backs_up_regular_zshenv_and_activates_gate
AssertionError: False is not true : link   .zshrc
Ran 1 test in 0.072s
FAILED (failures=1)
TEST_EXIT=1
```

The same test ran after adding `link ".zshenv"` to the existing installer path.

```text
python3 -B tests/test_agent_globs.py AgentGlobsTest.test_installer_backs_up_regular_zshenv_and_activates_gate
Ran 1 test in 0.110s
OK
TEST_EXIT=0
```

Both red phases used uncommitted test files.
There is no failing-test commit hash.

## Complete verification

```text
python3 -B tests/test_agent_globs.py
Ran 11 tests in 0.769s
OK
TEST_EXIT=0
/bin/zsh -n home/.zshenv                         exit 0
/bin/bash -n install.sh                         exit 0
shellcheck --shell=bash install.sh home/.zshenv  exit 0
Python ast.parse(tests/test_agent_globs.py)       PASS
git diff --check                                exit 0
```

ShellCheck checked the Bash-compatible syntax subset in `.zshenv`.
Native zsh syntax and execution checks provided zsh-specific proof.

The tests cover these behaviors:

- Exact `CLAUDECODE=1` or nonempty `CODEX_THREAD_ID` permits unmatched consumer flags and paths.
- Login and nonlogin noninteractive shells load the gate through native startup.
- Empty markers, `CLAUDECODE=0`, `true`, `01`, and Firstmate-only markers retain NOMATCH.
- Matching ordinary paths and matching include patterns still expand.
- Quoted patterns remain literal, and cat still rejects a missing file.
- Human interactive shells retain NOMATCH and the native startup order.
- Startup produces no additional output and preserves PATH.
- `ZDOTDIR` relocation and `-f` retain native semantics.
- The installer preserves regular files, valid links, and dangling links as backups.
- An absent destination becomes a link, and the intended link remains unchanged on repeat installation.

## Primary checkout and live-home preservation

The worker only read the primary checkout at `/Users/karanmanoharan/.dotfiles-karan`.
Before and after snapshots matched for HEAD, status, tracked diff, staged diff, and all seven dirty/untracked files.
The snapshots also matched inode, mode, modification time, and link target for all 11 inspected live destinations.
The snapshot SHA256 was `908b61fbd9c50c87bb9078f474872540c3b79b60cd6d5e5fd12f2034cfa1cae7` in both cases.

| Primary dirty/untracked file | Unchanged SHA256 |
| --- | --- |
| `home/.config/agents/AGENTS.md` | `c4a78a7142240fd37dbfa397247369034a0b210ae2340e96a39cfcadbf88eee1` |
| `home/.config/herdr/config.toml` | `0b9314153239b78311c391d7703913a4537e4b2e531b62a8441a7a178c78b131` |
| `home/.cursor/rules/jev-review.mdc` | `5dd3d00fc463a2f362949df73b6242044e6836615e25865c975a168f8aa9dd55` |
| `home/.zshrc` | `7d6d961b6ac36a91fb08b2ee7bfeb3cf10a8e783e04539e7cf5e51bb29c90054` |
| `home/firstmate-env.zsh` | `52603890e0773950aee4c099d9b17ff672b4a37b9712b0031583c30b6d9d43ed` |
| `install.sh` | `d06e41d0e87925c6be83b832476414ac871f494a9fc6a99558005250b7fe5a4f` |
| `scripts/check-jev-routing.py` | `350e280485ba7303b2fad4a244cc19502055044ce1b6b672ec51be9d9883d948` |

The live `.zshenv` retained its link to `/nix/store/h5n8zbgryphmhkcl1x8iy1d3mgcyknib-home-manager-files/.zshenv`.
The live `.zshrc` retained its link to `/Users/karanmanoharan/.dotfiles-karan/home/.zshrc`.
The other recorded destinations were `.zprofile`, `.dotfiles`, and the seven remaining installer destinations.

No live-home installation, Home Manager rebuild, Nix-store change, tool update, or no-mistakes run occurred.
Firstmate owns merge and later live activation.
A merged source PR does not install this fix in the live shell.
