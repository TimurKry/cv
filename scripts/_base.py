import base64
import datetime as dt
import html
import io
import json
import os
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
FONT_DIR = ROOT / "fonts"
OUT = ROOT / "cards"

# --------------------------------------------------------------------------- palette
THEMES = {
    "light": dict(paper="#F5F2EB", ink="#151514", muted="#6E6A62", line="#DDD7CA", cell0="#E6E0D3",
                  blue="#2D5BFF", red="#F0452B", yellow="#F6B800", on_blue="#FFFFFF", on_red="#FFFFFF",
                  on_yellow="#151514"),
    "dark": dict(paper="#121211", ink="#F2EEE6", muted="#8F8B83", line="#2A2926", cell0="#1F1E1C",
                 blue="#5A7DFF", red="#FF5A3D", yellow="#FFC61A", on_blue="#FFFFFF", on_red="#FFFFFF",
                 on_yellow="#151514"),
}


def mix(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


# --------------------------------------------------------------------------- fonts
FONTS = {  # css family -> file
    "S": "serif.woff2", "SI": "serif-italic.woff2", "G": "sans.woff2",
    "GB": "sans-semibold.woff2", "M": "mono.woff2",
}
_b64, _metrics = {}, {}


def font_css(families):
    rules = []
    for f in families:
        if f not in _b64:
            _b64[f] = base64.b64encode((FONT_DIR / FONTS[f]).read_bytes()).decode()
        rules.append(f"@font-face{{font-family:'{f}';src:url(data:font/woff2;base64,{_b64[f]}) format('woff2')}}")
    return "".join(rules)


def text_width(s, fam, size):
    if fam not in _metrics:
        t = TTFont(FONT_DIR / FONTS[fam])
        _metrics[fam] = (t.getBestCmap(), t["hmtx"].metrics, t["head"].unitsPerEm)
    cmap, hmtx, upm = _metrics[fam]
    w = 0
    for ch in s:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g else upm * 0.5
    return w * size / upm


def wrap(s, fam, size, max_w, max_lines=2):
    words, lines, cur = s.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_width(test, fam, size) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while text_width(lines[-1] + "…", fam, size) > max_w and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return [l for l in lines if l]


def esc(s):
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- svg shell
BASE_CSS = """
text{white-space:pre}
.S{font-family:'S',Georgia,serif}.SI{font-family:'SI',Georgia,serif;font-style:italic}
.G{font-family:'G',system-ui,sans-serif}.GB{font-family:'GB',system-ui,sans-serif;font-weight:600}
.M{font-family:'M',ui-monospace,monospace}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
.up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}
.fade{animation:fade .5s ease both}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def svg(w, h, body, families, css="", bg=None, th=None, defs=""):
    css_all = font_css(families) + BASE_CSS + css + ("*{animation:none!important}" if STATIC else "")
    shell = ""
    if bg is None and th is not None:
        shell = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" '
                 f'fill="{th["paper"]}" stroke="{th["line"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'fill="none"><defs><style>{css_all}</style>{defs}</defs>{shell}{body}</svg>')


def d(ms):  # animation-delay style
    return f'style="animation-delay:{int(ms)}ms"'


def countup(value, x, y, cls, size, fill, begin_ms, anchor="start", fmt="{:,}"):
    """Count-up number with SMIL <set> frames (CSS can't change text)."""
    if STATIC:
        return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
                f'text-anchor="{anchor}">{esc(fmt.format(value))}</text>')
    n, dur, out = 18, 900, []
    for i in range(n):
        t = i / (n - 1)
        v = round(value * (1 - (1 - t) ** 3))
        t0 = begin_ms + dur * i / n
        t1 = begin_ms + dur * (i + 1) / n
        sets = f'<set attributeName="visibility" to="visible" begin="{t0:.0f}ms" fill="freeze"/>'
        if i < n - 1:
            sets += f'<set attributeName="visibility" to="hidden" begin="{t1:.0f}ms" fill="freeze"/>'
        out.append(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
                   f'text-anchor="{anchor}" visibility="hidden">{esc(fmt.format(v))}{sets}</text>')
    return "".join(out)


