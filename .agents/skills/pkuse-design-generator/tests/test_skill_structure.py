# .agents/skills/pkuse-design-generator/tests/test_skill_structure.py
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
            "DESIGN.md",
        ):
            self.assertTrue((ROOT / "references" / name).is_file(), name)
        self.assertTrue((ROOT / "references/antd/llms-full-cn.txt").is_file())
        self.assertTrue((ROOT / "references/antd/llms-semantic-cn.md").is_file())
        self.assertTrue((ROOT / "references/components/INDEX.md").is_file())
        self.assertTrue((ROOT / "references/components/button.md").is_file())
        self.assertTrue((ROOT / "references/components/table.md").is_file())
        self.assertGreaterEqual(len(list((ROOT / "references/components").glob("*.md"))), 60)
        self.assertIn("components/INDEX.md", skill)
        self.assertIn("不要整份阅读", skill)

    def test_design_spec_merges_overlay_and_baseline(self) -> None:
        source = (ROOT / "references/ant-design-v6.md").read_text(encoding="utf-8")
        design = (ROOT / "references/DESIGN.md").read_text(encoding="utf-8")
        self.assertIn("https://ant.design/design.md", source)
        self.assertIn("Natural", source)
        self.assertIn("# Pkuse Design 设计规范", design)
        self.assertIn("## Pkuse 生成规则", design)
        self.assertIn("## Ant Design v6 基线规范", design)
        self.assertIn("#1677FF", design)
        self.assertIn("概述", design)
        self.assertIn("components/INDEX.md", design)

    def test_component_files_drop_abstract_dom_and_keep_when_to_use(self) -> None:
        button = (ROOT / "references/components/button.md").read_text(encoding="utf-8")
        self.assertIn("何时使用", button)
        self.assertIn("一个操作区域只能有一个主按钮", button)
        self.assertIn("语义槽", button)
        self.assertNotIn("Abstract DOM", button)
        for path in (ROOT / "references/components").glob("*.md"):
            self.assertNotIn("Abstract DOM Structure", path.read_text(encoding="utf-8"), path.name)


if __name__ == "__main__":
    unittest.main()
