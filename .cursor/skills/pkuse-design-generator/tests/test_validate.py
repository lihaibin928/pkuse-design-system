from __future__ import annotations

import importlib.util
import json
import os
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

REAL_ADAPTER = """
import type { Root } from "react-dom/client";
let root: Root | undefined;
function disposeResources(props: unknown, mountedRoot: Root | undefined): void {
  mountedRoot?.unmount();
}
function disposeCurrent(): void {
  const mountedRoot = root;
  root = undefined;
  disposeResources(undefined, mountedRoot);
}
export async function bootstrap(): Promise<void> {}
export async function mount(): Promise<void> {}
export async function unmount(): Promise<void> { disposeCurrent(); }
""".strip()


def _executed_commands(run_mock: Mock) -> list[str]:
    return [" ".join(call.args[0]) for call in run_mock.call_args_list]


def _write_package_json(project: Path, scripts: dict[str, str] | None = None) -> None:
    (project / "package.json").write_text(
        json.dumps({"scripts": scripts or {}}),
        encoding="utf-8",
    )


def _write_lifecycle_adapter(adapter_path: Path, *, body: str) -> None:
    adapter_path.parent.mkdir(parents=True, exist_ok=True)
    adapter_path.write_text(body, encoding="utf-8")


def _write_contract_compliant_project(project: Path) -> None:
    _write_lifecycle_adapter(project / "src/micro-app/adapter.tsx", body=REAL_ADAPTER)
    (project / "src/auth").mkdir(parents=True, exist_ok=True)
    (project / "src/app").mkdir(parents=True, exist_ok=True)
    (project / "src/routes").mkdir(parents=True, exist_ok=True)
    (project / "src/auth/permissions.ts").write_text(
        'export const PERMISSIONS = { HOME_VIEW: "home:view", ENTITY_EDIT: "entity:edit" } as const;\n',
        encoding="utf-8",
    )
    (project / "src/app/App.tsx").write_text(
        """
import { ConfigProvider } from "antd";
import { Routes } from "react-router-dom";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  return (
    <ConfigProvider>
      <Routes>
        {manifest.map((route) => (
          <span key={route.path}>{canAccessRoute(route, []) ? route.title : "deny"}</span>
        ))}
        {menu.length}
      </Routes>
    </ConfigProvider>
  );
}
""".strip(),
        encoding="utf-8",
    )
    (project / "src/routes/manifest.tsx").write_text(
        """
import { PERMISSIONS } from "../auth/permissions";
export function createRouteManifest() {
  return [{ path: "/", permissions: [PERMISSIONS.HOME_VIEW], menu: { order: 1 } }];
}
export function buildVisibleMenu(manifest) { return manifest; }
export function canAccessRoute(route, permissions) { return true; }
""".strip(),
        encoding="utf-8",
    )
    home = project / "src/features/home/HomePage.tsx"
    home.parent.mkdir(parents=True, exist_ok=True)
    home.write_text(
        """
import { Button, Empty, Result, Spin } from "antd";
import { useEffect, useState } from "react";
import { can } from "../../auth/access";
import { PERMISSIONS } from "../../auth/permissions";
export function HomePage({ service, permissions = [] }) {
  const [state, setState] = useState("loading");
  useEffect(() => { void service.list(); }, [service]);
  if (state === "loading") { return <Spin tip="loading" />; }
  if (state === "forbidden") { return <Result status="403" title="denied" />; }
  if (state === "error") { return <Result status="error" title="failed" />; }
  if (state === "empty") { return <Empty description="none" />; }
  return <Button disabled={!can(permissions, PERMISSIONS.ENTITY_EDIT)}>Edit</Button>;
}
""".strip(),
        encoding="utf-8",
    )
    _write_package_json(project, {"typecheck": "exit 0", "test": "exit 0", "build": "exit 0"})


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
    def test_rejects_comment_pseudo_exports(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_lifecycle_adapter(
                project / "src/micro-app/adapter.tsx",
                body="// export async function bootstrap() {}\n",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("lifecycle exports are incomplete" in item for item in report.errors))

    def test_rejects_string_pseudo_lifecycle_exports(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_lifecycle_adapter(
                project / "src/micro-app/adapter.tsx",
                body='const bootstrap = "export async function bootstrap(){}";',
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("lifecycle exports are incomplete" in item for item in report.errors))

    def test_rejects_undefined_root_argument_chain(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_lifecycle_adapter(
                project / "src/micro-app/adapter.tsx",
                body="""
function disposeResources(p, mountedRoot) { mountedRoot?.unmount(); }
function disposeCurrent() { const mountedRoot = root; root = undefined; disposeResources(undefined, undefined); }
export async function bootstrap() {}
export async function mount() {}
export async function unmount() { disposeCurrent(); }
""".strip(),
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("disposeCurrent" in item for item in report.errors))

    def test_rejects_plain_object_root_argument_chain(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_lifecycle_adapter(
                project / "src/micro-app/adapter.tsx",
                body="""
function disposeResources(p, mountedRoot) { mountedRoot?.unmount(); }
function disposeCurrent() { const mountedRoot = root; root = undefined; disposeResources(undefined, { unmount() {} }); }
export async function bootstrap() {}
export async function mount() {}
export async function unmount() { disposeCurrent(); }
""".strip(),
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("disposeCurrent" in item for item in report.errors))

    def test_accepts_real_root_cleanup_chain(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            report = MODULE.validate(project, run_commands=False)
            self.assertEqual([], report.errors, msg="\n".join(report.errors))

    def test_accepts_direct_root_unmount(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_package_json(project)
            _write_lifecycle_adapter(
                project / "src/micro-app/adapter.tsx",
                body="""
export async function bootstrap() {}
export async function mount() {}
export async function unmount() { root?.unmount(); }
""".strip(),
            )
            report = MODULE.validate(project, run_commands=False)
            lifecycle = [item for item in report.errors if "unmount in src/micro-app" in item]
            self.assertEqual([], lifecycle)

    def test_rejects_string_pseudo_config_provider(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                'export function App() { const tag = "<ConfigProvider>"; return tag; }\n',
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_self_closing_config_provider(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  return <ConfigProvider />;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_local_config_provider_function(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
function ConfigProvider() { return null; }
export function App() { return <ConfigProvider></ConfigProvider>; }
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_accepts_config_provider_alias_from_antd(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider as AntConfigProvider } from "antd";
import { Routes } from "react-router-dom";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  return (
    <AntConfigProvider>
      <Routes>
        {manifest.map((route) => (
          <span key={route.path}>{canAccessRoute(route, []) ? route.title : "deny"}</span>
        ))}
        {menu.length}
      </Routes>
    </AntConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_accepts_default_named_antd_config_provider_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import antd, { ConfigProvider } from "antd";
import { Routes } from "react-router-dom";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  void antd;
  return (
    <ConfigProvider>
      <Routes>
        {manifest.map((route) => (
          <span key={route.path}>{canAccessRoute(route, []) ? route.title : "deny"}</span>
        ))}
        {menu.length}
      </Routes>
    </ConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_rejects_empty_config_provider_wrapper(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  return <ConfigProvider></ConfigProvider>;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_whitespace_only_config_provider_wrapper(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
export function App() { return <ConfigProvider>   </ConfigProvider>; }
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_parallel_app_content_outside_provider(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
function AppContent() { return <div>content</div>; }
export function App() {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  return (
    <>
      <ConfigProvider></ConfigProvider>
      <AppContent />
    </>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_accepts_config_provider_wrapping_app_content(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
function AppContent({ manifest, menu }) {
  return (
    <div>
      {manifest.map((route) => (
        <span key={route.path}>{canAccessRoute(route, []) ? route.title : "deny"}</span>
      ))}
      {menu.length}
    </div>
  );
}
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  return (
    <ConfigProvider>
      <AppContent manifest={manifest} menu={menu} />
    </ConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_rejects_config_provider_with_span_placeholder(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
function AppContent() { return <div>content</div>; }
export function App() {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  return (
    <>
      <ConfigProvider><span /></ConfigProvider>
      <AppContent />
    </>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_config_provider_with_only_antd_app(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { App as AntdApp, ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  return (
    <ConfigProvider>
      <AntdApp><div>placeholder</div></AntdApp>
    </ConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_accepts_config_provider_with_router_provider_outlet(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
export function App() {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  const router = createBrowserRouter([{ path: "/", element: <div /> }]);
  return (
    <ConfigProvider>
      <RouterProvider router={router} />
    </ConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_accepts_config_provider_with_routes_outlet(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { Routes, Route } from "react-router-dom";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App() {
  const manifest = createRouteManifest({});
  const menu = buildVisibleMenu(manifest, []);
  return (
    <ConfigProvider>
      <Routes>
        <Route path="/" element={<div>{menu.length}</div>} />
      </Routes>
    </ConfigProvider>
  );
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_accepts_config_provider_with_children_prop_outlet(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
import { ConfigProvider } from "antd";
import { createRouteManifest, buildVisibleMenu, canAccessRoute } from "../routes/manifest";
export function App({ children }: { children: React.ReactNode }) {
  void createRouteManifest;
  void buildVisibleMenu;
  void canAccessRoute;
  return <ConfigProvider>{children}</ConfigProvider>;
}
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            config_errors = [item for item in report.errors if "ConfigProvider from antd" in item]
            self.assertEqual([], config_errors)

    def test_rejects_comment_pseudo_antd_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
// import { ConfigProvider } from "antd";
export function App() { return <ConfigProvider></ConfigProvider>; }
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

    def test_rejects_string_pseudo_antd_import(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/app/App.tsx").write_text(
                """
const note = 'import { ConfigProvider } from "antd"';
export function App() { return <div>{note}</div>; }
""".strip(),
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("ConfigProvider from antd" in item for item in report.errors))

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
            self.assertTrue(any("ReportsPage.tsx missing JSX baseline states" in item for item in report.errors))

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

    def test_reports_missing_rbac_manifest_permissions(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "src/routes/manifest.tsx").write_text(
                "export function createRouteManifest() { return [{ permissions: ['home:view'] }]; }\n"
                "export function buildVisibleMenu(m) { return m; }\n"
                "export function canAccessRoute() { return true; }\n",
                encoding="utf-8",
            )
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("permissions: [PERMISSIONS" in item for item in report.errors))

    def test_token_scan_includes_scripts_and_excludes_node_modules(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "scripts").mkdir(exist_ok=True)
            (project / "scripts/verify-build-base.mjs").write_text(
                'const token = "__APP_NAME__";\n',
                encoding="utf-8",
            )
            (project / "node_modules/fake/__APP_NAME__.ts").parent.mkdir(parents=True)
            (project / "node_modules/fake/__APP_NAME__.ts").write_text("token", encoding="utf-8")
            report = MODULE.validate(project, run_commands=False)
            self.assertTrue(any("scripts/verify-build-base.mjs" in item for item in report.errors))
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

    def test_pnpm_not_found_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value=None)
            run_mock = Mock(return_value=Mock(returncode=0))
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", run_mock):
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("pnpm is not available" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            run_mock.assert_not_called()

    def test_missing_script_reports_clear_error(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            (project / "package.json").write_text('{"scripts": {"test": "exit 0"}}', encoding="utf-8")
            which_mock = Mock(return_value="/usr/bin/pnpm")
            run_mock = Mock(return_value=Mock(returncode=0))
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", run_mock):
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("missing script: typecheck" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(["pnpm test"], _executed_commands(run_mock))

    def test_run_commands_records_non_zero_failure(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            scripts = json.loads((project / "package.json").read_text(encoding="utf-8"))["scripts"]
            scripts["typecheck"] = "exit 7"
            (project / "package.json").write_text(json.dumps({"scripts": scripts}), encoding="utf-8")

            def fake_run(command, cwd, check, env=None, timeout=None):  # type: ignore[no-untyped-def]
                return Mock(returncode=7 if command[-1] == "typecheck" else 0)

            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=fake_run) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (7): pnpm typecheck" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_command_exception_not_found_records_127(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)

            def raise_not_found(*args, **kwargs):  # type: ignore[no-untyped-def]
                raise FileNotFoundError("pnpm")

            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=raise_not_found) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertEqual(127, report.commands.get("pnpm typecheck"))
            self.assertTrue(any("command not found: pnpm typecheck" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_command_exception_timeout_records_124(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)

            def raise_timeout(*args, **kwargs):  # type: ignore[no-untyped-def]
                raise TimeoutExpired(cmd="pnpm typecheck", timeout=1)

            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=raise_timeout) as run_mock:
                    report = MODULE.validate(project, run_commands=True, command_timeout=1)
            self.assertEqual(124, report.commands.get("pnpm typecheck"))
            self.assertTrue(any("command timed out" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_command_returned_127_reports_failed_not_not_found(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", return_value=Mock(returncode=127)) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (127): pnpm typecheck" in item for item in report.errors))
            self.assertFalse(any("command not found" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_command_returned_124_reports_failed_not_timeout(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", return_value=Mock(returncode=124)) as run_mock:
                    report = MODULE.validate(project, run_commands=True)
            self.assertTrue(any("command failed (124): pnpm typecheck" in item for item in report.errors))
            self.assertFalse(any("command timed out" in item for item in report.errors))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_malformed_ipv6_public_base_is_rejected(self) -> None:
        self.assertFalse(MODULE._is_valid_public_base("http://[::1"))

    def test_run_commands_strips_vite_public_base_from_default_scripts(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            captured: list[dict[str, str] | None] = []

            def fake_run(command, cwd, check, env=None, timeout=None):  # type: ignore[no-untyped-def]
                captured.append(env)
                return Mock(returncode=0)

            with patch.dict(os.environ, {"VITE_PUBLIC_BASE": "https://leak.example/"}, clear=False):
                which_mock = Mock(return_value="/usr/bin/pnpm")
                with patch.object(MODULE.shutil, "which", which_mock):
                    with patch.object(MODULE.subprocess, "run", side_effect=fake_run) as run_mock:
                        MODULE.validate(project, run_commands=True)
            for env in captured[:3]:
                assert env is not None
                self.assertNotIn("VITE_PUBLIC_BASE", env)
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build"],
                _executed_commands(run_mock),
            )

    def test_build_qiankun_skipped_for_invalid_base(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            scripts = json.loads((project / "package.json").read_text(encoding="utf-8"))["scripts"]
            scripts["build:qiankun"] = "exit 0"
            (project / "package.json").write_text(json.dumps({"scripts": scripts}), encoding="utf-8")
            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", return_value=Mock(returncode=0)) as run_mock:
                    report = MODULE.validate(
                        project,
                        run_commands=True,
                        vite_public_base="/relative/path",
                    )
            executed = _executed_commands(run_mock)
            self.assertNotIn("pnpm build:qiankun", executed)
            self.assertEqual(["pnpm typecheck", "pnpm test", "pnpm build"], executed)
            which_mock.assert_called_once_with("pnpm")
            self.assertTrue(any("skipped pnpm build:qiankun" in item for item in report.warnings))

    def test_build_qiankun_runs_with_valid_vite_public_base(self) -> None:
        with TemporaryDirectory() as temp:
            project = Path(temp)
            _write_contract_compliant_project(project)
            scripts = json.loads((project / "package.json").read_text(encoding="utf-8"))["scripts"]
            scripts["build:qiankun"] = "exit 0"
            (project / "package.json").write_text(json.dumps({"scripts": scripts}), encoding="utf-8")
            captured: dict[str, str] = {}

            def fake_run(command, cwd, check, env=None, timeout=None):  # type: ignore[no-untyped-def]
                if command[-1] == "build:qiankun" and env:
                    captured.update(env)
                return Mock(returncode=0)

            which_mock = Mock(return_value="/usr/bin/pnpm")
            with patch.object(MODULE.shutil, "which", which_mock):
                with patch.object(MODULE.subprocess, "run", side_effect=fake_run) as run_mock:
                    report = MODULE.validate(
                        project,
                        run_commands=True,
                        vite_public_base="https://cdn.example.com/inventory/",
                    )
            self.assertEqual([], report.errors)
            self.assertEqual("https://cdn.example.com/inventory/", captured.get("VITE_PUBLIC_BASE"))
            which_mock.assert_called_once_with("pnpm")
            self.assertEqual(
                ["pnpm typecheck", "pnpm test", "pnpm build", "pnpm build:qiankun"],
                _executed_commands(run_mock),
            )


if __name__ == "__main__":
    unittest.main()
