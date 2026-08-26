# Task 6 评测准备报告

**日期：** 2026-08-18  
**状态：** 准备完成，可启动并行生成任务  
**工作目录：** `/Users/eric/Documents/Projects/pkuse-design-system`

## 概述

已完成 Task 6「评测准备」阶段，创建了 eval 定义、workspace 目录结构、断言元数据及空的 with/without skill 输出目录。未执行任何生成任务，未初始化 Git，未提交代码。

## 创建的文件与目录

### 1. evals.json

**路径：** `.cursor/skills/pkuse-design-generator/evals/evals.json`

包含 3 个真实 prompt（与 task-6-brief.md 完全一致），每个 eval 含 `id`、`prompt`、`expected_output`、`files`、`expectations`（10 条客观断言）。

### 2. Workspace 目录结构

**根路径：** `.cursor/skills/pkuse-design-generator-workspace/iteration-1/`

```
iteration-1/
├── inventory-management/
│   ├── eval_metadata.json
│   ├── with_skill/outputs/
│   └── without_skill/outputs/
├── expense-approval/
│   ├── eval_metadata.json
│   ├── with_skill/outputs/
│   └── without_skill/outputs/
└── service-monitoring/
    ├── eval_metadata.json
    ├── with_skill/outputs/
    └── without_skill/outputs/
```

### 3. eval_metadata.json 字段

每个 eval 目录下的 `eval_metadata.json` 包含：

| 字段 | 说明 |
|------|------|
| `eval_id` | 1 / 2 / 3 |
| `eval_name` | 描述性目录名 |
| `prompt` | 完整用户 prompt |
| `assertions` | 10 条可客观检查的断言 |

**断言清单（三个 eval 共用）：**

1. `pnpm typecheck` 退出码为 0
2. `pnpm test` 退出码为 0
3. `pnpm build` 退出码为 0
4. micro-app adapter 导出 `bootstrap`、`mount`、`unmount`
5. 应用支持 standalone 独立渲染（main entry）
6. route、menu、action 权限共用 permission 声明
7. 页面 import service contracts，不 import Mock fixtures
8. 存在 `ConfigProvider`，页面代码无硬编码颜色
9. 实现 loading、empty、error、forbidden 状态
10. README 说明主应用接入与 API 替换点

字段结构兼容 skill-creator viewer（`generate_review.py` 读取 `eval_id`、`prompt`；grader 使用 `assertions` 生成 `grading.json`）。

## 三个 Eval 摘要

| eval_id | eval_name | 目标应用 | prompt 关键词 |
|---------|-----------|----------|---------------|
| 1 | inventory-management | inventory-console | 商品库存、多条件筛选、调整库存、批量盘点、RBAC |
| 2 | expense-approval | expense-approval-center | 报销审批、流程时间线、票据摘要、通过/驳回 |
| 3 | service-monitoring | service-ops-console | 服务健康、日志检索、告警确认、操作审计、Ant Design v6 |

## JSON 校验结果

| 检查项 | 结果 |
|--------|------|
| `evals/evals.json` 可解析 | ✅ 通过 |
| 3 个 `eval_metadata.json` 可解析 | ✅ 通过 |
| eval_id / eval_name 与目录一致 | ✅ 通过 |
| prompt 与 evals.json 完全一致 | ✅ 通过 |
| with_skill/outputs 目录存在且为空 | ✅ 通过 |
| without_skill/outputs 目录存在且为空 | ✅ 通过 |
| 无应用生成内容 | ✅ 通过 |

## 下一步（Step 2）

对每个 prompt 并行启动 6 个 agent 运行：

- **With skill：** 输出至 `<eval-name>/with_skill/outputs/`
- **Without skill（baseline）：** 输出至 `<eval-name>/without_skill/outputs/`

Skill 路径：`.cursor/skills/pkuse-design-generator`

运行完成后立即写入各 run 目录的 `timing.json`，再进入 Step 3–5 的 grading、aggregate 与 review UI。

## 约束确认

- [x] 未初始化 Git
- [x] 未提交任何变更
- [x] 未生成应用内容
- [x] 仅完成评测准备
