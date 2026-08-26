# PKUSE Design Generator Skill 设计规格

## 目标

创建项目级 Cursor Agent Skill `pkuse-design-generator`。该 Skill 根据业务描述生成完整、可运行的企业后台子应用，并确保不同业务场景共享一致的 Ant Design 设计语言、工程结构和 qiankun 接入契约。

第一版生成结果采用：

- React
- Vite
- TypeScript
- Ant Design
- React Router
- pnpm
- Mock 数据与可替换 API Adapter
- 基础 RBAC
- 独立运行与 qiankun 挂载双模式

## 使用场景与触发范围

当用户提出以下需求时应使用该 Skill：

- 创建后台管理系统或管理控制台
- 创建 qiankun 微前端子应用
- 创建数据管理、审批、运营看板、系统配置或监控运维应用
- 根据业务对象生成完整的企业级 React 后台应用

Skill 的默认交付物是完整子应用，而不是单独页面或视觉稿。

## 首批场景

### 数据管理

包含查询表单、数据表格、批量操作、详情、新增和编辑流程。

### 审批流程

包含待办列表、流程详情、流程时间线、审核意见和通过/驳回操作。

### 运营看板

包含指标卡、趋势、排行、维度筛选和异常提醒。

### 系统配置

包含组织树、用户与角色、权限矩阵和参数配置。

### 监控运维

包含状态概览、资源列表、日志、告警和操作记录。

### 通用组合

根据业务描述识别领域对象与关键任务，组合前述页面模式；不创建脱离既有设计语言的新模式。

## Skill 架构

Skill 保存于 `.cursor/skills/pkuse-design-generator/`，采用渐进式加载：

```text
pkuse-design-generator/
├── SKILL.md
├── references/
│   ├── ant-design-v6.md
│   ├── design-system.md
│   ├── qiankun-contract.md
│   ├── page-patterns.md
│   └── engineering.md
├── assets/
│   ├── base-app/
│   └── scenarios/
├── scripts/
│   ├── scaffold.*
│   └── validate.*
└── evals/
    └── evals.json
```

### `SKILL.md`

负责触发说明、需求收集、场景识别、资产选择、生成步骤和验证闭环。保持精简，不重复引用文件中的详细规范。

### Ant Design 原文与 PKUSE 覆盖层

`references/ant-design-v6.md` 保存 <https://ant.design/design.md> 的完整原文快照，保留 YAML Token、设计原则、组件语义、Do/Don't 和定制方式，并记录来源、文档版本和抓取日期。

`references/design-system.md` 只保存 PKUSE 的生成决策和对 Ant Design 原文的章节引用。第一版不覆盖品牌 Token，直接采用 Ant Design 默认规范。未来企业品牌规范通过该覆盖层增加，不修改原始快照。

### 工程与场景参考

- `qiankun-contract.md` 定义生命周期、路由、通信、样式隔离和卸载清理。
- `page-patterns.md` 定义六类场景的信息架构和页面组合。
- `engineering.md` 定义目录结构、API、Mock、RBAC、错误处理和测试要求。
- `assets/base-app/` 提供稳定的完整应用骨架。
- `assets/scenarios/` 提供场景最小模板片段。
- `scripts/` 执行确定性脚手架与自动校验，减少模型每次重新生成固定代码造成的漂移。

## 生成流程

1. 判断请求是否属于企业后台子应用，并识别一个或多个业务场景。
2. 从用户描述提取应用名称、业务对象、角色、关键操作和特殊字段。
3. 仅询问无法可靠推断且会显著影响结果的信息。
4. 使用固定技术栈与基础应用骨架创建工程。
5. 注入 qiankun 双模式运行时。
6. 按场景组合页面、路由、菜单、权限点、领域类型、Mock 和 API Adapter。
7. 根据 Ant Design 原文及 PKUSE 规则检查组件语义、密度、状态与 Token 使用。
8. 运行类型检查、生产构建、qiankun 契约和静态规范校验。
9. 修复失败项并重新验证。
10. 输出生成位置、运行命令、权限信息、场景说明、校验结果和真实 API 接入清单。

## 生成应用结构

每个应用至少包含：

- 应用入口与 qiankun 适配器
- 路由与菜单配置
- 布局与页面容器
- 页面与领域组件
- 领域类型
- 类型化 Service Contract
- HTTP Adapter
- Mock Adapter 与 Mock 数据
- 用户、角色和权限配置
- 错误边界与状态页面
- 设计 Token 与 ConfigProvider
- 基础测试与运行文档

页面只能依赖类型化 Service，不得直接读取 Mock 数据。

## qiankun 运行时契约

### 版本策略

