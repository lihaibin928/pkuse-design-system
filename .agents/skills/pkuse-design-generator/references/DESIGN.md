<!--
Source: https://ant.design/design.md
Translation of: ant-design-v6.md
Captured: 2026-08-18
Runtime baseline verified: antd 6.7.1
-->

---
version: alpha
name: Ant Design
description: 蚂蚁集团的企业级 React UI 设计系统，围绕 Natural、Certain、Meaningful、Growing 四条价值观构建。
colors:
  primary: '#1677FF'
  success: '#52C41A'
  warning: '#FAAD14'
  error: '#FF4D4F'
  info: '#1677FF'
  blue: '#1677FF'
  blue-7: '#0958D9'
  purple: '#722ED1'
  cyan: '#13C2C2'
  green: '#52C41A'
  magenta: '#EB2F96'
  red: '#F5222D'
  orange: '#FA8C16'
  yellow: '#FADB14'
  volcano: '#FA541C'
  geekblue: '#2F54EB'
  gold: '#FAAD14'
  lime: '#A0D911'
  surface: '#FFFFFF'
  surface-container: '#FAFAFA'
  surface-layout: '#F5F5F5'
  on-surface: '#1F1F1F'
  on-surface-variant: '#595959'
  on-surface-disabled: '#BFBFBF'
  outline: '#D9D9D9'
  outline-variant: '#F0F0F0'
typography:
  display-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 38px
    fontWeight: '600'
    lineHeight: 46px
  headline-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
  headline-md:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  title-md:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 22px
  body-lg:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 20px
  code:
    fontFamily: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace"
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  none: 0px
  sm: 2px
  md: 4px
  DEFAULT: 6px
  lg: 8px
  xl: 16px
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  control-height: 32px
components:
  button-primary:
    backgroundColor: '{colors.primary}'
    textColor: '#FFFFFF'
    typography: '{typography.body-md}'
    rounded: '{rounded.DEFAULT}'
    height: 32px
    padding: 0 15px
  button-primary-hover:
    backgroundColor: '#4096FF'
  button-primary-active:
    backgroundColor: '#0958D9'
  button-default:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.on-surface}'
    typography: '{typography.body-md}'
    rounded: '{rounded.DEFAULT}'
    height: 32px
    padding: 0 15px
  button-default-hover:
    textColor: '#4096FF'
  input-field:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.on-surface}'
    typography: '{typography.body-md}'
    rounded: '{rounded.DEFAULT}'
    height: 32px
    padding: 4px 11px
  input-field-focus:
    backgroundColor: '{colors.surface}'
  select-field:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.on-surface}'
    typography: '{typography.body-md}'
    rounded: '{rounded.DEFAULT}'
    height: 32px
    padding: 0 11px
  card:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 24px
  modal:
    backgroundColor: '{colors.surface}'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 20px 24px
  menu-item-selected:
    backgroundColor: '#E6F4FF'
    textColor: '{colors.primary}'
    typography: '{typography.body-md}'
  tabs-tab-active:
    textColor: '{colors.primary}'
    typography: '{typography.body-md}'
  table-header:
    backgroundColor: '{colors.surface-container}'
    textColor: '{colors.on-surface}'
    typography: '{typography.title-md}'
    padding: 16px
  tag:
    backgroundColor: '{colors.surface-container}'
    textColor: '{colors.on-surface}'
    typography: '{typography.body-sm}'
    rounded: '{rounded.md}'
    padding: 0 7px
  tooltip:
    backgroundColor: 'rgba(0, 0, 0, 0.85)'
    textColor: '#FFFFFF'
    typography: '{typography.body-md}'
    rounded: '{rounded.md}'
    padding: 6px 8px
  dropdown-item-hover:
    backgroundColor: '{colors.surface-container}'
    textColor: '{colors.on-surface}'
  alert-success:
    backgroundColor: '#F6FFED'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 8px 12px
  alert-warning:
    backgroundColor: '#FFFBE6'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 8px 12px
  alert-error:
    backgroundColor: '#FFF2F0'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 8px 12px
  alert-info:
    backgroundColor: '#E6F4FF'
    textColor: '{colors.on-surface}'
    rounded: '{rounded.lg}'
    padding: 8px 12px
  badge-status-error:
    backgroundColor: '{colors.error}'
    rounded: '{rounded.full}'
    width: 6px
    height: 6px
  tag-blue:
    backgroundColor: '#E6F4FF'
    textColor: '{colors.blue-7}'
    typography: '{typography.body-sm}'
    rounded: '{rounded.md}'
    padding: 0 7px
