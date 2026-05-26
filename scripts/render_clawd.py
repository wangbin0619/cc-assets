"""Render Clawd mascot in multiple background colors. Pure stdlib (no Pillow)."""
import struct, zlib, os

# Box-drawing → 2×2 sub-cell fill (TL, TR, BL, BR).
CMAP = {
    ' ': (0,0,0,0),
    '▘': (1,0,0,0), '▝': (0,1,0,0), '▖': (0,0,1,0), '▗': (0,0,0,1),
    '▀': (1,1,0,0), '▄': (0,0,1,1), '▌': (1,0,1,0), '▐': (0,1,0,1),
    '▙': (1,0,1,1), '▟': (0,1,1,1), '▛': (1,1,1,0), '▜': (1,1,0,1),
    '▞': (0,1,1,0), '▚': (1,0,0,1), '█': (1,1,1,1),
}

CLAWD = [
    " ▐▛███▜▌",
    "▜█████▛▘",
    "▘▘    ▝▝",
]
CLAWD_HAPPY = [   # arms-up celebration pose, 4 rows
    "▝      ▘",
    " ▐▛██▜▌ ",
    "▜█████▛▘",
    "▘▘    ▝▝",
]

def render(mascot, bg_color, out_path, canvas=512, scale=24):
    cols = max(len(l) for l in mascot)
    rows = [l.ljust(cols) for l in mascot]
    raw_w, raw_h = cols * 2, len(rows) * 2

    # Build a fill mask.
    mask = [[0] * raw_w for _ in range(raw_h)]
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            tl, tr, bl, br = CMAP.get(ch, (0,0,0,0))
            x, y = c * 2, r * 2
            if tl: mask[y  ][x  ] = 1
            if tr: mask[y  ][x+1] = 1
            if bl: mask[y+1][x  ] = 1
            if br: mask[y+1][x+1] = 1

    big_w, big_h = raw_w * scale, raw_h * scale
    ox = (canvas - big_w) // 2
    oy = (canvas - big_h) // 2

    BG = bg_color
    FG = (255, 255, 255)

    buf = bytearray(canvas * canvas * 4)
    for y in range(canvas):
        for x in range(canvas):
            mx = (x - ox) // scale
            my = (y - oy) // scale
            if 0 <= mx < raw_w and 0 <= my < raw_h and mask[my][mx]:
                r, g, b = FG
            else:
                r, g, b = BG
            i = (y * canvas + x) * 4
            buf[i:i+4] = bytes((r, g, b, 255))

    def chunk(tag, data):
        crc = zlib.crc32(tag + data)
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc & 0xffffffff)

    raw = bytearray()
    for y in range(canvas):
        raw.append(0)
        raw.extend(buf[y * canvas * 4 : (y + 1) * canvas * 4])
    idat = zlib.compress(bytes(raw), level=9)

    with open(out_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", canvas, canvas, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))

OUT = "clawd"
os.makedirs(OUT, exist_ok=True)

# 6 standard-pose Clawds in different background colors.
PALETTE = {
    "orange": (217, 119, 87),   # Anthropic peach (default Clawd)
    "green":  (67,  160, 71),   # Material Green 600 — completion / success
    "blue":   (30,  136, 229),  # Material Blue 600 — calm / info
    "purple": (142, 36,  170),  # Material Purple 600 — distinct alternative
    "amber":  (251, 140, 0),    # Material Amber 700 — attention / waiting
    "pink":   (216, 27,  96),   # Material Pink 600 — high-contrast alt
}
for name, rgb in PALETTE.items():
    p = f"{OUT}/{name}.png"
    render(CLAWD, rgb, p)
    print(f"  wrote {p}  ({os.path.getsize(p)} B)")

# Bonus: arms-up "happy" Clawd in green — for celebration / mission complete.
p = f"{OUT}/happy-green.png"
render(CLAWD_HAPPY, PALETTE["green"], p, scale=20)  # smaller scale (4 rows → fits)
print(f"  wrote {p}  ({os.path.getsize(p)} B)")
