#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

TOKEN = re.compile(r"__APP_(?:NAME|TITLE|PREFIX)__")
VALID_HEX = re.compile(
    r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b"
)
INVALID_HEX = re.compile(r"#([0-9a-fA-F]{5}|[0-9a-fA-F]{7})\b")
ANY_HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")
EXPORT_ASYNC_FUNCTION = re.compile(
    r"export\s+async\s+function\s+([A-Za-z_$][\w$]*)\s*(?:<[^>]*>)?\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{"
)
FUNCTION_DECL = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*(?:<[^>]*>)?\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{"
)
MANIFEST_PERMISSIONS = re.compile(r"\bpermissions\s*:\s*\[[^\]]*PERMISSIONS\.")
PERMISSIONS_DECL = re.compile(r"export\s+const\s+PERMISSIONS\b")
COLOR_PROPERTY_CONTEXT = re.compile(
    r"(?:\b(?:color|background|backgroundColor|border|borderColor|outline|"
    r"boxShadow|textShadow|fill|stroke)\b|\b[a-zA-Z]*color[a-zA-Z]*)\s*:\s*$",
    re.IGNORECASE,
)
STYLE_OBJECT_CONTEXT = re.compile(r"\bstyle\s*=\s*\{\s*$")
TOKEN_OBJECT_CONTEXT = re.compile(r"\btoken\s*:\s*\{\s*$")

THEME_FILES = {"theme.ts", "theme.tsx"}
COLOR_SCAN_SUFFIXES = {".ts", ".tsx", ".css"}
TOKEN_SCAN_FILES = {
    "package.json",
    "vite.config.ts",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.node.json",
    "index.html",
    "README.md",
    ".env.qiankun.example",
}
TOKEN_SCAN_SUFFIXES = {
    ".ts",
    ".tsx",
    ".css",
    ".json",
    ".yaml",
    ".yml",
    ".env",
    ".mjs",
    ".html",
    ".md",
}
TOKEN_EXCLUDE_DIRS = {"node_modules", "dist", "coverage"}
MOCK_ALLOWED_PREFIX = "src/micro-app/"
MOCK_ALLOWED_FILES = {"src/app/services.ts"}
DEFAULT_COMMANDS = ("typecheck", "test", "build")
QIANKUN_COMMAND = "build:qiankun"
DEFAULT_COMMAND_TIMEOUT_SECONDS = 900
EXIT_NOT_FOUND = 127
EXIT_TIMEOUT = 124
STATE_VALUES = frozenset({"loading", "empty", "error", "forbidden"})


class CommandCause(str, Enum):
    RETURNED = "returned"
    NOT_FOUND = "not-found"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class StringToken:
    value: str
    start: int
    end: int
    quote: str


@dataclass
class LexResult:
    source: str
    code_only: str
    strings: list[StringToken] = field(default_factory=list)


@dataclass(frozen=True)
class CommandResult:
    exit_code: int
    cause: CommandCause


@dataclass(frozen=True)
class ImportBinding:
    imported: str
    local: str


@dataclass(frozen=True)
class ImportDeclaration:
    module: str
    bindings: tuple[ImportBinding, ...]
    side_effect: bool


class ValidationReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.commands: dict[str, int] = {}


def _mask(chars: list[str], source: str, start: int, end: int) -> None:
    for index in range(start, end):
        if source[index] != "\n":
            chars[index] = " "


def _skip_string(source: str, index: int, quote: str) -> int:
    index += 1
    length = len(source)
    while index < length:
        if source[index] == "\\":
            index += 2
            continue
        if source[index] == quote:
            return index + 1
        index += 1
    return length


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\n\r":
        index += 1
    return index


def _skip_line_comment(source: str, index: int, limit: int) -> int:
    index += 2
    while index < limit and source[index] != "\n":
        index += 1
    return index


def _skip_block_comment(source: str, index: int, limit: int) -> int:
    index += 2
    while index + 1 < limit and not (source[index] == "*" and source[index + 1] == "/"):
        index += 1
    return min(index + 2, limit)


def _skip_template_for_scan(source: str, index: int, limit: int) -> int:
    index += 1
    while index < limit:
        char = source[index]
        if char == "\\":
            index += 2
            continue
        if char == "$" and index + 1 < limit and source[index + 1] == "{":
            index = _scan_balanced_brace(source, index + 1, limit)
            continue
        if char == "`":
            return index + 1
        index += 1
    return index


