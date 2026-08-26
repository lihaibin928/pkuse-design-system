<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Calendar 日历

- 分组：数据展示
- 组件文档：<https://ant.design/components/calendar-cn.md>
- 语义文档：<https://ant.design/components/calendar-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## calendar-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `calendar-cn`

按照日历形式展示数据的容器。

## 何时使用

当数据是日期或按照日期划分时，例如日程、课表、价格日历等，农历等。目前支持年/月切换。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Calendar } from 'antd';
import type { CalendarProps } from 'antd';
import type { Dayjs } from 'dayjs';

const App: React.FC = () => {
  const onPanelChange = (value: Dayjs, mode: CalendarProps<Dayjs>['mode']) => {
    console.log(value.format('YYYY-MM-DD'), mode);
  };

  return <Calendar onPanelChange={onPanelChange} />;
};

export default App;
```

## 语义槽

### Calendar

- root（`semantic-mark-root`）: 根元素，包含日历组件的背景色、边框、圆角等基础样式和整体布局结构
- header（`semantic-mark-header`）: 头部元素，包含年份选择器、月份选择器、模式切换器的布局和样式控制
- body（`semantic-mark-body`）: 主体元素，包含日历表格的内边距、布局控制等样式，用于容纳日历网格
- content（`semantic-mark-content`）: 内容元素，包含日历表格的宽度、高度等尺寸控制和表格样式
- item（`semantic-mark-item`）: 条目元素，包含日历单元格的背景色、边框、悬停态、选中态等交互样式
- itemContent（`semantic-mark-itemContent`）: 条目内容元素，包含日历单元格内自定义内容区域的高度、溢出等样式控制

```tsx
<Calendar
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    body: "semantic-mark-body",
    content: "semantic-mark-content",
    item: "semantic-mark-item",
    itemContent: "semantic-mark-itemContent"
  }}
/>
```
