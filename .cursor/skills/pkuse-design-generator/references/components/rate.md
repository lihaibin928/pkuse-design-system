<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Rate 评分

- 分组：数据录入
- 组件文档：<https://ant.design/components/rate-cn.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## rate-cn`

用于对事物进行评分操作。

## 何时使用

- 对评价进行展示。
- 对事物进行快速的评级操作。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Rate } from 'antd';

const App: React.FC = () => <Rate />;

export default App;
```
