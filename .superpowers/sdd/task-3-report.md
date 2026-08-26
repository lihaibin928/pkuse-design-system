# Task 3 Report: Deterministic scaffold engine and scenario manifests

## Status

**DONE（阶段性，已复核修复）** — 脚手架原子性、回归测试与未使用 import 清理已完成；模板渲染测试仍因 `assets/base-app` 尚未存在而按计划失败。

## TDD 记录

### RED — Step 1–2：先写测试，确认失败

**命令：**

```bash
cd /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator
python -m unittest tests.test_scaffold -v
```

**结果：**

```
FileNotFoundError: [Errno 2] No such file or directory:
  '.../pkuse-design-generator/scripts/scaffold.py'
```

符合预期：`scripts/scaffold.py` 尚不存在，测试在 import 阶段失败。

### GREEN（部分）— Step 3–5：实现后复测

**命令：**

```bash
cd /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator
python -m unittest tests.test_scaffold -v
```

**结果：**

```
test_rejects_invalid_name_and_existing_output ... ok
test_renders_templates_and_scene_manifest ... ERROR

FileNotFoundError: .../inventory-console/package.json

Ran 2 tests in 0.002s
FAILED (errors=1)
```

**解读：**

| 测试 | 结果 | 说明 |
| --- | --- | --- |
| `test_rejects_invalid_name_and_existing_output` | PASS | kebab-case 校验、拒绝已存在输出目录 |
| `test_renders_templates_and_scene_manifest` | ERROR | `assets/base-app/` 未创建（Task 4），无 `.tpl` 可渲染，`package.json` 不存在 |

符合 Task 3 简报 Step 5 预期：import 成功；唯一失败原因为 `base-app` 缺失。

## 交付文件

