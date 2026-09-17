<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Breadcrumb 面包屑

- 分组：导航
- 组件文档：<https://ant.design/components/breadcrumb-cn.md>
- 语义文档：<https://ant.design/components/breadcrumb-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## breadcrumb-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `breadcrumb-cn`

显示当前页面在系统层级结构中的位置，并能向上返回。

## 何时使用

- 当系统拥有超过两级以上的层级结构时；
- 当需要告知用户『你在哪里』时；
- 当需要向上导航的功能时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Breadcrumb } from 'antd';

const App: React.FC = () => {
  return (
    <Breadcrumb
      items={[
        {
          title: 'Home',
        },
        {
          title: <a href="">Application Center</a>,
        },
        {
          title: <a href="">Application List</a>,
        },
        {
          title: 'An Application',
        },
      ]}
    />
  );
};

export default App;
```

## 语义槽

### Breadcrumb

- root（`semantic-mark-root`）: 根元素，包含文字颜色、字体大小、图标尺寸等基础样式，内部使用 flex 布局的有序列表
- item（`semantic-mark-item`）: Item 元素，包含文字颜色、链接的颜色变化、悬浮效果、内边距、圆角、高度、外边距等样式
- separator（`semantic-mark-separator`）: 分隔符元素，包含分隔符的外边距和颜色样式

```tsx
<Breadcrumb
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    separator: "semantic-mark-separator"
  }}
/>
```
