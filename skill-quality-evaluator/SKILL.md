---
name: skill-quality-evaluator
description: Evaluate the health and quality of an Agent Skill. Use when user wants to review, audit, or check the quality of a SKILL.md file. Triggers on: "review this skill", "audit my skill", "check skill quality", "evaluate this skill", "skill health check", "is my skill good", "skill quality evaluator". Also triggers when user discusses skill anti-patterns or wants improvement suggestions for an existing Skill.
metadata:
  version: "2.0"
  author: ima-assistant
  type: reviewer
---

# Skill Quality Evaluator

Evaluate a Skill against Anthropic's official Skill-building standards and best practices. Output a structured diagnostic report with scores, issues, and improvement suggestions.

## Use Cases

1. **Pre-deployment review** — Check a newly written Skill before sharing or using in production
2. **Troubleshooting** — Diagnose why a Skill isn't triggering or performing well
3. **Maintenance audit** — Periodically review existing Skills for bitrot or compliance drift

## Evaluation Process

### Step 0: Script Validation (MANDATORY — run first)

Before any human or AI judgment, run the structural validator. **This is non-negotiable.** Script catches objective violations that prompt-based review can miss.

```bash
python scripts/validate_skill.py <path-to-skill-folder>
```

This checks:
- SKILL.md exists with exact filename case
- YAML frontmatter is valid and parsable
- `name` is kebab-case, <= 64 chars, matches folder name
- `description` present, <= 1024 chars, contains WHAT + WHEN heuristics
- No XML angle brackets in frontmatter
- No reserved words ("claude", "anthropic") in name
- Body under 500 lines
- No README.md in skill folder

Exit code 0 = all structural checks pass. Exit code 1 = violations found — **fix structural issues before proceeding to prompt-based review**.

### Step 1: Read the Skill

Read the target SKILL.md and any files in `references/`. If Step 0 found violations, report them first.

### Step 2: Classify the Skill

Identify which official category the Skill belongs to:

| Category | Description | Review Focus |
|----------|-------------|-------------|
| Document & Asset Creation | Consistent output with embedded style guides | Output fidelity, template adherence |
| Workflow Automation | Multi-step processes with validation gates | Step completeness, error handling, rollback |
| MCP Enhancement | Workflow guidance on top of MCP tools | Tool coordination, error recovery |

### Step 3: Evaluate Against Quality Dimensions

Load `references/quality-checklist.md` for the full checklist. Four dimensions:

| Dimension | Weight | What It Checks |
|-----------|--------|---------------|
| Triggering Effectiveness | 30 | Does description include trigger phrases? Does it describe WHEN, not just WHAT? Will it fire on relevant queries and not fire on unrelated ones? |
| Structural Compliance | 25 | kebab-case name? Folder matches name? SKILL.md under 500 lines? Progressive disclosure used? No XML tags? |
| Functional Completeness | 25 | Are edge cases covered? Error handling present? Examples provided? Instructions actionable? |
| Maintainability | 20 | Overfitting risk? Hardcoded values? Gotchas documented? Can the Skill evolve without full rewrite? |

### Step 4: Generate Report

```markdown
# Skill Quality Report

## Overall Score: X/100

## 1. Triggering Effectiveness (X/30)
**Key findings:**
- ...

## 2. Structural Compliance (X/25)
**Key findings:**
- ...

## 3. Functional Completeness (X/25)
**Key findings:**
- ...

## 4. Maintainability (X/20)
**Key findings:**
- ...

## Issues (by priority)

| # | Severity | Dimension | Issue | Fix |
|---|----------|-----------|-------|-----|
| 1 | P0 | Structure | ... | ... |

## Recommendations

1. [P0] ...
2. [P1] ...
3. [P2] ...

## Verdict

[Healthy / Needs work / Requires rewrite]
```

### Severity Definitions

| Level | Meaning |
|-------|---------|
| P0 | Blocks triggering or violates official spec — Skill may not load |
| P1 | Degrades quality — Skill loads but performs poorly |
| P2 | Best practice — Not urgent but worth fixing |

## Key Rules Reference (from Anthropic Official Guide)

- `name`: kebab-case, <= 64 chars, must match folder name
- `description`: WHAT + WHEN, <= 1024 chars, include trigger phrases
- SKILL.md filename is case-sensitive
- No XML angle brackets anywhere in frontmatter
- No "claude" or "anthropic" in skill names
- SKILL.md body < 500 lines (use references/ for more)
- No README.md inside skill folder

## When NOT to Use This Skill

- User wants to CREATE a new Skill — use skill-creator instead
- User wants to improve Skill triggering — use description optimization
- User wants to test Skill on real inputs — use the Skill testing workflow
