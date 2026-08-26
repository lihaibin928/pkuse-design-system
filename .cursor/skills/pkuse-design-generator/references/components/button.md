<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Button 按钮

- 分组：通用
- 组件文档：<https://ant.design/components/button-cn.md>
- 语义文档：<https://ant.design/components/button-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## button-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `button-cn`

按钮用于开始一个即时操作。

## 何时使用

标记了一个（或封装一组）操作命令，响应用户点击行为，触发相应的业务逻辑。

在 Ant Design 中我们提供了五种按钮。

- 🔵 主按钮：用于主行动点，一个操作区域只能有一个主按钮。
- ⚪️ 默认按钮：用于没有主次之分的一组行动点。
- 😶 虚线按钮：常用于添加操作。
- 🔤 文本按钮：用于最次级的行动点。
- 🔗 链接按钮：一般用于链接，即导航至某位置。

以及四种状态属性与上面配合使用。

- ⚠️ 危险：删除/移动/修改权限等危险操作，一般需要二次确认。
- 👻 幽灵：用于背景色比较复杂的地方，常用在首页/产品页等展示场景。
- 🚫 禁用：行动点不可用的时候，一般需要文案解释。
- 🔃 加载中：用于异步操作等待反馈的时候，也可以避免多次提交。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 同一个决策面只保留一个主按钮，其余降为 default / link / text。
- 危险操作用 `danger`，并配合 `Popconfirm` 或确认对话框。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Button, Flex } from 'antd';

const App: React.FC = () => (
  <Flex gap="small" wrap>
    <Button type="primary">Primary Button</Button>
    <Button>Default Button</Button>
    <Button type="dashed">Dashed Button</Button>
    <Button type="text">Text Button</Button>
    <Button type="link">Link Button</Button>
  </Flex>
);

export default App;
```

## 语义槽

### Button

- root（`semantic-mark-root`）: 根元素，包含边框样式、背景色、内边距、圆角、阴影效果、过渡动画、光标样式、文字权重、对齐方式等完整的按钮外观样式
- content（`semantic-mark-content`）: 内容元素，包装按钮文本内容，控制文本的不换行显示、居中对齐、中文字符间距优化等文本排版样式
- icon（`semantic-mark-icon`）: 图标元素，包含图标的字体大小、颜色继承、SVG 样式重置等图标显示相关样式

```tsx
<Button
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    content: "semantic-mark-content",
    icon: "semantic-mark-icon"
  }}
/>
```
