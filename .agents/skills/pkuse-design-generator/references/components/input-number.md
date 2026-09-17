<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# InputNumber 数字输入框

- 分组：数据录入
- 组件文档：<https://ant.design/components/input-number-cn.md>
- 语义文档：<https://ant.design/components/input-number-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## input-number-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `input-number-cn`

通过鼠标或键盘，输入范围内的数值。

## 何时使用

当需要获取标准数值时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { InputNumberProps } from 'antd';
import { InputNumber } from 'antd';

const onChange: InputNumberProps['onChange'] = (value) => {
  console.log('changed', value);
};

const App: React.FC = () => <InputNumber min={1} max={10} defaultValue={3} onChange={onChange} />;

export default App;
```

## 语义槽

### InputNumber

- root（`semantic-mark-root`）: 根元素，设置行内块布局、宽度、边框圆角和重置样式
- input（`semantic-mark-input`）: 输入框元素，设置字体、行高、文本输入和交互样式
- prefix（`semantic-mark-prefix`）: 前缀的包裹元素，设置flex布局、对齐方式和右边距样式
- suffix（`semantic-mark-suffix`）: 后缀的包裹元素，设置flex布局、边距和过渡动画样式
- action（`semantic-mark-action`）: 单个操作按钮元素，设置按钮的样式、悬浮效果和点击交互
- actions（`semantic-mark-actions`）: 操作元素，设置绝对定位、宽度、flex布局和数值调节按钮样式

```tsx
<InputNumber
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    input: "semantic-mark-input",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix",
    action: "semantic-mark-action",
    actions: "semantic-mark-actions"
  }}
/>
```
