---
name: moego:writing-system-documents
description: Use when writing or reviewing compact-immune documents that persist in Agent Context throughout entire sessions — CLAUDE.md, role definitions, project rules, behavior specs, system prompts
triggers:
  - /moego:writing-system-documents
  - 编写或审查 CLAUDE.md
  - 编写 system prompt、角色定义、行为规范
  - 审计系统文档的 token 浪费或模糊规则
---

# Agent Resident System Document — Writing Guide

## Target Document Definition

The **target document** is any compact-immune, system-level document that resides in an Agent's Context Window throughout the entire session.

Every token is a fixed cost. Write accordingly.

---

## P0: Every Line Must Justify Its Token Cost

Three tests before a line earns residency:

1. Will Attention repeatedly query it across different tasks?
2. Does a more authoritative source already contain this? (code comments, README, framework docs)
3. Does removing it cause observable behavior degradation?

If any answer is no, the line doesn't belong.

```markdown
# ❌
## Project Background
This is a user management system built with TypeScript and PostgreSQL...

# ✅
Import paths use @/ alias pointing to src/ — no relative paths
Test files colocate with source, named *.test.ts
```

---

## P1: Proximity — Condition + Action + Constraint in One Block

```markdown
# ❌ Condition and action separated by unrelated content
Use gzip for log files
Keep code style consistent
List affected files before log operations

# ✅ One compact block
Log file ops: ls affected files first → confirm → then gzip. Never one-shot.
```

**Cluster by scenario, not by concept.**

```markdown
# ❌ By concept
## Tools
Use bash for commands
Use edit for modifications
## Safety
Confirm before destructive ops
Read before modifying

# ✅ By scenario
## File Operations
Modify: read current content → edit → never skip read
Delete/overwrite: ls affected files → user confirm → execute
```

---

## P2: Specificity — Verb + Object, Not Adjectives

```markdown
# ❌
Handle file operations carefully
Maintain code quality
Watch for performance issues

# ✅
Before file delete/overwrite: ls affected files, wait for user confirm
Split functions exceeding 50 lines; modularize files exceeding 300 lines
No N+1 queries — DB access through batch interfaces in service layer
```

**"Don't X, use Y" is more precise than "do Y" alone.**

```markdown
Don't use `any` — use `unknown` with type guards
Don't mutate state directly — dispatch through reducers
Don't call APIs in components — wrap in custom hooks
```

---

## P3: Guardrails — Define What Must Not Be Done and What Must Be Done First

**Boundaries > descriptions.**

```markdown
# ❌
You are a coding assistant that writes high-quality TypeScript

# ✅
Do not modify dependency versions in package.json — suggest for user to decide
Do not touch CI/CD configs (.github/workflows/*)
Do not refactor outside current task scope — flag and suggest
```

**Mandatory prerequisite steps > post-hoc checks.**

```markdown
# ❌
Check for errors after modifying files

# ✅
File modification flow: read → confirm current content → edit → run related tests
```

---

## P4: Density — Maximum Signal Per Token

```markdown
# ❌
When you need to modify a file, you should first read the current content
of the file, and then perform the modification, and after that run tests.

# ✅
File modification: read → edit → run related tests
```

```markdown
# ❌
For unit tests use vitest.
For E2E tests use playwright.
For API tests use supertest.

# ✅
| Test type | Tool |
|-----------|------|
| Unit | vitest |
| E2E | playwright |
| API | supertest |
```

Delete all atmosphere statements — "Please remember", "very important", "keep in mind".

---

## P5: Align With Training Distribution

Standard Markdown, backtick-wrapped commands/paths, short imperative sentences.

```markdown
# ✅
## Git Convention
Commit format: `type(scope): description`
- type: feat / fix / refactor / test / docs
- scope: module name, e.g. `auth`, `api`, `ui`
- Example: `feat(auth): add JWT refresh token rotation`
```

---

## P6: Verifiability — Every Rule Answerable Yes/No

```markdown
# ❌
Keep code clean
Organize structure well
Handle edge cases

# ✅
Single function ≤ 50 lines
Single file ≤ 300 lines
Every public function has JSDoc
Switch statements have default branch
```

---

## Template

```markdown
# [Project] System Rules

## Identity & Boundaries
[1-3 line role definition]
[Negative capability list — what not to do]

## Core Behavior Rules
[High-frequency rules, condition → action → constraint]

## Code Standards
[Technical rules, commands in backticks, "Don't X, use Y"]

## Project Structure
[Directory layout, key paths]

## Tools & Workflows
[Task-specific flows, tabulated tool selection]
```

---

## Self-Check

- [ ] Removing any line causes behavior degradation? (P0)
- [ ] Condition and action adjacent for every rule? (P1)
- [ ] No vague words — "careful", "maintain"? (P2)
- [ ] Capability boundaries defined? (P3)
- [ ] Mandatory prerequisite steps specified? (P3)
- [ ] No atmosphere statements? (P4)
- [ ] Standard Markdown with code blocks? (P5)
- [ ] Every rule verifiable yes/no? (P6)