def _scan_balanced_brace(source: str, open_brace: int, limit: int | None = None) -> int:
    if open_brace >= len(source) or source[open_brace] != "{":
        return open_brace + 1
    end = len(source) if limit is None else limit
    depth = 0
    index = open_brace
    while index < end:
        char = source[index]
        if char in {"'", '"'}:
            index = _skip_string(source, index, char)
            continue
        if char == "`":
            index = _skip_template_for_scan(source, index, end)
            continue
        if char == "/" and index + 1 < end:
            nxt = source[index + 1]
            if nxt == "/":
                index = _skip_line_comment(source, index, end)
                continue
            if nxt == "*":
                index = _skip_block_comment(source, index, end)
                continue
        if char == "{":
            depth += 1
            index += 1
            continue
        if char == "}":
            depth -= 1
            index += 1
            if depth == 0:
                return index
            continue
        index += 1
    return index


def _tokenize_expression(
    source: str,
    chars: list[str],
    start: int,
    end: int,
    strings: list[StringToken],
) -> None:
    index = start
    while index < end:
        char = source[index]
        if char in {"'", '"'}:
            literal_start = index
            index = _skip_string(source, index, char)
            strings.append(StringToken(source[literal_start + 1 : index - 1], literal_start, index, char))
            _mask(chars, source, literal_start + 1, index - 1)
            continue
        if char == "`":
            index = _tokenize_template(source, chars, index, strings)
            if index > end:
                break
            continue
        if char == "/" and index + 1 < end:
            nxt = source[index + 1]
            if nxt == "/":
                comment_start = index
                index = _skip_line_comment(source, index, end)
                _mask(chars, source, comment_start, index)
                continue
            if nxt == "*":
                comment_start = index
                index = _skip_block_comment(source, index, end)
                _mask(chars, source, comment_start, index)
                continue
        if char == "$" and index + 1 < end and source[index + 1] == "{":
            inner_end = _scan_balanced_brace(source, index + 1, end)
            _tokenize_expression(source, chars, index + 2, inner_end - 1, strings)
            index = inner_end
            continue
        index += 1


def _tokenize_template(source: str, chars: list[str], index: int, strings: list[StringToken]) -> int:
    start = index
    index += 1
    length = len(source)
    while index < length:
        char = source[index]
        if char == "\\":
            _mask(chars, source, index, min(index + 2, length))
            index += 2
            continue
        if char == "$" and index + 1 < length and source[index + 1] == "{":
            expr_end = _scan_balanced_brace(source, index + 1, length)
            _tokenize_expression(source, chars, index + 2, expr_end - 1, strings)
            index = expr_end
            continue
        if char == "`":
            strings.append(StringToken(source[start + 1 : index], start, index + 1, "`"))
            return index + 1
        _mask(chars, source, index, index + 1)
        index += 1
    strings.append(StringToken(source[start + 1 : index], start, index, "`"))
    return index


def tokenize(source: str) -> LexResult:
    chars = list(source)
    strings: list[StringToken] = []
    index = 0
    length = len(source)
    while index < length:
        char = source[index]
        if char in {"'", '"'}:
            literal_start = index
            index = _skip_string(source, index, char)
            strings.append(StringToken(source[literal_start + 1 : index - 1], literal_start, index, char))
            _mask(chars, source, literal_start + 1, index - 1)
            continue
        if char == "`":
            index = _tokenize_template(source, chars, index, strings)
            continue
        if char == "/" and index + 1 < length:
            nxt = source[index + 1]
            if nxt == "/":
                comment_start = index
                index += 2
                while index < length and source[index] != "\n":
                    index += 1
                _mask(chars, source, comment_start, index)
                continue
            if nxt == "*":
                comment_start = index
                index += 2
                while index + 1 < length and not (source[index] == "*" and source[index + 1] == "/"):
                    index += 1
                index = min(index + 2, length)
                _mask(chars, source, comment_start, index)
                continue
        index += 1
    return LexResult(source=source, code_only="".join(chars), strings=strings)


def to_code_only_view(source: str) -> str:
    return tokenize(source).code_only


def strip_comments(source: str) -> str:
    return to_code_only_view(source)


def _extract_brace_body(source: str, brace_index: int) -> tuple[str, int]:
    if brace_index >= len(source) or source[brace_index] != "{":
        return "", brace_index
    depth = 0
    index = brace_index
    length = len(source)
    while index < length:
        char = source[index]
        if char in {"'", '"', "`"}:
            index = _skip_string(source, index, char) if char != "`" else index + 1
            if char == "`":
                while index < length and source[index] != "`":
                    if source[index] == "\\":
                        index += 2
                        continue
                    if source[index] == "$" and index + 1 < length and source[index + 1] == "{":
                        index += 2
                        nested = 1
                        while index < length and nested:
                            if source[index] == "{":
                                nested += 1
                            elif source[index] == "}":
                                nested -= 1
                            index += 1
                        continue
                    index += 1
                index = min(index + 1, length)
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_index + 1 : index], index + 1
        index += 1
    return "", length


