### Task 2: qiankun, engineering, and page-pattern references

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/references/qiankun-contract.md`
- Create: `.cursor/skills/pkuse-design-generator/references/engineering.md`
- Create: `.cursor/skills/pkuse-design-generator/references/page-patterns.md`

**Interfaces:**
- Consumes: Ant Design overlay from Task 1.
- Produces: generation contracts referenced by `SKILL.md` and scenario manifests.

- [ ] **Step 1: Write the qiankun contract**

The document must define these exact interfaces:

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

Require `bootstrap`, `mount`, `unmount`, optional `update`, a fresh React Root and Router per mount, scoped container lookup, and cleanup of root, subscriptions, timers, listeners, and aborted requests. Specify standalone `/` routing and injected `routeBase` for embedded mode.

- [ ] **Step 2: Write engineering rules**

Define:

```text
src/
├── app/             composition, providers, theme
├── auth/            access checks and permission declarations
├── features/        business slices; pages live with components and services
├── micro-app/       qiankun adapter and contracts
├── mocks/           development-only adapters and fixtures
├── routes/          one declaration feeding router and menu
├── services/        shared HTTP transport and contracts
└── styles/          namespaced global baseline only
```

Require strict TypeScript, feature-local tests, typed service injection, AbortController support, Error Boundary, distinct 401/403/404/5xx handling, and route/menu/action RBAC derived from shared permission constants.

- [ ] **Step 3: Write all six page patterns**

Use this exact schema for every section:

```markdown
## <scene-id>

- Trigger signals:
- Primary user task:
- Required routes:
- Required page states:
- Required Ant Design patterns:
- Required permissions:
- Avoid:
```

Define:

- `data-management`: filters, table, detail, create/edit drawer, batch action.
- `approval-workflow`: queue, detail, timeline, comments, approve/reject confirmation.
- `dashboard`: metric cards, trends, ranking, filters, anomaly list.
- `system-config`: organization tree, users, roles, permission matrix, parameters.
- `monitoring`: status overview, resources, logs, alerts, operation history.
- `generic`: infer entities and compose existing patterns without inventing a new visual language.

- [ ] **Step 4: Run the structure test**

Expected: all tests in `test_skill_structure.py` pass.

