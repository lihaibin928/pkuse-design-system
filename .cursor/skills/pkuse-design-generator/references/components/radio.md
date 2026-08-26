<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Radio 单选框

- 分组：数据录入
- 组件文档：<https://ant.design/components/radio-cn.md>
- 语义文档：<https://ant.design/components/radio-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## radio-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `radio-cn`

用于在多个备选项中选中单个状态。

## 何时使用

- 用于在多个备选项中选中单个状态。
- 和 Select 的区别是，Radio 所有选项默认可见，方便用户在比较中选择，因此选项不宜过多。

```tsx
// 使用 Radio.Group 组件时，推荐的写法 ✅
return (
  <Radio.Group
    value={value}
    options={[
      { value: 1, label: 'A' },
      { value: 2, label: 'B' },
      { value: 3, label: 'C' },
    ]}
  />
);

// 不推荐的写法 🙅🏻‍♀️
return (
  <Radio.Group value={value}>
    <Radio value={1}>A</Radio>
    <Radio value={2}>B</Radio>
    <Radio value={3}>C</Radio>
  </Radio.Group>
);
```

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Radio } from 'antd';

const App: React.FC = () => <Radio>Radio</Radio>;

export default App;
```

## 语义槽

### Radio

- root（`semantic-mark-root`）: 根元素，包含布局样式、鼠标样式、禁用状态文字颜色等基础容器样式
- icon（`semantic-mark-icon`）: 选中框元素，包含圆角样式、过渡动画、边框样式、悬停状态、焦点状态等交互样式
- label（`semantic-mark-label`）: 文本元素，包含内边距、文字颜色、禁用状态、对齐方式等文本样式

```tsx
<Radio
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    icon: "semantic-mark-icon",
    label: "semantic-mark-label"
  }}
/>
```
