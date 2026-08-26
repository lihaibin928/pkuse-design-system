<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Cascader 级联选择

- 分组：数据录入
- 组件文档：<https://ant.design/components/cascader-cn.md>
- 语义文档：<https://ant.design/components/cascader-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## cascader-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `cascader-cn`

级联选择框。

## 何时使用

- 需要从一组相关联的数据集合进行选择，例如省市区，公司层级，事物分类等。
- 从一个较大的数据集合中进行选择时，用多级分类进行分隔，方便选择。
- 比起 Select 组件，可以在同一个浮层中完成选择，有较好的体验。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { CascaderProps } from 'antd';
import { Cascader } from 'antd';
import type { HTMLAriaDataAttributes } from 'antd/es/_util/aria-data-attrs';

type Option = {
  value: string;
  label: string;
  children?: Option[];
} & HTMLAriaDataAttributes;

const options: Option[] = [
  {
    value: 'zhejiang',
    label: 'Zhejiang',
    'aria-label': 'Zhejiang',
    'data-title': 'Zhejiang',
    children: [
      {
        value: 'hangzhou',
        label: 'Hangzhou',
        'aria-label': 'Hangzhou',
        'data-title': 'Hangzhou',
        children: [
          {
            value: 'xihu',
            label: 'West Lake',
            'aria-label': 'West Lake',
            'data-title': 'West Lake',
          },
        ],
      },
    ],
  },
  {
    value: 'jiangsu',
    label: 'Jiangsu',
    'aria-label': 'Jiangsu',
    'data-title': 'Jiangsu',
    children: [
      {
        value: 'nanjing',
        label: 'Nanjing',
        'aria-label': 'Nanjing',
        'data-title': 'Nanjing',
        children: [
          {
            value: 'zhonghuamen',
            label: 'Zhong Hua Men',
            'aria-label': 'Zhong Hua Men',
            'data-title': 'Zhong Hua Men',
          },
        ],
      },
    ],
  },
];

const onChange: CascaderProps<Option>['onChange'] = (value) => {
  console.log(value);
};

const App: React.FC = () => (
  <Cascader options={options} onChange={onChange} placeholder="Please select" />
);

export default App;
```

## 语义槽

### Cascader

- root（`semantic-mark-root`）: 根元素，包含相对定位、行内 flex 布局、光标样式、过渡动画、边框等选择器容器的基础样式
- prefix（`semantic-mark-prefix`）: 前缀元素，包含前缀内容的布局和样式
- suffix（`semantic-mark-suffix`）: 后缀元素，包含后缀内容的布局和样式，如清除按钮、箭头图标等
- input（`semantic-mark-input`）: 输入框元素，包含搜索输入框的样式、光标控制、字体继承等搜索相关样式，去除了边框样式
- content（`semantic-mark-content`）: 多选容器，包含已选项的布局、间距、换行相关样式
- clear（`semantic-mark-clear`）: 清除按钮元素，包含清除按钮的布局、样式和交互效果
- item（`semantic-mark-item`）: 多选项元素，包含边框、背景、内边距、外边距样式
- itemContent（`semantic-mark-itemContent`）: 多选项内容区域，包含文字的省略样式
- itemRemove（`semantic-mark-itemRemove`）: 多选项移除按钮，包含字体相关样式
- placeholder（`semantic-mark-placeholder`）: 占位符元素，包含占位符文本的字体样式和颜色
- popup.root（`semantic-mark-popup-root`）: 弹出菜单元素，包含弹出层的定位、层级、背景、边框、阴影等弹出容器样式
- popup.list（`semantic-mark-popup-list`）: 弹出菜单列表元素，包含选项列表的布局、滚动、最大高度等列表容器样式
- popup.listItem（`semantic-mark-popup-listItem`）: 弹出菜单条目元素，包含选项项的内边距、悬浮效果、选中状态、禁用状态等选项交互样式

```tsx
<Cascader
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    prefix: "semantic-mark-prefix",
    suffix: "semantic-mark-suffix",
    input: "semantic-mark-input",
    content: "semantic-mark-content",
    clear: "semantic-mark-clear",
    item: "semantic-mark-item",
    itemContent: "semantic-mark-itemContent",
    itemRemove: "semantic-mark-itemRemove",
    placeholder: "semantic-mark-placeholder",
    popup.root: "semantic-mark-popup-root",
    popup.list: "semantic-mark-popup-list",
    popup.listItem: "semantic-mark-popup-listItem"
  }}
/>
```
