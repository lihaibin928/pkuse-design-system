# Task 4 报告：可运行基础应用与 qiankun 双模式适配

## 状态

完成。未初始化 Git，未创建提交，仅修改任务简报允许的
`.cursor/skills/pkuse-design-generator/assets/base-app/`、
`.cursor/skills/pkuse-design-generator/tests/test_scaffold.py`，并新增本报告。

## RED

先扩展 `test_scaffold.py`，增加双模式生命周期、卸载清理、挂载元素一致性、
Ant Design 6、ConfigProvider、RBAC、Service Adapter 边界、Error Boundary 和基础
状态检查。

命令：

```text
python .cursor/skills/pkuse-design-generator/tests/test_scaffold.py -v
```

关键输出：

```text
Ran 7 tests
FAILED (errors=3)
FileNotFoundError: templates not found:
.../assets/base-app
```

失败原因符合预期：Task 4 的 `base-app` 模板尚不存在。

## GREEN

### 脚手架单测

任务简报给出的命令
`python -m unittest .cursor/skills/pkuse-design-generator/tests/test_scaffold.py -v`
在当前 Python 3.14.5 中被 `unittest` 解释为空模块名并报
`ValueError: Empty module name`。改用等价且兼容路径的 discover 形式：

```text
python -m unittest discover \
  -s .cursor/skills/pkuse-design-generator/tests \
  -p 'test_scaffold.py' -v
```

关键输出：

```text
Ran 7 tests in 0.194s
OK
```

### fixture 生成与依赖安装

```text
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name inventory-console \
  --title "库存中心" \
  --scene data-management \
  --output /tmp/pkuse-inventory-console-green
pnpm install --dir /tmp/pkuse-inventory-console-green
```

关键输出：

```text
/tmp/pkuse-inventory-console-green
Packages: +196
antd 6.6.0
qiankun 2.10.16
react/react-dom 19.2.8
react-router-dom 7.18.2
typescript 7.0.2
vite 8.2.1
vite-plugin-qiankun 1.0.15
vitest 4.1.10
Done
```

`pnpm view` 查询时 `antd` 最新值为 6.6.1，但本次 registry 解析实际安装
6.6.0，并提示 6.6.1 可用；模板保留 `^6.0.0`，lockfile 在 fixture 中固定实际
解析结果。未把临时 lockfile写入仓库。

### 类型、测试和构建

```text
cd /tmp/pkuse-inventory-console-green
pnpm typecheck
pnpm test
pnpm build
```

关键输出：

```text
typecheck: tsc -b --pretty false (exit 0)
test: Test Files 1 passed; Tests 2 passed
build: 1497 modules transformed; built in 637ms
dist/index.html                   1.53 kB
dist/assets/index-DxjlqI41.css    0.83 kB
dist/assets/index-0oy7_xbX.js   959.53 kB
```

实现过程中第一次 fixture 类型检查发现 Vite 8 的 `defineConfig` 不接受内联
`test` 字段；移除非必要字段后重新生成全新 fixture，最终 typecheck、test、
build 均通过。

## 实现摘要

- `main.tsx` 是唯一 qiankun/Vite 插件桥接入口；业务层无 qiankun import。
- 支持 standalone、`bootstrap`、`mount`、`unmount`、`update`。
- 每次 render/mount 创建新 React Root；`App` 每次实例化新 BrowserRouter。
- 嵌入模式严格从 `props.container` 查询
  `[data-pkuse-root='inventory-console']`；`index.html` 使用完全一致的挂载标记。
- standalone 使用本地管理员和 Mock Service，显示轻量 Header/Nav；嵌入模式
  只渲染业务内容，不重复宿主 shell。
- unmount 中止已登记请求，执行监听/计时清理，注销全局状态监听，卸载 Root，
  并清空 Root、props 和全局状态引用。
