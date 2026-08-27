---
name: pkuse-design-generator
description: Generates complete enterprise React admin sub-applications using Umi Max, TypeScript, Ant Design and qiankun. Use whenever the user asks to create a 后台管理系统、管理控制台、qiankun 子应用、CRUD 数据平台、审批中心、运营看板、系统配置或监控运维应用, even when they do not explicitly ask for a design-system generator.
---

# PKUSE Design Generator

生成完整可运行的企业后台子应用，而不是组件展览。工程结构以 `project-struct-react/` 与 `references/engineering.md` 为准。

对用户的全部回复使用简体中文：询问补全信息、进度说明、校验结果和最终汇报均用中文。代码标识符、命令、路径、权限码和 Token 名称保持原样。

## 工作流

1. 用 `references/page-patterns.md` 判断场景。
2. 只询问会改变架构且无法可靠推断的信息：应用名、核心实体、角色、关键操作或特殊字段。
3. 阅读 `references/design-system.md`、`references/qiankun-contract.md` 和 `references/engineering.md`。
4. 运行 `python scripts/scaffold.py --name <kebab-name> --title "<title>" --scene <scene> --output <path>`。
5. 生成领域页面时先读 `references/components/INDEX.md`，再只打开实际用到的 `references/components/<name>.md`。
6. 仅当拆分文件缺少少见 API 或示例时，再打开 `references/antd/llms-full-cn.txt` 或 `references/antd/llms-semantic-cn.md` 里对应的 `## <name>-cn` 章节。不要整份阅读这两份快照。
7. 按 Feature 模块化生成页面：`src/features/<slice>/{types,services,hooks,components}`，`src/pages/` 只做薄组装；更新 `src/router/routes.ts`、`src/access.ts` 与 `mock/`。
8. 运行 `python scripts/validate.py <path> --run-commands`。
9. 修复全部报错并重新校验。
10. 用中文汇报输出路径、命令、本地角色、所选模式、校验结果和仍走 Mock 的真实 API 清单。

## 设计决策

- 选择 Token、密度或主题时，阅读 `references/ant-design-v6.md` 或其译文 `references/ant-design-v6.zh.md`。
- 选择或实现具体组件时，阅读 `references/components/<name>.md`，不要把 `references/antd/` 下的全文快照整份读进上下文。
- 主色保持 Ant Design 默认蓝 `#1677FF`。不要把成功绿或自定义绿色壳层当作品牌色。
- 保留 `/design-system` 预览路由，便于对照基线 Token 和组件。
- 同一个决策面只保留一个主操作。
- 必须覆盖加载、空数据、错误、禁用和无权限状态。
- 页面只依赖 feature services / hooks，不得直接读取 `mock/`。
- qiankun 相关行为只放在 `.umirc.ts`（`qiankun.slave`）和 `src/app.ts`（layout、生命周期钩子）。业务 pages / features 不得导入 qiankun。

## 输出摘要

用简体中文返回：

- 生成路径
- `yarn install` 与 `yarn dev` 命令
- 独立运行和 qiankun 挂载说明
- 角色与权限
- 校验结果
- 仍使用 Mock 实现的 API
