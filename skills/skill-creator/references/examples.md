# SKILL 编写示例对比

通过好/坏对比帮助理解 SKILL 编写的关键决策。

## 1. Description 编写

> **核心规则**：description 只写触发条件和排除范围，不概括 SKILL 的工作流程。测试表明 Agent 会按 description 走捷径而跳过正文。

### ✅ 好的 description

```yaml
# 只写触发条件 + 排除范围，纯英语
description: >
  Use when the user asks to write, add, or update unit tests for @moego/ui
  components, or mentions "unit test", "test coverage".
  Not for Storybook interaction tests, visual regression, or E2E.
```

分析：

- 以 "Use when" 开头，聚焦触发条件
- 激活词：write, add, update tests, "unit test", "test coverage"
- 排除范围：Not for Storybook interaction tests, visual regression, or E2E
- 没有概括 SKILL 会做什么（不写"Write or update unit tests"这类功能描述）
- 长度：约 220 字符，在理想范围内

### ❌ 差的 description

```yaml
# 问题 1：概括了工作流程 — Agent 会按此执行而跳过正文
description: >
  Guide writing Agent Skills by researching domain, planning structure,
  drafting SKILL.md, and verifying with checklist. Activate when user
  asks to create a skill.

# 问题 2：太模糊，缺少触发词和排除范围
description: Help with testing.

# 问题 3：中英混合
description: >
  为 @moego/ui 组件编写单元测试。Activate when user mentions "test".

# 问题 4：包含实现细节，太长
description: >
  Write unit tests using vitest with @testing-library/react and storybook/test
  userEvent. Tests should use act() for interactions, document.querySelector
  for Portal components, vi.fn() for callbacks...
```

---

## 2. Progressive Disclosure

### ✅ 好的拆分

```text
SKILL.md（180 行）
├── 核心原则（4 条）
├── 关键约束（5 条摘要 + 链接到 references）
├── 分类决策树
├── 维度矩阵
└── Step 1-5 流程（每步 ~20 行）

references/
├── environment-constraints.md  — 导入约定、jsdom 限制、Portal 查询、交互模式
├── test-patterns.md            — 13 个维度的代码模板
└── update-strategy.md          — 变更时的测试更新策略
```

分析：

- 正文只有决策逻辑（决策树 + 矩阵 + 流程）
- 代码模板全部在 references
- 每个 reference 文件有明确的单一职责

### ❌ 差的拆分

```text
# 问题 1：所有内容堆在 SKILL.md（450+ 行）
SKILL.md（450 行）
├── 核心原则
├── 所有代码模板（内联）
├── 所有环境约束（内联）
├── 流程步骤
└── 更新策略

# 问题 2：拆分过细，references 太多
references/
├── import-conventions.md       — 只有 10 行
├── jsdom-limits.md             — 只有 8 行
├── portal-queries.md           — 只有 15 行
├── interaction-patterns.md     — 只有 12 行
├── basic-rendering.md          — 一个维度的模板
├── slot-structure.md           — 一个维度的模板
├── classnames-override.md      — 一个维度的模板
└── ... （每个维度一个文件）
```

---

## 3. 执行流程 Step 设计

### ✅ 好的 Step

```markdown
### Step 1: Research（阅读源码）

**输入**：组件名称

**必读文件**（按优先级）：
1. `SPEC.md`（如存在）
2. `ComponentName.tsx`
3. hooks 文件
4. `ComponentName.style.ts`
5. 已有测试文件

**提取清单**（阅读时逐项记录）：
- [ ] 所有 props 及其默认值
- [ ] 所有 `data-slot` 名称
- [ ] 是否使用 Portal

**输出**：填充完毕的提取清单
```

分析：

- 输入明确（组件名称）
- 操作具体（有优先级的文件列表 + 提取清单）
- 输出明确（填充完毕的清单）
- AI 可以机械执行，不需要额外判断

### ❌ 差的 Step

```markdown
### Step 1: 了解组件

阅读组件的源码，理解它的功能和用法。注意看看有哪些 props，
组件是怎么渲染的，有没有什么特殊的地方需要注意。
```

分析：

