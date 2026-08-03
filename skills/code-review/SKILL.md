---
name: code-review
description: Multi-axis code review covering correctness, readability, architecture, security, and performance. Use before merging any PR, after implementing a feature, or when reviewing AI-generated or refactored code.
metadata:
---

# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** "Approve a change when it definitely improves overall code health, even if it isn't perfect." The objective is continuous improvement rather than attaining perfection.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code accomplish its stated purpose?

- Alignment with spec or task requirements
- Handling of edge cases (null, empty, boundary values)
- Coverage of error paths beyond the happy path
- Test success and test validity
- Absence of off-by-one errors, race conditions, or state inconsistencies

### 2. Readability & Simplicity

Can another engineer understand this code without author explanation?

- Descriptive, convention-aligned naming conventions
- Straightforward control flow
- Logical code organization with clear module boundaries
- Elimination of unnecessary complexity or "clever" tricks
- Appropriate use of comments for non-obvious intent
- Removal of dead code artifacts

### 3. Architecture

Does the change fit the system's design?

- Alignment with existing patterns or justified new patterns
- Maintenance of clean module boundaries
- Elimination of code duplication
- Correct dependency direction without circular dependencies
- Appropriate abstraction levels

### 4. Security

Examine for potential vulnerabilities:

- "Is user input validated and sanitized?"
- Secrets excluded from code, logs, and version control
- Authentication/authorization checks where required
- Parameterized queries (no string concatenation)
- Output encoding to prevent XSS
- Dependencies from trusted sources with no known vulnerabilities
- "External data sources treated as untrusted"

### 5. Performance

Identify potential performance problems:

- Absence of N+1 query patterns
- No unbounded loops or unconstrained data fetching
- Synchronous operations that should be async
- Unnecessary re-renders in UI components
- Pagination on list endpoints
- Large objects created in hot paths

## Change Sizing

"Small, focused changes are easier to review, faster to merge, and safer to deploy."

```
~100 lines changed   → Good. Reviewable in one sitting.
~300 lines changed   → Acceptable if it's a single logical change.
~1000 lines changed  → Too large. Split it.
```

A single change should be "self-contained" and address one thing while maintaining system functionality.

## Change Descriptions

Every change requires a description that serves as standalone documentation in version control.

**First line:** Short, imperative phrasing that provides sufficient context for historical searches

**Body:** What is changing and why, including context, decisions, and reasoning not visible in code itself. Link to bugs, benchmarks, or design documents where relevant.

## Review Process

### Step 1: Understand the Context

Before examining code:

- What is this change attempting to accomplish?
- What spec or task does it implement?
- What behavior change is expected?

### Step 2: Review the Tests First

Tests reveal intent and coverage gaps:

- Existence and quality of tests
- Focus on behavior rather than implementation details
- Edge case coverage
- Descriptive test naming
- Regression detection capability

### Step 3: Review the Implementation

Evaluate the code against all five axes for each changed file.

### Step 4: Categorize Findings

Label each comment with severity to distinguish required versus optional feedback:

| Prefix | Meaning |
|--------|---------|
| *(no prefix)* | Required change |
| **Critical:** | Blocks merge (security, data loss, broken functionality) |
| **Nit:** | Minor, optional |
| **Optional:** / **Consider:** | Worth considering but not required |
| **FYI** | Informational only |

### Step 5: Verify the Verification

Confirm the author's verification approach:

- Tests executed and passing
- Build success
- Manual testing completion
- Screenshots for UI changes
- Before/after comparisons

## Multi-Model Review Pattern

Different models can catch different issues. Consider using sequential reviews where:

```
Model A writes code → Model B reviews → A addresses feedback → Human approval
```

This pattern surfaces issues that single-perspective review might miss.

## Dead Code Hygiene

After refactoring or implementation:

1. Identify unreachable or unused code
2. List it explicitly
3. Ask permission before deleting

"Don't leave dead code lying around — it confuses future readers and agents."

## Review Speed

"Slow reviews block entire teams." Respond within one business day maximum, with ideal response shortly after the request arrives.

## Handling Disagreements

Apply this hierarchy when disputes arise:

1. Technical facts and data override opinions
2. Style guides are authoritative on style matters
3. Software design should follow engineering principles, not preference
4. Codebase consistency is acceptable if it maintains overall health

"Don't accept 'I'll clean it up later.'" Deferred cleanup rarely happens.

## Honesty in Review

Maintain integrity in the review process:

- Provide evidence of actual review, not rubber-stamp approvals
- Address real issues directly rather than softening concerns
- Quantify problems when possible
- Push back on problematic approaches
- Defer gracefully to author's full context when appropriate

## Dependency Discipline

Before adding dependencies:

1. Does the existing stack solve this problem?
2. What is the dependency's size impact?
3. Is it actively maintained?
4. Are there known vulnerabilities?
5. Is the license compatible?

"Prefer standard library and existing utilities over new dependencies."

## The Review Checklist

A structured approach to reviewing changes:

```markdown
## Review: [Change title]

### Context
- [ ] I understand what this change does and why

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled
- [ ] Error paths handled
- [ ] Tests cover the change adequately

### Readability
- [ ] Names are clear and consistent
- [ ] Logic is straightforward
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows existing patterns
- [ ] No unnecessary coupling or dependencies
- [ ] Appropriate abstraction level

### Security
- [ ] No secrets in code
- [ ] Input validated at boundaries
- [ ] No injection vulnerabilities
- [ ] Auth checks in place
- [ ] External data sources treated as untrusted

### Performance
- [ ] No N+1 patterns
- [ ] No unbounded operations
- [ ] Pagination on list endpoints

### Verification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] Manual verification done (if applicable)

### Verdict
- [ ] **Approve** — Ready to merge
- [ ] **Request changes** — Issues must be addressed
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It works, that's good enough" | Working code that is unreadable, insecure, or architecturally flawed creates compounding debt |
| "I wrote it, so I know it's correct" | Authors have blind spots regarding their own assumptions; peer review helps identify them |
| "We'll clean it up later" | Deferred cleanup is rarely executed; use review as the quality gate |
| "AI-generated code is probably fine" | Generated code requires heightened scrutiny due to confident but incorrect output |
| "The tests pass, so it's good" | Test success is necessary but insufficient to address architecture, security, and readability concerns |

## Red Flags

- PRs merged without review
- Review that only verifies test passage
- Approval statements lacking evidence of substantive review
- Security-sensitive changes without security-focused examination
- Large PRs deemed too extensive to review properly
- Bug fix PRs without regression tests
- Review comments without severity indicators
- Acceptance of deferred cleanup

## Verification

After review completion:

- [ ] All Critical issues are resolved
- [ ] All Important issues are resolved or explicitly deferred with justification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] The verification story is documented
