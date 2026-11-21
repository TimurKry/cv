#!/usr/bin/env python3
"""Render the animated SVG cards for this repo's README (cards/ and cards/dark/).

  pip install fonttools brotli
  python scripts/render_cv_cards.py           # animated
  STATIC=1 python scripts/render_cv_cards.py  # final frame only

Edit the CV dict below, re-run, commit.
"""
import datetime as dt

from _base import THEMES, ROOT, STATIC, svg, d, esc, countup, text_width, mix  # noqa: E402

CV = {
    "name": "Timur Kryvasheyev",
    "role": "Full-Stack / Frontend Developer",
    "stack": "React · TypeScript · Next.js · Node.js · SQL",
    "meta": "Leipzig, Germany · EU citizen · remote / hybrid / relocation",
    "status": "Open to work",
    "stats": [  # value, suffix, label
        (6, "+", "years building for the web"),
        (7, "", "freelance client sites shipped"),
        (2, "+", "years in global MedTech"),
        (4, "", "languages: RU · BE · DE · EN"),
    ],
    "timeline_start": (2020, 1),
    "jobs": [  # title, company, start, end(None=now), color
        ("Freelance Full-Stack Developer", "Custom, Tilda, Webflow, Shopify", (2020, 6), None, "blue"),
        ("Game / XR Developer", "Actrio Studio · Unity, C#", (2021, 9), (2022, 7), "yellow"),
        ("Full-Stack Developer", "Straumann Group · MedTech", (2023, 10), (2026, 6), "red"),
    ],
    "skills": [
        ("FRONTEND", ["TypeScript", "React", "Next.js", "Tailwind", "Figma"]),
        ("BACKEND", ["Node.js", "REST APIs", "XML", "Scraping"]),
        ("DATA", ["SQL", "MySQL", "Schema design", "Query tuning"]),
        ("AI & TOOLS", ["Gemini API", "OpenAI API", "Cursor", "Git", "Docker"]),
    ],
}

OUT = ROOT / "cards"


def header(th):
    W, H = 840, 250
    x = 32
    pill_w = text_width(CV["status"], "M", 12) + 44
    body = [
        f'<text class="M up" x="{x}" y="48" font-size="11" fill="{th["muted"]}" letter-spacing="2.5">'
        f'CURRICULUM VITAE · {dt.date.today().year}</text>',
        f'<g class="up" {d(150)}><rect x="{W - 32 - pill_w}" y="28" width="{pill_w}" height="30" rx="15" '
        f'fill="{mix(th["paper"], th["blue"], .12)}" stroke="{th["blue"]}"/>'
        + ('' if STATIC else f'<circle class="pulse" cx="{W - 32 - pill_w + 18}" cy="43" r="9" fill="{th["blue"]}"/>') +
        f'<circle cx="{W - 32 - pill_w + 18}" cy="43" r="4" fill="{th["blue"]}"/>'
        f'<text class="M" x="{W - 32 - pill_w + 32}" y="47.5" font-size="12" fill="{th["blue"]}">'
        f'{esc(CV["status"])}</text></g>',
        f'<text class="S up" x="{x - 3}" y="122" font-size="66" fill="{th["ink"]}" letter-spacing="-1.5" '
        f'{d(250)}>{esc(CV["name"])}</text>',
        f'<text class="GB up" x="{x}" y="160" font-size="20" fill="{th["ink"]}" {d(400)}>{esc(CV["role"])}</text>',
        f'<text class="M up" x="{x}" y="186" font-size="12.5" fill="{th["blue"]}" {d(480)}>{esc(CV["stack"])}</text>',
        f'<line class="draw" x1="{x}" y1="206" x2="{W - 32}" y2="206" stroke="{th["line"]}" {d(600)}/>',
        f'<text class="M up" x="{x}" y="230" font-size="11.5" fill="{th["muted"]}" {d(650)}>{esc(CV["meta"])}</text>',
    ]
    css = """
.pulse{transform-box:fill-box;transform-origin:center;animation:pl 2.2s ease-out infinite}
@keyframes pl{0%{transform:scale(.4);opacity:.6}100%{transform:scale(1.6);opacity:0}}
.draw{stroke-dasharray:800;animation:dr 1.1s cubic-bezier(.6,0,.2,1) both}
@keyframes dr{from{stroke-dashoffset:800}to{stroke-dashoffset:0}}
"""
    return svg(W, H, "".join(body), ["S", "GB", "M"], css, th=th)


