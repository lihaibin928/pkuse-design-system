<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Listy 虚拟列表

- 分组：数据展示
- 组件文档：<https://ant.design/components/listy-cn.md>
- 语义文档：<https://ant.design/components/listy-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## listy-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `listy-cn`

高性能列表，支持分组，并可为长列表开启虚拟滚动。

## 何时使用

- 需要渲染长列表，又不想为每一行都付出挂载成本时 —— 开启 `virtual` 后只渲染视口内的行。
- 列表需要分组，并让分组标题吸顶时。
- 需要以命令式方式控制滚动位置（跳到某一项、某个分组或某个像素位置）时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Listy } from 'antd';

interface Item {
  id: number;
  content: string;
}

const items = Array.from<any, Item>({ length: 20 }, (_, index) => ({
  id: index,
  content: `Item ${index}`,
}));

const App: React.FC = () => {
  return <Listy<Item> items={items} height={400} rowKey="id" itemRender={(item) => item.content} />;
};

export default App;
```

## 语义槽

### Listy

- root（`semantic-mark-root`）: 根元素，即滚动容器，设置字体与相对定位
- item（`semantic-mark-item`）: 条目元素，设置内间距、分割线与悬浮背景
- groupHeader（`semantic-mark-groupHeader`）: 分组标题元素，设置吸顶定位与背景色

```tsx
<Listy
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    groupHeader: "semantic-mark-groupHeader"
  }}
/>
```
