---
name: moego:superflow
description: AI Native 开发工作流 - 从需求到交付的完整流程，包含 brainstorming、planning、TDD 执行、双阶段审查和验证门控
triggers:
  - /moego:superflow
  - 开始新功能开发
  - 开始 bug 修复
---

# Superflow - AI Native Development Workflow

AI Native 开发工作流，编排所有 superpowers 技能形成完整流程。

## Agent 行为指令（强制）

**当此技能被加载时，立即启动工作流。不要询问用户想做什么。**

行为规则：
1. **有明确任务描述** → 直接从 Phase 0 (brainstorming) 开始，围绕该任务展开
2. **无任务描述（仅加载技能）** → 直接开始 Phase 0，询问用户要开发什么功能/修复什么 bug
3. **永远不要** 问 "你想启动工作流吗？" 或 "你想从哪个阶段开始？"

错误示例（禁止）：
```
你加载了 superflow 工作流技能。你想要：
1. 启动完整工作流
2. 了解工作流
3. 从特定阶段开始
```

正确示例：
```
[执行启动前检查...]
[检查 superpowers 是否安装...]

开始 Phase 0: Requirements

你要开发什么功能？请简要描述。
```

---

## 启动前检查（Agent 必须执行）

**在开始工作流之前，必须检查 superpowers 是否已安装：**

```bash
# 检查 superpowers 是否存在
ls ~/.config/opencode/superpowers/skills 2>/dev/null || ls ~/.claude/superpowers/skills 2>/dev/null
```

**如果不存在，询问用户是否安装：**

```
检测到 superpowers 技能集未安装。superflow 依赖它来运行完整工作流。

是否现在安装？
1. 是，帮我安装
2. 否，我稍后手动安装
```

**如果用户选择安装，执行：**

```bash
# OpenCode
git clone https://github.com/obra/superpowers ~/.config/opencode/superpowers

# Claude Code (如果适用)
git clone https://github.com/obra/superpowers ~/.claude/superpowers
```

**安装完成后，继续工作流。**

---

## 核心理念

| 传统开发 | AI Native |
|----------|-----------|
| 人写代码，人审查 | AI 写代码，AI 审查，人决策 |
| 串行执行 | 并行子代理 |
| 手动验证 | 自动化验证门控 |
| 事后测试 | TDD 强制 |
| 凭感觉完成 | 证据驱动完成 |

## 前置要求

