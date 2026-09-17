<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# QRCode 二维码

- 分组：数据展示
- 组件文档：<https://ant.design/components/qr-code-cn.md>
- 语义文档：<https://ant.design/components/qr-code-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## qr-code-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `qr-code-cn`

能够将文本转换生成二维码的组件，支持自定义配色和 Logo 配置。

## 何时使用

当需要将文本转换成为二维码时使用。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Input, QRCode, Space } from 'antd';

const App: React.FC = () => {
  const [text, setText] = React.useState('https://ant.design/');

  return (
    <Space vertical align="center">
      <QRCode value={text || '-'} />
      <Input
        placeholder="-"
        maxLength={60}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
    </Space>
  );
};

export default App;
```

## 语义槽

### QrCode

- root（`semantic-mark-root`）: 根元素，设置flex布局、内边距、背景色、边框、圆角和相对定位样式
- cover（`semantic-mark-cover`）: 遮罩层元素，设置绝对定位、层级、背景色和加载状态覆盖样式

```tsx
<QrCode
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    cover: "semantic-mark-cover"
  }}
/>
```
