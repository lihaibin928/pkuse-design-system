<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Table 表格

- 分组：数据展示
- 组件文档：<https://ant.design/components/table-cn.md>
- 语义文档：<https://ant.design/components/table-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## table-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `table-cn`

展示行列数据。

## 何时使用

- 当有大量结构化的数据需要展现时；
- 当需要对数据进行排序、搜索、分页、自定义操作等复杂行为时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 列表主界面用表格，不要用卡片宫格替代。
- 表头和状态色走 Token；默认不做斑马纹。
- 删除 / 批量操作必须确认，并校验权限。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Flex, Space, Table, Tag } from 'antd';
import type { TableProps } from 'antd';

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
  tags: string[];
}

const columns: TableProps<DataType>['columns'] = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    render: (text) => <a>{text}</a>,
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
  },
  {
    title: 'Address',
    dataIndex: 'address',
    key: 'address',
  },
  {
    title: 'Tags',
    key: 'tags',
    dataIndex: 'tags',
    render: (_, { tags }) => (
      <Flex gap="small" align="center" wrap>
        {tags.map((tag) => {
          let color = tag.length > 5 ? 'geekblue' : 'green';
          if (tag === 'kawaii') {
            color = 'volcano';
          }
          return (
            <Tag color={color} key={tag}>
              {tag.toUpperCase()}
            </Tag>
          );
        })}
      </Flex>
    ),
  },
  {
    title: 'Action',
    key: 'action',
    render: (_, record) => (
      <Space size="medium">
        <a>Invite {record.name}</a>
        <a>Delete</a>
      </Space>
    ),
  },
];

const data: DataType[] = [
  {
    key: '1',
    name: 'John Brown',
    age: 32,
    address: 'New York No. 1 Lake Park',
    tags: ['nice', 'developer'],
  },
  {
    key: '2',
    name: 'Jim Green',
    age: 42,
    address: 'London No. 1 Lake Park',
    tags: ['kawaii'],
  },
  {
    key: '3',
    name: 'Joe Black',
    age: 32,
    address: 'Sydney No. 1 Lake Park',
    tags: ['cool', 'teacher'],
  },
];

const App: React.FC = () => <Table<DataType> columns={columns} dataSource={data} />;

export default App;
```

## 语义槽

### Table

- root（`semantic-mark-root`）: 根元素，包含字体大小、背景色、圆角、滚动条颜色等表格容器的基础样式
- section（`semantic-mark-section`）: 容器元素，包含清除浮动、最大宽度、滚动条背景等表格包装容器样式
- header.wrapper（`semantic-mark-header-wrapper`）: 头部容器元素，包含表头的布局和容器样式
- header.row（`semantic-mark-header-row`）: 头部行元素，包含表头行的布局和样式
- header.cell（`semantic-mark-header-cell`）: 头部单元格元素，包含相对定位、内边距、文字换行、背景色、文字颜色、字体权重等表头单元格样式
- title（`semantic-mark-title`）: 标题元素，包含表格标题的样式和布局
- body.wrapper（`semantic-mark-body-wrapper`）: 主体容器元素，包含表格主体的布局和容器样式
- body.row（`semantic-mark-body-row`）: 主体行元素，包含数据行的悬浮效果、选中状态、展开状态等交互样式
- body.cell（`semantic-mark-body-cell`）: 主体单元格元素，包含相对定位、内边距、文字换行等数据单元格的基础样式
- footer（`semantic-mark-footer`）: 底部元素，包含表格底部的背景色、文字颜色等样式
- content（`semantic-mark-content`）: 内容元素，包含表格内容区域的样式和布局
- pagination.root（`semantic-mark-pagination-root`）: 分页根元素，包含分页组件的基础样式和布局
- pagination.item（`semantic-mark-pagination-item`）: 分页单项元素，包含分页项的样式和交互效果

```tsx
<Table
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    section: "semantic-mark-section",
    header.wrapper: "semantic-mark-header-wrapper",
    header.row: "semantic-mark-header-row",
    header.cell: "semantic-mark-header-cell",
    title: "semantic-mark-title",
    body.wrapper: "semantic-mark-body-wrapper",
    body.row: "semantic-mark-body-row",
    body.cell: "semantic-mark-body-cell",
    footer: "semantic-mark-footer",
    content: "semantic-mark-content",
    pagination.root: "semantic-mark-pagination-root",
    pagination.item: "semantic-mark-pagination-item"
  }}
/>
```
