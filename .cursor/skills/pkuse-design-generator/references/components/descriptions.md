<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Descriptions 描述列表

- 分组：数据展示
- 组件文档：<https://ant.design/components/descriptions-cn.md>
- 语义文档：<https://ant.design/components/descriptions-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## descriptions-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `descriptions-cn`

展示多个只读字段的组合。

## 何时使用

常见于详情页的信息展示。

```tsx | pure
// >= 5.8.0 可用，推荐的写法 ✅

const items: DescriptionsProps['items'] = [
  {
    key: '1',
    label: 'UserName',
    children: <p>Zhou Maomao</p>,
  },
  {
    key: '2',
    label: 'Telephone',
    children: <p>1810000000</p>,
  },
  {
    key: '3',
    label: 'Live',
    children: <p>Hangzhou, Zhejiang</p>,
  },
  {
    key: '4',
    label: 'Remark',
    children: <p>empty</p>,
  },
  {
    key: '5',
    label: 'Address',
    children: <p>No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China</p>,
  },
];

<Descriptions title="User Info" items={items} />;

// <5.8.0 可用，>=5.8.0 时不推荐 🙅🏻‍♀️

<Descriptions title="User Info">
  <Descriptions.Item label="UserName">Zhou Maomao</Descriptions.Item>
  <Descriptions.Item label="Telephone">1810000000</Descriptions.Item>
  <Descriptions.Item label="Live">Hangzhou, Zhejiang</Descriptions.Item>
  <Descriptions.Item label="Remark">empty</Descriptions.Item>
  <Descriptions.Item label="Address">
    No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China
  </Descriptions.Item>
</Descriptions>;
```

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Descriptions } from 'antd';
import type { DescriptionsProps } from 'antd';

const items: DescriptionsProps['items'] = [
  {
    key: '1',
    label: 'UserName',
    children: 'Zhou Maomao',
  },
  {
    key: '2',
    label: 'Telephone',
    children: '1810000000',
  },
  {
    key: '3',
    label: 'Live',
    children: 'Hangzhou, Zhejiang',
  },
  {
    key: '4',
    label: 'Remark',
    children: 'empty',
  },
  {
    key: '5',
    label: 'Address',
    children: 'No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China',
  },
];

const App: React.FC = () => <Descriptions title="User Info" items={items} />;

export default App;
```

## 语义槽

### Descriptions

- root（`semantic-mark-root`）: 根元素，包含描述列表容器的基础样式、重置样式、边框样式、布局方向等整体样式
- header（`semantic-mark-header`）: 头部元素，包含flex布局、对齐方式、下边距等头部区域的布局和样式控制
- title（`semantic-mark-title`）: 标题元素，包含文本省略、flex占比、颜色、字体权重、字体大小、行高等标题文字样式
- extra（`semantic-mark-extra`）: 额外内容元素，包含左边距、颜色、字体大小等额外操作区域的样式
- label（`semantic-mark-label`）: 标签元素，包含颜色、字体权重、字体大小、行高、文本对齐、冒号样式等标签文字的样式
- content（`semantic-mark-content`）: 内容元素，包含表格单元格布局、颜色、字体大小、行高、文字换行等内容展示样式

```tsx
<Descriptions
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    extra: "semantic-mark-extra",
    label: "semantic-mark-label",
    content: "semantic-mark-content"
  }}
/>
```