- ConfigProvider 使用应用 `prefixCls` 和独立 CSS variable `key/prefix`；
  自定义 CSS 均位于应用命名空间下。
- 权限常量、`can`、本地 admin/viewer 角色已提供。
- 页面依赖 `EntityService`，由 `createServices(mode)` 注入 Mock/API Adapter；
  页面不 import mocks。
- 提供 React Error Boundary，以及 loading、empty、error、forbidden、disabled
  状态。

## 文件清单

```text
assets/base-app/
├── .gitignore.tpl
├── README.md.tpl
├── index.html.tpl
├── package.json.tpl
├── tsconfig.app.json.tpl
├── tsconfig.json.tpl
├── tsconfig.node.json.tpl
├── vite.config.ts.tpl
└── src/
    ├── main.tsx.tpl
    ├── app/
    │   ├── App.tsx.tpl
    │   ├── ErrorBoundary.tsx.tpl
    │   ├── services.ts.tpl
    │   └── theme.ts.tpl
    ├── auth/
    │   ├── access.test.ts.tpl
    │   ├── access.ts.tpl
    │   └── permissions.ts.tpl
    ├── features/home/HomePage.tsx.tpl
    ├── micro-app/
    │   ├── adapter.tsx.tpl
    │   ├── cleanup.ts.tpl
    │   └── contracts.ts.tpl
    ├── mocks/
    │   ├── entity.mock.ts.tpl
    │   └── roles.ts.tpl
    ├── services/
    │   ├── api.ts.tpl
    │   └── contracts.ts.tpl
    └── styles/global.css.tpl
```

另修改：

```text
.cursor/skills/pkuse-design-generator/tests/test_scaffold.py
```

## 自审

- 生成结果中无未替换 `__APP_*` token。
- `src/features/` 中无 Mock import。
- `src/` 中 qiankun import 仅位于 `main.tsx` 桥接层。
- IDE 对任务文件未报告 lint 错误。
- 单测、严格 TypeScript、Vitest、生产构建均通过。
- 未修改 `scripts/scaffold.py` 接口；仍使用其既有确定性模板替换机制。

## 关注事项

1. 生产构建成功，但 Vite 报单 chunk 约 959.53 kB、gzip 307.77 kB，超过
   500 kB 提示线；后续场景页面可通过路由懒加载和 vendor 分包优化。
2. `vite-plugin-qiankun` 当前稳定版仍为 1.0.15，属于社区适配层；已把依赖
   限制在 `main.tsx`/微应用边界，便于后续替换。
3. `pnpm install` 报告一个间接依赖 `whatwg-encoding@3.1.1` 已弃用，不影响
   本次 typecheck/test/build。

---

## Needs fixes 复核修复（2026-08-18）

### 新一轮 RED

先补脚手架断言及生成应用的 Vitest：

- `micro-app/adapter.test.tsx`：重复 mount 清理旧实例；render 失败后回滚
  Root、全局订阅、请求和资源。
- `routes/manifest.test.tsx`：HOME_VIEW 路由/菜单一致性及三层权限独立性。
- `services/api.test.ts`：401、403、404、5xx、422、网络错误类型映射。
- Python 测试增加 public base、环境示例、构建 URL 校验器、manifest、错误类型
  和上述 Vitest 文件断言。

```text
python -m unittest discover \
  -s .cursor/skills/pkuse-design-generator/tests \
  -p 'test_scaffold.py' -v
```

关键 RED：

```text
FAILED (failures=1, errors=1)
missing src/routes/manifest.tsx
vite.config.ts missing base: publicBase || "./"
```

生成 RED fixture 后运行：

```text
pnpm --dir /tmp/pkuse-task4-review-red test
```

关键 RED：

```text
Test Files 3 failed | 1 passed
Cannot find module './manifest'
Cannot find module './errors'
repeated mount: previous root unmount called 0 times
failed mount: failed root unmount called 0 times
```

