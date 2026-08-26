# 页面模式

每次生成请求归入一个主场景。仅当用户描述了多套互不相关的工作流时才组合场景。视觉遵循 `references/design-system.md` 和 `references/ant-design-v6.md`。组件何时使用与语义槽见 `references/components/INDEX.md`。

## 数据管理（data-management）

- 触发信号：CRUD、列表 / 查询、主数据、库存、目录、台账、导入导出、批量操作、「数据管理」、「台账」。
- 主任务：检索并筛选实体，查看行详情，新增或编辑记录，对选中行做批量操作。
- 必含路由：`/<entity>`（列表）、`/<entity>/:id`（详情）；新增 / 编辑在列表页用抽屉或对话框完成——除非表单超出抽屉容量，否则不单独建 `/new`。
- 必含页面状态：加载骨架屏、空数据（无行 / 无搜索结果）、可重试错误、已筛选 vs 已清空、行选择激活、抽屉打开（新增 / 编辑）、批量操作确认、危险操作无权限。
- 必用 Ant Design 模式：`Form` + 行内 `Space` 筛选条、带行选择和分页的 `Table`、新增 / 编辑用 `Drawer` 或 `Modal`、详情用 `Descriptions` 或分区面板、删除 / 批量用 `Popconfirm`、结果用 `message` / `notification`、状态列用 `Tag`。
- 必含权限：`<entity>:view`（列表 / 详情）、`<entity>:create`、`<entity>:edit`、`<entity>:delete`，有导出时加 `<entity>:export`；批量操作复用编辑 / 删除权限码。
- 避免：用卡片宫格替代主表格；无业务价值的未排序列；宽表单上做行内编辑；在 Token 外硬编码状态色；删除不确认或不校验权限。

## 审批流程（approval-workflow）

- 触发信号：approval、review、待办队列、提交 / 驳回、workflow、「审批」、「待办」、「流程」、「报销」、「工单审核」。
- 主任务：从队列处理指派事项，审阅完整上下文，阅读时间线与意见，确认后通过或驳回。
- 必含路由：`/approvals`（队列）、`/approvals/:id`（详情）；用户提到「我提交的」时可选 `/approvals/submitted`。
- 必含页面状态：队列加载 / 空、按状态 / 处理人筛选、详情加载、时间线有数据、意见录入、通过 / 驳回确认框、已提交 vs 已退回 vs 已完成标记、决策操作无权限。
- 必用 Ant Design 模式：队列用 `Table` 或 `List`、状态用 `Badge` / `Tag`、历程用 `Timeline`、意见用 `Comment` 或 `List`、驳回时 `Modal` 强制填写意见、申请摘要用 `Descriptions`、有 SLA 或紧急度时用 `Alert`。
- 必含权限：`<workflow>:view`（队列 / 详情）、`<workflow>:approve`、`<workflow>:reject`、`<workflow>:comment`；发起人专属路由用 `<workflow>:submit`。
- 避免：通过 / 驳回不确认；驳回原因不校验；省略时间线；把审批当成没有状态语义的普通 CRUD；做出与决策无关的重复详情布局。

## 运营看板（dashboard）

- 触发信号：dashboard、metrics、KPI、趋势、排行、overview、「看板」、「运营」、「数据概览」、「报表」。
- 主任务：监控关键指标，对比趋势，实体排行，按维度筛选，并对视图中的异常采取行动。
- 必含路由：`/dashboard`（单一总览）；深链可用查询参数筛选，不为每个卡片单独建页。
- 必含页面状态：全局加载、单个卡片局部错误（按卡降级）、时间范围内无数据、已筛选、异常列表空 vs 有数据、刷新中。
- 必用 Ant Design 模式：`Row` / `Col` 指标 `Card`、`Statistic`、图表容器（Ant Design Charts 或对齐 Token 的占位）、`Select` / `DatePicker` / `Segmented` 筛选、排行用 `Table` 或 `List`、异常用 `Alert` 或高亮 `List`、手动 / 自动刷新。
- 必含权限：`<domain>:dashboard:view`；有快照 / 导出时可选 `<domain>:export`。
- 避免：总览上多个主操作互相抢；图表没有轴标签或空状态；排行列表够用时再复制一张完整 CRUD 表；自造脱离 Ant Design Token 的图表外壳。

