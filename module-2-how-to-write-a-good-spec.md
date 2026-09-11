# Module 2: How To Write A Good Spec

This is the templates module. By the end you have a spec skeleton, a boundaries block, and a real spec to copy from.

- [2.1 Start With A Brief And Let The Agent Draft The Spec](#21-start-with-a-brief-and-let-the-agent-draft-the-spec)
- [2.2 The Six-Section Spec Template](#22-the-six-section-spec-template)
- [2.3 How To Set Boundaries The Agent Will Respect](#23-how-to-set-boundaries-the-agent-will-respect)
- [2.4 How To Write Test Plans The Agent Cannot Misread](#24-how-to-write-test-plans-the-agent-cannot-misread)
- [2.5 Reverse Engineering A Real Spec](#25-reverse-engineering-a-real-spec)

---

## 2.1 Start With A Brief And Let The Agent Draft The Spec

### Start With A Product Brief, Not A Full Spec

Begin with a clear goal statement and a few requirements, then let the agent expand that brief into a detailed spec. Review the draft before any code.

That is the first of five principles in Anthropic engineer Addy Osmani's [guide to specs for AI agents](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents). Agents excel at elaboration when they have a clear mission, and they drift off course without one.

Osmani asks the agent to write the result to a file such as spec.md. That file anchors the agent when a session restarts or the history grows too long.

The draft usually comes back structured: an overview, a feature list, tech stack suggestions, and a data model. Review it, correct any hallucination or off-target detail, and only then move to code.

Osmani's one exception: this works well unless you already have very specific technical requirements that must hold from the start.

### Keep The Brief About What And Why

A high-level brief focuses on what and why, not on how, at least at first. Ask three questions: who is the user, what do they need, and what does success look like.

Osmani's example brief for a to-do app: "Build a web app where users can track tasks (to-do list), with user accounts, a database, and a simple UI."

His success criteria in the same style: "User can add, edit, complete tasks; data is saved persistently; the app is responsive and secure."

[Spec Kit](https://github.com/github/spec-kit)'s docs say the same: describe what you build and why, and let the agent write the spec around user experience and success criteria. That is [the what-and-how split](module-1-fundamentals.md#13-spec-constitution-or-prompt-what-goes-where) covered earlier.

### Make The Agent Restate The Task, List Assumptions, And Flag Ambiguity

When an agent helps write the spec, force it to restate the task, list its assumptions, and flag any ambiguity.

That rule comes from Larridin CTO Ameya Kanitkar, via Gregor Ojstersek's [account of how Larridin does SDD](https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development).

The check catches the details the model would otherwise pick silently. Anything still open after it gets its own investigation before the spec is final. [The lesson on the spike-first workflow](module-3-how-to-run-sdd-end-to-end.md#32-how-to-use-the-spike-first-workflow) shows how Larridin does that.

Osmani runs the same check in a read-only planning mode, such as [Claude Code](https://claude.com/claude-code)'s Plan Mode. The agent analyzes the codebase and drafts the spec, but writes no code.

Ask it to question you about the plan, then to review the plan for architecture, best practices, security risks, and testing strategy. Refine until there is no room for misinterpretation, and only then let the agent execute.

### Hands-On: The Kickoff Prompt, Run In Planning Mode

Goal: Turn a one-paragraph brief into a reviewed spec.md before the agent writes any code.

Steps:

1. Switch your coding agent to its read-only planning mode, if it has one. Osmani's example is Claude Code's Plan Mode.
2. Paste Osmani's kickoff prompt, with your high-level brief in place of the placeholder:

```
You are an AI software engineer. Draft a detailed specification for [project X]
covering objectives, features, constraints, and a step-by-step plan.
```

3. Before you read the draft, make the agent run Larridin's check. Neither source gives a prompt for it, so this one is ours:

```
Before you finalize the spec: restate in your own words what needs to be built,
list every assumption you made, and flag anything in the brief that is ambiguous.
Ask me about each open point. Do not choose an answer yourself.
```

4. Answer its questions.
5. Ask it to review the plan for architecture, best practices, security risks, and testing strategy.
6. Correct any hallucination or detail that misses your vision, until there is no room for misinterpretation.
7. Leave planning mode.
8. Save the result as spec.md.

Expected result: A spec.md with an overview, a feature list, tech stack suggestions, and a data model. The agent stated every assumption, you resolved every ambiguity, and no code exists yet.

---

## 2.2 The Six-Section Spec Template

### Write The Smallest Spec That Leaves No Ambiguity

Write the smallest spec that unambiguously specifies the system. If a section feels like fluff, cut it. If a decision feels obvious, write it down anyway, because "obvious to you" is not the same as "obvious to the model."

That is Larridin CTO Ameya Kanitkar's recommendation, via Gregor Ojstersek's [account of how Larridin does SDD](https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development).

The bar for detail: the spec should be enough to hand to a junior engineer or a small model.

### The Six Sections

`[Infographic: the six sections as one stacked document outline, problem at the top and test plan at the bottom]`

Larridin's reference implementation is a promoted spike; [the lesson on the spike-first workflow](module-3-how-to-run-sdd-end-to-end.md#32-how-to-use-the-spike-first-workflow) covers how they build one. [The lesson on test plans](#24-how-to-write-test-plans-the-agent-cannot-misread) covers the sixth section in full.

### Blend A PRD With An SRS

Treat the spec as a structured document with clear sections, not a loose pile of notes. That is the second principle from Anthropic engineer Addy Osmani in [his guide to specs for AI agents](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents). A formal document gives a "literal-minded" agent a blueprint.

Osmani blends two document types. The Product Requirements Document (PRD) side keeps the user-centric "why" behind each feature. The Software Requirements Specification (SRS) side nails down specifics such as which database or API to use.

Use a consistent format. Many developers use Markdown headings or XML-like tags to mark sections, because models handle well-structured text better than free-form prose.

Be specific about your stack. Say "React 18 with TypeScript, Vite, and Tailwind CSS," not "React project," and include versions and key dependencies. Vague specs produce vague code.

Osmani warns that "minimal does not necessarily mean short." Do not shy away from detail where it matters, but keep the spec focused.

### Six Things Every Spec Must Cover

The most effective specs cover six areas. That is the pattern GitHub found in its analysis of more than 2,500 agent configuration files, which Osmani turns into a completeness checklist:

1. **Commands.** Full commands with flags, early in the file, such as `npm test`, `pytest -v`, `npm run build`. The agent references these constantly.
2. **Testing.** How to run tests, which framework, where test files live, and what coverage you expect.
3. **Project structure.** Where source code, tests, and docs live, stated explicitly.
4. **Code style.** One real code snippet that shows your style beats three paragraphs that describe it. Include naming conventions and formatting rules.
5. **Git workflow.** Branch naming, commit message format, PR requirements.
6. **Boundaries.** What the agent should never touch: secrets, vendor directories, production configs, specific folders.

These six areas belong to [the codebase-scoped layer](module-1-fundamentals.md#13-spec-constitution-or-prompt-what-goes-where), and Osmani blends them into one Project Spec document. [The lesson on boundaries](#23-how-to-set-boundaries-the-agent-will-respect) covers them in full.

### Two Skeletons To Copy

Larridin's six sections as a blank template:

```
# Spec: [feature or system]

## Problem statement
## Non-goals
## Assumptions
## Reference implementation
## Architecture
## Test plan
```

Osmani's skeleton for the config-side areas, from his guide:

```
# Project Spec: My team's tasks app

## Objective
- Build a web app for small teams to manage tasks...

## Tech Stack
- React 18+, TypeScript, Vite, Tailwind CSS
- Node.js/Express backend, PostgreSQL, Prisma ORM

## Commands
- Build: `npm run build` (compiles TypeScript, outputs to dist/)
- Test: `npm test` (runs Jest, must pass before commits)
- Lint: `npm run lint --fix` (auto-fixes ESLint errors)

## Project Structure
- `src/` – Application source code
- `tests/` – Unit and integration tests
- `docs/` – Documentation

## Boundaries
- ✅ Always: Run tests before commits, follow naming conventions
- ⚠️ Ask first: Database schema changes, adding dependencies
- 🚫 Never: Commit secrets, edit node_modules/, modify CI config
```

---

## 2.3 How To Set Boundaries The Agent Will Respect

### The Spec Is Coach And Referee

A good spec anticipates where the agent might go wrong and sets up guardrails. It also uses what you know, such as domain knowledge, edge cases, and gotchas, so the agent does not operate in a vacuum.

Addy Osmani of Anthropic's fourth principle, in [his guide to specs for AI agents](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents), says the spec is both coach and referee.

### The Three Tiers: Always, Ask First, Never

The most effective specs use a three-tier boundary system rather than a flat list of do's and don'ts. That is GitHub's finding from its study of 2,500 agent files, as Osmani reports it.

The tiers tell the agent when to proceed, when to pause, and when to stop:

- **✅ Always do**
- **⚠️ Ask first**
- **🚫 Never do**

"Never commit secrets" was the single most common helpful constraint in the study.

`[Infographic: the three tiers as a traffic light, Always in green, Ask first in amber, Never in red, one example line each]`

### Put Your Domain Knowledge In The Spec

Your spec should reflect insights that only an experienced developer, or someone with context, would know. Osmani's phrase for it: pour your mentorship into the spec.

If you build an e-commerce agent and you know that products and categories have a many-to-many relationship, state that clearly. Do not assume the agent will infer it, because it might not.

If a library is notoriously tricky, mention the pitfalls to avoid. The spec can hold advice such as "when using library X, watch out for the memory leak issue in version Y and apply this workaround."

Encode your style preferences too, such as "use functional components, not class components in React," and the agent will emulate your style.

A small example anchors the agent to the exact format you want. Many engineers include one in the spec, such as "All API responses should be JSON," followed by the error shape `{"error": "message"}`.

### A Boundaries Block To Copy

Osmani's three tiers with his example lines, as one block for your rules file or constitution, [the codebase-scoped layer](module-1-fundamentals.md#13-spec-constitution-or-prompt-what-goes-where):

```
## Boundaries

✅ Always do
- Always run tests before commits.
- Always follow the naming conventions in the style guide.
- Always log errors to the monitoring service.

⚠️ Ask first
- Ask before modifying database schemas.
- Ask before adding new dependencies.
- Ask before changing CI/CD configuration.

🚫 Never do
- Never commit secrets or API keys.
- Never edit node_modules/ or vendor/.
- Never remove a failing test without explicit approval.
```

---

## 2.4 How To Write Test Plans The Agent Cannot Misread

### Write The Test Plan Before The Implementation Plan

Test-driven development and spec-driven development fit together. Once you know what the system does, write the test plan before the implementation plan, not after.

Larridin CTO Ameya Kanitkar's rule, via Gregor Ojstersek's [account of how Larridin does SDD](https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development), makes the test plan part of the spec. Go over it and adjust it if something is wrong or missing.

There is no need to implement the tests yet. List them, name each one, and specify inputs and expected outputs. That list is a clear definition of done, and you measure the implementation plan against it.

Watch out for "ambiguous tests." The two pairs at the end of this lesson show Ojstersek's fix.

### Keep What BDD Taught: Plain Language And Given/When/Then

Experience from behavior-driven development (BDD) is still valid, and this new technology should not change much in this area. That is the view of Thoughtworks Technology Director Liu Shangqi in [his analysis of spec-driven development](https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices).

Specifications should still:

- Use domain-oriented ubiquitous language to describe business intent, not tech-bound implementations.
- Have a clear structure, with a common style to define scenarios with Given/When/Then.
- Strive for completeness yet conciseness, and cover the critical path without an enumeration of all cases. With AI, that also saves tokens.
- Aim for clarity and determinism. LLMs do not generate deterministic code, but clear specifications still reduce hallucinations.

Liu adds that the spec-by-example we use in BDD is essentially the few-shot prompt technique.

### Put Tests In The Success Criteria, Or In A Conformance Suite

Incorporate a test plan, or even actual tests, into your spec and prompt flow. In the spec's success criteria, say "these sample inputs should produce these outputs" or "the following unit tests should pass."

Addy Osmani, an engineer at Anthropic, gives that advice in [his guide to specs for AI agents](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents). He also relays Simon Willison's case for conformance suites: language-independent tests, often YAML-based, that any implementation must pass. A conformance suite is more rigorous than ad-hoc unit tests, because it derives directly from the spec, and you can reuse it across implementations.

Willison's summary, via Osmani: a robust test suite is "like giving the agents superpowers," because they can validate and iterate quickly when tests fail.

### Precise Tests, And A Scenario Skeleton To Copy

Ojstersek's two pairs, side by side:

```
Instead of:  Handles large inputs gracefully
Write:       Processes 10k rows in under 2 seconds with memory under 500MB

Instead of:  Fails safely on bad input
Write:       Returns a 400 with a specific error code when the payload
             is missing the customer_id field
```

The standard Given/When/Then form Thoughtworks recommends for each scenario, as a blank skeleton:

```
Scenario: [what the user does, in the domain's own words]
  Given [the starting state]
  When  [the action]
  Then  [the observable result]
```

Osmani's one-line conformance reference, for the spec's success criteria:

```
Must pass all cases in conformance/api-tests.yaml
```

---

## 2.5 Reverse Engineering A Real Spec

This lesson walks one real spec in its own order. The spec is on the left. Step through it, and the note beside each section says what it does for the agent and which rule it applies.

The spec is the [zero-dependency brainstorm server design](https://github.com/obra/superpowers/blob/main/docs/superpowers/specs/2026-03-11-zero-dep-brainstorm-server-design.md) by Jesse Vincent, author of the [superpowers](https://github.com/obra/superpowers) skills library for coding agents. It is about 860 words and changes an existing system, not a greenfield one.

`[Stepper: Sources/superpowers-brainstorm-server-spec.md]`

### The Title Line Is The Problem Statement

One sentence states what changes and into what: 714 vendored files become one file with no dependencies. The agent knows the problem and the shape of done before it reads anything else. This is Larridin's problem statement, in one paragraph.

### Motivation With An Honest Risk Assessment

The section names the risk, unpatched third-party code, and then sizes it: low, on a localhost-only server. That size tells the agent how much to build. Without it, an agent treats every risk as critical and over-engineers the fix.

### Architecture: Decisions Written Down So The Agent Does Not Guess

The spec fixes one file, a line budget, four built-ins, the RFC, three length encodings, and four opcodes. Each is a decision the agent would otherwise make on its own, and silently. Written down, they cannot drift between sessions.

### "Deliberately Skipped": Non-Goals Where They Bite

Four features the server will not have, with the reason and the proof that the omission is safe. This is where the spec stops the agent from building a full WebSocket library. The non-goals sit next to the section they apply to.

### Configuration Defaults And The Startup Sequence

Every variable carries its default, and the one non-obvious startup step carries its reason. Obvious to you is not obvious to the model. A missing default is a guess the agent makes for you.

### Error Handling, Case By Case

Each line pairs a condition with one response, so the agent can test each case. The last line is a decision not to build shutdown logic. A precise no is as useful as a precise yes.

### What Changes And What Stays The Same

The table lists what goes and the one file that replaces it. The list names six files the agent must not touch, and the one exception. These boundaries make a brownfield change safe.

### Platform Notes

Three facts only someone with context knows: which built-ins are cross-platform, where the file watcher is reliable, and that the scripts need bash. Without them, the agent finds out in production.

### Testing Strategy

Two test files, and what each covers. The test-only dependency is named as test-only, so the agent does not ship it. This list is the definition of done.

### Each Section, And The Rule It Applies

| Passage in the spec | What it does for the agent | Rule and source |
|---|---|---|
| Title line | States what you solve, in one sentence | Problem statement, Larridin via Ojstersek |
| Motivation, "the actual risk is low" | Gives the why, sized honestly | PRD side, Osmani |
| Architecture, protocol details | Writes down decisions the model would otherwise guess | Assumptions, Larridin via Ojstersek |
| "Deliberately skipped" | Names what the system will not do, next to where it applies | Non-goals, Larridin via Ojstersek |
| Configuration defaults, startup step six | States the obvious and explains the non-obvious | "Obvious to you is not obvious to the model," Kanitkar |
| Error handling | Pairs each condition with a response | Measurable tests, Ojstersek |
| What changes, what stays the same | Fences off code the agent must not touch | Boundaries, GitHub study via Osmani |
| Platform notes | Adds context only an experienced developer has | Domain knowledge and gotchas, Osmani |
| Testing | Defines done | Test plan, Larridin via Ojstersek |

### The Heading Outline To Copy

The outline of the original, to reuse as a skeleton for a brownfield spec:

```
# [Title: what changes, in one sentence]

## Motivation
## Architecture
### [Component or protocol]
### Configuration
### Startup Sequence
### Error Handling
## What Changes
## What Stays the Same
## Platform Compatibility
## Testing
```

`[Video: Owain Lewis, "How I Code With AI Agents (Spec-Driven Development)", 19 min: https://www.youtube.com/watch?v=RhaF4LVAVng]`

By this point you should have:

- A kickoff prompt that turns a one-paragraph brief into a reviewed spec.
- A check that makes the agent restate the task, list assumptions, and flag ambiguity.
- Larridin's six-section template and Osmani's Project Spec skeleton, ready to copy.
- A three-tier boundaries block for your rules file or constitution.
- Two ambiguous-versus-precise test pairs, a Given/When/Then skeleton, and a one-line conformance reference.
- A real, annotated brownfield spec to calibrate your own against.

