import React from 'react';

import type { FormInstance } from 'antd';
import { Button, Card, Form, Input, Select, Space } from 'antd';

interface OrderSearchFormProps {
  form: FormInstance;
  onSearch: () => void;
}

const OrderSearchForm: React.FC<OrderSearchFormProps> = ({
  form,
  onSearch,
}) => {
  return (
    <Card className="mb-4">
      <Form
        form={form}
        layout="inline"
        onFinish={onSearch}
        initialValues={{ status: undefined }}
      >
        <Form.Item name="orderNo" label="订单号">
          <Input placeholder="请输入订单号" allowClear />
        </Form.Item>
        <Form.Item name="status" label="状态">
          <Select
            placeholder="请选择状态"
            allowClear
            style={{ width: 120 }}
            options={[
              { value: 'pending', label: '待支付' },
              { value: 'paid', label: '已支付' },
              { value: 'shipped', label: '已发货' },
              { value: 'completed', label: '已完成' },
              { value: 'cancelled', label: '已取消' },
            ]}
          />
        </Form.Item>
        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit">
              查询
            </Button>
            <Button
              onClick={() => {
                form.resetFields();
                onSearch();
              }}
            >
              重置
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default OrderSearchForm;
