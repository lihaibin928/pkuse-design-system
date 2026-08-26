#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
TEMPLATES = ROOT / "assets/base-app"
SCENARIOS = ROOT / "assets/scenarios"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def _template_files() -> list[Path]:
    if not TEMPLATES.is_dir():
        raise FileNotFoundError(f"templates not found: {TEMPLATES}")
    files = [path for path in TEMPLATES.rglob("*") if path.is_file()]
    if not files:
        raise FileNotFoundError(f"templates directory has no files: {TEMPLATES}")
    return files


def scaffold(name: str, title: str, scene: str, output: Path) -> Path:
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("application name must use kebab-case")
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    scenario_path = SCENARIOS / f"{scene}.json"
    if not scenario_path.is_file():
        choices = ", ".join(sorted(path.stem for path in SCENARIOS.glob("*.json")))
        raise ValueError(f"unknown scene {scene!r}; choose one of: {choices}")

    template_files = _template_files()
    values = {
        "__APP_NAME__": name,
        "__APP_TITLE__": title,
        "__APP_PREFIX__": name.replace("-", "_"),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{output.name}.scaffold-",
            dir=output.parent,
        )
    )
    try:
        for source in template_files:
            relative = source.relative_to(TEMPLATES)
            target_name = relative.name.removesuffix(".tpl")
            target = staging / relative.parent / target_name
            target.parent.mkdir(parents=True, exist_ok=True)
            content = source.read_text(encoding="utf-8")
            for token, value in values.items():
                content = content.replace(token, value)
            target.write_text(content, encoding="utf-8")

        generated = staging / "src/generated"
        generated.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(scenario_path, generated / "scene.json")
        staging.rename(output)
        return output
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise


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
