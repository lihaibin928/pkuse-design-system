### Task 6: Skill evaluation cases and review workflow

**Files:**
- Create: `.cursor/skills/pkuse-design-generator/evals/evals.json`
- Create during execution: `.cursor/skills/pkuse-design-generator-workspace/iteration-1/**`

**Interfaces:**
- Consumes: completed Skill and Skill Creator evaluation scripts.
- Produces: three with-Skill outputs, three baseline outputs, grades, timing, `benchmark.json`, and human review UI.

- [ ] **Step 1: Create realistic evaluation prompts**

```json
{
  "skill_name": "pkuse-design-generator",
  "evals": [
    {
      "id": 1,
      "prompt": "为仓储团队生成一个名为 inventory-console 的 qiankun 子应用。需要商品和库存列表、多条件筛选、库存详情、调整库存抽屉、批量盘点；仓库管理员可编辑，审计员只读。使用 Mock，但提供可替换 API。",
      "expected_output": "A buildable data-management app with dual runtime, typed services, Mock adapter and RBAC.",
      "files": []
    },
    {
      "id": 2,
      "prompt": "创建 expense-approval-center 费用报销审批子应用。员工查看自己的申请，经理处理待办，财务复核；详情要有流程时间线、票据摘要、意见和通过/驳回确认。应用既能独立运行也能挂到 qiankun。",
      "expected_output": "A buildable approval app with role-specific routes/actions and explicit workflow states.",
      "files": []
    },
    {
      "id": 3,
      "prompt": "生成 service-ops-console 运维监控子应用，包含服务健康概览、实例列表、日志检索、告警详情、确认告警和操作审计。值班人员可确认告警，访客只读。遵循 Ant Design v6 规范。",
      "expected_output": "A buildable monitoring app with scenario-appropriate information architecture and permissions.",
      "files": []
    }
  ]
}
```

- [ ] **Step 2: Launch six runs in one turn**

For each prompt, launch one agent with:

```text
Skill path: .cursor/skills/pkuse-design-generator
Save outputs to: .cursor/skills/pkuse-design-generator-workspace/iteration-1/<eval-name>/with_skill/outputs/
```

Launch the matching baseline without a Skill and save under `without_skill/outputs/`. Capture each completion's token and duration values immediately in its `timing.json`.

- [ ] **Step 3: Add objective assertions while runs execute**

Each `eval_metadata.json` must assert:

- `pnpm typecheck`, `pnpm test`, and `pnpm build` succeed.
- lifecycle adapter exports `bootstrap`, `mount`, and `unmount`.
- application supports standalone rendering.
- route, menu, and action permissions use shared permission declarations.
- pages import service contracts and do not import Mock fixtures.
- `ConfigProvider` exists and page code has no hard-coded color.
- loading, empty, error, and forbidden states exist.
- README lists host integration and API replacement points.

- [ ] **Step 4: Grade and aggregate**

Run deterministic build and static checks first, then write `grading.json` with exact `text`, `passed`, and `evidence` keys. Aggregate:

```bash
cd /Users/eric/.claude/skills/skill-creator
python -m scripts.aggregate_benchmark \
  /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1 \
  --skill-name pkuse-design-generator
```

Expected: `benchmark.json` and `benchmark.md` exist and list with-Skill results before baselines.

- [ ] **Step 5: Open the required review UI**

```bash
python /Users/eric/.claude/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1 \
  --skill-name "pkuse-design-generator" \
  --benchmark /Users/eric/Documents/Projects/pkuse-design-system/.cursor/skills/pkuse-design-generator-workspace/iteration-1/benchmark.json
```

Ask the user to review Outputs and Benchmark. Do not revise the Skill until human feedback is received.

