<!-- markdownlint-disable MD013 -->

# cc-assets

Public assets (pixel mascot icons, sounds) for Claude Code hooks. Hosted publicly
so that downstream services like the Bark iOS push API can fetch them by URL.

Owned by [@wangbin0619](https://github.com/wangbin0619); referenced from the
private utility repo `01-VibeCoding-Utility/01-Shared-Artifacts/51-sound/`:

- `03-bark-push.sh` — Stop hook → mission complete push
- `04-bark-push-notification.sh` — Notification hook → waiting-for-input push

## Clawd icons (`clawd/`)

Clawd is the Claude Code startup mascot
(see [anthropics/claude-code#24926](https://github.com/anthropics/claude-code/issues/24926)),
an 8-bit-style sprite drawn in the terminal with Unicode box-drawing characters:

```text
 ▐▛███▜▌
▜█████▛▘
▘▘    ▝▝
```

Each PNG is 512×512 RGBA, ~2.4 KB, rendered with `scripts/render_clawd.py`
(stdlib `zlib` + `struct`, no Pillow / no external image dependency).

| File | Background | Default use |
| :--- | :--- | :--- |
| `clawd/orange.png` | Anthropic peach (#D97757) | Notification hook (waiting-for-input) |
| `clawd/green.png` | Material Green 600 | — |
| `clawd/blue.png` | Material Blue 600 | — |
| `clawd/purple.png` | Material Purple 600 | — |
| `clawd/amber.png` | Material Amber 700 | — |
| `clawd/pink.png` | Material Pink 600 | — |
| `clawd/happy-green.png` | Material Green + arms-up Clawd pose | Stop hook (mission complete) |

## Raw URLs

```text
https://raw.githubusercontent.com/wangbin0619/cc-assets/main/clawd/<file>.png
```

## Third-party mascot packs (`space-invader/`, `pixel-buddy/`)

Re-rendered from [TeXmeijin/claude-code-mascot-statusline](https://github.com/TeXmeijin/claude-code-mascot-statusline)
under its MIT license (see `LICENSE-third-party-mascot-packs`). Each pack has
16 distinct 16×16 indexed-color sprites covering 10 session states:

| State | Frames | Suggested Bark use |
| :--- | :---: | :--- |
| `idle_1`, `idle_2` | 2 | — |
| `thinking_1..3` | 3 | — |
| `tool_1`, `tool_2` | 2 | — |
| `ok_1` | 1 | mission complete (tool_success) |
| `fail_1` | 1 | failure notification |
| `question_1` | 1 | waiting for input (Notification hook) |
| `permission_1` | 1 | permission prompt |
| `sub_1`, `sub_2` | 2 | subagent running |
| `done_1`, `done_2` | 2 | mission complete (Stop hook) |
| `auth_1` | 1 | auth success |

Two packs, same state set, different art:

- `space-invader/*.png` — purple arcade-style alien on dark purple (#1a0a2e) background
- `pixel-buddy/*.png`   — yellow pixel cat with antlers on off-white (#f8fafc) background

### APNG (animated) experiment

`space-invader/idle.apng.png` is a 2-frame Animated PNG (idle\_1 → idle\_2, 600 ms each, infinite loop), packaged with a `.png` extension so non-APNG-aware viewers see frame 1 as a static PNG. iOS Bark may render only the first frame in the lock-screen banner; swap the Bark `ICON=` URL to this file to test.

## Adding a new variant

1. Edit `scripts/render_clawd.py` (add an entry to `PALETTE` or a new ASCII pose),
   OR `scripts/render_packs.py` to add a new pack JSON source.
2. Run `python3 scripts/render_clawd.py` or `python3 scripts/render_packs.py` from repo root.
3. Commit the new PNG + the updated script.

### Re-render the third-party packs

Sources are saved in `sources/<pack>.pack.json` (verbatim copies of the upstream
`packs/<pack>/pack.json`, MIT). Run:

```bash
python3 scripts/render_packs.py
```

Outputs land in `space-invader/` and `pixel-buddy/`, 16 sprite PNGs + 1 APNG demo each.
