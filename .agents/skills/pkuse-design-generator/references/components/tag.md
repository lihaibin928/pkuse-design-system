<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Tag 标签

- 分组：数据展示
- 组件文档：<https://ant.design/components/tag-cn.md>
- 语义文档：<https://ant.design/components/tag-cn/semantic_group.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## tag-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `tag-cn`

进行标记和分类的小标签。

## 何时使用

- 用于标记事物的属性和维度。
- 进行分类。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- Tag 只表示分类或非关键状态，不用作主操作或危险确认。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { CloseCircleOutlined, DeleteOutlined } from '@ant-design/icons';
import { Flex, Tag } from 'antd';

const preventDefault = (e: React.MouseEvent<HTMLElement>) => {
  e.preventDefault();
  console.log('Clicked! But prevent default.');
};

const App: React.FC = () => (
  <Flex gap="small" align="center" wrap>
    <Tag>Tag 1</Tag>
    <Tag>
      <a
        href="https://github.com/ant-design/ant-design/issues/1862"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="Ant Design issue"
      >
        Link
      </a>
    </Tag>
    <Tag closeIcon onClose={preventDefault}>
      Prevent Default
    </Tag>
    <Tag closeIcon={<CloseCircleOutlined />} onClose={console.log}>
      Tag 2
    </Tag>
    <Tag
      closable={{
        closeIcon: <DeleteOutlined />,
        'aria-label': 'Close Button',
      }}
      onClose={console.log}
    >
      Tag 3
    </Tag>
  </Flex>
);

export default App;
```

## 语义槽

### Tag.Group

- root（`semantic-mark-root`）: 根元素，设置标签组的容器样式和布局
- item（`semantic-mark-item`）: 标签项元素，设置行内块显示、高度、内边距、字体大小、行高、背景色、边框、圆角、透明度、过渡动画、可选中状态等样式

```tsx
<Tag.Group
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item"
  }}
/>
```

### Tag

- root（`semantic-mark-root`）: 根元素，包含行内块布局、自动高度、内边距、字体大小、行高、禁止换行、背景色、边框、圆角、透明度、过渡动画、文本对齐、相对定位等标签的基础样式
- icon（`semantic-mark-icon`）: 图标元素，包含字体大小、颜色、光标样式、过渡动画等图标的显示样式
- content（`semantic-mark-content`）: 内容元素，包含文本内容的颜色、字体样式等内容区域的样式
- close（`semantic-mark-close`）: 关闭元素，包含关闭按钮的布局、光标样式、过渡动画等交互样式

```tsx
<Tag
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    icon: "semantic-mark-icon",
    content: "semantic-mark-content",
    close: "semantic-mark-close"
  }}
/>
```
