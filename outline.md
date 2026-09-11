# The Code: Guide to Spec-Driven Development — Outline v1 (approved 2026-09-11)

Three modules, 13 lessons, ~11,000 words. Each lesson: short theory, then a curated hands-on piece where a source supplies one.

---

## Module 1: Fundamentals Of Spec-Driven Development (~2,300 words)

Opening line: What SDD is, why it appeared, and how to tell when it will pay off. No tooling yet.

### 1.1 What Spec-Driven Development Is, And Its Three Levels (~600)
- Theory: The definition (Böckeler, GitHub, Tessl). The three levels: spec-first, spec-anchored, spec-as-source. Almost all tools are spec-first; only Tessl aims at spec-as-source.
- Sources: Böckeler (martinfowler.com), GitHub blog, Thoughtworks.
- Hands-on: Table of the three levels with one line on what the human edits at each level.

### 1.2 Why Prompting Breaks As Codebases Grow (~700)
- Theory: Agents are literal-minded pair programmers, not search engines (GitHub). Translation loss at four handoffs (Gupta). "Vagueness got priced" (Clawdtalk). Microsoft's hard lesson: individual speed did not become team speed; "velocity and vector."
- Sources: GitHub blog, Gupta, Clawdtalk, Inside Track, The Code Jun 16.
- Hands-on: Osmani's vague-vs-specific prompt pair ("You are a helpful coding assistant" vs. "You are a test engineer who...").

### 1.3 Spec vs. Constitution vs. Prompt: What Goes Where (~500)
- Theory: Spec is task-scoped; constitution / memory bank / rules file is codebase-scoped; a long prompt is not a spec (Böckeler). What a spec technically defines: I/O, invariants, contracts (Thoughtworks). Constitution is a team exercise (Inside Track).
- Sources: Böckeler, Thoughtworks, Inside Track, Spec Kit repo.
- Hands-on: "What goes where" table, plus Spec Kit's constitution example prompt to copy.

### 1.4 When SDD Is Worth It, And When It Is Overkill (~500)
- Theory: Small change → prompt and review (Ojstersek). Fits one context window → skip the spec (Pocock). Right-size adoption (Gupta). Böckeler's bug fix that became 16 acceptance criteria. Three places it shines: greenfield, feature in existing system, legacy modernization (GitHub).
- Sources: Ojstersek, Pocock, Gupta, Böckeler, GitHub blog.
- Hands-on: Each source's use-or-skip rule, attributed, side by side.

---

## Module 2: How To Write A Good Spec (~4,400 words)

Opening line: The templates module. By the end the reader has a spec skeleton, a boundaries block, and a real spec to copy from.

### 2.1 How To Start High-Level And Let The Agent Draft The Details (~600)
- Theory: Give a product brief, have the agent expand it into spec.md, review before code (Osmani). Plan Mode as the read-only sandbox. Force the model to restate the task, list assumptions, flag ambiguity (Ojstersek/Larridin).
- Sources: Osmani, Ojstersek.
- Hands-on: Osmani's kickoff prompt ("You are an AI software engineer. Draft a detailed specification for [project X]...") + Plan Mode steps (Goal → Steps → Expected Result).

### 2.2 How To Structure A Spec With The Six-Section Template (~1,000)
- Theory: Problem statement, non-goals, assumptions, reference implementation, architecture, test plan (Larridin via Ojstersek). "Write the smallest spec that unambiguously specifies the system." Osmani's PRD/SRS framing and six core areas from GitHub's 2,500-file study.
- Sources: Ojstersek, The Code Jul 29, Osmani.
- Hands-on: Blank six-section template as a markdown block; Osmani's `# Project Spec` skeleton for the config-side areas.

### 2.3 How To Set Boundaries The Agent Will Respect (~600)
- Theory: Three tiers: ✅ Always / ⚠️ Ask first / 🚫 Never. "Never commit secrets" was the most common useful constraint. Bring domain knowledge and gotchas into the spec.
- Sources: Osmani (GitHub study).
- Hands-on: The boundaries block to paste into a rules file or constitution.

