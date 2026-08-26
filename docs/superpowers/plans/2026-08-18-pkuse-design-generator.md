# PKUSE Design Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a project-level Cursor Skill that generates complete React/Vite/TypeScript/Ant Design qiankun admin sub-applications from six enterprise scenario patterns.

**Architecture:** Keep `SKILL.md` as the orchestration layer, load design and engineering references only when relevant, and use Python standard-library scripts plus versioned template assets for deterministic scaffolding and validation. Generated applications isolate qiankun integration behind an adapter and keep pages dependent on typed service contracts rather than Mock implementations.

**Tech Stack:** Cursor Agent Skills, Markdown, Python 3.11+ standard library, React, Vite, TypeScript, Ant Design 6, React Router, qiankun 2.x, pnpm, Vitest.

## Global Constraints

- Skill name and directory are exactly `pkuse-design-generator`.
- Store the Skill at `.cursor/skills/pkuse-design-generator/`.
- Generated applications use React + Vite + TypeScript + Ant Design + React Router + pnpm.
- Generated applications support standalone and qiankun-mounted modes.
- Use Ant Design v6 design rules from `https://ant.design/design.md`.
- Preserve the complete Ant Design source snapshot and keep PKUSE decisions in a separate overlay.
- Include Mock data, a replaceable API adapter, and route/menu/action RBAC.
- Support data management, approval, dashboard, system configuration, monitoring, and generic-composition scenarios.
- Do not initialize git or create commits unless the user explicitly requests it.

---

## File Map

```text
.cursor/skills/pkuse-design-generator/
├── SKILL.md
├── references/
│   ├── ant-design-v6.md
│   ├── design-system.md
│   ├── qiankun-contract.md
│   ├── page-patterns.md
│   └── engineering.md
├── assets/
│   ├── base-app/
│   │   ├── package.json.tpl
│   │   ├── index.html.tpl
│   │   ├── vite.config.ts.tpl
│   │   ├── tsconfig.json
│   │   ├── src/main.tsx.tpl
│   │   ├── src/app/App.tsx.tpl
│   │   ├── src/app/theme.ts
│   │   ├── src/auth/access.ts
│   │   ├── src/micro-app/adapter.tsx.tpl
│   │   ├── src/micro-app/contracts.ts
│   │   ├── src/services/contracts.ts
│   │   ├── src/services/createServices.ts
│   │   └── src/styles/global.css.tpl
│   └── scenarios/
│       ├── data-management.json
│       ├── approval-workflow.json
│       ├── dashboard.json
│       ├── system-config.json
│       ├── monitoring.json
│       └── generic.json
├── scripts/
│   ├── scaffold.py
│   └── validate.py
├── tests/
│   ├── test_skill_structure.py
│   ├── test_scaffold.py
│   └── test_validate.py
└── evals/
    └── evals.json
```

Each reference owns one concern. `scaffold.py` copies and renders stable assets; the agent generates domain pages after scaffolding. `validate.py` checks both static conventions and executable project commands.

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

### Task 2: qiankun, engineering, and page-pattern references

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/references/qiankun-contract.md`
- Create: `.cursor/skills/pkuse-design-generator/references/engineering.md`
- Create: `.cursor/skills/pkuse-design-generator/references/page-patterns.md`

**Interfaces:**
- Consumes: Ant Design overlay from Task 1.
- Produces: generation contracts referenced by `SKILL.md` and scenario manifests.

- [ ] **Step 1: Write the qiankun contract**

The document must define these exact interfaces:

```ts
export interface UserIdentity {
  id: string;
  displayName: string;
  roles: string[];
  permissions: string[];
}

export interface GlobalStateActions {
  onGlobalStateChange?: (
    listener: (state: Record<string, unknown>, previous: Record<string, unknown>) => void,
    fireImmediately?: boolean,
  ) => void;
  setGlobalState?: (state: Record<string, unknown>) => boolean;
  offGlobalStateChange?: () => boolean;
}

