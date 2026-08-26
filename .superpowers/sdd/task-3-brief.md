### Task 3: Deterministic scaffold engine and scenario manifests

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/scripts/scaffold.py`
- Create: `.cursor/skills/pkuse-design-generator/assets/scenarios/*.json`
- Create: `.cursor/skills/pkuse-design-generator/tests/test_scaffold.py`

**Interfaces:**
- Consumes: `ScenarioManifest` JSON and `.tpl` files.
- Produces: `scaffold(name: str, title: str, scene: str, output: Path) -> Path`.

- [ ] **Step 1: Write failing scaffold tests**

```python
# .cursor/skills/pkuse-design-generator/tests/test_scaffold.py
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("scaffold", ROOT / "scripts/scaffold.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ScaffoldTest(unittest.TestCase):
    def test_renders_templates_and_scene_manifest(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "inventory-console"
            MODULE.scaffold("inventory-console", "库存中心", "data-management", output)
            package = (output / "package.json").read_text(encoding="utf-8")
            main = (output / "src/main.tsx").read_text(encoding="utf-8")
            manifest = (output / "src/generated/scene.json").read_text(encoding="utf-8")
            self.assertIn('"name": "inventory-console"', package)
            self.assertIn("库存中心", main)
            self.assertIn('"scene": "data-management"', manifest)
            self.assertNotIn("__APP_", package + main)

    def test_rejects_invalid_name_and_existing_output(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "target"
            output.mkdir()
            with self.assertRaisesRegex(ValueError, "kebab-case"):
                MODULE.scaffold("Bad Name", "Bad", "dashboard", Path(temp) / "new")
            with self.assertRaisesRegex(FileExistsError, "already exists"):
                MODULE.scaffold("valid-name", "Valid", "dashboard", output)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run and verify failure**

Run:

```bash
python -m unittest .cursor/skills/pkuse-design-generator/tests/test_scaffold.py -v
```

Expected: import fails because `scripts/scaffold.py` is absent.

- [ ] **Step 3: Implement the scaffold engine**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parents[1]
TEMPLATES = ROOT / "assets/base-app"
SCENARIOS = ROOT / "assets/scenarios"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def scaffold(name: str, title: str, scene: str, output: Path) -> Path:
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("application name must use kebab-case")
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    scenario_path = SCENARIOS / f"{scene}.json"
    if not scenario_path.is_file():
        choices = ", ".join(sorted(path.stem for path in SCENARIOS.glob("*.json")))
        raise ValueError(f"unknown scene {scene!r}; choose one of: {choices}")

    values = {
        "__APP_NAME__": name,
        "__APP_TITLE__": title,
        "__APP_PREFIX__": name.replace("-", "_"),
    }
    output.mkdir(parents=True)
    for source in TEMPLATES.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(TEMPLATES)
        target_name = relative.name.removesuffix(".tpl")
        target = output / relative.parent / target_name
        target.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_text(encoding="utf-8")
        for token, value in values.items():
            content = content.replace(token, value)
        target.write_text(content, encoding="utf-8")

    generated = output / "src/generated"
    generated.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(scenario_path, generated / "scene.json")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(scaffold(args.name, args.title, args.scene, args.output))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create six scenario manifests**

Each JSON file follows:

```json
{
  "scene": "data-management",
  "routes": ["list", "detail"],
  "patterns": ["query-form", "data-table", "edit-drawer"],
  "states": ["loading", "empty", "error", "forbidden"],
  "permissions": ["read", "create", "update", "delete", "batch"]
}
```

Use scene-specific route, pattern, and permission values matching `page-patterns.md`. `generic.json` uses empty arrays plus `"composeFromRequest": true`.

- [ ] **Step 5: Run scaffold tests**

Expected: imports succeed; tests fail only because `assets/base-app` is not yet present.