### 2.4 How To Write Test Plans The Agent Cannot Misread (~800)
- Theory: Test plan before implementation plan (Larridin). Name each test, inputs, expected outputs; the list is the definition of done. Given/When/Then and ubiquitous language carry over from BDD (Thoughtworks). Conformance suites (Osmani/Willison).
- Sources: Ojstersek, Thoughtworks, Osmani.
- Hands-on: Ojstersek's ambiguous-vs-precise pairs ("handles large inputs gracefully" → "processes 10k rows in under 2s with memory under 500MB") + a Given/When/Then skeleton.

### 2.5 Reverse Engineering A Real Spec (~1,400)
- Theory: Walk the superpowers zero-dependency server spec in its own order: motivation with honest risk assessment, architecture, deliberately skipped scope, configuration defaults, error handling, "what stays the same," platform notes, testing strategy. Notes only on what each section does for the agent.
- Sources: obra/superpowers spec (link 2).
- Hands-on: The spec itself, linked, with margin notes. `[Video: possible walkthrough of writing a design spec]`

---

## Module 3: How To Run SDD End To End (~4,500 words)

Opening line: Two complete workflows, one adoption story, and the failure modes to watch for.

### 3.1 How To Get Started With GitHub Spec Kit (~1,500)
- Theory: The loop: constitution → specify → clarify → plan → tasks → analyze → implement → converge. Your job at each gate is to verify, not just steer (GitHub). Repeat tasks/implement until converge reports done.
- Sources: Spec Kit repo, GitHub blog, Gupta, The Code Jun 16.
- Hands-on: Install + init commands, then the seven slash commands with the repo's photo-album example prompts, in order, Goal → Steps → Expected Result. Brownfield tip: draft the spec from existing docs, cover only what changes. `[Video: Spec Kit walkthrough]`

### 3.2 How To Use The Spike-First Workflow (~1,000)
- Theory: Spike the risky parts → promote the spike to a commented reference implementation → write the spec → test plan → implementation plan (~3k lines for an 800-line spec) → implement with a small model. Decisions stop in the spec phase; a new architectural call in the plan means the spec was incomplete. Write spec with a top model, build with a cheap one.
- Sources: Ojstersek (Larridin, Ameya Kanitkar).
- Hands-on: The six-step sequence as a checklist; the `spec/spikes/reference/` folder convention; the "restate, list assumptions, flag ambiguity" prompt.

### 3.3 How Microsoft Adopted SDD On A Team (~900)
- Theory: Microsoft Digital's story: ad-hoc adoption, the hard lesson, six-stage workflow, five pillars, how roles changed (PMs own the spec, architects own the constitution, devs validate intent). Outcomes: onboarding from 2–3 weeks to days via parameterized specs.
- Sources: Inside Track, Gupta.
- Hands-on: The four-step playbook (Pilot → Formalize → Iterate → Refine and scale) as a checklist, plus Microsoft's five key takeaways.

### 3.4 The Common SDD Pitfalls And How To Avoid Them (~1,100)
- Theory: Böckeler: verbosity, reviewing markdown over code, false sense of control, agents ignoring or over-following the constitution. Osmani: vague prompts, overlong context, skipping human review, vibe coding vs. engineering, the lethal trifecta. Thoughtworks: non-determinism and spec drift, so keep deterministic CI. Pocock: the spec goes stale; durable learnings go to ADRs.
- Sources: Böckeler, Osmani, Thoughtworks, Pocock.
- Hands-on: Osmani's self-verification prompt ("After implementing, compare the result with the spec and list any items not addressed"), and his anti-pattern list.
- Closing (unheaded): "By this point you should have:" bullets for the whole guide.

---

## Cut from sources, on purpose
InfoQ five-layer model and drift detection; the waterfall debate; Kiro vs. Tessl tool comparison; Pocock's full skills chain; Osmani's subagent/multi-agent material; Spec Kit extensions, presets, bundles.
