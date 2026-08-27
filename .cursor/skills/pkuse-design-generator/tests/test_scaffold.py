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
            app = (output / "src/app.ts").read_text(encoding="utf-8")
            umirc = (output / ".umirc.ts").read_text(encoding="utf-8")
            manifest = (output / "src/generated/scene.json").read_text(encoding="utf-8")
            self.assertIn('"name": "inventory-console"', package)
            self.assertIn("库存中心", app)
            self.assertIn("库存中心", umirc)
            self.assertIn('"scene": "data-management"', manifest)
            self.assertNotIn("__APP_", package + app + umirc)

    def test_generated_runtime_has_umi_qiankun_slave(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "ops-console"
            MODULE.scaffold("ops-console", "运维中心", "monitoring", output)
            app = (output / "src/app.ts").read_text(encoding="utf-8")
            umirc = (output / ".umirc.ts").read_text(encoding="utf-8")
            package = (output / "package.json").read_text(encoding="utf-8")

            self.assertIn("export const qiankun", app)
            self.assertIn("async bootstrap", app)
            self.assertIn("async mount", app)
            self.assertIn("async unmount", app)
            self.assertIn("menuRender: false", app)
            self.assertIn("menuHeaderRender: false", app)
            self.assertIn("qiankun:", umirc)
            self.assertIn("slave:", umirc)
            self.assertIn("antd:", umirc)
            self.assertIn('"@umijs/max"', package)
            self.assertIn('"antd": "^6.6.1"', package)
            self.assertIn('"@ant-design/icons": "^6.3.2"', package)
            self.assertTrue((output / "src/pages/DesignSystem/index.tsx").is_file())
            self.assertFalse((output / "vite.config.ts").exists())
            self.assertFalse((output / "src/micro-app").exists())

    def test_generated_app_has_feature_access_and_routes(self) -> None:
        with TemporaryDirectory() as temp:
            output = Path(temp) / "access-console"
            MODULE.scaffold("access-console", "权限中心", "system-config", output)
            access = (output / "src/access.ts").read_text(encoding="utf-8")
            routes = (output / "src/router/routes.ts").read_text(encoding="utf-8")
            request = (output / "src/utils/request.ts").read_text(encoding="utf-8")
            page = (output / "src/pages/User/UserList/index.tsx").read_text(
                encoding="utf-8"
            )
            modal = (
                output / "src/features/user/components/UserListWithModal/index.tsx"
            ).read_text(encoding="utf-8")

            self.assertIn("canViewUser", access)
            self.assertIn("canEditUser", access)
            self.assertIn("access: 'canViewUser'", routes)
            self.assertIn("component: './DesignSystem'", routes)
            self.assertIn("BizError", request)
            self.assertNotIn("/mock/", page)
            self.assertNotIn("/mocks/", page)
            self.assertIn("useUserList", page)
            self.assertIn("<Access", modal)
            self.assertTrue((output / "mock/user.ts").is_file())
            self.assertTrue((output / "src/features/user/services/index.ts").is_file())

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
