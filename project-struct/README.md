# PKUSE Design System

基于 **Umi Max** 的企业级后台管理子应用模板，采用 Feature 模块化架构，内置用户管理、订单管理等示例页面，并针对 **qiankun 微前端** 子应用场景做了布局适配。

## 技术栈

| 类别 | 技术 |
| --- | --- |
| 框架 | [Umi Max 4](https://umijs.org/docs/max/introduce) |
| UI | [Ant Design 5](https://ant.design/) · [Ant Design Pro Components](https://procomponents.ant.design/) |
| 语言 | TypeScript 5 |
| 样式 | Less · [Tailwind CSS 3](https://tailwindcss.com/) |
| 工程化 | Husky · lint-staged · Prettier · ESLint · Stylelint |

## 功能特性

- **Feature 模块化**：按业务域拆分 `types` / `services` / `hooks` / `components`，页面层保持薄封装
- **统一请求层**：全局 `request` 拦截器，统一 HTTP 与业务错误处理
- **权限体系**：集成 Umi `access` 插件，支持基于初始状态的权限控制
- **Mock 数据**：开发环境内置用户、订单接口 Mock，开箱即用
- **微前端友好**：生产环境自动隐藏侧边栏，由主应用统一导航
- **Hash 路由**：启用 `hash: true`，便于子应用独立部署与嵌入

## 快速开始

### 环境要求

- Node.js >= 18
- npm / yarn / pnpm（项目配置默认使用 yarn）

### 安装依赖

```bash
yarn install
# 或
npm install
```

### 本地开发

```bash
yarn dev
# 或
npm start
```

启动后访问 [http://localhost:8000](http://localhost:8000)。

### 构建生产包

```bash
yarn build
```

产物输出至 `dist/` 目录。

### 代码格式化

```bash
yarn format
```

## 路由说明

| 路径                   | 页面     | 菜单可见 |
| ---------------------- | -------- | -------- |
| `/home`                | 首页     | 是       |
| `/access`              | 权限演示 | 是       |
| `/order/list`          | 订单列表 | 是       |
| `/user/list`           | 用户列表 | 是       |
| `/user/detail?id={id}` | 用户详情 | 否       |

路由配置位于 [`src/router/routes.ts`](src/router/routes.ts)。

## 项目结构

```
.
├── mock/                    # 开发 Mock 接口
│   ├── user.ts
│   └── order.ts
├── src/
│   ├── access.ts            # 权限定义
│   ├── app.ts               # 运行时配置（layout、initialState、request）
│   ├── router/
│   │   └── routes.ts        # 路由表
│   ├── utils/
│   │   └── request.ts       # HTTP 拦截与错误处理
│   ├── types/
│   │   ├── api.d.ts         # 接口通用类型（Api.Response）
│   │   └── app.d.ts         # 应用全局类型（App.InitialState）
│   ├── components/          # 跨模块通用组件
│   ├── pages/               # 路由页面（薄层，负责组装 feature）
│   │   ├── Home/
│   │   ├── Access/
│   │   ├── Order/OrderList/
│   │   └── User/
│   │       ├── UserList/
│   │       └── UserDetail/
│   └── features/            # 业务模块
│       ├── shared/          # 跨 feature 共享（constants、hooks、utils）
│       ├── user/
│       │   ├── types.ts
│       │   ├── services/
│       │   ├── hooks/
│       │   └── components/
│       └── order/
│           ├── types.ts
│           ├── services/
│           ├── hooks/
│           └── components/
├── .umirc.ts                # Umi 构建配置
├── tailwind.config.js
└── tailwind.css
```

## 架构约定

### 分层职责

```
pages（路由入口）
  └── 组装 Form、Layout、Spin，调用 hooks

features（业务域）
  ├── types.ts      领域模型与查询参数类型
  ├── services/     API 请求封装，返回领域数据
  ├── hooks/        数据获取、分页、弹窗等业务逻辑
  └── components/   展示组件（SearchForm、Table、Modal 等）
```

### 新增业务模块

以 `product` 为例，推荐按以下步骤扩展：

1. 在 `src/features/product/` 下创建 `types.ts`、`services/`、`hooks/`、`components/`
2. 在 `src/pages/Product/ProductList/` 下创建页面入口
3. 在 `src/router/routes.ts` 注册路由
4. 在 `mock/` 下添加对应 Mock 接口（开发阶段）

### 类型规范

- **接口响应**：使用全局 `Api.Response<T>` 包装后端返回
- **应用状态**：使用 `App.InitialState`，与 `getInitialState`、`access.ts` 保持一致

```typescript
// src/types/api.d.ts
declare namespace Api {
  interface Response<T = undefined> {
    code: number;
    message?: string;
    data: T;
  }
}

// src/types/app.d.ts
declare namespace App {
  interface InitialState {
    name: string;
  }
}
```

### Service 层示例

```typescript
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

## Mock 与 API

开发环境通过 Umi Mock 插件提供本地接口：

| 方法 | 路径             | 说明                                   |
| ---- | ---------------- | -------------------------------------- |
| GET  | `/api/users`     | 用户列表（支持分页、姓名、角色筛选）   |
| GET  | `/api/users/:id` | 用户详情                               |
| POST | `/api/users`     | 新建用户                               |
| PUT  | `/api/users/:id` | 更新用户                               |
| GET  | `/api/orders`    | 订单列表（支持分页、订单号、状态筛选） |

Mock 文件位于 [`mock/`](mock/) 目录。接入真实后端时，在 [`.umirc.ts`](.umirc.ts) 中配置 `proxy` 转发即可。

## 微前端（qiankun）

本项目可作为 qiankun 子应用嵌入主应用：

- **开发环境**：渲染完整 Pro Layout 侧边栏，便于独立调试
- **生产环境**：通过 `src/app.ts` 中的 `layout` 配置隐藏 `menuRender` 与 `menuHeaderRender`，避免与主应用导航重复

```typescript
// src/app.ts
export const layout = () => {
  const isDev = process.env.NODE_ENV === 'development';
  return {
    ...(isDev ? {} : { menuRender: false, menuHeaderRender: false }),
  };
};
```

## 代码规范

项目通过 Git Hooks 保证提交质量：

- **pre-commit**：lint-staged 执行 ESLint / Stylelint 修复与 Prettier 格式化
- **commit-msg**：`max verify-commit` 校验 commit message 格式

手动格式化：

```bash
yarn format
```

## 配置说明

主要配置文件：

| 文件 | 用途 |
| --- | --- |
| [`.umirc.ts`](.umirc.ts) | Umi 构建、插件、路由、Mock、代理 |
| [`tailwind.config.js`](tailwind.config.js) | Tailwind 内容扫描路径 |
| [`.prettierrc`](.prettierrc) | 代码格式化规则 |
| [`.lintstagedrc`](.lintstagedrc) | 提交前 lint 范围 |

## 内置页面

### 用户管理

- 列表查询（姓名、角色筛选）
- 分页表格
- 新建 / 编辑用户（Modal）
- 跳转详情页

### 订单管理

- 列表查询（订单号、状态筛选）
- 分页表格

### 权限演示

- 基于 `access.canSeeAdmin` 的条件渲染示例

## 相关文档

- [Umi Max 简介](https://umijs.org/docs/max/introduce)
- [Umi 路由配置](https://umijs.org/docs/guides/routes)
- [Umi Access 权限](https://umijs.org/docs/max/access)
- [Ant Design](https://ant.design/components/overview-cn/)
- [Ant Design Pro Components](https://procomponents.ant.design/)
