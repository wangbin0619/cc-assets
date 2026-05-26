"""Batch-render TeXmeijin's space-invader + pixel-buddy mascot packs to PNGs,
plus one APNG demo (space-invader idle animation, 2 frames @ 600ms).

Source: https://github.com/TeXmeijin/claude-code-mascot-statusline (MIT, © 2026 meijin).
Reproduced with attribution in cc-assets/README.md.
"""
import json, struct, zlib, os

def hexrgb(h):
    h = h.lstrip('#')
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def render(grid, palette_rgb, canvas, scale, bg_rgb):
    src_h, src_w = len(grid), len(grid[0])
    bw, bh = src_w * scale, src_h * scale
    ox, oy = (canvas - bw)//2, (canvas - bh)//2
    buf = bytearray(canvas * canvas * 4)
    for y in range(canvas):
        for x in range(canvas):
            mx, my = (x - ox)//scale, (y - oy)//scale
            if 0 <= mx < src_w and 0 <= my < src_h:
                idx = grid[my][mx]
                rgb = palette_rgb[idx] if idx and palette_rgb[idx] is not None else bg_rgb
            else:
                rgb = bg_rgb
            i = (y*canvas + x) * 4
            buf[i:i+4] = bytes((rgb[0], rgb[1], rgb[2], 255))
    return buf

def png_chunk(tag, data):
    crc = zlib.crc32(tag + data)
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc & 0xffffffff)

def compress_scanlines(buf, w, h):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(buf[y*w*4:(y+1)*w*4])
    return zlib.compress(bytes(raw), level=9)

def write_png(buf, w, h, out):
    with open(out, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        f.write(png_chunk(b"IDAT", compress_scanlines(buf, w, h)))
        f.write(png_chunk(b"IEND", b""))

def write_apng(frame_bufs, w, h, delay_ms_per_frame, out, num_plays=0):
    """APNG with shared IHDR. Each frame is full-canvas, no offset, dispose=APNG_DISPOSE_OP_NONE, blend=APNG_BLEND_OP_SOURCE.
    Sequence: IHDR → acTL → (fcTL → IDAT) for frame 0 → for i≥1: (fcTL → fdAT) → IEND."""
    n = len(frame_bufs)
    with open(out, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        f.write(png_chunk(b"acTL", struct.pack(">II", n, num_plays)))
        seq = 0
        # Frame 0: fcTL + IDAT
        f.write(png_chunk(b"fcTL", struct.pack(">IIIIIHHBB",
            seq, w, h, 0, 0,
            delay_ms_per_frame[0], 1000,  # delay numerator / denominator (ms)
            1,  # dispose_op = 1 (APNG_DISPOSE_OP_BACKGROUND) — clear region
            0   # blend_op = 0 (SOURCE)
        )))
        seq += 1
        f.write(png_chunk(b"IDAT", compress_scanlines(frame_bufs[0], w, h)))
        # Frames 1..n-1: fcTL + fdAT
        for i in range(1, n):
            f.write(png_chunk(b"fcTL", struct.pack(">IIIIIHHBB",
                seq, w, h, 0, 0,
                delay_ms_per_frame[i], 1000, 1, 0
            )))
            seq += 1
            fdat = struct.pack(">I", seq) + compress_scanlines(frame_bufs[i], w, h)
            f.write(png_chunk(b"fdAT", fdat))
            seq += 1
        f.write(png_chunk(b"IEND", b""))

PACKS = {
    'space-invader': {
        'src': 'sources/space-invader.pack.json',
        'out': 'space-invader',
        'bg':  hexrgb('#1a0a2e'),  # dark purple (palette[1])
    },
    'pixel-buddy': {
        'src': 'sources/pixel-buddy.pack.json',
        'out': 'pixel-buddy',
        'bg':  hexrgb('#f8fafc'),  # light gray (palette light slot)
    },
}

CANVAS = 512
SCALE = 32  # 16×16 → 512×512

for pack_name, cfg in PACKS.items():
    os.makedirs(cfg['out'], exist_ok=True)
    with open(cfg['src']) as f:
        d = json.load(f)
    pal_rgb = [None if c is None else hexrgb(c) for c in d['sprite']['palette']]
    for sprite_name, grid in d['sprites'].items():
        buf = render(grid, pal_rgb, CANVAS, SCALE, cfg['bg'])
        write_png(buf, CANVAS, CANVAS, f"{cfg['out']}/{sprite_name}.png")
    print(f"  {pack_name}: rendered {len(d['sprites'])} sprites to {cfg['out']}/")

# APNG demo: space-invader idle (2 frames @ 600ms)
print("\nBuilding APNG demo: space-invader idle (2 frames × 600ms each)...")
with open(PACKS['space-invader']['src']) as f:
    d = json.load(f)
pal_rgb = [None if c is None else hexrgb(c) for c in d['sprite']['palette']]
bg = PACKS['space-invader']['bg']
frames = d['states']['idle']  # ['idle_1','idle_2']
bufs = [render(d['sprites'][n], pal_rgb, CANVAS, SCALE, bg) for n in frames]
out_apng = f"{PACKS['space-invader']['out']}/idle.apng.png"
write_apng(bufs, CANVAS, CANVAS, [600, 600], out_apng, num_plays=0)
print(f"  wrote {out_apng}  ({os.path.getsize(out_apng)} B)  — file ext .png so iOS treats as PNG, APNG-aware decoders animate")
