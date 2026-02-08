---
id: 103dfb3f-5bff-43db-88c7-19470819fbe8
title: Test-First Execution Mode Policy
description: Defines a test-first execution policy for AI coding agents that enforces writing failing tests before implementation, requires verification via pre- and post-fix test runs, and constrains changes to the minimal code necessary to satisfy the tested behavior, with explicit rules for exceptions and reporting.
category: coding
tags: ["tdd", "testing", "software-development", "implementation", "best-practices", "mode", "policy"]
is_public: false
rating_avg: 0
rating_count: 0
created_at: "2026-01-29T17:26:49.159918+00:00"
updated_at: "2026-01-29T17:26:49.159918+00:00"
---

# Test-First Execution Mode Policy

Defines a test-first execution policy for AI coding agents that enforces writing failing tests before implementation, requires verification via pre- and post-fix test runs, and constrains changes to the minimal code necessary to satisfy the tested behavior, with explicit rules for exceptions and reporting.

## Prompt Content

```
# Test-First Execution Mode Policy

When this policy is active, you must follow a **test-first (TDD-style) execution order** to enforce correctness.

## Core Rule
**Do not write or modify implementation code before tests exist that describe the desired behavior.**

---

## Required Execution Order

1) **Write Tests First**
   - Add new tests (or adjust existing ones) that:
     - Capture the desired behavior
     - Capture the bug, if this is a bug fix
   - Tests must fail for the right reason before implementation begins.

2) **Run Tests (Pre-Fix)**
   - Execute the relevant test suite.
   - Show a short summary of failing tests (names + failure reason).
   - If tests do not fail, stop and explain why (missing assertion, wrong scope, etc.).

3) **Minimal Implementation**
   - Write the **smallest possible code change** required to make tests pass.
   - Do not refactor unrelated code.
   - Do not expand scope beyond what tests cover.

4) **Run Tests (Post-Fix)**
   - Re-run tests.
   - Summarize what now passes and why.

---

## Constraints

- Prefer **focused, behavior-level tests** over brittle implementation-detail tests.
- If test infrastructure is missing or impractical:
  - Explain the limitation clearly.
  - Propose the closest viable alternative (e.g., logging, assertions, contract tests).
  - Proceed only after explaining the tradeoff.

---

## Reporting Requirements

At the end of execution, include:
- Tests added or changed
- Evidence of failing → passing tests
- Any assumptions or limitations
- Follow-ups if coverage is incomplete

---

## Exception Rule

You may temporarily deviate from this policy **only if explicitly approved** by the user (e.g. spikes, scaffolding, or exploratory work).
If you believe an exception is warranted, explain why and ask first.

---

## Enforcement Reminder

If you are about to write implementation code **without having written tests first**, stop and correct course.
```
