from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from subprocess import TimeoutExpired
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

SCAFFOLD_SPEC = importlib.util.spec_from_file_location(
    "scaffold", ROOT / "scripts/scaffold.py"
)
SCAFFOLD = importlib.util.module_from_spec(SCAFFOLD_SPEC)
assert SCAFFOLD_SPEC and SCAFFOLD_SPEC.loader
sys.modules[SCAFFOLD_SPEC.name] = SCAFFOLD
SCAFFOLD_SPEC.loader.exec_module(SCAFFOLD)

REAL_APP_TS = """
export const qiankun = {
  async bootstrap() {},
  async mount() {},
  async unmount() {},
};
export async function getInitialState() {
  return { name: "app" };
}
export const layout = () => ({
  menuRender: false,
  menuHeaderRender: false,
});
""".strip()

REAL_UMIRC = """
export default {
  antd: {},
  access: {},
  qiankun: { slave: {} },
};
""".strip()


def _executed_commands(run_mock: Mock) -> list[str]:
    return [" ".join(call.args[0]) for call in run_mock.call_args_list]


def _write_package_json(project: Path, scripts: dict[str, str] | None = None) -> None:
    (project / "package.json").write_text(
        json.dumps({"scripts": scripts or {}}),
        encoding="utf-8",
    )


def _write_umirc(project: Path, body: str | None = None) -> None:
    (project / ".umirc.ts").write_text(body or REAL_UMIRC, encoding="utf-8")


def _write_app_runtime(project: Path, body: str | None = None) -> None:
    src = project / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "app.ts").write_text(body or REAL_APP_TS, encoding="utf-8")


def _write_contract_compliant_project(project: Path) -> None:
    _write_package_json(project, {"build": "exit 0"})
    _write_umirc(project)
    _write_app_runtime(project)
    (project / "src/router").mkdir(parents=True, exist_ok=True)
    (project / "src/access.ts").write_text(
        "export default () => ({ canViewUser: true, canEditUser: true });\n",
        encoding="utf-8",
    )
    (project / "src/router/routes.ts").write_text(
        """
export default [
  { path: "/user/list", component: "./User/UserList", access: "canViewUser" },
];
""".strip(),
        encoding="utf-8",
    )
    home = project / "src/features/home/HomePage.tsx"
    home.parent.mkdir(parents=True, exist_ok=True)
    home.write_text(
        """
import { Access, useAccess } from "@umijs/max";
import { Button, Empty, Result, Spin } from "antd";
import { useEffect, useState } from "react";
export function HomePage({ service }) {
  const access = useAccess();
  const [state, setState] = useState("loading");
  useEffect(() => { void service.list(); }, [service]);
  if (state === "loading") { return <Spin tip="loading" />; }
  if (state === "forbidden") { return <Result status="403" title="denied" />; }
  if (state === "error") { return <Result status="error" title="failed" />; }
  if (state === "empty") { return <Empty description="none" />; }
  return (
    <Access accessible={access.canEditUser}>
      <Button>Edit</Button>
    </Access>
  );
}
""".strip(),
        encoding="utf-8",
    )


class TokenizerTest(unittest.TestCase):
    def test_string_token_metadata(self) -> None:
        lex = MODULE.tokenize('const x = "abc";')
        self.assertEqual(1, len(lex.strings))
        self.assertEqual("abc", lex.strings[0].value)
        self.assertEqual('"', lex.strings[0].quote)

    def test_masks_template_expression_string(self) -> None:
        source = "const x = `${\"<ConfigProvider>\"}`;"
        view = MODULE.to_code_only_view(source)
        self.assertNotIn("ConfigProvider", view)

    def test_masks_comment_inside_template_expression(self) -> None:
        source = "const x = `${/* fake export */ 1}`;"
        view = MODULE.to_code_only_view(source)
        self.assertNotIn("fake export", view)
        self.assertIn("1", view)

    def test_masks_nested_template_literal(self) -> None:
        source = "const x = `outer ${`inner ${\"secret\"}` end`;"
        view = MODULE.to_code_only_view(source)
        self.assertNotIn("secret", view)
        self.assertNotIn("inner", view)

    def test_template_brace_in_string_does_not_close_expression(self) -> None:
        source = r'const x = `${"}"; realCode()}`;'
        view = MODULE.to_code_only_view(source)
        self.assertIn("realCode()", view)

    def test_template_brace_in_comment_does_not_close_expression(self) -> None:
        source = r"const x = `${/* } */ realCode()}`;"
        view = MODULE.to_code_only_view(source)
        self.assertIn("realCode()", view)
        self.assertNotIn("}", view.split("realCode()")[0][-5:])

    def test_template_nested_brace_in_string(self) -> None:
        source = r'const x = `nested ${`inner ${"{"}` end`;'
        view = MODULE.to_code_only_view(source)
        self.assertNotIn("inner", view)
        self.assertIn("end", view)


