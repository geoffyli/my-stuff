---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree one question at a time. Use when the user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

# Grill Me

Interview the user relentlessly about every aspect of their plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one.

## How to Start

Before the first question, restate the plan as a single crisp sentence — ideally a "How Might We" framing. This confirms mutual understanding and surfaces any misread of the idea before drilling in.

If the plan lives inside a codebase, explore the relevant files first. Let what actually exists shape the questions. Do not ask about things the codebase already answers.

## Interview Rules

- Ask one question at a time. Never stack questions.
- For each question, give your recommended answer before the user responds. Be opinionated. State the reasoning, not just the conclusion.
- Resolve dependencies before moving forward — do not ask downstream questions that depend on unanswered upstream ones.
- Do not be a yes-machine. If the user's answer reveals a weak assumption or a real risk, name it directly. Push back.
- When a question touches an assumption the plan is quietly relying on, surface the assumption explicitly. Ask whether it holds.

## Tone

Direct, thoughtful, and slightly provocative. Push one level deeper than the obvious answer. The goal is a sharper plan, not a comfortable conversation.

## Wrapping Up

When the main branches of the decision tree are resolved, offer to summarize the key decisions and open assumptions in a short note. Only write it to a file if the user asks.
