"""One-hue SVG diagrams for the spec-driven development guide.

Rules (from the-code-lead-magnet skill): one hue only. Weak node = pale
#E9F2FF fill inside a #0F6FDB border; strong node = solid #0F6FDB with white
text; grey #5C5C5C is for connectors and structure only. Square corners.
Labels in Inter, eyebrows and captions in the mono stack.

Each entry in DIAGRAMS maps a keyword found in the markdown placeholder to a
(css class, viewBox width, viewBox height, aria label, svg body, source html).
"""
import html

WEAK, STRONG, LINE, RULE = "#E9F2FF", "#0F6FDB", "#0F6FDB", "#5C5C5C"
INK, INK2, INK3, SURFACE = "#000000", "#3F3F3F", "#5C5C5C", "#FFFFFF"
SANS = "Inter,system-ui,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,Menlo,monospace"

SRC = {
    "bockeler": ('Understanding Spec-Driven-Development', "https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html"),
    "gupta": ('Spec-Driven Development: A Spec-First Approach to AI-Native Engineering', "https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/"),
    "insidetrack": ('Engineering the Frontier Firm', "https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/"),
    "speckit": ('Spec Kit quick start guide', "https://github.github.io/spec-kit/quickstart.html"),
    "osmani": ('How to write a good spec for AI agents', "https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents"),
    "ojstersek": ('How to Do Spec-Driven Development', "https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development"),
    "pocock": ('The /to-spec Skill', "https://www.aihero.dev/skills-to-spec"),
    "github": ('Spec-driven development with AI', "https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/"),
}


