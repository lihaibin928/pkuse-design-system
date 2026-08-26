<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Alert 警告提示

- 分组：反馈
- 组件文档：<https://ant.design/components/alert-cn.md>
- 语义文档：<https://ant.design/components/alert-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## alert-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `alert-cn`

警告提示，展现需要关注的信息。

## 何时使用

- 当某个页面需要向用户显示警告的信息时。
- 非浮层的静态展现形式，始终展现，不会自动消失，用户可以点击关闭。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 用语义类型表达状态，不要把整页做成成功绿。
- 关键状态用 Alert / Result，不要只用 Tag。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Alert } from 'antd';

const App: React.FC = () => <Alert title="Success Text" type="success" />;

export default App;
```

## 语义槽

### Alert

- root（`semantic-mark-root`）: 根元素，包含边框、背景色、内边距、圆角、位置布局等警告提示框的基础样式
- section（`semantic-mark-section`）: 内容元素，采用 flex 布局控制内容区域的排版和最小宽度
- icon（`semantic-mark-icon`）: 图标元素，包含图标的颜色、行高、外边距等样式，支持不同类型的状态图标
- title（`semantic-mark-title`）: 标题元素，包含标题文字的颜色、字体等样式
- description（`semantic-mark-description`）: 描述元素，包含描述文字的字体大小、行高等排版样式
- actions（`semantic-mark-actions`）: 操作组元素，包含操作按钮的布局和间距样式
- close（`semantic-mark-close`）: 关闭按钮元素，包含按钮的基础样式

```tsx
<Alert
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    section: "semantic-mark-section",
    icon: "semantic-mark-icon",
    title: "semantic-mark-title",
    description: "semantic-mark-description",
    actions: "semantic-mark-actions",
    close: "semantic-mark-close"
  }}
/>
```
