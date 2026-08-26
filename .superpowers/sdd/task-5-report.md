# Task 5 报告：静态与可执行校验器

## 状态

完成（含第六轮 Important 修复）。未初始化 Git，未创建提交。

---

## GREEN（最终）

### 单元测试（64 项）

命令：

```text
python -m unittest discover \
  -s .cursor/skills/pkuse-design-generator/tests \
  -p 'test_validate.py' -v
```

关键输出：

```text
Ran 64 tests in 0.376s
OK
```

**TokenizerTest（7）** — 同第五轮

**ValidateTest（57）** — 第五轮 52 项基础上新增：
- `test_rejects_config_provider_with_span_placeholder`
- `test_rejects_config_provider_with_only_antd_app`
- `test_accepts_config_provider_with_router_provider_outlet`
- `test_accepts_config_provider_with_routes_outlet`
- `test_accepts_config_provider_with_children_prop_outlet`

完整清单见第五轮报告；其余 52 项名称不变。

### 干净 fixture 可执行校验

```text
python .cursor/skills/pkuse-design-generator/scripts/scaffold.py \
  --name inventory-console --title "库存中心" --scene data-management \
  --output /tmp/pkuse-inventory-console-validate-r6
cd /tmp/pkuse-inventory-console-validate-r6 && pnpm install

python .cursor/skills/pkuse-design-generator/scripts/validate.py \
  /tmp/pkuse-inventory-console-validate-r6
# exit: 0

python .cursor/skills/pkuse-design-generator/scripts/validate.py \
  /tmp/pkuse-inventory-console-validate-r6 \
  --run-commands --vite-public-base "https://cdn.example.com/inventory/"
# typecheck / test(16) / build / build:qiankun 均 exit 0
# exit: 0
```

### 第六轮实现要点

| 模块 | 内容 |
| --- | --- |
| **ConfigProvider 出口** | Provider 匹配范围内必须含实际应用出口之一：`<AppContent />`、`<RouterProvider />`、`<Routes>`、`{children}`（children 须为函数参数/props 真实标识）；span/div/AntdApp 占位不算 |

---

## 历史（RED 历程，非最终结论）

<details>
<summary>第一～五轮 → 10/23/43/51/59 测试</summary>

lifecycle、tokenize、CSS 声明 value、命令 mock、ConfigProvider 开闭标签等逐步完善。
</details>

---

## 关注事项

1. **词法器非完整 TS parser**：出口检测基于 JSX 标签名与 `{children}` 标识符匹配。
2. **CSS 解析**：基于 `{...}` 块与 `;` 分声明，未覆盖全部 at-rule 变体。
3. **`{children}` 出口**：仅接受参数列表中声明的 `children` 标识符，不含 props.xxx 形式。
4. **Mock 白名单**：`src/micro-app/**` + `src/app/services.ts`。
5. **命令测试全 mock**：不依赖宿主 pnpm；集成 fixture 需预 `pnpm install`。
