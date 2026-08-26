# PKUSE 生成规则

以 [已捕获的 Ant Design v6 规范](ant-design-v6.md)（[中文版](ant-design-v6.zh.md)）作为视觉与交互基线。第一版直接采用 Ant Design 默认主题，不另造品牌色。

组件选用看 [components/INDEX.md](components/INDEX.md)，实现某个组件时只打开对应的 `components/<name>.md`。`antd/llms-full-cn.txt` 与 `antd/llms-semantic-cn.md` 是官网全文快照，默认不要整份阅读。

即时预览：打开 `docs/design-preview/index.html`，视觉对照 `ant-design-v6.md`，并含后台常用组件选用表。生成的子应用独立运行后，打开 `/design-system`。

## 色彩

- 品牌主色固定为 Ant Design 默认蓝 `#1677FF`（`colorPrimary`）。按钮、链接、焦点环、选中导航、激活 Tab 都用主色。
- `#52C41A` 是 `colorSuccess`，只表示成功/正常状态，不能当品牌色、顶栏、侧栏、页面底色或主按钮。
- 不要使用墨绿、森林绿、青绿色皮肤（例如 `#12372a`、`#176b4d`、`#f2f5f2` 这类自定义绿色壳层）。
- 分类用预设色，状态用语义色（success / warning / error / info），主操作才用主色。
- 使用 `ConfigProvider` 的 Token；不要硬编码颜色，也不要硬编码可用 Token 表达的间距。

## 必守规则

- 冲突时以 Natural、Certain、Meaningful、Growing 作为决策准则。
- 间距对齐 4px 网格，采用默认 14px 企业后台密度。
- 同一个决策面上只保留一个主按钮。
- 表格、表单、导航、浮层和反馈优先使用 Ant Design 组件，不要先造自定义等价物。
- 必须覆盖 hover、focus、loading、empty、error、disabled 和无权限状态。
- 自定义 CSS 使用应用命名空间，并配置应用级 `prefixCls` 与 CSS Variable key。
