<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Skeleton 骨架屏

- 分组：反馈
- 组件文档：<https://ant.design/components/skeleton-cn.md>
- 语义文档：<https://ant.design/components/skeleton-cn/semantic_element.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## skeleton-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `skeleton-cn`

在需要等待加载内容的位置提供一个占位图形组合。

## 何时使用

- 网络较慢，需要长时间等待加载处理的情况下。
- 图文信息内容较多的列表/卡片中。
- 只在第一次加载数据的时候使用。
- 可以被 Spin 完全代替，但是在可用的场景下可以比 Spin 提供更好的视觉效果和用户体验。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Skeleton } from 'antd';

const App: React.FC = () => <Skeleton />;

export default App;
```

## 语义槽

### Skeleton.Element

- root（`semantic-mark-root`）: 根元素
- content（`semantic-mark-content`）: 内容元素

```tsx
<Skeleton.Element
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    content: "semantic-mark-content"
  }}
/>
```

### Skeleton

- root（`semantic-mark-root`）: 根元素，包含表格显示、宽度、动画效果、圆角等骨架屏容器的基础样式
- header（`semantic-mark-header`）: 头部元素，包含表格单元格、内边距、垂直对齐等头像占位区域的布局样式
- section（`semantic-mark-section`）: 区块元素，包含骨架屏内容区域的布局样式
- avatar（`semantic-mark-avatar`）: 头像元素，包含行内块显示、垂直对齐、背景色、尺寸、圆角等头像占位的样式
- title（`semantic-mark-title`）: 标题元素，包含宽度、高度、背景色、圆角等标题占位的样式
- paragraph（`semantic-mark-paragraph`）: 段落元素，包含内边距、列表项样式、背景色、圆角等段落占位的样式

```tsx
<Skeleton
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    section: "semantic-mark-section",
    avatar: "semantic-mark-avatar",
    title: "semantic-mark-title",
    paragraph: "semantic-mark-paragraph"
  }}
/>
```
