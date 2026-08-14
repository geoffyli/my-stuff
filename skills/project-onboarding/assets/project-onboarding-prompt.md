# Project Onboarding — Standalone Agent Prompt

Comprehensively investigate the current software project and create one concise, evidence-backed Markdown onboarding guide for a new developer.

Your goal is not to summarize every file. Build a trustworthy orientation map that helps the developer:

- explain what the project does and why it exists
- identify its major components and boundaries
- run, test, and debug it, or understand verified blockers
- trace at least one representative business flow end to end
- locate the main change points for common work
- recognize important dependencies, risks, and operational constraints
- progress toward a first safe contribution

## Defaults

- Treat the current repository or project workspace as the target.
- Assume the audience is a general software developer with no project-specific knowledge unless the user specifies another role, responsibility, or experience level.
- Use repository content as the baseline evidence.
- Inspect external documents or connected systems only when the user supplies or explicitly authorizes them.
- Start immediately unless ambiguity would materially change the result, such as several unrelated projects or a monorepo with no discernible focal product.
- Write `PROJECT_ONBOARDING.md` at the repository root unless the user specifies another output path.
- Treat that onboarding document as the only permitted write. Never overwrite an existing file without explicit permission.
- Keep the investigation read-only. Use safe, non-destructive inspection or verification commands when helpful, but do not change tracked project content, install global software, modify infrastructure, invoke production behavior, or invent credentials.

## Investigation expectations

Use your judgment to choose the best exploration strategy. Optimize for systematic coverage and trustworthy understanding rather than mechanically reading every file.

For a small project, near-exhaustive inspection may be efficient. For a large project, map the whole system and deep-dive into representative components and flows. Inspect relevant sources such as:

- README files, project documentation, decision records, and supplied external context
- manifests, dependency definitions, build systems, and workspace configuration
- entry points, module boundaries, public interfaces, and core domain code
- data models, migrations, persistence, events, APIs, and external integrations
- tests, fixtures, local development setup, and debugging configuration
- CI/CD, deployment, infrastructure, observability, support, and ownership artifacts
- version-control history that clarifies evolution, active areas, or non-obvious decisions

Use version-control history selectively. Do not rank contributors, infer performance from activity counts, or turn the guide into commit analytics.

For a monorepo, explain the repository-wide landscape first and then deep-dive into components needed for representative business and developer flows. Do not create a mini-guide for every package unless requested. Ask for scope only when several unrelated products exist and no reasonable focal point can be inferred.

Establish both the business and technical picture:

- Identify the purpose, users or consumers, value, important workflows, domain entities, terminology, and consequential business rules.
- Map components, boundaries, runtime topology, data movement, integrations, and representative end-to-end flows.
- Determine how a developer sets up, runs, tests, debugs, changes, delivers, observes, and supports the project where evidence allows.
- Distinguish current behavior from business intent, historical rationale, and planned work.
- Detect conflicts between code, configuration, tests, documentation, tickets, and other sources. Report conflicts rather than silently selecting a convenient narrative.

Classify consequential conclusions:

- **Verified** — directly supported by inspected evidence.
- **Inferred** — strongly suggested but not explicitly established.
- **Unknown** — important information that could not be established.
- **Ask the team** — a targeted question whose answer would close a meaningful gap.

Anchor every major section to compact evidence. Prefer repository-relative paths plus a class, function, configuration key, heading, or other stable locator. For external sources, cite the title and URL or supplied identifier. For version history, cite a commit identifier when it materially supports the conclusion. Do not clutter every sentence with citations.

## Required output structure

Use these six top-level sections by default. Merge, omit, or adapt subsections when the project warrants it, but preserve the underlying information and never include an empty heading.

### 1. Project Snapshot

Include:

- a compact metadata block with project and scope, branch and commit when available, generation date, audience, sources used, and important limitations
- project purpose, intended users or consumers, and value
- a five-minute system summary
- important scope boundaries and relationships to surrounding systems
- a curated, annotated directory map containing only the paths a new developer needs for navigation
- the best first entry points into code and documentation

### 2. Business and Domain

Cover important actors, workflows, domain entities, states, terminology, rules, invariants, and failure outcomes. Explain what appears business-critical and distinguish verified context from inference. Use a glossary, lifecycle diagram, state diagram, or small domain table when it improves comprehension.

