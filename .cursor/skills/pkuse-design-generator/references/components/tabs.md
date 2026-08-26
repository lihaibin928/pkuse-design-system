<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Tabs 标签页

- 分组：导航
- 组件文档：<https://ant.design/components/tabs-cn.md>
- 语义文档：<https://ant.design/components/tabs-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## tabs-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `tabs-cn`

选项卡切换组件。

## 何时使用

提供平级的区域将大块内容进行收纳和展现，保持界面整洁。

Ant Design 依次提供了三级选项卡，分别用于不同的场景。

- 卡片式的页签，提供可关闭的样式，常用于容器顶部。
- 既可用于容器顶部，也可用于容器内部，是最通用的 Tabs。
- [Radio.Button](/components/radio-cn/#radio-demo-radiobutton) 可作为更次级的页签来使用。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 激活项用主色文字和下划线，不要给 Tab 加背景填充。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Tabs } from 'antd';
import type { TabsProps } from 'antd';

const onChange = (key: string) => {
  console.log(key);
};

const items: TabsProps['items'] = [
  {
    key: '1',
    label: 'Tab 1',
    children: 'Content of Tab Pane 1',
  },
  {
    key: '2',
    label: 'Tab 2',
    children: 'Content of Tab Pane 2',
  },
  {
    key: '3',
    label: 'Tab 3',
    children: 'Content of Tab Pane 3',
  },
];

const App: React.FC = () => <Tabs defaultActiveKey="1" items={items} onChange={onChange} />;

export default App;
```

## 语义槽

### Tabs

- root（`semantic-mark-root`）: 根元素，包含标签页容器的基础样式、布局和方向控制
- item（`semantic-mark-item`）: Item 元素，包含相对定位、内边距、颜色、文本省略、圆角、过渡动画等标签项的样式和交互效果
- remove（`semantic-mark-remove`）: 删除按钮元素，包含可编辑标签页关闭按钮的尺寸、颜色、悬浮态和交互反馈等样式
- header（`semantic-mark-header`）: 头部元素，包含标签页头部导航的布局、背景、边框等样式
- indicator（`semantic-mark-indicator`）: 指示器元素，包含指示条的颜色、位置、尺寸、过渡动画等活跃状态指示样式
- body（`semantic-mark-body`）: 内容区域元素，包含标签页面板容器的布局、动画和尺寸控制
- content（`semantic-mark-content`）: 内容元素，包含单个标签页面板的布局、内边距等内容展示样式
- popup.root（`semantic-mark-popup-root`）: 弹出菜单元素，包含下拉菜单的绝对定位、层级、显示控制、最大高度、滚动等样式

```tsx
<Tabs
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    remove: "semantic-mark-remove",
    header: "semantic-mark-header",
    indicator: "semantic-mark-indicator",
    body: "semantic-mark-body",
    content: "semantic-mark-content",
    popup.root: "semantic-mark-popup-root"
  }}
/>
```
