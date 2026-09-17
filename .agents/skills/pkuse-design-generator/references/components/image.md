<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Image 图片

- 分组：数据展示
- 组件文档：<https://ant.design/components/image-cn.md>
- 语义文档：<https://ant.design/components/image-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## image-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `image-cn`

可预览的图片。

## 何时使用

- 需要展示图片时使用。
- 加载显示大图或加载失败时容错处理。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { Image } from 'antd';

const App: React.FC = () => (
  <Image
    width={200}
    alt="basic"
    src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
  />
);

export default App;
```

## 语义槽

### Image

- root（`semantic-mark-root`）: 根元素，设置相对定位和行内块布局样式
- image（`semantic-mark-image`）: 图片元素，设置宽度、高度和垂直对齐样式
- cover（`semantic-mark-cover`）: 悬浮图片显示的提示元素，设置绝对定位、背景色、透明度和过渡动画样式
- popup.root（`semantic-mark-popup-root`）: 预览根元素，设置固定定位、层级和背景遮罩样式
- popup.mask（`semantic-mark-popup-mask`）: 预览遮罩元素，设置绝对定位和半透明背景样式
- popup.body（`semantic-mark-popup-body`）: 预览内容元素，设置flex布局、居中对齐和指针事件样式
- popup.footer（`semantic-mark-popup-footer`）: 预览页脚元素，设置绝对定位、居中布局和底部操作区域样式
- popup.actions（`semantic-mark-popup-actions`）: 预览操作组元素，设置flex布局、背景色、圆角和操作按钮样式
- popup.close（`semantic-mark-popup-close`）: 预览关闭按钮元素，设置按钮的基础样式

```tsx
<Image
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    image: "semantic-mark-image",
    cover: "semantic-mark-cover",
    popup.root: "semantic-mark-popup-root",
    popup.mask: "semantic-mark-popup-mask",
    popup.body: "semantic-mark-popup-body",
    popup.footer: "semantic-mark-popup-footer",
    popup.actions: "semantic-mark-popup-actions",
    popup.close: "semantic-mark-popup-close"
  }}
/>
```