这些失败分别复现了 RBAC/错误分类缺失和生命周期非幂等、非原子问题。

### 修复 1：生产 qiankun 资源基址

- `vite.config.ts.tpl` 通过 `loadEnv` 读取 `VITE_PUBLIC_BASE`，只接受绝对
  HTTP(S) URL并补齐尾部 `/`。
- 未配置时 `base` 为 `./`，构建产物使用相对 entry 的资源 URL，禁止
  `/assets/...` 根绝对路径。
- 新增 `.env.example.tpl`，README 说明 public base、部署目录和 qiankun
  entry 的对应关系。
- 新增 `scripts/verify-build-base.mjs.tpl`；`pnpm build` 自动检查 HTML 中
  `src`、`href` 和插件生成的内联 `import(...)` 资源 URL。

默认构建 HTML 证据：

```text
import('./assets/index-enUl-EiB.js')
href="./assets/index-BY_h1XT6.css"
Verified 2 deploy-safe asset URL(s)
```

绝对基址构建命令及 HTML 证据：

```text
VITE_PUBLIC_BASE="https://cdn.example.com/apps/review-console/" \
  pnpm --dir /tmp/pkuse-task4-review-final2 build

import('https://cdn.example.com/apps/review-console/assets/index-B_hckmQE.js')
href="https://cdn.example.com/apps/review-console/assets/index-BY_h1XT6.css"
Verified 2 deploy-safe asset URL(s)
```

### 修复 2：mount 原子性与幂等

- 每次 render/mount 首先调用 `disposeCurrent()`；先摘除全局 root/props 引用，
  再逐项清理，避免重复 mount 覆盖旧 Root。
- selector 查询、订阅、Root 创建、render 被置于同一事务式 try/catch 中。
- 任一步骤抛错均执行 `abortAllRequests`、`clearAllResources`、全局状态
  unsubscribe、失败 Root unmount 和全局状态清空，然后重新抛出原错误。
- 清理项通过 `callSafely` 独立执行，单个 cleanup 抛错不会阻断后续清理。
- Vitest 使用受控 React Root 覆盖重复 mount 和 render 失败回滚；失败 render
  中登记真实 AbortController 与 cleanup，断言均被执行。

### 修复 3：RBAC 单一数据源

- 新增 `routes/manifest.tsx.tpl`，统一保存 `path`、`title`、`permissions`、
  `menu` 和 `element`。
- Router 使用 `createRouteManifest` 和 `canAccessRoute`；无 HOME_VIEW 时导航
  到 `/403`。
- standalone 菜单由同一 manifest 的 `buildVisibleMenu` 生成并隐藏无权限项。
- HOME_VIEW 实际保护首页；ENTITY_VIEW 保护页面数据；ENTITY_EDIT 独立控制
  编辑按钮，三者均来自共享 `PERMISSIONS`。

### 修复 4：API 错误分类

- 新增 `services/errors.ts.tpl`：`UnauthorizedError`、`ForbiddenError`、
  `NotFoundError`、`ServerError`、`NetworkError`、`BusinessError`。
- API Adapter 通过 `mapHttpError` 映射 401/403/404/5xx/其他业务 4xx，
  fetch/传输异常通过 `mapNetworkError` 映射；保留 request id。
- 页面分别呈现登录失效、Forbidden、NotFound、业务校验、服务端/网络错误；
  只有可重试服务与网络错误显示重试操作。

### 干净 fixture GREEN

fixture：

```text
/tmp/pkuse-task4-review-final2
```

完整命令：

```text
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name review-console --title "复核控制台" \
  --scene data-management \
  --output /tmp/pkuse-task4-review-final2
pnpm install --dir /tmp/pkuse-task4-review-final2
pnpm --dir /tmp/pkuse-task4-review-final2 typecheck
pnpm --dir /tmp/pkuse-task4-review-final2 test
pnpm --dir /tmp/pkuse-task4-review-final2 build
```