---

# Pkuse Design 设计规范

本文件是 Pkuse Design 的设计系统规范文件，由两部分组成：「Pkuse 生成规则」为部门叠加约定，「Ant Design v6 基线规范」为视觉与交互基线全文（含上方 front-matter 中的全部 Design Token）。冲突时以下方基线为准，叠加规则不得与之矛盾。

即时预览：打开 `docs/design-preview/index.html`，视觉对照本文件基线部分；组件选用看 [components/INDEX.md](components/INDEX.md)。生成的子应用独立运行后，打开 `/design-system`。

## Pkuse 生成规则

以已捕获的 Ant Design v6 规范（[英文原版](ant-design-v6.md)，中文全文已并入本文件「Ant Design v6 基线规范」）作为视觉与交互基线。第一版直接采用 Ant Design 默认主题，不另造品牌色。

组件选用看 [components/INDEX.md](components/INDEX.md)，实现某个组件时只打开对应的 `components/<name>.md`。`antd/llms-full-cn.txt` 与 `antd/llms-semantic-cn.md` 是官网全文快照，默认不要整份阅读。

即时预览：打开 `docs/design-preview/index.html`，视觉对照 `ant-design-v6.md`，并含后台常用组件选用表。生成的子应用独立运行后，打开 `/design-system`。

### 色彩

- 品牌主色固定为 Ant Design 默认蓝 `#1677FF`（`colorPrimary`）。按钮、链接、焦点环、选中导航、激活 Tab 都用主色。
- `#52C41A` 是 `colorSuccess`，只表示成功/正常状态，不能当品牌色、顶栏、侧栏、页面底色或主按钮。
- 不要使用墨绿、森林绿、青绿色皮肤（例如 `#12372a`、`#176b4d`、`#f2f5f2` 这类自定义绿色壳层）。
- 分类用预设色，状态用语义色（success / warning / error / info），主操作才用主色。
- 使用 `ConfigProvider` 的 Token；不要硬编码颜色，也不要硬编码可用 Token 表达的间距。

### 必守规则

- 冲突时以 Natural、Certain、Meaningful、Growing 作为决策准则。
- 间距对齐 4px 网格，采用默认 14px 企业后台密度。
- 同一个决策面上只保留一个主按钮。
- 表格、表单、导航、浮层和反馈优先使用 Ant Design 组件，不要先造自定义等价物。
- 必须覆盖 hover、focus、loading、empty、error、disabled 和无权限状态。
- 自定义 CSS 使用应用命名空间，并配置应用级 `prefixCls` 与 CSS Variable key。
- antd v6 组件 API 以 `color` / `variant` 模型为准：虚线按钮用 `variant="dashed"`，旧 `dashed` 布尔属性已废弃不生效。

### 页面模版与布局规范（Pkuse 叠加）

以下为部门页面模版的原型构建标准，生成应用框架、表单页、列表页时按本节落地，覆盖上方基线的对应默认值。定稿原型见 `docs/design-preview/scene-entry.html`（表单页）与 `scene-display.html`（列表页），样式细节以 `docs/design-preview/assets/theme.css` 为准。

**切图与字体资产（从 `docs/design-preview/assets/` 复制，不要重新导出）**

| 文件 | 用途 | 说明 |
| --- | --- | --- |
| `header-bg.svg` | 顶栏底图 | Figma「Group 228」，1928×72 含出血边距 |
| `logo-icon.svg` | 顶栏徽标 | Figma「image 87」，内容区 41×37 |
| `layout-sider.svg` | 侧栏背景图 | 251×914，含出血边距 |
| `fonts/inter-latin-400.woff2`、`fonts/inter-latin-500.woff2` | 侧栏菜单字体 | Inter latin 子集，中文回退 PingFang SC |