| 文件 | 动作 |
| --- | --- |
| `.cursor/skills/pkuse-design-generator/scripts/scaffold.py` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/data-management.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/approval-workflow.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/dashboard.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/system-config.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/monitoring.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/assets/scenarios/generic.json` | 新建 |
| `.cursor/skills/pkuse-design-generator/tests/test_scaffold.py` | 新建 |
| `.superpowers/sdd/task-3-report.md` | 新建（本报告） |

未修改任务范围外文件；未初始化 Git；未创建 commit。

## 实现摘要

### `scaffold(name, title, scene, output) -> Path`

1. **kebab-case 校验**：`^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`，违例抛出 `ValueError("application name must use kebab-case")`。
2. **拒绝覆盖**：`output.exists()` 时抛出 `FileExistsError("output already exists: ...")`。
3. **场景校验**：读取 `assets/scenarios/{scene}.json`；未知场景列出可用选项。
4. **Token 替换**：`__APP_NAME__`、`__APP_TITLE__`、`__APP_PREFIX__`（`-` → `_`）。
5. **模板渲染**：递归遍历 `assets/base-app/`，`.tpl` 后缀去除后写入目标路径。
6. **场景清单复制**：复制到 `{output}/src/generated/scene.json`。

CLI：`python scripts/scaffold.py --name ... --title ... --scene ... --output ...`

### 六个场景清单（对齐 `page-patterns.md`）

| 场景 | routes | patterns | permissions 要点 |
| --- | --- | --- | --- |
| `data-management` | list, detail | query-form, data-table, edit-drawer | read, create, update, delete, batch |
| `approval-workflow` | queue, detail, submitted | approval-queue, timeline, approve-reject-modal 等 | view, approve, reject, comment, submit |
| `dashboard` | overview | metric-cards, trends, ranking 等 | view, export |
| `system-config` | organization, users, roles, permissions, parameters | org-tree, permission-matrix 等 | org/users/roles/permissions/params 的 view/edit |
| `monitoring` | overview, resources, logs, alerts, operations | status-cards, log-search, ack-silence-modal 等 | overview/resources/logs/alerts/operations view + alerts-ack |
| `generic` | `[]` | `[]` | `[]` + `"composeFromRequest": true` |

各场景共享基础 states：`loading`, `empty`, `error`, `forbidden`（dashboard 额外含 `partial-error`, `refresh`）。

## 自检

- [x] TDD：先 RED（import 失败），后部分 GREEN（校验通过、模板测试按计划失败）。
- [x] kebab-case、拒绝覆盖、场景校验、递归 `.tpl` 渲染、三 token 替换、场景 JSON 复制。
- [x] 六个 JSON 与 `references/page-patterns.md` 路由/模式/权限语义一致；`generic` 含 `composeFromRequest`。
- [x] 未触碰 `assets/base-app/`（Task 4 范围）。
- [x] 未初始化 Git、未提交、未改任务外文件。

## 关注事项

1. **Task 4 阻塞**：`test_renders_templates_and_scene_manifest` 需 `assets/base-app/` 含 `package.json.tpl`、`src/main.tsx.tpl` 等模板后方可全绿。
2. **测试命令路径**：从仓库根目录 `python -m unittest .cursor/skills/.../test_scaffold.py` 在 Python 3.14 下可能报 `ValueError: Empty module name`；建议在 skill 目录内 `python -m unittest tests.test_scaffold -v` 或 Task 4 补充 `discover` 包装。
3. ~~**空模板目录行为**~~：已在复核修复中解决（见下文）。

---

## 复核修复（原子性与回归测试）

### 问题

1. 模板缺失、空模板或渲染中途异常时会留下/返回半成品 `output`。
2. 缺少未知场景拒绝与失败不留 output 的回归测试。
3. `scaffold.py` 存在未使用的 `json` import。

### TDD 修复记录

#### RED — 先增测试，确认失败

**新增测试：**

- `test_rejects_unknown_scene` — 未知场景抛出 `ValueError`，且不创建 `output`
- `test_does_not_leave_output_when_templates_missing` — `base-app` 缺失时不留 `output`
- `test_does_not_leave_output_when_render_fails` — 渲染中途异常时不留 `output`

**命令：**

```bash
cd /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator
python -m unittest tests.test_scaffold -v
```

**结果（修复前）：**

```
test_rejects_unknown_scene ... ok
test_rejects_invalid_name_and_existing_output ... ok
test_does_not_leave_output_when_templates_missing ... FAIL  # 未抛 FileNotFoundError，且留下 output
test_does_not_leave_output_when_render_fails ... FAIL       # 异常后 output 仍存在
test_renders_templates_and_scene_manifest ... ERROR         # 按计划因 base-app 缺失失败
```

#### GREEN — 实现原子性后复测

**`scaffold.py` 变更：**

1. 新增 `_template_files()`：预先拒绝缺失或无文件的 `assets/base-app`。
2. 在 `output.parent` 下用 `tempfile.mkdtemp` 创建同级 staging 目录，完整渲染后再 `staging.rename(output)`。
3. `except` 分支 `shutil.rmtree(staging)`，确保异常时不留下 `output` 或 staging。
4. 删除未使用的 `json` import。

**命令：**

```bash
cd /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator
python -m unittest tests.test_scaffold -v
```

**结果（修复后）：**

```
test_does_not_leave_output_when_render_fails ... ok
test_does_not_leave_output_when_templates_missing ... ok
test_rejects_invalid_name_and_existing_output ... ok
test_rejects_unknown_scene ... ok
test_renders_templates_and_scene_manifest ... ERROR

FileNotFoundError: templates not found: .../assets/base-app

Ran 5 tests in 0.005s
FAILED (errors=1)
```

**解读：**

| 测试 | 结果 | 说明 |
| --- | --- | --- |
| `test_rejects_unknown_scene` | PASS | 未知场景 + 无 output 残留 |
| `test_rejects_invalid_name_and_existing_output` | PASS | kebab-case / 已存在 output 拒绝 |
| `test_does_not_leave_output_when_templates_missing` | PASS | 预先拒绝缺失 base-app，无 output |
| `test_does_not_leave_output_when_render_fails` | PASS | 渲染异常清理 staging，无 output |
| `test_renders_templates_and_scene_manifest` | ERROR | 按计划：Task 4 未提供 base-app |

### 修改文件

| 文件 | 变更 |
| --- | --- |
| `.cursor/skills/pkuse-design-generator/scripts/scaffold.py` | 原子性 staging/rename、预校验模板、移除 `json` import |
| `.cursor/skills/pkuse-design-generator/tests/test_scaffold.py` | 新增 3 项回归测试 |
| `.superpowers/sdd/task-3-report.md` | 追加本修复记录 |

未初始化 Git；未创建 commit。

### 复核后关注事项

1. **Task 4 仍为唯一阻塞**：模板渲染集成测试需在 `base-app/` 就绪后全绿。
2. **空模板目录**：`_template_files()` 对空目录抛出 `FileNotFoundError("templates directory has no files: ...")`，与缺失目录区分消息，行为一致（均不留 output）。
3. **跨文件系统 rename**：staging 与 output 同在 `output.parent`，同盘 `rename` 为原子操作；若 Task 4 文档需跨挂载点输出，应另行评估。
