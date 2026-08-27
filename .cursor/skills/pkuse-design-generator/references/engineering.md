# 工程规则

生成的子应用以 `project-struct-react/` 为工程结构基准，使用 **Umi Max**、TypeScript、Ant Design、Ant Design Pro Components。除非用户明确要求更换技术栈，否则遵循本目录和约束。视觉 Token 与组件选用仍遵循 `references/design-system.md`。

## 技术栈

| 类别 | 选型 |
| --- | --- |
| 框架 | Umi Max 4（`@umijs/max`） |
| UI | Ant Design 6 · Ant Design Pro Components |
| 语言 | TypeScript（`strict`） |
| 样式 | Less（组件旁）· Tailwind CSS（工具类） |
| 包管理 | 与 `.umirc.ts` 的 `npmClient` 保持一致（当前为 `yarn`） |
| 工程化 | Husky · lint-staged · Prettier · ESLint · Stylelint |
| 路由 | Hash 路由（`hash: true`），路由表写在 `src/router/routes.ts` |

本地开发：`yarn install` 后 `yarn dev`（`http://localhost:8000`）。生产构建：`yarn build`，产物在 `dist/`。

## 目录结构

```text
.
├── mock/                    开发环境接口 Mock（Umi Mock 插件）
├── src/
│   ├── access.ts            权限定义（Umi access 插件唯一入口）
│   ├── app.ts               运行时配置：getInitialState、layout、request
│   ├── router/
│   │   └── routes.ts        路由 / 菜单唯一清单
│   ├── utils/
│   │   └── request.ts       HTTP 拦截与错误处理
│   ├── types/
│   │   ├── api.d.ts         接口通用类型（Api.Response）
│   │   └── app.d.ts         应用全局类型（App.InitialState）
│   ├── constants/           全局常量（非业务域）
│   ├── assets/              静态资源
│   ├── components/          跨业务域通用组件
│   ├── pages/               路由页面（薄层，只组装 feature）
│   └── features/            业务模块
│       ├── shared/          跨 feature 共享（constants、hooks、utils、components）
│       └── <slice>/
│           ├── types.ts
│           ├── services/
│           ├── hooks/
│           └── components/
├── .umirc.ts                Umi 构建配置（引入 routes、antd、access、mock、proxy）
├── tailwind.config.js
└── tailwind.css
```

### 目录职责

| 路径 | 应包含 | 不得包含 |
| --- | --- | --- |
| `src/app.ts` | `getInitialState`、`layout`、导出 `request` | 业务 UI、领域 Service |
| `src/access.ts` | 由 `InitialState` 派生的权限开关 | HTTP 调用、页面组件 |
| `src/router/routes.ts` | 路由、菜单名、图标、`hideInMenu`、`access` | 第二套平行路由表 |
| `src/utils/request.ts` | 全局请求配置、业务码与 HTTP 错误处理 | 领域 DTO、页面逻辑 |
| `src/types/` | `Api`、`App` 等全局命名空间 | 业务实体类型（放 feature `types.ts`） |
| `src/components/` | 跨模块壳层组件（如 Guide） | 某业务域专用表格 / 表单 |
| `src/pages/<Domain>/` | `PageContainer`、组装 SearchForm / Table / Modal、调用 hooks | 直接 `request`、直接读 `mock/` |
| `src/features/<slice>/` | `types.ts`、`services/`、`hooks/`、`components/` | 路由注册、qiankun / layout 配置 |
| `src/features/shared/` | 分页默认值、通用 hooks、跨域工具 | 某个域的 DTO 或 API |
| `mock/` | `'METHOD /path'` 处理器，返回 `Api.Response` | 被 `src/pages` 或 `src/features` 静态导入 |

### 分层职责

```text
pages（路由入口）
  └── 组装 PageContainer、Form、Spin，调用 hooks

features（业务域）
  ├── types.ts      领域模型与查询 / 列表类型
  ├── services/     调用 request，返回领域 data
  ├── hooks/        列表分页、详情加载、弹窗提交等业务状态
  └── components/   SearchForm、Table（含 _columns）、Modal、Card 等展示组件
```

页面保持薄封装：不在 `pages/` 里写列定义、接口拼接或弹窗提交逻辑。

## 新增业务模块

以 `product` 为例：

