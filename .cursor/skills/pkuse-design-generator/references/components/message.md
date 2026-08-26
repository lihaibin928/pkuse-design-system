<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Message 全局提示

- 分组：反馈
- 组件文档：<https://ant.design/components/message-cn.md>
- 语义文档：<https://ant.design/components/message-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## message-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `message-cn`

全局展示操作反馈信息。

## 何时使用

- 可提供成功、警告和错误等反馈信息。
- 顶部居中显示并自动消失，是一种不打断用户操作的轻量级提示方式。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Button, message } from 'antd';

const App: React.FC = () => {
  const [messageApi, contextHolder] = message.useMessage();

  const info = () => {
    messageApi.info('Hello, Ant Design!');
  };

  return (
    <>
      {contextHolder}
      <Button type="primary" onClick={info}>
        Display normal message
      </Button>
    </>
  );
};

export default App;
```

## 语义槽

### Message

- list（`semantic-mark-list`）: 消息列表根元素，设置定位、层级、宽度、滚动区域和位置样式
- listContent（`semantic-mark-listContent`）: 消息列表内容元素，设置消息项排列、间距和高度动画样式
- root（`semantic-mark-root`）: 消息项根元素，设置背景色、圆角、阴影、内边距和动画样式
- wrapper（`semantic-mark-wrapper`）: 图标与标题的包裹元素，设置内容布局、间距和对齐样式
- icon（`semantic-mark-icon`）: 图标元素，设置字体大小、行高和状态颜色样式
- title（`semantic-mark-title`）: 标题元素，设置文本颜色、字号、行高和内容展示样式

```tsx
<Message
  {...otherProps}
  classNames={{
    list: "semantic-mark-list",
    listContent: "semantic-mark-listContent",
    root: "semantic-mark-root",
    wrapper: "semantic-mark-wrapper",
    icon: "semantic-mark-icon",
    title: "semantic-mark-title"
  }}
/>
```
