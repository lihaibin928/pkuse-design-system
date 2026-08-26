<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Divider 分割线

- 分组：布局
- 组件文档：<https://ant.design/components/divider-cn.md>
- 语义文档：<https://ant.design/components/divider-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## divider-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `divider-cn`

区隔内容的分割线。

## 何时使用

- 对不同章节的文本段落进行分割。
- 对行内文字/链接进行分割，例如表格的操作列。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Divider } from 'antd';

const App: React.FC = () => (
  <>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nonne merninisti licere mihi ista
      probare, quae sunt a te dicta? Refert tamen, quo modo.
    </p>
    <Divider />
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nonne merninisti licere mihi ista
      probare, quae sunt a te dicta? Refert tamen, quo modo.
    </p>
    <Divider dashed />
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nonne merninisti licere mihi ista
      probare, quae sunt a te dicta? Refert tamen, quo modo.
    </p>
  </>
);

export default App;
```

## 语义槽

### Divider

- root（`semantic-mark-root`）: 根元素，包含边框顶部样式、分隔线样式等分割线容器的基础样式
- content（`semantic-mark-content`）: 内容元素，包含行内块显示、内边距等分割线文本内容的样式
- rail（`semantic-mark-rail`）: 背景条元素，包含边框顶部样式等分割线连接条的样式

```tsx
<Divider
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    content: "semantic-mark-content",
    rail: "semantic-mark-rail"
  }}
/>
```
