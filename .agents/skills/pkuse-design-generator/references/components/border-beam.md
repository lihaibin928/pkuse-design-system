<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# BorderBeam 边框流光

- 分组：其他
- 组件文档：<https://ant.design/components/border-beam-cn.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## border-beam-cn`

为容器边框提供持续流动的装饰性高亮效果。

## 何时使用

- 需要强化某个容器的视觉关注度，但又不希望引入业务状态语义时。
- 适合登录面板、推荐卡片、AI 模块、重点 CTA 区域等场景。
- 它是装饰性效果，不应替代焦点态、校验态或业务状态边框。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { BorderBeam, Card } from 'antd';

const App: React.FC = () => (
  <div style={{ width: 360 }}>
    <BorderBeam>
      <Card title="Workspace overview">
        Review task status, deployment health, and recent automation activity in one panel.
      </Card>
    </BorderBeam>
  </div>
);

export default App;
```
