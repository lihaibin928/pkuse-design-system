<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Timeline 时间轴

- 分组：数据展示
- 组件文档：<https://ant.design/components/timeline-cn.md>
- 语义文档：<https://ant.design/components/timeline-cn/semantic_items.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## timeline-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `timeline-cn`

垂直展示的时间流信息。

## 何时使用

- 当有一系列信息需按时间排列时，可正序和倒序。
- 需要有一条时间轴进行视觉上的串联时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Timeline } from 'antd';

const App: React.FC = () => (
  <Timeline
    items={[
      {
        content: 'Create a services site 2015-09-01',
      },
      {
        content: 'Solve initial network problems 2015-09-01',
      },
      {
        content: 'Technical testing 2015-09-01',
      },
      {
        content: 'Network problems being solved 2015-09-01',
      },
    ]}
  />
);

export default App;
```

## 语义槽

### Timeline.Items

- root（`semantic-mark-root`）: 根元素
- wrapper（`semantic-mark-wrapper`）: 节点内裹元素
- icon（`semantic-mark-icon`）: 节点图标元素
- header（`semantic-mark-header`）: 节点头部元素
- title（`semantic-mark-title`）: 节点标题元素
- section（`semantic-mark-section`）: 节点区域元素
- content（`semantic-mark-content`）: 节点内容元素
- rail（`semantic-mark-rail`）: 节点连接线元素

```tsx
<Timeline.Items
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    wrapper: "semantic-mark-wrapper",
    icon: "semantic-mark-icon",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    section: "semantic-mark-section",
    content: "semantic-mark-content",
    rail: "semantic-mark-rail"
  }}
/>
```

### Timeline

- root（`semantic-mark-root`）: 根元素，设置时间轴容器的列表样式重置、垂直布局、点状图标、轮廓样式、交替布局等基础容器样式
- item（`semantic-mark-item`）: 节点元素，设置单个时间节点的相对定位、外边距、内边距、字体大小、完成状态、颜色主题、布局方向等节点基础样式
- itemWrapper（`semantic-mark-itemWrapper`）: 节点包装元素，设置时间节点内容的包装容器样式
- itemIcon（`semantic-mark-itemIcon`）: 节点图标元素，设置节点头部图标的绝对定位、宽高尺寸、背景色、边框、圆角、波纹动画等图标样式
- itemHeader（`semantic-mark-itemHeader`）: 节点头部元素，设置包含标题和连接线的头部区域布局、对齐方式、文本方向等样式
- itemTitle（`semantic-mark-itemTitle`）: 节点标题元素，设置节点标题文字的字体大小、行高、颜色等文本样式
- itemSection（`semantic-mark-itemSection`）: 节点区域元素，设置包含头部和内容的区域容器的Flex布局、换行、间距等布局样式
- itemContent（`semantic-mark-itemContent`）: 节点内容元素，设置节点详细内容的相对定位、顶部偏移、左侧外边距、文字颜色、词汇换行等内容样式
- itemRail（`semantic-mark-itemRail`）: 节点连接线元素，设置连接时间节点的轨道线条的绝对定位、顶部偏移、左侧偏移、高度、边框颜色、宽度、样式等连接线样式

```tsx
<Timeline
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    itemWrapper: "semantic-mark-itemWrapper",
    itemIcon: "semantic-mark-itemIcon",
    itemHeader: "semantic-mark-itemHeader",
    itemTitle: "semantic-mark-itemTitle",
    itemSection: "semantic-mark-itemSection",
    itemContent: "semantic-mark-itemContent",
    itemRail: "semantic-mark-itemRail"
  }}
/>
```
