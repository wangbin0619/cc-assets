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

## Adding a new variant

1. Edit `scripts/render_clawd.py` (add an entry to `PALETTE` or a new ASCII pose).
2. Run `python3 scripts/render_clawd.py` from repo root.
3. Commit the new PNG + the updated script.
