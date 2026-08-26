<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Statistic 统计数值

- 分组：数据展示
- 组件文档：<https://ant.design/components/statistic-cn.md>
- 语义文档：<https://ant.design/components/statistic-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## statistic-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `statistic-cn`

展示统计数值。

## 何时使用

- 当需要突出某个或某组数字时。
- 当需要展示带描述的统计类数据时使用。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Button, Col, Row, Statistic } from 'antd';

const App: React.FC = () => (
  <Row gutter={16}>
    <Col span={12}>
      <Statistic title="Active Users" value={112893} />
    </Col>
    <Col span={12}>
      <Statistic title="Account Balance (CNY)" value={112893} precision={2} />
      <Button style={{ marginTop: 16 }} type="primary">
        Recharge
      </Button>
    </Col>
    <Col span={12}>
      <Statistic title="Active Users" value={112893} loading />
    </Col>
  </Row>
);

export default App;
```

## 语义槽

### Statistic

- root（`semantic-mark-root`）: 根元素，包含统计数值组件的重置样式和整体容器样式
- header（`semantic-mark-header`）: 头部元素，包含下内边距和标题区域的布局样式
- title（`semantic-mark-title`）: 标题元素，包含文字颜色、字体大小等标题文字的显示样式
- content（`semantic-mark-content`）: 内容元素，包含前缀、数值、后缀的布局和对齐等内容区域样式
- value（`semantic-mark-value`）: 数值元素，包含文字颜色、字体大小、字体族等统计数值的展示样式
- prefix（`semantic-mark-prefix`）: 前缀元素，包含行内块显示、右外边距等前缀内容的布局样式
- suffix（`semantic-mark-suffix`）: 后缀元素，包含行内块显示、左外边距等后缀内容的布局样式

```tsx
<Statistic
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    content: "semantic-mark-content",
    value: "semantic-mark-value",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix"
  }}
/>
```
