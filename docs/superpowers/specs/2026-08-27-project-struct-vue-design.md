# project-struct-vue 工程模板设计规格

## 目标

在仓库根目录新增 `project-struct-vue/`，作为 Vue 企业后台子应用的工程结构基准，功能与目录职责对齐现有 `project-struct-react/`。它必须同时支持独立运行和 qiankun 挂载，并内置与 React 模板相同的用户、订单示例页。

本次范围只交付该模板目录。不修改 `pkuse-design-generator` Skill，也不生成 Vue 子应用脚手架脚本。

## 非目标

- Vue 版 Cursor Skill / `scaffold.py` / `validate.py`
- qiankun 主应用
- 像素级复刻 React 侧 Ant Design 6（ant-design-vue 4 对齐的是 Ant Design 4/5）
- 真实后端
- 把 React 模板里的 Umi 插件体系原样搬到 Vue

## 技术栈

| 类别 | 选型 |
| --- | --- |
| 框架 | Vue 3（SFC + `<script setup lang="ts">`） |
| 构建 | Vite |
| 路由 | Vue Router 4，Hash 模式 |
| 状态 | Pinia（存放 `initialState`：name、user、authToken） |
| UI | ant-design-vue 4.2.x · `@ant-design/icons-vue` |
| 请求 | axios，封装于 `src/utils/request.ts` |
| Mock | `vite-plugin-mock`，根目录 `mock/` |
| 微前端 | `vite-plugin-qiankun`，生命周期只在 `src/main.ts` |
| 语言 | TypeScript `strict` |
| 样式 | 组件旁 Less · Tailwind CSS 3 工具类 |
| 包管理 | yarn |
| 工程化 | Husky · lint-staged · Prettier · ESLint · Stylelint |
| 开发端口 | `8001`（避免与 React 模板 `8000` 冲突） |

主色使用 Ant Design 默认蓝 `#1677FF`。不另造品牌色。

## 目录结构

```text
project-struct-vue/
├── mock/
│   ├── user.ts
│   └── order.ts
├── src/
│   ├── main.ts                 独立运行入口；导出 qiankun 生命周期
│   ├── App.vue                 根组件，挂 Layout
│   ├── access.ts               由 initialState 派生权限开关
│   ├── layouts/
│   │   └── BasicLayout.vue     侧栏 + 内容区；生产环境隐藏侧栏
│   ├── router/
│   │   ├── index.ts            createRouter、beforeEach
│   │   └── routes.ts           路由 / 菜单唯一清单
│   ├── stores/
│   │   └── app.ts              Pinia：name、user、authToken
│   ├── utils/
│   │   └── request.ts          axios 实例、业务码与 HTTP 错误处理
│   ├── types/
│   │   ├── api.d.ts            Api.Response
│   │   └── app.d.ts            App.InitialState、App.UserIdentity、QiankunProps
│   ├── constants/
│   ├── assets/
│   ├── components/             跨业务域通用组件（如 Guide）
│   ├── pages/                  路由薄入口（.vue）
│   │   ├── Home/
│   │   ├── Access/
│   │   ├── Order/OrderList/
│   │   └── User/
│   │       ├── UserList/
│   │       └── UserDetail/
│   └── features/
│       ├── shared/             constants、composables、utils、components
│       ├── user/
│       │   ├── types.ts
│       │   ├── services/
│       │   ├── composables/
│       │   └── components/
│       └── order/
│           ├── types.ts
│           ├── services/
│           ├── composables/
│           └── components/
├── index.html
├── vite.config.ts
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── tailwind.css
```

与 React 模板的对应关系：

| React | Vue |
| --- | --- |
| `.umirc.ts` + `src/app.ts` | `vite.config.ts` + `src/main.ts` + `src/stores/app.ts` |
| Umi `layout` | `src/layouts/BasicLayout.vue` |
| `features/<slice>/hooks/` | `features/<slice>/composables/` |
| `@umijs/max` `request` | axios `src/utils/request.ts` |
| Umi Mock 插件 | `vite-plugin-mock` |
| Umi `access` 插件 | `src/access.ts` + `router.beforeEach` |
| Pro Components `PageContainer` / `ProTable` | ant-design-vue `Layout` / `Table` / `Form` / `Modal` 拼出同等交互 |

