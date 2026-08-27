# qiankun 微应用契约

生成的子应用是 **Umi Max qiankun slave**。生命周期由 Umi 导出；业务代码不得直接导入 qiankun API，也不得在 pages / features 里读取 `__POWERED_BY_QIANKUN__`。

## 文件布局

```text
.umirc.ts          qiankun.slave、hash、antd、access、routes
src/app.ts         getInitialState、layout、qiankun 钩子（bootstrap/mount/unmount/update）
src/access.ts      由 InitialState.user.permissions 派生权限开关
src/router/routes.ts
```

不要再创建 `src/micro-app/`。

## TypeScript 接口

主应用传入的身份放在 `App.UserIdentity`（`src/types/app.d.ts`），由 `src/app.ts` 写入 `getInitialState`：

```ts
interface UserIdentity {
  id: string;
  displayName: string;
  roles: string[];
  permissions: string[];
}

type QiankunProps = {
  container?: Element;
  user?: UserIdentity;
  authToken?: string;
};
```

## 运行模式

| 模式 | 入口 | 容器 | 路由 | 认证来源 |
| --- | --- | --- | --- | --- |
| 独立运行 | `yarn dev` / `max dev` | Umi 默认根节点 | Hash，基路径 `/` | `getInitialState` 本地标题；无 `user` 时 `access.ts` 视为管理端 |
| 嵌入（qiankun） | Umi slave 生命周期 | 主应用 `props.container` | 同样 Hash；主应用负责外层导航 | `src/app.ts` 的 `qiankun.mount` 写入 `user`、`authToken` |

`.umirc.ts` 必须开启：

```ts
qiankun: {
  slave: {},
},
hash: true,
```

## 生命周期

在 `src/app.ts` 导出 `qiankun` 钩子（Umi 会再导出给主应用）：

| 钩子 | 是否必须 | 职责 |
| --- | --- | --- |
| `bootstrap` | 是 | 幂等准备，不写业务 DOM |
| `mount` | 是 | 保存主应用 `user` / `authToken` / `container` |
| `unmount` | 是 | 清空已保存的 props 引用 |
| `update` | 可选 | 主应用更新用户或 token 时同步，不重新发明一套路由 |

```ts
export const qiankun = {
  async bootstrap() {},
  async mount(props: QiankunProps = {}) {
    qiankunProps = props;
  },
  async update(props: QiankunProps = {}) {
    qiankunProps = props;
  },
  async unmount() {
    qiankunProps = {};
  },
};
```

不要在业务组件里 `createRoot`。挂载与卸载由 Umi 负责。

## 布局

`src/app.ts` 的 `layout`：

- **开发环境**：渲染 Pro Layout 侧栏，便于独立调试
- **生产环境**：`menuRender: false`、`menuHeaderRender: false`，避免与主应用导航重复

## 路由

| 关注点 | 规则 |
| --- | --- |
| 清单 | 只维护 `src/router/routes.ts`，由 `.umirc.ts` 引入 |
| 应用内跳转 | `history` / `useSearchParams`（`umi` 或 `@umijs/max`） |
| 跨应用跳转 | 交给主应用；子应用不要改 `window.location` 去切主应用路由 |
| 权限 | 路由项的 `access` 字段指向 `src/access.ts` 的开关 |

## 认证传递

| 字段 | 用途 |
| --- | --- |
| `user` | 初始化 `App.InitialState`，驱动 `access.ts`、菜单和操作 |
| `authToken` | 需要时写入请求头；默认 cookie 凭证见 `src/utils/request.ts` 的 `credentials: 'include'` |

独立运行时 `user` 可为空；`access.ts` 将空用户视为可验证全部开关的本地管理员。嵌入模式必须传入带 `permissions` 的 `user`。

## 样式隔离

- 通过 Umi `antd` 插件使用 `ConfigProvider`；不要在 pages 里再包一层全局 Provider。
- 自定义样式放在组件旁 Less 或 Tailwind；不要使用会泄漏到主应用的无前缀元素选择器。
- 不为 Ant Design 浮层强制要求 Shadow DOM。

## 生成检查清单

- [ ] `.umirc.ts` 包含 `qiankun.slave` 与 `antd`
- [ ] `src/app.ts` 导出 `qiankun` 的 bootstrap / mount / unmount
- [ ] 生产环境隐藏子应用侧栏
- [ ] pages / features 不导入 qiankun、不读取 `__POWERED_BY_QIANKUN__`
- [ ] 路由与权限分别只来自 `src/router/routes.ts` 与 `src/access.ts`
