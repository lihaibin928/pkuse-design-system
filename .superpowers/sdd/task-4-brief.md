### Task 4: Runnable base application and qiankun adapter

**Files:**
- Create: all files listed under `assets/base-app/` in the File Map.
- Modify: `.cursor/skills/pkuse-design-generator/tests/test_scaffold.py`

**Interfaces:**
- Consumes: `MicroAppProps`, `createServices(mode)`, and template replacement values.
- Produces: a standalone Vite app with `bootstrap`, `mount`, `unmount`, and `update`.

- [ ] **Step 1: Extend scaffold tests for runtime invariants**

```python
def test_generated_runtime_has_dual_mode_and_cleanup(self) -> None:
    with TemporaryDirectory() as temp:
        output = Path(temp) / "ops-console"
        MODULE.scaffold("ops-console", "运维中心", "monitoring", output)
        adapter = (output / "src/micro-app/adapter.tsx").read_text(encoding="utf-8")
        package = (output / "package.json").read_text(encoding="utf-8")
        self.assertIn("export async function bootstrap", adapter)
        self.assertIn("export async function mount", adapter)
        self.assertIn("export async function unmount", adapter)
        self.assertIn("root?.unmount()", adapter)
        self.assertIn("offGlobalStateChange?.()", adapter)
        self.assertIn('"antd": "^6', package)
```

- [ ] **Step 2: Create package and build configuration templates**

`package.json.tpl` must define:

```json
{
  "name": "__APP_NAME__",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "typecheck": "tsc -b --pretty false",
    "test": "vitest run"
  },
  "dependencies": {
    "@ant-design/icons": "^6.0.0",
    "antd": "^6.0.0",
    "qiankun": "^2.10.16",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "^5.0.0",
    "vite": "^7.0.0",
    "vite-plugin-qiankun": "^1.0.15",
    "vitest": "^3.0.0"
  }
}
```

During implementation, add dependencies with `pnpm add` rather than inventing patch versions; retain major-version floors in this template and commit the generated lockfile only if the user later requests repository commits.

- [ ] **Step 3: Create runtime contracts**

```ts
// src/micro-app/contracts.ts
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

- [ ] **Step 4: Create the lifecycle adapter**

```tsx
// src/micro-app/adapter.tsx.tpl
import { createRoot, type Root } from "react-dom/client";
import { App } from "../app/App";
import type { MicroAppProps } from "./contracts";

let root: Root | undefined;
let activeProps: MicroAppProps | undefined;

function getMountElement(props: MicroAppProps): Element {
  const element = props.container
    ? props.container.querySelector("[data-pkuse-root='__APP_NAME__']")
    : document.querySelector("[data-pkuse-root='__APP_NAME__']");
  if (!element) throw new Error("Mount element not found for __APP_NAME__");
  return element;
}

export function render(props: MicroAppProps = {}): void {
  activeProps = props;
  root = createRoot(getMountElement(props));
  root.render(<App props={props} title="__APP_TITLE__" />);
}

export async function bootstrap(): Promise<void> {}

export async function mount(props: MicroAppProps): Promise<void> {
  render(props);
}

export async function unmount(): Promise<void> {
  activeProps?.offGlobalStateChange?.();
  root?.unmount();
  root = undefined;
  activeProps = undefined;
}

export async function update(props: MicroAppProps): Promise<void> {
  await unmount();
  render(props);
}
```

- [ ] **Step 5: Create Vite adaptation, standalone entry, and app providers**

`vite.config.ts.tpl` integrates the community adapter behind Vite configuration:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import qiankun from "vite-plugin-qiankun";

export default defineConfig({
  plugins: [react(), qiankun("__APP_NAME__", { useDevMode: true })],
  server: {
    cors: true,
    headers: { "Access-Control-Allow-Origin": "*" },
  },
});
```

`src/main.tsx.tpl` registers the isolated adapter with the plugin and starts locally only in standalone mode:

```tsx
import { qiankunWindow, renderWithQiankun } from "vite-plugin-qiankun/dist/helper";
import { bootstrap, mount, render, unmount, update } from "./micro-app/adapter";
import "./styles/global.css";

renderWithQiankun({ bootstrap, mount, unmount, update });

if (!qiankunWindow.__POWERED_BY_QIANKUN__) {
  render();
}

export { bootstrap, mount, unmount, update };
```

`App.tsx.tpl` creates a Router per render and wraps routes in `ConfigProvider`, `App`, and an Error Boundary. Embedded mode renders business content without duplicating the host shell; standalone mode renders a compact local header and navigation. Keeping plugin imports in `main.tsx` ensures pages and domain modules remain independent of the Vite/qiankun bridge.

- [ ] **Step 6: Create theme, RBAC, services, and namespaced CSS**

Implement:

```ts
export function can(permissions: readonly string[], required?: string): boolean {
  return required === undefined || permissions.includes(required);
}
```

```ts
export interface ServiceResult<T> {
  data: T;
  requestId: string;
}

export interface EntityService<T> {
  list(signal?: AbortSignal): Promise<ServiceResult<T[]>>;
  get(id: string, signal?: AbortSignal): Promise<ServiceResult<T>>;
}
```

`theme.ts` exports an Ant Design `ThemeConfig` without hard-coded page-level colors. `global.css.tpl` scopes custom selectors under `[data-pkuse-app="__APP_NAME__"]`.

- [ ] **Step 7: Run scaffold tests and build a fixture**

Run:

```bash
python -m unittest .cursor/skills/pkuse-design-generator/tests/test_scaffold.py -v
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name inventory-console \
  --title "库存中心" \
  --scene data-management \
  --output /tmp/pkuse-inventory-console
cd /tmp/pkuse-inventory-console && pnpm install && pnpm typecheck && pnpm build
```

Expected: all unittests pass, TypeScript exits `0`, and Vite writes `dist/`.

