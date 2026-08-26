<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Checkbox 多选框

- 分组：数据录入
- 组件文档：<https://ant.design/components/checkbox-cn.md>
- 语义文档：<https://ant.design/components/checkbox-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## checkbox-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `checkbox-cn`

收集用户的多项选择。

## 何时使用

- 在一组可选项中进行多项选择时；
- 单独使用可以表示两种状态之间的切换，和 `switch` 类似。区别在于切换 `switch` 会直接触发状态改变，而 `checkbox` 一般用于状态标记，需要和提交操作配合。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Checkbox } from 'antd';
import type { CheckboxProps } from 'antd';

const onChange: CheckboxProps['onChange'] = (e) => {
  console.log(`checked = ${e.target.checked}`);
};

const App: React.FC = () => <Checkbox onChange={onChange}>Checkbox</Checkbox>;

export default App;
```

## 语义槽

### Checkbox

- root（`semantic-mark-root`）: 根元素，包含行内 flex 布局、基线对齐、光标样式、重置样式等复选框容器的基础样式
- icon（`semantic-mark-icon`）: 选中框元素，包含尺寸、方向、背景色、边框、圆角、过渡动画，以及选中状态的勾选标记样式
- label（`semantic-mark-label`）: 文本元素，包含文本的内边距和与复选框的间距样式

```tsx
<Checkbox
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    icon: "semantic-mark-icon",
    label: "semantic-mark-label"
  }}
/>
```