def stats(th):
    W, H = 840, 150
    cw = (W - 64) / 4
    body = []
    for i, (v, suf, label) in enumerate(CV["stats"]):
        x = 32 + i * cw
        if i:
            body.append(f'<line x1="{x - 14}" y1="34" x2="{x - 14}" y2="{H - 30}" stroke="{th["line"]}"/>')
        col = th["blue"] if i == 0 else th["ink"]
        body.append(countup(v, x, 86, "S", 54, col, 150 + i * 130, fmt="{}" + suf))
        body.append(f'<text class="G up" x="{x}" y="116" font-size="12.5" fill="{th["muted"]}" '
                    f'{d(250 + i * 130)}>{esc(label)}</text>')
    return svg(W, H, "".join(body), ["S", "G"], th=th)


def timeline(th):
    W = 840
    jobs = CV["jobs"]
    H = 110 + len(jobs) * 62
    x0, x1 = 32, W - 32
    today = dt.date.today()
    sy, sm = CV["timeline_start"]
    t0 = sy * 12 + sm
    t1 = today.year * 12 + today.month + 4

    def X(ym):
        return x0 + (ym[0] * 12 + ym[1] - t0) / (t1 - t0) * (x1 - x0)

    body = [f'<text class="M up" x="{x0}" y="44" font-size="11" fill="{th["muted"]}" letter-spacing="2.5">'
            f'EXPERIENCE · TIMELINE</text>']
    axis_y = H - 34
    for y in range(sy, today.year + 1):
        xx = X((y, 1))
        body.append(f'<line x1="{xx:.1f}" y1="64" x2="{xx:.1f}" y2="{axis_y}" stroke="{th["line"]}" '
                    f'stroke-dasharray="2 4"/>')
        body.append(f'<text class="M fade" x="{xx + 4:.1f}" y="{axis_y + 20}" font-size="10.5" '
                    f'fill="{th["muted"]}" {d(100)}>{y}</text>')
    nx = X((today.year, today.month))
    body.append(f'<line x1="{nx:.1f}" y1="64" x2="{nx:.1f}" y2="{axis_y}" stroke="{th["blue"]}" '
                f'stroke-width="1.5"/><text class="M" x="{nx - 4:.1f}" y="{axis_y + 20}" font-size="10.5" '
                f'text-anchor="end" fill="{th["blue"]}">now</text>')
    for i, (title, sub, start, end, color) in enumerate(jobs):
        y = 76 + i * 62
        a = X(start)
        b = X(end or (today.year, today.month))
        fg = th["on_" + color]
        span = f'{start[1]:02d}/{start[0]} – ' + (f'{end[1]:02d}/{end[0]}' if end else "present")
        body.append(f'<rect class="bar" x="{a:.1f}" y="{y}" width="{b - a:.1f}" height="40" rx="8" '
                    f'fill="{th[color]}" {d(250 + i * 200)}/>')
        if not end and not STATIC:
            body.append(f'<circle class="pulse" cx="{b:.1f}" cy="{y + 20}" r="10" fill="{th[color]}"/>')
        # put labels inside the bar if they fit, else to its right/left
        tw = max(text_width(title, "GB", 13.5), text_width(sub + "  " + span, "M", 10.5)) + 24
        if b - a >= tw:
            tx, anchor, c1, c2 = a + 12, "start", fg, fg
        elif x1 - b >= tw:
            tx, anchor, c1, c2 = b + 12, "start", th["ink"], th["muted"]
        else:
            tx, anchor, c1, c2 = a - 12, "end", th["ink"], th["muted"]
        body.append(f'<g class="up" {d(550 + i * 200)}>'
                    f'<text class="GB" x="{tx:.1f}" y="{y + 17}" font-size="13.5" fill="{c1}" '
                    f'text-anchor="{anchor}">{esc(title)}</text>'
                    f'<text class="M" x="{tx:.1f}" y="{y + 32}" font-size="10.5" fill="{c2}" opacity=".85" '
                    f'text-anchor="{anchor}">{esc(sub)}  ·  {span}</text></g>')
    css = """
.bar{transform-box:fill-box;transform-origin:left;animation:gr 1s cubic-bezier(.2,.9,.3,1) both}
@keyframes gr{from{transform:scaleX(0)}to{transform:none}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pl 2.2s ease-out 1.5s infinite both}
@keyframes pl{0%{transform:scale(.3);opacity:.7}100%{transform:scale(1.7);opacity:0}}
"""
    return svg(W, H, "".join(body), ["GB", "M"], css, th=th)