`pages/` 只组装 Layout、查询区、表格、弹窗，并调用 composable。不得在页面里写列定义、接口拼接或弹窗提交逻辑。

## 运行时

### 请求

`src/utils/request.ts` 行为对齐 React 模板：

- `credentials: include`
- 业务成功：`success === true`，或 `code` 为 `0` / `200`
- 业务失败：`message.error`，抛错给调用方
- `code === 100000` 或 HTTP 401：跳转 `/login`（Hash：`#/login`）
- 网络失败给出中文提示

页面与 feature 只通过 `request` 调 `/api/*`，不得静态导入 `mock/`。

### Mock API

与 React 模板路径、语义一致：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/users` | 用户列表（分页、姓名、角色） |
| GET | `/api/users/:id` | 用户详情 |
| POST | `/api/users` | 新建用户 |
| PUT | `/api/users/:id` | 更新用户 |
| GET | `/api/orders` | 订单列表（分页、订单号、状态） |

### 权限

`src/access.ts` 从 Pinia `initialState` 派生 `{ canSeeAdmin }`。独立运行且无主应用 `user` 时，视为管理端（`canSeeAdmin: true`）。`Access` 页与带 `access` 字段的路由用该开关控制。无权时路由守卫拦截，页面展示无权限状态。

### qiankun

只允许出现在 `src/main.ts` 与 `vite.config.ts`。业务 `pages/`、`features/` 不得导入 qiankun，不得读取 `__POWERED_BY_QIANKUN__`。

| 模式 | 入口 | 容器 | 路由 | 认证 |
| --- | --- | --- | --- | --- |
| 独立运行 | `yarn dev` | `#app` | Hash，基路径 `/` | 本地 `initialState.name` |
| 嵌入 | `bootstrap` / `mount` / `unmount` / `update` | `props.container` | 同样 Hash | `mount`/`update` 写入 `user`、`authToken` |

与 React 模板一致：仅 `NODE_ENV === 'development'` 时渲染侧栏与菜单头；生产构建隐藏，由主应用导航。独立 `yarn dev` 可见侧栏。

Vite 需配置 `base` 与 `origin` 以便作为子应用加载；`esbuild`/`IIFE` 辅助函数冲突按 Vite qiankun 惯例处理。

## 页面

| 路径 | 页面 | 菜单 |
| --- | --- | --- |
| `/home` | 首页，欢迎文案 | 是 |
| `/access` | 权限演示 | 是 |
| `/order/list` | 订单列表：查询、分页、加载/空/错误 | 是 |
| `/user/list` | 用户列表：查询、分页、新建/编辑弹窗 | 是 |
| `/user/detail?id=` | 用户详情 | 否 |
| `/` | 重定向到 `/home` | — |

列表页必须覆盖：加载、空数据、错误、禁用。用户编辑成功后刷新列表。

## 命令

```bash
cd project-struct-vue
yarn install
yarn dev      # http://localhost:8001
yarn build    # dist/
yarn format
```

`package.json` 的 `name` 为 `project-struct-vue`。

## 完成标准

- 目录存在于仓库根路径 `project-struct-vue/`
- `yarn install` 后 `yarn dev` 可打开首页、权限页、订单列表、用户列表与详情
- 独立运行可见侧栏；以生产模式理解的嵌入约定下侧栏关闭
- `yarn build` 成功产出 `dist/`
- 请求错误与业务码处理与 React 模板语义一致
- 业务代码无 qiankun 导入

## 风险

- ant-design-vue 4 不是 Ant Design 6，组件 API 与视觉会与 React 模板有差异；以交互与分层对齐为准，不以像素对齐为准。
- Vue 侧没有 Pro Components 完整对等物；表格列、查询表单、弹窗用手写组件表达，不引入重量级第三方 Pro 套件。
