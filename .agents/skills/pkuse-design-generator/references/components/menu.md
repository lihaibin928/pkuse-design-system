<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Menu 导航菜单

- 分组：导航
- 组件文档：<https://ant.design/components/menu-cn.md>
- 语义文档：<https://ant.design/components/menu-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## menu-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `menu-cn`

为页面和功能提供导航的菜单列表。

## 何时使用

导航菜单是一个网站的灵魂，用户依赖导航在各个页面中进行跳转。一般分为顶部导航和侧边导航，顶部导航提供全局性的类目和功能，侧边导航提供多级结构来收纳和排列网站架构。

更多布局和导航的使用可以参考：[通用布局](/components/layout-cn)。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 选中态只用组件语义（浅底 + 主色文字），不要自造导航皮肤。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { AppstoreOutlined, MailOutlined, SettingOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';

type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  {
    label: 'Navigation One',
    key: 'mail',
    icon: <MailOutlined />,
  },
  {
    label: 'Navigation Two',
    key: 'app',
    icon: <AppstoreOutlined />,
    disabled: true,
  },
  {
    label: 'Navigation Three - Submenu',
    key: 'SubMenu',
    icon: <SettingOutlined />,
    children: [
      {
        type: 'group',
        label: 'Item 1',
        children: [
          { label: 'Option 1', key: 'setting:1' },
          { label: 'Option 2', key: 'setting:2' },
        ],
      },
      {
        type: 'group',
        label: 'Item 2',
        children: [
          { label: 'Option 3', key: 'setting:3' },
          { label: 'Option 4', key: 'setting:4' },
        ],
      },
    ],
  },
  {
    key: 'alipay',
    label: (
      <a href="https://ant.design" target="_blank" rel="noopener noreferrer">
        Navigation Four - Link
      </a>
    ),
  },
];

const App: React.FC = () => {
  const [current, setCurrent] = useState('mail');

  const onClick: MenuProps['onClick'] = (e) => {
    console.log('click ', e);
    setCurrent(e.key);
  };

  return <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />;
};

export default App;
```

## 语义槽

### Menu

- root（`semantic-mark-root`）: 根元素，包含菜单容器的基础样式和布局
- item（`semantic-mark-item`）: 条目元素，包含相对定位、块级显示、外边距、空白符处理、光标样式、过渡动画等菜单项的基础交互样式
- itemContent（`semantic-mark-itemContent`）: 条目内容元素，包含菜单项内容的布局和排版样式
- itemIcon（`semantic-mark-itemIcon`）: 图标元素，包含最小宽度、字体大小、过渡动画、图标重置样式，以及与文本的间距控制
- itemTitle（`semantic-mark-itemTitle`）: 菜单标题元素(horizontal 模式不生效)，包含标题文字的样式和布局
- list（`semantic-mark-list`）: 菜单列表元素(horizontal 模式不生效)，包含菜单列表的布局和容器样式
- popup（`semantic-mark-popup`）: 弹出菜单(inline 模式不生效)，包含弹出层的定位、层级、背景等样式
- subMenu.itemTitle（`semantic-mark-subMenu-itemTitle`）: 子菜单标题元素，包含子菜单标题的样式和交互效果
- subMenu.list（`semantic-mark-subMenu-list`）: 子菜单列表元素，包含子菜单列表的布局和容器样式
- subMenu.item（`semantic-mark-subMenu-item`）: 子菜单单项元素，包含子菜单项的样式和交互效果
- subMenu.itemIcon（`semantic-mark-subMenu-itemIcon`）: 子菜单条目图标元素，包含子菜单图标的尺寸和样式
- subMenu.itemContent（`semantic-mark-subMenu-itemContent`）: 子菜单条目内容元素，包含子菜单内容的布局和排版

```tsx
<Menu
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    item: "semantic-mark-item",
    itemContent: "semantic-mark-itemContent",
    itemIcon: "semantic-mark-itemIcon",
    itemTitle: "semantic-mark-itemTitle",
    list: "semantic-mark-list",
    popup: "semantic-mark-popup",
    subMenu.itemTitle: "semantic-mark-subMenu-itemTitle",
    subMenu.list: "semantic-mark-subMenu-list",
    subMenu.item: "semantic-mark-subMenu-item",
    subMenu.itemIcon: "semantic-mark-subMenu-itemIcon",
    subMenu.itemContent: "semantic-mark-subMenu-itemContent"
  }}
/>
```