def extract_function_bodies(source: str) -> dict[str, str]:
    code = to_code_only_view(source)
    bodies: dict[str, str] = {}
    for match in FUNCTION_DECL.finditer(code):
        name = match.group(1)
        body, _ = _extract_brace_body(code, match.end() - 1)
        bodies[name] = body
    return bodies


def extract_export_async_functions(source: str) -> dict[str, str]:
    code = to_code_only_view(source)
    exports: dict[str, str] = {}
    for match in EXPORT_ASYNC_FUNCTION.finditer(code):
        name = match.group(1)
        body, _ = _extract_brace_body(code, match.end() - 1)
        exports[name] = body
    return exports


def _module_context_before(code: str, start: int) -> str | None:
    window = code[max(0, start - 120) : start]
    if re.search(r"\bfrom\s*$", window):
        return "from"
    if re.search(r"\bimport\s*\(\s*$", window):
        return "dynamic"
    if re.search(r"\brequire\s*\(\s*$", window):
        return "require"
    if re.search(r"(?<![\w$])\bimport\s*$", window):
        return "import"
    return None


def extract_module_specifiers(source: str) -> list[str]:
    lex = tokenize(source)
    specifiers: list[str] = []
    seen: set[str] = set()
    for string_token in lex.strings:
        if string_token.quote == "`":
            continue
        if _module_context_before(lex.code_only, string_token.start) is None:
            continue
        if string_token.value not in seen:
            seen.add(string_token.value)
            specifiers.append(string_token.value)
    return specifiers


def _function_parameters(code: str, name: str) -> list[str]:
    match = re.search(rf"function\s+{re.escape(name)}\s*\(([^)]*)\)", code)
    if not match:
        return []
    params: list[str] = []
    for part in match.group(1).split(","):
        token = part.strip()
        if token:
            params.append(re.split(r"\s*[:=]", token)[0].strip())
    return params


def _validate_root_cleanup_chain(source: str) -> bool:
    code = to_code_only_view(source)
    exports = extract_export_async_functions(source)
    if "unmount" not in exports:
        return False
    unmount_body = exports["unmount"]
    if re.search(r"\broot\s*\??\.\s*unmount\s*\(\s*\)", unmount_body):
        return True
    if not re.search(r"\bdisposeCurrent\s*\(\s*\)", unmount_body):
        return False
    functions = extract_function_bodies(source)
    dispose_current = functions.get("disposeCurrent", "")
    capture = re.search(r"\b(?:const|let)\s+(\w+)\s*=\s*root\b", dispose_current)
    if not capture:
        return False
    mounted_local = capture.group(1)
    if not re.search(r"\broot\s*=\s*undefined\b", dispose_current):
        return False
    if not re.search(
        rf"\bdisposeResources\s*\(\s*[^,]+,\s*{re.escape(mounted_local)}\s*\)",
        dispose_current,
    ):
        return False
    dispose_resources = functions.get("disposeResources", "")
    params = _function_parameters(code, "disposeResources")
    if len(params) < 2 or params[1] == "undefined":
        return False
    root_param = params[1]
    if not re.search(
        rf"\b{re.escape(root_param)}\s*\??\.\s*unmount\s*\(\s*\)",
        dispose_resources,
    ):
        return False
    if re.search(r"\bdisposeResources\s*\(\s*[^,]+,\s*undefined\s*\)", dispose_current):
        return False
    if re.search(r"\bdisposeResources\s*\(\s*[^,]+,\s*\{", dispose_current):
        return False
    return True


def _relative_path(project: Path, path: Path) -> str:
    return path.relative_to(project).as_posix()


def _source_files(project: Path) -> list[Path]:
    src = project / "src"
    if not src.is_dir():
        raise ValueError(f"src directory not found: {src}")
    return sorted(src.rglob("*.ts")) + sorted(src.rglob("*.tsx"))


def _read_package_scripts(project: Path) -> dict[str, str]:
    package_json = project / "package.json"
    if not package_json.is_file():
        raise ValueError(f"package.json not found: {package_json}")
    try:
        payload = json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid package.json: {exc.msg}") from None
    scripts = payload.get("scripts")
    if not isinstance(scripts, dict):
        raise ValueError("package.json missing scripts object")
    return {str(name): str(command) for name, command in scripts.items()}


