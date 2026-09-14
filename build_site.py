#!/usr/bin/env python3
"""Build the static course site from the three module markdown files.

Usage: python3 build_site.py
Output: site/index.html, site/module-N/index.html, site/whats-next/index.html

The design system comes verbatim from the-code-lead-magnet skill references.
"""
import html
import os
import re
import shutil

import diagrams

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.expanduser("~/.claude/skills/the-code-lead-magnet/references")
OUT = os.path.join(ROOT, "site")
SLUG = "spec-driven-development"
COURSE_TITLE = "How Engineers at Anthropic and OpenAI Run Spec-Driven Development"
COURSE_PROMISE = ("Comprehensive guide for you to learn fundamentals of spec driven development, followed by "
                  "lessons to help you write good specs and run SDD end to end.")
COURSE_DESC = ("A curated guide to spec-driven development for engineering teams: what a spec is, "
               "how to write one agents cannot misread, and how to run SDD end to end with GitHub Spec Kit.")

MODULES = [
    ("module-1-fundamentals.md", "Fundamentals Of Spec-Driven Development", "Fundamentals"),
    ("module-2-how-to-write-a-good-spec.md", "How To Write A Good Spec", "How To Write A Good Spec"),
    ("module-3-how-to-run-sdd-end-to-end.md", "How To Run SDD End To End", "How To Run SDD End To End"),
]

# Where each quoted person's words come from, for the .srcq source line.
QUOTE_SOURCES = {
    "Sadasivuni": ("Engineering the Frontier Firm", "https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/"),
    "Verma": ("Engineering the Frontier Firm", "https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/"),
    "Gupta": ("Engineering the Frontier Firm", "https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/"),
    "Kumar": ("Engineering the Frontier Firm", "https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/"),
    "Böckeler": ("Understanding Spec-Driven-Development", "https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html"),
}

# ----------------------------------------------------------------- helpers

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def css_blocks():
    ds = read(os.path.join(SKILL, "design-system.css"))
    ds = re.sub(r"^<!--.*?-->\s*", "", ds, flags=re.S)
    parts = re.split(r"(?=/\* =+\n\s+\d of 4)", ds)
    parts = [p.strip() for p in parts if p.strip()]
    assert len(parts) == 4, len(parts)
    cl = read(os.path.join(SKILL, "course-layer.css"))
    five, six = cl.split("/* ---------- <style> 6 of 6 (only when .tryit is used) ---------- */")
    five = five.split("/* ---------- <style> 5 of 6 ---------- */")[1].strip()
    six = six.strip()
    return parts + [five, six]