export interface MicroAppProps extends GlobalStateActions {
  container?: Element | ShadowRoot;
  routeBase?: string;
  user?: UserIdentity;
  authToken?: string;
  navigate?: (path: string) => void;
}
```

Require `bootstrap`, `mount`, `unmount`, optional `update`, a fresh React Root and Router per mount, scoped container lookup, and cleanup of root, subscriptions, timers, listeners, and aborted requests. Specify standalone `/` routing and injected `routeBase` for embedded mode.

- [ ] **Step 2: Write engineering rules**

Define:

```text
src/
├── app/             composition, providers, theme
├── auth/            access checks and permission declarations
├── features/        business slices; pages live with components and services
├── micro-app/       qiankun adapter and contracts
├── mocks/           development-only adapters and fixtures
├── routes/          one declaration feeding router and menu
├── services/        shared HTTP transport and contracts
└── styles/          namespaced global baseline only
```

Require strict TypeScript, feature-local tests, typed service injection, AbortController support, Error Boundary, distinct 401/403/404/5xx handling, and route/menu/action RBAC derived from shared permission constants.

- [ ] **Step 3: Write all six page patterns**

Use this exact schema for every section:

```markdown
## <scene-id>

- Trigger signals:
- Primary user task:
- Required routes:
- Required page states:
- Required Ant Design patterns:
- Required permissions:
- Avoid:
```

Define:

- `data-management`: filters, table, detail, create/edit drawer, batch action.
- `approval-workflow`: queue, detail, timeline, comments, approve/reject confirmation.
- `dashboard`: metric cards, trends, ranking, filters, anomaly list.
- `system-config`: organization tree, users, roles, permission matrix, parameters.
- `monitoring`: status overview, resources, logs, alerts, operation history.
- `generic`: infer entities and compose existing patterns without inventing a new visual language.

- [ ] **Step 4: Run the structure test**

Expected: all tests in `test_skill_structure.py` pass.

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

### Task 4: Runnable base application and qiankun adapter

**Files:**
- Create: all files listed under `assets/base-app/` in the File Map.
- Modify: `.cursor/skills/pkuse-design-generator/tests/test_scaffold.py`

**Interfaces:**
- Consumes: `MicroAppProps`, `createServices(mode)`, and template replacement values.
- Produces: a standalone Vite app with `bootstrap`, `mount`, `unmount`, and `update`.

- [ ] **Step 1: Extend scaffold tests for runtime invariants**

```python
def test_generated_runtime_has_dual_mode_and_cleanup(self) -> None:
    with TemporaryDirectory() as temp:
        output = Path(temp) / "ops-console"
        MODULE.scaffold("ops-console", "运维中心", "monitoring", output)
        adapter = (output / "src/micro-app/adapter.tsx").read_text(encoding="utf-8")
        package = (output / "package.json").read_text(encoding="utf-8")
        self.assertIn("export async function bootstrap", adapter)
        self.assertIn("export async function mount", adapter)
        self.assertIn("export async function unmount", adapter)
        self.assertIn("root?.unmount()", adapter)
        self.assertIn("offGlobalStateChange?.()", adapter)
        self.assertIn('"antd": "^6', package)
```

- [ ] **Step 2: Create package and build configuration templates**

`package.json.tpl` must define:

```json
{
  "name": "__APP_NAME__",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "typecheck": "tsc -b --pretty false",
    "test": "vitest run"
  },
  "dependencies": {
    "@ant-design/icons": "^6.0.0",
    "antd": "^6.0.0",
    "qiankun": "^2.10.16",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "^5.0.0",
    "vite": "^7.0.0",
    "vite-plugin-qiankun": "^1.0.15",
    "vitest": "^3.0.0"
  }
}
```

During implementation, add dependencies with `pnpm add` rather than inventing patch versions; retain major-version floors in this template and commit the generated lockfile only if the user later requests repository commits.

- [ ] **Step 3: Create runtime contracts**

```ts
// src/micro-app/contracts.ts
export interface UserIdentity {
  id: string;
  displayName: string;
  roles: string[];
  permissions: string[];
}

export interface GlobalStateActions {
  onGlobalStateChange?: (
    listener: (state: Record<string, unknown>, previous: Record<string, unknown>) => void,
    fireImmediately?: boolean,
  ) => void;
  setGlobalState?: (state: Record<string, unknown>) => boolean;
  offGlobalStateChange?: () => boolean;
}

export interface MicroAppProps extends GlobalStateActions {
  container?: Element | ShadowRoot;
  routeBase?: string;
  user?: UserIdentity;
  authToken?: string;
  navigate?: (path: string) => void;
}
```

- [ ] **Step 4: Create the lifecycle adapter**

```tsx
// src/micro-app/adapter.tsx.tpl
import { createRoot, type Root } from "react-dom/client";
import { App } from "../app/App";
import type { MicroAppProps } from "./contracts";

let root: Root | undefined;
let activeProps: MicroAppProps | undefined;

