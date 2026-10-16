---
name: feature-spec
description: Use when creating a feature spec from specs/roadmap.md, specs/mission.md, specs/tech-stack.md. Generates YYYY-MM-DD-feature-name folder with plan.md, requirements.md, validations.md. Use ONLY for phased feature-spec workflow.
---

# Feature Spec

Reusable workflow to stop repeating the feature-spec prompt. Run when user says "feature spec", "next phase", "spec the feature".

## Workflow

1. **Find next phase**
   - Read `specs/roadmap.md` to find the next incomplete phase.
   - Read `specs/mission.md` and `specs/tech-stack.md` for scope and stack guidance.
   - Check `git status` for clean tree.

2. **Make a branch**
   - Create branch: `feature/YYYY-MM-DD-feature-name` (lowercase, hyphen-separated).
   - Example: `feature/2026-10-16-oltp-seed`

3. **Ask before writing (REQUIRED)**
   - You MUST call the AskUserQuestion tool ONCE with 3 grouped questions before any write to disk:
     - Q1 `plan.md`: task groups, granularity, order.
     - Q2 `requirements.md`: scope, decisions, context / non-goals.
     - Q3 `validations.md`: success checks, merge gate.
   - Do NOT create directory or files until user answers.

4. **Create spec folder**
   - New directory: `specs/YYYY-MM-DD-feature-name/`
   - Inside, create exactly:
     - `plan.md` — series of numbered task groups, each independently verifiable, in implementation order.
     - `requirements.md` — scope, decisions, context, non-goals. Must cite `specs/mission.md` and `specs/tech-stack.md`.
     - `validations.md` — how to know implementation succeeded and can be merged (commands, queries, expected output).

## File Templates

### plan.md
```markdown
# Plan — <feature-name> (<YYYY-MM-DD>)
Phase: <roadmap phase reference>
## 1. <group> — <what>
- [ ] task
- Verify: <check>
## 2. <group>
...
```

### requirements.md
```markdown
# Requirements — <feature-name>
## Scope
## Decisions
## Context (mission/tech-stack links)
## Non-Goals
```

### validations.md
```markdown
# Validations — <feature-name>
## Success Checks
1. Command: `<cmd>` → expected: `<output>`
## Merge Gate
- [ ] all checks green
```

## Rules
- Never write to `specs/YYYY-MM-DD-feature-name/` before AskUserQuestion answers return.
- Keep phases very small, matching `specs/roadmap.md` style.
- Refer to mission + tech-stack, do not contradict them.
