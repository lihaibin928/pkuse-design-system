<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Popconfirm 气泡确认框

- 分组：反馈
- 组件文档：<https://ant.design/components/popconfirm-cn.md>
- 语义文档：<https://ant.design/components/popconfirm-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## popconfirm-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `popconfirm-cn`

点击元素，弹出气泡式的确认框。

## 何时使用

目标元素的操作需要用户进一步的确认时，在目标元素附近弹出浮层提示，询问用户。

和 `confirm` 弹出的全屏居中模态对话框相比，交互形式更轻量。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { PopconfirmProps } from 'antd';
import { Button, message, Popconfirm } from 'antd';

const App: React.FC = () => {
  const [messageApi, holder] = message.useMessage();

  const confirm: PopconfirmProps['onConfirm'] = (e) => {
    console.log(e);
    messageApi.success('Click on Yes');
  };

  const cancel: PopconfirmProps['onCancel'] = (e) => {
    console.log(e);
    messageApi.error('Click on No');
  };

  return (
    <>
      {holder}
      <Popconfirm
        title="Delete the task"
        description="Are you sure to delete this task?"
        onConfirm={confirm}
        onCancel={cancel}
        okText="Yes"
        cancelText="No"
      >
        <Button danger>Delete</Button>
      </Popconfirm>
    </>
  );
};

export default App;
```

## 语义槽

### Popconfirm

- root（`semantic-mark-root`）: 根元素，设置绝对定位、层级、变换原点、箭头指向和弹层容器样式
- container（`semantic-mark-container`）: 容器元素，设置背景色、内边距、圆角、阴影、边框和内容展示样式
- icon（`semantic-mark-icon`）: 图标元素，设置确认图标的尺寸、颜色和布局样式
- arrow（`semantic-mark-arrow`）: 箭头元素，设置宽高、位置、颜色和边框样式
- title（`semantic-mark-title`）: 标题元素，设置标题文本样式和间距
- content（`semantic-mark-content`）: 描述元素，设置描述文本样式和布局

```tsx
<Popconfirm
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    container: "semantic-mark-container",
    icon: "semantic-mark-icon",
    arrow: "semantic-mark-arrow",
    title: "semantic-mark-title",
    content: "semantic-mark-content"
  }}
/>
```
