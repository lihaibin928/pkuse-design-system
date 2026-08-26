<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Notification 通知提醒框

- 分组：反馈
- 组件文档：<https://ant.design/components/notification-cn.md>
- 语义文档：<https://ant.design/components/notification-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## notification-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `notification-cn`

全局展示通知提醒信息。

## 何时使用

在系统四个角显示通知提醒信息。经常用于以下情况：

- 较为复杂的通知内容。
- 带有交互的通知，给出用户下一步的行动点。
- 系统主动推送。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useMemo } from 'react';
import {
  RadiusBottomleftOutlined,
  RadiusBottomrightOutlined,
  RadiusUpleftOutlined,
  RadiusUprightOutlined,
} from '@ant-design/icons';
import { Button, Divider, notification, Space } from 'antd';
import type { NotificationArgsProps } from 'antd';

type NotificationPlacement = NotificationArgsProps['placement'];

const Context = React.createContext({ name: 'Default' });

const App: React.FC = () => {
  const [api, contextHolder] = notification.useNotification();

  const openNotification = (placement: NotificationPlacement) => {
    api.info({
      title: `Notification ${placement}`,
      description: <Context.Consumer>{({ name }) => `Hello, ${name}!`}</Context.Consumer>,
      placement,
    });
  };

  const contextValue = useMemo(() => ({ name: 'Ant Design' }), []);

  return (
    <Context.Provider value={contextValue}>
      {contextHolder}
      <Space>
        <Button
          type="primary"
          onClick={() => openNotification('topLeft')}
          icon={<RadiusUpleftOutlined />}
        >
          topLeft
        </Button>
        <Button
          type="primary"
          onClick={() => openNotification('topRight')}
          icon={<RadiusUprightOutlined />}
        >
          topRight
        </Button>
      </Space>
      <Divider />
      <Space>
        <Button
          type="primary"
          onClick={() => openNotification('bottomLeft')}
          icon={<RadiusBottomleftOutlined />}
        >
          bottomLeft
        </Button>
        <Button
          type="primary"
          onClick={() => openNotification('bottomRight')}
          icon={<RadiusBottomrightOutlined />}
        >
          bottomRight
        </Button>
      </Space>
    </Context.Provider>
  );
};

export default App;
```

## 语义槽

### Notification

- list（`semantic-mark-list`）: 通知列表根元素，设置定位、层级、宽度、滚动区域和位置样式
- listContent（`semantic-mark-listContent`）: 通知列表内容元素，设置通知项排列、间距和高度动画样式
- root（`semantic-mark-root`）: 通知项根元素，设置背景色、圆角、阴影、内边距和动画样式
- wrapper（`semantic-mark-wrapper`）: 图标与内容的包裹元素，设置内容布局样式
- icon（`semantic-mark-icon`）: 图标元素，设置绝对定位、字体大小、行高和状态颜色样式
- section（`semantic-mark-section`）: 内容区域元素，包含标题和描述内容
- title（`semantic-mark-title`）: 标题元素，设置颜色、字体大小、行高和外边距样式
- description（`semantic-mark-description`）: 描述元素，设置字体大小、颜色和外边距样式
- actions（`semantic-mark-actions`）: 操作组元素，设置右浮动、上边距和操作按钮布局样式
- close（`semantic-mark-close`）: 关闭按钮元素，设置位置、尺寸和交互样式
- progress（`semantic-mark-progress`）: 进度条元素，设置自动关闭通知的进度样式

```tsx
<Notification
  {...otherProps}
  classNames={{
    list: "semantic-mark-list",
    listContent: "semantic-mark-listContent",
    root: "semantic-mark-root",
    wrapper: "semantic-mark-wrapper",
    icon: "semantic-mark-icon",
    section: "semantic-mark-section",
    title: "semantic-mark-title",
    description: "semantic-mark-description",
    actions: "semantic-mark-actions",
    close: "semantic-mark-close",
    progress: "semantic-mark-progress"
  }}
/>
```
