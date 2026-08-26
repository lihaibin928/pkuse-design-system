### Task 1: Skill entry and design references

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/SKILL.md`
- Create: `.cursor/skills/pkuse-design-generator/references/ant-design-v6.md`
- Create: `.cursor/skills/pkuse-design-generator/references/design-system.md`
- Create: `.cursor/skills/pkuse-design-generator/tests/test_skill_structure.py`

**Interfaces:**
- Consumes: approved design specification.
- Produces: discoverable Skill metadata and `references/design-system.md` rules used by all later tasks.

- [ ] **Step 1: Write the failing structure test**

```python
# .cursor/skills/pkuse-design-generator/tests/test_skill_structure.py
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]


class SkillStructureTest(unittest.TestCase):
    def test_skill_metadata_and_references(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(skill, r"(?m)^name: pkuse-design-generator$")
        self.assertIn("qiankun", skill.lower())
        self.assertIn("后台", skill)
        for name in (
            "ant-design-v6.md",
            "design-system.md",
            "qiankun-contract.md",
            "page-patterns.md",
            "engineering.md",
        ):
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_overlay_links_to_source_without_duplicating_it(self) -> None:
        source = (ROOT / "references/ant-design-v6.md").read_text(encoding="utf-8")
        overlay = (ROOT / "references/design-system.md").read_text(encoding="utf-8")
        self.assertIn("https://ant.design/design.md", source)
        self.assertIn("Natural", source)
        self.assertIn("ant-design-v6.md", overlay)
        self.assertLess(len(overlay), len(source))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the missing files fail**

Run:

```bash
python -m unittest discover .cursor/skills/pkuse-design-generator/tests -p 'test_skill_structure.py' -v
```

Expected: `FileNotFoundError` for `SKILL.md`.

- [ ] **Step 3: Save the Ant Design source snapshot**

Fetch `https://ant.design/design.md` and save it verbatim after this provenance header:

```markdown
<!--
Source: https://ant.design/design.md
Captured: 2026-08-18
Runtime baseline verified: antd 6.6.1
-->
```

- [ ] **Step 4: Create the Skill entry**

```markdown
---
name: pkuse-design-generator
description: Generates complete enterprise React admin sub-applications using Vite, TypeScript, Ant Design and qiankun. Use whenever the user asks to create a 后台管理系统、管理控制台、qiankun 子应用、CRUD 数据平台、审批中心、运营看板、系统配置或监控运维应用, even when they do not explicitly ask for a design-system generator.
---

# PKUSE Design Generator

Generate a complete, runnable sub-application rather than a component showcase.

## Workflow

1. Classify the request using `references/page-patterns.md`.
2. Ask only for missing information that changes the architecture: app name, core entity, roles, critical actions, or unusual fields.
3. Read `references/design-system.md`, `references/qiankun-contract.md`, and `references/engineering.md`.
4. Run `python scripts/scaffold.py --name <kebab-name> --title "<title>" --scene <scene> --output <path>`.
5. Generate domain pages, route/menu/permission declarations, service contracts, Mock data, and API adapters.
6. Run `python scripts/validate.py <path> --run-commands`.
7. Fix every reported error and rerun validation.
8. Report the output path, commands, local roles, selected patterns, checks, and real API replacement list.

## Design decisions

- Read `references/ant-design-v6.md` when choosing tokens, component semantics, density, state treatment, or customization.
- Keep one primary action per decision surface.
- Include loading, empty, error, disabled, and permission-denied states.
- Pages depend on typed services, never Mock files.
- Keep qiankun-specific behavior inside `src/micro-app/`.

## Output summary

Return:

- Generated path
- `pnpm install` and `pnpm dev` commands
- Standalone and qiankun entry instructions
- Roles and permissions
- Validation results
- APIs that still use Mock implementations
```

- [ ] **Step 5: Create the PKUSE overlay**

```markdown
# PKUSE generation rules

Use [the captured Ant Design v6 specification](ant-design-v6.md) as the visual and interaction baseline.

## Required rules

- Preserve Natural, Certain, Meaningful, and Growing as decision criteria.
- Use `ConfigProvider` tokens; do not hard-code colors or token-expressible spacing.
- Keep spacing on the 4 px grid and use the default 14 px enterprise density.
- Keep one primary button per decision surface.
- Use preset colors for categories, semantic colors for status, and primary color for the dominant action.
- Use Ant Design components for tables, forms, navigation, overlays, and feedback before creating custom equivalents.
- Include hover, focus, loading, empty, error, disabled, and permission-denied states.
- Namespace CSS and configure an application-specific `prefixCls` and CSS variable key.
```

- [ ] **Step 6: Run the structure test**

Run the same unittest command. Expected: failure only for the three references created in later tasks; no metadata or overlay assertion failures.