**应用框架（顶栏 + 侧边菜单 + 主显示区）**

顶栏（高 60px，固定在顶部）：

- 背景：底色 `#EBF4FE` + `header-bg.svg`（`no-repeat 50% 0 / 100.4167% 112.5%`，切图出血裁掉后内容区正好铺满）+ 下缘阴影 `0 4px 4px rgba(0,0,0,.03)`。
- 左起：徽标 41×37（`logo-icon.svg`，`-3.97px 0 / 121.03% 123.72%` 映射）、品牌字「方正小标宋 FZXiaoBiaoSong-B05」24px/400 `#333`（回退 STZhongsong / SimSun）、一级导航；右端：Ai⁺ 徽标、帮助、通知、用户头像。
- 一级导航：纯文字项（14px `#333`），不带图标；选中项主色文字 + 底部 2px 主色短下划线（`::after`，距底 9px、左右缩进 14px、圆角 2px），不得出现第二条（白色）底线。
- 导航超出可视宽度时溢出隐藏，两侧放 `‹` `›` 箭头按钮（22×22，`#4E5969`，hover 主色）：点击平滑滚动 240px，滚到头的一侧箭头隐藏；鼠标滚轮悬停在导航上时纵向滚动转为横向。
- 顶栏内容均为固定元素，不随主显示区滚动。

侧边菜单（宽 235px，固定）：

- 背景：底色 `#F2F7FD` + `layout-sider.svg`（`no-repeat left -12px bottom -14px / 112% 108%`）+ 右缘阴影 `0 4px 7.8px rgba(0,46,98,.21)`。
- 菜单项通栏（无圆角、无左右留白）：高 43px、项间距 6px（节距 49px）；图标 20×20 距左 31px；文字距左 59px（与图标间距 8px）。
- 文字 Inter 16px/500 `#4E5969`（`@font-face` 自托管上方 woff2）；hover 浅主色底 `rgba(12,118,240,.08)`。
- 选中态：通栏实色 `#0C76F0`，白字白图标（不是浅蓝底 + 主色文字）。
- 不显示分组标签；不同页面使用不同语义图标（如表单页 `FormOutlined`、列表页 `TableOutlined`）。
- 暂无收起态，不要自行添加收起功能。

主显示区：

- 背景 `#F7FBFF`，四周内边距 16px；顶栏与侧边菜单固定，仅主显示区滚动。

**表单页（新建/编辑表单）**

页面 = 主显示区里的一张白卡片（内边距 16px、圆角 8px、阴影 `0 1px 2px rgba(0,0,0,.05), 0 1px 6px -1px rgba(0,0,0,.03), 0 2px 4px rgba(0,0,0,.03)`），操作栏与表单都在卡片内；不要把表单裸放在页面底色上。

- 操作栏在卡片内吸顶：高 52px、白底、下边线 `#F0F0F0`、上侧圆角与阴影与卡片一致；静止时位于卡片顶部（距顶栏 16px），滚动后吸附到主显示区顶缘（`position: sticky; top: -16px`，负外边距抵消卡片内边距）。
- 操作栏结构：`← 返回`（线性箭头图标 + 文字 `rgba(0,0,0,.65)`，hover 主色）、1px 分隔线 `#F0F0F0`、面包屑、右侧 `暂存 / 提交 / 重置`。
- 面包屑只做层级位置展示：仅当前页一项、纯文本、不做链接、`#1890FF` 文字（无外框）。
- 操作按钮必须使用真实 antd Button（波纹等点击特效为组件原生行为），不要手写仿制。
- 表单主体 ProForm：`layout: 'horizontal'`、`colon: false`、`labelCol: { flex: '0 0 84px' }`。**不要使用 `grid` / `colProps` / `labelWidth`**：该版本（pro-components 3.1.14-0）普通表单不处理 `labelWidth`，且关闭栅格后默认退化为纵向布局，必须显式 horizontal；两列栅格用样式实现——列距 48px、字段行距 22px、多行文本与上传区通栏。
- 标签右对齐、色 `rgba(0,0,0,.65)`、右侧留白 10px；控件高 32px。
- 字段分组：分组标题 16px/600 通栏，右侧 1px 延伸细线（`::after` 撑满剩余宽度），上下边距 4px / 18px。
- 可选字段的说明文字放 `extra`：12px `rgba(0,0,0,.55)`、上边距 4px。
- 上传区不带标签、通栏：Upload.Dragger，虚线框 `#D9D9D9`、底 `#FAFCFF`、圆角 8px、内边距 22px；图标 34px `rgba(0,0,0,.25)`、主文案 14px/500 `rgba(0,0,0,.65)`、说明 12px `rgba(0,0,0,.55)`，三行间距 6px，整体高约 133px。
- 字段与校验（演示字段，按「基础信息 / 登记信息 / 辅助信息」三组）：姓名（必填）、手机号（必填 + 11 位格式校验）、部门（下拉）、登记类型（单选，默认个人登记）｜入职日期（日期，宽度 100%）、随行人数（数字 1–99 + 说明）、需要接送（开关）、随行设备（多选，**`options` 必须带 `value`**，否则整组不显示）、服务评分（评分）、物品重量（滑杆 0–30 + 说明）｜备注（多行，通栏）、附件上传（通栏）。
- `暂存` 为非破坏操作（仅提示，不校验不清空）；`提交` 通过校验后提示成功并重置表单。
- 响应式：主显示区宽 ≤860px 时表单退化为单列。

