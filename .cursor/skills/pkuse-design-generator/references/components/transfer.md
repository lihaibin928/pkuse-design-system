<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Transfer 穿梭框

- 分组：数据录入
- 组件文档：<https://ant.design/components/transfer-cn.md>
- 语义文档：<https://ant.design/components/transfer-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## transfer-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `transfer-cn`

双栏穿梭选择框。

## 何时使用

- 需要在多个可选项中进行多选时。
- 比起 Select 和 TreeSelect，穿梭框占据更大的空间，可以展示可选项的更多信息。

穿梭选择框用直观的方式在两栏中移动元素，完成选择行为。

选择一个或以上的选项后，点击对应的方向键，可以把选中的选项移动到另一栏。其中，左边一栏为 `source`，右边一栏为 `target`，API 的设计也反映了这两个概念。

> 注意：穿梭框组件只支持受控使用，不支持非受控模式。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { Transfer } from 'antd';
import type { TransferProps } from 'antd';

interface RecordType {
  key: string;
  title: string;
  description: string;
}

const mockData = Array.from({ length: 20 }).map<RecordType>((_, i) => ({
  key: i.toString(),
  title: `content${i + 1}`,
  description: `description of content${i + 1}`,
}));

const initialTargetKeys = mockData.filter((item) => Number(item.key) > 10).map((item) => item.key);

const App: React.FC = () => {
  const [targetKeys, setTargetKeys] = useState<TransferProps['targetKeys']>(initialTargetKeys);
  const [selectedKeys, setSelectedKeys] = useState<TransferProps['targetKeys']>([]);

  const onChange: TransferProps['onChange'] = (nextTargetKeys, direction, moveKeys) => {
    console.log('targetKeys:', nextTargetKeys);
    console.log('direction:', direction);
    console.log('moveKeys:', moveKeys);
    setTargetKeys(nextTargetKeys);
  };

  const onSelectChange: TransferProps['onSelectChange'] = (
    sourceSelectedKeys,
    targetSelectedKeys,
  ) => {
    console.log('sourceSelectedKeys:', sourceSelectedKeys);
    console.log('targetSelectedKeys:', targetSelectedKeys);
    setSelectedKeys([...sourceSelectedKeys, ...targetSelectedKeys]);
  };

  const onScroll: TransferProps['onScroll'] = (direction, e) => {
    console.log('direction:', direction);
    console.log('target:', e.target);
  };

  return (
    <Transfer
      dataSource={mockData}
      titles={['Source', 'Target']}
      targetKeys={targetKeys}
      selectedKeys={selectedKeys}
      onChange={onChange}
      onSelectChange={onSelectChange}
      onScroll={onScroll}
      render={(item) => item.title}
    />
  );
};

export default App;
```

## 语义槽

### Transfer

- root（`semantic-mark-root`）: 根元素，设置flex布局、穿梭框容器的基础样式和布局控制
- section（`semantic-mark-section`）: 区域元素，设置flex布局、宽度、高度、最小高度、边框、圆角等单侧穿梭框的容器样式
- source.section（`semantic-mark-source-section`）: 源区域元素，仅作用于左侧穿梭框容器样式
- target.section（`semantic-mark-target-section`）: 目标区域元素，仅作用于右侧穿梭框容器样式
- source.header（`semantic-mark-source-header`）: 源头部元素，仅作用于左侧头部区域样式
- target.header（`semantic-mark-target-header`）: 目标头部元素，仅作用于右侧头部区域样式
- source.title（`semantic-mark-source-title`）: 源标题元素，仅作用于左侧标题文本样式
- target.title（`semantic-mark-target-title`）: 目标标题元素，仅作用于右侧标题文本样式
- source.body（`semantic-mark-source-body`）: 源内容元素，仅作用于左侧列表主体区域样式
- target.body（`semantic-mark-target-body`）: 目标内容元素，仅作用于右侧列表主体区域样式
- source.list（`semantic-mark-source-list`）: 源列表元素，仅作用于左侧列表内容区域样式
- target.list（`semantic-mark-target-list`）: 目标列表元素，仅作用于右侧列表内容区域样式
- source.item（`semantic-mark-source-item`）: 源列表项元素，仅作用于左侧列表项样式
- target.item（`semantic-mark-target-item`）: 目标列表项元素，仅作用于右侧列表项样式
- source.itemIcon（`semantic-mark-source-itemIcon`）: 源列表项图标元素，仅作用于左侧图标样式
- target.itemIcon（`semantic-mark-target-itemIcon`）: 目标列表项图标元素，仅作用于右侧图标样式
- source.itemContent（`semantic-mark-source-itemContent`）: 源列表项内容元素，仅作用于左侧文本内容样式
- target.itemContent（`semantic-mark-target-itemContent`）: 目标列表项内容元素，仅作用于右侧文本内容样式
- source.footer（`semantic-mark-source-footer`）: 源页脚元素，仅作用于左侧页脚区域样式
- target.footer（`semantic-mark-target-footer`）: 目标页脚元素，仅作用于右侧页脚区域样式
- header（`semantic-mark-header`）: 头部元素，设置flex布局、对齐方式、高度、内边距、颜色、背景色、下边框、圆角等头部区域的样式
- title（`semantic-mark-title`）: 标题元素，设置文本省略、flex占比、文本对齐、自动左边距等标题文字的布局和样式
- body（`semantic-mark-body`）: 内容元素，设置列表主体区域的容器样式和布局控制
- list（`semantic-mark-list`）: 列表元素，设置列表内容的样式、布局和滚动控制
- item（`semantic-mark-item`）: 列表项元素，设置相对定位、内边距、边框、悬停态、选中态、禁用态等列表项的交互样式
- itemIcon（`semantic-mark-itemIcon`）: 列表项图标元素，设置复选框等图标的样式和交互状态
- itemContent（`semantic-mark-itemContent`）: 列表项内容元素，设置文本省略、内边距等列表项文本内容的展示样式
- footer（`semantic-mark-footer`）: 页脚元素，设置底部操作区域的样式和布局
- actions（`semantic-mark-actions`）: 操作元素，设置穿梭按钮组的样式、布局和交互状态

```tsx
<Transfer
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    section: "semantic-mark-section",
    source.section: "semantic-mark-source-section",
    target.section: "semantic-mark-target-section",
    source.header: "semantic-mark-source-header",
    target.header: "semantic-mark-target-header",
    source.title: "semantic-mark-source-title",
    target.title: "semantic-mark-target-title",
    source.body: "semantic-mark-source-body",
    target.body: "semantic-mark-target-body",
    source.list: "semantic-mark-source-list",
    target.list: "semantic-mark-target-list",
    source.item: "semantic-mark-source-item",
    target.item: "semantic-mark-target-item",
    source.itemIcon: "semantic-mark-source-itemIcon",
    target.itemIcon: "semantic-mark-target-itemIcon",
    source.itemContent: "semantic-mark-source-itemContent",
    target.itemContent: "semantic-mark-target-itemContent",
    source.footer: "semantic-mark-source-footer",
    target.footer: "semantic-mark-target-footer",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    body: "semantic-mark-body",
    list: "semantic-mark-list",
    item: "semantic-mark-item",
    itemIcon: "semantic-mark-itemIcon",
    itemContent: "semantic-mark-itemContent",
    footer: "semantic-mark-footer",
    actions: "semantic-mark-actions"
  }}
/>
```
