<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Space 间距

- 分组：布局
- 组件文档：<https://ant.design/components/space-cn.md>
- 语义文档：<https://ant.design/components/space-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## space-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `space-cn`

设置组件之间的间距。

## 何时使用

避免组件紧贴在一起，拉开统一的空间。

- 适合行内元素的水平间距。
- 可以设置各种水平对齐方式。
- 需要表单组件之间紧凑连接且合并边框时，使用 Space.Compact（自 `antd@4.24.0` 版本开始提供该组件）。

### 与 Flex 组件的区别 {#difference-with-flex-component}

- Space 为内联元素提供间距，其本身会为每一个子元素添加包裹元素用于内联对齐。适用于行、列中多个子元素的等距排列。
- Flex 为块级元素提供间距，其本身不会添加包裹元素。适用于垂直或水平方向上的子元素布局，并提供了更多的灵活性和控制能力。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Popconfirm, Space, Upload } from 'antd';

const App: React.FC = () => (
  <Space>
    Space
    <Button type="primary">Button</Button>
    <Upload>
      <Button icon={<UploadOutlined />}>Click to Upload</Button>
    </Upload>
    <Popconfirm title="Are you sure delete this task?" okText="Yes" cancelText="No">
      <Button>Confirm</Button>
    </Popconfirm>
  </Space>
);

export default App;
```

## 语义槽

### Space

- root（`semantic-mark-root`）: 根元素，包含 flex 布局、间隙设置、对齐方式、换行等间距容器的基础样式
- item（`semantic-mark-item`）: 包裹的子组件，包含间距项的布局和样式，为每个子元素提供包装用于内联对齐
- separator（`semantic-mark-separator`）: 分隔符，包含分隔元素的样式

```tsx
<Space
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    separator: "semantic-mark-separator"
  }}
/>
```
