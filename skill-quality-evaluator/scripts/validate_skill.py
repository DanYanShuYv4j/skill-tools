#!/usr/bin/env python3
"""
Skill structural validator — checks objective compliance rules.
Runs before the prompt-based evaluator. Zero AI judgment needed.
Usage: python validate_skill.py <path-to-skill-folder>
Exit code 0 = all checks pass. Exit code 1 = violations found.

NO external dependencies — uses only Python stdlib.
"""

import sys, os, re, json

def fail(msg):
    print(f"  FAIL  {msg}")

def ok(msg):
    print(f"  OK    {msg}")

def parse_simple_yaml(text):
    """Parse flat YAML key: value pairs. No external deps."""
    result = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            # Strip quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            result[key] = val
    return result if result else None


def check_skill(skill_dir):
    skill_dir = os.path.abspath(skill_dir)
    folder_name = os.path.basename(skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    violations = []

    print(f"\n=== Validating: {folder_name} ===\n")

    # --- SKILL.md exists ---
    if not os.path.isfile(skill_md):
        fail("SKILL.md not found")
        violations.append("SKILL.md missing")
        return violations
    ok("SKILL.md exists")

    # --- SKILL.md filename exact case ---
    actual_name = os.path.basename(skill_md)
    if actual_name != "SKILL.md":
        fail(f"SKILL.md case mismatch: found '{actual_name}', must be 'SKILL.md'")
        violations.append("SKILL.md case mismatch")
    else:
        ok("SKILL.md filename case correct")

    # --- No README.md ---
    readme = os.path.join(skill_dir, "README.md")
    if os.path.isfile(readme):
        fail("README.md found — not a valid skill file, remove it")
        violations.append("README.md present")
    else:
        ok("No README.md")

    # --- Read SKILL.md ---
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # --- YAML frontmatter ---
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        fail("No valid YAML frontmatter (missing --- delimiters)")
        violations.append("YAML frontmatter missing")
        return violations
    ok("YAML frontmatter delimiters present")

    fm_raw = fm_match.group(1)
    fm = parse_simple_yaml(fm_raw)
    if fm is None:
        fail("YAML frontmatter parse error")
        violations.append("YAML parse error")
        return violations
    ok("YAML frontmatter parse OK")

    # --- name field ---
    name_val = fm.get("name", "")
    if not name_val:
        fail("Missing 'name' in frontmatter")
        violations.append("name missing")
    elif not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name_val):
        fail(f"name '{name_val}' is not kebab-case")
        violations.append("name not kebab-case")
    elif len(name_val) > 64:
        fail(f"name '{name_val}' exceeds 64 chars ({len(name_val)})")
        violations.append("name exceeds 64 chars")
    else:
        ok(f"name '{name_val}' is valid kebab-case")

    # --- name matches folder ---
    if name_val and name_val != folder_name:
        fail(f"name '{name_val}' doesn't match folder '{folder_name}'")
        violations.append("name != folder name")
    elif name_val:
        ok(f"name matches folder name")

    # --- no reserved words ---
    for word in ["claude", "anthropic"]:
        if word in name_val.lower():
            fail(f"name contains reserved word '{word}'")
            violations.append(f"reserved word '{word}' in name")

    # --- description ---
    desc = fm.get("description", "")
    if not desc:
        fail("Missing 'description' in frontmatter")
        violations.append("description missing")
    else:
        desc_len = len(desc)
        if desc_len > 1024:
            fail(f"description {desc_len} chars, exceeds 1024 limit")
            violations.append("description exceeds 1024 chars")
        else:
            ok(f"description present ({desc_len} chars)")

        # Check it contains BOTH what AND when (heuristic)
        has_what = any(kw in desc.lower() for kw in ["生成","create","build","help","guide","generate","evaluate","review","audit","convert","extract"])
        has_when = any(kw in desc.lower() for kw in ["when","use this","trigger","用户","should","适用"])
        if not has_what:
            print(f"  WARN  description may be missing WHAT (no action keywords detected)")
        if not has_when:
            print(f"  WARN  description may be missing WHEN (no trigger keywords detected)")

    # --- No XML tags ---
    if "<" in fm_raw and ">" in fm_raw:
        # Only flag if it looks like an XML tag, not frontmatter syntax
        xml_pattern = re.findall(r"</?\w+[^>]*>", fm_raw)
        if xml_pattern:
            fail(f"XML angle brackets in frontmatter: {xml_pattern}")
            violations.append("XML tags in frontmatter")
        else:
            ok("No XML tags in frontmatter")
    else:
        ok("No angle brackets in frontmatter")

    # --- Body line count ---
    body = content[fm_match.end():].strip()
    body_lines = len(body.split("\n"))
    if body_lines > 500:
        fail(f"Body {body_lines} lines, exceeds 500 limit")
        violations.append("body exceeds 500 lines")
    else:
        ok(f"Body {body_lines} lines (under 500)")

    # --- Required sections heuristic ---
    sections = re.findall(r"^#{1,3}\s+(.+)", body, re.MULTILINE)
    if len(sections) < 2:
        print(f"  WARN  Body has only {len(sections)} section headers, may be too sparse")

    # --- Summary ---
    print(f"\n=== Result: {'PASS' if not violations else 'FAIL'} ===\n")
    if violations:
        print(f"Violations ({len(violations)}):")
        for v in violations:
            print(f"  - {v}")
    else:
        print("All structural checks passed.")

    return violations


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <skill-folder>")
        sys.exit(2)

    violations = check_skill(sys.argv[1])
    sys.exit(1 if violations else 0)
