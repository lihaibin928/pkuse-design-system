import React from 'react';

import { Card, Empty, Table } from 'antd';

import { DEFAULT_PAGINATION_PARAMS } from '@/features/shared/constants';
import { Order, OrderListInfo } from '../../types';
import { getOrderColumns } from './_columns';

interface OrderTableProps {
  orderListInfo?: OrderListInfo;
  loading?: boolean;
  onPageChange: (pageNo: number, pageSize: number) => void;
}

const OrderTable: React.FC<OrderTableProps> = ({
  orderListInfo,
  loading,
  onPageChange,
}) => {
  return (
    <Card title="订单列表" className="mt-4">
      <Table<Order>
        columns={getOrderColumns()}
        dataSource={orderListInfo?.list}
        rowKey="id"
        loading={loading}
        locale={{ emptyText: <Empty description="暂无数据" /> }}
        pagination={{
          current: orderListInfo?.pageNo || DEFAULT_PAGINATION_PARAMS.pageNo,
          pageSize:
            orderListInfo?.pageSize || DEFAULT_PAGINATION_PARAMS.pageSize,
          total: orderListInfo?.total,
          onChange: onPageChange,
          showSizeChanger: true,
        }}
      />
    </Card>
  );
};

export default OrderTable;