1. 在 `src/features/product/` 下创建 `types.ts`、`services/`、`hooks/`、`components/`。
2. 在 `src/pages/Product/ProductList/`（及需要的详情页）创建页面入口。
3. 在 `src/router/routes.ts` 注册路由（详情页设 `hideInMenu: true`）。
4. 开发阶段在 `mock/` 增加对应接口。

Feature 内推荐命名：

| 层 | 约定 |
| --- | --- |
| Service | 具名导出 `fetchXxxList` / `fetchXxxDetail` / `updateXxx`，从 `services/index.ts` 再导出 |
| Hook | `useXxxList`、`useXxxDetail`、`useXxxEdit`；列表 hook 接收 `form`，返回 `loading`、数据、`onSearch`、`onPageChange` |
| 组件 | `XxxSearchForm`、`XxxTable`（列定义放 `_columns.tsx`）、`XxxEditModal`、`XxxDetailCard` |
| 类型 | `Xxx`、`XxxListQuery`、`XxxListInfo`（含 `list` / `total` / `pageNo` / `pageSize`） |

分页默认值使用 `@/features/shared/constants` 的 `DEFAULT_PAGINATION_PARAMS`，不要在各 feature 重复字面量。

## TypeScript

- 沿用 Umi 生成的 `tsconfig`（根目录 `tsconfig.json` extends `src/.umi/tsconfig.json`）；除有明确文档的逃生口外禁止 `any`。
- 对象形状优先用 `interface`；联合类型和映射类型用 `type`。
- 领域类型从 `src/features/<slice>/types.ts` 导出。
- 接口响应一律包在全局 `Api.Response<T>` 中；应用状态用 `App.InitialState`，与 `getInitialState`、`access.ts` 保持一致。
- 路径别名 `@/` → `src/`。

```ts
// src/types/api.d.ts
declare namespace Api {
  interface Response<T = undefined> {
    code: number;
    message?: string;
    msg?: string;
    data: T;
    success?: boolean;
  }
}

// src/types/app.d.ts
declare namespace App {
  interface InitialState {
    name: string;
  }
}
```

## 服务层

页面和组件只通过 **feature hooks / services** 取数，绝不导入 `mock/`。

```ts
// features/user/services/index.ts
import { request } from '@umijs/max';
import type { UserListInfo, UserListQuery } from '../types';

export async function fetchUserList(
  params: UserListQuery,
): Promise<UserListInfo> {
  const res = await request<Api.Response<UserListInfo>>('/api/users', {
    method: 'GET',
    params,
  });
  return res.data;
}
```

- Service 只负责请求与拆包 `data`，不持有 React 状态。
- Hook 负责 `loading`、分页、表单查询值和刷新；列表首次加载可跳过表单值。
- 生产环境通过 `.umirc.ts` 的 `proxy` 转发真实后端；不要在页面里切换 Mock 模块。

## HTTP 传输

共享客户端写在 `src/utils/request.ts`，由 `src/app.ts` 再导出给 Umi `request` 插件。成功码视为 `code ∈ {0, 200}`，或显式 `success: true`。

| 状态 | 行为 |
| --- | --- |
| HTTP 401 或业务会话过期码（如 `100000`） | 跳转 `/login`；不要当成权限不足 |
| HTTP 403 | 提示「暂无访问权限」；已登录用户留在应用内 |
| HTTP 404 | 资源不存在；详情页用 Ant Design `Result` 404，不要只 toast |
| HTTP 5xx | 提示服务异常 / 超时，允许重试 |
| 网络断开或无响应 | 提示检查网络，与 5xx 区分 |
| 业务失败（`success === false` 或非成功 `code`） | 抛出 `BizError`，用接口 `message` / `msg` |

不要把 401 和 403 收成同一条文案。拦截器已处理的错误，页面不要再弹一遍相同 toast。

## 运行时与布局

`src/app.ts` 是运行时唯一入口：

- `getInitialState` 提供用户身份，供 layout 与 `access.ts` 使用。
- `layout`：开发环境渲染 Pro Layout 侧栏，便于独立调试；**生产环境**设置 `menuRender: false`、`menuHeaderRender: false`，避免与 qiankun 主应用导航重复。
- 导出 `request`，不要在别处再配一套拦截器。

