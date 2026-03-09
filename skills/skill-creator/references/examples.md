# SKILL 编写示例对比

通过好/坏对比帮助理解 SKILL 编写的关键决策。

## 1. Description 编写

### ✅ 好的 description

```yaml
# 三要素齐全，简洁精准，纯英语
description: >
  Write or update unit tests for @moego/ui components. Activate when the user
  asks to write, add, or update tests, or mentions "unit test", "test coverage".
  Not for Storybook interaction tests, visual regression, or E2E.
```

分析：

- 做什么：Write or update unit tests for @moego/ui components
- 激活词：write, add, update tests, "unit test", "test coverage"
- 不做什么：Not for Storybook interaction tests, visual regression, or E2E
- 长度：约 220 字符，在理想范围内

### ❌ 差的 description

```yaml
# 问题 1：太模糊，缺少触发词和排除范围
description: Help with testing.

# 问题 2：中英混合
description: >
  为 @moego/ui 组件编写单元测试。Activate when user mentions "test".

# 问题 3：包含实现细节，太长
description: >
  Write unit tests using vitest with @testing-library/react and storybook/test
  userEvent. Tests should use act() for interactions, document.querySelector
  for Portal components, vi.fn() for callbacks. Support controlled/uncontrolled
  patterns with rerender, classNames override with slot helpers, deprecated
  props compatibility testing, and ARIA attribute verification. Activate when
  the user asks to write tests or mentions "unit test", "test coverage",
  "testing". Not for Storybook interaction tests or E2E tests.
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

## 8. 效果评估：子 Agent A/B 对比测试

SKILL 写完后，除了格式检查，还应通过子 Agent 做隔离的 A/B 对比测试来评估实际效果。参考 [LangChain Evaluating Skills](https://blog.langchain.com/evaluating-skills/) 的方法论。

### 为什么必须用子 Agent

直接让当前 Agent 自己评估"有没有效果"，它会脑补一个结论。子 Agent 的上下文是隔离的——Agent A 完全不知道 SKILL 的存在，Agent B 只知道 SKILL 告诉它的内容。这样差异才真实。

### 操作步骤

#### 1. 定义 2-3 个代表性任务

选 SKILL 目标领域内的典型场景，覆盖不同子类型。例如对 skill-creator：

- 任务 1："帮我创建一个 code-review 的 SKILL"（从零创建，Ruleset 型）
- 任务 2："审查 e2e 这个 SKILL 有没有问题"（审查现有，Workflow 型）

#### 2. 每个任务跑两个子 Agent

**子 Agent A（无 SKILL 基线）**：prompt 只给任务描述 + AGENTS.md，不提供 SKILL 的任何文件。

```text
prompt 模板：

你是一个 AI 编码助手。以下是项目的 AGENTS.md：
<agents_md>
[AGENTS.md 全文]
</agents_md>

任务：[任务描述]

要求：不要读取或修改任何文件，只输出你的方案文本。
```

**子 Agent B（有 SKILL）**：prompt 给任务描述 + AGENTS.md + SKILL 全套文件（SKILL.md + 所有 references）。

```text
prompt 模板：

你是一个 AI 编码助手。以下是项目的 AGENTS.md：
<agents_md>
[AGENTS.md 全文]
</agents_md>

以下是你必须遵循的 SKILL 编写指南及其参考文档：
<skill_md>
[SKILL.md 全文]
</skill_md>
<specification>
[references/specification.md 全文]
</specification>
<checklist>
[references/writing-checklist.md 全文]
</checklist>
<examples>
[references/examples.md 全文（排除本节内容避免递归）]
</examples>

任务：[任务描述]

要求：不要读取或修改任何文件，严格按照 SKILL 编写指南执行，只输出方案文本。
```

关键：两个子 Agent 的任务描述必须完全相同，只有上下文不同。

#### 3. 对比评估

对每组 A/B 输出，逐项打分：

| 评估维度               | 检查方法                                              | 权重 |
| ---------------------- | ----------------------------------------------------- | ---- |
| Frontmatter 合规       | name/version/description 是否符合规范                 | 高   |
| Description 质量       | 是否包含三要素、纯英语、长度合理                      | 高   |
| 结构合理性             | 是否选择了正确的 SKILL 类型和对应结构                 | 高   |
| 流程可执行性           | 每个 Step 是否有输入/操作/输出                        | 中   |
| 验证闭环               | 是否有验证步骤和失败回退                              | 中   |
| Progressive Disclosure | 是否合理拆分正文和 references                         | 中   |
| 信息密度               | 是否只包含 Agent 无法自行推断的内容                   | 低   |
| 项目约定遵守           | 禁止项（triggers、moego- 前缀、硬编码凭证等）是否遵守 | 高   |

#### 4. 判定与迭代

- B 在多数高权重维度明显优于 A → SKILL 有效
- A/B 差异不大 → SKILL 内容可能冗余，需精简
- B 在某些维度反而更差 → SKILL 中有误导性内容，需修正

### 信息密度测试（可选）

对 SKILL 中的每个主要章节，删除后重跑子 Agent B：

- 删除后输出质量不变 → 该章节冗余，考虑删除
- 删除后输出质量下降 → 该章节有价值，保留