**列表页（ProTable）**

- 查询区一行最多 4 个查询元素（`span: 6`）；查询项超出一行时使用展开 / 收起。
- 常用查询项：单号（模糊输入）、姓名（模糊输入）、类型（下拉 valueEnum）、状态（下拉 valueEnum）、登记时间（区间）。
- 工具栏：右侧主操作 `+ 新建`（primary）与 `导入`、`批量删除`；勾选行后不显示「已选择 X 项」提示条（`tableAlertRender: false`）。
- 表头背景 `#E6F4FF`（覆盖基线），文字保持默认深色。
- 分页位于表格右下角：页码 + 每页条数选择。

## Ant Design v6 基线规范

### 概述

本文描述 **Ant Design v6** 的默认浅色主题。系统遵循语义化版本：大版本（v5 → v6）表示设计语言重构，小版本与补丁版本保持本文稳定。主版本内每次发布的 Token 漂移见 [CHANGELOG.en-US.md](https://github.com/ant-design/ant-design/blob/master/CHANGELOG.en-US.md)。

Ant Design 是蚂蚁集团用于交付企业软件的开源设计系统，主要面向中后台控制台、看板和运营工具。系统创建于 2015 年，目的是给大型产品团队一套有主张的共同基础，使密集、数据丰富的界面不必在每个屏幕上重新决定基础规则。

四个价值观指导系统中的每一个决策：

- **Natural（自然）。** 界面遵循既有惯例，不让回头用户感到意外。优先采用操作系统和前代企业软件中已存在的模式，而不是发明新交互。
- **Certain（确定）。** 用户始终知道自己处于什么状态、输入产生了什么结果、下一步是什么。悬停、焦点、加载和错误状态明确且一致。
- **Meaningful（有意义）。** 视觉强调只留给行动。不传达信息的装饰一律去掉。
- **Growing（生长）。** 系统可以从小表单扩到密表格、再扩到多租户管理控制台，而不失去一致性。

### 色彩

色板由一个 **primary** 品牌种子、四个语义状态种子（`success`、`warning`、`error`、`info`），以及文字与表面的中性基色构成。种子经 `@ant-design/colors` 自动展开为背景浅色、悬停、按下和描边阶梯——改种子，整套派生色一起移动。

`#1677FF` 被选为主色，因为蓝色读起来可信、专注，既没有更深海军蓝的刻板，也没有高饱和青色的俏皮。它是操作、链接、焦点环、选中导航和激活 Tab 的默认品牌色。

无障碍说明：本文记录的是 Ant Design 的默认视觉 Token。部分品牌色组合（尤其是白字配 `#1677FF`，以及主文字配浅选中底）低于 WCAG AA 小字 4.5:1 对比度阈值。若需严格无障碍，通过 `ConfigProvider` 加深 `colorPrimary`，或做组件级 Token 覆盖，不要发明一次性颜色。

运行时 Token 系统中的中性文字和叠层用 `rgba(0, 0, 0, α)` 表达，而不是实心灰 hex。原因是叠层：文字压在浅色卡片或彩色单元格高亮上时，实心灰会切断底色，透明黑会自然混合。四级标准透明度是 `0.88`（主文字，本文导出为 `#1F1F1F`）、`0.65`（次文字，`#595959`）、`0.45`（三级 / 描述文字），以及 `0.25`（占位 / 禁用，`#BFBFBF`）。文档中的 hex 是叠在白底上的等效结果，供需要 hex 的静态导出目标使用；能走 alpha 的下游应优先使用 `@ant-design/cssinjs` 的 `rgba()` 形式。

预设色（`blue`、`purple`、`cyan`、`green`、`magenta`、`red`、`orange`、`yellow`、`volcano`、`geekblue`、`gold`、`lime`；运行时 Token 中 `pink` 是 `magenta` 的已弃用别名）只留给标签、图表和分类可视化——绝不用于主界面可操作元素。状态用功能色（`success` / `warning` / `error` / `info`），每个屏幕上最重要的那个操作才用 `primary`。

### 字体

基础字号是 **14px**，不是 16。企业控制台用信息密度换取额外易读空间——1440px 宽的窗口需要同时舒服地放下侧栏、顶栏、八列表格和详情区。14px 正文在这些栏宽下接近约 75 字符的扫视甜点。

字体栈按系统 UI 字体优先：Apple 的 `-apple-system`，然后 `BlinkMacSystemFont`，然后 Windows 的 `Segoe UI`，然后 Android / ChromeOS 的 `Roboto`，然后 `Helvetica Neue`，然后 `Arial`，Linux 用 `Noto Sans` 兜底。Emoji 回退保持简短。代码字体按同样顺序使用 `SFMono-Regular`、`Consolas`、`Liberation Mono`、`Menlo` 和 `Courier`。

产品界面只用 **两个字重**：400（正文、控件、菜单项、Tab 标签）和 600（`fontWeightStrong` —— 标题、表头，以及任何 title 级文字）。细体（100–300）、粗体（700+）和斜体不用于界面骨架——它们会破坏系统追求的平静、确定语气。斜体只允许出现在长文本文档里。选中 / 激活态的视觉强调来自颜色和描边（边框、下划线），不是字重。

### 布局

所有间距对齐 **4px 网格**。六档间距刻度（`unit`、`xs`、`sm`、`md`、`lg`、`xl` → 4 / 4 / 8 / 16 / 24 / 32px）覆盖系统中每一个间隙、槽和内边距。Token 驱动的代码里不出现魔法数字——`padding: 11px`、`gap: 13px`；输入框水平 11px 内边距之所以存在，只因为设计早于 4px 网格，一像素迁移会牵动海量已有屏幕。

表面采用 **三层模型**：

1. **`bg-layout`**（`#F5F5F5`）——页面背景。它包围并容纳其他一切。
2. **`bg-container`**（`#FFFFFF`）——卡片、面板、表格和表单的表面。大多数内容住在这里。
3. **`bg-elevated`**（`#FFFFFF`，与 `bg-container` 同 hex）——对话框、下拉、气泡的表面。与 `bg-container` 的区别不靠颜色，靠阴影。

永远不要在产品代码里写死 `#FFF` 或 `#FAFAFA`。读 Token。三层模型让暗色算法可以翻转表面阶梯而不拆布局。

### 层级与深度

Ant Design 是 **flat-first（扁平优先）**。层级由边框和色调对比承担。阴影只出现在真正浮于上下文之上的表面。

阴影 Token 由 `colorShadow` 生成，因此同一名称可适应浅色和深色主题。核心档位是：

- **Tertiary**（`boxShadowTertiary`）——轻抬起阴影：`0 1px 2px 0 rgba(0,0,0,0.05), 0 1px 6px -1px rgba(0,0,0,0.03), 0 2px 4px 0 rgba(0,0,0,0.03)`。
- **Popup**（`boxShadow` 和 `boxShadowSecondary`）——标准浮层阴影：`0 6px 16px 0 rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)`。
- **Card**（`boxShadowCard`）——更紧的卡片抬起阴影，用于卡片需要与容器分离时。
- **方向性抽屉与溢出阴影**（`boxShadowDrawer*`、`boxShadowTabsOverflow*`）——贴边表面和滚动提示的专用 Token。
- **Popover arrow**（`boxShadowPopoverArrow`）——只用于 Tooltip 和气泡上的小三角指针。

动效使用三种时长和一组 cubic-bezier 缓动，全部以 Token 暴露：

- `motionDurationFast` —— 0.1s，用于状态变化（悬停、焦点、按下）。
- `motionDurationMid` —— 0.2s，用于组件内部过渡（折叠、淡入）。
- `motionDurationSlow` —— 0.3s，用于表面级变化（对话框进入、抽屉滑入）。

缓动是预定义的：`motionEaseInOut`、`motionEaseOut`、`motionEaseIn`、`motionEaseOutBack`、`motionEaseOutCirc` 等。不要任意挑选 `transition-timing-function`。若设计需求对不上现有缓动，用 `motionEaseInOut` 然后继续。

### 形状

默认圆角是 **6px**。足够现代亲和，又小到 32px 高的按钮仍呈现干净、接近矩形的轮廓，适合密集表单。

按组件类别：

- **控件**（按钮、输入、选择、下拉触发）—— 6px（`rounded.DEFAULT`）。
- **表面**（卡片、对话框、抽屉、通知）—— 8px（`rounded.lg`）。
- **标签和小芯片** —— 4px（`rounded.md`）。
- **Tooltip 和气泡** —— 4px（`rounded.md`）。

全胶囊（`rounded.full`，9999px）只给圆形头像、徽标和圆点——不给按钮或标签。直角（0px）留给表格和分段控件的内边。相邻元素混用圆角是坏味道：8px 圆角的卡片里不该放 16px 圆角的按钮。

### 组件

组件原型捕捉系统最常见的表面和状态。下列每一项都对应 YAML front-matter 中的 Token 引用。

- **Button（primary）** —— 每个屏幕唯一的主导操作。实心 `primary` 填充、白字、32px 高、6px 圆角。悬停把填充变亮为 `#4096FF`；按下变暗为 `#0958D9`。同一决策面不要叠两个 `primary` 按钮。
- **Button（default）** —— 次要操作。白表面上透明背景、深色文字、1px 描边。悬停把文字色改为 `#4096FF`；边框跟着变色。
- **Input field** —— 32px 高，与按钮对齐。细 1px 描边；焦点态把边框加粗为主色并加上内发光。占位文字使用 `on-surface-disabled`。
- **Select** —— 视觉上与 Input 相同。触发器在交互前读起来就像输入框。
- **Card** —— 工作马容器。白表面、8px 圆角、可选 `boxShadowCard` 层级。内边距四边 24px；嵌套控件保持 16px 间隙。
- **Modal** —— 与 Card 同表面和圆角，但使用次级阴影档，居中叠在 `rgba(0, 0, 0, 0.45)` 遮罩上。主体 padding 为上下 20px × 左右 24px。
- **Menu（选中项）** —— `#E6F4FF` 背景、`primary` 文字。这是导航里“你在这里”的唯一视觉线索。
- **Tabs（激活项）** —— `primary` 文字和 2px `primary` 下划线。未激活 Tab 为 `on-surface-variant`。任何状态下 Tab 都没有背景填充。
- **Table（表头行）** —— `surface-container` 背景，`title-md` 字体（14px / 600）。表体行只在悬停时变底，默认不做斑马纹——系统相信用户能读密集数据，不需要斑马条纹。
- **Tag** —— 小分类标签。4px 圆角、12px 字、低饱和粉彩来自预设色板。关键状态不要用 Tag——用 Alert 或 Badge。
- **Alert** —— 语义反馈表面。成功、警告、错误和信息 Alert 使用浅语义底 + 正常文字色；状态由图标和底色传达，不用低对比的彩色正文。
- **Badge 状态点** —— 紧凑状态指示。危急状态可用 `error` 填充，但在无障碍关键流程里，圆点不能代替文字。
- **Tooltip** —— 高对比反相表面：`rgba(0,0,0,0.85)` 背景、白字。始终由框架定位，不要手动钉死。
- **Dropdown menu（项悬停）** —— 悬停用 `surface-container` 填充，不改文字色。悬停提示本身已经足够。

### 对与错

- **做** 用四条设计价值观当平局裁决。两种做法冲突时，更能让用户状态确定、更易读的那个胜出。
- **不做** 同一表面叠两个 `primary` 色按钮。只留一个，其余降为 `default`。
- **做** 从 `colors.surface`、`colors.surface-container` 和 `colors.surface-layout` 读表面。它们对应三层模型。
- **不做** 硬编码 `#FFFFFF` 或 `#FAFAFA`。hex 是附带结果，角色才重要。
- **做** 找不到更具体 Token 时，组件级过渡使用 `motionDurationMid`（0.2s）。
- **不做** 发明自定义 `cubic-bezier` 曲线。用已命名缓动。
- **做** 把预设色板（`blue` 到 `lime`）留给标签、图表和分类可视化。
- **不做** 在预设色板外铸造强调色给一次性 UI 表面。若某屏看起来需要，多半该改布局。
- **做** 通过间距刻度，把每一个间隙、内边距和槽对齐 4px 网格。
- **不做** 在产品代码里用魔法数字。刻度缺一档时，该重看设计，而不是一像素覆盖。

### 定制

上文 YAML front-matter 中的每个值都是 `defaultAlgorithm` 产出的**默认值**——浅色主题。Ant Design 主题化比替换 Design Token 更广：包含算法派生、组件级覆盖、动态切换、嵌套主题作用域、CSS 变量输出、静态 Token 消费，以及零运行时 CSS 提取。完整运行时 API 与示例见 [Customize Theme](https://ant.design/docs/react/customize-theme.md)。

主题配置的主入口是 `ConfigProvider` 的 `theme` 属性：

1. **Seed token 覆盖。** 向 `ConfigProvider` 传入 `theme.token` 以替换任意种子。主色和语义色种子（`colorPrimary`、`colorSuccess`、`colorWarning`、`colorError`、`colorInfo`）会展开为派生阶梯，而 `colorBgBase` 与 `colorTextBase` 驱动中性表面和文字。间距、圆角和字号种子同理。

2. **算法切换。** 设置 `theme.algorithm` 以更换派生逻辑。`defaultAlgorithm`、`darkAlgorithm` 和 `compactAlgorithm` 可单独使用，也可组成数组——不要手工反色；算法会处理非线性的色板、表面、阴影和尺寸关系。

3. **组件级覆盖。** `theme.components.Button`（或任一组件的 Token 命名空间）可以覆盖单个组件的 Component Token 和所消费的 Alias Token，不影响其他组件。在组件配置里，`algorithm` 可以让该覆盖仍跟随种子 Token 关系。

4. **运行时作用域。** 改 `ConfigProvider.theme` 可动态切换主题；嵌套的 `ConfigProvider` 实例创建局部主题，未改的 Token 从父级继承。静态 API（如 `message.xxx`、`Modal.xxx`、`notification.xxx`）不会自动拿到周围上下文；需要主题化静态反馈时，使用 hook API、`App` 或显式 context holder。

5. **Token 消费与输出。** React 内用 `theme.useToken()`，React 外用 `theme.getDesignToken()` 消费已解析 Token。需要 CSS 变量时用 `theme.cssVar`；必须关闭运行时样式生成时，用 `theme.zeroRuntime` 配合预构建或提取的 CSS。

自定义主题时，先保住 Ant Design 的交互结构、密度、状态反馈和组件语义，再改最小必要种子集：通常是 `colorPrimary`、状态色、`borderRadius`、`fontFamily`、`fontSize` 和中性表面基色。品牌页可以看起来不同，但表单、表格、导航、浮层、焦点态和校验反馈仍应像 Ant Design。避免生成绕过 Token、算法、`theme.components`、CSS 变量或提取静态样式的自定义 CSS 规则；若主题无法通过这些官方层表达，应视为设计系统扩展，而不是页面一次性样式。