PAGE_CSS = """/* ============================================================
   7 of 7 — spec-driven-development additions
   ============================================================ */
/* Tables use the full content column, not the prose measure. */
.section > .tablewrap { max-width: none; }
.section h3 { font: 600 18px / 1.35 var(--sans); letter-spacing: -.005em; margin: var(--s-8) 0 var(--s-3); max-width: var(--measure); text-wrap: balance; }
.section ol { max-width: var(--measure); margin-bottom: var(--s-5); }
.section > .placeholder { margin-block: var(--s-8); }
.placeholder { border: 1px dashed var(--wash-line); background: var(--wash); padding: var(--s-4) var(--s-5); max-width: var(--measure); }
.placeholder__k { font: 600 var(--t-1) / 1 var(--mono); letter-spacing: .18em; color: var(--accent-ink-on-wash); }
.placeholder p { margin: var(--s-2) 0 0; color: var(--ink-2); font-size: 14px; }
.tryit__k b { color: var(--ink); letter-spacing: 0; text-transform: none; font-weight: 600; }
.tryit ol, .tryit ul { max-width: none; }
.tryit .codeblock { margin-bottom: var(--s-4); }
.codeblock--wrap pre { white-space: pre-wrap; overflow-wrap: anywhere; padding-right: 84px; }
.srcq figcaption b { font-weight: 600; }
.landing .landing__sub + .landing__sub { margin-top: var(--s-3); }
.section > .do { max-width: var(--measure); }
.section > .card { max-width: var(--measure); }
.tryit .card { background: var(--surface); border-color: var(--wash-line); padding: var(--s-4) var(--s-5); margin-top: var(--s-3); }
.score__group { font: 600 var(--t-1) / 1 var(--mono); letter-spacing: .18em; text-transform: uppercase; color: var(--ink-3); padding: var(--s-1) var(--s-1) var(--s-2); }
.score__text { display: grid; grid-template-columns: 1.6em minmax(0, 1fr); column-gap: var(--s-3); align-items: baseline; }
.score__n { font: 500 var(--t-2) / 1.5 var(--mono); color: var(--accent-ink); font-variant-numeric: tabular-nums; }
.score__text .score__fix { grid-column: 2; }
.score__item[aria-pressed="true"] .score__n { color: var(--ink-3); }
.score__note { margin: var(--s-4) var(--s-1) 0; font-size: 14px; color: var(--ink-2); max-width: none; }
.section > .pairs { margin-block: var(--s-8); max-width: var(--measure); }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: var(--s-3); margin-bottom: var(--s-3); }
.pair__side { padding: var(--s-4) var(--s-5); border: 1px solid var(--border); background: var(--surface); }
.pair__side--after { background: var(--wash); border-color: var(--wash-line); }
.pair__k { display: block; font: 600 var(--t-1) / 1 var(--mono); letter-spacing: .18em; color: var(--ink-3); margin-bottom: var(--s-3); }
.pair__side--after .pair__k { color: var(--accent-ink-on-wash); }
.pair__side p { margin: 0; font: 500 var(--t-2) / 1.6 var(--mono); color: var(--ink-2); max-width: none; }
.pair__side--after p { color: var(--ink); }
@media (max-width: 640px) { .pair { grid-template-columns: 1fr; } }
.section > .walk { margin-block: var(--s-8); max-width: none; }
.walk { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: var(--s-4); align-items: start; }
.walk__spec { background: var(--surface); border: 1px solid var(--border); height: 560px; overflow-y: auto; overscroll-behavior: contain; padding: var(--s-4) var(--s-5); scroll-behavior: smooth; }
.walk__spec:focus-visible { outline: 2px solid var(--accent-ink); outline-offset: -2px; }
.walk__doc { font-size: 13.5px; line-height: 1.55; color: #7A7A7A; }
.walk__doc h4, .walk__doc h5, .walk__doc h6 { font-family: var(--sans); color: #6A6A6A; margin: 0; }
.walk__doc code { color: inherit; border-color: var(--hairline); }
.walk__doc strong { color: inherit; }
.walk__blk.is-on, .walk__blk.is-on strong { color: var(--ink); }
.walk__blk.is-on code { color: var(--ink); border-color: var(--border); }
.walk__doc h4 { font-size: 16px; font-weight: 600; }
.walk__doc h5 { font-size: 14px; font-weight: 600; }
.walk__doc h6 { font-size: 13.5px; font-weight: 600; }
.walk__doc p { margin: 0; max-width: none; }
.walk__doc ul, .walk__doc ol { margin: 0; max-width: none; padding-left: 1.2em; }
.walk__doc li { margin: 2px 0; }
.walk__doc code { font-size: .85em; }
.walk__doc table { min-width: 0; font-size: 12.5px; }
.walk__doc th, .walk__doc td { padding: 6px 10px; }
.walk__blk { padding: 6px 10px; margin: 0 -10px; border-left: 2px solid transparent; cursor: pointer; transition: background var(--dur-1) var(--ease), border-color var(--dur-1) var(--ease); }
.walk__blk--plain { cursor: default; }
.walk__blk.is-on { background: var(--wash); border-left-color: var(--primary); color: var(--ink); }
.walk__blk.is-on h4, .walk__blk.is-on h5, .walk__blk.is-on h6 { color: var(--accent-ink-on-wash); }
.walk__credit { margin: var(--s-5) 0 0; font: 500 var(--t-1) / 1.5 var(--mono); color: var(--ink-3); max-width: none; }
.walk__notes { position: sticky; top: 90px; background: var(--wash); border: 1px solid var(--wash-line); padding: var(--s-5); }
.walk__bar { display: flex; align-items: center; justify-content: space-between; gap: var(--s-2); margin-bottom: var(--s-5); }
.walk__bar .btn { flex: 1 1 0; justify-content: center; }
.walk__dots { display: flex; gap: 4px; list-style: none; margin: 0; padding: 0; flex-wrap: wrap; }
.walk__dots li { margin: 0; }
.walk__dots button { width: 24px; height: 24px; border: 1px solid var(--wash-line); background: var(--surface); color: var(--ink-3); font: 600 11px / 1 var(--mono); cursor: pointer; }
.walk__dots button.is-on { background: var(--primary); border-color: var(--primary); color: var(--on-primary); }
.walk__k { font: 600 var(--t-1) / 1 var(--mono); letter-spacing: .18em; color: var(--accent-ink-on-wash); }
.walk__loc { margin: var(--s-2) 0 0; font: 500 var(--t-2) / 1.5 var(--mono); color: var(--ink-3); max-width: none; }
.walk__note h4 { font: 600 17px / 1.3 var(--sans); margin: var(--s-3) 0 var(--s-3); color: var(--ink); text-wrap: balance; }
.walk__tag { display: inline-block; margin-top: var(--s-2); padding: 5px 9px; border: 1px solid var(--wash-line); background: var(--surface); font: 600 var(--t-1) / 1 var(--mono); letter-spacing: .04em; color: var(--accent-ink-on-wash); }
.walk__tag:hover { border-color: var(--accent-ink); text-decoration: none; }
.walk__note p { margin: 0 0 var(--s-3); max-width: none; font-size: 14.5px; color: var(--ink-2); }
.walk__note p:last-child { margin-bottom: 0; }
@media (max-width: 479px) { .walk__dots { display: none; } }
@media (max-width: 899px) {
  .walk { grid-template-columns: 1fr; }
  .walk__spec { height: 340px; order: 2; }
  .walk__notes { position: static; order: 1; }
}
""" + diagrams.css() + "\n"

LOGO = None


def logo_svg():
    global LOGO
    if LOGO is None:
        sh = read(os.path.join(SKILL, "shell.html"))
        m = re.search(r'<svg class="brand__logo".*?</svg>', sh, re.S)
        LOGO = m.group(0)
    return LOGO


def curly(s):
    # straight quotes to typographic quotes in prose (never called on code)
    s = re.sub(r'(^|[\s(\[—>])"', lambda m: m.group(1) + "“", s)
    s = s.replace('"', "”")
    s = re.sub(r"(^|[\s(\[])'", lambda m: m.group(1) + "‘", s)
    s = s.replace("'", "’")
    return s


def map_href(href, depth):
    """Rewrite markdown cross-links to site links. depth: '' on landing, '../' on subpages."""
    m = re.match(r"^(module-(\d)-[^#]*\.md)?#(\d)(\d)-", href)
    if m:
        return ("../module-%s/" % m.group(2) if m.group(1) else "") + "#lesson-%s-%s" % (m.group(3), m.group(4))
    if href.startswith("#"):
        return href  # h3 anchor in same page
    if href.startswith("module-"):
        return href
    return None


def inline(text, depth="../"):
    """Inline markdown to HTML: code spans, links, bold, quotes."""
    out = []
    # bold first, so a bold span that contains a code span still pairs up
    text = re.sub(r"\*\*(.+?)\*\*", "\x02\\1\x03", text)
    parts = re.split(r"(`[^`]*`)", text)
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append("<code>" + html.escape(part[1:-1]) + "</code>")
            continue
        seg = html.escape(part, quote=False)
        seg = curly(seg)

        def link(m):
            label, href = m.group(1), m.group(2)
            internal = map_href(href, depth)
            if internal is not None:
                return '<a href="%s">%s</a>' % (internal, label)
            return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (href, label)
        seg = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, seg)
        out.append(seg)
    return "".join(out).replace("\x02", "<strong>").replace("\x03", "</strong>")


