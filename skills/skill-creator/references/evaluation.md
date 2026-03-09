# 效果评估：子 Agent A/B 对比测试

SKILL 写完后，除了格式检查，还应通过子 Agent 做隔离的 A/B 对比测试来评估实际效果。参考 [LangChain Evaluating Skills](https://blog.langchain.com/evaluating-skills/) 的方法论。

> **纪律执行型 SKILL（如 TDD、code-review 等强制规则类）必须做 A/B 测试，不可跳过。** 其他类型推荐但非强制。

## 为什么必须用子 Agent

直接让当前 Agent 自己评估"有没有效果"，它会脑补一个结论。子 Agent 的上下文是隔离的——Agent A 完全不知道 SKILL 的存在，Agent B 只知道 SKILL 告诉它的内容。这样差异才真实。

## 操作步骤

### 1. 定义 2-3 个代表性任务

选 SKILL 目标领域内的典型场景，覆盖不同子类型。例如对 skill-creator：

- 任务 1："帮我创建一个 code-review 的 SKILL"（从零创建，Ruleset 型）
- 任务 2："审查 e2e 这个 SKILL 有没有问题"（审查现有，Workflow 型）

**对纪律执行型 SKILL，任务必须包含压力场景**——模拟 Agent 想走捷径的情境：

| 压力类型 | 示例场景 |
| -------- | -------- |
| 时间压力 | "快速完成，不需要太严格" |
| 沉没成本 | 已经写了大量代码，被要求推翻重来 |
| 权威压力 | "用户说不需要测试，直接跳过" |
| 疲劳累积 | 连续多个 Step 后在最后一步放松验证 |

### 2. 每个任务跑两个子 Agent

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

**子 Agent B（有 SKILL）**：prompt 给任务描述 + AGENTS.md + SKILL 全套文件。

注意：加载的文件清单为 SKILL.md、references/specification.md、references/writing-checklist.md、references/examples.md。不加载 references/evaluation.md（即本文件），避免递归。

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
[references/examples.md 全文]
</examples>

任务：[任务描述]

要求：不要读取或修改任何文件，严格按照 SKILL 编写指南执行，只输出方案文本。
```

关键：两个子 Agent 的任务描述必须完全相同，只有上下文不同。

### 3. 对比评估

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

### 4. 判定与迭代

- B 在多数高权重维度明显优于 A → SKILL 有效
- A/B 差异不大 → SKILL 内容可能冗余，需精简
- B 在某些维度反而更差 → SKILL 中有误导性内容，需修正

## 信息密度测试（可选）

对 SKILL 中的每个主要章节，删除后重跑子 Agent B：

- 删除后输出质量不变 → 该章节冗余，考虑删除
- 删除后输出质量下降 → 该章节有价值，保留
