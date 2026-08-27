export type OrderStatus =
  | 'pending'
  | 'paid'
  | 'shipped'
  | 'completed'
  | 'cancelled';

export interface Order {
  id: string;
  orderNo: string;
  amount: number;
  status: OrderStatus;
  createdAt: string;
  customerName: string;
}

export interface OrderListQuery {
  orderNo?: string;
  status?: OrderStatus;
  startTime?: string;
  endTime?: string;
  pageNo?: number;
  pageSize?: number;
}

export interface OrderListInfo {
  list: Order[];
  total: number;
  pageNo: number;
  pageSize: number;
}
