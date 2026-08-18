#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "flicker-workflow",
    "flicker-plan",
    "flicker-implement",
    "flicker-test",
    "flicker-release",
    "flicker-ship",
    "flicker-recall",
    "flicker-triage",
    "flicker-health-watchdog",
}

found = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
assert found == EXPECTED, f"skill inventory differs: found={sorted(found)}"

for name in sorted(EXPECTED):
    body = (SKILLS / name / "SKILL.md").read_text()
    assert body.startswith("---\n"), f"{name}: missing frontmatter"
    assert re.search(r"^name: " + re.escape(name) + r"$", body, re.MULTILINE), f"{name}: wrong name"
    assert re.search(r"^description: .+$", body, re.MULTILINE), f"{name}: missing description"
    assert "Generated from orlando-umbrella/flicker" not in body, f"{name}: still marked generated"
    assert "/Users/" not in body and "~/Sites/" not in body, f"{name}: private path leaked"

health = (SKILLS / "flicker-health-watchdog" / "SKILL.md").read_text()
triage = (SKILLS / "flicker-triage" / "SKILL.md").read_text()
assert "do not use for suggestion inbox triage" in health.lower()
assert "do not use for" in triage.lower() and "changing code" in triage.lower()
assert "do not mutate infrastructure" in health.lower()
assert "GET /api/v1/projects/<project>/suggestions?status=open" in triage

print(f"PASS: {len(EXPECTED)} canonical public skills")
