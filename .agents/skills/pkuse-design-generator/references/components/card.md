<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Card 卡片

- 分组：数据展示
- 组件文档：<https://ant.design/components/card-cn.md>
- 语义文档：<https://ant.design/components/card-cn/semantic_meta.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## card-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `card-cn`

通用卡片容器。

## 何时使用

最基础的卡片容器，可承载文字、列表、图片、段落，常用于后台概览页面。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Card, Space } from 'antd';

const App: React.FC = () => (
  <Space vertical size={16}>
    <Card title="Default size card" extra={<a href="#">More</a>} style={{ width: 300 }}>
      <p>Card content</p>
      <p>Card content</p>
      <p>Card content</p>
    </Card>
    <Card size="small" title="Small size card" extra={<a href="#">More</a>} style={{ width: 300 }}>
      <p>Card content</p>
      <p>Card content</p>
      <p>Card content</p>
    </Card>
  </Space>
);

export default App;
```

## 语义槽

### Card.Meta

- root（`semantic-mark-root`）: 设置元信息根元素
- section（`semantic-mark-section`）: 设置元信息内容元素
- avatar（`semantic-mark-avatar`）: 设置元信息图标
- title（`semantic-mark-title`）: 设置元信息标题
- description（`semantic-mark-description`）: 设置元信息描述

```tsx
<Card.Meta
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    section: "semantic-mark-section",
    avatar: "semantic-mark-avatar",
    title: "semantic-mark-title",
    description: "semantic-mark-description"
  }}
/>
```

### Card

- root（`semantic-mark-root`）: 卡片根元素，包含位置定位、背景色、边框、圆角、阴影、内边距等卡片容器的基础样式
- header（`semantic-mark-header`）: 卡片头部区域，包含 flex 布局、最小高度、内边距、文字颜色、字体权重、字体大小、背景色、下边框、顶部圆角等样式
- body（`semantic-mark-body`）: 卡片内容区域，包含内边距、字体大小等内容展示的基础样式
- extra（`semantic-mark-extra`）: 卡片右上角的操作区域，包含额外内容的文字颜色和布局样式
- title（`semantic-mark-title`）: 卡片标题，包含行内块布局、flex 占比、文本省略等标题显示样式
- actions（`semantic-mark-actions`）: 卡片底部操作组，包含 flex 布局、列表样式重置、背景色、上边框、底部圆角等操作按钮容器样式
- cover（`semantic-mark-cover`）: 标题封面，包含封面图片的显示和布局样式

```tsx
<Card
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    body: "semantic-mark-body",
    extra: "semantic-mark-extra",
    title: "semantic-mark-title",
    actions: "semantic-mark-actions",
    cover: "semantic-mark-cover"
  }}
/>
```