def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s]+", "-", s).strip("-")


def code_name(lang, body):
    b = body.lstrip()
    if lang == "bash":
        return "terminal"
    tests = [
        ("# Spec:", "spec.md"), ("# Project Spec", "spec.md"), ("## Boundaries", "rules file"),
        ("# [Title", "spec outline"), ("Scenario:", "scenario"), ("Instead of:", "test plan"),
        ("Must pass", "success criteria"), ("Does not work", "prompt"), ("1. Pilot", "playbook"),
        ("1. Make the", "takeaways"), ("1. Spike", "checklist"),
    ]
    for pre, name in tests:
        if b.startswith(pre):
            return name
    return "prompt"


def scorelist(body, key, prompt):
    """A numbered checklist code block -> tappable score list. Indented lines become the item's note."""
    items, tail, after_blank = [], [], False
    for ln in body.split("\n"):
        m = re.match(r"^(\d+)\. (.*)$", ln)
        if m:
            items.append([m.group(2).strip(), ""]); after_blank = False
        elif not ln.strip():
            after_blank = bool(items)
        elif after_blank:
            tail.append(ln.strip())
        elif items:
            items[-1][1] = (items[-1][1] + " " + ln.strip()).strip()
    out = ['<div class="card">', '  <div class="score" data-key="%s">' % key]
    for i, (t, note) in enumerate(items, 1):
        fix = '<span class="score__fix">%s</span>' % html.escape(note) if note else ""
        out.append('    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span>'
                   '<span class="score__text"><span class="score__n">%d</span>%s%s</span></button>' % (i, html.escape(t), fix))
    if tail:
        out.append('    <p class="score__note">%s</p>' % html.escape(" ".join(tail)))
    out.append('    <div class="score__result"><div class="score__num">0 / %d</div><p class="score__verdict">%s</p>'
               '<button class="btn btn--ghost btn--sm score__reset" type="button">Reset</button></div>' % (len(items), prompt))
    out.append('    <p class="visually-hidden score__live" role="status" aria-live="polite"></p>\n  </div>\n</div>')
    return "\n".join(out)


def pairs(body):
    """'Instead of:/Write:' or 'Does not work:/Works:' blocks -> side-by-side before/after cards. None if not a pair block."""
    if body.lstrip().startswith("Instead of:"):
        labels = ("INSTEAD OF", "WRITE")
        chunks = re.findall(r"Instead of:\s*(.*?)\nWrite:\s*(.*?)(?=\n\s*\n|\Z)", body, re.S)
        rows = [(re.sub(r"\s+", " ", a).strip(), re.sub(r"\s+", " ", w).strip()) for a, w in chunks]
    elif body.lstrip().startswith("Does not work:"):
        labels = ("DOES NOT WORK", "WORKS")
        m = re.match(r"Does not work:\s*(.*?)\n\s*\nWorks:\s*(.*)", body.strip(), re.S)
        rows = [(re.sub(r"\s+", " ", m.group(1)).strip(), re.sub(r"\s+", " ", m.group(2)).strip())]
    else:
        return None
    out = ['<div class="pairs">']
    for before, after in rows:
        out.append('  <div class="pair">\n    <div class="pair__side pair__side--before"><span class="pair__k">%s</span><p>%s</p></div>\n'
                   '    <div class="pair__side pair__side--after"><span class="pair__k">%s</span><p>%s</p></div>\n  </div>'
                   % (labels[0], html.escape(before), labels[1], html.escape(after)))
    out.append('</div>')
    return "\n".join(out)


def codeblock(lang, body):
    p = pairs(body)
    if p:
        return p
    name = code_name(lang, body)
    if name == "checklist":
        return scorelist(body, "spec-driven-development.module-3.spike-first",
                         "Tick each step as you finish it on one feature. This browser remembers your ticks.")
    if name == "playbook":
        return scorelist(body, "spec-driven-development.module-3.playbook",
                         "Tick each step as your pilot reaches it. This browser remembers your ticks.")
    wrap = " codeblock--wrap"  # copy text wraps inside the box instead of scrolling sideways
    return ('<div class="codeblock%s">\n  <span class="codeblock__name">%s</span>\n'
            '  <button class="codeblock__copy" type="button" data-copy="">Copy</button>\n'
            '<pre><code>%s</code></pre>\n</div>' % (wrap, name, html.escape(body.rstrip("\n"))))


def placeholder(text):
    m = re.match(r"\[(Infographic|Checklist candidate|Video):\s*(.*)\]$", text.strip("` "))
    kind, body = m.group(1), m.group(2)
    if kind == "Video":
        # "Channel, "Title", N min: URL"
        vm = re.match(r'(.*?),\s*[“"](.*?)[”"]([^,]*),?\s*(\d+ min):\s*(\S+)$', body)
        chan, title, extra, mins, url = vm.groups()
        if extra.strip():
            chan = chan + extra
        vid = re.search(r"v=([\w-]+)", url).group(1)
        return ('<figure class="video">\n  <div class="video__frame">\n'
                '    <iframe src="https://www.youtube-nocookie.com/embed/%s" title="%s" loading="lazy" '
                'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n  </div>\n'
                '  <figcaption>Watch: <a href="%s" target="_blank" rel="noopener noreferrer">%s</a> (%s, %s).</figcaption>\n</figure>'
                % (vid, html.escape(title), url, html.escape(title), html.escape(chan), mins))
    if kind == "Infographic":
        d = diagrams.render(body)
        if d:
            return d[1]
    if kind == "Checklist candidate":
        return diagrams.CHECKLIST
    label = "INFOGRAPHIC · PLANNED" if kind == "Infographic" else "CHECKLIST · PLANNED"
    return '<div class="placeholder"><span class="placeholder__k">%s</span><p>%s</p></div>' % (label, html.escape(body))


