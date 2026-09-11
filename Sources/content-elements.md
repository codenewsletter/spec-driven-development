# SDD Guide — Content Elements (from source read-through)

Each element: what it is, why it's high value, and which source(s) carry it.

## A. Foundations (the "why" and "what")

1. **Definition, and the three maturity levels** — Spec-first / Spec-anchored / Spec-as-source. Cleanest framing in the sources; lets readers place any tool or workflow. (Böckeler)
2. **Spec vs. memory bank vs. prompt** — a spec is task-scoped; rules files / constitution / CLAUDE.md / AGENTS.md are codebase-scoped; a "detailed prompt" is not a spec. (Böckeler, Thoughtworks, Osmani)
3. **Why prompting breaks at scale: "guesses compound"** — vague prompt = thousands of unstated requirements; "31% more PRs merge with no review"; translation loss at four handoffs. (GitHub blog, Gupta, The Code Jun 16)
4. **"Vagueness got priced"** — with a human reader a fuzzy sentence costs a hallway chat, with an agent it's a wrong build billed in tokens. Strong narrative hook for the intro. (Clawdtalk)
5. **Velocity and vector** — Microsoft's framing of why SDD beats vibe coding; "preserve intent, not generate the most code." (Inside Track)
6. **Is this waterfall again?** — the objection and the rebuttal (short feedback loops, not long ones; MDD parallel and its lessons). (Thoughtworks, Böckeler)
7. **Token economics** — write the spec with a high-tier model, implement with a low-tier one ("even Haiku works"). (Ojstersek)

## B. Workflows (step-by-step, the core of the guide)

8. **The Spec Kit loop** — Constitution → Specify → Clarify → Plan → Tasks → Analyze → Implement → Converge, with what each gate is for and the human-verify checkpoint at each. (Spec Kit repo, GitHub blog, Gupta)
9. **The Larridin workflow (spike-first)** — Spike → promote spike to reference implementation → write spec → test plan BEFORE implementation plan → implementation plan (~3k lines for an 800-line spec) → implement with a small model. Most concrete practitioner workflow in the sources. (Ojstersek)
10. **Osmani's five principles** — start high-level and let AI draft; structure like a PRD/SRS; modular prompts not one giant prompt; self-checks + boundaries; test/iterate/evolve. (Osmani)
11. **Plan Mode as the spec-writing sandbox** — read-only exploration, agent interviews you, refine until no room for misinterpretation, then exit. (Osmani)
12. **Decision-first workflows** — grill-with-docs → /to-spec → /to-tickets → implement → code-review; "the spec is a decision record, not a place decisions get made." (Pocock)
13. **Microsoft's 4-step adoption playbook** — Pilot → Formalize → Iterate → Refine and scale; "right-size adoption." (Gupta)
14. **Kiro's Requirements → Design → Tasks** as the lightweight alternative; Tessl as spec-as-source. Tool comparison table. (Böckeler)

## C. Templates and checklists (copy-paste value)

15. **Six-section spec template (Larridin)** — Problem statement / Non-goals / Assumptions / Reference implementation / Architecture / Test plan. "Write the smallest spec that unambiguously specifies the system." (Ojstersek, The Code Jul 29)
16. **Six core areas for agent config (GitHub 2,500-file study)** — Commands / Testing / Project structure / Code style / Git workflow / Boundaries. Plus Osmani's markdown skeleton. (Osmani)
17. **Three-tier boundaries** — ✅ Always / ⚠️ Ask first / 🚫 Never; "never commit secrets" is the most common useful constraint. (Osmani)
18. **Constitution template** — architectural principles, governance, security standards, dev constraints; a team exercise, not an individual one. Spec Kit example prompt. (Inside Track, Spec Kit repo, The Code Jun 16)
19. **Ambiguous vs. precise test-plan lines** — "handles large inputs gracefully" → "processes 10k rows in under 2s with memory under 500MB"; "fails safely" → "returns 400 with error code X when customer_id missing." (Ojstersek)
20. **Given/When/Then acceptance criteria + user stories** — BDD carries over; ubiquitous language; critical path not every case. (Thoughtworks, Böckeler on Kiro)
21. **What a spec should technically define** — I/O mappings, pre/postconditions, invariants, interface types, integration contracts, state machines. (Thoughtworks)
22. **Self-verification prompt snippets** — "after implementing, compare with the spec and list unmet items"; LLM-as-judge; conformance suites (YAML). (Osmani)
23. **Spec Kit quick-start commands** — uv install, specify init, example /speckit.* prompts, directory layout, extensions (bug, assess), presets, bundles. (Spec Kit repo)
24. **Extended TOC / spec summary technique** for large specs; split into SPEC_backend / SPEC_frontend; fresh session per major feature. (Osmani)

