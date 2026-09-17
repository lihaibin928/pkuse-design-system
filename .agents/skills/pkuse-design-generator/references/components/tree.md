<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Tree 树形控件

- 分组：数据展示
- 组件文档：<https://ant.design/components/tree-cn.md>
- 语义文档：<https://ant.design/components/tree-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## tree-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `tree-cn`

多层次的结构列表。

## 何时使用

文件夹、组织架构、生物分类、国家地区等等，世间万物的大多数结构都是树形结构。使用 `树控件` 可以完整展现其中的层级关系，并具有展开收起选择等交互功能。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Tree } from 'antd';
import type { TreeDataNode, TreeProps } from 'antd';

const treeData: TreeDataNode[] = [
  {
    title: 'parent 1',
    key: '0-0',
    children: [
      {
        title: 'parent 1-0',
        key: '0-0-0',
        disabled: true,
        children: [
          {
            title: 'leaf',
            key: '0-0-0-0',
            disableCheckbox: true,
          },
          {
            title: 'leaf',
            key: '0-0-0-1',
          },
        ],
      },
      {
        title: 'parent 1-1',
        key: '0-0-1',
        children: [{ title: <span style={{ color: '#1677ff' }}>sss</span>, key: '0-0-1-0' }],
      },
    ],
  },
];

const App: React.FC = () => {
  const onSelect: TreeProps['onSelect'] = (selectedKeys, info) => {
    console.log('selected', selectedKeys, info);
  };

  const onCheck: TreeProps['onCheck'] = (checkedKeys, info) => {
    console.log('onCheck', checkedKeys, info);
  };

  return (
    <Tree
      checkable
      defaultExpandedKeys={['0-0-0', '0-0-1']}
      defaultSelectedKeys={['0-0-1']}
      defaultCheckedKeys={['0-0-0', '0-0-1']}
      onSelect={onSelect}
      onCheck={onCheck}
      treeData={treeData}
    />
  );
};

export default App;
```

## 语义槽

### Tree

- root（`semantic-mark-root`）: 根元素，设置树形控件的基础样式、布局和容器控制
- item（`semantic-mark-item`）: 条目元素，设置树节点的基础样式、拖拽状态、角色属性、缩进、切换器、内容包装器等节点结构
- itemTitle（`semantic-mark-itemTitle`）: 标题元素，设置树节点标题文字的显示样式和文本内容
- itemIcon（`semantic-mark-itemIcon`）: 图标元素，设置树节点图标的样式、尺寸和状态显示
- itemSwitcher（`semantic-mark-itemSwitcher`）: 展开收起切换器元素，设置树节点展开/收起按钮的样式和背景

```tsx
<Tree
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    itemTitle: "semantic-mark-itemTitle",
    itemIcon: "semantic-mark-itemIcon",
    itemSwitcher: "semantic-mark-itemSwitcher"
  }}
/>
```