def srcq(para):
    """A paragraph that is a quote with 'says Name, Role' attribution -> .srcq figure. Else None."""
    if not para.startswith('"'):
        return None
    m = re.search(r'"\s*(?:says|writes)\s+([^.]+?)\.|," (\w+) says\.|," she writes\.', para)
    if not m:
        return None
    quotes = re.findall(r'"([^"]+)"', para)
    parts = [q.strip().rstrip(",") for q in quotes]
    for i in range(len(parts) - 1):
        # A fragment split by attribution: close the sentence if the next one starts a new sentence.
        if parts[i] and parts[i][-1] not in ".!?:;" and parts[i + 1][:1].isupper():
            parts[i] += "."
    if parts and parts[-1][-1:] not in ".!?":
        parts[-1] += "."
    quote = " ".join(parts)
    who = m.group(1) or m.group(2) or "Birgitta Böckeler"
    FULL = {"Gupta": "Apoorv Gupta, Principal Software Engineer at Microsoft Digital",
            "Verma": "Mridul Verma, Senior Software Engineer at Microsoft Digital",
            "Birgitta B\u00f6ckeler": "Birgitta B\u00f6ckeler, Distinguished Engineer at Thoughtworks"}
    who = FULL.get(who, who)
    surname = [k for k in QUOTE_SOURCES if k in who]
    src = QUOTE_SOURCES[surname[0]] if surname else None
    cap = "<b>%s</b>" % html.escape(who)
    if src:
        cap += '. Source: <a href="%s" target="_blank" rel="noopener noreferrer">%s</a>.' % (src[1], html.escape(src[0]))
    return ('<figure class="srcq">\n  <blockquote>“%s”</blockquote>\n  <figcaption>%s</figcaption>\n</figure>'
            % (html.escape(quote, quote=False).replace("'", "’"), cap))


# ----------------------------------------------------------------- markdown -> blocks

def parse_blocks(md):
    """Yield (kind, payload) blocks from module markdown."""
    lines = md.split("\n")
    i, n = 0, len(lines)
    blocks = []
    while i < n:
        ln = lines[i]
        if ln.startswith("```"):
            lang = ln[3:].strip()
            j = i + 1
            body = []
            while j < n and not lines[j].startswith("```"):
                body.append(lines[j]); j += 1
            blocks.append(("code", (lang, "\n".join(body))))
            i = j + 1; continue
        if ln.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            blocks.append(("table", rows)); continue
        if ln.startswith("#"):
            level = len(ln) - len(ln.lstrip("#"))
            blocks.append(("h%d" % level, ln.lstrip("#").strip())); i += 1; continue
        if ln.startswith("`["):
            blocks.append(("placeholder", ln)); i += 1; continue
        if ln.strip() == "---":
            i += 1; continue
        if re.match(r"^(\d+)\. ", ln):
            items = []
            while i < n and re.match(r"^(\d+)\. ", lines[i]):
                num = int(re.match(r"^(\d+)\.", lines[i]).group(1))
                items.append((num, re.sub(r"^\d+\. ", "", lines[i]))); i += 1
            blocks.append(("ol", items)); continue
        if ln.startswith("- "):
            items = []
            while i < n and lines[i].startswith("- "):
                items.append(lines[i][2:]); i += 1
            blocks.append(("ul", items)); continue
        if ln.strip() == "":
            i += 1; continue
        para = []
        while i < n and lines[i].strip() != "" and not lines[i].startswith(("```", "|", "#", "- ", "`[")) and not re.match(r"^\d+\. ", lines[i]):
            para.append(lines[i]); i += 1
        blocks.append(("p", " ".join(para)))
    return blocks


def render_table(rows):
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows if not re.match(r"^\|[-| ]+\|$", r)]
    head, body = cells[0], cells[1:]
    h = "<thead><tr>" + "".join("<th>%s</th>" % inline(c) for c in head) + "</tr></thead>"
    b = "<tbody>" + "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>" for r in body) + "</tbody>"
    return '<div class="tablewrap">\n<table>\n%s\n%s\n</table>\n</div>' % (h, b)


def render_ol(items):
    """Contiguous numbered items become one <ol start=n>."""
    return '<ol start="%d">\n%s\n</ol>' % (items[0][0], "\n".join("  <li>%s</li>" % inline(t) for _, t in items))


def render_block(kind, payload):
    if kind == "p":
        q = srcq(payload)
        return q if q else "<p>%s</p>" % inline(payload)
    if kind == "ul":
        return "<ul>\n%s\n</ul>" % "\n".join("  <li>%s</li>" % inline(t) for t in payload)
    if kind == "ol":
        return render_ol(payload)
    if kind == "code":
        return codeblock(*payload)
    if kind == "table":
        return render_table(payload)
    if kind == "placeholder":
        return placeholder(payload)
    if kind == "h3":
        return '<h3 id="%s">%s</h3>' % (slug(payload), inline(payload))
    raise ValueError(kind)


def render_tryit(title, blocks):
    """Hands-on h3 section -> .tryit panel."""
    out = ['<div class="tryit">', '  <div class="tryit__k">HANDS-ON · <b>%s</b></div>' % inline(title)]
    for kind, payload in blocks:
        if kind == "p":
            m = re.match(r"^(Goal|Steps|Expected result):\s*(.*)$", payload)
            if m:
                out.append('  <p><span class="tryit__label">%s:</span> %s</p>' % (m.group(1), inline(m.group(2))))
                continue
        out.append("  " + render_block(kind, payload))
    out.append("</div>")
    return "\n".join(out)


# ----------------------------------------------------------------- page assembly

def parse_module(md):
    blocks = parse_blocks(md)
    title = blocks[0][1]
    dek = blocks[1][1]
    lessons = []
    cur = None
    for kind, payload in blocks[2:]:
        if kind == "ul" and cur is None:
            continue  # the module index
        if kind == "h2":
            num, t = payload.split(" ", 1)
            cur = {"num": num, "title": t, "blocks": []}
            lessons.append(cur); continue
        cur["blocks"].append((kind, payload))
    # split the recap off the last lesson
    last = lessons[-1]["blocks"]
    idx = next(i for i, (k, p) in enumerate(last) if k == "p" and p.startswith("By this point you should have"))
    recap_items = last[idx + 1][1]
    outro = [p for k, p in last[idx + 2:] if k == "p"]
    lessons[-1]["blocks"] = last[:idx]
    return title, dek, lessons, recap_items, outro


