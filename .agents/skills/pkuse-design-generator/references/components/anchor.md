<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Anchor 锚点

- 分组：导航
- 组件文档：<https://ant.design/components/anchor-cn.md>
- 语义文档：<https://ant.design/components/anchor-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## anchor-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `anchor-cn`

用于跳转到页面指定位置。

## 何时使用

需要展现当前页面上可供跳转的锚点链接，以及快速在锚点之间跳转。

> 开发者注意事项：
>
> 自 `4.24.0` 起，由于组件从 class 重构成 FC，之前一些获取 `ref` 并调用内部实例方法的写法都会失效

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Anchor, Col, Row } from 'antd';

const App: React.FC = () => (
  <Row>
    <Col span={16}>
      <div id="part-1" style={{ height: '100vh', background: 'rgba(255,0,0,0.02)' }} />
      <div id="part-2" style={{ height: '100vh', background: 'rgba(0,255,0,0.02)' }} />
      <div id="part-3" style={{ height: '100vh', background: 'rgba(0,0,255,0.02)' }} />
    </Col>
    <Col span={8}>
      <Anchor
        items={[
          {
            key: 'part-1',
            href: '#part-1',
            title: 'Part 1',
          },
          {
            key: 'part-2',
            href: '#part-2',
            title: 'Part 2',
          },
          {
            key: 'part-3',
            href: '#part-3',
            title: 'Part 3',
          },
        ]}
      />
    </Col>
  </Row>
);

export default App;
```

## 语义槽

### Anchor

- root（`semantic-mark-root`）: 根元素，包含布局定位、内边距、边距、背景色等基础样式
- item（`semantic-mark-item`）: 链接项元素，包含内边距、文字颜色、悬停状态、过渡动画等样式
- itemTitle（`semantic-mark-itemTitle`）: 标题文字元素，包含字体样式、颜色变化、文本装饰、过渡效果等样式
- indicator（`semantic-mark-indicator`）: 指示器元素，包含宽度、高度、背景色、位置变化、过渡动画等样式

```tsx
<Anchor
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    itemTitle: "semantic-mark-itemTitle",
    indicator: "semantic-mark-indicator"
  }}
/>
```