关键 GREEN：

```text
Python unittest: Ran 7 tests, OK
TypeScript: tsc -b --pretty false, exit 0
Vitest: Test Files 4 passed (4), Tests 13 passed (13)
Vite: 1499 modules transformed, built successfully
Build URL check: Verified 2 deploy-safe asset URL(s)
```

### 依赖版本选择

保持已通过安装和构建验证的组合，不为计划中的数字降级：

```text
antd 6.6.0
qiankun 2.10.16
react/react-dom 19.2.8
react-router-dom 7.18.2
@vitejs/plugin-react 5.2.0
typescript 7.0.2
vite 8.2.1
vite-plugin-qiankun 1.0.15
vitest 4.1.10
```

理由：该组合由当前 registry 实际解析，已通过 strict typecheck、13 个 Vitest
和两种 public base 的生产构建；降级只为数字对齐会放弃已经取得的兼容性证据。

### 新增/变更文件补充

```text
assets/base-app/.env.example.tpl
assets/base-app/scripts/verify-build-base.mjs.tpl
assets/base-app/src/micro-app/adapter.test.tsx.tpl
assets/base-app/src/routes/manifest.tsx.tpl
assets/base-app/src/routes/manifest.test.tsx.tpl
assets/base-app/src/services/errors.ts.tpl
assets/base-app/src/services/api.test.ts.tpl
assets/base-app/{vite.config.ts.tpl,package.json.tpl,README.md.tpl}
assets/base-app/src/{micro-app/adapter.tsx.tpl,app/App.tsx.tpl}
assets/base-app/src/{services/api.ts.tpl,features/home/HomePage.tsx.tpl}
.cursor/skills/pkuse-design-generator/tests/test_scaffold.py
```

### 复核后关注事项

1. 构建仍有单 chunk 约 962.79 kB（gzip 308.88 kB）的 Vite 警告；不影响
   qiankun entry/base 正确性，后续可通过路由懒加载和 vendor 分包优化。
2. `vite-plugin-qiankun@1.0.15` 仍是社区桥接层；所有插件耦合继续限制在
   `main.tsx`/micro-app 边界。
3. `whatwg-encoding@3.1.1` 间接依赖弃用警告仍存在，不影响本次全部验证。

---

## 第二次 Needs fixes 修复（2026-08-18）

### 根因与 RED

第二次复核确认上一版仍由同一个 `pnpm build` 同时承担 standalone 和 qiankun
生产构建，`base: publicBase || "./"` 让缺失 public base 的 qiankun 构建静默
成功，无法阻止错误部署。API Adapter 的宽泛 catch 还会把成功响应的 JSON
解析失败误标成 NetworkError。

先扩展 Python 断言，要求独立 `build:qiankun`、qiankun mode 强制校验和
`.env.qiankun.example`；再扩展 `api.test.ts`，通过真实 Adapter 调用覆盖 fetch
拒绝、204 空响应及 200 非法 JSON。

RED 证据：

```text
Python: FAILED (failures=2)
- vite.config.ts missing mode === "qiankun"
- services/errors.ts missing ProtocolError

Vitest: 2 failed | 14 passed
- invalid 2xx payload was not ProtocolError
- empty 2xx payload was not ProtocolError
```

### standalone / qiankun 构建拆分

生成应用现在提供：

```text
pnpm build
  -> tsc -b
  -> vite build --mode standalone
  -> verify-build-base.mjs

pnpm build:qiankun
  -> tsc -b
  -> vite build --mode qiankun
  -> verify-build-base.mjs --require-absolute
```

行为：

- standalone mode 固定 `base: "./"`，允许相对资源，只用于独立部署。
- qiankun mode 必须提供 `VITE_PUBLIC_BASE`；空值、相对 URL、非 HTTP(S) URL
  均在加载 Vite 配置时失败。
