const USERS = Array.from({ length: 128 }, (_, index) => {
  const id = index + 1;

  return {
    id,
    name: `用户${id}`,
    role: id % 2 === 0 ? 'admin' : 'user',
    status: id % 2 === 0 ? 1 : 0,
    createdAt: '2025-01-01',
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
  'GET /api/users': (req: any, res: any) => {
    const pageNo = toNumber(req.query.pageNo, 1);
    const pageSize = toNumber(req.query.pageSize, 10);
    const name = String(req.query.name || '').trim();
    const role = String(req.query.role || '').trim();

    let list = USERS;

    if (name) {
      list = list.filter((item) => item.name.includes(name));
    }

    if (role) {
      list = list.filter((item) => item.role === role);
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

  'GET /api/users/:id': (req: any, res: any) => {
    const id = toNumber(req.params.id, 0);
    const user = USERS.find((item) => item.id === id);

    if (!user) {
      res.status(404).send({
        code: 404,
        msg: '用户不存在',
        data: null,
        success: false,
      });
      return;
    }

    res.send(success(user));
  },

  'POST /api/users': (req: any, res: any) => {
    const payload = req.body || {};
    const nextId = USERS.length
      ? Math.max(...USERS.map((item) => item.id)) + 1
      : 1;
    const user = {
      id: nextId,
      name: payload.name || `用户${nextId}`,
      role: payload.role === 'admin' ? 'admin' : 'user',
      status: 1,
      createdAt: '2025-01-01',
    };

    USERS.unshift(user);
    res.send(success(user));
  },

  'PUT /api/users/:id': (req: any, res: any) => {
    const id = toNumber(req.params.id, 0);
    const index = USERS.findIndex((item) => item.id === id);

    if (index === -1) {
      res.status(404).send({
        code: 404,
        msg: '用户不存在',
        data: null,
        success: false,
      });
      return;
    }

    USERS[index] = {
      ...USERS[index],
      ...req.body,
      id,
    };

    res.send(success(USERS[index]));
  },
};
