const ORDER_STATUSES = [
  'pending',
  'paid',
  'shipped',
  'completed',
  'cancelled',
] as const;

const ORDERS = Array.from({ length: 50 }, (_, index) => {
  const id = index + 1;

  return {
    id: String(id),
    orderNo: `ORD${20260000 + id}`,
    amount: Number((((id * 137) % 10000) / 100).toFixed(2)),
    status: ORDER_STATUSES[index % ORDER_STATUSES.length],
    createdAt: new Date(
      Date.UTC(2026, 0, ((id - 1) % 28) + 1, 8, 0, 0),
    ).toISOString(),
    customerName: `客户${id}`,
  };
});

function toNumber(value: unknown, fallback: number) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function success(data: unknown) {
  return {
    code: 0,
    msg: 'success',
    data,
    success: true,
  };
}

export default {
  'GET /api/orders': (req: any, res: any) => {
    const pageNo = toNumber(req.query.pageNo, 1);
    const pageSize = toNumber(req.query.pageSize, 10);
    const orderNo = String(req.query.orderNo || '').trim();
    const status = String(req.query.status || '').trim();
    const startTime = String(req.query.startTime || '').trim();
    const endTime = String(req.query.endTime || '').trim();

    let list = ORDERS;

    if (orderNo) {
      list = list.filter((item) => item.orderNo.includes(orderNo));
    }

    if (status) {
      list = list.filter((item) => item.status === status);
    }

    if (startTime) {
      list = list.filter((item) => item.createdAt >= startTime);
    }

    if (endTime) {
      list = list.filter((item) => item.createdAt <= endTime);
    }

    const start = (pageNo - 1) * pageSize;

    setTimeout(() => {
      res.send(
        success({
          list: list.slice(start, start + pageSize),
          total: list.length,
          pageNo,
          pageSize,
        }),
      );
    }, 400);
  },
};
