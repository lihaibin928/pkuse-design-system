#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANTD = ROOT / "references" / "antd"
COMPONENTS = ROOT / "references" / "components"
CAPTURED = "2026-08-24"

SKIP_SLUGS = {"_util", "changelog", "overview"}
SKIP_SEMANTIC_PREFIXES = ("blog",)

FULL_HEAD = re.compile(r"^## ([a-z0-9_-]+)-cn\s*$", re.M)
SEM_HEAD = re.compile(r"^# (.+?)-cn(?: (\S+))? Semantic\s*$", re.M)
YAML_BLOCK = re.compile(r"^---\n(.*?)\n---", re.S | re.M)
WHEN_TO_USE = re.compile(
    r"^## 何时使用(?:\s*\{#[^}]+\})?\s*\n(.*?)(?=^## |\Z)",
    re.S | re.M,
)
EXAMPLES = re.compile(
    r"^## 代码演示(?:\s*\{#[^}]+\})?\s*\n(.*?)(?=^## |\Z)",
    re.S | re.M,
)
FENCE_TSX = re.compile(r"```tsx\n(.*?)```", re.S)
SEM_PARTS = re.compile(
    r"^### Semantic Parts\s*\n(.*?)(?=^### |\Z)",
    re.S | re.M,
)
SEM_EXAMPLE = re.compile(
    r"^### 使用案例\s*\n(.*?)(?=^### |\Z)",
    re.S | re.M,
)

PKUSE_NOTES = {
    "button": "- 同一个决策面只保留一个主按钮，其余降为 default / link / text。\n- 危险操作用 `danger`，并配合 `Popconfirm` 或确认对话框。",
    "table": "- 列表主界面用表格，不要用卡片宫格替代。\n- 表头和状态色走 Token；默认不做斑马纹。\n- 删除 / 批量操作必须确认，并校验权限。",
    "form": "- 筛选条与编辑表单都用 `Form`，提交走类型化 Service。\n- 校验失败定位到字段，保留已输入内容。",
    "modal": "- 短流程用 `Modal`；表单超出抽屉容量才用独立页。\n- 同一决策面不要并排两个主按钮。",
    "drawer": "- 列表上的新增 / 编辑优先用 `Drawer` 或 `Modal`，不要默认拆 `/new`。",
    "alert": "- 用语义类型表达状态，不要把整页做成成功绿。\n- 关键状态用 Alert / Result，不要只用 Tag。",
    "tag": "- Tag 只表示分类或非关键状态，不用作主操作或危险确认。",
    "badge": "- 状态点不能在无障碍关键流程里代替文字。",
    "result": "- 401 与 403、404、5xx 使用不同 Result，不要收成同一条文案。",
    "empty": "- 空数据保留查询区；区分「无数据」和「无搜索结果」。",
    "spin": "- 加载用 Spin / Skeleton，不要换绿色骨架屏。",
    "menu": "- 选中态只用组件语义（浅底 + 主色文字），不要自造导航皮肤。",
    "tabs": "- 激活项用主色文字和下划线，不要给 Tab 加背景填充。",
    "select": "- 触发器在交互前应看起来像 Input，高度与按钮对齐。",
    "input": "- 占位符用禁用文字色；焦点态走主色描边。",
}


