---
name: jira
description: Read MoeGo Jira issues using JIRA_EMAIL and JIRA_TOKEN, and analyze private Jira image attachments by downloading them locally before direct image inspection.
compatibility: opencode
---

## When to use me

- Use this for MoeGo Jira tickets and Jira attachments.

## Instructions

- Jira auth is available via `JIRA_EMAIL` and `JIRA_TOKEN`.
- Use Jira REST API to read private issues and attachments.
- For image attachments, do not rely on direct remote image access.
- First download the protected attachment to a local temp file with an authenticated request.
- Then inspect the local image directly.
- Use OCR only as a fallback when direct image inspection is insufficient.
