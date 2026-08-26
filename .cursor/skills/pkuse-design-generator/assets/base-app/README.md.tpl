# __APP_TITLE__

由 PKUSE Design Generator 生成的 React、Vite、TypeScript、Ant Design 6
后台子应用，支持独立运行和 qiankun 2.x 挂载。

## 本地运行

```bash
pnpm install
pnpm dev
```

独立模式使用本地管理员与 Mock Service。运行 `pnpm typecheck`、`pnpm test`
和 `pnpm build` 完成质量检查。`pnpm build` 是独立部署构建，资源使用相对
URL。

## qiankun 接入

主应用容器须包含：

```html
<div data-pkuse-root="__APP_NAME__"></div>
```

注册时注入 `container`、`routeBase`、`user`、`authToken`、`navigate` 及可选
全局状态 actions。嵌入模式不渲染独立导航壳层；每次挂载均创建新的 React
Root 与 Router，卸载时会中止请求并清理订阅、监听和计时资源。

### 生产 entry 与资源基址

qiankun 生产构建必须使用独立命令：

```bash
pnpm build:qiankun
```

部署前复制 `.env.qiankun.example` 为 `.env.qiankun`，将
`VITE_PUBLIC_BASE` 设为子应用静态目录的绝对 HTTP(S) URL：

```dotenv
VITE_PUBLIC_BASE=https://cdn.example.com/apps/__APP_NAME__/
```

对应的 qiankun `entry` 为：

```text
https://cdn.example.com/apps/__APP_NAME__/index.html
```

`VITE_PUBLIC_BASE` 表示 entry 所在目录，因此主应用注册地址始终是
`VITE_PUBLIC_BASE + "index.html"`。配置后，qiankun 构建 HTML 中的全部入口
JS/CSS URL 均以该绝对值为基址。`build:qiankun` 在变量缺失、相对 URL 或非
HTTP(S) URL 时直接失败，并自动执行绝对资源 URL 校验。

不要把独立部署的 `pnpm build` 产物作为 qiankun 生产 entry；该命令允许相对
资源，只用于独立站点部署。

## API 替换

独立模式默认使用 `src/mocks/entity.mock.ts`。嵌入模式使用
`src/services/api.ts`，当前待替换端点为：

- `GET /api/entities`
- `GET /api/entities/:id`