def src(*keys):
    parts = ['<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (SRC[k][1], html.escape(SRC[k][0])) for k in keys]
    return "Source: " + "; ".join(parts) + "."


# ------------------------------------------------------------------ primitives

def text(x, y, s, size=13, weight=500, fill=INK, anchor="start", family=SANS, extra=""):
    return '<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" %s>%s</text>' % (
        x, y, family, size, weight, fill, anchor, extra, html.escape(s))


def lines(x, y, rows, size=12.5, weight=500, fill=INK, anchor="start", lh=None, family=SANS):
    lh = lh or size * 1.3
    return "".join(text(x, y + i * lh, r, size, weight, fill, anchor, family) for i, r in enumerate(rows))


def eyebrow(x, y, s, fill=INK3, anchor="start"):
    return text(x, y, s, 10, 600, fill, anchor, MONO, 'letter-spacing="1.6"')


def node(x, y, w, h, title, sub=(), strong=False, dashed=False, title_size=13, sub_size=11.5):
    fill = STRONG if strong else WEAK
    stroke = LINE
    ink = SURFACE if strong else INK
    ink2 = SURFACE if strong else INK2
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    out = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="1"%s/>' % (x, y, w, h, fill, stroke, dash)
    t = title if isinstance(title, (list, tuple)) else [title]
    total = len(t) * title_size * 1.25 + (len(sub) * sub_size * 1.3 + (6 if sub else 0))
    ty = y + (h - total) / 2 + title_size
    out += lines(x + w / 2, ty, t, title_size, 600, ink, "middle", title_size * 1.25)
    if sub:
        out += lines(x + w / 2, ty + len(t) * title_size * 1.25 + 6, sub, sub_size, 400, ink2, "middle", sub_size * 1.3)
    return out


def arrow(x1, y1, x2, y2, dashed=False):
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5" marker-end="url(#ah)"%s/>' % (x1, y1, x2, y2, RULE, dash)


def path(d, dashed=False, arrowhead=True):
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    m = ' marker-end="url(#ah)"' if arrowhead else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="1.5"%s%s/>' % (d, RULE, dash, m)


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>' % RULE)


# ------------------------------------------------------------------ diagrams

def three_levels():
    W, H = 620, 255
    o = [DEFS]
    cols = [
        ("LEVEL 1", "Spec-first", ["Write the spec, then use it", "for the task at hand"], ["Human edits: the spec before", "the task, the code after"], False),
        ("LEVEL 2", "Spec-anchored", ["Keep the spec after the task,", "use it to evolve the feature"], ["Human edits: the spec and", "the code, kept in step"], False),
        ("LEVEL 3", "Spec-as-source", ["The spec is the main source", "file over time"], ["Human edits: only the spec,", "never the code"], True),
    ]
    bw, bh, gap = 180, 96, 25
    for i, (eb, title, desc, edits, strong) in enumerate(cols):
        x = 15 + i * (bw + gap)
        y = 120 - i * 40
        o.append(eyebrow(x, y - 10, eb))
        o.append(node(x, y, bw, bh, title, desc, strong=strong))
        o.append(lines(x, y + bh + 20, edits, 11.5, 500, INK2))
        if i < 2:
            o.append(arrow(x + bw + 3, y + bh / 2, x + bw + gap - 3, y + bh / 2 - 40))
    return ("levels", W, H, "Böckeler's three levels of spec-driven development, as three rising steps: spec-first, spec-anchored, and spec-as-source, with what the human edits at each.", "".join(o), src("bockeler"))


def four_handoffs():
    W, H = 620, 175
    o = [DEFS]
    stages = [["Stakeholder", "needs"], ["Product", "requirements"], ["Architecture", "and design"], ["Implemen-", "tation"], ["Validation", "and release"]]
    bw, bh, gap, y = 96, 56, 30, 60
    for i, s in enumerate(stages):
        x = 15 + i * (bw + gap)
        o.append(node(x, y, bw, bh, s, strong=(i == 0)))
        if i < 4:
            ax = x + bw
            o.append(arrow(ax + 3, y + bh / 2, ax + gap - 3, y + bh / 2))
            o.append('<rect x="%s" y="%s" width="10" height="10" fill="%s" stroke="%s" stroke-width="1" transform="rotate(45 %s %s)"/>' % (ax + gap / 2 - 5, y + bh + 18, SURFACE, LINE, ax + gap / 2, y + bh + 23))
            o.append(text(ax + gap / 2, y + bh + 48, "leak %d" % (i + 1), 10, 600, INK3, "middle", MONO, 'letter-spacing="1.2"'))
    o.append(eyebrow(15, 30, "INTENT MOVES LEFT TO RIGHT. MEANING LEAKS AT EVERY HANDOFF."))
    return ("handoffs", W, H, "The four handoffs where intent leaks: stakeholder needs to product requirements, requirements to architecture and design, design to implementation, implementation to validation and release.", "".join(o), src("gupta"))


def three_scopes():
    W, H = 620, 310
    LQ, RQ = "\u201c", "\u201d"
    o = []
    o.append('<rect x="15" y="15" width="590" height="280" fill="%s" stroke="%s" stroke-width="1"/>' % (WEAK, LINE))
    o.append(text(30, 39, "Constitution", 14, 600, INK))
    o.append(text(30, 56, "The whole codebase, every session. Architectural principles, governance, security standards, limits.", 11.5, 400, INK2))
    o.append(text(30, 73, "e.g. principles for code quality, testing standards, UX consistency, performance", 10.5, 500, INK3, family=MONO))
    o.append('<rect x="45" y="88" width="530" height="192" fill="%s" stroke="%s" stroke-width="1"/>' % (SURFACE, LINE))
    o.append(text(60, 112, "Spec", 14, 600, INK))
    o.append(text(60, 129, "One task or feature, while it is created or changed. The what and the why.", 11.5, 400, INK2))
    o.append(text(60, 146, "e.g. albums grouped by date, re-organized by drag and drop, never nested", 10.5, 500, INK3, family=MONO))
    o.append('<rect x="75" y="162" width="470" height="100" fill="%s" stroke="%s" stroke-width="1"/>' % (STRONG, LINE))
    o.append(text(90, 186, "Prompt", 14, 600, SURFACE))
    o.append(text(90, 203, "One request to the agent. The instruction for the step at hand.", 11.5, 400, SURFACE))
    o.append(text(90, 228, "e.g. %sYou are a test engineer who writes tests for React components,%s" % (LQ, RQ), 10.5, 500, SURFACE, family=MONO))
    o.append(text(90, 244, "   %sfollows these examples, and never modifies source code.%s" % (LQ, RQ), 10.5, 500, SURFACE, family=MONO))
    return ("scopes", W, H, "Three nested scopes: the constitution wraps the whole codebase, the spec wraps one feature, and the prompt wraps one request, each with an example from the sources.", "".join(o), src("bockeler", "insidetrack"))


def decision_flow():
    W, H = 620, 330
    o = [DEFS]
    qx, qw, qh = 15, 250, 50
    ox, ow = 360, 245
    rows = [
        (["Have you decided", "what to build?"], "no", ["Decide first"], False),
        (["Is it a small change? One file,", "one adjustment to a feature"], "yes", ["Prompt the agent,", "then review the code"], False),
        (["Does the work fit", "one context window?"], "yes", ["Implement.", "Skip the spec."], False),
        (["Spans several sessions, or", "feasibility is uncertain"], "", ["Write the spec,", "then cut it into tickets"], True),
    ]
    for i, (q, ans, out, strong) in enumerate(rows):
        y = 20 + i * 78
        o.append(node(qx, y, qw, qh, q, title_size=12.5))
        o.append(node(ox, y, ow, qh, out, strong=strong, title_size=12.5))
        o.append(arrow(qx + qw + 3, y + qh / 2, ox - 3, y + qh / 2))
        if ans:
            o.append(text((qx + qw + ox) / 2, y + qh / 2 - 6, ans, 10, 600, INK3, "middle", MONO, 'letter-spacing="1.2"'))
        if i < 3:
            o.append(arrow(qx + qw / 2, y + qh + 3, qx + qw / 2, y + 78 - 3))
            o.append(text(qx + qw / 2 + 8, y + qh + 20, "yes" if i == 0 else "no", 10, 600, INK3, "start", MONO, 'letter-spacing="1.2"'))
    return ("decide", W, H, "A decision flow for when to write a spec: decide first if nothing is decided; prompt and review for a small change; implement without a spec if the work fits one context window; write the spec when the work spans sessions or feasibility is uncertain.", "".join(o), src("ojstersek", "pocock"))


def six_sections():
    W, H = 620, 300
    o = []
    o.append('<rect x="15" y="15" width="300" height="270" fill="%s" stroke="%s" stroke-width="1"/>' % (SURFACE, LINE))
    o.append(eyebrow(30, 38, "SPEC.MD"))
    rows = [
        ("1", "Problem statement", "What you solve and for whom. One paragraph."),
        ("2", "Non-goals", "What the system will not do."),
        ("3", "Assumptions", "Decisions made, so the model does not guess."),
        ("4", "Reference implementation", "The promoted spike, shortcuts marked."),
        ("5", "Architecture", "Data model, boundaries, interfaces, errors."),
        ("6", "Test plan", "Named tests with inputs and outputs. Done."),
    ]
    for i, (n, t, d) in enumerate(rows):
        y = 52 + i * 38
        strong = i in (0, 5)
        o.append('<rect x="30" y="%s" width="270" height="30" fill="%s" stroke="%s" stroke-width="1"/>' % (y, STRONG if strong else WEAK, LINE))
        o.append(text(40, y + 20, n, 11, 600, SURFACE if strong else INK3, family=MONO))
        o.append(text(58, y + 20, t, 12.5, 600, SURFACE if strong else INK))
        o.append('<line x1="300" y1="%s" x2="330" y2="%s" stroke="%s" stroke-width="1"/>' % (y + 15, y + 15, RULE))
        o.append(text(336, y + 19, d, 11, 400, INK2))
    return ("sections", W, H, "Larridin's six-section spec as one stacked outline: problem statement, non-goals, assumptions, reference implementation, architecture, test plan.", "".join(o), src("ojstersek"))


def three_tiers():
    W, H = 620, 160
    o = []
    tiers = [
        ("✅ ALWAYS DO", ["The agent proceeds", "without asking"], "“Always run tests before commits.”", 0),
        ("⚠️ ASK FIRST", ["The agent pauses for", "a human check"], "“Ask before adding dependencies.”", 1),
        ("\U0001f6ab NEVER DO", ["The agent stops.", "Hard limit."], "“Never commit secrets or keys.”", 2),
    ]
    bw, gap = 186, 16
    for i, (eb, sub, ex, level) in enumerate(tiers):
        x = 15 + i * (bw + gap)
        fill = [WEAK, SURFACE, STRONG][level]
        sw = [1, 2, 1][level]
        ink = SURFACE if level == 2 else INK
        ink2 = SURFACE if level == 2 else INK2
        o.append('<rect x="%s" y="20" width="%s" height="120" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, bw, fill, LINE, sw))
        o.append(text(x + 14, 46, eb, 11, 600, ink, family=MONO, extra='letter-spacing="1.4"'))
        o.append(lines(x + 14, 72, sub, 12.5, 600, ink))
        o.append(text(x + 14, 122, ex, 9.5, 400, ink2))
    return ("tiers", W, H, "The three boundary tiers as a scale from open to closed: Always do, where the agent proceeds; Ask first, where it pauses; Never do, where it stops.", "".join(o), src("osmani"))


def speckit_loop():
    W, H = 620, 312
    o = [DEFS]
    o.append(node(215, 15, 190, 44, "/speckit.constitution", ["once per project"], strong=True, title_size=12))
    core = ["specify", "plan", "tasks", "implement", "converge"]
    bw, gap, y = 100, 22, 110
    xs = [15 + i * (bw + gap) for i in range(5)]
    o.append(arrow(310, 62, 310, y - 3))
    for i, c in enumerate(core):
        o.append(node(xs[i], y, bw, 46, "/speckit." + c, title_size=11.5))
        if i < 4:
            o.append(arrow(xs[i] + bw + 3, y + 23, xs[i + 1] - 3, y + 23))
    # converge loops back to implement until Converged
    o.append(path("M%s %s L%s %s L%s %s L%s %s" % (xs[4] + bw / 2, y + 49, xs[4] + bw / 2, y + 80, xs[3] + bw / 2, y + 80, xs[3] + bw / 2, y + 52)))
    o.append(text((xs[3] + xs[4] + bw) / 2, y + 96, "repeat until Converged", 10, 600, INK3, "middle", MONO, 'letter-spacing="1"'))
    gates = [("clarify", 0, ["no open ambiguity"]), ("checklist", 1, ["requirements complete,", "clear, and consistent"]), ("analyze", 2, ["conflicts and gaps", "across the three files"])]
    gy = 235
    for c, i, sub in gates:
        gx = xs[i] + bw / 2 + gap / 2 - 4
        o.append(node(gx, gy, 124, 62, "/speckit." + c, sub, dashed=True, title_size=11, sub_size=9.5))
        o.append(arrow(gx + 62, gy - 3, gx + 62, y + 49 + 3, dashed=True))
    o.append(eyebrow(15, 88, "CORE LOOP, ONCE PER FEATURE"))
    o.append(eyebrow(15, 225, "OPTIONAL QUALITY GATES"))
    return ("loop", W, H, "Spec Kit's nine commands as a loop: constitution once at the top, then specify, plan, tasks, implement, and converge in a ring that repeats until converged, with clarify, checklist, and analyze as optional gates between steps.", "".join(o), src("speckit"))


def spike_pipeline():
    W, H = 620, 195
    o = [DEFS]
    steps = [["Spike the", "risky parts"], ["Promote it to a", "reference"], ["Write the", "spec"], ["Write the", "test plan"], ["Write the", "plan"], ["Implement", "from the plan"]]
    bw, gap, y = 86, 14, 90
    xs = [15 + i * (bw + gap) for i in range(6)]
    for i, s in enumerate(steps):
        o.append(node(xs[i], y, bw, 56, s, strong=(i == 5), title_size=11.5))
        o.append(text(xs[i], y - 8, "0%d" % (i + 1), 10, 600, INK3, family=MONO, extra='letter-spacing="1.2"'))
        if i < 5:
            o.append(arrow(xs[i] + bw + 2, y + 28, xs[i + 1] - 2, y + 28))

    def bracket(a, b, label, yy, anchor="middle"):
        x1, x2 = xs[a], xs[b] + bw
        o.append(path("M%s %s L%s %s L%s %s L%s %s" % (x1, yy + 8, x1, yy, x2, yy, x2, yy + 8), arrowhead=False))
        lx = {"start": x1, "end": x2, "middle": (x1 + x2) / 2}[anchor]
        o.append(text(lx, yy - 6, label, 10.5, 600, INK3, anchor, MONO, 'letter-spacing="1.2"'))
    bracket(0, 1, "PROVE IT WORKS, THEN COMMENT IT", 42, "start")
    bracket(2, 4, "TOP MODEL", 42)
    bracket(5, 5, "SMALL MODEL", 42, "end")
    o.append(text(xs[1], 176, "spec/spikes/reference/<name>", 10.5, 500, INK3, family=MONO))
    o.append(text(xs[4], 176, "plans/", 10.5, 500, INK3, family=MONO))
    return ("spike", W, H, "Larridin's six-step pipeline: spike, reference implementation, spec, test plan, implementation plan, code, with a top model over the spec steps and a small model over the build step.", "".join(o), src("ojstersek"))


def six_stages():
    W, H = 620, 190
    o = [DEFS]
    o.append(node(15, 15, 590, 40, "Constitution: architectural principles, governance, security standards, limits", strong=True, title_size=12))
    o.append(text(15, 76, "agreed by the whole team before any spec", 10.5, 500, INK3, family=MONO))
    stages = [["Define the", "problem and", "outcomes"], ["Clarify", "ambiguities"], ["Create the", "technical", "plan"], ["Break work", "into traceable", "tasks"], ["Validate", "requirements", "against plans"], ["Implement", "and test"]]
    bw, gap, y = 88, 12, 100
    for i, s in enumerate(stages):
        x = 15 + i * (bw + gap)
        o.append(node(x, y, bw, 70, s, title_size=11.5))
        o.append(text(x, y - 8, "%d" % (i + 1), 10, 600, INK3, family=MONO))
        if i < 5:
            o.append(arrow(x + bw + 2, y + 35, x + bw + gap - 2, y + 35))
    return ("stages", W, H, "Microsoft Digital's six SDD stages as a pipeline under a constitution bar: define, clarify, plan, break into tasks, validate, implement and test.", "".join(o), src("insidetrack"))


def five_pillars():
    W, H = 620, 218
    o = []
    o.append('<path d="M15 60 L310 18 L605 60 Z" fill="%s" stroke="%s" stroke-width="1"/>' % (STRONG, LINE))
    o.append(text(310, 50, "The value of SDD", 13, 600, SURFACE, "middle"))
    pillars = [["Spec as the", "source of truth"], ["Living,", "executable", "artifacts"], ["AI-assisted", "automation"], ["Human", "validation and", "collaboration"], ["Predictability", "and", "measurability"]]
    bw, gap = 106, 15
    for i, p in enumerate(pillars):
        x = 15 + i * (bw + gap)
        o.append(node(x, 72, bw, 120, p, title_size=12))
    o.append('<rect x="15" y="196" width="590" height="8" fill="%s" stroke="%s" stroke-width="1"/>' % (WEAK, LINE))
    return ("pillars", W, H, "Five pillars under one roof labeled the value of SDD: spec as the source of truth, living executable artifacts, AI-assisted automation, human validation and collaboration, predictability and measurability.", "".join(o), src("insidetrack"))


def four_roles():
    W, H = 620, 250
    o = []
    roles = [
        ("LEADERS", ["Reward clarity and alignment before", "implementation, and drive adoption:", "SDD only paid off as a standard."]),
        ("DEVELOPERS", ["Understand the problem fully, with", "success defined, before any code.", "Make the agent understand it too."]),
        ("PMS", ["Own the spec. Define success criteria,", "resolve ambiguities, keep priorities", "visible through implementation."]),
        ("ARCHITECTS", ["Create and maintain the constitution,", "so issues surface before", "implementation, not in review."]),
    ]
    cw, ch, gap = 287, 105, 16
    for i, (eb, body) in enumerate(roles):
        x = 15 + (i % 2) * (cw + gap)
        y = 15 + (i // 2) * (ch + gap)
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (x, y, cw, ch, WEAK if i % 3 else SURFACE, LINE))
        o.append(text(x + 16, y + 26, eb, 10.5, 600, STRONG, family=MONO, extra='letter-spacing="1.6"'))
        o.append(lines(x + 16, y + 50, body, 11.5, 400, INK2))
    return ("roles", W, H, "Four role cards, one line each on what changed at Microsoft: leaders, developers, program and product managers, architects.", "".join(o), src("insidetrack"))


DIAGRAMS = {
    "three levels": three_levels,
    "four handoffs": four_handoffs,
    "nested scopes": three_scopes,
    "decision flow": decision_flow,
    "six sections": six_sections,
    "three tiers": three_tiers,
    "nine commands": speckit_loop,
    "six steps": spike_pipeline,
    "six stages": six_stages,
    "five pillars": five_pillars,
    "four role cards": four_roles,
}


def render(key_text):
    """Return (css_class, html) for the placeholder text, or None."""
    for key, fn in DIAGRAMS.items():
        if key in key_text:
            cls, w, h, label, body, source = fn()
            svg = ('<svg class="diagram--%s" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">%s</svg>'
                   % (cls, w, h, html.escape(label), body))
            out = ('<div class="card card--flush diagram">\n  <figure>\n    <div class="scroller">\n      %s\n    </div>\n'
                   '    <figcaption><span class="scroll-hint">Scroll sideways &rarr;</span>%s</figcaption>\n  </figure>\n</div>' % (svg, source))
            return cls, out
    return None


def css():
    return "\n".join(".diagram--%s { min-width: 600px; }" % fn()[0] for fn in DIAGRAMS.values())


# Osmani's six anti-patterns as a pre-handoff check (rule 10: a checklist component)
CHECKLIST = """<div class="card">
  <div class="score" data-key="spec-driven-development.module-3.pre-handoff">
    <div class="score__group">Pre-handoff check</div>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">1</span>No vague prompts. Inputs, outputs, and constraints are specific.</span></button>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">2</span>No overlong context. Only what is relevant is in the prompt, summarized or retrieved.</span></button>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">3</span>Human review is scheduled. Nobody commits code they could not explain.</span></button>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">4</span>The mode is named. Prototype, or production with specs, tests, and review.</span></button>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">5</span>The lethal trifecta is covered. Speed, non-determinism, and cost each have a check.</span></button>
    <button class="score__item" type="button" aria-pressed="false"><span class="score__box" aria-hidden="true"></span><span class="score__text"><span class="score__n">6</span>All six core areas are present. Commands, testing, structure, style, git workflow, boundaries.</span></button>
    <div class="score__result">
      <div class="score__num">0 / 6</div>
      <p class="score__verdict">Tick each item before you hand a spec to the agent. This browser remembers your ticks.</p>
      <button class="btn btn--ghost btn--sm score__reset" type="button">Reset</button>
    </div>
    <p class="visually-hidden score__live" role="status" aria-live="polite"></p>
  </div>
</div>"""
