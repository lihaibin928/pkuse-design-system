<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Modal 对话框

- 分组：反馈
- 组件文档：<https://ant.design/components/modal-cn.md>
- 语义文档：<https://ant.design/components/modal-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## modal-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `modal-cn`

展示一个对话框，提供标题、内容区、操作区。

## 何时使用

需要用户处理事务，又不希望跳转页面以致打断工作流程时，可以使用 `Modal` 在当前页面正中打开一个浮层，承载相应的操作。

另外当需要一个简洁的确认框询问用户时，可以使用 [`App.useApp`](/components/app-cn/) 封装的语法糖方法。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 短流程用 `Modal`；表单超出抽屉容量才用独立页。
- 同一决策面不要并排两个主按钮。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { Button, Modal } from 'antd';

const App: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <Button type="primary" onClick={showModal}>
        Open Modal
      </Button>
      <Modal
        title="Basic Modal"
        closable={{ 'aria-label': 'Custom Close Button' }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
      </Modal>
    </>
  );
};

export default App;
```

## 语义槽

### Modal

- root（`semantic-mark-root`）: 根元素，包含相对定位、顶部位置、宽度、最大宽度、外边距、底部内边距等模态框容器的基础布局样式
- mask（`semantic-mark-mask`）: 遮罩层元素，包含固定定位、层级、背景色、动画过渡等遮罩层的样式
- wrapper（`semantic-mark-wrapper`）: 包裹层元素，一般用于动画容器，包含动画和过渡效果的样式
- container（`semantic-mark-container`）: Modal 容器元素，包含相对定位、背景色、背景裁剪、边框、圆角、阴影、指针事件、内边距等模态框主体样式
- header（`semantic-mark-header`）: 头部元素，包含头部内边距、下边框等头部区域样式
- title（`semantic-mark-title`）: 标题元素，包含外边距、颜色、字体权重、字体大小、行高、文字换行等标题文字样式
- body（`semantic-mark-body`）: 内容元素，包含内容区域的背景色、内边距等内容展示样式
- footer（`semantic-mark-footer`）: 底部元素，包含底部的背景色、内边距、上边框、圆角等底部区域样式
- close（`semantic-mark-close`）: 预览关闭按钮元素，设置按钮的基础样式

```tsx
<Modal
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    mask: "semantic-mark-mask",
    wrapper: "semantic-mark-wrapper",
    container: "semantic-mark-container",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    body: "semantic-mark-body",
    footer: "semantic-mark-footer",
    close: "semantic-mark-close"
  }}
/>
```
