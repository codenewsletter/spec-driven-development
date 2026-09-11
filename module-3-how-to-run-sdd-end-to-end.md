# Module 3: How To Run SDD End To End

Two complete workflows, one adoption story, and the failure modes to watch for. By the end you can run a spec from idea to converged code with a tool, or with a folder convention and a checklist.

- [3.1 How To Get Started With GitHub Spec Kit](#31-how-to-get-started-with-github-spec-kit)
- [3.2 How To Use The Spike-First Workflow](#32-how-to-use-the-spike-first-workflow)
- [3.3 How Microsoft Adopted SDD Across Teams](#33-how-microsoft-adopted-sdd-across-teams)
- [3.4 The Common SDD Pitfalls And How To Avoid Them](#34-the-common-sdd-pitfalls-and-how-to-avoid-them)

---

## 3.1 How To Get Started With GitHub Spec Kit

### The Spec Drives The Plan, The Tasks, And The Code

[Spec Kit](https://github.com/github/spec-kit) makes the spec the center of the engineering process. You do not write a spec and set it aside; the spec drives the implementation, the checklists, and the task breakdown.

The agent writes the bulk of those artifacts. Your job is to steer, and above all to verify, says GitHub Principal Product Manager Den Delimarsky, who [introduced the open source toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/).

Each phase has a specific job, and you do not move to the next one until you validate the current one. At each checkpoint you ask three questions:

- Does the spec capture what you want to build?
- Does the plan account for real-world constraints?
- Did the agent miss an omission or an edge case?

Spec Kit works with more than 30 coding agents, from [GitHub Copilot](https://github.com/features/copilot) to [Claude Code](https://claude.com/claude-code) and [Gemini CLI](https://github.com/google-gemini/gemini-cli). The workflow is the same in each; only the command prefix changes.

### Nine Commands, And What You Check At Each Step

Spec Kit's [quick start guide](https://github.github.io/spec-kit/quickstart.html) runs the full loop in nine slash commands. Constitution runs once per project; every other command runs once per feature.

| Step | Command | What you give it | What it produces | Your check before the next step |
|---|---|---|---|---|
| 1 | `/speckit.constitution` | Your project principles, standards, and guardrails | The governing principles that every later step is evaluated against | The rules are true for this project, not invented to fill the template |
| 2 | `/speckit.specify` | A natural-language description of what to build and why | A feature directory under `specs/` with `spec.md`: requirements and user stories | The spec describes users, outcomes, and success, not the tech stack |
| 3 | `/speckit.clarify` | Optionally, a focus area | Targeted questions on underspecified areas, with your answers folded back into the spec | No open ambiguity remains before you plan |
| 4 | `/speckit.plan` | Your tech stack and architecture choices | `plan.md` and the design artifacts | The plan respects your architecture and constraints |
| 5 | `/speckit.checklist` | Nothing | A custom quality checklist, "unit tests for your requirements" | You mark an item done only when that requirement is complete, clear, and consistent |
| 6 | `/speckit.tasks` | Nothing | A dependency-ordered `tasks.md` | Each task is small enough to implement and test on its own |
| 7 | `/speckit.analyze` | Nothing | A read-only report of conflicts, gaps, and ambiguities across `spec.md`, `plan.md`, and `tasks.md` | You fix flagged issues at the source and re-run before you implement |
| 8 | `/speckit.implement` | Nothing, or one phase for a large feature | Code and tests, task by task in dependency order | You review focused changes, not a thousand-line dump |
| 9 | `/speckit.converge` | Nothing | An assessment of the code against spec, plan, and tasks, with remaining work appended to `tasks.md` | Repeat implement and converge until it reports Converged |

`[Infographic: the nine commands as a loop, constitution once at the top, the six core commands as the ring, clarify, checklist, and analyze as optional gates]`

Clarify, checklist, and analyze are optional gates. The quick start's short path for small features skips them and runs the five core commands; the full path for production runs all nine. Implement reads the checklist state before it starts, and asks you before it proceeds if any items are unchecked.

Delimarsky's example of a task: instead of "build authentication," you get "create a user registration endpoint that validates email format."

Microsoft Principal Software Engineer Apoorv Gupta [describes the same lifecycle](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/) in one line. Define intent, remove ambiguity, plan with constraints, implement with AI, and validate against the spec.

### Hands-On: Install Spec Kit And Build The Photo-Album Example

Goal: Take a new project from an empty folder to converged code with Spec Kit's own example prompts.

The commands and prompts below come from the [Spec Kit README](https://github.com/github/spec-kit) and its quick start guide. Spec Kit requires [uv](https://docs.astral.sh/uv/), Python 3.11 or later, and Git.

Steps:

1. Install the Specify CLI from PyPI.

```bash
uv tool install specify-cli
```

2. Initialize a project. The integration flag selects your coding agent; the README's example uses GitHub Copilot. Run `specify integration list` to see every option.

```bash
specify init my-project --integration copilot
cd my-project
```

3. Launch your coding agent in the project directory. Most agents expose the commands as `/speckit.*`; some skills-based agents use `$speckit-*` instead.

4. Establish the project principles. This runs once per project.

```text
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

5. Create the spec. Focus on the what and the why, not the tech stack.

```text
/speckit.specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

6. Resolve ambiguities before you plan. Answer the agent's questions; it folds your answers back into the spec. You can add a focus area after the command.

```text
/speckit.clarify
```

7. Provide your tech stack and architecture choices.

```text
/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

8. Generate the quality checklist and work through it. Mark an item only when the requirement itself is complete, clear, and consistent.

```text
/speckit.checklist
```

9. Break the plan into tasks.

```text
/speckit.tasks
```

10. Check consistency across the spec, the plan, and the tasks. Fix what it flags at the source, then re-run it.

```text
/speckit.analyze
```

11. Build it.

```text
/speckit.implement
```

12. Verify completeness. If converge appends tasks, run implement and converge again.

```text
/speckit.converge
```

Expected result: `/speckit.converge` reports Converged, and the `specs/` directory holds a `spec.md`, a `plan.md`, and a `tasks.md` that match the code.

`[Video: Den Delimarsky, "The ONLY guide you'll need for GitHub Spec Kit", 40 min: https://www.youtube.com/watch?v=a9eR1xsfvHg]`

### In An Existing Codebase, Spec Only The Change

You do not need to recreate an existing system from specifications before you use Spec Kit. Initialize in place, capture the rules that already matter, and run the workflow for the next bounded change. Those are the first four steps of the [Spec Kit guide for existing projects](https://github.github.io/spec-kit/guides/existing-projects.html).

First, commit or stash your work and create a branch, so every generated file shows up in a normal code review. Then initialize from the repository root.

```bash
specify init --here --force --integration <key>
```

The `--force` flag allows initialization in a non-empty directory. It may replace files at conflicting managed paths, but it does not delete the rest of your application.

Second, run the constitution command with principles that are already true for the repository. Use the README, the architecture decisions, the contribution guide, and the CI configuration as evidence, and do not invent standards to fill the template.

```text
/speckit.constitution Preserve public API compatibility. Follow the existing service boundaries. Every database migration must include a rollback plan. Run the repository's established unit and integration test suites.
```

Third, choose one bounded first change: a feature, a bug fix, or a modernization slice you can review on its own. Describe the outcome and the compatibility boundaries that must stay intact.

```text
/speckit.specify Add CSV export to the existing orders page. Preserve current filters and authorization behavior. Export only the rows visible to the signed-in user, and do not change the existing JSON API response.
```

The codebase stays the implementation context. The new `spec.md` defines the change you intend to make, not a retroactive specification of every existing behavior.

Fourth, continue through the normal loop. At the plan step, verify that the design reuses the existing architecture, dependencies, and test conventions.

Delimarsky calls feature work in an existing system [the place where SDD is most powerful](module-1-fundamentals.md#14-when-to-use-sdd-and-when-to-skip-it).

`[Video: Den Delimarsky, "Using GitHub Spec Kit with your EXISTING PROJECTS", 45 min: https://www.youtube.com/watch?v=SGHIQTsPzuY]`


---

## 3.2 How To Use The Spike-First Workflow

### Write The Spec With A Top Model, Build It With A Cheap One

Write the spec with a higher-tier model, then build it with a lower-tier one. A great spec gives instructions so clear that a cheaper model returns a very similar output.

Gregor Ojstersek, who writes the Engineering Leadership newsletter, [sees more companies use that workflow](https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development). Token costs rise, so infinite prompting is no longer a luxury you have.

Larridin, a platform that measures AI adoption and AI fluency, is his example of an AI-native team. The spec is almost perfect before implementation starts, and every engineer owns a feature end to end, from spec to working code.

The six steps below come from Ameya Kanitkar, CTO at Larridin. Two of them, the spec and the test plan, already have their own lessons, so this lesson covers the steps around them.

### Step 1: Spike The Risky Parts First

Before you write the spec, prove that the "risky" things work. A complete spec is impossible while you deal with unknowns, so Larridin creates a spike task to resolve them first.

A spike is not a small MVP. It is small, ugly, throwaway-quality work, just enough to answer the question "does this actually work?"

The purpose is to remove technical uncertainty that would otherwise contaminate the spec with different options. Kanitkar's examples:

- If the API you build has three edge cases, spike those.
- If the whole system depends on how fast your API is, spike the hot path and measure it.
- If you build a new view with many records, prove that the API returns them fast enough.

Larridin's own case was a model to measure AI Fluency. They wrote a spike to make sure the core logic worked and was token efficient. Once they were happy with the results, the rest of the design followed: queue, monitoring, database.

Stop when you have an answer, not when the code is pretty. If you worry about variable names, function names, or file structure, that is the sign you put too much thought into implementation details.

### Step 2: Turn The Spike Into A Reference Implementation

Once the spike works, do not throw it away. It is now your reference implementation, the thing you point the model to and say "I know this pattern works, because here it's working!"

Kanitkar calls this one of the most underrated parts of SDD. A working example beats a full page of spec, because the model sees the approach instead of a guess.

Larridin keeps every reference at a known location, `spec/spikes/reference/referenceName`.

Comment the parts that prove the approach, and the parts that are hardcoded, lack error handling, or are off point. Kanitkar's warning: a spike without comments can be as dangerous as no spike, because the model reproduces the wrong parts alongside the right ones.

### Step 3: Write The Spec, Then The Test Plan

With a commented reference in place, write the spec. It should be detailed enough to hand to a junior engineer or a small model.

Use AI to help, and make it [restate the task, list assumptions, and flag ambiguity](module-2-how-to-write-a-good-spec.md#21-start-with-a-brief-and-let-the-agent-draft-the-spec). Anything still open gets a new spike, or an update to the existing one.

The structure is [the six-section template](module-2-how-to-write-a-good-spec.md#22-the-six-section-spec-template), with the reference implementation as its fourth section. The test plan comes [before the implementation plan](module-2-how-to-write-a-good-spec.md#24-how-to-write-test-plans-the-agent-cannot-misread), and its list of named tests is the definition of done.

### Step 4: Create The Implementation Plan

The implementation plan is the boring part: a sequence of steps that turns the spec into code, file by file and function by function. Each step is defined so clearly that the model has no chance to go a different direction.

It is far more detailed than the spec: if the spec is around 800 lines, the plan is around 3,000.

Ask the model to create the plan from the spec and output it to a separate folder, such as `plans`. Then review it in detail.

If the plan makes a new architectural call, that is a signal the spec was not complete. Go back and update the spec; do not patch the plan with architecture details and leave the spec unchanged.

Kanitkar's reason: the whole point of the workflow is that decisions end in the spec phase. New decisions in the last phase can silently introduce problems.

### Step 5: Implement With A Small Model

Once you are happy with the plan, the implementation is the easy part. Tell the model to create the code from the implementation plan.

Any small model works; Kanitkar says even Haiku works great. How you ship is your choice: one PR, several PRs, or PRs the model creates under a convention you set.

`[Infographic: the six steps as a pipeline, spike to reference to spec to test plan to plan to code, with "top model" over the spec steps and "small model" over the build step]`

### Hands-On: The Six Steps As A Checklist

Goal: Run one feature through Larridin's workflow, from unknowns to code, with each artifact in a known place.

```
1. Spike the risky parts. Stop when you have an answer.
2. Promote the spike to a reference implementation at spec/spikes/reference/<name>.
   Comment what proves the approach and what is hardcoded or missing.
3. Write the spec with a top model. Make it restate, list assumptions, flag ambiguity.
   Spike or update the spike for anything still open.
4. Write the test plan before the implementation plan. Name each test, inputs, expected outputs.
5. Ask the model for an implementation plan in plans/. Review it.
   A new architectural call in the plan means the spec is incomplete: fix the spec.
6. Implement with a small model from the plan. Ship as one PR or several.
```

To see what steps 3 to 5 produce, read the public pair Ojstersek links as his example. Both come from Jesse Vincent's superpowers repo: the [Worktree Rototill design spec](https://github.com/obra/superpowers/blob/main/docs/superpowers/specs/2026-04-06-worktree-rototill-design.md) and its [implementation plan](https://github.com/obra/superpowers/blob/main/docs/superpowers/plans/2026-04-06-worktree-rototill.md).

The spec is about 340 lines. The plan is about 870, split into gated tasks with named files and checkbox steps. Its header names the spec it implements.

Expected result: a commented reference in the repo, a spec with a test plan, a much longer plan, and code from a small model.

Ojstersek's closing line: clear thinking and good judgment are the hard part, and once they are done, the code is easy.


---

## 3.3 How Microsoft Adopted SDD Across Teams

### SDD Paid Off Once It Became The Standard

SDD delivered the greatest value at Microsoft once it became a standard way of working, not an optional process that individuals could bypass. The adoption has to be deliberate, Microsoft Digital, the company's IT organization, finds in its [account of a year of AI-native engineering](https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/). It starts with [the hard lesson](module-1-fundamentals.md#12-why-prompting-breaks-as-codebases-grow): ad-hoc adoption made individuals faster and teams no faster.

"It's not something where you decide, today I woke up and I'll start using SDD," says Apoorv Gupta, Principal Software Engineer at Microsoft Digital. "It doesn't work like that. It's a mindset shift and a learning curve."

Microsoft serves as its own Customer Zero, so the process below is the one it offers customers as a model.

### The Six-Stage Workflow, Run On Spec Kit

Microsoft Digital's developers and PMs begin with specifications that capture business goals, user requirements, edge cases, and acceptance tests. The specs are version-controlled in the same repository as the code and updated as the project evolves.

Before any spec, the team agrees on [a constitution](module-1-fundamentals.md#13-spec-constitution-or-prompt-what-goes-where). Then the teams run six stages on [Spec Kit](https://github.com/github/spec-kit).

`[Infographic: the six stages as a pipeline with the constitution as a bar above all of them]`

Each stage builds on the spec, so teams trace implementation decisions back to business requirements. Agents enhance the spec and generate code, tests, and documentation from it; engineers validate intent, review outputs, and refine requirements.

"Effective SDD adoption relies on well-scoped specifications," says Ajeya Kumar, Principal Software Engineer at Microsoft Digital. Smaller, focused specs produce outputs that are easier to review. Kumar calls the split of large requirements into multiple specs a key practice for quality and for intent.

### The Five Pillars Behind The Value

`[Infographic: the five pillars as five columns under one roof labeled "value of SDD"]`

Microsoft names five pillars that drive the value of SDD, from its own experience:

- **Spec as the source of truth.** The spec is the single authoritative reference for all stakeholders.
- **Living, executable artifacts.** Specs evolve with the project, stay synchronized with the code and tests, and are co-authored by the stakeholders.
- **AI-assisted automation.** Agents generate, test, and validate code from the spec.
- **Human validation and collaboration.** Human expertise reviews specs, refines requirements, and validates outcomes.
- **Predictability and measurability.** Teams track progress, measure outcomes, and improve predictability.

### How Roles Changed: Leaders, Developers, PMs, Architects

The biggest change at Microsoft was behavioral: specifications stopped being documents that supported development and became the artifact that drove it. Roles coupled to the old lifecycle had to change.

`[Infographic: four role cards, leaders, developers, PMs, architects, one line each on what changed]`

**Leadership.** Leaders reward clarity, alignment, and collaboration before implementation begins, and they drive adoption, since SDD only paid off as a standard.

**Developers.** The first step is now a complete understanding of the problem, with success defined, before any code. "As developers, we get excited and want to jump directly into coding," says Mridul Verma, Senior Software Engineer at Microsoft Digital. "Changing that habit was really tricky."

The developer must make sure the agent fully understands the task before the coding starts. "SDD makes you clarify and refine your thoughts first for agents, not for yourself," says Sudhakar Sadasivuni, Principal Group Engineering Manager at Microsoft Digital. "This is agent-first solutioning, not human-first solutioning."

Engineers now spend more time on requirements, edge cases, plan evaluation, and validation of AI output, and less on every line of code.

**Program and product managers.** PMs keep stakeholder management, prioritization, and roadmap planning. What changed is ownership.

"In spec-driven development, PMs become the owners of the spec," Gupta says. "Everything starts with the spec, so they become the starting point for the entire system. If the specs are right, then everything falls into place."

PMs define success criteria, resolve ambiguities, document business requirements, and keep priorities visible through implementation. Gopal Panigrahy, Principal Product Manager at Microsoft Digital, describes the payoff. You move from an idea to a prototype, show it to customers and leaders, and get feedback much faster.

**Architects.** Architects own the constitution, so architectural decisions come early and teams find issues before implementation rather than in review.

### Outcomes From Three Projects

Gupta reports three projects in his [Microsoft for Developers post](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/), with one summary: spec quality equals output quality.

- **Repeated onboarding turned into a pattern.** In a brownfield project, each new asset type needed the same UI, API, and test changes. The team captured the pattern in parameterized specs and documented only the deviations per asset. Onboarding fell from 2 to 3 weeks to a few days.
- **A multi-service platform aligned before the build.** A large greenfield project covered attendees, facilities, security, vendors, logistics, and compliance. The constitution, specs, and plans served as the source of truth. The team improved cross-service consistency, made constraints explicit, and reduced churn as implementation scaled.
- **A prototype became a product faster.** In another brownfield project, the team moved a React and TypeScript prototype to a working product. The product had multiple agents, health monitoring, and admin dashboards. Custom prompts and quality-gate scripts made the process repeatable across contributors.

### Hands-On: The Adoption Playbook And Microsoft's Five Takeaways

Goal: Start SDD in your organization with one pilot, and check the pilot against the guidelines Microsoft learned.

Gupta's four-step playbook, for teams that do not need to adopt the full lifecycle at once:

```
1. Pilot: start with one feature or workflow where alignment problems are visible.
2. Formalize: write a lightweight spec with scenarios, constraints, and acceptance criteria.
3. Iterate: use AI to generate implementation artifacts from that shared context.
4. Refine and scale: review the output against the spec and refine the workflow as you learn.

Keep the process lightweight at first. Treat specs as living artifacts.
Avoid over-specifying too early. Expand the workflow only where it adds clear value.
```

Microsoft Digital's five key takeaways for an organization that considers SDD:

```
1. Make the specification the source of truth. A living artifact, not static documentation.
2. Resolve ambiguity before implementation begins. Requirements, constraints, edge cases, success criteria.
3. Assign clear ownership. PMs, architects, developers, and designers all maintain the spec.
4. Establish architectural guardrails early. Governance, security, and design principles before code.
5. Use AI to accelerate execution, not replace judgment. Humans validate outputs and alignment with intent.
```

Expected result: one pilot feature with a lightweight spec, a review of its output against that spec, and a decision on where to expand next.


---

## 3.4 The Common SDD Pitfalls And How To Avoid Them

### These Pitfalls Come From Real Use, Not Theory

Every SDD tool and workflow shares the same failure modes, and the sources below found them in use, not in theory.

Birgitta Böckeler, Distinguished Engineer at Thoughtworks, [tried three SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) on real tasks. Anthropic engineer Addy Osmani [collected the anti-patterns](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents) from GitHub's study of agent files and from Simon Willison.

Liu Shangqi, Technology Director for APAC at Thoughtworks, [names the deterministic backstop](https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices). Matt Pocock, author of the AI Hero skills, [says when the spec should die](https://www.aihero.dev/skills-to-spec).

### Böckeler's Four Questions After Testing Three Tools

**One workflow to fit all sizes?** Two of the tools provide one opinionated workflow each, Spec Kit among them. Böckeler is sure that neither suits the majority of real coding problems. [The bug fix that became 16 acceptance criteria](module-1-fundamentals.md#14-when-to-use-sdd-and-when-to-skip-it) is her example.

An effective SDD tool would at least offer a few core workflows for different sizes and types of change.

**Reviewing markdown over reviewing code?** Spec Kit created a lot of markdown files for her to review. They repeated each other and the code that already existed, and some contained code.

"To be honest, I'd rather review code than all these markdown files," she writes. An effective tool would need a very good spec review experience.

**False sense of control?** Even with all the files, templates, prompts, and checklists, the agent frequently did not follow all the instructions. Larger context windows do not mean the AI picks up everything in them.

Her example: Spec Kit's research step described the existing classes her feature built on. The agent then took those descriptions as a new specification and generated the classes all over again, as duplicates. She also saw the opposite, where the agent went overboard because it followed one constitution article too eagerly.

Her fix is the old one: small, iterative steps keep you in control, so she is skeptical of verbose up-front spec design. Small work packages almost seem counter to the idea of SDD, and an effective tool would have to cater to them anyway.

**Are we making it worse?** Her closing worry is that some tools feed agents our existing workflows too literally, and amplify review overload and hallucination. The German word she reaches for is "Verschlimmbesserung": to make something worse in the attempt to make it better.

### Osmani's Six Anti-Patterns

Osmani lists the mistakes that derail even well-intentioned spec-driven workflows, in this order.

**Vague prompts.** "Build me something cool" or "Make it work better" gives the agent nothing to anchor on. Be specific about inputs, outputs, and constraints; [the vague and specific prompt pair](module-1-fundamentals.md#12-why-prompting-breaks-as-codebases-grow) shows the difference.

**Overlong contexts without summarization.** Dump 50 pages of documentation into a prompt and the model rarely figures it out. Use hierarchical summaries or retrieval to surface only what is relevant, because context length is not a substitute for context quality.

**Skipping human review.** Willison's personal rule: "I won't commit code I couldn't explain to someone else." Code that passes tests is not therefore correct, secure, or maintainable. AI-generated code can look solid and collapse under edge cases you did not test, like a house of cards.

**Conflating vibe coding with production engineering.** Rapid prototyping with AI is great for exploration and throwaway projects. If you ship that code to production without rigorous specs, tests, and review, you ask for trouble, so know which mode you are in.

**Ignoring the "lethal trifecta".** Willison warns of three properties that make agents dangerous, and your spec and review process must account for all three:

- Speed: they work faster than you can review.
- Non-determinism: the same input gives different outputs.
- Cost: it encourages corner-cutting on verification.

**Missing the six core areas.** If the spec skips commands, testing, project structure, code style, git workflow, or boundaries, the agent likely lacks something it needs. Use [the six-area list](module-2-how-to-write-a-good-spec.md#22-the-six-section-spec-template) as a sanity check before handoff.

`[Checklist candidate: the six anti-patterns as a pre-handoff check, one line each]`

### Code From A Spec Still Needs CI To Catch Drift

Code generation from a spec is not deterministic, so spec drift and hallucination are inherently difficult to avoid. Liu's conclusion: teams still need highly deterministic CI/CD practices to ensure software quality and safeguard their architectures.

Böckeler saw the same thing when she generated code several times from one spec with the third tool she tried, and got different results. She iterated the spec to make it more specific, which reminded her how hard it is to write an unambiguous and complete specification.

Liu adds a second caution. Over-formalized specs can cause unnecessary trouble and slow down change and feedback cycles, the same problem as the early stages of waterfall.

### The Spec Goes Stale, So Keep Lessons Elsewhere

Nothing keeps the spec in sync once implementation starts. Pocock's view: the spec is a snapshot of what you knew at that moment, and it goes stale the first time implementation teaches you something.

He treats it as throwaway once the work ships. The artifacts meant to outlive it are your CONTEXT.md and your ADRs. If something learned during implementation deserves to last, it belongs there, not in an edited spec.

Spec Kit and Microsoft take the other view, where [the spec is a living artifact](#in-an-existing-codebase-spec-only-the-change) maintained alongside the code. Böckeler notes that Spec Kit creates a branch per spec. To her that suggests a spec that lives for the lifetime of a change request, not of a feature.

### Hands-On: Osmani's Self-Verification Prompt

Goal: Make the agent audit its own output against the spec before you review it.

Steps:

1. Append Osmani's instruction to the implementation prompt.

```text
After implementing, compare the result with the spec and confirm all requirements are met. List any items that are not addressed.
```

2. For a single function or task, use his shorter form at the end of the prompt.

```text
(After writing the function, review the above requirements list and ensure each is satisfied, marking any missing ones.)
```

Expected result: the code, followed by a short checklist of each requirement and whether the code meets it. Osmani's caveat: it is not foolproof, but it catches omissions before you even run tests.

By this point you should have:

- The definition of spec-driven development, its three levels, and each source's rule for when to use it and when to skip it.
- A six-section spec template, a project spec skeleton, a boundaries block, and the rules for test plans the agent cannot misread.
- A real spec, reverse engineered section by section, with its heading outline to copy.
- The Spec Kit loop, with its nine commands, the gate checks, and the brownfield steps.
- The spike-first workflow as a six-step checklist, with the reference implementation convention.
- Microsoft's adoption playbook and five takeaways for a team or an organization.
- The pitfalls from four sources, and a self-verification prompt to catch omissions before review.