function getMountElement(props: MicroAppProps): Element {
  const element = props.container
    ? props.container.querySelector("[data-pkuse-root='__APP_NAME__']")
    : document.querySelector("[data-pkuse-root='__APP_NAME__']");
  if (!element) throw new Error("Mount element not found for __APP_NAME__");
  return element;
}

export function render(props: MicroAppProps = {}): void {
  activeProps = props;
  root = createRoot(getMountElement(props));
  root.render(<App props={props} title="__APP_TITLE__" />);
}

export async function bootstrap(): Promise<void> {}

export async function mount(props: MicroAppProps): Promise<void> {
  render(props);
}

export async function unmount(): Promise<void> {
  activeProps?.offGlobalStateChange?.();
  root?.unmount();
  root = undefined;
  activeProps = undefined;
}

export async function update(props: MicroAppProps): Promise<void> {
  await unmount();
  render(props);
}
```

- [ ] **Step 5: Create Vite adaptation, standalone entry, and app providers**

`vite.config.ts.tpl` integrates the community adapter behind Vite configuration:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import qiankun from "vite-plugin-qiankun";

export default defineConfig({
  plugins: [react(), qiankun("__APP_NAME__", { useDevMode: true })],
  server: {
    cors: true,
    headers: { "Access-Control-Allow-Origin": "*" },
  },
});
```

`src/main.tsx.tpl` registers the isolated adapter with the plugin and starts locally only in standalone mode:

```tsx
import { qiankunWindow, renderWithQiankun } from "vite-plugin-qiankun/dist/helper";
import { bootstrap, mount, render, unmount, update } from "./micro-app/adapter";
import "./styles/global.css";

renderWithQiankun({ bootstrap, mount, unmount, update });

if (!qiankunWindow.__POWERED_BY_QIANKUN__) {
  render();
}

export { bootstrap, mount, unmount, update };
```

`App.tsx.tpl` creates a Router per render and wraps routes in `ConfigProvider`, `App`, and an Error Boundary. Embedded mode renders business content without duplicating the host shell; standalone mode renders a compact local header and navigation. Keeping plugin imports in `main.tsx` ensures pages and domain modules remain independent of the Vite/qiankun bridge.

- [ ] **Step 6: Create theme, RBAC, services, and namespaced CSS**

Implement:

```ts
export function can(permissions: readonly string[], required?: string): boolean {
  return required === undefined || permissions.includes(required);
}
```

```ts
export interface ServiceResult<T> {
  data: T;
  requestId: string;
}

export interface EntityService<T> {
  list(signal?: AbortSignal): Promise<ServiceResult<T[]>>;
  get(id: string, signal?: AbortSignal): Promise<ServiceResult<T>>;
}
```

`theme.ts` exports an Ant Design `ThemeConfig` without hard-coded page-level colors. `global.css.tpl` scopes custom selectors under `[data-pkuse-app="__APP_NAME__"]`.

- [ ] **Step 7: Run scaffold tests and build a fixture**

Run:

```bash
python -m unittest .cursor/skills/pkuse-design-generator/tests/test_scaffold.py -v
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name inventory-console \
  --title "库存中心" \
  --scene data-management \
  --output /tmp/pkuse-inventory-console
cd /tmp/pkuse-inventory-console && pnpm install && pnpm typecheck && pnpm build
```

Expected: all unittests pass, TypeScript exits `0`, and Vite writes `dist/`.

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