- 清晰错误信息：
  `qiankun build requires VITE_PUBLIC_BASE to be an absolute HTTP(S) URL`。
- qiankun 构建校验器要求所有入口 JS/CSS URL 为绝对 HTTP(S) URL；当变量从
  shell 注入时，还逐项断言 URL 以标准化后的 `VITE_PUBLIC_BASE` 开头。
- `.env.qiankun.example` 说明复制为 `.env.qiankun`，并明确
  `entry = VITE_PUBLIC_BASE + index.html`。
- README 明确禁止把 standalone `pnpm build` 产物作为 qiankun 生产 entry。

### ProtocolError 修复

- 新增独立 `ProtocolError`（状态语义 502、可重试）。
- Adapter 将 fetch 调用包在专用 try/catch 中；只有 fetch rejection 被映射为
  NetworkError，AbortError 保持原样。
- HTTP status 映射和成功响应 JSON 解析位于 fetch catch 之外。
- 2xx 空 body、非法 JSON 或 JSON `null` 映射为 ProtocolError，并保留
  request id。
- 页面把 ProtocolError 作为“服务响应异常”呈现并提供重试，而不是显示网络
  连接失败。

### 干净 fixture 与完整验证

fixture：

```text
/tmp/pkuse-task4-third-final2
```

生成、安装及主验证：

```text
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name third-review --title "三次复核" \
  --scene data-management \
  --output /tmp/pkuse-task4-third-final2
pnpm install --dir /tmp/pkuse-task4-third-final2
pnpm --dir /tmp/pkuse-task4-third-final2 typecheck
pnpm --dir /tmp/pkuse-task4-third-final2 test
pnpm --dir /tmp/pkuse-task4-third-final2 build
```

关键输出：

```text
Python unittest: Ran 7 tests, OK
TypeScript: exit 0
Vitest: Test Files 4 passed (4), Tests 16 passed (16)
standalone build: 1499 modules transformed, exit 0
standalone URL check: Verified 2 deploy-safe asset URL(s)
```

qiankun 缺失值失败断言：

```text
pnpm build:qiankun
Error: qiankun build requires VITE_PUBLIC_BASE to be an absolute HTTP(S) URL
PASS: missing base rejected
```

qiankun 相对值失败断言：

```text
VITE_PUBLIC_BASE="./assets/" pnpm build:qiankun
Error: qiankun build requires VITE_PUBLIC_BASE to be an absolute HTTP(S) URL
PASS: relative base rejected
```

qiankun 绝对值成功：

```text
VITE_PUBLIC_BASE="https://cdn.example.com/apps/third-review/" \
  pnpm build:qiankun

1499 modules transformed
Verified 2 deploy-safe asset URL(s)
exit 0
```

构建 HTML 入口证据：

```text
import('https://cdn.example.com/apps/third-review/assets/index-DAs9pDWE.js')
href="https://cdn.example.com/apps/third-review/assets/index-Csq37pTV.css"
```

### 本轮文件变更

```text
assets/base-app/package.json.tpl
assets/base-app/vite.config.ts.tpl
assets/base-app/scripts/verify-build-base.mjs.tpl
assets/base-app/README.md.tpl
assets/base-app/.env.qiankun.example.tpl
assets/base-app/src/services/errors.ts.tpl
assets/base-app/src/services/api.ts.tpl
assets/base-app/src/services/api.test.ts.tpl
assets/base-app/src/features/home/HomePage.tsx.tpl
.cursor/skills/pkuse-design-generator/tests/test_scaffold.py
```

删除容易误导构建 mode 的旧 `assets/base-app/.env.example.tpl`。

### 关注事项

1. Vite 仍报告约 963 kB 单 chunk 警告；与构建模式和资源基址正确性无关。
2. `whatwg-encoding@3.1.1` 间接依赖弃用警告仍存在。
3. 保持上一轮已安装并验证的依赖组合，未为计划数字做无证据降级。
