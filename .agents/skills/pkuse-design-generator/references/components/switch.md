<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Switch 开关

- 分组：数据录入
- 组件文档：<https://ant.design/components/switch-cn.md>
- 语义文档：<https://ant.design/components/switch-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## switch-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `switch-cn`

使用开关切换两种状态之间。

## 何时使用

- 需要表示开关状态/两种状态之间的切换时；
- 和 `checkbox` 的区别是，切换 `switch` 会直接触发状态改变，而 `checkbox` 一般用于状态标记，需要和提交操作配合。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Switch } from 'antd';

const onChange = (checked: boolean) => {
  console.log(`switch to ${checked}`);
};

const App: React.FC = () => <Switch defaultChecked onChange={onChange} />;

export default App;
```

## 语义槽

### Switch

- root（`semantic-mark-root`）: 根元素，包含最小宽度、高度、行高、垂直对齐、背景色、边框、圆角、光标样式、过渡动画、用户选择等开关容器的基础样式
- content（`semantic-mark-content`）: 内容元素，包含块级显示、溢出隐藏、圆角、高度、内边距、过渡动画等开关内容区域的布局和样式
- indicator（`semantic-mark-indicator`）: 指示器元素,包含绝对定位、宽度、高度、背景色、圆角、阴影、过渡动画等开关把手的样式和交互效果

```tsx
<Switch
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    content: "semantic-mark-content",
    indicator: "semantic-mark-indicator"
  }}
/>
```