STEP_RULES = [  # (heading text that starts a region, step number); 0 = not annotated
    ("Motivation", 2), ("Architecture", 3), ("WebSocket Protocol", 3), ("HTTP Server", 3),
    ("Configuration", 5), ("Startup Sequence", 5), ("Application-Level WebSocket Messages", 3),
    ("File Watching", 3), ("Error Handling", 6), ("What Changes", 7), ("What Stays the Same", 7),
    ("Platform Compatibility", 8), ("Testing", 9),
]


STEP_LOCS = {1: "Title", 2: "Motivation", 3: "Architecture", 4: "Deliberately skipped", 5: "Configuration and Startup Sequence",
             6: "Error Handling", 7: "What Changes and What Stays the Same", 8: "Platform Compatibility", 9: "Testing"}
RULE_LINKS = [("Problem statement", "#lesson-2-2"), ("PRD side", "#lesson-2-2"), ("Assumptions", "#lesson-2-2"),
              ("Non-goals", "#lesson-2-2"), ("Obvious to you", "#lesson-2-2"), ("Measurable tests", "#lesson-2-4"),
              ("Boundaries", "#lesson-2-3"), ("Domain knowledge", "#lesson-2-3"), ("Test plan", "#lesson-2-4")]


def render_walk(spec_path, notes, tags):
    """The annotated-spec stepper: the whole spec on the left, one note per step on the right."""
    blocks = parse_blocks(read(os.path.join(ROOT, spec_path)))
    step = 1
    doc = []
    for kind, payload in blocks:
        if kind in ("h1", "h2", "h3"):
            for head, n in STEP_RULES:
                if kind != "h1" and payload.strip() == head:
                    step = n
            tag = {"h1": "h4", "h2": "h5", "h3": "h6"}[kind]
            inner = "<%s>%s</%s>" % (tag, inline(payload), tag)
        else:
            inner = render_block(kind, payload)
        this = 4 if kind == "p" and payload.startswith("**Deliberately skipped:**") else step
        doc.append('<div class="walk__blk%s" data-step="%d">%s</div>' % ("" if this else " walk__blk--plain", this, inner))
    out = ['<div class="walk" id="walk-2-5">',
           '  <div class="walk__spec" tabindex="0" aria-label="The spec, with the current section highlighted">',
           '    <div class="walk__doc">', "\n".join(doc), '    </div>',
           '    <p class="walk__credit">Zero-Dependency Brainstorm Server, by <a href="https://github.com/obra/superpowers/blob/main/docs/superpowers/specs/2026-03-11-zero-dep-brainstorm-server-design.md" target="_blank" rel="noopener noreferrer">Jesse Vincent</a>, MIT license. Shown in full.</p>',
           '  </div>',
           '  <div class="walk__notes">',
           '    <div class="walk__bar">',
           '      <button class="btn btn--ghost btn--sm walk__prev" type="button" aria-label="Previous section">&larr; Prev</button>',
           '      <button class="btn btn--primary btn--sm walk__next" type="button" aria-label="Next section">Next &rarr;</button>',
           '    </div>']
    for i, (title, paras) in enumerate(notes, 1):
        tag_html = ""
        out.append('    <div class="walk__note" data-step="%d"%s><span class="walk__k">SECTION %d OF %d</span>'
                   '<h4>%s</h4>%s%s</div>'
                   % (i, "" if i == 1 else " hidden", i, len(notes), STEP_LOCS.get(i, inline(title)),
                      "".join("<p>%s</p>" % inline(t) for t in paras), tag_html))
    out.append('  </div>\n</div>')
    return "\n".join(out)


def render_lesson(lesson):
    out = ['<section class="section" id="lesson-%s">' % lesson["num"].replace(".", "-"),
           '  <span class="lesson__num">%s</span>' % lesson["num"],
           "  <h2>%s</h2>" % inline(lesson["title"])]
    blocks = lesson["blocks"]
    # a sub-heading directly under the lesson title adds nothing; drop it
    if blocks and blocks[0][0] == "h3" and not blocks[0][1].startswith("Hands-On:"):
        blocks = blocks[1:]
    i = 0
    while i < len(blocks):
        kind, payload = blocks[i]
        if kind == "placeholder" and payload.startswith("`[Stepper:"):
            spec_path = re.match(r"`\[Stepper:\s*(.*?)\]`", payload).group(1)
            j = i + 1
            notes = []
            while j < len(blocks) and not (blocks[j][0] == "h3" and blocks[j][1].startswith("The Spec")):
                if blocks[j][0] == "h3":
                    notes.append((blocks[j][1], []))
                elif blocks[j][0] == "p" and notes:
                    notes[-1][1].append(blocks[j][1])
                j += 1
            # the mapping table that follows the notes supplies each note's rule tag
            k = j
            while k < len(blocks) and blocks[k][0] != "table":
                k += 1
            tags = []
            if k < len(blocks):
                rows = [[c.strip() for c in r.strip("|").split("|")] for r in blocks[k][1] if not re.match(r"^\|[-| ]+\|$", r)]
                tags = [r[2] for r in rows[1:]]
            out.append(render_walk(spec_path, notes, tags))
            i = j; continue
        if kind == "h3" and payload.startswith("Hands-On:"):
            j = i + 1
            while j < len(blocks) and blocks[j][0] != "h3":
                j += 1
            # everything up to the next h3 belongs to the hands-on, except a trailing
            # transition paragraph that mentions "next lesson" and any video after it
            inner = blocks[i + 1:j]
            tail = []
            while inner and ((inner[-1][0] == "p" and ("next lesson" in inner[-1][1] or "closing line" in inner[-1][1] or "one team" in inner[-1][1] or "learned what to adopt" in inner[-1][1])) or inner[-1][0] == "placeholder"):
                tail.insert(0, inner.pop())
            out.append(render_tryit(payload[len("Hands-On:"):].strip(), inner))
            for k, p in tail:
                out.append(render_block(k, p))
            i = j; continue
        out.append(render_block(kind, payload))
        i += 1
    out.append("</section>")
    return "\n".join(out)


