<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Empty 空状态

- 分组：数据展示
- 组件文档：<https://ant.design/components/empty-cn.md>
- 语义文档：<https://ant.design/components/empty-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## empty-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `empty-cn`

空状态时的展示占位图。

## 何时使用

- 当目前没有数据时，用于显式的用户提示。
- 初始化场景时的引导创建流程。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 空数据保留查询区；区分「无数据」和「无搜索结果」。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Empty } from 'antd';

const App: React.FC = () => <Empty />;

export default App;
```

## 语义槽

### Empty

- root（`semantic-mark-root`）: 根元素，设置文本对齐、字体和行高样式
- image（`semantic-mark-image`）: 图标元素，设置高度、透明度、边距和图片样式
- description（`semantic-mark-description`）: 描述元素，设置文本颜色样式
- footer（`semantic-mark-footer`）: 底部元素，设置顶部边距和操作按钮样式

```tsx
<Empty
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    image: "semantic-mark-image",
    description: "semantic-mark-description",
    footer: "semantic-mark-footer"
  }}
/>
```
