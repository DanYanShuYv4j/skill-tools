# Skill Quality Checklist

Detailed check items for each evaluation dimension.

## 1. Triggering Effectiveness (30 pts)

### Description Quality (15 pts)
- [ ] Description includes WHAT the skill does AND WHEN to trigger (not just a summary)
- [ ] Specific trigger phrases present (user language, not technical jargon)
- [ ] Description doesn't leak workflow steps that enable shortcut behavior
- [ ] No ambiguity — a different evaluator would agree on when this should trigger
- [ ] Near-miss queries considered (e.g., "analyze design" should NOT trigger a PDF skill)

### Trigger Coverage (15 pts)
- [ ] Obvious triggers covered (exact keyword matches)
- [ ] Paraphrased triggers covered (different phrasing, same intent)
- [ ] Negative space defined — when should this NOT trigger
- [ ] Contextual triggers covered (file types, project state, preceding actions)
- [ ] Description is under 1024 characters

## 2. Structural Compliance (25 pts)

### Frontmatter & Metadata (10 pts)
- [ ] `name` is kebab-case, matches folder name, <= 64 chars
- [ ] `description` field is present and valid YAML
- [ ] No XML angle brackets in frontmatter
- [ ] No reserved words ("claude", "anthropic") in name
- [ ] `---` delimiters correct on both sides of frontmatter

### Progressive Disclosure (10 pts)
- [ ] SKILL.md body under 500 lines
- [ ] Detailed content moved to `references/` where appropriate
- [ ] Clear pointers in body about when to read reference files
- [ ] No README.md inside skill folder (not a valid skill file)

### File Organization (5 pts)
- [ ] Folder name matches `name` field exactly
- [ ] SKILL.md filename case-correct (S-K-I-L-L uppercase, .md lowercase)
- [ ] Scripts in `scripts/`, references in `references/`, assets in `assets/`

## 3. Functional Completeness (25 pts)

### Instruction Quality (10 pts)
- [ ] Instructions are actionable (not vague "help the user with X")
- [ ] Error handling guidance present (what to do when things fail)
- [ ] Examples provided for key operations
- [ ] Output format specified where relevant

### Edge Case Coverage (10 pts)
- [ ] Empty/missing input handled
- [ ] Invalid input handled (wrong format, unsupported types)
- [ ] Concurrent/modified-during-execution scenarios considered
- [ ] Skill composition — works alongside other skills without conflict

### Verification (5 pts)
- [ ] Success criteria defined (how to know the skill worked)
- [ ] Self-check or validation step included
- [ ] Testing approach suggested

## 4. Maintainability (20 pts)

### Overfitting Prevention (10 pts)
- [ ] No hardcoded paths, filenames, or environment-specific values
- [ ] Instructions explain WHY not just WHAT
- [ ] Patterns generalized — not tuned to a single test case
- [ ] Version-specific references avoided or versioned properly

### Evolution Readiness (10 pts)
- [ ] Gotchas documented (model tendencies, common mistakes)
- [ ] Clear what CAN change (parameters) vs what MUST NOT change (core workflow)
- [ ] Instructions are modular — parts can be updated independently
- [ ] No silent assumptions about tools, MCP servers, or environment

## Quick Reference: Official Spec Violations

These are automatic P0 issues per Anthropic's official guide:

- [ ] SKILL.md filename not exact (wrong case, wrong extension)
- [ ] XML angle brackets in frontmatter
- [ ] "claude" or "anthropic" in skill name
- [ ] Missing or malformed YAML frontmatter
- [ ] name doesn't match folder name
- [ ] Description missing or exceeds 1024 chars
