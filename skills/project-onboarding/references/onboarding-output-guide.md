# Onboarding Output Guide

Use this guide to shape `PROJECT_ONBOARDING.md`. Preserve the information model, but adapt subsection depth and ordering to the project. Do not include empty headings or force irrelevant content.

## Contents

1. [Snapshot metadata](#snapshot-metadata)
2. [Six-section information model](#six-section-information-model)
3. [Visual communication](#visual-communication)
4. [Evidence and uncertainty](#evidence-and-uncertainty)
5. [Learning and roadmap design](#learning-and-roadmap-design)
6. [Final quality gate](#final-quality-gate)

## Snapshot metadata

Open the document with a compact metadata block or table containing:

- project and investigated scope
- branch and commit identifier when available
- generation date
- audience and any relevant assumed experience
- repository and external sources used
- important access, execution, or verification limitations

Make clear that the guide is a snapshot of the recorded revision rather than timeless truth.

## Six-section information model

Use these six top-level sections by default.

### 1. Project Snapshot

Give the shortest useful orientation:

- project purpose, intended users or consumers, and value
- system summary that a new developer can repeat accurately
- important scope boundaries and relationships to surrounding systems
- a curated, annotated map of only the paths needed for navigation
- the best first entry points into code and documentation

Do not paste a broad directory tree. Select paths that reveal architecture, business logic, developer workflow, or operations, and explain each selection.

### 2. Business and Domain

Explain what the software means, not just what frameworks it uses:

- important actors, workflows, domain entities, states, and terminology
- consequential rules, invariants, and failure outcomes
- sources of inputs and consumers of outputs
- what appears business-critical versus supporting behavior
- verified context, reasonable inference, and unanswered business questions

Use a glossary, lifecycle diagram, state diagram, or small domain table when it reduces prose.

### 3. Technical System

Create a navigable technical model:

- architecture style and runtime components
- module responsibilities and boundaries
- entry points and public interfaces
- data stores, schemas, migrations, caches, queues, and external integrations
- configuration and environment model
- representative synchronous, asynchronous, batch, or scheduled flows
- important cross-cutting behavior such as authentication, validation, transactions, retries, idempotency, error handling, or concurrency
- notable technical risks, legacy areas, or active transitions supported by evidence

Trace a small number of representative flows deeply enough that the reader knows where behavior begins, how it moves, where state changes, and how success or failure emerges.

### 4. Working with the Project

Help the developer act safely:

- prerequisites and access requirements
- setup, build, run, test, debug, lint, and other essential commands
- local dependencies, fixtures, profiles, and configuration
- test strategy and where different test types live
- coding and contribution conventions that materially affect changes
- CI/CD, release, deployment, environment, and rollback model
- logging, metrics, tracing, alerts, dashboards, support, and ownership when relevant
- known blockers or steps that were documented but not verified

Do not claim a command works unless it was safely verified or clearly label it as documentation-derived and unverified.

### 5. Learning and Onboarding Roadmap

Combine prioritized learning with capability milestones.

For learning items, include:

| Priority | Concept or technology | Why it matters here | Where it appears | Required depth | Verification activity |
|---|---|---|---|---|---|
| Essential now | ... | ... | ... | ... | ... |

Use **Essential now**, **Learn when encountered**, and **Awareness only**. Avoid raw lists of languages, frameworks, or dependencies.

For roadmap milestones, include:

| Milestone | Activities | Expected outcome | Completion check |
|---|---|---|---|
| Orient | ... | ... | ... |

Use the applicable sequence: **Orient**, **Run**, **Trace**, **Change**, **Contribute**, and **Operate**. Tailor activities to real files, flows, commands, tests, and delivery mechanisms. Do not organize the roadmap around fixed days or weeks.

End with a plausible first safe contribution profile, such as a focused test, small bug fix, documentation correction, or contained behavior change. Do not invent an actual task when no evidence supports one.

### 6. Evidence, Risks, and Open Questions

Close the gaps honestly:

- key evidence by major section
- source conflicts and likely stale documentation
- inferred conclusions that require confirmation
- meaningful areas not inspected or not verifiable
- technical, operational, domain, or onboarding risks
- concise, prioritized questions to ask the team

Avoid a dump of every file inspected. Cite the evidence that supports important conclusions and helps the reader continue exploring.

## Visual communication

Prefer visuals when they expose relationships, boundaries, or sequence faster than prose.

Include at least two Mermaid diagrams when evidence permits:

1. a system context, component, or architecture view
2. a representative sequence, event, data, or business flow

Add more when useful:

| Need | Useful diagram |
|---|---|
| System boundaries and dependencies | Flowchart, C4, or architecture diagram |
| Request, event, or batch progression | Sequence or flowchart |
| Entity relationships | Entity-relationship diagram |
| Domain lifecycle | State diagram |
| Deployment/runtime topology | Architecture or flowchart |
| Module dependency direction | Flowchart |

Keep diagrams readable and scoped. Explain the onboarding takeaway immediately before or after each diagram. Ensure that nodes and edges are supported by inspected evidence. If evidence is insufficient, state the gap rather than completing a plausible-looking diagram.

Use tables for exact mappings and comparisons. Use prose for interpretation, caveats, and small numbers of connected ideas.

## Evidence and uncertainty

Every major section must contain compact source anchors. Good anchors include:

- `relative/path/File.java` — `ClassName.methodName`
- `relative/path/config.yml` — `service.retry` configuration
- `docs/architecture.md` — “Runtime topology”
- supplied document title and URL
- commit identifier and concise relevance

Prefer stable symbols and headings; add line numbers only when helpful. Never use citations to disguise weak support.

Label consequential uncertainty with **Verified**, **Inferred**, **Unknown**, or **Ask the team**. When sources conflict, describe the conflict and its practical implication.

## Learning and roadmap design

Prioritize knowledge by the work the developer must perform, not by the prominence of a technology.

A strong learning item is project-specific:

> Understand consumer groups, offset handling, and retry behavior because settlement processing enters through the consumers in `settlement-worker/`. Verify by tracing one event from handler through persistence and failure handling.

A weak learning item is generic:

> Learn Kafka.

Completion checks should be observable. Prefer “trace an API request from route to persisted state and identify its failure responses” over “understand the API.”

## Final quality gate

Before writing the output, confirm all applicable checks:

- Business and technical explanations agree with inspected evidence.
- The recorded project, scope, branch, revision, date, audience, and sources are accurate.
- Every major section has useful source anchors.
- Verified facts, inferences, conflicts, unknowns, and team questions are distinguishable.
- Mermaid syntax is valid and every shown relationship is evidence-supported.
- The guide enables the reader to explain, navigate, run, trace, change, contribute to, and where relevant operate the project.
- Learning items are prioritized, project-specific, and paired with verification activities.
- Roadmap milestones have concrete activities, expected outcomes, and completion checks.
- Commands and workflows are marked verified or unverified accurately.
- No secret, credential, private key, sensitive personal data, or unnecessary proprietary excerpt appears.
- The directory map is curated and annotated rather than exhaustive.
- No generic tutorial, dependency dump, file-by-file summary, repeated documentation, or empty template section remains.
- The document is high-density, visual, and skimmable without hiding material risks or gaps.
- `PROJECT_ONBOARDING.md` is the only project file created or changed, unless the user explicitly authorized another output path.
