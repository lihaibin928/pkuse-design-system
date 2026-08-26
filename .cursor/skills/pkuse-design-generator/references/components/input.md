<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Input 输入框

- 分组：数据录入
- 组件文档：<https://ant.design/components/input-cn.md>
- 语义文档：<https://ant.design/components/input-cn/semantic_input.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## input-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `input-cn`

通过鼠标或键盘输入内容，是最基础的表单域的包装。

## 何时使用

- 需要用户输入表单域内容时。
- 提供组合型输入框，带搜索的输入框，还可以进行大小选择。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 占位符用禁用文字色；焦点态走主色描边。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Input } from 'antd';

const App: React.FC = () => <Input placeholder="Basic usage" />;

export default App;
```

## 语义槽

### Input.Input

- root（`semantic-mark-root`）: 根元素，包含相对定位、行内块布局、宽度、最小宽度、内边距、颜色、字体、行高、圆角、过渡动画等输入框容器的基础样式
- input（`semantic-mark-input`）: 输入框元素，包含输入框的核心交互样式和文本输入相关的样式
- prefix（`semantic-mark-prefix`）: 前缀的包裹元素，包含前缀内容的布局和样式
- suffix（`semantic-mark-suffix`）: 后缀的包裹元素，包含后缀内容的布局和样式
- clear（`semantic-mark-clear`）: 清除按钮元素，包含清除内容按钮的布局、显隐和交互样式
- count（`semantic-mark-count`）: 文字计数元素，包含字符计数显示的字体和颜色样式

```tsx
<Input.Input
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    input: "semantic-mark-input",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix",
    clear: "semantic-mark-clear",
    count: "semantic-mark-count"
  }}
/>
```

### Input.Otp

- root（`semantic-mark-root`）: 根元素，设置行内flex布局、对齐方式、列间距和包装样式
- input（`semantic-mark-input`）: 输入框元素，设置文本居中、内边距和数字输入样式
- separator（`semantic-mark-separator`）: 分隔符元素，设置OTP输入框之间的分隔符显示样式

```tsx
<Input.Otp
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    input: "semantic-mark-input",
    separator: "semantic-mark-separator"
  }}
/>
```

### Input.Password

- root（`semantic-mark-root`）: 根元素
- input（`semantic-mark-input`）: 输入框元素
- prefix（`semantic-mark-prefix`）: 前缀的包裹元素
- suffix（`semantic-mark-suffix`）: 后缀的包裹元素
- clear（`semantic-mark-clear`）: 清除按钮元素
- count（`semantic-mark-count`）: 文字计数元素

```tsx
<Input.Password
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    input: "semantic-mark-input",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix",
    clear: "semantic-mark-clear",
    count: "semantic-mark-count"
  }}
/>
```

### Input.Search

- root（`semantic-mark-root`）: 根元素
- input（`semantic-mark-input`）: 输入框元素
- prefix（`semantic-mark-prefix`）: 前缀的包裹元素
- suffix（`semantic-mark-suffix`）: 后缀的包裹元素
- clear（`semantic-mark-clear`）: 清除按钮元素
- count（`semantic-mark-count`）: 文字计数元素
- button.root（`semantic-mark-button-root`）: 按钮根元素
- button.icon（`semantic-mark-button-icon`）: 按钮图标元素
- button.content（`semantic-mark-button-content`）: 按钮内容元素

```tsx
<Input.Search
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    input: "semantic-mark-input",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix",
    clear: "semantic-mark-clear",
    count: "semantic-mark-count",
    button.root: "semantic-mark-button-root",
    button.icon: "semantic-mark-button-icon",
    button.content: "semantic-mark-button-content"
  }}
/>
```

### Input.Textarea

- root（`semantic-mark-root`）: 根元素，设置文本域包装器的样式、边框、圆角、过渡动画和状态控制
- textarea（`semantic-mark-textarea`）: 文本域元素，设置字体、行高、内边距、颜色、背景、边框、文本输入和多行文本展示样式
- clear（`semantic-mark-clear`）: 清除按钮元素，包含清除内容按钮的布局、显隐和交互样式
- count（`semantic-mark-count`）: 文字计数元素，设置字符计数显示的位置、字体、颜色和数值统计样式

```tsx
<Input.Textarea
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    textarea: "semantic-mark-textarea",
    clear: "semantic-mark-clear",
    count: "semantic-mark-count"
  }}
/>
```
