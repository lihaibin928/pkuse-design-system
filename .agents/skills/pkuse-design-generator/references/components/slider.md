<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Slider 滑动输入条

- 分组：数据录入
- 组件文档：<https://ant.design/components/slider-cn.md>
- 语义文档：<https://ant.design/components/slider-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## slider-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `slider-cn`

滑动型输入器，展示当前值和可选范围。

## 何时使用

当用户需要在数值区间/自定义区间内进行选择时，可为连续或离散值。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React, { useState } from 'react';
import { Slider, Switch } from 'antd';

const App: React.FC = () => {
  const [disabled, setDisabled] = useState(false);

  const onChange = (checked: boolean) => {
    setDisabled(checked);
  };

  return (
    <>
      <Slider defaultValue={30} disabled={disabled} />
      <Slider range defaultValue={[20, 50]} disabled={disabled} />
      Disabled: <Switch size="small" checked={disabled} onChange={onChange} />
    </>
  );
};

export default App;
```

## 语义槽

### Slider

- root（`semantic-mark-root`）: 根元素，设置相对定位、高度、边距、内边距、光标样式和触摸事件控制
- track（`semantic-mark-track`）: 轨道选取条元素，设置绝对定位、背景色、圆角和过渡动画样式
- tracks（`semantic-mark-tracks`）: 多段轨道容器元素，设置绝对定位和过渡动画样式
- rail（`semantic-mark-rail`）: 背景轨道元素，设置绝对定位、背景色、圆角和过渡动画样式
- handle（`semantic-mark-handle`）: 滑块控制点元素，设置绝对定位、尺寸、轮廓线、用户选择、背景色、边框阴影、圆角、光标样式和过渡动画

```tsx
<Slider
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    track: "semantic-mark-track",
    tracks: "semantic-mark-tracks",
    rail: "semantic-mark-rail",
    handle: "semantic-mark-handle"
  }}
/>
```