def _is_valid_public_base(value: str) -> bool:
    try:
        candidate = value.strip()
        if not candidate:
            return False
        parsed = urlparse(candidate)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def _iter_token_scan_files(project: Path) -> list[Path]:
    files: list[Path] = []
    for root_name in ("src", "scripts"):
        root = project / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in TOKEN_SCAN_SUFFIXES:
                if not any(part in TOKEN_EXCLUDE_DIRS for part in path.parts):
                    files.append(path)
    for name in TOKEN_SCAN_FILES:
        path = project / name
        if path.is_file():
            files.append(path)
    return sorted(set(files))


def _normalize_module_specifier(specifier: str) -> str:
    normalized = specifier.replace("\\", "/").strip()
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    return normalized.rstrip("/")


def _points_to_mocks(specifier: str) -> bool:
    normalized = _normalize_module_specifier(specifier)
    return (
        "/mocks/" in normalized
        or normalized.startswith("mocks/")
        or normalized.endswith("/mocks")
        or normalized == "mocks"
        or normalized.endswith("/mocks/index")
    )


def _is_mock_import_allowed(relative: str) -> bool:
    return relative.startswith(MOCK_ALLOWED_PREFIX) or relative in MOCK_ALLOWED_FILES


def _strip_css_url_hash_refs(value: str) -> str:
    return re.sub(r"url\s*\(\s*#[^)]*\)", "", value, flags=re.IGNORECASE)


def _collect_css_declaration_values(block_body: str) -> list[str]:
    values: list[str] = []
    index = 0
    length = len(block_body)
    while index < length:
        if block_body[index] == "{":
            close = _scan_balanced_brace(block_body, index, length)
            inner = block_body[index + 1 : close - 1]
            values.extend(_collect_css_declaration_values(inner))
            index = close
            continue
        semi = block_body.find(";", index)
        if semi == -1:
            chunk = block_body[index:].strip()
            index = length
        else:
            chunk = block_body[index:semi].strip()
            index = semi + 1
        if not chunk or ":" not in chunk:
            continue
        _, _, value = chunk.partition(":")
        value = value.strip()
        if value:
            values.append(value)
    return values


def _extract_css_declaration_values(text: str) -> list[str]:
    code = to_code_only_view(text)
    values: list[str] = []
    index = 0
    while index < len(code):
        brace = code.find("{", index)
        if brace == -1:
            break
        close = _scan_balanced_brace(code, brace, len(code))
        if close <= brace:
            break
        values.extend(_collect_css_declaration_values(code[brace + 1 : close - 1]))
        index = close
    return values


def _find_css_hex_colors(text: str) -> list[str]:
    violations: list[str] = []
    seen: set[str] = set()
    for value in _extract_css_declaration_values(text):
        cleaned = _strip_css_url_hash_refs(value)
        for pattern in (INVALID_HEX, VALID_HEX):
            for match in pattern.finditer(cleaned):
                hex_value = match.group(0)
                if hex_value not in seen:
                    seen.add(hex_value)
                    violations.append(hex_value)
    return violations


def _is_color_context(code: str, string_start: int) -> bool:
    before = code[max(0, string_start - 80) : string_start]
    return bool(
        COLOR_PROPERTY_CONTEXT.search(before)
        or STYLE_OBJECT_CONTEXT.search(before)
        or TOKEN_OBJECT_CONTEXT.search(before)
    )


def _find_ts_color_violations(source: str) -> list[str]:
    lex = tokenize(source)
    violations: list[str] = []
    for string_token in lex.strings:
        if string_token.quote == "`":
            continue
        if not _is_color_context(lex.code_only, string_token.start):
            continue
        for match in INVALID_HEX.finditer(string_token.value):
            violations.append(match.group(0))
        for match in VALID_HEX.finditer(string_token.value):
            violations.append(match.group(0))
    for match in INVALID_HEX.finditer(lex.code_only):
        if _is_color_context(lex.code_only, match.start()):
            violations.append(match.group(0))
    for match in VALID_HEX.finditer(lex.code_only):
        if _is_color_context(lex.code_only, match.start()):
            violations.append(match.group(0))
    return violations


def _feature_page_paths(project: Path) -> list[Path]:
    features = project / "src/features"
    if not features.is_dir():
        return []
    return [
        path
        for path in features.rglob("*.tsx")
        if path.is_file() and ".test." not in path.name
    ]


def _page_has_action_surface(code: str) -> bool:
    return bool(
        re.search(
            r"<\s*(?:Button|Switch|Dropdown|Popconfirm|Menu\.Item|Upload)\b",
            code,
        )
        or re.search(r"\bon(?:Click|Submit|Change|Press)\s*=", code)
    )


def _page_is_data_request(code: str) -> bool:
    return bool(
        re.search(r"\bservice\s*[\.\(]", code)
        or re.search(r"\bEntityService\b", code)
        or (
            re.search(r"\buseEffect\s*\(", code)
            and re.search(r"\bservice\b", code)
        )
    )


