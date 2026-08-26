<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Splitter 分隔面板

- 分组：布局
- 组件文档：<https://ant.design/components/splitter-cn.md>
- 语义文档：<https://ant.design/components/splitter-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## splitter-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `splitter-cn`

自由切分指定区域

## 何时使用

- 可以水平或垂直地分隔区域。
- 当需要自由拖拽调整各区域大小。
- 当需要指定区域的最大最小宽高时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Flex, Splitter, Typography } from 'antd';

export const Desc: React.FC<Readonly<{ text?: string | number }>> = (props) => (
  <Flex justify="center" align="center" style={{ height: '100%' }}>
    <Typography.Title type="secondary" level={5} style={{ whiteSpace: 'nowrap' }}>
      {props.text}
    </Typography.Title>
  </Flex>
);

const App: React.FC = () => (
  <Splitter style={{ height: 200, boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
    <Splitter.Panel defaultSize="40%" min="20%" max="70%">
      <Desc text="First" />
    </Splitter.Panel>
    <Splitter.Panel>
      <Desc text="Second" />
    </Splitter.Panel>
  </Splitter>
);

export default App;
```

## 语义槽

### Splitter

- root（`semantic-mark-root`）: 根元素，设置flex布局、宽度高度、对齐方式和拉伸样式
- panel（`semantic-mark-panel`）: 面板元素，设置flex基础值、增长比例和面板容器样式
- dragger（`semantic-mark-dragger`）: 拖拽控制元素，设置绝对定位、用户选择、层级、居中对齐、背景色、悬停态和激活态样式

```tsx
<Splitter
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    panel: "semantic-mark-panel",
    dragger: "semantic-mark-dragger"
  }}
/>
```
