<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Mentions 提及

- 分组：数据录入
- 组件文档：<https://ant.design/components/mentions-cn.md>
- 语义文档：<https://ant.design/components/mentions-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## mentions-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `mentions-cn`

用于在输入中提及某人或某事。

## 何时使用

用于在输入中提及某人或某事，常用于发布、聊天或评论功能。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Mentions } from 'antd';
import type { GetProp, MentionProps } from 'antd';

type MentionsOptionProps = GetProp<MentionProps, 'options'>[number];

const onChange = (value: string) => {
  console.log('Change:', value);
};

const onSelect = (option: MentionsOptionProps) => {
  console.log('select', option);
};

const App: React.FC = () => (
  <Mentions
    style={{ width: '100%' }}
    onChange={onChange}
    onSelect={onSelect}
    defaultValue="@afc163"
    options={[
      {
        value: 'afc163',
        label: 'afc163',
      },
      {
        value: 'zombieJ',
        label: 'zombieJ',
      },
      {
        value: 'yesmeck',
        label: 'yesmeck',
      },
    ]}
  />
);

export default App;
```

## 语义槽

### Mentions

- root（`semantic-mark-root`）: 根元素，设置行内flex布局、相对定位、内边距和边框样式
- textarea（`semantic-mark-textarea`）: 文本域元素，设置字体、行高、文本输入和背景样式
- popup（`semantic-mark-popup`）: 弹出框元素，设置绝对定位、层级、背景色、圆角、阴影和下拉选项样式
- suffix（`semantic-mark-suffix`）: 后缀元素，包含后缀内容的布局和样式，如清除按钮等

```tsx
<Mentions
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    textarea: "semantic-mark-textarea",
    popup: "semantic-mark-popup",
    suffix: "semantic-mark-suffix"
  }}
/>
```
