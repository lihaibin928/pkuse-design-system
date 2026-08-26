<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Tour 漫游式引导

- 分组：数据展示
- 组件文档：<https://ant.design/components/tour-cn.md>
- 语义文档：<https://ant.design/components/tour-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## tour-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `tour-cn`

用于分步引导用户了解产品功能的气泡组件。

## 何时使用

常用于引导用户了解产品功能。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useRef, useState } from 'react';
import { EllipsisOutlined } from '@ant-design/icons';
import { Button, Divider, Space, Tour } from 'antd';
import type { TourProps } from 'antd';

const App: React.FC = () => {
  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);

  const [open, setOpen] = useState<boolean>(false);

  const steps: TourProps['steps'] = [
    {
      title: 'Upload File',
      description: 'Put your files here.',
      cover: (
        <img
          draggable={false}
          alt="tour.png"
          src="https://user-images.githubusercontent.com/5378891/197385811-55df8480-7ff4-44bd-9d43-a7dade598d70.png"
        />
      ),
      target: () => ref1.current,
    },
    {
      title: 'Save',
      description: 'Save your changes.',
      target: () => ref2.current,
    },
    {
      title: 'Other Actions',
      description: 'Click to see other actions.',
      target: () => ref3.current,
    },
  ];
  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>
        Begin Tour
      </Button>
      <Divider />
      <Space>
        <Button ref={ref1}>Upload</Button>
        <Button ref={ref2} type="primary">
          Save
        </Button>
        <Button ref={ref3} icon={<EllipsisOutlined />} />
      </Space>
      <Tour open={open} onClose={() => setOpen(false)} steps={steps} />
    </>
  );
};

export default App;
```

## 语义槽

### Tour

- root（`semantic-mark-root`）: 引导根容器，设置绝对定位、层级控制、最大宽度、可见性、箭头背景色变量、主题样式等容器样式
- cover（`semantic-mark-cover`）: 卡片封面区域，设置文本居中对齐、内边距、图片宽度等图片展示样式
- close（`semantic-mark-close`）: 关闭按钮元素，设置绝对定位、尺寸、颜色、悬浮态和交互反馈等关闭按钮样式
- section（`semantic-mark-section`）: 卡片主要内容区域，设置文本对齐、边框圆角、盒阴影、相对定位、背景色、边框、背景裁剪等卡片样式
- footer（`semantic-mark-footer`）: 卡片底部操作区域，设置内边距、文本右对齐、边框圆角、Flex布局等底部容器样式
- actions（`semantic-mark-actions`）: 操作按钮组容器，设置左侧自动外边距、按钮间距等按钮组布局样式
- indicator（`semantic-mark-indicator`）: 单个指示器元素，设置宽高尺寸、行内块显示、圆角、背景色、右外边距、激活状态等圆点样式
- indicators（`semantic-mark-indicators`）: 指示器组容器，设置行内块显示等指示器容器样式
- header（`semantic-mark-header`）: 卡片头部区域，设置内边距、宽度计算、词汇换行等头部容器样式
- title（`semantic-mark-title`）: 引导标题文字，设置字体粗细等标题文本样式
- description（`semantic-mark-description`）: 引导描述文字，设置内边距、词汇换行等描述文本样式
- mask（`semantic-mark-mask`）: 遮罩层元素，设置固定定位、全屏覆盖、层级、指针事件、过渡动画等遮罩样式

```tsx
<Tour
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    cover: "semantic-mark-cover",
    close: "semantic-mark-close",
    section: "semantic-mark-section",
    footer: "semantic-mark-footer",
    actions: "semantic-mark-actions",
    indicator: "semantic-mark-indicator",
    indicators: "semantic-mark-indicators",
    header: "semantic-mark-header",
    title: "semantic-mark-title",
    description: "semantic-mark-description",
    mask: "semantic-mark-mask"
  }}
/>
```
