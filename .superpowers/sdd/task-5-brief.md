### Task 5: Validator with executable and static checks

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/scripts/validate.py`
- Create: `.cursor/skills/pkuse-design-generator/tests/test_validate.py`

**Interfaces:**
- Consumes: generated project path.
- Produces: `ValidationReport(errors: list[str], warnings: list[str], commands: dict[str, int])`.

- [ ] **Step 1: Write failing validator tests**

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ValidateTest(unittest.TestCase):
    def test_reports_missing_contracts_and_hard_coded_colors(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "src").mkdir()
            (project / "src/page.tsx").write_text(
                "const style = { color: '#1677FF' }; export default style;",
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("lifecycle" in item for item in report.errors))
            self.assertTrue(any("hard-coded color" in item for item in report.errors))

    def test_accepts_scaffolded_contracts(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            adapter = project / "src/micro-app"
            adapter.mkdir(parents=True)
            (adapter / "adapter.tsx").write_text(
                "export async function bootstrap(){};"
                "export async function mount(){};"
                "export async function unmount(){root?.unmount();}",
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertEqual([], report.errors)
```

- [ ] **Step 2: Run and verify import failure**

```bash
python -m unittest .cursor/skills/pkuse-design-generator/tests/test_validate.py -v
```

Expected: import fails because `scripts/validate.py` is absent.

- [ ] **Step 3: Implement validator**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    commands: dict[str, int] = field(default_factory=dict)


def validate(project: Path, run_commands: bool) -> ValidationReport:
    report = ValidationReport()
    source_files = list((project / "src").rglob("*.ts")) + list((project / "src").rglob("*.tsx"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    lifecycle = project / "src/micro-app/adapter.tsx"
    if not lifecycle.is_file() or not all(
        f"function {name}" in combined for name in ("bootstrap", "mount", "unmount")
    ):
        report.errors.append("qiankun lifecycle exports are incomplete")
    elif not any(
        expression in lifecycle.read_text(encoding="utf-8")
        for expression in ("root?.unmount()", "root.unmount()")
    ):
        report.errors.append("unmount does not dispose the React root")

    for path in source_files:
        text = path.read_text(encoding="utf-8")
        if COLOR.search(text) and path.name != "theme.ts":
            report.errors.append(f"hard-coded color outside theme: {path}")
    if "/mocks/" in combined.replace("\\", "/"):
        report.errors.append("application source imports mocks directly")

    if run_commands:
        for command in (("pnpm", "typecheck"), ("pnpm", "test"), ("pnpm", "build")):
            result = subprocess.run(command, cwd=project, check=False)
            report.commands[" ".join(command)] = result.returncode
            if result.returncode:
                report.errors.append(f"command failed: {' '.join(command)}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--run-commands", action="store_true")
    args = parser.parse_args()
    report = validate(args.project, args.run_commands)
    for item in report.errors:
        print(f"ERROR: {item}")
    for item in report.warnings:
        print(f"WARN: {item}")
    raise SystemExit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run validator tests and validate the fixture**

```bash
python -m unittest .cursor/skills/pkuse-design-generator/tests/test_validate.py -v
python .cursor/skills/pkuse-design-generator/scripts/validate.py \
  /tmp/pkuse-inventory-console --run-commands
```

Expected: unittests pass and validator exits `0`.