- 没有输入/输出
- "理解"、"注意看看"、"特殊的地方"太模糊
- AI 不知道具体要提取什么信息
- 没有完成标准

---

## 4. 验证步骤

### ✅ 好的验证

```markdown
### Step 4: Verify（验证）

**运行测试**（必须非监听模式）：
\`\`\`bash
npx vitest run path/to/test.tsx --reporter=verbose
\`\`\`

**验证标准**：
- [ ] 所有测试通过
- [ ] 无 TypeScript 类型错误
- [ ] 无未使用的导入

**失败回退**：
如果测试失败，根据排查表修复后重新运行。最多 3 轮。
3 轮后仍有失败，向用户报告具体错误并请求指导。
```

### ❌ 差的验证

```markdown
### 验证

运行测试确认通过。
```

分析：

- 没有具体命令
- 没有验证标准清单
- 没有失败回退机制

---

## 5. 核心原则编写

### ✅ 好的原则

```markdown
## 核心原则

> 测试是组件的行为契约文档。好的测试回答"这个组件对外承诺了什么"，
> 而不是"内部怎么实现的"。

1. **Test Behavior, Not Implementation** — 测用户可感知的行为和公共 API 契约
2. **Minimal Reproduction** — 每个 test case 只设置触发目标行为所需的最少 props
3. **Descriptive Naming** — 测试名称即行为文档
4. **Deterministic & Isolated** — 测试之间无依赖，顺序无关
```

分析：

- 引言用一句话传达核心价值观
- 每条原则有英文关键词 + 中文解释
- 3-5 条，不多不少
- 指导 AI 在模糊场景下做出正确判断

### ❌ 差的原则

```markdown
## 原则

- 写好测试
- 覆盖率要高
- 代码要整洁
- 遵循最佳实践
```

分析：

- 太空泛，没有可操作性
- "好"、"高"、"整洁"没有定义
- 无法指导 AI 在具体场景下做决策

---

## 6. SKILL 类型结构对比

### Orchestrator 型（编排多个 Skill）

以仓库内 `superflow` 为参考：

```markdown
---
name: superflow
version: 1.3.0
description: >
  This skill should be used when the user wants to start a new feature, fix a bug,
  or run the MoeGo AI-native development workflow end-to-end. Invoke when the user
  says "开始新功能开发", "开始 bug 修复", "run superflow", or asks to scaffold a
  full development cycle from requirements to delivery.
---

# Superflow - AI Native Development Workflow

AI Native 开发工作流，编排所有 superpowers 技能形成完整流程。

## Agent 行为指令（强制）
[加载后立即启动，不询问用户]

## 核心理念
[传统 vs AI Native 对比表]

## 前置要求
[依赖的 Skill 集合及安装方式]

## 完整工作流
Phase 0: Requirements → Phase 1: Planning → Phase 2: Environment → ...

## 每个 Phase
- 使用技能：引用子 Skill 名称
- 流程：简要描述（详细逻辑在子 Skill 中）
- 退出条件：明确的完成标准

## 快速参考
[Phase → 技能 → 输出 的汇总表]
```

分析：

- 正文只放编排逻辑和 Phase 间的衔接，不重复子 Skill 的内容
- 每个 Phase 有明确的退出条件，驱动流程推进
- 前置要求明确列出依赖，Agent 可自动检查

### Ruleset 型（规则和约定集合）

以仓库内 `writing-prompts` 为参考：

```markdown
---
name: writing-prompts
version: 1.1.0
description: >
  This skill should be used when composing one-shot prompts, task instructions,
  questions, code requests, or analysis prompts to send to an LLM. Also triggers
  when the user wants to optimize an existing prompt or improve output quality.
---

# AI Prompt Writing Guide

## Scope
[一句话界定适用范围]

## P1: Format and Constraints Before Task Content
[规则 + ✅/❌ 代码示例]

## P2: Proximity — All Info for One Decision in One Block
[规则 + ✅/❌ 代码示例]

...

## Self-Check
[检查清单，对应每条规则]
```

分析：

