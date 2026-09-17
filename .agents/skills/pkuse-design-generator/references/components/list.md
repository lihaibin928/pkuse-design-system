<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# List 列表

- 分组：数据展示
- 组件文档：<https://ant.design/components/list-cn.md>
- 语义文档：<https://ant.design/components/list-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## list-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `list-cn`

最基础的列表展示，可承载文字、列表、图片、段落。

## 何时使用

最基础的列表展示，可承载文字、列表、图片、段落，常用于后台数据展示页面。

:::warning{title=废弃提示}
List 组件已经进入废弃阶段，将于下个 major 版本移除，请改用 [Listy](/components/listy-cn)，迁移方式参见 [如何从 List 迁移？](#faq-migrate-from-list)。
:::

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Divider, List, Typography } from 'antd';

const data = [
  'Racing car sprays burning fuel into crowd.',
  'Japanese princess to wed commoner.',
  'Australian walks 100km after outback crash.',
  'Man charged over missing wedding girl.',
  'Los Angeles battles huge wildfires.',
];

const App: React.FC = () => (
  <>
    <Divider titlePlacement="start">Default Size</Divider>
    <List
      header={<div>Header</div>}
      footer={<div>Footer</div>}
      bordered
      dataSource={data}
      renderItem={(item) => (
        <List.Item>
          <Typography.Text mark>[ITEM]</Typography.Text> {item}
        </List.Item>
      )}
    />
    <Divider titlePlacement="start">Small Size</Divider>
    <List
      size="small"
      header={<div>Header</div>}
      footer={<div>Footer</div>}
      bordered
      dataSource={data}
      renderItem={(item) => <List.Item>{item}</List.Item>}
    />
    <Divider titlePlacement="start">Large Size</Divider>
    <List
      size="large"
      header={<div>Header</div>}
      footer={<div>Footer</div>}
      bordered
      dataSource={data}
      renderItem={(item) => <List.Item>{item}</List.Item>}
    />
  </>
);

export default App;
```

## 语义槽

### List

- extra（`semantic-mark-extra`）: 设置额外内容
- actions（`semantic-mark-actions`）: 设置列表操作组

```tsx
<List
  {...otherProps}
  classNames={{
    extra: "semantic-mark-extra",
    actions: "semantic-mark-actions"
  }}
/>
```
