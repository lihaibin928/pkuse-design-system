<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# TreeSelect 树选择

- 分组：数据录入
- 组件文档：<https://ant.design/components/tree-select-cn.md>
- 语义文档：<https://ant.design/components/tree-select-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## tree-select-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `tree-select-cn`

树型选择控件。

## 何时使用

类似 Select 的选择控件，可选择的数据结构是一个树形结构时，可以使用 TreeSelect，例如公司层级、学科系统、分类目录等等。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { TreeSelect } from 'antd';
import type { TreeSelectProps } from 'antd';

const treeData = [
  {
    value: 'parent 1',
    title: 'parent 1',
    children: [
      {
        value: 'parent 1-0',
        title: 'parent 1-0',
        children: [
          {
            value: 'leaf1',
            title: 'leaf1',
          },
          {
            value: 'leaf2',
            title: 'leaf2',
          },
          {
            value: 'leaf3',
            title: 'leaf3',
          },
          {
            value: 'leaf4',
            title: 'leaf4',
          },
          {
            value: 'leaf5',
            title: 'leaf5',
          },
          {
            value: 'leaf6',
            title: 'leaf6',
          },
        ],
      },
      {
        value: 'parent 1-1',
        title: 'parent 1-1',
        children: [
          {
            value: 'leaf11',
            title: <b style={{ color: '#08c' }}>leaf11</b>,
          },
        ],
      },
    ],
  },
];
const App: React.FC = () => {
  const [value, setValue] = useState<string>();

  const onChange = (newValue: string) => {
    setValue(newValue);
  };

  const onPopupScroll: TreeSelectProps['onPopupScroll'] = (e) => {
    console.log('onPopupScroll', e);
  };

  return (
    <TreeSelect
      showSearch
      style={{ width: '100%' }}
      value={value}
      styles={{
        popup: {
          root: { maxHeight: 400, overflow: 'auto' },
        },
      }}
      placeholder="Please select"
      allowClear
      treeDefaultExpandAll
      onChange={onChange}
      treeData={treeData}
      onPopupScroll={onPopupScroll}
    />
  );
};

export default App;
```

## 语义槽

### TreeSelect

- root（`semantic-mark-root`）: 根元素，设置树选择器的基础样式、边框、圆角容器样式
- prefix（`semantic-mark-prefix`）: 前缀元素，设置前缀内容的布局和样式
- input（`semantic-mark-input`）: 输入框元素，设置文本输入、搜索、选择值显示等输入框的核心交互样式
- suffix（`semantic-mark-suffix`）: 后缀元素，设置后缀内容、清除按钮、下拉箭头等后缀区域的样式
- content（`semantic-mark-content`）: 多选容器，包含已选项的布局、间距、换行相关样式
- item（`semantic-mark-item`）: 多选项元素，包含边框、背景、内边距、外边距样式
- itemContent（`semantic-mark-itemContent`）: 多选项内容区域，包含文字的省略样式
- itemRemove（`semantic-mark-itemRemove`）: 多选项移除按钮，包含字体相关样式
- placeholder（`semantic-mark-placeholder`）: 占位符元素，包含占位符文本的字体样式和颜色
- popup.root（`semantic-mark-popup-root`）: 弹出菜单元素，设置下拉树形选择面板的定位、层级、背景、边框、阴影等弹层样式
- popup.item（`semantic-mark-popup-item`）: 弹出菜单条目元素，设置树节点选项的样式、悬停态、选中态等交互状态
- popup.itemTitle（`semantic-mark-popup-itemTitle`）: 弹出菜单标题元素，设置树节点标题文字的显示样式
- popup.itemSwitcher（`semantic-mark-popup-itemSwitcher`）: 弹出菜单切换器元素，设置树节点展开/收起按钮的样式和背景

```tsx
<TreeSelect
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    prefix: "semantic-mark-prefix",
    input: "semantic-mark-input",
    suffix: "semantic-mark-suffix",
    content: "semantic-mark-content",
    item: "semantic-mark-item",
    itemContent: "semantic-mark-itemContent",
    itemRemove: "semantic-mark-itemRemove",
    placeholder: "semantic-mark-placeholder",
    popup.root: "semantic-mark-popup-root",
    popup.item: "semantic-mark-popup-item",
    popup.itemTitle: "semantic-mark-popup-itemTitle",
    popup.itemSwitcher: "semantic-mark-popup-itemSwitcher"
  }}
/>
```