微前端生命周期与主应用 props 的协议见 `references/qiankun-contract.md`。业务 feature 与 pages **不得**直接导入 qiankun API，也不得在组件里判断 `__POWERED_BY_QIANKUN__`。

## RBAC

权限开关只在 `src/access.ts` 定义一次，从 `App.InitialState` 派生：

```ts
export default (initialState: App.InitialState) => {
  return {
    canSeeAdmin: !!(initialState && initialState.name !== 'dontHaveAccess'),
    canViewUser: true,
    canEditUser: true,
  };
};
```

路由、菜单和操作都使用这些字段，不要在页面里写散落的角色字符串。

| 层级 | 规则 |
| --- | --- |
| 路由 | `src/router/routes.ts` 的项可设 `access: 'canViewUser'`；无权限时由 Umi access 插件拦截。 |
| 菜单 | 同一份路由表生成菜单；`hideInMenu: true` 的详情 / 编辑页不出现在侧栏。无权限的项不展示。 |
| 操作 | 使用 `useAccess()` 与 `<Access accessible={access.canEditUser}>`；无权限时隐藏或禁用，并用 tooltip 说明。 |

权限码与 `references/page-patterns.md` 中的 `<entity>:<action>` 对齐时，在 `access.ts` 映射为稳定的 camelCase 开关（例如 `user:edit` → `canEditUser`），只维护这一处映射。

## 路由与菜单清单

唯一数据源是 `src/router/routes.ts`，由 `.umirc.ts` 的 `routes` 引入：

```ts
export default [
  { path: '/', redirect: '/home' },
  {
    name: '用户列表',
    path: '/user/list',
    component: './User/UserList',
    icon: 'UserOutlined',
    access: 'canViewUser',
  },
  {
    name: '用户详情',
    path: '/user/detail',
    component: './User/UserDetail',
    hideInMenu: true,
  },
];
```

- `component` 相对 `src/pages/`（Umi 约定 `./User/UserList` → `src/pages/User/UserList`）。
- 路由和侧栏都来自这份清单；不要在 `app.ts` 或页面里再维护一套菜单。
- 站内跳转用 `history`（`umi` / `@umijs/max`），查询参数用 `useSearchParams`。

## Mock 规则

- Mock 放在仓库根目录 `mock/`，按 Umi 约定导出 `'GET /api/users'` 等形式的处理器。
- 响应必须是 `Api.Response`：`{ code, msg, data, success }`。列表需支持分页与筛选查询参数。
- 资源不存在时返回 HTTP 404 且 `success: false`，不要默默给空对象。
- `src/` 下的业务代码不得静态导入 `mock/`；开发时由 Umi Mock 插件拦截 `/api/*`。
- 接入真实后端时在 `.umirc.ts` 配置 `proxy`，而不是删掉 Service。

## 测试

- 业务测试就近放置：`src/features/<slice>/**/*.test.ts(x)`。
- 优先测 hooks 与 `access.ts` 的权限派生，不必为了断言权限去挂载整棵 layout。
- 请求错误分支以 `src/utils/request.ts` 为单测重点（401 / 403 / 业务码）。

## 样式

- 通过 Umi `antd` 插件与 `ConfigProvider` 使用 Ant Design Token；见 `references/design-system.md`。
- 页面级容器优先用 Pro Components 的 `PageContainer`。
- 组件私有样式用同目录 Less；工具类用 Tailwind。
- 不要使用会泄漏到主应用页面的无前缀元素选择器。

## 代码规范

- `pre-commit`：lint-staged 跑 ESLint / Stylelint 与 Prettier。
- `commit-msg`：`max verify-commit` 校验提交说明。
- 手动格式化：`yarn format`。

## 生成应用检查清单

- [ ] TypeScript 可通过（Umi / `tsc` 无新增 `any`）。
- [ ] 生产构建通过（`yarn build`）。
- [ ] `pages/` 只组装 feature，不直接 `request`、不导入 `mock/`。
- [ ] 每个业务域具备 `types` / `services` / `hooks` / `components`。
- [ ] HTTP 错误集中在 `src/utils/request.ts`；401 与 403 文案分离。
- [ ] 路由、菜单和操作共用 `src/access.ts` 与 `src/router/routes.ts`。
- [ ] 开发环境有侧栏，生产环境隐藏菜单，交由主应用导航。
- [ ] 详情页 404 使用 `Result`，列表空数据与 loading 有明确状态。