### Task 6: Skill evaluation cases and review workflow

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/evals/evals.json`
- Create during execution: `.cursor/skills/pkuse-design-generator-workspace/iteration-1/**`

**Interfaces:**
- Consumes: completed Skill and Skill Creator evaluation scripts.
- Produces: three with-Skill outputs, three baseline outputs, grades, timing, `benchmark.json`, and human review UI.

- [ ] **Step 1: Create realistic evaluation prompts**

```json
{
  "skill_name": "pkuse-design-generator",
  "evals": [
    {
      "id": 1,
      "prompt": "为仓储团队生成一个名为 inventory-console 的 qiankun 子应用。需要商品和库存列表、多条件筛选、库存详情、调整库存抽屉、批量盘点；仓库管理员可编辑，审计员只读。使用 Mock，但提供可替换 API。",
      "expected_output": "A buildable data-management app with dual runtime, typed services, Mock adapter and RBAC.",
      "files": []
    },
    {
      "id": 2,
      "prompt": "创建 expense-approval-center 费用报销审批子应用。员工查看自己的申请，经理处理待办，财务复核；详情要有流程时间线、票据摘要、意见和通过/驳回确认。应用既能独立运行也能挂到 qiankun。",
      "expected_output": "A buildable approval app with role-specific routes/actions and explicit workflow states.",
      "files": []
    },
    {
      "id": 3,
      "prompt": "生成 service-ops-console 运维监控子应用，包含服务健康概览、实例列表、日志检索、告警详情、确认告警和操作审计。值班人员可确认告警，访客只读。遵循 Ant Design v6 规范。",
      "expected_output": "A buildable monitoring app with scenario-appropriate information architecture and permissions.",
      "files": []
    }
  ]
}
```

- [ ] **Step 2: Launch six runs in one turn**

For each prompt, launch one agent with:

```text
Skill path: .cursor/skills/pkuse-design-generator
Save outputs to: .cursor/skills/pkuse-design-generator-workspace/iteration-1/<eval-name>/with_skill/outputs/
```

Launch the matching baseline without a Skill and save under `without_skill/outputs/`. Capture each completion's token and duration values immediately in its `timing.json`.

- [ ] **Step 3: Add objective assertions while runs execute**

Each `eval_metadata.json` must assert:

- `pnpm typecheck`, `pnpm test`, and `pnpm build` succeed.
- lifecycle adapter exports `bootstrap`, `mount`, and `unmount`.
- application supports standalone rendering.
- route, menu, and action permissions use shared permission declarations.
- pages import service contracts and do not import Mock fixtures.
- `ConfigProvider` exists and page code has no hard-coded color.
- loading, empty, error, and forbidden states exist.
- README lists host integration and API replacement points.

- [ ] **Step 4: Grade and aggregate**

Run deterministic build and static checks first, then write `grading.json` with exact `text`, `passed`, and `evidence` keys. Aggregate:

```bash
cd /Users/eric/.claude/skills/skill-creator
python -m scripts.aggregate_benchmark \
  /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1 \
  --skill-name pkuse-design-generator
```

Expected: `benchmark.json` and `benchmark.md` exist and list with-Skill results before baselines.

- [ ] **Step 5: Open the required review UI**

```bash
python /Users/eric/.claude/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1 \
  --skill-name "pkuse-design-generator" \
  --benchmark /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1/benchmark.json
```

Ask the user to review Outputs and Benchmark. Do not revise the Skill until human feedback is received.

### Task 7: Feedback iteration and final verification

**Files:**
- Modify: Skill files identified by evaluation evidence and user feedback.
- Create: `.cursor/skills/pkuse-design-generator-workspace/iteration-2/**`

**Interfaces:**
- Consumes: `feedback.json`, benchmark analyst notes, and run transcripts.
- Produces: improved Skill, second comparison, and final verification evidence.

- [ ] **Step 1: Read feedback and classify causes**

For every non-empty review, map the issue to one of:

- missing instruction in `SKILL.md`
- missing design or scenario guidance
- unstable deterministic template
- validator blind spot
- evaluation-only variance

Change the smallest general rule or reusable asset that addresses the cause; do not special-case an evaluation's names or fields.

- [ ] **Step 2: Rerun local tests**

```bash
python -m unittest discover .cursor/skills/pkuse-design-generator/tests -v
rm -rf /tmp/pkuse-inventory-console
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name inventory-console \
  --title "库存中心" \
  --scene data-management \
  --output /tmp/pkuse-inventory-console
cd /tmp/pkuse-inventory-console
pnpm install
pnpm typecheck
pnpm test
pnpm build
```

Expected: all commands exit `0`.

- [ ] **Step 3: Rerun all comparison cases**

Create `iteration-2` with the same prompts and baseline policy. Aggregate and launch the viewer with:

```bash
python /Users/eric/.claude/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-2 \
  --skill-name "pkuse-design-generator" \
  --benchmark /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-2/benchmark.json \
  --previous-workspace /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1
```

- [ ] **Step 4: Final self-check**

Run:

```bash
python -m unittest discover .cursor/skills/pkuse-design-generator/tests -v
python .cursor/skills/pkuse-design-generator/scripts/validate.py \
  /tmp/pkuse-inventory-console --run-commands
```

Confirm:

- Skill metadata triggers on all six scenario families.
- `SKILL.md` remains below 500 lines.
- every linked reference and script exists.
- full Ant Design source and PKUSE overlay remain separate.
- all three generated applications build and pass validation.
- user feedback is empty or explicitly accepts remaining trade-offs.

## Execution Notes

This directory is not currently a git repository. The implementation may create and verify files, but it must not initialize git or commit unless the user separately authorizes those actions.