def _find_state_branch_body(code: str, lex: LexResult, state_value: str) -> str | None:
    for string_token in lex.strings:
        if string_token.value != state_value or string_token.quote == "`":
            continue
        before = code[max(0, string_token.start - 40) : string_token.start]
        if not re.search(r"\bstate\s*===\s*$", before):
            continue
        close_paren = code.find(")", string_token.end)
        if close_paren == -1:
            continue
        brace_index = code.find("{", close_paren)
        if brace_index == -1:
            continue
        body, _ = _extract_brace_body(code, brace_index)
        return body
    return None


def _page_state_checks(source: str) -> dict[str, bool]:
    lex = tokenize(source)
    code = lex.code_only
    results = {name: False for name in STATE_VALUES}
    for state_value in STATE_VALUES:
        body = _find_state_branch_body(code, lex, state_value)
        if not body:
            continue
        if state_value == "loading" and re.search(r"<\s*Spin\b", body):
            results["loading"] = True
        elif state_value == "empty" and re.search(r"<\s*Empty\b", body):
            results["empty"] = True
        elif state_value == "error" and re.search(r"<\s*Result\b", body):
            results["error"] = True
        elif state_value == "forbidden" and re.search(
            r"<\s*Result\b[\s\S]*?status\s*=",
            body,
        ):
            results["forbidden"] = True
    return results


def _page_has_permission_disabled_guard(code: str) -> bool:
    return bool(
        re.search(
            r"disabled\s*=\s*\{[^}]*\bcan\s*\([^)]*PERMISSIONS\.[^}]*\}",
            code,
            re.DOTALL,
        )
    )


def _string_token_at(lex: LexResult, index: int) -> StringToken | None:
    for string_token in lex.strings:
        if string_token.quote == "`":
            continue
        if string_token.start >= index and string_token.start <= index + 3:
            return string_token
    return None


def parse_import_declarations(source: str) -> list[ImportDeclaration]:
    lex = tokenize(source)
    code = lex.code_only
    declarations: list[ImportDeclaration] = []
    for match in re.finditer(r"(?<![\w$])import(?![\w$])", code):
        index = match.end()
        index = _skip_ws(code, index)
        bindings: list[ImportBinding] = []
        side_effect = False
        if index < len(code) and code[index] == "{":
            body, index = _extract_brace_body(code, index)
            for part in body.split(","):
                part = part.strip()
                if not part:
                    continue
                if part.startswith("type "):
                    part = part[5:].strip()
                if " as " in part:
                    imported, local = (segment.strip() for segment in part.split(" as ", 1))
                else:
                    imported = local = part
                bindings.append(ImportBinding(imported, local))
            index = _skip_ws(code, index)
        elif index < len(code) and code[index] not in {",", "}"}:
            default_match = re.match(r"([\w$]+)", code[index:])
            if default_match:
                index += default_match.end()
                index = _skip_ws(code, index)
                if index < len(code) and code[index] == ",":
                    index += 1
                    index = _skip_ws(code, index)
                if index < len(code) and code[index] == "{":
                    body, index = _extract_brace_body(code, index)
                    for part in body.split(","):
                        part = part.strip()
                        if not part:
                            continue
                        if part.startswith("type "):
                            part = part[5:].strip()
                        if " as " in part:
                            imported, local = (segment.strip() for segment in part.split(" as ", 1))
                        else:
                            imported = local = part
                        bindings.append(ImportBinding(imported, local))
                    index = _skip_ws(code, index)
        if code.startswith("from", index):
            index += 4
            index = _skip_ws(code, index)
            module_token = _string_token_at(lex, index)
            if module_token is None:
                continue
            declarations.append(
                ImportDeclaration(module_token.value, tuple(bindings), side_effect=False)
            )
            continue
        if not bindings:
            module_token = _string_token_at(lex, index)
            if module_token is None:
                continue
            declarations.append(
                ImportDeclaration(module_token.value, tuple(), side_effect=True)
            )
    return declarations


def _config_provider_jsx_name(source: str) -> str | None:
    for declaration in parse_import_declarations(source):
        if declaration.module != "antd":
            continue
        for binding in declaration.bindings:
            if binding.imported == "ConfigProvider":
                return binding.local
    return None