此工作流依赖 [superpowers](https://github.com/obra/superpowers) 技能集。Agent 会在启动时自动检查并提示安装。

手动安装方式：
```bash
# OpenCode
git clone https://github.com/obra/superpowers ~/.config/opencode/superpowers

# Claude Code
git clone https://github.com/obra/superpowers ~/.claude/superpowers
```

## 完整工作流

```
Phase 0: Requirements (brainstorming)
         ↓
Phase 1: Planning (writing-plans)
         ↓
Phase 1.5: E2E Planning (moego:e2e) [自动判断]
         ↓
Phase 2: Environment (using-git-worktrees)
         ↓
Phase 3: Execution (subagent-driven-development)
         ↓
Phase 3.5: E2E Implementation (moego:e2e) [自动触发]
         ↓
Phase 4: Completion (verification + finishing)
```

---

## Phase 0: Requirements

**使用技能:** `superpowers:brainstorming`

**流程:**
1. 检查项目上下文（文件、文档、最近提交）
2. 一次问一个问题（优先多选题）
3. 提出 2-3 个方案，带权衡分析
4. 200-300 字分段呈现设计，逐段确认
5. 输出：`docs/plans/YYYY-MM-DD-<topic>-design.md`

**退出条件:** 设计文档已提交到 git

---

## Phase 1: Planning

**使用技能:** `superpowers:writing-plans`

**流程:**
1. 假设执行者零上下文
2. 创建 bite-sized 任务（每步 2-5 分钟）
3. 每步包含：文件路径、代码、验证命令、预期输出
4. 输出：`docs/plans/YYYY-MM-DD-<feature>.md`

**退出条件:** 实现计划已定义所有任务

---

## Phase 1.5: E2E Planning（自动触发）

**使用技能:** `moego:e2e` (Plan 模式)

**自动触发条件:** Agent 根据 Phase 0/1 的内容判断是否需要 E2E 测试：

| 需要 E2E | 不需要 E2E |
|----------|------------|
| 涉及 UI 交互、页面、用户流程 | 纯后端 API、工具类、脚本 |
| 新增/修改前端功能 | 重构、性能优化（无行为变更） |
| 用户可见的行为变更 | 配置变更、依赖升级 |
| Plan 中提到"页面"、"表单"、"按钮"等 | Plan 中无 UI 相关描述 |

**如果判断需要 E2E：**

1. 自动调用 `moego:e2e` 技能的 Plan 模式
2. 基于设计文档和实现计划生成测试场景
3. 输出 E2E 测试计划（场景清单 + 优先级 + 数据策略）
4. 将 E2E 任务追加到实现计划中

**如果判断不需要 E2E：**

直接跳过，进入 Phase 2。

**退出条件:** E2E 测试计划已生成（或自动判断为不需要）

---

## Phase 2: Environment

**使用技能:** `superpowers:using-git-worktrees`

**流程:**
1. 创建隔离 worktree
2. 安装依赖
3. 验证基线测试通过

**退出条件:** 干净工作区，测试通过

---

## Phase 3: Execution

**使用技能:** `superpowers:subagent-driven-development`

### Per-Task Loop

```
┌─────────────────────────────────────────────────────────┐
│  1. Dispatch Implementer 子代理                          │
│     - 提供完整任务文本 + 上下文                            │
│     - 遵循 TDD: RED → GREEN → REFACTOR                  │
│     - 自审 + 提交                                        │
├─────────────────────────────────────────────────────────┤
│  2. Dispatch Spec Reviewer 子代理                        │
│     - 检查：是否符合规格？                                 │
│     - 检查：是否多做/少做？                                │
│     - 不通过 → Implementer 修复 → 重审                    │
├─────────────────────────────────────────────────────────┤
│  3. Dispatch Code Quality Reviewer 子代理                │
│     - 检查：代码质量                                      │
│     - 不通过 → Implementer 修复 → 重审                    │
├─────────────────────────────────────────────────────────┤
│  4. Mark task complete                                  │
│     - 仅在双阶段审查都通过后                               │
└─────────────────────────────────────────────────────────┘
```

### 支持技能

| 场景 | 技能 |
|------|------|
| 遇到 Bug | `superpowers:systematic-debugging` |
| 多个独立问题 | `superpowers:dispatching-parallel-agents` |

---

## Phase 3.5: E2E Implementation（自动触发）

**使用技能:** `moego:e2e` (Impl 模式)

**自动触发条件:** Phase 1.5 生成了 E2E 测试计划。

**流程:**
1. 读取 E2E 测试计划
2. 检索现有 Page Object / Utils
3. 生成/扩展测试代码
4. 应用 MoeGo E2E 最佳实践
5. 输出：`.spec.ts` 文件 + Page Object

**退出条件:** E2E 测试代码已生成并通过

---

## Phase 4: Completion

### 验证

**使用技能:** `superpowers:verification-before-completion`

**Iron Law:** 无证据不能声明完成。

```
1. IDENTIFY: 什么命令能证明这个声明？
2. RUN: 执行完整命令
3. READ: 完整输出，检查退出码
4. VERIFY: 输出是否确认声明？
5. ONLY THEN: 做出声明
```

### 完成

**使用技能:** `superpowers:finishing-a-development-branch`

**流程:**
1. 验证所有测试通过
2. 呈现 4 个选项：
   - 本地合并
   - 推送并创建 PR
   - 保持原样
   - 丢弃
3. 执行选择
4. 清理 worktree

---

## 快速参考

| Phase | 技能 | 输出 |
|-------|------|------|
| 0. Requirements | brainstorming | 设计文档 |
| 1. Planning | writing-plans | 实现计划 |
| 1.5. E2E Planning | moego:e2e (Plan) | E2E 测试计划 |
| 2. Environment | using-git-worktrees | 干净工作区 |
| 3. Execution | subagent-driven-development | 可工作代码 |
| 3.5. E2E Impl | moego:e2e (Impl) | E2E 测试代码 |
| 4. Completion | verification + finishing | 合并/PR 的代码 |

---

## AI Native 优势

| 能力 | 如何利用 |
|------|----------|
| **并行** | `dispatching-parallel-agents` 处理独立问题 |
| **无状态** | 每任务新子代理，无上下文污染 |
| **不疲劳** | 每任务双阶段审查（Spec + Quality） |
| **一致性** | TDD 强制执行，不会"偷懒跳过" |
| **可验证** | `verification-before-completion` 门控 |

---

## 最小可行工作流

如果完整流程太重，从这个开始：

```
1. brainstorming     → 确认要做什么
2. writing-plans     → 写出 bite-sized 任务
3. TDD 执行每个任务   → RED → GREEN → REFACTOR
4. verification      → 跑命令，看证据
5. 完成
```

**核心:** TDD + 验证门控。这两个不能省。

---

## Red Flags - STOP

- 跳过 brainstorming（"我知道要做什么"）
- 跳过 planning（"很简单"）
- 跳过 worktree（"我直接在 main 上改"）
- 跳过 reviews（"代码看起来没问题"）
- 没有验证证据就声明完成

**以上任何一条都意味着：STOP。遵循工作流。**

---

## 相关技能

| 技能 | 用途 |
|------|------|
| `superpowers:brainstorming` | 需求探索和设计 |
| `superpowers:writing-plans` | 编写实现计划 |
| `superpowers:using-git-worktrees` | 创建隔离工作区 |
| `superpowers:subagent-driven-development` | 子代理驱动执行 |
| `superpowers:test-driven-development` | TDD 流程 |
| `superpowers:systematic-debugging` | 系统化调试 |
| `superpowers:dispatching-parallel-agents` | 并行代理调度 |
| `superpowers:verification-before-completion` | 完成前验证 |
| `superpowers:finishing-a-development-branch` | 完成开发分支 |
| `superpowers:requesting-code-review` | 请求代码审查 |
| `superpowers:receiving-code-review` | 接收代码审查 |
| `moego:e2e` | E2E 测试规划与实现 |
