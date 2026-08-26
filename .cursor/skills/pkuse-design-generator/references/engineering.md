# 工程规则

生成的子应用使用 Vite、React、TypeScript、Ant Design、React Router 和 pnpm。除非用户明确要求更换技术栈，否则遵循本目录结构和约束。

## 目录结构

```text
src/
├── app/             组合、Provider、主题
├── auth/            访问校验与权限声明
├── features/        业务切片；页面与组件、服务放在一起
├── micro-app/       qiankun 适配器与契约
├── mocks/           仅开发环境的适配器与夹具
├── routes/          同时供给路由和菜单的一份声明
├── services/        共享 HTTP 传输与契约
└── styles/          仅放带命名空间的全局基线
```

### 目录职责

| 路径 | 应包含 | 不得包含 |
| --- | --- | --- |
| `app/` | `App.tsx`、`ConfigProvider`、布局壳、错误边界包装 | 业务页面 |
| `auth/` | 权限常量、`canAccess` 辅助函数、路由守卫组件 | HTTP 调用 |
| `features/<slice>/` | `pages/`、`components/`、`services/`、`types/`、就近测试 | qiankun 生命周期代码 |
| `micro-app/` | 生命周期、props 适配、清理注册表 | 业务 UI |
| `mocks/` | Mock 适配器、夹具、本地角色预设 | 从生产页面反向导入 |
| `routes/` | 路由和侧栏共用的一份路由 / 菜单清单 | 重复的路由定义 |
| `services/` | `httpClient`、共享拦截器、基础错误类型 | 业务特有 DTO |
| `styles/` | 带命名空间的重置、CSS 变量挂钩 | 组件级样式（放在组件旁） |

## TypeScript

- `tsconfig.json` 开启 `strict: true`；除有明确文档的逃生口外禁止 `any`。
- 对象形状优先用 `interface`；联合类型和映射类型用 `type`。
- 领域类型从 `features/<slice>/types/` 导出。
- 服务契约是接口；适配器实现这些接口。
- 若 Vite 与 TS 已配置，允许路径别名 `@/` → `src/`。

## 服务层

页面和组件只依赖**类型化服务接口**，绝不依赖 Mock 模块。

```ts
// features/inventory/services/inventory.contract.ts
export interface InventoryService {
  listItems(params: ListParams, signal?: AbortSignal): Promise<PagedResult<Item>>;
  getItem(id: string, signal?: AbortSignal): Promise<Item>;
}

// features/inventory/services/inventory.api.ts — 生产适配器
// mocks/inventory.mock.ts — 开发适配器；仅在 app/bootstrap 中接线
```

注入方式：

```ts
// app/services.ts
export const services = {
  inventory: import.meta.env.DEV ? mockInventoryService : apiInventoryService,
} satisfies Record<string, unknown>;
```

每个异步服务方法接受可选的 `AbortSignal`。从 `useEffect` 清理和路由切换中传入该信号。

## HTTP 传输

共享客户端放在 `src/services/httpClient.ts`：

| 状态 | 行为 |
| --- | --- |
| 401 | 清除会话上下文；嵌入模式通过 `navigate('/login')` 跳转，独立运行走本地登录路由 |
| 403 | 抛出类型化 `ForbiddenError`；UI 展示无权限状态，不用通用 toast |
| 404 | 抛出类型化 `NotFoundError`；详情页渲染 Ant Design `Result` 404 |
| 5xx | 抛出类型化 `ServerError`；提供重试；有关联编号时记录 |
| 网络 | 抛出类型化 `NetworkError`；区分离线与超时 |

不要把 401 和 403 收成同一条文案。

## 错误边界

- 用应用级 Error Boundary（`app/ErrorBoundary.tsx`）包裹路由出口。
- 业务页可对高风险部件（图表、富文本编辑器）再加局部边界。
- 降级界面使用带重新加载操作的 Ant Design `Result`；开发环境记录错误元数据。

## RBAC

权限码只在 `src/auth/permissions.ts` 定义一次：

```ts
export const PERMISSIONS = {
  INVENTORY_VIEW: 'inventory:view',
  INVENTORY_EDIT: 'inventory:edit',
  INVENTORY_DELETE: 'inventory:delete',
} as const;

export type Permission = (typeof PERMISSIONS)[keyof typeof PERMISSIONS];
```

路由、菜单和操作校验都从同一组常量派生：

| 层级 | 规则 |
| --- | --- |
| 路由 | 清单项包含 `permissions: Permission[]`。缺少权限时守卫重定向到 `/403`。 |
| 菜单 | 用同一份清单生成菜单；用户无权访问的项不展示。 |
| 操作 | 按钮调用 `canAccess(PERMISSIONS.X)`；无权限时隐藏或禁用，并用 tooltip 说明。 |

独立运行模式至少在 `src/mocks/roles.ts` 提供两组 Mock 角色（例如 `admin`、`viewer`），用于验证权限差异。

会话与权限：

- **401** —— 会话过期或缺少 token；提供重新认证路径。
- **403** —— 已认证但权限不足；留在应用内并给出说明。

## 路由与菜单清单

唯一数据源在 `src/routes/manifest.ts`：

```ts
export interface AppRoute {
  path: string;
  title: string;
  permissions: Permission[];
  menu?: { icon: string; order: number };
  lazy: () => Promise<{ default: ComponentType }>;
}
```

路由和侧栏都导入这份清单；不要维护两套平行列表。

## Mock 规则

- Mock 适配器实现与 API 适配器相同的服务接口。
- 契约方法没有对应 Mock 处理时，抛出明确错误并点名缺失的处理函数——绝不默默返回空数组。
- `mocks/` 只通过动态导入或环境开关排除出生产包。

## 测试

- 业务测试就近放置：`features/<slice>/**/*.test.ts(x)`。
- 尽量在不挂载整个应用的情况下测试权限辅助函数和路由守卫。
- 用 `micro-app/lifecycle.test.ts` 对 qiankun 生命周期导出做最小挂载 / 卸载冒烟测试。

## 样式

- 通过 `ConfigProvider` 使用 Ant Design Token；见 `references/design-system.md`。
- 全局 CSS 放在 `src/styles/`，并带应用命名空间前缀。
- 不要使用会泄漏到主应用页面的无前缀元素选择器。

## 生成应用检查清单

- [ ] 严格 TypeScript 通过（`pnpm exec tsc --noEmit`）。
- [ ] 生产构建通过（`pnpm build`）。
- [ ] 页面导入的是服务，不是 Mock。
- [ ] 列表 / 详情请求已接入 AbortController。
- [ ] 401、403、404 和 5xx 路径彼此区分。
- [ ] 路由、菜单和操作共用 `PERMISSIONS` 常量。
- [ ] Error Boundary 包裹路由内容。
- [ ] qiankun 行为隔离在 `src/micro-app/` 下。