def _extract_jsx_element_content(code: str, tag_name: str, start: int = 0) -> str | None:
    tag = re.escape(tag_name)
    open_pattern = re.compile(rf"<\s*{tag}\b")
    close_pattern = re.compile(rf"<\s*/\s*{tag}\s*>")
    open_match = open_pattern.search(code, start)
    if not open_match:
        return None
    gt = code.find(">", open_match.start())
    if gt == -1:
        return None
    if re.search(r"/\s*>$", code[open_match.start() : gt + 1]):
        return None
    content_start = gt + 1
    depth = 1
    pos = content_start
    while pos < len(code) and depth > 0:
        next_open = open_pattern.search(code, pos)
        next_close = close_pattern.search(code, pos)
        if next_close is None:
            return None
        if next_open and next_open.start() < next_close.start():
            nested_gt = code.find(">", next_open.start())
            if nested_gt == -1:
                return None
            if not re.search(r"/\s*>$", code[next_open.start() : nested_gt + 1]):
                depth += 1
            pos = nested_gt + 1
            continue
        depth -= 1
        if depth == 0:
            return code[content_start:next_close.start()]
        pos = next_close.end()
    return None


def _split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(text):
        if char in "{[(":
            depth += 1
        elif char in "}] )":
            depth = max(depth - 1, 0)
        elif char == "," and depth == 0:
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def _identifiers_from_param_list(params: str) -> set[str]:
    names: set[str] = set()
    params = params.strip()
    if not params:
        return names
    for part in _split_top_level_commas(params):
        part = part.strip()
        if not part:
            continue
        if part.startswith("{"):
            close = _scan_balanced_brace(part, 0, len(part))
            body = part[1 : close - 1]
            for segment in _split_top_level_commas(body):
                segment = segment.strip()
                if not segment:
                    continue
                if ":" in segment:
                    segment = segment.split(":", 1)[0].strip()
                if segment.startswith("..."):
                    segment = segment[3:].strip()
                name = segment.split("=")[0].strip()
                if re.fullmatch(r"[\w$]+", name):
                    names.add(name)
            continue
        if part.startswith("..."):
            part = part[3:].strip()
        name = re.split(r"\s*[:=]", part)[0].strip()
        if re.fullmatch(r"[\w$]+", name):
            names.add(name)
    return names


def _collect_parameter_identifiers(source: str) -> set[str]:
    code = to_code_only_view(source)
    identifiers: set[str] = set()
    patterns = [
        re.compile(r"(?:export\s+)?(?:async\s+)?function\s+\w+\s*\(([^)]*)\)"),
        re.compile(r"(?:export\s+)?const\s+\w+\s*=\s*\(([^)]*)\)\s*=>"),
    ]
    for pattern in patterns:
        for match in pattern.finditer(code):
            identifiers.update(_identifiers_from_param_list(match.group(1)))
    return identifiers


APP_OUTLET_PATTERNS = (
    re.compile(r"<\s*AppContent\b"),
    re.compile(r"<\s*RouterProvider\b"),
    re.compile(r"<\s*Routes\b"),
)


def _provider_has_app_outlet(content: str, source: str) -> bool:
    if not content.strip():
        return False
    for pattern in APP_OUTLET_PATTERNS:
        if pattern.search(content):
            return True
    if "children" in _collect_parameter_identifiers(source):
        return bool(re.search(r"\{\s*children\s*\}", content))
    return False


def _has_antd_config_provider_wrapper(source: str) -> bool:
    jsx_name = _config_provider_jsx_name(source)
    if jsx_name is None:
        return False
    lex = tokenize(source)
    code = lex.code_only
    if re.search(rf"function\s+{re.escape(jsx_name)}\b", code):
        return False
    content = _extract_jsx_element_content(code, jsx_name)
    if content is None:
        return False
    return _provider_has_app_outlet(content, source)


def _check_lifecycle(project: Path, report: ValidationReport) -> None:
    adapter = project / "src/micro-app/adapter.tsx"
    if not adapter.is_file():
        report.errors.append("qiankun lifecycle exports are incomplete in src/micro-app/adapter.tsx")
        return
    source = adapter.read_text(encoding="utf-8")
    exports = extract_export_async_functions(source)
    missing = [name for name in ("bootstrap", "mount", "unmount") if name not in exports]
    if missing:
        report.errors.append(
            "qiankun lifecycle exports are incomplete in src/micro-app/adapter.tsx "
            f"(missing: {', '.join(missing)})"
        )
        return
    if not _validate_root_cleanup_chain(source):
        report.errors.append(
            "unmount in src/micro-app/adapter.tsx must follow disposeCurrent -> "
            "mountedRoot=root -> disposeResources(..., mountedRoot) -> mountedRoot.unmount(), "
            "or call root?.unmount() directly"
        )


def _check_tokens(project: Path, report: ValidationReport) -> None:
    for path in _iter_token_scan_files(project):
        if TOKEN.search(path.read_text(encoding="utf-8")):
            report.errors.append(
                f"unreplaced template token found: {_relative_path(project, path)}"
            )