class ValidateTest(unittest.TestCase):
    def test_rejects_comment_pseudo_lifecycle_exports(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_umirc(project)
            _write_app_runtime(
                project,
                body="// export const qiankun = { async bootstrap() {}, async mount() {}, async unmount() {} }\n",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("lifecycle exports are incomplete" in item for item in report.errors))

    def test_rejects_string_pseudo_lifecycle_exports(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_umirc(project)
            _write_app_runtime(
                project,
                body='const note = "export const qiankun = { async bootstrap() {} }";\n',
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("lifecycle exports are incomplete" in item for item in report.errors))

    def test_rejects_missing_qiankun_slave(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            _write_umirc(project, body="export default { antd: {}, access: {} };\n")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("qiankun slave config is missing" in item for item in report.errors))

    def test_accepts_real_qiankun_runtime(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            report = MODULE.validate(project, run_commands=False)
            self.assertEqual([], report.errors, msg="\n".join(report.errors))

    def test_rejects_comment_pseudo_antd_plugin(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            _write_umirc(
                project,
                body="""
export default {
  // antd: {},
  qiankun: { slave: {} },
  access: {},
};
""".strip(),
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("antd plugin" in item for item in report.errors))

    def test_rejects_string_pseudo_antd_plugin(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            _write_umirc(
                project,
                body="""
const note = "antd: {}";
export default { qiankun: { slave: {} }, access: {} };
""".strip(),
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("antd plugin" in item for item in report.errors))

    def test_reports_tsx_style_inline_color(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/HomePage.tsx"
            page.write_text(
                page.read_text(encoding="utf-8")
                + '\nconst style = { color: "#1677FF" };\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("hard-coded color #1677FF" in item for item in report.errors))

    def test_allows_plain_description_string_with_hex(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/HomePage.tsx"
            page.write_text(
                page.read_text(encoding="utf-8") + '\nconst note = "color #123456";\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            color_errors = [item for item in report.errors if "hard-coded color" in item]
            self.assertEqual([], color_errors)

    def test_reports_css_hex_color(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            css = project / "src/styles/global.css"
            css.parent.mkdir(parents=True, exist_ok=True)
            css.write_text(".brand { color: #1677ff; }\n", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("hard-coded color #1677ff" in item for item in report.errors))

    def test_allows_css_selector_id_hex(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            css = project / "src/styles/global.css"
            css.parent.mkdir(parents=True, exist_ok=True)
            css.write_text("#abcdef { margin: 0; }\n", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            color_errors = [item for item in report.errors if "hard-coded color" in item]
            self.assertEqual([], color_errors)

    def test_allows_css_url_hash_reference_hex(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            css = project / "src/styles/global.css"
            css.parent.mkdir(parents=True, exist_ok=True)
            css.write_text(
                ".icon { fill: url(#abcdef); background-image: url(#abc); }\n",
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            color_errors = [item for item in report.errors if "hard-coded color" in item]
            self.assertEqual([], color_errors)

    def test_reports_css_border_and_custom_property_colors(self) -> None:
        cases = [
            ".box { border: 1px solid #fff; }",
            ":root { --brand-color: #1677ff; }",
        ]
        for css_text in cases:
            with self.subTest(css_text=css_text):
                with TemporaryDirectory() as temp:
                    project = Path(temp)
                    _write_contract_compliant_project(project)
                    css = project / "src/styles/global.css"
                    css.parent.mkdir(parents=True, exist_ok=True)
                    css.write_text(css_text + "\n", encoding="utf-8")
                    report = MODULE.validate(project, run_commands=False)
                    self.assertTrue(
                        any("hard-coded color" in item for item in report.errors),
                        msg=css_text,
                    )

    def test_reports_invalid_hex_length_five(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            css = project / "src/styles/global.css"
            css.parent.mkdir(parents=True, exist_ok=True)
            css.write_text(".brand { color: #12345; }\n", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("hard-coded color #12345" in item for item in report.errors))

    def test_reports_extended_color_property_contexts(self) -> None:
        cases = [
            ("background", "#abc"),
            ("backgroundColor", "#abcd"),
            ("border", "#123456"),
            ("borderColor", "#12345678"),
            ("outline", "#fff"),
            ("boxShadow", "0 0 1px #1677ff"),
            ("textShadow", "1px 1px #000"),
            ("fill", "#f00"),
            ("stroke", "#0f0"),
            ("colorPrimary", "#1677ff"),
            ("colorBgContainer", "#ffffff"),
        ]
        for prop, value in cases:
            with self.subTest(prop=prop, value=value):
                with TemporaryDirectory() as temp:
                    project = Path(temp)
                    _write_contract_compliant_project(project)
                    page = project / "src/features/home/HomePage.tsx"
                    page.write_text(
                        page.read_text(encoding="utf-8")
                        + f'\nconst token = {{ {prop}: "{value}" }};\n',
                        encoding="utf-8",
                    )
                    report = MODULE.validate(project, run_commands=False)
                    hex_match = re.search(r"#[0-9a-fA-F]{3,8}", value)
                    assert hex_match is not None
                    self.assertTrue(
                        any(f"hard-coded color {hex_match.group(0).lower()}" in item.lower() for item in report.errors),
                        msg=f"expected violation for {prop}: {value}",
                    )

    def test_reports_valid_and_invalid_hex_lengths_in_tsx(self) -> None:
        valid = ["#abc", "#abcd", "#123456", "#12345678"]
        invalid = ["#12345", "#1234567"]
        for hex_value in valid:
            with self.subTest(hex_value=hex_value, valid=True):
                with TemporaryDirectory() as temp:
                    project = Path(temp)
                    _write_contract_compliant_project(project)
                    page = project / "src/features/home/HomePage.tsx"
                    page.write_text(
                        page.read_text(encoding="utf-8") + f'\nconst style = {{ color: "{hex_value}" }};\n',
                        encoding="utf-8",
                    )
                    report = MODULE.validate(project, run_commands=False)
                    self.assertTrue(
                        any(f"hard-coded color {hex_value.lower()}" in item.lower() for item in report.errors)
                    )
        for hex_value in invalid:
            with self.subTest(hex_value=hex_value, valid=False):
                with TemporaryDirectory() as temp:
                    project = Path(temp)
                    _write_contract_compliant_project(project)
                    page = project / "src/features/home/HomePage.tsx"
                    page.write_text(
                        page.read_text(encoding="utf-8") + f'\nconst style = {{ color: "{hex_value}" }};\n',
                        encoding="utf-8",
                    )
                    report = MODULE.validate(project, run_commands=False)
                    self.assertTrue(
                        any(f"hard-coded color {hex_value.lower()}" in item.lower() for item in report.errors)
                    )

    def test_plain_string_mock_path_is_not_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/HomePage.tsx"
            page.write_text(
                page.read_text(encoding="utf-8") + '\nconst note = "../mocks/entity.mock";\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            mock_errors = [item for item in report.errors if "imports mocks directly" in item]
            self.assertEqual([], mock_errors)

    def test_reports_namespace_mock_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/BadPage.tsx"
            page.write_text(
                'import * as mocks from "../mocks/entity.mock";\nexport function BadPage() { return null; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_dynamic_mock_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/BadPage.tsx"
            page.write_text(
                'const load = () => import("../mocks/entity.mock");\nexport function BadPage() { return null; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_export_star_mock_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/BadPage.tsx"
            page.write_text(
                'export * from "../mocks/entity.mock";\nexport function BadPage() { return null; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_export_star_as_mock_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/BadPage.tsx"
            page.write_text(
                'export * as mocks from "../mocks/entity.mock";\nexport function BadPage() { return null; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_require_mock_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            page = project / "src/features/home/BadPage.tsx"
            page.write_text(
                'const mocks = require("../mocks/entity.mock");\nexport function BadPage() { return null; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_default_named_and_side_effect_mock_imports(self) -> None:
        cases = [
            'import mock, { item } from "../mocks/index";',
            'export { item } from "../mocks/entity.mock";',
            'import "../mocks/side-effect";',
        ]
        for snippet in cases:
            with self.subTest(snippet=snippet):
                with TemporaryDirectory() as temp:
                    project = Path(temp)
                    _write_contract_compliant_project(project)
                    page = project / "src/features/home/BadPage.tsx"
                    page.write_text(f"{snippet}\nexport function BadPage() {{ return null; }}\n", encoding="utf-8")
                    report = MODULE.validate(project, run_commands=False)
                    self.assertTrue(any("imports mocks directly" in item for item in report.errors))

    def test_reports_action_without_disabled_guard(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/features/settings").mkdir(parents=True, exist_ok=True)
            (project / "src/features/settings/SettingsPage.tsx").write_text(
                """
export function SettingsPage() {
  return <Button onClick={() => undefined}>Save</Button>;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("SettingsPage.tsx must guard actions" in item for item in report.errors))

    def test_reports_multi_feature_partial_state_missing(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            second = project / "src/features/reports/ReportsPage.tsx"
            second.parent.mkdir(parents=True, exist_ok=True)
            second.write_text(
                """
import { Spin } from "antd";
import { useEffect, useState } from "react";
export function ReportsPage({ service }) {
  const [state, setState] = useState("loading");
  useEffect(() => { void service.list(); }, [service]);
  if (state === "loading") return <Spin />;
  return null;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("feature reports missing JSX baseline states" in item for item in report.errors))

    def test_rejects_forbidden_error_import_without_jsx_state(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/features/home/HomePage.tsx").write_text(
                """
import { Empty, Result, Spin } from "antd";
import { ForbiddenError } from "../../services/errors";
import { useEffect, useState } from "react";
export function HomePage({ service }) {
  const [state, setState] = useState("loading");
  useEffect(() => { void service.list(); }, [service]);
  if (state === "loading") return <Spin />;
  if (state === "empty") return <Empty />;
  if (state === "error") return <Result status="error" />;
  void ForbiddenError;
  return null;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(
                any("missing JSX baseline states" in item and "forbidden" in item for item in report.errors)
            )

    def test_reports_missing_route_access_flags(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/router/routes.ts").write_text(
                "export default [{ path: '/user/list', component: './User/UserList' }];\n",
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("access: flags" in item for item in report.errors))

    def test_token_scan_includes_scripts_and_excludes_node_modules(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "scripts").mkdir(exist_ok=True)
            (project / "scripts/leftover.mjs").write_text(
                'const token = "__APP_NAME__";\n',
                encoding="utf-8",
            )
            (project / "node_modules/fake/__APP_NAME__.ts").parent.mkdir(parents=True)
            (project / "node_modules/fake/__APP_NAME__.ts").write_text("token", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("scripts/leftover.mjs" in item for item in report.errors))
            self.assertFalse(any("node_modules" in item for item in report.errors))

    def test_missing_src_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("src directory not found" in item for item in report.errors))

    def test_invalid_package_json_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "src").mkdir()
            (project / "package.json").write_text("{not-json", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("invalid package.json" in item for item in report.errors))

    def test_accepts_scaffolded_project_static_checks(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp) / "inventory-console"
            SCAFFOLD.scaffold("inventory-console", "库存中心", "data-management", project)
            report = MODULE.validate(project, run_commands=False)
            self.assertEqual([], report.errors, msg="\n".join(report.errors))

    def test_yarn_not_found_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value=None)
            run_mock = Mock(return_value=Mock(returncode=0))
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", run_mock):
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("yarn is not available" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            run_mock.assert_not_called()

    def test_missing_script_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "package.json").write_text('{"scripts": {"dev": "exit 0"}}', encoding="utf-8")
            which_mock = Mock(return_value="/usr/bin/yarn")
            run_mock = Mock(return_value=Mock(returncode=0))
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", run_mock):
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("missing script: build" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual([], _executed_commands(run_mock))

    def test_run_commands_records_non_zero_failure(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)

            def fake_run(command, cwd, check, env=None, timeout=None):  # type: ignore[no-untyped-def]
                return Mock(returncode=7 if command[-1] == "build" else 0)

            which_mock = Mock(return_value="/usr/bin/yarn")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=fake_run) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (7): yarn build" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual(["yarn build"], _executed_commands(run_mock))

    def test_command_exception_not_found_records_127(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)

            def raise_not_found(*args, **kwargs):  # type: ignore[no-untyped-def]
                raise FileNotFoundError("yarn")

            which_mock = Mock(return_value="/usr/bin/yarn")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=raise_not_found) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertEqual(127, report.commands.get("yarn build"))
            self.assertTrue(any("command not found: yarn build" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual(["yarn build"], _executed_commands(run_mock))

    def test_command_exception_timeout_records_124(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)

            def raise_timeout(*args, **kwargs):  # type: ignore[no-untyped-def]
                raise TimeoutExpired(cmd="yarn build", timeout=1)

            which_mock = Mock(return_value="/usr/bin/yarn")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=raise_timeout) as run_mock:
                    report = MODULE.validate(project, run_commands=True, command_timeout=1)
            self.assertEqual(124, report.commands.get("yarn build"))
            self.assertTrue(any("command timed out" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual(["yarn build"], _executed_commands(run_mock))

    def test_command_returned_127_reports_failed_not_not_found(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value="/usr/bin/yarn")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", return_value=Mock(returncode=127)) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (127): yarn build" in item for item in report.errors))
            self.assertFalse(any("command not found" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual(["yarn build"], _executed_commands(run_mock))

    def test_command_returned_124_reports_failed_not_timeout(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value="/usr/bin/yarn")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", return_value=Mock(returncode=124)) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (124): yarn build" in item for item in report.errors))
            self.assertFalse(any("command timed out" in item for item in report.errors))
            which_mock.assert_called_once_with("yarn")
            self.assertEqual(["yarn build"], _executed_commands(run_mock))

    def test_malformed_ipv6_public_base_is_rejected(self) -> None:
        self.assertFalse(MODULE._is_valid_public_base("http://[::1"))


if __name__ == "__main__":
    unittest.main()