## 系统配置（system-config）

- 触发信号：organization、users、roles、permissions、settings、parameters、「系统配置」、「组织」、「角色」、「权限矩阵」。
- 主任务：维护组织树，给用户分配角色，配置权限矩阵，安全地修改系统参数。
- 必含路由：`/settings/organization`、`/settings/users`、`/settings/roles`、`/settings/permissions`、`/settings/parameters`——仅当用户明确缩小范围时才合并。
- 必含页面状态：树加载 / 空、用户表已筛选、角色编辑器脏 / 已保存、矩阵部分 vs 全部加载、参数校验错误、保存确认、各配置分区无权限。
- 必用 Ant Design 模式：组织用 `Tree`、用户用带操作的 `Table`、用户角色分配用 `Modal` / `Drawer`、权限用 `Transfer` 或复选矩阵、参数用带行内校验的 `Form`、配置分区用 `Tabs`、危险角色变更用 `Popconfirm`。
- 必含权限：`settings:org:view|edit`、`settings:users:view|edit`、`settings:roles:view|edit`、`settings:permissions:view|edit`、`settings:params:view|edit`——只生成请求涉及的子集。
- 避免：用扁平列表冒充组织树；改权限却不展示生效影响；不相关配置页不用 Tab 分开；静默覆盖参数且不确认。

## 监控运维（monitoring）

- 触发信号：monitoring、observability、alerts、logs、resources、uptime、「监控」、「运维」、「告警」、「日志」。
- 主任务：判断系统健康，检查资源，检索日志，分诊告警，审计近期操作。
- 必含路由：`/monitor/overview`、`/monitor/resources`、`/monitor/logs`、`/monitor/alerts`、`/monitor/operations`——仅当用户指定窄范围（例如只要日志）时才收折。
- 必含页面状态：总览降级 / 健康、资源列表加载 / 空、日志搜索无结果、实时跟踪 vs 已暂停、告警已确认 vs 正在触发、操作历史分页、变更类操作（确认 / 静默）无权限。
- 必用 Ant Design 模式：带语义色的状态摘要 `Card`、资源 / 告警 / 操作用 `Table`、日志用 `Input.Search` + 时间范围、严重级别用 `Tag`、告警 / 日志详情用 `Drawer`、确认 / 静默用 `Modal`、活跃事件数用 `Badge`。
- 必含权限：`monitor:overview:view`、`monitor:resources:view`、`monitor:logs:view`、`monitor:alerts:view`、`monitor:alerts:ack`、`monitor:operations:view`。
- 避免：没有暂停 / 刷新的假实时流；告警不分严重级别；日志没有时间范围；把监控总览做成业务看板；破坏性操作不写审计记录。

## 通用组合（generic）

- 触发信号：无法明确归入上述五类的后台需求；混合中后台工具；未点名标准模式的领域控制台。
- 主任务：从描述推断主实体和用户任务，用最接近的既有模式组合页面，不另造视觉语言。
- 必含路由：按推断实体推导 REST 路径（`/<entity>`、`/settings/...`、`/dashboard` 等）；只搭建覆盖所述任务的最小集合，不生成用不到的分区。
- 必含页面状态：每个组合页都带上所借模式应有的加载、空数据、错误和无权限状态；不因场景是混合而省略。
- 必用 Ant Design 模式：复用匹配模式中的组件（实体管理以表格为中心、顺序审核用时间线、摘要用卡片）；语义不超出 `references/ant-design-v6.md`。
- 必含权限：从用户描述中的实体和动词推导 `<domain>:<resource>:<action>`；路由、菜单和按钮与 `references/engineering.md` 中的同一常量对齐。
- 避免：已有模式够用时仍发明新布局（自定义向导、非 Ant 导航）；做成组件展览页；用户没要求却为同一实体同时做 CRUD 和看板；模式不落在已声明的角色或任务上。
