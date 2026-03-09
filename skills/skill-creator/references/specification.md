# Agent Skills Frontmatter 规范

基于 [Agent Skills 开放标准](https://agentskills.io/specification) 整理的字段约束。

## 必填字段

| 字段          | 类型   | 约束                                                    | 示例                          |
| ------------- | ------ | ------------------------------------------------------- | ----------------------------- |
| `name`        | string | 1-64 字符，kebab-case，必须与目录名一致                 | `component-unit-testing`      |
| `version`     | string | 语义化版本号（SemVer）                                  | `1.0.0`                       |
| `description` | string | 1-1024 字符，描述 SKILL 的功能、触发条件和排除范围      | 见下方 description 编写指南   |

## 可选字段

| 字段            | 类型     | 说明                                           |
| --------------- | -------- | ---------------------------------------------- |
| `license`       | string   | SPDX 许可证标识符，如 `MIT`、`Apache-2.0`      |
| `compatibility` | string[] | 兼容的 AI 助手列表，如 `["claude", "copilot"]` |
| `metadata`      | object   | 自定义键值对，用于扩展信息                     |
| `allowed-tools` | string[] | SKILL 允许使用的工具列表                       |

## `name` 字段规则

```text
✅ component-unit-testing     — kebab-case，与目录名一致
✅ code-to-spec-writing       — 描述性命名
✅ skill-authoring             — 简洁明了

❌ ComponentUnitTesting        — 不是 kebab-case
❌ unit_testing                — 下划线不符合 kebab-case
❌ test                        — 太模糊，不具描述性
❌ my-super-awesome-skill-v2   — 超过必要长度，避免版本号
```

## `description` 编写指南

description 是 AI 助手判断是否激活 SKILL 的唯一依据。必须包含三个要素：

### 1. 做什么（What）

一句话说明 SKILL 的核心功能。

### 2. 激活关键词（When）

列出用户可能使用的触发词和短语，帮助 AI 匹配。

### 3. 不做什么（Not）

明确排除范围，避免误激活。

### 格式模板

```yaml
description: >
  [做什么的一句话描述]。Activate when the user asks to [触发动作],
  or mentions "[关键词1]", "[关键词2]", "[关键词3]".
  Not for [排除范围1], [排除范围2], or [排除范围3].
```

### 示例对比

```yaml
# ✅ 好的 description — 三要素齐全，简洁精准
description: >
  Write or update unit tests for @moego/ui components. Activate when the user
  asks to write, add, or update tests, or mentions "unit test", "test coverage".
  Not for Storybook interaction tests, visual regression, or E2E.

# ❌ 差的 description — 缺少触发词和排除范围
description: >
  This skill helps with testing components.

# ❌ 差的 description — 中英混合
description: >
  为组件编写单元测试。Activate when user mentions "test".

# ❌ 差的 description — 太长，包含实现细节
description: >
  Write unit tests for React components using vitest and @testing-library/react
  with storybook/test userEvent, supporting Portal components with document
  queries, controlled/uncontrolled patterns, classNames override testing,
  deprecated props compatibility, and accessibility attribute verification.
  Activate when...
```

### 长度控制

- 目标：150-300 字符
- 上限：1024 字符（标准硬限制）
- 超过 300 字符时检查是否包含了不必要的实现细节

## 目录结构

```text
skills/<name>/
├── SKILL.md                    # 主文件：frontmatter + 核心流程（≤ 1,500 词）
├── references/                 # 按需加载的详细内容
│   ├── xxx.md                  # 代码模板、详细规范等
│   └── yyy.md
├── scripts/                    # 可选：自动化脚本
└── assets/                     # 可选：图片等静态资源
```

### 脚本路径约定

脚本路径使用 `${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/` 引用。

### 多工具适配

Plugin System 通过 `install.sh` 自动为 Codex/OpenCode 创建 adapter symlink，无需手动创建软链接。修改 Skill 后运行 `install.sh` 验证 adapter symlink 正确。

## Progressive Disclosure 三层模型

```text
Layer 1: Metadata（~100 tokens）
  └─ frontmatter: name + description
  └─ AI 助手用此判断是否激活

Layer 2: Instructions（≤ 1,500 词）
  └─ SKILL.md 正文
  └─ 激活后加载，包含核心流程和决策逻辑

Layer 3: Resources（按需加载）
  └─ references/ 目录下的文件
  └─ 执行具体 Step 时按需读取
```

关键：Layer 2 只放决策逻辑和流程框架，具体的代码模板、详细规范、示例集合放 Layer 3。