def _check_hard_coded_colors(project: Path, report: ValidationReport) -> None:
    for path in sorted(project.rglob("*")):
        if not path.is_file() or path.suffix not in COLOR_SCAN_SUFFIXES:
            continue
        if any(part in TOKEN_EXCLUDE_DIRS for part in path.parts):
            continue
        if ".test." in path.name or path.name in THEME_FILES:
            continue
        relative = _relative_path(project, path)
        source = path.read_text(encoding="utf-8")
        if path.suffix == ".css":
            colors = _find_css_hex_colors(source)
        else:
            colors = _find_ts_color_violations(source)
        if colors:
            report.errors.append(
                f"hard-coded color {colors[0]} outside theme tokens: {relative}"
            )


def _check_mock_imports(project: Path, source_files: list[Path], report: ValidationReport) -> None:
    for path in source_files:
        relative = _relative_path(project, path)
        if relative.startswith("src/mocks/") or _is_mock_import_allowed(relative):
            continue
        source = path.read_text(encoding="utf-8")
        for specifier in extract_module_specifiers(source):
            if _points_to_mocks(specifier):
                report.errors.append(
                    f"application source imports mocks directly (only src/micro-app/ and "
                    f"src/app/services.ts may wire mocks): {relative} -> {specifier}"
                )
                break


def _check_config_provider(project: Path, report: ValidationReport) -> None:
    app_file = project / "src/app/App.tsx"
    if not app_file.is_file():
        report.errors.append(
            "src/app/App.tsx must import ConfigProvider from antd and wrap content with "
            "an opening/closing <ConfigProvider> element"
        )
        return
    if not _has_antd_config_provider_wrapper(app_file.read_text(encoding="utf-8")):
        report.errors.append(
            "src/app/App.tsx must import ConfigProvider from antd and wrap content with "
            "an opening/closing <ConfigProvider> element"
        )


def _check_manifest_and_router(project: Path, report: ValidationReport) -> None:
    permissions_file = project / "src/auth/permissions.ts"
    manifest_file = project / "src/routes/manifest.tsx"
    if not manifest_file.is_file():
        manifest_file = project / "src/routes/manifest.ts"
    app_file = project / "src/app/App.tsx"

    if not permissions_file.is_file() or not PERMISSIONS_DECL.search(
        to_code_only_view(permissions_file.read_text(encoding="utf-8"))
    ):
        report.errors.append(
            "shared permission constants are missing from src/auth/permissions.ts"
        )
        return
    if not manifest_file.is_file():
        report.errors.append("route manifest file is missing under src/routes/")
        return
    manifest_code = to_code_only_view(manifest_file.read_text(encoding="utf-8"))
    if not MANIFEST_PERMISSIONS.search(manifest_code):
        report.errors.append(
            "route manifest must declare permissions: [PERMISSIONS.*] entries"
        )
    if not app_file.is_file():
        report.errors.append("src/app/App.tsx must consume the shared route manifest")
        return
    app_code = to_code_only_view(app_file.read_text(encoding="utf-8"))
    router_checks = {
        "createRouteManifest": bool(re.search(r"\bcreateRouteManifest\s*\(", app_code)),
        "buildVisibleMenu": bool(re.search(r"\bbuildVisibleMenu\s*\(\s*manifest\b", app_code)),
        "canAccessRoute": bool(re.search(r"\bcanAccessRoute\s*\(\s*route\b", app_code)),
        "manifest.map": bool(re.search(r"\bmanifest\s*\.\s*map\s*\(", app_code)),
    }
    missing_router = [name for name, ok in router_checks.items() if not ok]
    if missing_router:
        report.errors.append(
            "src/app/App.tsx must route and menu through the same manifest helpers "
            f"(missing: {', '.join(missing_router)})"
        )


def _check_feature_actions(project: Path, report: ValidationReport) -> None:
    feature_files = _feature_page_paths(project)
    if not feature_files:
        report.errors.append("no feature pages found for permission action guards")
        return
    for path in feature_files:
        code = to_code_only_view(path.read_text(encoding="utf-8"))
        if not _page_has_action_surface(code):
            continue
        if not _page_has_permission_disabled_guard(code):
            report.errors.append(
                f"{_relative_path(project, path)} must guard actions with "
                "disabled={{...can(..., PERMISSIONS.*)...}}"
            )