def band(page):
    return ('<div class="band">\n  <div>\n    <h3>The Code: Your daily unfair advantage in software engineering.</h3>\n'
            '    <p>Join 350,000+ software engineers, tech leads, and CTOs who start their morning with The Code.</p>\n  </div>\n'
            '  <a class="btn btn--primary" href="https://codenewsletter.ai/subscribe?source=leadmagnets&amp;utm_medium=%s-%s" '
            'target="_blank" rel="noopener noreferrer">Subscribe to Newsletter</a>\n</div>' % (SLUG, page))


def rail(all_modules, current, depth):
    """current: 'landing' | 'module-N' | 'whats-next'."""
    def href(target):
        return depth + target
    out = ['<nav class="rail" id="rail-sheet" aria-label="Course contents">',
           '  <div class="rail__sheetbar"><span class="rail__sheettitle">Contents</span><button class="rail__done" type="button">Done</button></div>',
           '  <ol class="rail__course">']
    cur = " is-current" if current == "landing" else ""
    out.append('    <li class="rail__group%s"><a class="rail__ghead" href="%s"%s><span class="rail__gt">Start Here</span></a></li>'
               % (cur, "#top" if cur else href(""), ' aria-current="page"' if cur else ""))
    for n, (short, lessons) in enumerate(all_modules, 1):
        mid = "module-%d" % n
        is_cur = current == mid
        out.append('    <li class="rail__group%s">' % (" is-current" if is_cur else ""))
        out.append('      <a class="rail__ghead" href="%s"%s><span class="rail__gt">Module %d: %s</span></a>'
                   % ("#top" if is_cur else href(mid + "/"), ' aria-current="page"' if is_cur else "", n, inline(short)))
        out.append('      <ol class="rail__lessons"%s>' % (' id="rail-list"' if is_cur else ""))
        for num, t in lessons:
            anchor = "#lesson-" + num.replace(".", "-")
            out.append('        <li><a href="%s"><span class="rail__ln">%s</span>%s</a></li>'
                       % (anchor if is_cur else href(mid + "/" + anchor), num, inline(t)))
        out.append("      </ol>\n    </li>")
    cur = " is-current" if current == "whats-next" else ""
    out.append('    <li class="rail__group%s"><a class="rail__ghead" href="%s"%s><span class="rail__gt">What’s Next</span></a></li>'
               % (cur, "#top" if cur else href("whats-next/"), ' aria-current="page"' if cur else ""))
    out.append("  </ol>\n</nav>")
    out.append('<button class="sheetbtn" id="sheetbtn" type="button" aria-expanded="false" aria-controls="rail-sheet">'
               '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg>Contents</button>')
    out.append('<div class="sheet-scrim" id="sheet-scrim"></div>')
    out.append('<div class="figview" id="figview" hidden><button class="figview__close" type="button">Close</button><div class="figview__scroll"><div class="figview__inner"></div></div></div>')
    return "\n".join(out)


def page(title, desc, canonical, page_key, rail_html, main_html):
    styles = "\n\n".join("<style>\n%s\n</style>" % c for c in css_blocks() + [PAGE_CSS])
    js = read(os.path.join(SKILL, "course-behaviors.js"))
    sub = 'https://codenewsletter.ai/subscribe?source=leadmagnets&amp;utm_medium=%s-%s' % (SLUG, page_key)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} &#8212; The Code</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)} &#8212; The Code">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:site_name" content="The Code">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F9F9F9">
<link rel="icon" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgcm9sZT0iaW1nIiBhcmlhLWxhYmVsPSJUaGUgQ29kZSI+CiAgPHJlY3Qgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjMjg4Q0ZGIi8+CiAgPHJlY3QgeD0iMy42IiB5PSIzLjYiIHdpZHRoPSIxNi44IiBoZWlnaHQ9IjE2LjgiIGZpbGw9IiNGRkZGRkYiLz4KICA8cGF0aCBkPSJNOC4yIDYuNEwxNy43IDEyLjNMMTMuMiAxMy41TDE1LjUgMTcuOUwxMy4zIDE4LjlMMTEgMTQuNkw4LjIgMTcuNFoiIGZpbGw9IiMyODhDRkYiLz4KPC9zdmc+Cg==" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Eczar:wght@500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap">

{styles}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="topbar">
  <div class="wrap topbar__inner">
    <a class="brand" href="#top" aria-label="The Code, top of page">{logo_svg()}</a>
    <a class="btn btn--primary" href="{sub}" target="_blank" rel="noopener noreferrer">Subscribe to Newsletter</a>
  </div>
  <div class="progress" id="progress" role="presentation"></div>
</header>

<div class="wrap layout" id="top">

{rail_html}

  <main id="main">
{main_html}
  </main>
</div>

<footer class="site-footer">
  <div class="wrap foot">
    <div>
      <span class="brand brand--sm">{logo_svg()}</span>
      <p class="dim" style="margin-top:var(--s-3);font-size:14px;max-width:34ch">Curated briefings for engineering leaders building with AI.</p>
    </div>
    <a class="btn btn--primary" href="{sub}" target="_blank" rel="noopener noreferrer">Subscribe to Newsletter</a>
  </div>
</footer>

