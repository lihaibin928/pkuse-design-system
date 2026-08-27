# __APP_TITLE__

由 PKUSE Design Generator 生成的 **Umi Max** 后台子应用，采用 Feature 模块化结构，UI 使用 **Ant Design 6**，支持独立运行和作为 qiankun 子应用嵌入。

## 本地运行

```bash
yarn install
yarn dev
```

启动后访问 [http://localhost:8000](http://localhost:8000)。独立模式使用 `mock/` 接口。设计 Token 预览：`/#/design-system`。

生产构建：

```bash
yarn build
```

产物输出至 `dist/`。

## 工程结构

```text
mock/                    开发 Mock 接口
src/access.ts            权限开关
src/app.ts               getInitialState、layout、qiankun 生命周期
src/router/routes.ts     路由 / 菜单唯一清单
src/utils/request.ts     HTTP 拦截
src/pages/               路由薄入口
src/features/            types / services / hooks / components
```

页面只组装 feature，不得直接 `request` 或导入 `mock/`。详细约定见仓库 `references/engineering.md`。

## qiankun 接入

`.umirc.ts` 已开启 `qiankun.slave`。Umi 会导出 `bootstrap` / `mount` / `unmount`；`src/app.ts` 中的 `qiankun` 钩子接收主应用 `user`、`authToken`。

- **开发环境**：渲染 Pro Layout 侧栏，便于独立调试
- **生产环境**：隐藏 `menuRender` / `menuHeaderRender`，由主应用导航

主应用注册时注入 `container`、`user`、`authToken`。Hash 路由已开启（`hash: true`）。

## API 替换

开发环境走 Umi Mock。接入真实后端时在 `.umirc.ts` 配置 `proxy`。当前 Mock 接口：

- `GET /api/users`
- `GET /api/users/:id`
- `POST /api/users`
- `PUT /api/users/:id`
- `GET /api/orders`