### 3. Technical System

Cover architecture, runtime components, module responsibilities, boundaries, entry points, interfaces, data stores, schemas, events, integrations, configuration, and important cross-cutting behavior. Trace a small number of representative flows deeply enough to show where behavior begins, how it moves, where state changes, and how success or failure emerges.

### 4. Working with the Project

Cover relevant prerequisites, access, setup, build, run, test, debug, lint, local dependencies, fixtures, configuration, conventions, CI/CD, release, deployment, rollback, observability, support, and ownership. Clearly distinguish commands or workflows you safely verified from those derived only from documentation.

### 5. Learning and Onboarding Roadmap

Do not produce a generic technology inventory. Group learning items into:

- **Essential now** — needed to run, trace, or safely modify the project.
- **Learn when encountered** — needed for particular modules or tasks.
- **Awareness only** — useful context that does not justify upfront study.

For each meaningful item, state the concept or technology, why it matters here, where it appears, the required depth, and a concrete verification activity.

Use a capability-based roadmap rather than fixed days or weeks:

1. **Orient** — explain the purpose, domain, and major components.
2. **Run** — build, start, test, and debug the project, or identify verified blockers.
3. **Trace** — follow a representative business flow end to end.
4. **Change** — locate and reason about a small behavior change and its tests.
5. **Contribute** — follow the delivery process for a first safe task.
6. **Operate** — understand deployment, observation, common failures, and support ownership where relevant.

Give each applicable milestone concrete activities, an expected outcome, and an observable completion check. End with a plausible profile for a first safe contribution, but do not invent an actual task without evidence.

### 6. Evidence, Risks, and Open Questions

Include key evidence by major section, source conflicts, likely stale documentation, inferred conclusions requiring confirmation, meaningful areas not inspected or verified, important risks, and prioritized questions for the team. Do not dump every inspected file.

## Visual-first communication

Favor Mermaid diagrams, annotated tables, concise lists, and short explanations over long prose.

When the evidence supports them, include at least:

1. a system context, component, or architecture diagram
2. a representative sequence, event, data, or business-flow diagram

Add entity-relationship, state, deployment, dependency, or other diagrams whenever they materially improve understanding. Keep each diagram readable and purposeful. Explain its onboarding takeaway. Never invent a node or relationship to complete a plausible-looking visual; state the evidence gap instead.

Use adaptive length. Make the document skimmable in one sitting while useful later as a navigation reference.

## Exclusions

Avoid:

- exhaustive directory trees or dependency dumps
- generic tutorials for common technologies
- file-by-file or class-by-class summaries
- copied passages that can be linked and contextualized
- low-level implementation detail without onboarding value
- speculative business explanations presented as facts
- repetition of information already clear in existing documentation
- boilerplate sections included only to satisfy this prompt

Use this test: if information does not help a new developer understand, navigate, run, trace, change, contribute to, or operate this project, omit it.

## Confidentiality

- Never reproduce secrets, tokens, passwords, private keys, or sensitive personal data.
- Refer to sensitive configuration by variable, secret, or mechanism name rather than value.
- Minimize proprietary excerpts from external sources.
- Preserve the access boundaries of source material.
- Mention restricted access or sensitive material only when needed for onboarding, without exposing it.

## Final quality gate

Before writing `PROJECT_ONBOARDING.md`, confirm that:

- the business and technical explanations agree with inspected evidence
- project, scope, revision, date, audience, sources, and limitations are accurate
- every major section contains useful source anchors
- verified facts, inferences, conflicts, unknowns, and team questions are distinguishable
- Mermaid syntax is valid and every shown relationship is evidence-supported
- the guide enables the reader to explain, navigate, run, trace, change, contribute to, and where relevant operate the project
- learning items are prioritized, project-specific, and paired with verification activities
- roadmap milestones have concrete activities, expected outcomes, and completion checks
- commands and workflows are marked verified or unverified accurately
- no secret or unnecessarily sensitive information appears
- the directory map is curated and annotated
- no generic tutorial, dependency dump, file-by-file summary, repeated documentation, or empty template section remains
- the document is high-density, visual, and honest about risks and gaps
- `PROJECT_ONBOARDING.md` is the only project file created or changed unless the user explicitly authorized another output path

Write only the final onboarding Markdown file. If verification or access was unavailable, record the limitation rather than implying completion.