第一版以当前 npm 稳定版 qiankun 2.x 为基线。Vite 适配能力封装在 `micro-app/adapter` 中，使业务代码不直接依赖具体社区插件。适配器可在后续官方 Vite 方案稳定后替换。

### 生命周期

应用导出 `bootstrap`、`mount` 和 `unmount`，并可选导出 `update`。

- 独立运行时挂载到本地 `#root`，启用本地用户和 Mock。
- qiankun 模式从 `props.container` 内查找挂载点。
- 每次 `mount` 创建新的 React Root 与 Router。
- `unmount` 销毁 React Root、请求、订阅、定时器和全局监听。

### 路由

路由基路径由主应用通过 props 注入；独立运行使用 `/`。业务页面不直接读取 qiankun 全局变量。

### 主子应用通信

使用统一 TypeScript Props 契约传递：

- 当前用户
- 权限码
- 认证信息
- 路由跳转能力
- 全局状态订阅与更新能力

业务模块通过本地适配层消费这些能力，保持 qiankun 依赖集中。

### 样式隔离

- 使用应用级 Ant Design `ConfigProvider`。
- 配置独立 CSS 前缀与 CSS Variable key。
- 自定义样式使用应用命名空间。
- 禁止页面向全局注入无前缀选择器。
- 不把 Shadow DOM 作为默认前提，以避免组件弹层和第三方库兼容问题。

## 设计系统规则

生成结果遵循 Ant Design v6 原文基线：

- 使用 Natural、Certain、Meaningful、Growing 作为冲突决策准则。
- 使用 Ant Design Token，不硬编码颜色和可由 Token 表达的间距。
- 使用 4 px 间距网格和企业后台默认信息密度。
- 一个决策面只保留一个主按钮。
- 明确提供 hover、focus、loading、empty、error、disabled 和 permission-denied 状态。
- 预设颜色用于标签、图表和分类；语义颜色用于状态；主色用于主要操作。
- 表格、表单、导航、浮层和反馈使用 Ant Design 既有组件语义。
- 自定义视觉不能绕开 ConfigProvider、Token 或组件级配置。

## RBAC

权限码是路由、菜单和操作按钮的共同数据源：

- 无路由权限时进入 403 页面。
- 无菜单权限时不展示入口。
- 无操作权限时隐藏或禁用操作，并保留必要解释。
- 独立运行时提供至少两组本地角色用于验证权限差异。
- 会话失效与权限不足使用不同状态和恢复路径。

## 错误处理

错误按层级处理：

- qiankun 挂载失败：记录应用标识和挂载阶段，呈现可恢复提示。
- 路由错误：进入应用内 404。
- React 渲染错误：由页面 Error Boundary 隔离。
- API 错误：区分网络、认证、权限、业务校验和服务端错误。
- 表单错误：定位到字段并保留用户已输入内容。
- Mock 未匹配：明确报告缺少的契约，不返回模糊空数据。

## 评测方案

### 对照场景

1. 库存与商品数据管理
2. 费用报销审批中心
3. 服务监控与告警平台

每个场景分别运行加载 Skill 和不加载 Skill 的生成任务。

### 客观检查

- 依赖安装成功。
- TypeScript 检查通过。
- 生产构建通过。
- 应用可独立启动。
- 正确导出 qiankun 生命周期。
- `unmount` 执行完整清理。
- 路由、菜单和权限点一致。
- Mock 与真实 API Adapter 可切换。
- 页面不直接耦合 Mock。
- ConfigProvider 与 Token 使用正确。
- 不硬编码规范中的颜色与间距。
- 包含加载、空数据、错误和无权限状态。
- 包含运行说明、主应用接入说明和 API 清单。

### 人工评审

使用 `skill-creator` 的评审页面比较：

- 信息架构是否符合场景。
- 结果是否像真实企业应用而不是组件展览。
- 三种场景是否形成合理差异。
- 视觉层级和操作反馈是否符合 Ant Design 价值观。

根据客观通过率、构建结果和人工反馈迭代 Skill。

## 完成标准

Skill 达到以下条件后可视为第一版完成：

- 三个对照场景均能生成可构建的完整应用。
- 生成应用同时支持独立运行和 qiankun 挂载。
- 自动校验覆盖工程、生命周期、权限和关键设计规则。
- Ant Design 原文快照与 PKUSE 覆盖层职责清晰。
- 用户在评审页面确认场景结构和视觉结果可接受。
- Skill 文档保持渐进式加载，`SKILL.md` 不承载大段重复参考内容。

## 非目标

第一版不包含：

- Vue 子应用生成。
- qiankun 主应用生成。
- 企业品牌 Token 定制。
- 真实后端实现。
- 低代码页面编辑器。
- 跨多个子应用的复杂业务编排。
