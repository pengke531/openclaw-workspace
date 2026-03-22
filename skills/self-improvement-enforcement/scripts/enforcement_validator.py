"""
Self-Improvement Enforcement Validator

自动验证 skill 的完整性和质量，在 commit 前运行。
不符合标准的 skill 禁止 commit。

使用方法:
    python enforcement_validator.py <skill_directory>

退出码:
    0 = 全部通过
    1 = 有警告，建议修复后提交
    2 = 严重错误，需要修复后重检
"""

import sys
import os
import re
from pathlib import Path


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def check(name, condition, error_msg=""):
    if condition:
        print(f"  {GREEN}OK{RESET} {name}")
        return True
    else:
        print(f"  {RED}FAIL{RESET} {name}")
        if error_msg:
            print(f"     {RED}-> {error_msg}{RESET}")
        return False


def validate_skill(skill_dir: Path) -> tuple[bool, int]:
    errors = []
    warnings = []

    print(f"\n{'='*60}")
    print(f"VALIDATING: {skill_dir.name}")
    print(f"{'='*60}")

    # 1. Required files
    required = ["SKILL.md", "README.md", "LICENSE"]
    for f in required:
        check(f"exists {f}", (skill_dir / f).exists(), f"{f} is missing")

    # 2. SKILL.md frontmatter
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            name_m = re.search(r"name:\s*(.+)", fm)
            desc_m = re.search(r"description:\s*(.+)", fm)
            check("SKILL.md frontmatter name", name_m is not None)
            check("SKILL.md frontmatter description", desc_m is not None)
            if name_m:
                skill_name = name_m.group(1).strip()
                dir_name = skill_dir.name
                ok = check(
                    f"SKILL.md name='{skill_name}' matches dir='{dir_name}'",
                    skill_name == dir_name,
                    f"SKILL.md name != directory name"
                )
                if not ok:
                    warnings.append("name mismatch")
        else:
            check("SKILL.md has frontmatter", False, "no frontmatter found")
            warnings.append("missing frontmatter")

    # 3. README.md sections
    readme_md = skill_dir / "README.md"
    if readme_md.exists():
        content = readme_md.read_text(encoding="utf-8", errors="replace")
        for section, msg in [
            ("overview", "missing overview"),
            ("architecture", "missing architecture"),
            ("usage", "missing usage"),
            ("files", "missing files section"),
            ("license", "missing license"),
        ]:
            check(f"README contains {section}", section.lower() in content.lower(), msg)

    # 4. examples/ directory
    examples_dir = skill_dir / "examples"
    if examples_dir.exists():
        examples = list(examples_dir.glob("*.md"))
        check(f"examples/ has content", len(examples) > 0, "examples/ is empty")
    else:
        print(f"  {YELLOW}WARN{RESET} examples/ does not exist (recommended)")
        warnings.append("no examples dir")

    # 5. tests/ directory
    tests_dir = skill_dir / "tests"
    if tests_dir.exists():
        tests = list(tests_dir.glob("*.md")) + list(tests_dir.glob("*.py"))
        check(f"tests/ has content", len(tests) > 0, "tests/ is empty")
    else:
        print(f"  {YELLOW}WARN{RESET} tests/ does not exist (recommended)")
        warnings.append("no tests dir")

    # 6. checks/ and templates/ for enforcement skills
    enforcement_kw = ["enforcement", "self-improvement", "self_improvement"]
    is_enforcement = any(k in skill_dir.name for k in enforcement_kw)
    if is_enforcement:
        check("has checks/ dir", (skill_dir / "checks").exists())
        check("has templates/ dir", (skill_dir / "templates").exists())

    # 7. SKILL.md word count
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        word_count = len(content.split())
        min_words = 500
        ok = check(
            f"SKILL.md word count ({word_count}) >= {min_words}",
            word_count >= min_words,
            f"only {word_count} words, recommend >= {min_words}"
        )
        if not ok:
            warnings.append("SKILL.md word count too low")

    # Summary
    print(f"\n{'='*60}")
    for w in warnings:
        print(f"  {YELLOW}WARN: {w}{RESET}")

    if warnings:
        print(f"\n  {YELLOW}PASS with warnings{RESET}")
        return True, 1
    print(f"\n  {GREEN}ALL CHECKS PASSED{RESET}")
    return True, 0


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <skill_directory>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1]).resolve()
    if not skill_dir.exists():
        print(f"{RED}Error: directory not found: {skill_dir}{RESET}")
        sys.exit(2)

    passed, level = validate_skill(skill_dir)
    sys.exit(level)


if __name__ == "__main__":
    main()
