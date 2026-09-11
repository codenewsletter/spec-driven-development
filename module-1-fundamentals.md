# Module 1: Fundamentals Of Spec-Driven Development

This module explains what spec-driven development is, why it appeared, and how to tell when it will pay off. No tooling yet; that starts in the lessons on how to run SDD end to end.

- [1.1 What Spec-Driven Development Is, And Its Three Levels](#11-what-spec-driven-development-is-and-its-three-levels)
- [1.2 Why Prompting Breaks As Codebases Grow](#12-why-prompting-breaks-as-codebases-grow)
- [1.3 Spec, Constitution, Or Prompt: What Goes Where](#13-spec-constitution-or-prompt-what-goes-where)
- [1.4 When To Use SDD, And When To Skip It](#14-when-to-use-sdd-and-when-to-skip-it)

---

## 1.1 What Spec-Driven Development Is, And Its Three Levels

### Write The Spec Before The Code

Spec-driven development (SDD) means you write a spec before you write code with AI, and the spec is then the source of truth for both. That is Thoughtworks Distinguished Engineer Birgitta Böckeler's working definition, after she [tested three tools that call themselves SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html).

GitHub Principal Product Manager Den Delimarsky gives [the plainest version](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/): you do not code first and document later; you start with a spec.

The spec is a contract for how your code should behave, and your tools and agents use it to generate, test, and validate code. To maintain software is to evolve specifications, and code becomes "the last-mile approach."

### What A Spec Is

A spec is a structured, behavior-oriented artifact, written in natural language, that expresses software functionality and guides AI coding agents. Each variant of SDD decides the spec's structure, its level of detail, and where the files sit in the project.

The closest definition in common use compares a spec to a Product Requirements Document (PRD). Thoughtworks [argues that a spec is more](https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices): it defines the external behavior of the software, not only the business requirements.

A spec is not a detailed prompt either. [The lesson on specs, constitutions, and prompts](#13-spec-constitution-or-prompt-what-goes-where) draws both lines.

### The Three Levels: Spec-First, Spec-Anchored, Spec-As-Source

Böckeler found that tools and definitions use the term at three different levels:

1. **Spec-first.** You write a well thought-out spec first, then use it in the AI-assisted workflow for the task at hand.
2. **Spec-anchored.** You keep the spec after the task is complete, and use it to evolve and maintain that feature.
3. **Spec-as-source.** The spec is the main source file over time. The human edits only the spec and never touches the code.

`[Infographic: the three levels as a ladder, spec-first to spec-anchored to spec-as-source, with what the human edits at each rung]`

Every SDD approach she found is spec-first. Not all aim higher, and the authors often leave the strategy to maintain the spec vague.

Her test of GitHub's [Spec Kit](https://github.com/github/spec-kit) shows the gap. GitHub describes specs as living artifacts, but Spec Kit creates a branch for every spec. To Böckeler that makes it spec-first: the spec lives for one change request, not for the life of a feature.

Thoughtworks describes the same split as an industry disagreement. At the radical end, code is a byproduct and the spec is the sole source of truth that needs maintenance.

At the old-school end, the spec drives code generation the way tests do in test-driven development. The code remains the source of truth you maintain.

Liu Shangqi, Technology Director for APAC at Thoughtworks, puts himself in the second camp.

`[Video: Thoughtworks Technology Podcast, "What is spec-driven development?" with Böckeler and Laura Tacho, 46 min: https://www.youtube.com/watch?v=YV4Ii6bJ0OQ]`

---

## 1.2 Why Prompting Breaks As Codebases Grow

### Agents Are Literal-Minded Pair Programmers, Not Search Engines

The problem is not the agent's coding ability. It is our approach: we treat coding agents like search engines when we should treat them like literal-minded pair programmers.

That diagnosis comes from GitHub Principal Product Manager Den Delimarsky in [the post that introduced Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/). Agents excel at pattern recognition, but they still need unambiguous instructions.

The symptoms are familiar. You describe your goal, you get a block of code back, and it looks right but does not quite work.

A vague prompt like "add photo sharing to my app" forces the model to guess at thousands of unstated requirements. Some guesses are wrong, and you find out deep into the implementation.

### Small Guesses Add Up In Big Codebases

For two years, teams shipped AI code the same way. You prompt the agent, it fills the gaps with a guess, and you clean up the rest. That worked for small tasks and failed as codebases grew.

The bigger the system, the more of what you want lives in details you never typed. The issue is no longer how fast the agent writes code; it is whether anyone wrote down what the code was supposed to do.

Teams ship software that works but misses the original intent, because meaning leaks as ideas move through the lifecycle. Microsoft Principal Software Engineer Apoorv Gupta [names the four leaks](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/).

`[Infographic: the four handoffs where intent leaks, needs to requirements to design to implementation to release]`

Without a shared artifact that preserves intent, every handoff becomes an interpretation step. AI can accelerate those steps, but it cannot correct ambiguity that was never resolved.

When requirements, constraints, and edge cases live only in prompts, teams get fast output without a durable source of truth. Microsoft lists the results: architectural drift, code drift, inconsistent implementations, harder reviews, and rework.

### Faster Developers Did Not Make Faster Teams

Individual developers got faster and the gains stopped there, Microsoft Digital, the company's IT organization, [found after a year of ad-hoc AI adoption](https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/).

"We quickly identified that improving the individual productivity of a developer was not resulting in a boost to team productivity," says Sudhakar Sadasivuni, Principal Group Engineering Manager at Microsoft Digital. "That was our hard lesson."

The problem was the process around the tools, not the tools. Human handoffs shaped the traditional software development lifecycle, and every handoff introduces a gap in intent.

Teams that cannot consistently communicate intent discover that more coding velocity produces more variability and more rework.

Mridul Verma, Senior Software Engineer at Microsoft Digital, frames the fix as velocity and vector. Velocity is how fast your development moves; vector is the direction you move in.

"Speed without direction is just expensive chaos, and we learned that the hard way through vibe coding," Verma says. "After burning our hands on those traps, we realized that SDD gives you both velocity and vector."

Vignesh Vijayaraghavan, Senior Software Engineer at Microsoft Digital, puts the goal in one line: "In the AI era, the best dev teams aren't the ones that generate the most code. It's about how they're best able to preserve intent."

### The Vague Prompt And The Specific Prompt, Side By Side

Most agent files fail because they are too vague, the stark divide GitHub found in its study of more than 2,500 agent configuration files.

Anthropic engineer Addy Osmani [draws the rule from it](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents): be specific about inputs, outputs, and constraints. A vague prompt gives the agent nothing to anchor on.

```
Does not work:
You are a helpful coding assistant.

Works:
You are a test engineer who writes tests for React components,
follows these examples, and never modifies source code.
```

`[Video: IBM Developer, "Agentic Coding + Planning: Why Specs Matter More Than Code" with Bri Kopecki, 14 min: https://www.youtube.com/watch?v=o7AzbObl8Tk]`

---

## 1.3 Spec, Constitution, Or Prompt: What Goes Where

### The Spec Covers One Task, The Constitution Covers The Codebase

A spec matters only to the tasks that create or change one piece of functionality. The general context for a codebase, such as rules files and high-level descriptions of the product and the code, applies in every AI coding session.

Böckeler [draws that line](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) and borrows a name for the general context from the tools: the memory bank.

Spec Kit calls its memory bank the constitution. It holds the high-level principles that are "immutable" and apply to every change; Böckeler describes it as a very powerful rules file.

Microsoft [defines what goes in it](https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/): a shared set of architectural principles, governance requirements, security standards, and development limitations that everyone adheres to.

The team agrees on the constitution before any spec, as a team-wide exercise, so employees and agents work from the same facts.

### A Long Prompt Is Not A Spec

Böckeler warns that people already use "spec" as a synonym for "detailed prompt."

Thoughtworks [sets the bar](https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices): a spec explicitly defines the external behavior of the target software. That means input and output mappings, preconditions and postconditions, invariants, constraints, interface types, integration contracts, and sequential logic or state machines.

Thoughtworks puts technical requirements in a third place: architectural style and constraints go in rules files such as [AGENTS.md](https://agents.md/). The agent then generates code from the finalized spec against those rules.

### The Spec Holds The What, The Plan Holds The How

The [Spec Kit repo](https://github.com/github/spec-kit) separates the three artifacts by command. The constitution step creates or updates the project's governing principles and development guidelines.

The specify step focuses on the what and the why, not the tech stack. The plan step is where the stack, architecture, and constraints go.

Its photo-album example shows the split in two lines. The spec describes albums grouped by date, re-organized by drag and drop, never nested, with photos previewed in a tile-like interface.

The plan says the application uses Vite with a minimal number of libraries, vanilla HTML, CSS, and JavaScript, and a local SQLite database for metadata.

### A Constitution Prompt To Copy

`[Infographic: three nested scopes, constitution around the codebase, spec around one feature, prompt around one request]`

Spec Kit's example prompt for the constitution step, to run first:

```
/speckit.constitution Create principles focused on code quality,
testing standards, user experience consistency, and performance
requirements
```

The lesson on how to get started with Spec Kit runs the full loop from this step onward.

---

## 1.4 When To Use SDD, And When To Skip It

### For A Small Change, Prompt And Review

For a small change, like a refactor of one file or a small adjustment to a feature, prompt the agent and review the code. SDD is overhead there, says Gregor Ojstersek, who writes the Engineering Leadership newsletter, in [his account of how Larridin does SDD](https://newsletter.eng-leadership.com/p/how-to-do-spec-driven-development).

On a bigger project, especially one of uncertain feasibility, the spec saves a lot of time on rewrites and reviews of bad AI-generated code. Decisions on the fly are usually worse than decisions made beforehand.

Microsoft [reached the same conclusion across its teams](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/): not every change needs the full lifecycle, so adoption should be right-sized.

### If The Work Fits One Session, Skip The Spec

Reach for a spec when the build is too big for one agent session and has to survive a split across several. Matt Pocock, who runs AI Hero, calls that [the whole trigger](https://www.aihero.dev/skills-to-spec).

The spec exists because context windows end; it is what survives when you clear the conversation. On a single-session change it buys you nothing and adds a synthesis step where the model can drift.

### The Bug Fix That Became 16 Acceptance Criteria

Böckeler asked a spec tool to fix a small bug, and [the workflow turned it into 4 user stories with 16 acceptance criteria](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html). Her verdict: a sledgehammer to crack a nut.

One generated user story read: "As a developer, I want the transformation function to handle edge cases gracefully, so that the system remains robust when new category formats are introduced."

Her second test was a 3 to 5 point feature that built on a lot of existing code. The steps and the markdown files felt like overkill, and she never finished.

In the same time, she believes, plain AI-assisted coding would ship the feature and leave her more in control.

### Three Places Where SDD Pays Off

GitHub [names three scenarios](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) where the approach works especially well:

1. **Greenfield, zero to one.** A small amount of upfront work on a spec and a plan makes the agent build what you intend. Without it you get a generic solution from common patterns.
2. **Feature work in existing systems, N to N+1.** This is where SDD is most powerful. The spec forces clarity on how the feature interacts with the existing system. The plan encodes the architectural constraints so the new code feels native.
3. **Legacy modernization.** The original intent is often lost to time. The spec captures the essential business logic, the plan designs a fresh architecture, and the agent rebuilds without inherited technical debt.

The core benefit, in GitHub's words, is to separate the stable "what" from the flexible "how."

### Four Rules For When To Use SDD, Side By Side

`[Infographic: a decision flow, small change to prompt and review, fits one session to implement, spans sessions or uncertain feasibility to write the spec]`

| Source | Use SDD when | Skip it when |
|---|---|---|
| Ojstersek, Larridin | A bigger project, especially one of uncertain feasibility | A small refactor or a small feature adjustment: prompt, then review |
| Pocock, AI Hero | The work spans several agent sessions | The work is decided and fits one context window |
| Böckeler, Thoughtworks | Many situations; she writes some form of spec first herself | A small bug fix or a 3 to 5 point feature turns into a pile of markdown |
| GitHub | Greenfield, a feature in an existing system, or a legacy rebuild | Quick prototypes where vibe coding is enough |

By this point you should have:

- A working definition of spec-driven development, and Böckeler's three levels to place any tool or workflow.
- The reason prompting alone breaks as codebases grow: agents guess at what you never typed, and guesses compound across handoffs.
- A clear split between the constitution, the spec, and the prompt, and Spec Kit's constitution prompt to start with.
- Four use-or-skip rules from four sources, so you can tell a spec-sized task from a prompt-sized one.