## D. Real examples and case studies

25. **Annotated real spec: superpowers zero-dep brainstorm server** — motivation with honest risk assessment, explicit "deliberately skipped" scope, config with defaults, error handling, "what stays the same," platform notes, testing strategy. Ideal for a "good spec, section by section" teardown. (Link 2)
26. **Microsoft Digital case study** — individual productivity didn't become team productivity; six-stage workflow; role changes for leaders / devs / PMs / architects; "PMs become owners of the spec." (Inside Track)
27. **Three Microsoft project examples** — parameterized specs cut asset onboarding from 2–3 weeks to days; multi-service greenfield platform; prototype → product with quality-gate scripts. (Gupta)
28. **Larridin "AI Fluency" spike example** — spike core logic first, rest of design followed. (Ojstersek)
29. **Böckeler's failure stories** — Kiro turned a bug fix into 4 user stories / 16 acceptance criteria; spec-kit agent re-generated existing classes as duplicates; "I'd rather review code than all these markdown files." Essential honesty section. (Böckeler, The Code Jun 16)
30. **InfoQ order-service walkthrough** — one YAML spec flowing through Specification → Generation → Artifact → Validation → Runtime layers. (InfoQ)

## E. Frameworks and mental models

31. **When to use SDD, when not to** — decision table: small fix → prompt and review; decided + fits one context window → skip spec; decided + multi-session → spec; risky/unknown → spike first. (Ojstersek, Pocock, Gupta, Böckeler)
32. **Three places SDD shines** — greenfield, N-to-N+1 feature work (most powerful), legacy modernization. (GitHub blog, Spec Kit repo)
33. **Functional vs. technical spec separation** — the aspiration and why it's hard in practice. (Böckeler, Thoughtworks)
34. **Five pillars of SDD value** — source of truth, living artifacts, AI automation, human validation, predictability. (Inside Track)
35. **Five-layer execution model + architectural inversion table** — classical vs. SDD; drift detection; SpecOps; bounded autonomy (breaking schema changes need human approval). For the "advanced / enterprise" section. (InfoQ)
36. **Spec lifecycle: snapshot or living?** — Pocock: throwaway once shipped, durable learnings go to CONTEXT.md/ADRs; GitHub/Microsoft: living artifact; Spec Kit branches-per-spec tension. Present as an open choice. (Pocock, Böckeler, GitHub)
37. **"Decisions stop in the spec phase"** — if the implementation plan makes a new architectural call, the spec was incomplete; go back and fix the spec. (Ojstersek)
38. **Seams before prose** — agree the test seams (as few as possible) before writing the spec. (Pocock)
39. **SDD + context engineering** — spec as compressed context; Context7/MCP; AGENTS.md as system prompt; subagents per spec slice; single vs. multi-agent table. (Thoughtworks, Osmani)

## F. Pitfalls and honest caveats

40. **Anti-patterns list** — vague prompts, overlong context without summarization, skipping human review ("won't commit code I couldn't explain"), conflating vibe coding with engineering, the lethal trifecta (speed, non-determinism, cost). (Osmani)
41. **False sense of control** — agents ignore or over-follow checklists; larger context ≠ better adherence. (Böckeler)
42. **Non-determinism and spec drift** — same spec, different code; still need deterministic CI/CD. (Thoughtworks, Böckeler on Tessl)
43. **Cost objection** — "is SDD efficient under usage-based billing?" and the "human gates are a hindrance" pushback with the risk/compliance rebuttal. (Gupta comments)
44. **Who is the target user?** — developer doing PM work; PM as spec owner. (Böckeler, Inside Track)

## G. Tooling landscape (reference section)

45. Spec Kit (GitHub), Kiro (Amazon), Tessl, OpenSpec + Ralph loop, Pocock's skills (/to-spec, /to-tickets, grill-with-docs), Osmani's agent-skills (/spec, interview-me, idea-refine), Claude Code Plan Mode, JetBrains SDD course, Oracle markdown-file demo. (multiple)

## Gaps to fill from outside these sources
- The Larridin full spec + implementation plan examples (linked but not captured)
- A worked brownfield example end-to-end (all tutorials are greenfield; Böckeler flags this)
- Any quantitative outcome data beyond Microsoft's 2–3 weeks → days anecdote
