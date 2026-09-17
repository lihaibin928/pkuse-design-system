<!-- 由 scripts/split_antd_docs.py 生成，抓取日期 2026-08-24。不要手改后当权威源。 -->

# Form 表单

- 分组：数据录入
- 组件文档：<https://ant.design/components/form-cn.md>
- 语义文档：<https://ant.design/components/form-cn/semantic.md>
- 全文快照：`../antd/llms-full-cn.txt` 中的 `## form-cn`
- 语义快照：`../antd/llms-semantic-cn.md` 中的 `form-cn`

高性能表单控件，自带数据域管理。包含数据录入、校验以及对应样式。

## 何时使用

- 用于创建一个实体或收集信息。
- 需要对输入的数据类型进行校验时。

## PKUSE

- 视觉与 Token 遵循 `references/design-system.md` 和 `references/ant-design-v6.zh.md`。
- 筛选条与编辑表单都用 `Form`，提交走类型化 Service。
- 校验失败定位到字段，保留已输入内容。
- 需要改外观时使用下面的语义槽 `classNames` / `styles`，不要写无前缀的 `.ant-*` 选择器。

## 基本示例

只保留官方第一个示例。更多 Demo 和完整 API 到全文快照中查阅。

```tsx
import React from 'react';
import type { FormProps } from 'antd';
import { Button, Checkbox, Form, Input } from 'antd';

type FieldType = {
  username?: string;
  password?: string;
  remember?: string;
};

const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
  console.log('Success:', values);
};

const onFinishFailed: FormProps<FieldType>['onFinishFailed'] = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

const App: React.FC = () => (
  <Form
    name="basic"
    labelCol={{ span: 8 }}
    wrapperCol={{ span: 16 }}
    style={{ maxWidth: 600 }}
    initialValues={{ remember: true }}
    onFinish={onFinish}
    onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <Form.Item<FieldType>
      label="Username"
      name="username"
      rules={[{ required: true, message: 'Please input your username!' }]}
    >
      <Input />
    </Form.Item>

    <Form.Item<FieldType>
      label="Password"
      name="password"
      rules={[{ required: true, message: 'Please input your password!' }]}
    >
      <Input.Password />
    </Form.Item>

    <Form.Item<FieldType> name="remember" valuePropName="checked" label={null}>
      <Checkbox>Remember me</Checkbox>
    </Form.Item>

    <Form.Item label={null}>
      <Button type="primary" htmlType="submit">
        Submit
      </Button>
    </Form.Item>
  </Form>
);

export default App;
```

## 语义槽

### Form

- root（`semantic-mark-root`）: 根元素，包含表单项的底边距、垂直对齐、过渡动画、隐藏状态、错误警告状态等表单项容器的基础样式
- label（`semantic-mark-label`）: 标签元素，包含 flex 布局、溢出隐藏、文本不换行、文本对齐、垂直对齐，以及标签的颜色、字体大小、高度、必填标记等标签显示样式
- content（`semantic-mark-content`）: 内容元素，包含表单内容区域的布局、样式和控件容器的相关样式
- help（`semantic-mark-help`）: 帮助信息容器元素，包含帮助文案与校验信息区域的间距、过渡与展示样式
- helpItem（`semantic-mark-helpItem`）: 帮助信息单项元素，包含错误、警告与提示文案的排版样式
- extra（`semantic-mark-extra`）: 额外提示容器元素，包含补充说明文案的间距、颜色与排版样式

```tsx
<Form
  {...otherProps}
  classNames={{
    root: "semantic-mark-root",
    label: "semantic-mark-label",
    content: "semantic-mark-content",
    help: "semantic-mark-help",
    helpItem: "semantic-mark-helpItem",
    extra: "semantic-mark-extra"
  }}
/>
```
