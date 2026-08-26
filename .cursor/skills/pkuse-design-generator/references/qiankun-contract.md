# qiankun 微应用契约

生成的子应用必须暴露兼容 qiankun 的生命周期，并通过 `src/micro-app/` 中的类型化适配器消费主应用 props。业务代码不得直接导入 qiankun API。

## TypeScript 接口

放在 `src/micro-app/contracts.ts`，作为主应用 ↔ 子应用通信的唯一事实来源。

```ts
export interface UserIdentity {
  id: string;
  displayName: string;
  roles: string[];
  permissions: string[];
}

export interface GlobalStateActions {
  onGlobalStateChange?: (
    listener: (state: Record<string, unknown>, previous: Record<string, unknown>) => void,
    fireImmediately?: boolean,
  ) => void;
  setGlobalState?: (state: Record<string, unknown>) => boolean;
  offGlobalStateChange?: () => boolean;
}

export interface MicroAppProps extends GlobalStateActions {
  container?: Element | ShadowRoot;
  routeBase?: string;
  user?: UserIdentity;
  authToken?: string;
  navigate?: (path: string) => void;
}
```

## 运行模式

| 模式 | 入口 | 容器 | 路由基路径 | 认证来源 |
| --- | --- | --- | --- | --- |
| 独立运行 | `src/main.tsx` | `index.html` 中的 `#root` | `/` | 来自 `src/mocks/` 的本地 Mock 用户 |
| 嵌入（qiankun） | `src/micro-app/lifecycle.ts` | 在 `props.container` 内查找 | `props.routeBase ?? '/'` | `props.user`、`props.authToken` |

只在适配器中判断模式：

```ts
export function isQiankunRuntime(): boolean {
  return Boolean((window as Window & { __POWERED_BY_QIANKUN__?: boolean }).__POWERED_BY_QIANKUN__);
}
```

## 容器查找

始终在注入的容器内解析挂载节点；嵌入模式下不要假定存在全局 `#root`。

```ts
const MOUNT_SELECTOR = '[data-micro-app-root]';

export function resolveMountNode(container?: Element | ShadowRoot): HTMLElement {
  const scope = container ?? document;
  const node = scope.querySelector<HTMLElement>(MOUNT_SELECTOR);
  if (!node) {
    throw new Error(`Mount node "${MOUNT_SELECTOR}" not found inside container`);
  }
  return node;
}
```

生成的应用壳必须渲染 `<div data-micro-app-root />` 作为 React 挂载点。

## 生命周期导出

从 `src/micro-app/lifecycle.ts` 导出（`isQiankunRuntime()` 为真时由 Vite 入口再导出）：

| 钩子 | 是否必须 | 职责 |
| --- | --- | --- |
| `bootstrap` | 是 | 一次性异步初始化：校验环境、预加载共享配置。不写 DOM。 |
| `mount` | 是 | 创建全新的 React Root 与 Router，把 props 接入 Provider，渲染到作用域容器。 |
| `unmount` | 是 | 完整清理（见下文）。 |
| `update` | 可选 | 主应用传入新的用户、token 或路由基路径时，在不重新挂载的情况下应用变更后的 `MicroAppProps`。 |

### bootstrap

```ts
export async function bootstrap(): Promise<void> {
  // 仅做幂等准备；每次应用加载调用一次即可。
}
```

### mount

每次 `mount` 时：

1. 把 `MicroAppProps` 存入适配器上下文。
2. 通过 `resolveMountNode(props.container)` 解析挂载节点。
3. 创建**新的** `createRoot(mountNode)`。
4. 创建**新的** `BrowserRouter`，`basename = props.routeBase ?? '/'`。
5. 把 `user`、`authToken`、`navigate` 和全局状态操作传入应用 Provider。
6. 渲染 `<App />`。

```ts
let root: Root | null = null;

export async function mount(props: MicroAppProps): Promise<void> {
  const mountNode = resolveMountNode(props.container);
  root = createRoot(mountNode);
  root.render(
    <BrowserRouter basename={props.routeBase ?? '/'}>
      <MicroAppProvider value={props}>
        <App />
      </MicroAppProvider>
    </BrowserRouter>,
  );
}
```

