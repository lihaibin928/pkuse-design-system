import React from 'react';

import { PageContainer } from '@ant-design/pro-components';
import { useAccess } from '@umijs/max';
import { Form, Result } from 'antd';

import OrderSearchForm from '@/features/order/components/OrderSearchForm';
import OrderTable from '@/features/order/components/OrderTable';
import useOrderList from '@/features/order/hooks/useOrderList';

const OrderList: React.FC = () => {
  const [form] = Form.useForm();
  const access = useAccess();

  const { loading, orderListInfo, onPageChange, onSearch } = useOrderList({
    form,
  });

  if (!access.canViewOrder) {
    return <Result status="403" title="暂无权限" />;
  }

  return (
    <PageContainer title="订单管理">
      <OrderSearchForm form={form} onSearch={onSearch} />
      <OrderTable
        loading={loading}
        orderListInfo={orderListInfo}
        onPageChange={onPageChange}
      />
    </PageContainer>
  );
};

export default OrderList;
