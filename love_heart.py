import math as m
import random as r
import turtle as t
import tkinter.font as tkf

SC = 21
OY = 20
DURATION = 10
TICK = 16
ANIM = 42
LIFT = 34
GAP = 7
SIZES = (9, 10, 11, 12)
FONT = "Segoe UI"
BG = "#06010a"   # Ultra-deep obsidian purple background matching image

# ----------------------------------------------------------------------------
# Screen & Landscape Right-Dock Setup (matching EYE)
# ----------------------------------------------------------------------------
s = t.Screen()
cv = s.getcanvas()
root = cv.winfo_toplevel()
root.title("Love Heart - Multilingual Neon Living Heart")
s.bgcolor(BG)
s.tracer(0)

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
win_w = min(1040, max(750, sw - 80))
win_h = min(720, max(520, sh - 120))
r_px = max(0, sw - win_w - 60)
r_py = max(0, (sh - win_h) // 2 - 20)

s.setup(width=win_w, height=win_h, startx=r_px, starty=r_py)

def snap_right(event=None):
    curr_sw = root.winfo_screenwidth()
    curr_sh = root.winfo_screenheight()
    rx = max(0, curr_sw - win_w - 60)
    ry = max(0, (curr_sh - win_h) // 2 - 20)
    root.geometry(f"{win_w}x{win_h}+{rx}+{ry}")

def snap_center(event=None):
    curr_sw = root.winfo_screenwidth()
    curr_sh = root.winfo_screenheight()
    cx = max(0, (curr_sw - win_w) // 2)
    cy = max(0, (curr_sh - win_h) // 2 - 20)
    root.geometry(f"{win_w}x{win_h}+{cx}+{cy}")

is_topmost = False
def toggle_topmost(event=None):
    global is_topmost
    is_topmost = not is_topmost
    root.attributes("-topmost", is_topmost)

def on_close(event=None):
    try:
        root.destroy()
    except Exception:
        pass

root.bind("<Right>", snap_right)
root.bind("<c>", snap_center)
root.bind("<C>", snap_center)
root.bind("<t>", toggle_topmost)
root.bind("<T>", toggle_topmost)
root.bind("<Escape>", on_close)
root.bind("<q>", on_close)
root.bind("<Q>", on_close)
root.protocol("WM_DELETE_WINDOW", on_close)

# Elevate and focus on launch
snap_right()
root.lift()
root.attributes("-topmost", True)
root.after(600, lambda: root.attributes("-topmost", False) if not is_topmost else None)
root.focus_force()
root.after_idle(snap_right)
root.after(60, snap_right)
root.after(150, snap_right)

rng = r.Random(11)

# Authentic multilingual phrases matching reference image
PHRASES = [
    "Ich liebe dich", "Ti amo", "Je t'aime", "αγαπώ", "Te amo", 
    "我爱你", "मैं तुमसे प्यार करता हूँ", "Aku cinta kamu", "사랑해", 
    "Seni seviyorum", "愛してる", "Jag älskar dig", "I love you", 
    "我喜欢你", "Σ' αγαπώ", "Я тебя кохаю", "Anh yêu em", 
    "मैं तुम्हें प्यार करता हूँ", "I te amo", "Kocham cię", 
    "Я тебя люблю", "Ik hou van jou", "Eu te amo", "Alku cinta kamu",
    "ฉันรักเธอ"
]

# Signature Neon Palette extracted directly from the reference image
NEON_PALETTE = [
    (1.00, 0.12, 0.62),  # Hot Neon Pink / Magenta
    (0.00, 0.88, 1.00),  # Electric Cyan / Neon Aqua
    (0.74, 0.22, 1.00),  # Electric Violet / Purple
    (1.00, 0.32, 0.54),  # Neon Coral / Warm Rose
    (0.12, 0.78, 1.00),  # Vibrant Sky Blue
    (0.95, 0.22, 0.82),  # Radiant Fuchsia Orchid
]

_fonts = {}


def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(
            root=cv, family=FONT, size=size, weight="bold"
        )
    return _fonts[size]


def heart(a):
    x = 16 * (m.sin(a) ** 3)
    y = (
        13 * m.cos(a)
        - 5 * m.cos(2 * a)
        - 2 * m.cos(3 * a)
        - m.cos(4 * a)
    )
    return x * SC, y * SC + OY


def hx(c):
    return "#%02x%02x%02x" % tuple(
        int(max(0, min(1, v)) * 255) for v in c
    )


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def dim(c, k):
    return tuple(v * k for v in c)


POLY = [heart(2 * m.pi * i / 720) for i in range(720)]
EDGES = list(zip(POLY, POLY[1:] + POLY[:1]))
YMAX = max(p[1] for p in POLY)
YMIN = min(p[1] for p in POLY)
CY = (YMAX + YMIN) / 2


def spans(y):
    xs = []
    for (x1, y1), (x2, y2) in EDGES:
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return list(zip(xs[0::2], xs[1::2]))


def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 14:
                out.append((lo, hi))
    return out


def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        yield from order


def math_dist(x, y):
    return m.hypot(x / (16 * SC), (y - CY) / (14.5 * SC))


def build():
    cycle = phrase_cycle()
    row_h = max(font_for(z).metrics("linespace") for z in SIZES) + 4
    half = row_h / 2
    placed = []

    y = YMAX - half
    row_idx = 0
    while y > YMIN + half:
        row = intersect(spans(y + half), spans(y - half))
        row_idx += 1

        for lo, hi in row:
            lo += 4
            hi -= 4
            cur = lo + rng.uniform(0, 8)
            line = []

            while True:
                fit = None
                for _ in range(12):
                    text = next(cycle)
                    size = rng.choice(SIZES)
                    w = font_for(size).measure(text)
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + GAP

            if not line:
                continue

            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2

            for i, (x, text, size, w) in enumerate(line):
                edge = i == 0 or i == len(line) - 1
                # Alternating neon palette assignment matching reference image
                color_idx = (len(placed) * 2 + row_idx + rng.choice([0, 1])) % len(NEON_PALETTE)
                neon_col = NEON_PALETTE[color_idx]
                placed.append(dict(x=x, y=y, text=text, size=size, edge=edge, color=neon_col))

        y -= row_h

    for p in placed:
        rad = min(1.0, math_dist(p["x"], p["y"]))
        p["rad"] = rad

    edges = [p for p in placed if p["edge"]]
    inner = [p for p in placed if not p["edge"]]
    edges.sort(key=lambda p: m.atan2(p["x"], p["y"] - CY) % (2 * m.pi))
    inner.sort(key=lambda p: -p["rad"] + rng.uniform(0, 0.08))
    return edges + inner


# ----------------------------------------------------------------------------
# Perimeter Neon Contour, Sparkles & Floating Border Hearts (matching image)
# ----------------------------------------------------------------------------
PERIMETER_HEARTS = [
    (0, 138, "♥", 15, (0.76, 0.22, 1.00)),       # top center purple heart
    (-260, 205, "✦", 10, (1.00, 0.25, 0.70)),    # upper left sparkle
    (-360, 45, "♡", 19, (1.00, 0.18, 0.65)),     # left flank hollow heart
    (-300, -100, "♥", 12, (1.00, 0.32, 0.55)),   # lower left heart
    (-170, -210, "✦", 11, (0.00, 0.88, 1.00)),   # bottom left cyan star
    (0, -355, "♥", 14, (1.00, 0.22, 0.65)),      # bottom tip heart
    (170, -210, "✦", 10, (1.00, 0.25, 0.70)),    # bottom right sparkle
    (270, -105, "♥", 14, (1.00, 0.20, 0.65)),    # lower right heart
    (360, 35, "♥", 16, (1.00, 0.20, 0.65)),      # right flank heart
    (310, 175, "♥", 13, (0.76, 0.22, 1.00)),     # upper right heart
    (140, 215, "✦", 10, (0.00, 0.88, 1.00)),     # upper right sparkle
]

# Draw soft neon perimeter glow line
perimeter_ids = []
for i in range(0, 720, 16):
    p1 = heart(2 * m.pi * i / 720)
    p2 = heart(2 * m.pi * ((i + 10) % 720) / 720)
    # subtle glowing dotted contour
    col = (1.0, 0.18, 0.60) if (i // 16) % 2 == 0 else (0.76, 0.22, 1.00)
    lid = cv.create_line(p1[0], -p1[1], p2[0], -p2[1], fill=hx(dim(col, 0.25)), width=1)
    perimeter_ids.append(lid)

# Draw decorative perimeter hearts & sparkles
border_items = []
for px, py, sym, sz, c in PERIMETER_HEARTS:
    # Outer bloom
    cv.create_text(px, -py, text=sym, font=(FONT, sz + 2, "bold"), fill=hx(dim(c, 0.30)))
    # Core neon icon
    tid = cv.create_text(px, -py, text=sym, font=(FONT, sz, "bold"), fill=hx(c))
    border_items.append((tid, c))


FLASH = (1.0, 0.92, 0.98)
main_ids = []
active = []
tick_no = 0


def clamp(v):
    return max(0.0, min(1.0, v))


def spawn(p):
    x, y = p["x"], -p["y"]
    size, text, c = p["size"], p["text"], p["color"]
    font = (FONT, size, "bold")
    glow_font = (FONT, size + 2, "bold")

    # Layered Neon Glow:
    # 1. Outer ambient bloom (large, soft translucent hue)
    glow = cv.create_text(x, y, text=text, font=glow_font, fill=BG)
    # 2. Mid-layer halo (offset for volumetric bloom)
    halo = cv.create_text(x + 1, y + 1, text=text, font=font, fill=BG)
    # 3. Core crisp filament text
    main = cv.create_text(x, y - LIFT, text=text, font=font, fill=BG)

    p.update(glow=glow, halo=halo, main=main,
             f=0, dx=rng.uniform(-10, 10))
    main_ids.append((main, c, glow, halo))
    active.append(p)


def animate(p):
    p["f"] += 1
    u = clamp(p["f"] / ANIM)
    e = 1 - (1 - u) ** 3
    c = p["color"]
    x, y = p["x"], -p["y"]
    hover = (1 - e) * LIFT
    px = x + p["dx"] * (1 - e)
    py = y - hover

    # Volumetric neon blooming during animation
    cv.itemconfig(p["glow"], fill=hx(mix(BGC, dim(c, 0.28), e)))
    cv.itemconfig(p["halo"], fill=hx(mix(BGC, dim(c, 0.48), e * e)))
    cv.coords(p["glow"], px, py)
    cv.coords(p["halo"], px + 1, py + 1)

    flash = 0.75 * math_sin(clamp((u - 0.55) / 0.45))
    col = mix(mix(BGC, c, e ** 1.4), FLASH, flash)
    cv.itemconfig(p["main"], fill=hx(col))
    cv.coords(p["main"], px, py)

    if u >= 1:
        cv.coords(p["glow"], x, y)
        cv.coords(p["halo"], x + 1, y + 1)
        cv.coords(p["main"], x, y)
        cv.itemconfig(p["glow"], fill=hx(dim(c, 0.26)))
        cv.itemconfig(p["halo"], fill=hx(dim(c, 0.46)))
        cv.itemconfig(p["main"], fill=hx(c))
        return False
    return True


def math_sin(v):
    return m.sin(m.pi * v)


BGC = tuple(int(BG[i:i + 2], 16) / 255 for i in (1, 3, 5))
ORDER = build()
items = iter(ORDER)
RATE = len(ORDER) / (DURATION * 1000 / TICK)
acc = 0.0
spawning = True


def step():
    global spawning, acc
    if spawning:
        acc += RATE
        try:
            while acc >= 1:
                acc -= 1
                spawn(next(items))
        except StopIteration:
            spawning = False

    active[:] = [p for p in active if animate(p)]

    if not spawning and not active:
        shimmer()
        return
    cv.after(TICK, step)


def _safe(i, c):
    try:
        cv.itemconfig(i, fill=hx(c))
    except Exception:
        pass


def shimmer():
    if main_ids:
        for _ in range(1):
            main, c, glow, halo = rng.choice(main_ids)
            # Flash core filament to crystal white-neon & intensify glow
            _safe(main, mix(c, FLASH, 0.85))
            _safe(halo, mix(c, FLASH, 0.50))
            cv.after(240, lambda m=main, h=halo, col=c: (_safe(m, col), _safe(h, dim(col, 0.46))))

    # Gentle ambient breathing on perimeter border hearts
    if border_items and rng.random() < 0.4:
        tid, c = rng.choice(border_items)
        _safe(tid, mix(c, FLASH, 0.6))
        cv.after(300, lambda t=tid, col=c: _safe(t, col))

    cv.after(140, shimmer)


try:
    cv.after(200, step)
    t.done()
except (t.Terminator, Exception):
    pass
