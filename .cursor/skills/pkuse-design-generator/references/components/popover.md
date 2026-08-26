<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Popover 气泡卡片

- 分组：数据展示
- 组件文档：<https://ant.design/components/popover-cn.md>
- 语义文档：<https://ant.design/components/popover-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## popover-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `popover-cn`

点击/鼠标移入元素，弹出气泡式的卡片浮层。

## 何时使用

当目标元素有进一步的描述和相关操作时，可以收纳到卡片中，根据用户的操作行为进行展现。

和 `Tooltip` 的区别是，用户可以对浮层上的元素进行操作，因此它可以承载更复杂的内容，比如链接或按钮等。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Button, Popover } from 'antd';

const content = (
  <div>
    <p style={{ margin: 0 }}>Content</p>
    <p style={{ margin: 0 }}>Content</p>
  </div>
);

const App: React.FC = () => (
  <Popover content={content} title="Title">
    <Button type="primary">Hover me</Button>
  </Popover>
);

export default App;
```

## 语义槽

### Popover

- root（`semantic-mark-root`）: 根元素，设置绝对定位、层级、变换原点、箭头指向和弹层容器样式
- container（`semantic-mark-container`）: 容器元素，设置背景色、内边距、圆角、阴影、边框和内容展示样式
- arrow（`semantic-mark-arrow`）: 箭头元素，设置宽高、位置、颜色和边框样式
- title（`semantic-mark-title`）: 标题元素，设置标题文本样式和间距
- content（`semantic-mark-content`）: 内容元素，设置内容文本样式和布局

```tsx
<Popover
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    container: "semantic-mark-container",
    arrow: "semantic-mark-arrow",
    title: "semantic-mark-title",
    content: "semantic-mark-content"
  }}
/>
```
