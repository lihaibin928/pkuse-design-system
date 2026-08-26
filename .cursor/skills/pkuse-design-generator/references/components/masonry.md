<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Masonry 瀑布流

- 分组：布局
- 组件文档：<https://ant.design/components/masonry-cn.md>
- 语义文档：<https://ant.design/components/masonry-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## masonry-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `masonry-cn`

## 何时使用

- 展示不规则高度的图片或卡片时
- 需要按照列数均匀分布内容时
- 需要响应式调整列数时

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Card, Masonry } from 'antd';
import type { MasonryProps } from 'antd';

type MasonryItemType = NonNullable<MasonryProps<number>['items']>[number];

const heights = [150, 50, 90, 70, 110, 150, 130, 80, 50, 90, 100, 150, 60, 50, 80].map(
  (height, index) => {
    const item: MasonryItemType = {
      key: `item-${index}`,
      data: height,
    };

    if (index === 4) {
      item.children = (
        <Card
          size="small"
          cover={
            <img
              alt="food"
              src="https://images.unsplash.com/photo-1491961865842-98f7befd1a60?w=523&auto=format"
            />
          }
        >
          <Card.Meta title="I'm Special" description="Let's have a meal" />
        </Card>
      );
    }

    return item;
  },
);

const App: React.FC = () => (
  <Masonry
    columns={4}
    gutter={16}
    items={heights}
    itemRender={({ data, index }) => (
      <Card size="small" style={{ height: data }}>
        {index + 1}
      </Card>
    )}
  />
);

export default App;
```

## 语义槽

### Masonry

- root（`semantic-mark-root`）: 根元素，设置相对定位、flex布局和瀑布流容器样式
- item（`semantic-mark-item`）: 条目元素，设置绝对定位、宽度计算、过渡动画和瀑布流项目样式

```tsx
<Masonry
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item"
  }}
/>
```
