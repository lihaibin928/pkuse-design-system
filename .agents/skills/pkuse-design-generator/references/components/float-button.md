<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# FloatButton 悬浮按钮

- 分组：通用
- 组件文档：<https://ant.design/components/float-button-cn.md>
- 语义文档：<https://ant.design/components/float-button-cn/semantic_group.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## float-button-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `float-button-cn`

悬浮于页面上方的按钮。

## 何时使用

- 用于网站上的全局功能；
- 无论浏览到何处都可以看见的按钮。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { FloatButton } from 'antd';

const App: React.FC = () => <FloatButton onClick={() => console.log('onClick')} />;

export default App;
```

## 语义槽

### FloatButton.Group

- root（`semantic-mark-root`）: 根元素，设置悬浮按钮组的容器样式、固定定位、层级、内边距、间距、方向模式等组合布局样式
- list（`semantic-mark-list`）: 列表元素，设置按钮组列表的Flex布局、圆角、阴影、动画过渡、垂直对齐等列表容器样式
- item（`semantic-mark-item`）: 列表项元素，设置单个悬浮按钮的样式、尺寸、形状、类型、状态、图标内容等按钮基础样式
- itemIcon（`semantic-mark-itemIcon`）: 列表项图标元素，设置悬浮按钮内图标的尺寸、颜色、对齐等图标显示样式
- itemContent（`semantic-mark-itemContent`）: 列表项内容元素，设置悬浮按钮内文字内容、徽标、描述等内容区域样式
- trigger（`semantic-mark-trigger`）: 触发元素，设置菜单模式下触发按钮的样式、形状、图标、悬停态、展开收起状态等交互样式
- triggerIcon（`semantic-mark-triggerIcon`）: 触发图标元素，设置触发按钮内图标的样式、旋转动画、切换状态等图标交互样式
- triggerContent（`semantic-mark-triggerContent`）: 触发内容元素，设置触发按钮内容区域的文字、标识、状态指示等内容样式

```tsx
<FloatButton.Group
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    list: "semantic-mark-list",
    item: "semantic-mark-item",
    itemIcon: "semantic-mark-itemIcon",
    itemContent: "semantic-mark-itemContent",
    trigger: "semantic-mark-trigger",
    triggerIcon: "semantic-mark-triggerIcon",
    triggerContent: "semantic-mark-triggerContent"
  }}
/>
```

### FloatButton

- root（`semantic-mark-root`）: 根元素，设置悬浮按钮的基础样式、形状尺寸、类型主题、固定定位、层级、阴影、间距等容器样式
- content（`semantic-mark-content`）: 内容元素，设置按钮内文字内容的字体大小、颜色、对齐、换行等文本显示样式
- icon（`semantic-mark-icon`）: 图标元素，设置按钮内图标的尺寸、颜色、行高、对齐等图标显示样式

```tsx
<FloatButton
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    content: "semantic-mark-content",
    icon: "semantic-mark-icon"
  }}
/>
```
