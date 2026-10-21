---
name: pkuse-prototype
description: Create or edit interactive enterprise product prototypes using the PKUSE Design and Ant Design v6 baseline. Use for 原型、交互稿、页面草图、表单流程、列表详情、审批、看板、组件演示或现有原型修改. Do not scaffold a complete Umi or qiankun application unless the user explicitly asks for a production application.
---

# PKUSE Prototype

用简体中文沟通和交付。代码标识符、命令、路径、权限码和 Token 名称保持原样。

## 规范读取

1. 开始设计前读取 `../pkuse-design-generator/references/DESIGN.md`。
2. 需要选用组件时，先读取 `../pkuse-design-generator/references/components/INDEX.md`，再只读取实际使用的 `components/<name>.md`。
3. 只有拆分文档缺少少见 API 或交互示例时，才在 `../pkuse-design-generator/references/antd/` 的快照中搜索对应章节；不要整份加载。

## 工作方式

1. 检查当前工作区、已有技术栈、页面结构和用户现有改动；优先在现有原型中增量修改。
2. 从用户描述提炼页面目标、主要角色、核心任务、关键字段与主流程。只询问会显著改变信息架构且无法合理推断的问题。
3. 先确定信息层级和交互状态，再实现视觉。原型必须能点击和演示关键流程，不只做静态截图。
4. React / Ant Design 项目优先使用真实 Ant Design 或 Pro Components；不要先造自定义等价组件。
5. 静态 HTML 原型沿用项目已有的组件挂载、公共样式和脚本结构，不为单个组件另建平行架构。
6. 实现后启动本地预览，检查目标视口下的默认态、hover、focus、展开层、选择结果和关键响应式布局。
7. 用浏览器截图或等价方式做视觉校验；修复明显的对齐、遮挡、溢出和交互问题后再交付。

## 原型约束

- 默认采用 PKUSE / Ant Design v6 企业后台密度：14px 正文、32px 控件、4px 间距网格、6px 控件圆角、8px 表面圆角。
- 主色使用 `#1677FF`；成功绿只表示成功或正常状态。
- 同一决策面只保留一个主操作，其余操作降级为默认、文字或链接按钮。
- 使用真实、简洁的中文业务数据，避免 lorem ipsum、无意义占位和装饰性指标。
- 覆盖任务相关的加载、空数据、错误、禁用、无权限或确认状态；不机械添加与任务无关的状态。
- 浮层、表格、表单、导航与反馈优先使用设计系统组件和 Token。
- 保留用户现有技术栈与文件组织。除非用户明确要求，不把轻量原型升级成完整生产应用，也不引入新的框架或构建系统。

## 当前设计系统仓库

当工作区包含 `docs/design-preview` 时：

- `*.html` 是页面入口与组件挂载点。
- `assets/theme.css` 和 `assets/layout.js` 是共享视觉与导航资源。
- `vendor/protable.js` 是现有 React、Ant Design、Pro Components 与组件示例的统一浏览器包。
- 新组件应优先沿用现有统一渲染方式；不要为了单个组件在 `assets/` 下增加独立实现。
- 若只有构建产物、缺少源码与构建配置，允许对统一包做带唯一匹配和语法校验的最小机械修改，并更新页面缓存版本。

## 交付

最终用简体中文简要说明：

- 完成了哪些页面或交互
- 修改的关键文件
- 验证过的关键状态
- 本地预览地址或启动命令
- 仍属于演示或 Mock 的行为