### update（可选）

实现时比较 props，更新认证上下文和路由 basename，且不泄漏上次的订阅。

### unmount

`unmount` 必须幂等且完整：

1. 中止所有进行中的 HTTP 请求（共享 `AbortController` 注册表）。
2. 清除应用注册的 interval 和 timeout。
3. 通过 `offGlobalStateChange` 或已保存的 disposer 取消全局状态监听。
4. 移除 mount 之后注册的 window / document 监听。
5. 调用 `root.unmount()`，然后把 `root` 设为 `null`。
6. 清除适配器持有的 props 引用。

```ts
export async function unmount(): Promise<void> {
  abortAllRequests();
  clearAllTimers();
  disposeAllSubscriptions();
  root?.unmount();
  root = null;
}
```

## 路由

| 关注点 | 规则 |
| --- | --- |
| 独立运行 basename | 始终为 `'/'` |
| 嵌入 basename | 使用主应用传入的 `props.routeBase`；省略时默认 `'/'` |
| 应用内链接 | 使用 React Router 的 `<Link>` / `useNavigate`；路径相对 basename |
| 跨应用跳转 | 调用 `props.navigate?.(absoluteHostPath)`；不要为了主应用路由去改 `window.location` |
| 路由守卫 | 从注入的 `user` 或认证上下文读权限，不要读 qiankun 全局变量 |

主应用注入示例：

```ts
// 主应用以 activeRule '/admin/inventory' 注册微应用
mount({ routeBase: '/admin/inventory', container, user, authToken, navigate });
```

内部路由 `/items` 在浏览器中解析为 `/admin/inventory/items`。

## 全局状态

在适配器中订阅，向业务层暴露类型化 hook：

```ts
// 适配器在每次 mount 注册一次
props.onGlobalStateChange?.((state, prev) => {
  microAppStore.setGlobalState(state);
}, true);
```

卸载时调用 `offGlobalStateChange`，或主应用实现返回的 disposer。

## 认证传递

| 字段 | 用途 |
| --- | --- |
| `user` | 初始化 RBAC 上下文；驱动菜单、路由守卫和操作可见性 |
| `authToken` | 作为 `Authorization` 头交给 HTTP 适配器 |
| `navigate` | API 返回 401 时跳转到主应用登录 |

独立运行模式提供带至少两种角色的 Mock `UserIdentity`，用于权限测试。

## 样式隔离

- 为 Ant Design `ConfigProvider` 配置应用级 `prefixCls` 和 CSS 变量前缀。
- 自定义样式放在应用命名空间下（见 `references/design-system.md`）。
- 页面不要注入无前缀的全局选择器。
- 不为 Ant Design 浮层强制要求 Shadow DOM。

## 挂载失败处理

若 `resolveMountNode` 抛错或 `mount` 拒绝：

1. 记录应用名和生命周期阶段。
2. 容器可用时，在其中渲染可恢复降级（带重试说明的 Ant Design `Result`）。
3. 不要留下半成品 Root、悬挂监听或未清理的定时器。

## 文件布局

```text
src/micro-app/
├── contracts.ts      # MicroAppProps 及相关类型
├── lifecycle.ts      # bootstrap / mount / unmount / update
├── adapter.ts        # isQiankunRuntime、resolveMountNode、清理注册表
├── provider.tsx      # props 的 React context
└── cleanup.ts        # 请求中止 / 定时器 / 订阅注册表
```

## 生成检查清单

- [ ] 从 qiankun 入口导出全部四个生命周期钩子。
- [ ] 每次 `mount` 使用全新的 React Root 和 Router。
- [ ] 挂载节点在 `props.container` 内解析。
- [ ] `unmount` 中止请求，并清除订阅 / 定时器 / 监听。
- [ ] 独立运行 basename 为 `/`；嵌入模式使用 `props.routeBase`。
- [ ] `src/micro-app/` 之外没有 qiankun 导入。