def _check_feature_states(project: Path, report: ValidationReport) -> None:
    feature_files = _feature_page_paths(project)
    if not feature_files:
        report.errors.append(
            "no feature pages found for loading/empty/error/forbidden baseline states"
        )
        return
    checked_any = False
    for path in feature_files:
        source = path.read_text(encoding="utf-8")
        code = to_code_only_view(source)
        if not _page_is_data_request(code):
            continue
        checked_any = True
        missing = [name for name, ok in _page_state_checks(source).items() if not ok]
        if missing:
            report.errors.append(
                f"{_relative_path(project, path)} missing JSX baseline states: {', '.join(missing)}"
            )
    if not checked_any:
        report.errors.append(
            "no feature pages declare data-request flows to validate baseline UI states"
        )


def _base_command_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("VITE_PUBLIC_BASE", None)
    return env


def _run_pnpm_script(
    project: Path,
    script: str,
    env: dict[str, str],
    timeout_seconds: int,
) -> CommandResult:
    try:
        result = subprocess.run(
            ("pnpm", script),
            cwd=project,
            check=False,
            env=env,
            timeout=timeout_seconds,
        )
        return CommandResult(exit_code=result.returncode, cause=CommandCause.RETURNED)
    except FileNotFoundError:
        return CommandResult(exit_code=EXIT_NOT_FOUND, cause=CommandCause.NOT_FOUND)
    except subprocess.TimeoutExpired:
        return CommandResult(exit_code=EXIT_TIMEOUT, cause=CommandCause.TIMEOUT)


def _record_command_failure(
    report: ValidationReport,
    label: str,
    result: CommandResult,
    timeout_seconds: int,
) -> None:
    report.commands[label] = result.exit_code
    if result.cause is CommandCause.NOT_FOUND:
        report.errors.append(f"command not found: {label}")
        return
    if result.cause is CommandCause.TIMEOUT:
        report.errors.append(f"command timed out after {timeout_seconds}s: {label}")
        return
    if result.exit_code:
        report.errors.append(f"command failed ({result.exit_code}): {label}")


def _validate_commands(
    project: Path,
    report: ValidationReport,
    vite_public_base: str | None,
    timeout_seconds: int,
) -> None:
    if shutil.which("pnpm") is None:
        report.errors.append("pnpm is not available on PATH")
        return
    try:
        scripts = _read_package_scripts(project)
    except ValueError as exc:
        report.errors.append(str(exc))
        return
    base_env = _base_command_env()
    for script in DEFAULT_COMMANDS:
        if script not in scripts:
            report.errors.append(f"package.json missing script: {script}")
            continue
        label = f"pnpm {script}"
        _record_command_failure(
            report,
            label,
            _run_pnpm_script(project, script, base_env, timeout_seconds),
            timeout_seconds,
        )
    if QIANKUN_COMMAND not in scripts:
        return
    if vite_public_base and _is_valid_public_base(vite_public_base):
        qiankun_env = base_env.copy()
        qiankun_env["VITE_PUBLIC_BASE"] = vite_public_base.strip()
        label = f"pnpm {QIANKUN_COMMAND}"
        _record_command_failure(
            report,
            label,
            _run_pnpm_script(project, QIANKUN_COMMAND, qiankun_env, timeout_seconds),
            timeout_seconds,
        )
    else:
        report.warnings.append(
            "skipped pnpm build:qiankun because VITE_PUBLIC_BASE was not provided "
            "as an absolute http(s) URL"
        )


def _validate_project_layout(project: Path, report: ValidationReport) -> bool:
    if not project.is_dir():
        report.errors.append(f"project directory not found: {project}")
        return False
    try:
        _read_package_scripts(project)
    except ValueError as exc:
        report.errors.append(str(exc))
        return False
    return True


def validate(
    project: Path,
    run_commands: bool = False,
    vite_public_base: str | None = None,
    command_timeout: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
) -> ValidationReport:
    report = ValidationReport()
    if not _validate_project_layout(project, report):
        return report
    try:
        source_files = _source_files(project)
    except ValueError as exc:
        report.errors.append(str(exc))
        return report
    _check_lifecycle(project, report)
    _check_tokens(project, report)
    _check_hard_coded_colors(project, report)
    _check_mock_imports(project, source_files, report)
    _check_config_provider(project, report)
    _check_manifest_and_router(project, report)
    _check_feature_actions(project, report)
    _check_feature_states(project, report)
    if run_commands:
        _validate_commands(project, report, vite_public_base, command_timeout)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--run-commands", action="store_true")
    parser.add_argument("--vite-public-base")
    parser.add_argument("--command-timeout", type=int, default=DEFAULT_COMMAND_TIMEOUT_SECONDS)
    args = parser.parse_args()
    report = validate(
        args.project,
        run_commands=args.run_commands,
        vite_public_base=args.vite_public_base,
        command_timeout=args.command_timeout,
    )
    for item in report.errors:
        print(f"ERROR: {item}")
    for item in report.warnings:
        print(f"WARN: {item}")
    raise SystemExit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