<script>
{js}
</script>
<script>
/* Tappable checklists: any .score[data-key] is its own list with its own localStorage key. */
(function () {{
  'use strict';
  var VERDICTS = {{
    'spec-driven-development.module-3.spike-first': function (n, total) {{
      if (n === total) return 'One feature is through the whole workflow: a commented reference, a spec with a test plan, a much longer plan, and code from a small model.';
      if (n >= 5) return 'The plan is reviewed. If it made a new architectural call, fix the spec before the last step.';
      if (n >= 3) return 'The spec exists. Write the test plan before the implementation plan, not after.';
      if (n >= 1) return 'Started. Stop the spike when you have an answer, not when the code is pretty.';
      return 'Nothing ticked yet. Spike the risky parts first.';
    }},
    'spec-driven-development.module-3.playbook': function (n, total) {{
      if (n === total) return 'The pilot ran the whole loop. Decide where to expand next, and only where it adds clear value.';
      if (n >= 2) return 'A lightweight spec exists. Let AI generate the artifacts from it, then review them against the spec.';
      if (n >= 1) return 'A pilot is chosen. Keep the spec lightweight: scenarios, constraints, acceptance criteria.';
      return 'Nothing ticked yet. Pick one feature where alignment problems are visible.';
    }},
    'spec-driven-development.module-3.pre-handoff': function (n, total) {{
      if (n === total) return 'All six covered. Hand the spec to the agent, and run the self-verification prompt below when it is done.';
      if (n >= 4) return 'Nearly there. The missing items are the ones that derail well-intentioned workflows.';
      if (n >= 1) return 'Started. The first two are where most specs fall short.';
      return 'Nothing ticked yet. Start with the prompt itself.';
    }}
  }};
  document.querySelectorAll('.score[data-key]').forEach(function (card) {{
    var KEY = 'the-code.' + card.getAttribute('data-key') + '.v1';
    var items = Array.prototype.slice.call(card.querySelectorAll('.score__item'));
    var num = card.querySelector('.score__num');
    var verdict = card.querySelector('.score__verdict');
    var live = card.querySelector('.score__live');
    var reset = card.querySelector('.score__reset');
    var verdictFor = VERDICTS[card.getAttribute('data-key')] || function (n, t) {{ return n + ' of ' + t + ' done.'; }};
    var read = function () {{ try {{ var raw = localStorage.getItem(KEY); return raw ? JSON.parse(raw) : []; }} catch (e) {{ return []; }} }};
    var write = function (state) {{ try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{ /* private mode */ }} }};
    var isOn = function (b) {{ return b.getAttribute('aria-pressed') === 'true'; }};
    var touched = false;
    var PROMPT = verdict.textContent;
    var render = function (announce) {{
      var n = items.filter(isOn).length;
      num.textContent = n + ' / ' + items.length;
      verdict.textContent = (!touched && n === 0) ? PROMPT : verdictFor(n, items.length, items);
      if (announce && live) live.textContent = n + ' of ' + items.length + '. ' + verdict.textContent;
    }};
    var saved = read();
    if (saved.length) touched = true;
    items.forEach(function (btn, i) {{
      if (saved.indexOf(i) !== -1) btn.setAttribute('aria-pressed', 'true');
      btn.addEventListener('click', function () {{
        btn.setAttribute('aria-pressed', isOn(btn) ? 'false' : 'true');
        touched = true;
        write(items.reduce(function (acc, b, j) {{ if (isOn(b)) acc.push(j); return acc; }}, []));
        render(true);
      }});
    }});
    if (reset) reset.addEventListener('click', function () {{
      items.forEach(function (b) {{ b.setAttribute('aria-pressed', 'false'); }});
      write([]); touched = false; render(true);
    }});
    render(false);
  }});
}})();
</script>
<script>
/* Annotated-spec stepper: highlight the current section in the spec pane, show its note. */
(function () {{
  'use strict';
  document.querySelectorAll('.walk').forEach(function (walk) {{
    var pane = walk.querySelector('.walk__spec');
    var blks = Array.prototype.slice.call(walk.querySelectorAll('.walk__blk'));
    var notes = Array.prototype.slice.call(walk.querySelectorAll('.walk__note'));
    var dots = Array.prototype.slice.call(walk.querySelectorAll('.walk__dots button'));
    var prev = walk.querySelector('.walk__prev'), next = walk.querySelector('.walk__next');
    var total = notes.length, cur = 1;
    var show = function (n, scroll) {{
      cur = Math.max(1, Math.min(total, n));
      var first = null;
      blks.forEach(function (b) {{
        var on = b.getAttribute('data-step') === String(cur);
        b.classList.toggle('is-on', on);
        if (on && !first) first = b;
      }});
      notes.forEach(function (x) {{ x.hidden = x.getAttribute('data-step') !== String(cur); }});
      dots.forEach(function (d) {{ d.classList.toggle('is-on', d.getAttribute('data-goto') === String(cur)); }});
      prev.disabled = cur === 1; next.disabled = cur === total;
      if (scroll && first) pane.scrollTo({{ top: Math.max(0, first.offsetTop - pane.offsetTop - 12), behavior: 'smooth' }});
    }};
    prev.addEventListener('click', function () {{ show(cur - 1, true); }});
    next.addEventListener('click', function () {{ show(cur + 1, true); }});
    dots.forEach(function (d) {{ d.addEventListener('click', function () {{ show(+d.getAttribute('data-goto'), true); }}); }});
    blks.forEach(function (b) {{
      var n = +b.getAttribute('data-step');
      if (n) b.addEventListener('click', function () {{ show(n, false); }});
    }});
    walk.addEventListener('keydown', function (e) {{
      if (e.key === 'ArrowRight') {{ show(cur + 1, true); e.preventDefault(); }}
      if (e.key === 'ArrowLeft') {{ show(cur - 1, true); e.preventDefault(); }}
    }});
    show(1, false);
  }});
}})();
</script>
</body>
</html>
"""


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    parsed = []
    for fname, full, short in MODULES:
        title, dek, lessons, recap, outro = parse_module(read(os.path.join(ROOT, fname)))
        parsed.append({"full": full, "short": short, "dek": dek, "lessons": lessons, "recap": recap, "outro": outro})
    all_modules = [(m["short"], [(l["num"], l["title"]) for l in m["lessons"]]) for m in parsed]
    total = sum(len(m["lessons"]) for m in parsed)

    # ---- landing
    toc = "\n".join('          <li><a href="module-%d/"><span class="toc__n">%02d</span><span class="toc__t">%s <span class="meta">&middot; %d lessons</span></span></a></li>'
                    % (n, n, inline(m["full"], ""), len(m["lessons"])) for n, m in enumerate(parsed, 1))
    main = f"""
    <section class="landing">
      <h1 class="display display--xl">{COURSE_TITLE}</h1>
      <p class="landing__sub">{COURSE_PROMISE}</p>
      <div class="landing__cta">
        <a class="btn btn--primary" href="module-1/">Start Course</a>
        <span class="meta">{len(parsed)} modules &middot; {total} lessons</span>
      </div>
    </section>
    <hr class="hero-divider">
    <section class="section section--contents" id="modules">
      <div class="card toc toc--split">
        <span class="eyebrow">The modules</span>
        <ol>
{toc}
        </ol>
      </div>
    </section>
