import { request } from '@umijs/max';

import { OrderListInfo, OrderListQuery } from '../types';

export async function fetchOrderList(
  params: OrderListQuery,
): Promise<OrderListInfo> {
  const res = await request<Api.Response<OrderListInfo>>('/api/orders', {
    method: 'GET',
    params,
  });

  return res.data;
}
