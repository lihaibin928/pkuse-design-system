<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Steps 步骤条

- 分组：导航
- 组件文档：<https://ant.design/components/steps-cn.md>
- 语义文档：<https://ant.design/components/steps-cn/semantic_items.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## steps-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `steps-cn`

引导用户按照流程完成任务的导航条。

## 何时使用

当任务复杂或者存在先后关系时，将其分解成一系列步骤，从而简化任务。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Flex, Steps } from 'antd';

const content = 'This is a content.';
const items = [
  {
    title: 'Finished',
    content,
  },
  {
    title: 'In Progress',
    content,
    subTitle: 'Left 00:00:08',
  },
  {
    title: 'Waiting',
    content,
  },
];

const App: React.FC = () => (
  <Flex vertical gap="large">
    <Steps current={1} items={items} />
    <Steps current={1} items={items} variant="outlined" />
    <Steps current={1} items={items} size="small" />
    <Steps current={1} items={items} size="small" variant="outlined" />
  </Flex>
);

export default App;
```

## 语义槽

### Steps.Items

- root（`semantic-mark-root`）: 根元素
- wrapper（`semantic-mark-wrapper`）: 步骤项内裹元素
- icon（`semantic-mark-icon`）: 步骤项图标元素
- header（`semantic-mark-header`）: 步骤项头部元素
- title（`semantic-mark-title`）: 步骤项标题元素
- subtitle（`semantic-mark-subtitle`）: 步骤项副标题元素
- section（`semantic-mark-section`）: 步骤项区域元素
- content（`semantic-mark-content`）: 步骤项内容元素
- rail（`semantic-mark-rail`）: 步骤项连接线元素

```tsx
<Steps.Items
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    wrapper: "semantic-mark-wrapper",
    icon: "semantic-mark-icon",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    subtitle: "semantic-mark-subtitle",
    section: "semantic-mark-section",
    content: "semantic-mark-content",
    rail: "semantic-mark-rail"
  }}
/>
```

### Steps

- root（`semantic-mark-root`）: 根元素，包含 flex 布局、禁止换行、对齐方式、CSS 变量等步骤条容器的基础样式
- item（`semantic-mark-item`）: 步骤项元素，包含 flex 布局、相对定位等单个步骤项的基础容器样式
- itemWrapper（`semantic-mark-itemWrapper`）: 步骤项内裹元素，包含 flex 布局、禁止换行、顶部内边距等步骤项内容的包装样式
- itemIcon（`semantic-mark-itemIcon`）: 步骤项图标元素，包含图标的尺寸、定位、字体大小等图标显示相关样式
- itemHeader（`semantic-mark-itemHeader`）: 步骤项头部元素，包含 flex 布局、禁止换行、对齐方式等头部区域的布局样式
- itemTitle（`semantic-mark-itemTitle`）: 步骤项标题元素，包含颜色、字体大小、行高、文字换行、过渡动画等标题文字样式
- itemSubtitle（`semantic-mark-itemSubtitle`）: 步骤项副标题元素，包含颜色、字体权重、字体大小、行高、外边距、文字换行等副标题样式
- itemSection（`semantic-mark-itemSection`）: 步骤项区域元素，包含步骤项内容区域的布局和样式
- itemContent（`semantic-mark-itemContent`）: 步骤项内容元素，包含颜色、字体大小、行高、文字换行、过渡动画等内容文字样式
- itemRail（`semantic-mark-itemRail`）: 步骤项连接线元素，包含边框样式、边框宽度、过渡动画等连接线的样式

```tsx
<Steps
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    itemWrapper: "semantic-mark-itemWrapper",
    itemIcon: "semantic-mark-itemIcon",
    itemHeader: "semantic-mark-itemHeader",
    itemTitle: "semantic-mark-itemTitle",
    itemSubtitle: "semantic-mark-itemSubtitle",
    itemSection: "semantic-mark-itemSection",
    itemContent: "semantic-mark-itemContent",
    itemRail: "semantic-mark-itemRail"
  }}
/>
```
