<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Upload 上传

- 分组：数据录入
- 组件文档：<https://ant.design/components/upload-cn.md>
- 语义文档：<https://ant.design/components/upload-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## upload-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `upload-cn`

文件选择上传和拖拽上传控件。

## 何时使用

上传是将信息（网页、文字、图片、视频等）通过网页或者上传工具发布到远程服务器上的过程。

- 当需要上传一个或一些文件时。
- 当需要展现上传的进度时。
- 当需要使用拖拽交互时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import { UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { Button, message, Upload } from 'antd';

const App: React.FC = () => {
  const [messageApi, contextHolder] = message.useMessage();

  const props: UploadProps = {
    name: 'file',
    action: 'https://660d2bd96ddfa2943b33731c.mockapi.io/api/upload',
    headers: {
      authorization: 'authorization-text',
    },
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        messageApi.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        messageApi.error(`${info.file.name} file upload failed.`);
      }
    },
  };

  return (
    <>
      {contextHolder}
      <Upload {...props}>
        <Button icon={<UploadOutlined />}>Click to Upload</Button>
      </Upload>
    </>
  );
};

export default App;
```

## 语义槽

### Upload

- root（`semantic-mark-root`）: 根元素容器，包含布局样式、禁用状态文字颜色、用户选择控制、鼠标样式等基础样式
- list（`semantic-mark-list`）: 文件列表容器，包含布局排列、过渡动画、间距控制等样式
- item（`semantic-mark-item`）: 文件项元素，包含内边距、背景色、边框样式、悬停效果、状态颜色、过渡动画等样式
- trigger（`semantic-mark-trigger`）: 上传按钮容器，包含按钮样式、禁用状态、隐藏控制等样式

```tsx
<Upload
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    list: "semantic-mark-list",
    item: "semantic-mark-item",
    trigger: "semantic-mark-trigger"
  }}
/>
```
