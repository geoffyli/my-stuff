---
name: project-onboarding
description: Comprehensively investigate a software project and create a concise, evidence-backed PROJECT_ONBOARDING.md for a new developer, covering business context, technical architecture, developer workflows, prioritized learning, and a capability-based onboarding roadmap. Use when the user asks to onboard to, understand, explore, map, or create an onboarding guide for a repository or software project, optionally using user-provided documentation or connected project sources. Do not use for isolated code explanations, routine code review, or general technology tutorials.
---

# Project Onboarding

Create one high-density, visual onboarding guide that helps a new developer explain, navigate, run, trace, change, contribute to, and where relevant operate the project.

Read [references/onboarding-output-guide.md](references/onboarding-output-guide.md) before drafting the guide. Use it as an information model, not as a reason to include empty or irrelevant sections.

## Apply the defaults

- Treat the current repository or project workspace as the target.
- Assume the audience is a general software developer with no project-specific knowledge. Use a user-specified role, responsibilities, or experience instead when provided.
- Use repository content as the baseline evidence. Inspect external documents or connected systems only when the user supplies or explicitly authorizes them.
- Start immediately unless ambiguity would materially change the result, such as several unrelated projects or a monorepo with no discernible focal product.
- Write `PROJECT_ONBOARDING.md` at the repository root unless the user specifies another path.
- Treat the onboarding document as the only permitted write. Never overwrite an existing file without explicit permission.
- Keep the investigation read-only. Use safe, non-destructive inspection or verification commands when helpful, but do not change tracked project content, install global software, modify infrastructure, invoke production behavior, or invent credentials.

## Investigate with judgment

Choose the exploration technique and depth that best fit the project. Optimize for systematic coverage and trustworthy understanding, not for reading every file.

For a small project, near-exhaustive inspection may be efficient. For a large project, map the whole system and deep-dive into representative components and flows. Inspect sources such as these when relevant:

- README files, project documentation, decision records, and supplied external context
- manifests, dependency definitions, build systems, and workspace configuration
- entry points, module boundaries, public interfaces, and core domain code
- data models, migrations, persistence, events, APIs, and external integrations
- tests, fixtures, local development setup, and debugging configuration
- CI/CD, deployment, infrastructure, observability, support, and ownership artifacts
- version-control history that clarifies evolution, active areas, or non-obvious decisions

Use version-control history selectively. Do not rank contributors, infer performance from activity counts, or turn the guide into commit analytics.

For a monorepo, explain the repository-wide landscape first, then deep-dive into components required for representative business and developer flows. Do not create a mini-guide for every package unless requested. Ask for scope only when the monorepo contains several unrelated products and no reasonable focal point can be inferred.

## Build an evidence-backed model

Establish both the business and technical picture:

- Identify the project's purpose, users or consumers, value, important workflows, domain entities, terminology, and consequential business rules.
- Map components, boundaries, runtime topology, data movement, integrations, and representative end-to-end flows.
- Determine how a developer sets up, runs, tests, debugs, changes, delivers, observes, and supports the project, where the available evidence allows.
- Distinguish current behavior from business intent, historical rationale, and planned work.
- Detect conflicts between code, configuration, tests, documentation, tickets, and other sources. Report conflicts rather than silently choosing a convenient narrative.

Classify consequential conclusions:

- **Verified** — directly supported by inspected evidence.
- **Inferred** — strongly suggested but not explicitly established.
- **Unknown** — important information that could not be established.
- **Ask the team** — a targeted question whose answer would close a meaningful gap.

Anchor every major section to compact evidence. Prefer repository-relative paths plus a class, function, configuration key, heading, or other stable locator. For external sources, cite the title and URL or supplied identifier. For history, cite a commit identifier when it materially supports the conclusion. Do not clutter every sentence with citations.

## Prioritize learning and action

Do not produce a generic technology inventory. Group learning items into:

- **Essential now** — needed to run, trace, or safely modify the project.
- **Learn when encountered** — needed for particular modules or tasks.
- **Awareness only** — useful context that does not justify upfront study.

For every meaningful learning item, state why it matters here, where it appears, the depth required, and a concrete way to verify understanding.

Build a capability-based roadmap rather than a fixed day/week schedule. Progress through these outcomes when relevant:

1. **Orient** — explain the purpose, domain, and major components.
2. **Run** — build, start, test, and debug the project, or identify verified blockers.
3. **Trace** — follow a representative business flow end to end.
4. **Change** — locate and reason about a small behavior change and its tests.
5. **Contribute** — follow the project's delivery process for a first safe task.
6. **Operate** — understand deployment, observation, common failures, and support ownership where relevant.

Give each milestone concrete activities, an expected outcome, and an observable completion check. Add time estimates only when genuinely useful; never organize the roadmap around fixed elapsed time.

## Write for orientation

Use the six top-level sections defined in the output guide. Merge, omit, or adapt subsections when the project warrants it, but preserve the underlying information.

Favor diagrams, annotated tables, concise lists, and short explanations over long prose. Include at least two meaningful Mermaid diagrams when the evidence supports them: normally a system/component view and a representative end-to-end flow. Add data, dependency, deployment, state, or event diagrams when they materially improve understanding. Never invent a node or relationship to complete a diagram.

Include a curated, annotated directory map rather than an exhaustive tree. Explain why each selected path matters.

Avoid:

- exhaustive directory trees or dependency dumps
- generic tutorials for common technologies
- file-by-file or class-by-class summaries
- copied passages that can be linked and contextualized
- implementation detail without onboarding value
- speculative business explanations presented as facts
- repetition of information already clear in existing documentation
- boilerplate sections included only to satisfy a template

Use adaptive length. Make the guide skimmable in one sitting while useful later as a navigation reference.

## Protect sensitive information

- Never reproduce secrets, tokens, passwords, private keys, or sensitive personal data.
- Refer to sensitive configuration by variable, secret, or mechanism name rather than value.
- Minimize proprietary excerpts from external sources.
- Preserve the access boundaries of the source material.
- Mention that sensitive information or restricted access is relevant only when needed for onboarding, without exposing it.

## Validate before writing

Apply the quality gate in the output guide. Confirm that the document is internally consistent, source-grounded, visually useful, safe, aligned to the recorded scope and revision, and capable of guiding a new developer toward a first safe contribution.

Write only the final onboarding Markdown file. If verification or access was unavailable, state that limitation in the file rather than implying completion.
