import React from 'react';

import type { FormInstance } from 'antd';
import { Button, Card, Form, Input, Select, Space } from 'antd';

interface UserSearchFormProps {
  onSearch: () => void;
  form: FormInstance;
}

const UserSearchForm: React.FC<UserSearchFormProps> = ({ onSearch, form }) => {
  const onReset = () => {
    form.resetFields();
    onSearch();
  };

  const roleOptions = [
    { value: 'admin', label: '管理员' },
    { value: 'user', label: '普通用户' },
  ];

  return (
    <Card style={{ marginBottom: 16 }}>
      <Form form={form} layout="inline" onFinish={onSearch}>
        <Form.Item name="name" label="用户名">
          <Input placeholder="请输入" allowClear />
        </Form.Item>
        <Form.Item name="role" label="角色">
          <Select allowClear style={{ width: 120 }} options={roleOptions} />
        </Form.Item>
        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit">
              查询
            </Button>
            <Button onClick={onReset}>重置</Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default UserSearchForm;
