import type { TableColumnsType } from 'antd';
import { Tag } from 'antd';

import { Order } from '../../types';

export const getOrderColumns = (): TableColumnsType<Order> => [
  {
    title: '订单号',
    dataIndex: 'orderNo',
    ellipsis: true,
  },
  {
    title: '客户名称',
    dataIndex: 'customerName',
  },
  {
    title: '金额',
    dataIndex: 'amount',
    render: (amount: number) => <span>¥{amount.toFixed(2)}</span>,
  },
  {
    title: '状态',
    dataIndex: 'status',
    render: (status: string) => {
      const statusMap: Record<string, { text: string; color: string }> = {
        pending: { text: '待支付', color: 'default' },
        paid: { text: '已支付', color: 'processing' },
        shipped: { text: '已发货', color: 'success' },
        completed: { text: '已完成', color: 'success' },
        cancelled: { text: '已取消', color: 'error' },
      };
      const { text, color } = statusMap[status] || {
        text: '未知',
        color: 'default',
      };
      return <Tag color={color}>{text}</Tag>;
    },
  },
  {
    title: '创建时间',
    dataIndex: 'createdAt',
    render: (text: string) => new Date(text).toLocaleString(),
  },
];
