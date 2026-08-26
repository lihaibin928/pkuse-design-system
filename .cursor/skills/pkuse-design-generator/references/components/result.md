<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Result 结果

- 分组：反馈
- 组件文档：<https://ant.design/components/result-cn.md>
- 语义文档：<https://ant.design/components/result-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## result-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `result-cn`

用于反馈一系列操作任务的处理结果。

## 何时使用

当有重要操作需告知用户处理结果，且反馈内容较为复杂时使用。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 401 与 403、404、5xx 使用不同 Result，不要收成同一条文案。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Button, Result } from 'antd';

const App: React.FC = () => (
  <Result
    status="success"
    title="Successfully Purchased Cloud Server ECS!"
    subTitle="Order number: 2017182818828182881 Cloud server configuration takes 1-5 minutes, please wait."
    extra={[
      <Button type="primary" key="console">
        Go Console
      </Button>,
      <Button key="buy">Buy Again</Button>,
    ]}
  />
);

export default App;
```

## 语义槽

### Result

- root（`semantic-mark-root`）: 根元素，包含文本对齐、布局样式等基础容器样式
- title（`semantic-mark-title`）: 标题元素，包含字体大小、文字颜色、行高、对齐方式等文字样式
- subTitle（`semantic-mark-subTitle`）: 副标题元素，包含字体大小、文字颜色、行高等文字样式
- body（`semantic-mark-body`）: 内容元素，包含外边距、内边距、背景色等内容区域样式
- extra（`semantic-mark-extra`）: 操作区域元素，包含外边距、文本对齐、内部元素间距等布局样式
- icon（`semantic-mark-icon`）: 图标元素，包含外边距、文本对齐、字体大小、状态颜色等图标样式

```tsx
<Result
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    title: "semantic-mark-title",
    subTitle: "semantic-mark-subTitle",
    body: "semantic-mark-body",
    extra: "semantic-mark-extra",
    icon: "semantic-mark-icon"
  }}
/>
```