"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(COURSE_TITLE, COURSE_DESC, "https://codenewsletter.ai/" + SLUG, "landing",
                     rail(all_modules, "landing", ""), main))

    # ---- module pages
    for n, m in enumerate(parsed, 1):
        mid = "module-%d" % n
        os.makedirs(os.path.join(OUT, mid))
        toc = "\n".join('          <li><a href="#lesson-%s"><span class="toc__n">%s</span><span class="toc__t">%s</span></a></li>'
                        % (l["num"].replace(".", "-"), l["num"], inline(l["title"])) for l in m["lessons"])
        body = [f"""
    <section class="landing" id="{mid}">
      <h1 class="display">Module {n}: {inline(m["full"])}</h1>
      <p class="landing__sub">{inline(m["dek"])}</p>
      <div class="landing__cta">
        <a class="btn btn--primary" href="#lesson-{n}-1">Start module</a>
        <span class="meta">Module {n} of {len(parsed)} &middot; {len(m["lessons"])} lessons</span>
      </div>
    </section>
    <hr class="hero-divider">
    <section class="section section--contents" id="contents">
      <div class="card toc toc--split">
        <span class="eyebrow">You will learn</span>
        <ol>
{toc}
        </ol>
      </div>
    </section>
"""]
        band_after = 3  # between the third and fourth lesson, about two-thirds through
        for k, l in enumerate(m["lessons"], 1):
            body.append("    <!-- ============================ %s ============================ -->" % l["num"])
            body.append(render_lesson(l))
            if k == band_after:
                body.append(band(mid))
        last = n == len(parsed)
        recap_k = "END OF THE GUIDE" if last else "END OF MODULE %d" % n
        recap = "\n".join("          <li>%s</li>" % inline(t) for t in m["recap"])
        outro = "\n".join("      <p>%s</p>" % inline(p) for p in m["outro"])
        if last:
            nxt = ('      <div class="next">\n        <div>\n          <span class="next__k">UP NEXT</span>\n'
                   '          <h3>What’s Next</h3>\n          <p>You finished the guide. Here is how to keep going.</p>\n        </div>\n'
                   '        <a class="btn btn--primary" href="../whats-next/">What’s Next</a>\n      </div>')
        else:
            nm = parsed[n]
            nxt = ('      <div class="next">\n        <div>\n          <span class="next__k">UP NEXT</span>\n'
                   '          <h3>Module %d: %s</h3>\n          <p>%s</p>\n        </div>\n'
                   '        <a class="btn btn--primary" href="../module-%d/">Start Module %d</a>\n      </div>'
                   % (n + 1, inline(nm["full"]), inline(nm["dek"]), n + 1, n + 1))
        body.append(f"""
    <section class="section" id="end-of-module">
      <div class="recap">
        <span class="recap__k">{recap_k}</span>
        <h3>By this point you should have:</h3>
        <ul>
{recap}
        </ul>
      </div>
{outro}
{nxt}
    </section>
""")
        with open(os.path.join(OUT, mid, "index.html"), "w", encoding="utf-8") as f:
            f.write(page("Module %d: %s" % (n, m["full"]), m["dek"],
                         "https://codenewsletter.ai/%s/%s" % (SLUG, mid), mid,
                         rail(all_modules, mid, "../"), "\n".join(body)))

    # ---- what's next
    os.makedirs(os.path.join(OUT, "whats-next"))
    sub = "https://codenewsletter.ai/subscribe?source=leadmagnets&amp;utm_medium=%s-whats-next" % SLUG
    main = f"""
    <section class="landing">
      <h1 class="display">What’s Next</h1>
      <p class="landing__sub">You finished all three modules. You now have a spec template, a boundaries block, a test-plan pattern, and two complete workflows to run spec-driven development at work.</p>
      <p class="landing__sub">Your next steps to keep levelling up:</p>
    </section>
    <hr class="hero-divider">
    <section class="section section--contents" id="next-steps">
      <div class="next">
        <div>
          <span class="next__k">EVERY WEEKDAY</span>
          <h3>Subscribe to the daily newsletter</h3>
          <p>One briefing a day on what is happening in AI and coding, and how to use AI better as a software engineering professional.</p>
        </div>
        <a class="btn btn--primary" href="{sub}" target="_blank" rel="noopener noreferrer">Subscribe to Newsletter</a>
      </div>
      <div class="next">
        <div>
          <span class="next__k">MORE GUIDES</span>
          <h3>Explore more guides like this one</h3>
          <p>Toolkits, guides and prompts. Pick the next one and go hands-on today.</p>
        </div>
        <a class="btn btn--primary" href="https://codenewsletter.ai/guides" target="_blank" rel="noopener noreferrer">See All Guides</a>
      </div>
    </section>
"""
    with open(os.path.join(OUT, "whats-next", "index.html"), "w", encoding="utf-8") as f:
        f.write(page("What’s Next", "Where to go after the spec-driven development guide.",
                     "https://codenewsletter.ai/%s/whats-next" % SLUG, "whats-next",
                     rail(all_modules, "whats-next", "../"), main))
    print("built", OUT)


if __name__ == "__main__":
    build()
