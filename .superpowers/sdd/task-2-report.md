# Task 2 Report: qiankun, engineering, and page-pattern references

## Status

**DONE** — 三个 references 已创建，结构测试全部通过。

## Test command and output

```bash
python -m unittest discover .cursor/skills/pkuse-design-generator/tests -p 'test_skill_structure.py' -v
```

```
test_overlay_links_to_source_without_duplicating_it ... ok
test_skill_metadata_and_references ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

## Changed files

| File | Action |
| --- | --- |
| `.cursor/skills/pkuse-design-generator/references/qiankun-contract.md` | 新建 |
| `.cursor/skills/pkuse-design-generator/references/engineering.md` | 新建 |
| `.cursor/skills/pkuse-design-generator/references/page-patterns.md` | 新建 |
| `.superpowers/sdd/task-2-report.md` | 新建（本报告） |

未修改任务范围外文件；未初始化 Git；未创建 commit。

## Self-review

### qiankun-contract.md

- 包含简报要求的三个 TypeScript 接口（`UserIdentity`、`GlobalStateActions`、`MicroAppProps`）原文。
- 定义 `bootstrap` / `mount` / `unmount` / 可选 `update` 及每次 mount 新建 React Root 与 Router。
- 规定 scoped container lookup（`data-micro-app-root`）、独立运行 basename `/` 与嵌入模式 `props.routeBase`。
- 列出 unmount 清理项：root、订阅、定时器、监听器、AbortController。
- 说明全局状态、鉴权传播、样式隔离与挂载失败处理。

### engineering.md

- 包含简报规定的 `src/` 目录树及职责表。
- 要求 strict TypeScript、feature-local tests、typed service injection、AbortController。
- 区分 401 / 403 / 404 / 5xx / 网络错误处理路径。
- 规定 Error Boundary、单一 `PERMISSIONS` 常量驱动 route/menu/action RBAC。
- Mock 未匹配时显式报错，页面不直接依赖 Mock。

### page-patterns.md

- 六个场景（`data-management`、`approval-workflow`、`dashboard`、`system-config`、`monitoring`、`generic`）均使用简报指定 schema。
- 每节覆盖 trigger signals、primary user task、routes、page states、Ant Design patterns、permissions、avoid。
- 视觉语义通过引用 `design-system.md` / `ant-design-v6.md` 保持与 Ant Design 原文分离。

### Overlay separation

- 未修改 `ant-design-v6.md` 或 `design-system.md`。
- 新文档不含 Ant Design 原文重复内容，仅引用 overlay 与设计快照。

## Concerns

1. **结构测试范围有限**：当前 `test_skill_structure.py` 仅校验文件存在与 overlay 链接，不断言 references 正文关键词；后续任务（scaffold/validate）应补充契约级校验。
2. **qiankun 2.x 适配细节**：文档以 qiankun 2.x 为基线并封装于 `micro-app/adapter`；具体 Vite 插件选型留待 Task 3+ 模板实现时落地。
3. **page-patterns 路由粒度**：`system-config` 与 `monitoring` 默认多路由；`generic` 场景依赖模型推断，生成时须按用户描述裁剪，避免过度脚手架。
