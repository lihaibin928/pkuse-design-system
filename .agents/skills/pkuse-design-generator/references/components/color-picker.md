<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# ColorPicker 颜色选择器

- 分组：数据录入
- 组件文档：<https://ant.design/components/color-picker-cn.md>
- 语义文档：<https://ant.design/components/color-picker-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## color-picker-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `color-picker-cn`

用于选择颜色。

## 何时使用

当用户需要自定义颜色选择的时候使用。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { ColorPicker } from 'antd';

const Demo = () => <ColorPicker defaultValue="#1677ff" />;

export default Demo;
```

## 语义槽

### ColorPicker

- root（`semantic-mark-root`）: 触发器容器，包含边框样式、过渡动画、尺寸控制等样式，显示颜色块和文本内容
- body（`semantic-mark-body`）: 色块容器，包含底色、边框等样式
- content（`semantic-mark-content`）: 色块颜色元素，包含实际选择的颜色样式
- description（`semantic-mark-description`）: 描述文本内容，包含字体样式、颜色等样式
- popup.root（`semantic-mark-popup-root`）: 弹出面板根容器，包含背景色、阴影效果、色彩选择面板、滑块控制和预设颜色等样式

```tsx
<ColorPicker
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    body: "semantic-mark-body",
    content: "semantic-mark-content",
    description: "semantic-mark-description",
    popup.root: "semantic-mark-popup-root"
  }}
/>
```
