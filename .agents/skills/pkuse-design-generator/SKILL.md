---
name: pkuse-design-generator
description: Generates complete enterprise React admin sub-applications using Umi Max, TypeScript, Ant Design and qiankun. Accepts three kinds of input - a URL link, requirement/design text, or a system screenshot. Use whenever the user asks to create a 后台管理系统、管理控制台、qiankun 子应用、CRUD 数据平台、审批中心、运营看板、系统配置或监控运维应用, even when they do not explicitly ask for a design-system generator.
---

# PKUSE Design Generator

生成完整可运行的企业后台子应用，而不是组件展览。

对用户的全部回复使用简体中文：询问补全信息、进度说明、校验结果和最终汇报均用中文。代码标识符、命令、路径、权限码和 Token 名称保持原样。

## 输入源

接受以下任意一种输入，可同时提供多种互补：

1. **URL 链接**：目标系统或参考设计的页面地址。用浏览器打开实际渲染内容，提取信息架构、菜单层级、核心列表、表单字段与操作入口；无法访问时明确说明，并降级为按其余输入推断。
2. **需求设计文字**：一段需求或设计描述。从中提取应用名、核心实体、角色、关键操作与状态要求；描述含糊、不足以定架构时，按工作流第 2 步追问。
3. **系统设计截图**：现有系统的界面截图。按截图还原页面结构、菜单层级、表格列、表单控件与操作入口；截图中的可见信息优先于其他输入的推断。

多种输入同时提供时交叉比对，以覆盖信息最全的一份为准；相互矛盾的地方向用户确认后再动手。

## 工作流

1. 识别输入源类型（URL 链接 / 需求设计文字 / 系统设计截图，见「输入源」），解析出场景、实体、角色与操作，判断应用场景（数据管理、审批流程、监控运维、仪表盘或系统配置）。
2. 只询问会改变架构且无法可靠推断的信息：应用名、核心实体、角色、关键操作或特殊字段。
3. 阅读 `references/DESIGN.md`。
4. 生成领域页面时先读 `references/components/INDEX.md`，再只打开实际用到的 `references/components/<name>.md`。
5. 仅当拆分文件缺少少见 API 或示例时，再打开 `references/antd/llms-full-cn.txt` 或 `references/antd/llms-semantic-cn.md` 里对应的 `## <name>-cn` 章节。不要整份阅读这两份快照。
6. 按 Feature 模块化生成页面：`src/features/<slice>/{types,services,hooks,components}`，`src/pages/` 只做薄组装；更新 `src/router/routes.ts`、`src/access.ts` 与 `mock/`。
7. 运行 `python scripts/validate.py <path> --run-commands`。
8. 修复全部报错并重新校验。
9. 用中文汇报输出路径、命令、本地角色、所选模式、校验结果和仍走 Mock 的真实 API 清单。

## 设计决策

- 选择 Token、密度或主题时，阅读 `references/DESIGN.md` 的「Ant Design v6 基线规范」部分。
- 生成页面模版（应用框架、表单页、列表页）时，遵循 `references/DESIGN.md` 的「页面模版与布局规范（Pkuse 叠加）」原型构建标准，并复制其中列出的切图与字体资产（`docs/design-preview/assets/`）：应用框架为 60px 固定顶栏（切图底图 + 徽标 + 小标宋品牌字 + 带滑动箭头的一级导航）+ 235px 固定侧边菜单（Inter 字体、通栏选中蓝条、右缘阴影）+ 独立滚动的主显示区（四周 16px）；表单页为白卡片 + 卡内吸顶操作栏（返回 / 面包屑 / 暂存 / 提交 / 重置）+ 分组两列表单（标签 84px 右对齐无冒号、列距 48px、可选字段带说明文字、上传区通栏）；列表页查询区一行最多 4 个查询元素，超出走展开 / 收起，表头背景 `#E6F4FF`，工具栏为 新建 / 导入 / 批量删除。
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
