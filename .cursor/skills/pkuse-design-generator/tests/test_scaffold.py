# .cursor/skills/pkuse-design-generator/tests/test_scaffold.py
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest
from unittest.mock import patch

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

    def test_generated_runtime_has_dual_mode_and_cleanup(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "ops-console"
            MODULE.scaffold("ops-console", "运维中心", "monitoring", output)
            adapter = (output / "src/micro-app/adapter.tsx").read_text(
                encoding="utf-8"
            )
            main = (output / "src/main.tsx").read_text(encoding="utf-8")
            html = (output / "index.html").read_text(encoding="utf-8")
            package = (output / "package.json").read_text(encoding="utf-8")
            vite = (output / "vite.config.ts").read_text(encoding="utf-8")

            self.assertIn("export async function bootstrap", adapter)
            self.assertIn("export async function mount", adapter)
            self.assertIn("export async function unmount", adapter)
            self.assertIn("export async function update", adapter)
            self.assertIn("mountedRoot?.unmount()", adapter)
            self.assertIn("props?.offGlobalStateChange?.()", adapter)
            self.assertIn("callSafely(abortAllRequests)", adapter)
            self.assertIn("callSafely(clearAllResources)", adapter)
            self.assertIn("props.container", adapter)
            self.assertIn("disposeCurrent()", adapter)
            self.assertIn("nextRoot = createRoot(mountElement)", adapter)
            self.assertIn("renderWithQiankun", main)
            self.assertIn("data-pkuse-root='ops-console'", adapter)
            self.assertIn('data-pkuse-root="ops-console"', html)
            self.assertIn('"antd": "^6', package)
            self.assertIn('"qiankun": "^2', package)
            self.assertIn('mode === "qiankun"', vite)
            self.assertIn("requires VITE_PUBLIC_BASE", vite)
            self.assertIn("VITE_PUBLIC_BASE", vite)
            self.assertIn('"build:qiankun"', package)
            self.assertIn("verify-build-base.mjs", package)
            self.assertTrue((output / ".env.qiankun.example").is_file())
            self.assertTrue(
                (output / "src/micro-app/adapter.test.tsx").is_file()
            )

    def test_generated_app_has_provider_rbac_and_service_boundaries(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "access-console"
            MODULE.scaffold("access-console", "权限中心", "system-config", output)
            app = (output / "src/app/App.tsx").read_text(encoding="utf-8")
            access = (output / "src/auth/access.ts").read_text(encoding="utf-8")
            services = (output / "src/app/services.ts").read_text(encoding="utf-8")
            page = (output / "src/features/home/HomePage.tsx").read_text(
                encoding="utf-8"
            )
            manifest = (output / "src/routes/manifest.tsx").read_text(
                encoding="utf-8"
            )
            errors = (output / "src/services/errors.ts").read_text(
                encoding="utf-8"
            )

            self.assertIn("ConfigProvider", app)
            self.assertIn('prefixCls="access-console"', app)
            self.assertIn('key: "access_console"', app)
            self.assertIn("ErrorBoundary", app)
            self.assertIn("createRouteManifest", app)
            self.assertIn("buildVisibleMenu", app)
            self.assertIn("canAccessRoute", app)
            self.assertNotIn('from "../features/home/HomePage"', app)
            self.assertIn("export function can(", access)
            self.assertIn("createServices", services)
            self.assertIn("MockEntityService", services)
            self.assertIn("ApiEntityService", services)
            self.assertNotIn("/mocks/", page)
            self.assertIn("createRouteManifest", manifest)
            self.assertIn("PERMISSIONS.HOME_VIEW", manifest)
            self.assertIn("buildVisibleMenu", manifest)
            self.assertIn("UnauthorizedError", errors)
            self.assertIn("ForbiddenError", errors)
            self.assertIn("NotFoundError", errors)
            self.assertIn("ServerError", errors)
            self.assertIn("NetworkError", errors)
            self.assertIn("BusinessError", errors)
            self.assertIn("ProtocolError", errors)
            self.assertTrue((output / "src/routes/manifest.test.tsx").is_file())
            self.assertTrue((output / "src/services/api.test.ts").is_file())
            for state in ("loading", "empty", "error", "forbidden"):
                self.assertIn(state, page)

    def test_rejects_invalid_name_and_existing_output(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "target"
            output.mkdir()
            with self.assertRaisesRegex(ValueError, "kebab-case"):
                MODULE.scaffold("Bad Name", "Bad", "dashboard", Path(temp) / "new")
            with self.assertRaisesRegex(FileExistsError, "already exists"):
                MODULE.scaffold("valid-name", "Valid", "dashboard", output)

    def test_rejects_unknown_scene(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "new-app"
            with self.assertRaisesRegex(ValueError, "unknown scene"):
                MODULE.scaffold("new-app", "New", "not-a-scene", output)
            self.assertFalse(output.exists())

    def test_does_not_leave_output_when_templates_missing(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "inventory-console"
            missing_templates = Path(temp) / "missing-base-app"
            with patch.object(MODULE, "TEMPLATES", missing_templates):
                with self.assertRaises(FileNotFoundError):
                    MODULE.scaffold(
                        "inventory-console",
                        "库存中心",
                        "data-management",
                        output,
                    )
            self.assertFalse(output.exists())

    def test_does_not_leave_output_when_render_fails(self) -> None:
        with TemporaryDirectory() as temp:
            templates = Path(temp) / "base-app"
            templates.mkdir()
            (templates / "first.tpl").write_text("first", encoding="utf-8")
            (templates / "second.tpl").write_text("second", encoding="utf-8")
            output = Path(temp) / "out-app"

            original_read_text = Path.read_text

            def read_text_side_effect(self: Path, *args: object, **kwargs: object) -> str:
                if self.name == "second.tpl":
                    raise OSError("simulated render failure")
                return original_read_text(self, *args, **kwargs)

            with patch.object(MODULE, "TEMPLATES", templates):
                with patch.object(Path, "read_text", read_text_side_effect):
                    with self.assertRaises(OSError):
                        MODULE.scaffold("out-app", "Out", "data-management", output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
