<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# DatePicker 日期选择框

- 分组：数据录入
- 组件文档：<https://ant.design/components/date-picker-cn.md>
- 语义文档：<https://ant.design/components/date-picker-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## date-picker-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `date-picker-cn`

输入或选择日期的控件。

## 何时使用

当用户需要输入一个日期，可以点击标准输入框，弹出日期面板进行选择。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { DatePickerProps } from 'antd';
import { DatePicker, Flex } from 'antd';

const onChange: DatePickerProps['onChange'] = (date, dateString) => {
  console.log(date, dateString);
};

const Demo: React.FC = () => (
  <Flex gap="small" justify="flex-start" align="flex-start" vertical>
    <DatePicker onChange={onChange} />
    <DatePicker onChange={onChange} picker="week" />
    <DatePicker onChange={onChange} picker="month" />
    <DatePicker onChange={onChange} picker="quarter" />
    <DatePicker onChange={onChange} picker="year" />
  </Flex>
);

export default Demo;
```

## 语义槽

### DatePicker

- root（`semantic-mark-root`）: 根元素，包含相对定位、行内flex布局、内边距、边框圆角、过渡动画等日期选择器容器的基础样式
- prefix（`semantic-mark-prefix`）: 前缀元素，包含flex布局、右外边距等前缀内容的布局样式
- input（`semantic-mark-input`）: 输入框元素，包含相对定位、宽度、颜色、字体、行高、过渡动画等输入框的核心交互样式
- suffix（`semantic-mark-suffix`）: 后缀元素，包含flex布局、颜色、行高、指针事件、过渡动画等后缀内容的样式
- popup（`semantic-mark-popup`）: 弹出框元素
- popup.container（`semantic-mark-popup-container`）: 容器元素，设置背景色、内边距、圆角、阴影、边框和内容展示样式
- popup.header（`semantic-mark-popup-header`）: 弹出框头部元素，包含导航按钮、月份年份选择器等头部控制区域的布局和样式
- popup.body（`semantic-mark-popup-body`）: 弹出框主体元素，包含日期面板表格的容器布局和样式
- popup.content（`semantic-mark-popup-content`）: 弹出框内容元素，包含日期表格的宽度、边框、单元格等内容展示样式
- popup.item（`semantic-mark-popup-item`）: 弹出框单项元素，包含日期单元格的尺寸、背景色、边框圆角、悬停态、选中态等交互样式
- popup.footer（`semantic-mark-popup-footer`）: 弹出框底部元素，包含确认取消按钮、快捷选择等底部操作区域的布局样式

```tsx
<DatePicker
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    prefix: "semantic-mark-prefix",
    input: "semantic-mark-input",
    suffix: "semantic-mark-suffix",
    popup: "semantic-mark-popup",
    popup.container: "semantic-mark-popup-container",
    popup.header: "semantic-mark-popup-header",
    popup.body: "semantic-mark-popup-body",
    popup.content: "semantic-mark-popup-content",
    popup.item: "semantic-mark-popup-item",
    popup.footer: "semantic-mark-popup-footer"
  }}
/>
```
