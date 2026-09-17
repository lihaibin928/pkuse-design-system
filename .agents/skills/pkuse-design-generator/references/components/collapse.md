<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Collapse 折叠面板

- 分组：数据展示
- 组件文档：<https://ant.design/components/collapse-cn.md>
- 语义文档：<https://ant.design/components/collapse-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## collapse-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `collapse-cn`

可以折叠/展开的内容区域。

## 何时使用

- 对复杂区域进行分组和隐藏，保持页面的整洁。
- `手风琴` 是一种特殊的折叠面板，只允许单个内容区域展开。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { CollapseProps } from 'antd';
import { Collapse } from 'antd';

const text = `
  A dog is a type of domesticated animal.
  Known for its loyalty and faithfulness,
  it can be found as a welcome guest in many households across the world.
`;

const items: CollapseProps['items'] = [
  {
    key: '1',
    label: 'This is panel header 1',
    children: <p>{text}</p>,
  },
  {
    key: '2',
    label: 'This is panel header 2',
    children: <p>{text}</p>,
  },
  {
    key: '3',
    label: 'This is panel header 3',
    children: <p>{text}</p>,
  },
];

const App: React.FC = () => {
  const onChange = (key: string | string[]) => {
    console.log(key);
  };

  return <Collapse items={items} defaultActiveKey={['1']} onChange={onChange} />;
};

export default App;
```

## 语义槽

### Collapse

- root（`semantic-mark-root`）: 根元素，包含折叠面板的边框、圆角、背景色等容器样式，控制面板的整体布局和外观
- header（`semantic-mark-header`）: 头部元素，包含flex布局、内边距、颜色、行高、光标样式、过渡动画等面板头部的交互和样式
- title（`semantic-mark-title`）: 标题元素，包含flex自适应布局、右边距等标题文字的布局和排版样式
- body（`semantic-mark-body`）: 内容元素，包含内边距、颜色、背景色等面板内容区域的展示样式
- icon（`semantic-mark-icon`）: 图标元素，包含字体大小、过渡动画、旋转变换等展开收起箭头的样式和动效

```tsx
<Collapse
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    body: "semantic-mark-body",
    icon: "semantic-mark-icon"
  }}
/>
```
