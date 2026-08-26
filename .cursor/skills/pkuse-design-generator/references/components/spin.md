<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Spin 加载中

- 分组：反馈
- 组件文档：<https://ant.design/components/spin-cn.md>
- 语义文档：<https://ant.design/components/spin-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## spin-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `spin-cn`

用于页面和区块的加载中状态。

## 何时使用

页面局部处于等待异步数据或正在渲染过程时，合适的加载动效会有效缓解用户的焦虑。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 加载用 Spin / Skeleton，不要换绿色骨架屏。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Spin } from 'antd';

const App: React.FC = () => <Spin />;

export default App;
```

## 语义槽

### Spin

- root（`semantic-mark-root`）: 根元素，设置绝对定位、显示控制、颜色、字体大小、文本对齐、垂直对齐、透明度和过渡动画(fullscreen 为 false 时才有效)
- section（`semantic-mark-section`）: 加载元素区域，设置相对定位、弹性盒子布局、对齐方式和颜色
- indicator（`semantic-mark-indicator`）: 指示器元素，设置宽度、高度、字体大小、行内块显示、过渡动画、变换原点、行高
- description（`semantic-mark-description`）: 描述元素，设置字体大小、行高
- container（`semantic-mark-container`）: 容器元素，放置被 Spin 包裹的子元素，设置透明度和过渡动画

```tsx
<Spin
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    section: "semantic-mark-section",
    indicator: "semantic-mark-indicator",
    description: "semantic-mark-description",
    container: "semantic-mark-container"
  }}
/>
```
