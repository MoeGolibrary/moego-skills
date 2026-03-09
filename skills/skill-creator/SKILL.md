---
name: skill-creator
description: >
  Guide writing, reviewing, and refactoring Agent Skills (SKILL.md).
  Activate when the user asks to create, write, review, or improve a SKILL,
  or mentions "skill authoring", "write a skill", "improve skill", "skill best practices".
  Not for using or invoking existing skills, nor for writing general prompts or documentation.
---

# SKILL 编写指南

指导编写符合 Agent Skills 开放标准的 SKILL.md 文件——让 AI 助手能准确识别、激活并执行特定领域任务。

## 核心原则

> SKILL 是 AI 助手的能力模块。好的 SKILL 回答"什么时候激活、怎么执行、怎么验证"，而不是堆砌所有可能用到的知识。

1. **Progressive Disclosure** — 三层渐进式加载：metadata (~100 tokens) → instructions (≤ 1,500 词) → resources (按需)
2. **Body 精简** — SKILL.md 的 frontmatter + 核心指令部分 ≤ 1,500 词，超出部分拆到 `references/`
3. **Trigger 精准** — `description` 必须明确说明"做什么 + 什么时候激活 + 不做什么"
4. **Workflow 可执行** — 每个 Step 有明确的输入、操作、输出，AI 可机械执行
5. **Verify 闭环** — 必须有验证步骤和失败回退机制
6. **Only Non-Inferable** — 只写 Agent 无法从代码/文档中自行推断的信息；过多上下文反而降低 Agent 性能（参见 [ETH Zurich 研究](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)）

---

## 关键约束

在编写任何 SKILL 前必须内化以下约束。详细的字段规范见 [references/specification.md](references/specification.md)。

- **Frontmatter 必填**：`name`（kebab-case，1-64 字符，与目录名一致）、`version`（语义化版本号）和 `description`（1-1024 字符，纯英语）
- **description 三要素**：做什么 + 激活关键词 + 不做什么（负面触发）
- **目录结构**：源文件在 `skills/<name>/`，脚本路径引用 `${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/`
- **正文长度**：frontmatter + 核心指令部分 ≤ 1,500 词（references/ 不计入）
- **正文语言**：SKILL.md 正文和 references 建议使用中文；frontmatter `description` 必须使用英语
- **引用路径**：references 中的文件用相对路径引用，如 `[references/xxx.md](references/xxx.md)`
- **禁止项**：不使用 `triggers` 字段；`name` 不加 `moego-` 前缀；脚本不硬编码凭证或 API Key
- **已弃用内容零提及**：全文不出现 `deprecated`、`废弃`、`已弃用`

---

## SKILL 结构决策树

```text
目标领域是否有明确的分步执行流程？
├─ 是 → 是否主要编排/调度其他 Skill？
│       ├─ 是 → Orchestrator 型 SKILL（如 superflow）
│       │       结构：核心理念 → 前置要求 → Phase 1..N 流程（每 Phase 引用子 Skill）→ 快速参考表
│       │
│       └─ 否 → Workflow 型 SKILL（如 component-unit-testing, code-to-spec）
│               结构：核心原则 → 约束/Edge Cases → 分类矩阵（如有）→ Step 1..N 流程
│
└─ 否 → 目标领域是否主要是规则和约定？
         ├─ 是 → Ruleset 型 SKILL（如 writing-prompts, code-review）
         │       结构：核心原则 → 规则表 → 示例（✅/❌）→ 检查清单
         │
         └─ 否 → Knowledge 型 SKILL（如 architecture-guide）
                  结构：核心原则 → 知识图谱/决策树 → 常见场景 → FAQ
```

---

## 执行流程

### Step 0: Research（调研）

**输入**：用户描述的 SKILL 目标领域

**操作**：

1. 确认目标领域的核心任务和边界
2. 收集该领域的关键约束、常见 edge cases、最佳实践
3. 如果是重构现有 SKILL，阅读现有文件并评估问题
4. 阅读 [references/specification.md](references/specification.md) 确认 frontmatter 规范
5. 评估信息密度——对每条候选内容问："Agent 能否从代码/文档中自行推断？"如果能，不写入 SKILL

**输出**：领域知识摘要 + SKILL 类型判定（Workflow / Ruleset / Knowledge）

### Step 1: Plan（规划结构）

**输入**：Step 0 的调研结果

**操作**：

1. 根据 SKILL 类型选择结构模板
2. 规划 SKILL.md 正文章节（控制在 500 行内）
3. 规划 `references/` 拆分方案——将代码模板、详细规范、示例等大块内容拆出
4. 确认正文 ≤ 1,500 词（references/ 不计入）
5. 列出文件清单和每个文件的职责

**输出**：文件清单 + 各文件章节大纲

### Step 2: Draft（撰写）

**输入**：Step 1 的结构规划

**操作**：

1. 编写 frontmatter（参照 [references/specification.md](references/specification.md)）
2. 编写 SKILL.md 正文
3. 编写 references 文件
4. 创建软链接

**写作规则**：

- 每个 Step 必须有「输入」「操作」「输出」三段
- Edge cases 集中在正文顶部，不散落在各 Step 中
- 代码模板放 references，正文只放决策逻辑
- 验证步骤必须包含失败回退（最多 N 轮 + 上报用户）
- 只写 Agent 无法自行推断的内容——可推断的常识、通用编码规范不写入
- 脚本使用环境变量获取凭证，不硬编码 API Key 或密码
- 全文不出现 `deprecated`、`废弃`、`已弃用`

**输出**：完整的 SKILL 文件集

### Step 3: Verify（校验）

**输入**：Step 2 的文件集

**对照 [references/writing-checklist.md](references/writing-checklist.md) 逐项检查。**

重点验证：

- [ ] frontmatter + 核心指令部分 ≤ 1,500 词
- [ ] frontmatter `name` 与目录名一致，无 `moego-` 前缀
- [ ] frontmatter 包含 `version` 字段
- [ ] 无 `triggers` 字段
- [ ] `description` 纯英语，包含三要素
- [ ] 每个 Step 有输入/操作/输出
- [ ] 有验证步骤和失败回退
- [ ] references 引用路径正确
- [ ] 脚本不硬编码凭证，使用环境变量
- [ ] 全文不出现 `deprecated`、`废弃`、`已弃用`
- [ ] 运行 `install.sh` 确认 adapter symlink 正确

**失败回退**：发现问题则修正后重新检查，最多 2 轮。

**输出**：通过检查的最终文件集

### Step 4: Deliver（交付）

向用户报告：

- 创建的文件列表
- SKILL 的激活方式和触发关键词
- 需要用户关注的设计决策（如有）