def skills(th):
    W = 840
    cols = CV["skills"]
    cw = (W - 64) / len(cols)
    rows = max(len(c[1]) for c in cols)
    H = 84 + rows * 36
    body = [f'<text class="M up" x="32" y="44" font-size="11" fill="{th["muted"]}" letter-spacing="2.5">'
            f'STACK</text>']
    accent = ["blue", "red", "yellow", "blue"]
    n = 0
    for i, (head, items) in enumerate(cols):
        x = 32 + i * cw
        body.append(f'<rect x="{x}" y="62" width="18" height="3" rx="1.5" fill="{th[accent[i % 4]]}"/>'
                    f'<text class="M" x="{x + 26}" y="67" font-size="10.5" fill="{th["ink"]}" '
                    f'letter-spacing="1.5">{esc(head)}</text>')
        for j, it in enumerate(items):
            y = 84 + j * 36
            w = text_width(it, "G", 13) + 24
            body.append(f'<g class="chip" {d(200 + n * 45)}><rect x="{x}" y="{y}" width="{w:.1f}" height="28" '
                        f'rx="14" fill="{mix(th["paper"], th["ink"], .06)}" stroke="{th["line"]}"/>'
                        f'<text class="G" x="{x + 12}" y="{y + 18.5}" font-size="13" fill="{th["ink"]}">'
                        f'{esc(it)}</text></g>')
            n += 1
    css = """
.chip{transform-box:fill-box;transform-origin:left center;animation:cp .5s cubic-bezier(.3,1.5,.5,1) both}
@keyframes cp{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
"""
    return svg(W, H, "".join(body), ["G", "M"], css, th=th)


def button(th, label, sub, color, idx):
    W, H = 272, 76
    bg, fg = th[color], th["on_" + color]
    body = (f'<g class="up" {d(150 + idx * 120)}><rect width="{W}" height="{H}" rx="16" fill="{bg}"/>'
            f'<text class="M" x="20" y="30" font-size="10.5" fill="{fg}" letter-spacing="2" opacity=".85">'
            f'{esc(sub)}</text>'
            f'<text class="S" x="19" y="60" font-size="25" fill="{fg}">{esc(label)}</text>'
            f'<g class="dl"><text class="G" x="{W - 22}" y="50" font-size="26" fill="{fg}" '
            f'text-anchor="end">↓</text></g></g>')
    css = """
.dl{animation:bob 2.4s ease-in-out infinite}
@keyframes bob{0%,70%,100%{transform:none}80%{transform:translateY(4px)}90%{transform:translateY(-1px)}}
"""
    return svg(W, H, body, ["S", "G", "M"], css, bg=bg)


BUTTONS = [  # file, label, sub, color, pdf
    ("btn-fullstack-en", "Full-Stack CV", "PDF · ENGLISH", "blue", "cv-fullstack-developer.pdf"),
    ("btn-fullstack-de", "Lebenslauf", "PDF · DEUTSCH", "red", "cv-fullstack-developer-de.pdf"),
    ("btn-frontend-en", "Frontend CV", "PDF · ENGLISH", "yellow", "cv-frontend-developer.pdf"),
]


def main():
    for theme, th in THEMES.items():
        out = OUT if theme == "light" else OUT / "dark"
        out.mkdir(parents=True, exist_ok=True)
        files = {"header.svg": header(th), "stats.svg": stats(th),
                 "timeline.svg": timeline(th), "skills.svg": skills(th)}
        for i, (f, label, sub, color, _) in enumerate(BUTTONS):
            files[f + ".svg"] = button(th, label, sub, color, i)
        for name, c in files.items():
            (out / name).write_text(c)
        print(f"{theme}: {len(files)} cards")


if __name__ == "__main__":
    main()
