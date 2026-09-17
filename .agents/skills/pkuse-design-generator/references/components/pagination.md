<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Pagination 分页

- 分组：导航
- 组件文档：<https://ant.design/components/pagination-cn.md>
- 语义文档：<https://ant.design/components/pagination-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## pagination-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `pagination-cn`

分页器用于分隔长列表，每次只加载一个页面。

## 何时使用

- 当加载/渲染所有数据将花费很多时间时；
- 可切换页码浏览数据。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Pagination } from 'antd';

const App: React.FC = () => <Pagination defaultCurrent={1} total={50} />;

export default App;
```

## 语义槽

### Pagination

- root（`semantic-mark-root`）: 根元素，设置flex布局、对齐方式、换行和列表样式
- item（`semantic-mark-item`）: 页码元素，设置尺寸、内边距、边框、背景色、悬停态和激活态样式

```tsx
<Pagination
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item"
  }}
/>
```
