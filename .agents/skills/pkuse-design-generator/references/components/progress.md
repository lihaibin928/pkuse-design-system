<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Progress 进度条

- 分组：反馈
- 组件文档：<https://ant.design/components/progress-cn.md>
- 语义文档：<https://ant.design/components/progress-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## progress-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `progress-cn`

展示操作的当前进度。

## 何时使用

在操作需要较长时间才能完成时，为用户显示该操作的当前进度和状态。

- 当一个操作会打断当前界面，或者需要在后台运行，且耗时可能超过 2 秒时；
- 当需要显示一个操作完成的百分比时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Flex, Progress } from 'antd';

const App: React.FC = () => (
  <Flex gap="small" vertical>
    <Progress percent={30} />
    <Progress percent={50} status="active" />
    <Progress percent={70} status="exception" />
    <Progress percent={100} />
    <Progress percent={50} showInfo={false} />
  </Flex>
);

export default App;
```

## 语义槽

### Progress

- root（`semantic-mark-root`）: 根元素，设置相对定位和基础容器样式
- body（`semantic-mark-body`）: 主体元素，设置进度条的布局和尺寸样式
- rail（`semantic-mark-rail`）: 导轨元素，设置背景轨道的颜色和圆角样式，steps 模式下没有该元素
- track（`semantic-mark-track`）: 轨迹元素，设置进度填充部分的颜色和过渡动画样式
- indicator（`semantic-mark-indicator`）: 指示器元素，设置百分比文本或图标的位置和字体样式

```tsx
<Progress
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    body: "semantic-mark-body",
    rail: "semantic-mark-rail",
    track: "semantic-mark-track",
    indicator: "semantic-mark-indicator"
  }}
/>
```
