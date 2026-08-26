<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Badge 徽标数

- 分组：数据展示
- 组件文档：<https://ant.design/components/badge-cn.md>
- 语义文档：<https://ant.design/components/badge-cn/semantic_ribbon.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## badge-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `badge-cn`

图标右上角的圆形徽标数字。

## 何时使用

一般出现在通知图标或头像的右上角，用于显示需要处理的消息条数，通过醒目视觉形式吸引用户处理。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 状态点不能在无障碍关键流程里代替文字。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { ClockCircleOutlined } from '@ant-design/icons';
import { Avatar, Badge, Space } from 'antd';

const App: React.FC = () => (
  <Space size="medium">
    <Badge count={5}>
      <Avatar shape="square" size="large" />
    </Badge>
    <Badge count={0} showZero>
      <Avatar shape="square" size="large" />
    </Badge>
    <Badge count={<ClockCircleOutlined style={{ color: '#f5222d' }} />}>
      <Avatar shape="square" size="large" />
    </Badge>
  </Space>
);

export default App;
```

## 语义槽

### Badge.Ribbon

- root（`semantic-mark-root`）: 根元素，设置相对定位和包装容器样式
- indicator（`semantic-mark-indicator`）: 指示器元素，设置绝对定位、内边距、背景色、圆角和缎带样式
- content（`semantic-mark-content`）: 文本元素，设置文本颜色和缎带内容显示样式

```tsx
<Badge.Ribbon
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    indicator: "semantic-mark-indicator",
    content: "semantic-mark-content"
  }}
/>
```

### Badge

- root（`semantic-mark-root`）: 根元素，包含相对定位、行内块布局、适应内容宽度等基础布局样式
- indicator（`semantic-mark-indicator`）: 指示器元素，包含定位、层级、尺寸、颜色、字体、文本对齐、背景、圆角、阴影、过渡动画等完整的徽标样式

```tsx
<Badge
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    indicator: "semantic-mark-indicator"
  }}
/>
```
