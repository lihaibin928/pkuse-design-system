<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Segmented 分段控制器

- 分组：数据展示
- 组件文档：<https://ant.design/components/segmented-cn.md>
- 语义文档：<https://ant.design/components/segmented-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## segmented-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `segmented-cn`

用于展示多个选项并允许用户选择其中单个选项。

## 何时使用

- 用于展示多个选项并允许用户选择其中单个选项；
- 当切换选中选项时，关联区域的内容会发生变化。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Segmented } from 'antd';

const Demo: React.FC = () => (
  <Segmented<string>
    options={['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']}
    onChange={(value) => {
      console.log(value); // string
    }}
  />
);

export default Demo;
```

## 语义槽

### Segmented

- root（`semantic-mark-root`）: 根元素，设置行内块布局、内边距、背景色、圆角、过渡动画和容器样式
- item（`semantic-mark-item`）: 选项元素，设置相对定位、文本对齐、光标样式、过渡动画、选中态背景色和悬停态样式
- icon（`semantic-mark-icon`）: 图标元素，设置图标的尺寸、颜色和与文本的间距样式
- label（`semantic-mark-label`）: 标签内容元素，设置最小高度、行高、内边距、文本省略和内容布局样式

```tsx
<Segmented
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    icon: "semantic-mark-icon",
    label: "semantic-mark-label"
  }}
/>
```
