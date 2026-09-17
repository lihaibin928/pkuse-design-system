<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Drawer 抽屉

- 分组：反馈
- 组件文档：<https://ant.design/components/drawer-cn.md>
- 语义文档：<https://ant.design/components/drawer-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## drawer-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `drawer-cn`

屏幕边缘滑出的浮层面板。

## 何时使用

抽屉从父窗体边缘滑入，覆盖住部分父窗体内容。用户在抽屉内操作时不必离开当前任务，操作完成后，可以平滑地回到原任务。

- 当需要一个附加的面板来控制父窗体内容，这个面板在需要时呼出。比如，控制界面展示样式，往界面中添加内容。
- 当需要在当前任务流中插入临时任务，创建或预览附加内容。比如展示协议条款，创建子对象。

> 开发者注意事项：
>
> 自 `5.17.0` 版本，我们提供了 `loading` 属性，内置 Spin 组件作为加载状态，但是自 `5.18.0` 版本开始，我们修复了设计失误，将内置的 Spin 组件替换成了 Skeleton 组件，同时收窄了 `loading` api 的类型范围，只能接收 boolean 类型。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 列表上的新增 / 编辑优先用 `Drawer` 或 `Modal`，不要默认拆 `/new`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { Button, Drawer } from 'antd';

const App: React.FC = () => {
  const [open, setOpen] = useState(false);

  const showDrawer = () => {
    setOpen(true);
  };

  const onClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Button type="primary" onClick={showDrawer}>
        Open
      </Button>
      <Drawer
        title="Basic Drawer"
        closable={{ 'aria-label': 'Close Button' }}
        onClose={onClose}
        open={open}
      >
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
      </Drawer>
    </>
  );
};

export default App;
```

## 语义槽

### Drawer

- root（`semantic-mark-root`）: 根元素，包含固定定位、层级控制、指针事件、颜色等抽屉容器的基础样式和布局控制
- mask（`semantic-mark-mask`）: 遮罩层元素，包含绝对定位、层级、背景色、指针事件等遮罩层的样式和交互控制
- section（`semantic-mark-section`）: Drawer 容器元素，包含flex布局、宽高、溢出控制、背景色、指针事件等抽屉主体的样式
- header（`semantic-mark-header`）: 头部元素，包含flex布局、对齐方式、内边距、字体大小、行高、下边框等头部区域的样式
- body（`semantic-mark-body`）: 内容元素，包含flex占比、最小尺寸、内边距、溢出滚动等内容区域的展示和布局样式
- footer（`semantic-mark-footer`）: 底部元素，包含flex收缩、内边距、上边框等底部操作区域的样式
- title（`semantic-mark-title`）: 标题元素，包含flex占比、外边距、字体权重、字体大小、行高等标题文字的样式
- extra（`semantic-mark-extra`）: 额外元素，包含flex固定布局等额外操作内容的样式控制
- dragger（`semantic-mark-dragger`）: 拖拽元素，用于调整抽屉大小的拖拽手柄，包含绝对定位、背景透明、指针事件控制、hover状态样式、拖拽状态样式等
- close（`semantic-mark-close`）: 关闭按钮元素，包含按钮的基础样式

```tsx
<Drawer
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    mask: "semantic-mark-mask",
    section: "semantic-mark-section",
    header: "semantic-mark-header",
    body: "semantic-mark-body",
    footer: "semantic-mark-footer",
    title: "semantic-mark-title",
    extra: "semantic-mark-extra",
    dragger: "semantic-mark-dragger",
    close: "semantic-mark-close"
  }}
/>
```