- 每条规则独立成章，编号清晰（P1..P9）
- 每条规则都有 ✅/❌ 对比示例，AI 可直接模式匹配
- 末尾的 Self-Check 与规则编号一一对应，形成闭环
- 没有分步流程——因为规则型 SKILL 的使用方式是"查阅 + 对照"，不是"按步骤执行"

---

## 7. Only Non-Inferable 原则

### ✅ 好的内容取舍

```markdown
## 关键约束

1. Portal 组件渲染在 document.body 下，测试时必须用 `document.querySelector`
   而非 `within(container)` 查询
2. 使用 `act()` 包裹所有触发状态更新的交互操作
```

分析：

- 这些是 Agent 无法从组件源码中自行推断的测试环境限制
- 不写的话 Agent 大概率会用错误的查询方式

### ❌ 差的内容取舍

```markdown
## 关键约束

1. 使用 `import { render } from '@testing-library/react'` 渲染组件
2. 使用 `expect(element).toBeInTheDocument()` 断言元素存在
3. 测试文件放在 `__tests__` 目录下
4. 使用 `describe` 和 `it` 组织测试
```

分析：

- 这些是 vitest + testing-library 的通用用法，Agent 完全能自行推断
- 写入 SKILL 只会浪费 token，不提供额外价值
- ETH Zurich 研究表明：可推断的上下文反而降低 Agent 性能

---

## 8. 反合理化模式（纪律执行型 SKILL）

纪律执行型 SKILL（强制规则类，如 TDD、code-review）需要预判 Agent 在压力下的合理化行为并主动堵漏。

### ✅ 好的反合理化设计

```markdown
## Red Flags — 发现以下念头时立即停下

- 已经写了代码再补测试
- "手动验证过了，不需要自动化测试"
- "这次情况特殊，可以跳过"
- "用户说不需要，所以我不做"
- "精神上遵守了，只是字面上略有不同"

**以上全部意味着：删除代码，从头开始。**

| 借口 | 反驳 |
| ---- | ---- |
| "太简单不需要测试" | 简单的代码也会出错，测试只需 30 秒 |
| "先写后测效果一样" | 先写测试 = "应该做什么"；后补测试 = "做了什么"，本质不同 |
| "用户要求跳过" | 质量标准不因用户要求而降低 |

**违反规则的字面意思就是违反规则的精神。**
```

分析：

- Red Flags 清单让 Agent 能自检"正在合理化"
- 借口-反驳表针对具体的逃避模式
- "字面 = 精神"声明堵住了整类漏洞
- 最终行动明确（删除代码，从头开始）

### ❌ 差的反合理化设计

```markdown
## 注意事项

请遵守规则，不要跳过步骤。
```

分析：

- 没有列出具体的合理化借口
- Agent 在压力下会轻松绕过这种模糊声明
- 没有提供自检机制

---

## 9. Token 压缩技巧

SKILL 正文有 ≤ 1,500 词的限制，以下技巧帮助在有限空间内传递最大信息量。

### 用交叉引用替代重复

```markdown
# ❌ 差：在 SKILL 中重复其他 Skill 的内容
当搜索时，启动子 Agent，使用以下模板...
[20 行重复的指令]

# ✅ 好：引用其他 Skill
子 Agent 调度流程见 [references/subagent-dispatch.md](references/subagent-dispatch.md)。
```

### 用工具 --help 替代参数文档

```markdown
# ❌ 差：在 SKILL 中列举所有参数
search-conversations 支持 --text, --both, --after DATE, --before DATE, --limit N...

# ✅ 好：引导查看帮助
search-conversations 支持多种模式和过滤器，运行 --help 查看详情。
```

### 压缩示例

```markdown
# ❌ 差：冗长示例（42 词）
用户："之前 React Router 的认证错误是怎么处理的？"
Agent："我来搜索过去的对话，查找 React Router 认证相关的模式。"
[启动子 Agent，搜索查询："React Router authentication error handling 401"]

# ✅ 好：最小示例（15 词）
用户："React Router 认证错误怎么处理的？"
→ 启动子 Agent 搜索 → 综合结果
```

### 核心原则

- 一个优秀的示例胜过多个平庸的示例
- 可从代码/文档推断的内容不写入 SKILL
- 代码模板放 references，正文只放决策逻辑
