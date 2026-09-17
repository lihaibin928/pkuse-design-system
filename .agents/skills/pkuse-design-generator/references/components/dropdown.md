<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Dropdown 下拉菜单

- 分组：导航
- 组件文档：<https://ant.design/components/dropdown-cn.md>
- 语义文档：<https://ant.design/components/dropdown-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## dropdown-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `dropdown-cn`

向下弹出的列表。

## 何时使用

当页面上的操作命令过多时，用此组件可以收纳操作元素。点击或移入触点，会出现一个下拉菜单。可在列表中进行选择，并执行相应的命令。

- 用于收罗一组命令操作。
- Select 用于选择，而 Dropdown 是命令集合。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { DownOutlined, SmileOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Dropdown, Space } from 'antd';

const items: MenuProps['items'] = [
  {
    key: '1',
    label: (
      <a target="_blank" rel="noopener noreferrer" href="https://www.antgroup.com">
        1st menu item
      </a>
    ),
  },
  {
    key: '2',
    label: (
      <a target="_blank" rel="noopener noreferrer" href="https://www.aliyun.com">
        2nd menu item (disabled)
      </a>
    ),
    icon: <SmileOutlined />,
    disabled: true,
  },
  {
    key: '3',
    label: (
      <a target="_blank" rel="noopener noreferrer" href="https://www.luohanacademy.com">
        3rd menu item (disabled)
      </a>
    ),
    disabled: true,
  },
  {
    key: '4',
    danger: true,
    label: 'a danger item',
  },
];

const App: React.FC = () => (
  <Dropdown menu={{ items }}>
    <a onClick={(e) => e.preventDefault()}>
      <Space>
        Hover me
        <DownOutlined />
      </Space>
    </a>
  </Dropdown>
);

export default App;
```

## 语义槽

### Dropdown

- root（`semantic-mark-root`）: dropdown 的根元素，设置定位、层级和容器样式
- itemTitle（`semantic-mark-itemTitle`）: dropdown 选项的标题内容区域，设置布局和文字样式
- item（`semantic-mark-item`）: dropdown 的单个选项元素，设置选项的交互状态和背景样式
- itemContent（`semantic-mark-itemContent`）: dropdown 选项的主要内容区域，设置内容布局和链接样式
- itemIcon（`semantic-mark-itemIcon`）: dropdown 选项的图标区域，设置图标的尺寸和间距样式

```tsx
<Dropdown
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    itemTitle: "semantic-mark-itemTitle",
    item: "semantic-mark-item",
    itemContent: "semantic-mark-itemContent",
    itemIcon: "semantic-mark-itemIcon"
  }}
/>
```