def split_by(pattern: re.Pattern[str], text: str) -> list[tuple[re.Match[str], str]]:
    matches = list(pattern.finditer(text))
    chunks: list[tuple[re.Match[str], str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunks.append((match, text[match.end() : end]))
    return chunks


def yaml_field(raw: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.+)$", raw, re.M)
    if not match:
        return ""
    value = match.group(1).strip().strip("'\"")
    if value in {"", "|"}:
        return ""
    return value


def yaml_group(raw: str) -> str:
    nested = re.search(r"(?m)^group:\s*\n(?:[ \t]+.+\n)*?[ \t]+title:\s+(.+)$", raw)
    if nested:
        return nested.group(1).strip().strip("'\"")
    inline = re.search(r"(?m)^group:\s+([^:\n]+)$", raw)
    if inline:
        return inline.group(1).strip().strip("'\"")
    return "其他"


def first_tsx(block: str) -> str:
    match = FENCE_TSX.search(block)
    if not match:
        return ""
    return f"```tsx\n{match.group(1).rstrip()}\n```"


def parse_full(text: str) -> dict[str, dict[str, str]]:
    docs: dict[str, dict[str, str]] = {}
    for match, body in split_by(FULL_HEAD, text):
        slug = match.group(1)
        if slug in SKIP_SLUGS:
            continue
        yaml_match = YAML_BLOCK.search(body)
        raw_yaml = yaml_match.group(1) if yaml_match else ""
        when = WHEN_TO_USE.search(body)
        examples = EXAMPLES.search(body)
        source = re.search(r"^Source:\s*(\S+)", body, re.M)
        docs[slug] = {
            "title": yaml_field(raw_yaml, "title") or slug,
            "subtitle": yaml_field(raw_yaml, "subtitle"),
            "group": yaml_group(raw_yaml),
            "description": yaml_field(raw_yaml, "description"),
            "source_doc": source.group(1) if source else "",
            "when": when.group(1).strip() if when else "",
            "demo": first_tsx(examples.group(1)) if examples else "",
        }
    return docs


def parse_semantic(text: str) -> dict[str, list[dict[str, str]]]:
    docs: dict[str, list[dict[str, str]]] = defaultdict(list)
    for match, body in split_by(SEM_HEAD, text):
        slug = match.group(1).strip()
        if slug in SKIP_SLUGS or any(slug.startswith(prefix) for prefix in SKIP_SEMANTIC_PREFIXES):
            continue
        if " " in slug:
            continue
        variant = match.group(2) or ""
        source = re.search(r"^Source:\s*(\S+)", body, re.M)
        heading = re.search(r"^##\s+(.+)$", body, re.M)
        parts = SEM_PARTS.search(body)
        example = SEM_EXAMPLE.search(body)
        docs[slug].append(
            {
                "variant": variant,
                "heading": heading.group(1).strip() if heading else slug,
                "source": source.group(1) if source else "",
                "parts": parts.group(1).strip() if parts else "",
                "example": first_tsx(example.group(1)) if example else "",
            }
        )
    return docs


def render_component(slug: str, full: dict[str, str] | None, semantics: list[dict[str, str]]) -> str:
    title = (full or {}).get("title") or (semantics[0]["heading"] if semantics else slug)
    subtitle = (full or {}).get("subtitle") or ""
    group = (full or {}).get("group") or "其他"
    description = (full or {}).get("description") or ""
    source_doc = (full or {}).get("source_doc") or f"https://ant.design/components/{slug}-cn.md"
    source_sem = next((item["source"] for item in semantics if item["source"]), "")
    heading = f"{title} {subtitle}".strip() if subtitle and subtitle != title else title

    lines = [
        f"<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 {CAPTURED}。不要手改后当权威源。 -->",
        "",
        f"# {heading}",
        "",
        f"- 分组：{group}",
        f"- 组件文档：<{source_doc}>",
    ]
    if source_sem:
        lines.append(f"- 语义文档：<{source_sem}>")
    lines.append(f"- 全文快照：`../antd/llms-full-cn.txt` 中的 `## {slug}-cn`")
    if source_sem:
        lines.append(f"- 语义快照：`../antd/llms-semantic-cn.md` 中的 `{slug}-cn`")
    if description:
        lines += ["", description]
    lines += ["", "## 何时使用", ""]
    lines.append((full or {}).get("when") or "官方文档未提供「何时使用」。按页面模式选择该组件，不要用自定义等价物替代。")
    lines += ["", "## PKUSE", "", "- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。"]
    extra = PKUSE_NOTES.get(slug)
    if extra:
        lines.append(extra)
    lines.append("- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。")
    if (full or {}).get("demo"):
        lines += ["", "## 基本示例", "", "只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。", "", full["demo"]]
    if semantics:
        lines += ["", "## 语义槽", ""]
        for item in semantics:
            label = item["heading"]
            lines += [f"### {label}", ""]
            lines.append(item["parts"] or "该变体未提供 Semantic Parts。")
            if item["example"]:
                lines += ["", item["example"]]
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_index(items: list[tuple[str, str, str, str]]) -> str:
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for slug, title, subtitle, group in items:
        grouped[group].append((slug, title, subtitle))
    lines = [
        "# 组件选用索引",
        "",
        f"由 `scripts/split_antd_docs.py` 从 `../antd/` 快照生成（{CAPTURED}）。",
        "",
        "生成页面时只打开本页和实际用到的 `references/components/<name>.md`。",
        "不要整份阅读 `llms-full-cn.txt` 或 `llms-semantic-cn.md`。",
        "拆分文件缺少少见 API 或示例时，再打开快照里对应的 `## <name>-cn` 章节。",
        "",
        "## 后台常用",
        "",
        "数据管理 / 审批 / 看板优先看：`table` `form` `button` `input` `select` `modal` `drawer` `menu` `tabs` `tag` `alert` `badge` `empty` `result` `spin` `pagination` `descriptions` `date-picker` `popconfirm` `dropdown` `card` `statistic` `timeline` `list` `tree` `transfer`。",
        "",
    ]
    for group in sorted(grouped, key=lambda name: (name == "其他", name)):
        lines += [f"## {group}", ""]
        for slug, title, subtitle in sorted(grouped[group], key=lambda item: item[0]):
            label = f"{title} {subtitle}".strip() if subtitle else title
            lines.append(f"- [{label}]({slug}.md) — `{slug}`")
        lines.append("")
    return "\n".join(lines)


def prepend_capture_header(path: Path, source: str, kind: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.startswith("<!--"):
        return
    header = (
        f"<!--\n"
        f"Source: {source}\n"
        f"Captured: {CAPTURED}\n"
        f"Kind: {kind}\n"
        f"Usage: 权威快照。生成时默认不要整份阅读，先打开 references/components/<name>.md。\n"
        f"-->\n\n"
    )
    path.write_text(header + text, encoding="utf-8")


def main() -> None:
    full_path = ANTD / "llms-full-cn.txt"
    semantic_path = ANTD / "llms-semantic-cn.md"
    prepend_capture_header(full_path, "https://ant.design/llms-full-cn.txt", "component docs")
    prepend_capture_header(semantic_path, "https://ant.design/llms-semantic-cn.md", "component semantics")

    full_docs = parse_full(full_path.read_text(encoding="utf-8"))
    semantic_docs = parse_semantic(semantic_path.read_text(encoding="utf-8"))
    slugs = sorted(set(full_docs) | set(semantic_docs))

    COMPONENTS.mkdir(parents=True, exist_ok=True)
    for stale in COMPONENTS.glob("*.md"):
        stale.unlink()

    index_items: list[tuple[str, str, str, str]] = []
    for slug in slugs:
        full = full_docs.get(slug)
        semantics = semantic_docs.get(slug, [])
        (COMPONENTS / f"{slug}.md").write_text(
            render_component(slug, full, semantics),
            encoding="utf-8",
        )
        index_items.append(
            (
                slug,
                (full or {}).get("title") or slug,
                (full or {}).get("subtitle") or "",
                (full or {}).get("group") or "其他",
            )
        )
    (COMPONENTS / "INDEX.md").write_text(render_index(index_items), encoding="utf-8")
    print(f"wrote {len(slugs)} component files + INDEX.md")


if __name__ == "__main__":
    main()
