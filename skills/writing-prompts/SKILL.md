---
name: moego:writing-prompts
description: Use when composing one-shot prompts, task instructions, questions, code requests, or analysis prompts to send to an LLM — any input consumed once that does not reside in context long-term
triggers:
  - /moego:writing-prompts
  - 编写 prompt、任务指令、LLM 输入
  - 优化或审查现有 prompt
  - prompt 输出不符合预期需要改进
---

# AI Prompt Writing Guide

## Scope

Any text you send to an LLM — task instructions, questions, creative briefs, code requests, analysis prompts.

---

## P1: Format and Constraints Before Task Content

```
# ❌ Format instruction at the end
Here's our Q3 revenue data: [data]
Please analyze trends and present as a markdown table.

# ✅ Format instruction first
Respond with a markdown table comparing Q3 metrics across regions.
Here's the data: [data]
```

```
# ❌ Constraints buried after the request
Write a function that sorts users by signup date.
Use TypeScript. No external libraries. Return type should be User[].

# ✅ Constraints before the request
TypeScript, no external libraries, return type User[].
Write a function that sorts users by signup date.
```

---

## P2: Proximity — All Info for One Decision in One Block

```
# ❌ Scattered
We're using PostgreSQL 15.
[... 200 words about other things ...]
Write a query to find duplicate emails.
[... 100 words about other things ...]
The users table has columns: id, email, name, created_at.

# ✅ Together
Table: users (id, email, name, created_at), PostgreSQL 15.
Write a query to find duplicate emails.
```

---

## P3: Specificity — Narrow the Output Space

```
# ❌
Improve this code.

# ✅
Reduce the time complexity of the `findDuplicates` function from O(n²) to O(n)
using a Set. Keep the function signature unchanged.
```

```
# ❌
Write something about our product launch.

# ✅
Write a 3-paragraph internal announcement for Slack:
P1: what launched and for whom
P2: key differentiators (mention latency and pricing)
P3: where to find docs and who to contact
```

**Specify what you don't want when the default is likely wrong.**

```
# ✅
Explain TCP handshake. No analogies, no "imagine" scenarios.
Technical audience — use correct terminology.
```

---

## P4: Show, Don't Describe — Use Examples

```
# ❌ Describing the format
Convert each item to a structured entry with the name, category,
and a brief one-line description.

# ✅ One example does the work
Convert each item to this format:

**Kafka** | Messaging | Distributed event streaming platform for high-throughput pipelines

Items to convert: [list]
```

**For complex tasks, show both positive and negative examples.**

```
# ✅
Rewrite these error messages for end users.

Good: "Unable to save — file is open in another program. Close it and try again."
Bad: "Error: EACCES write permission denied on fd 7"

Messages to rewrite: [list]
```

---

## P5: One Prompt, One Job

```
# ❌ Two unrelated jobs
Review this PR for bugs AND write release notes for the changes.

# ✅ Split
Prompt 1: Review this PR. Flag bugs, race conditions, and missing error handling.
Prompt 2: Based on this diff, write release notes. One bullet per user-facing change.
```

Related tasks sharing context — keep together, make sequence explicit:

```
# ✅
Step 1: Identify all API endpoints in this file that lack input validation.
Step 2: For each one, add zod schema validation. Keep existing behavior unchanged.
```

---

## P6: Role Only When It Shifts Default Behavior

```
# ❌ Default restated (zero shift)
You are a helpful AI assistant. Please help me with the following task.

# ✅ Role shifts behavior
You are a senior security auditor. Evaluate this auth flow.
Assume the attacker has network access and leaked session tokens.
```

```
# ✅ Role constrains output
You are a technical writer for an API reference.
Write in present tense, active voice, no marketing language.
```

---

## P7: Delimiters for Multi-Part Input

```
# ❌ Ambiguous boundaries
Please summarize this and focus on financial impact.
The company reported Q3 results showing a 15% decline in revenue...
Also make sure to mention the CEO's statement about restructuring.

# ✅ Clear delimiters
<instruction>
Summarize the following article in 3 sentences. Focus on financial impact.
Include the CEO's restructuring statement.
</instruction>

<article>
The company reported Q3 results showing a 15% decline in revenue...
</article>
```

---

## P8: Constrain Length and Scope Explicitly

```
# ❌
Explain how DNS works.

# ✅
Explain DNS resolution in 4 steps, one sentence each.
Scope: from browser URL bar to IP address. Skip DNSSEC.
```

```
# ✅
Write a `retry` wrapper. Max 20 lines. Exponential backoff, max 3 attempts.
No external dependencies.
```

---

## P9: Reference Material Before Questions About It

```
# ❌ Question before context
What are the main risks in this contract?
[5 pages of contract text]

# ✅ Context before question
<contract>
[5 pages of contract text]
</contract>

What are the top 3 financial risks in this contract? For each, quote the relevant clause.
```

---

## Self-Check

- [ ] Format/constraints before main content? (P1)
- [ ] All info for each decision in one block? (P2)
- [ ] Any vague words replaceable with specific actions? (P3)
- [ ] Would an example communicate better than description? (P4)
- [ ] Multiple unrelated tasks that should be split? (P5)
- [ ] Role instruction actually changes default behavior? (P6)
- [ ] Instruction, context, and data clearly delimited? (P7)
- [ ] Length and scope explicitly stated? (P8)
- [ ] Reference material before questions about it? (P9)
