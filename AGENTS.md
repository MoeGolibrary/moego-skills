# AGENTS.md

MoeGo 研发团队 AI Agent Plugin 仓库。为 AI 编码代理提供可扩展的 Skills 集合，具体 Skill 列表见 `skills/` 目录下各子目录的 `SKILL.md`。

## 仓库结构

```text
.claude-plugin/             # Plugin manifest + Marketplace 配置
skills/<name>/SKILL.md      # Skill 定义（每个 Skill 一个目录）
skills/<name>/references/   # Skill 参考文档（按需加载，不常驻上下文）
skills/<name>/scripts/      # Skill 脚本（bash/python）
adapters/                   # 非 Claude Code 工具的安装适配（Codex/OpenCode/Cursor）
bin/                        # CLI 管理命令
hooks/hooks.json            # 预留：会话级 hook
docs/adr/                   # 架构决策记录
install.sh                  # 兼容旧有安装流程的脚本（依赖 bin/）
```

## Skill 开发

### 命名规则

- `plugin.json` 中 `"name": "moego"` — Plugin 命名空间
- SKILL.md 的 `name` 字段使用 bare name（如 `superflow`），不加 `moego-` 前缀
- Claude Code 自动拼接为 `/moego:<skill-name>`
- Codex/OpenCode 通过 adapter symlink 获得 `moego-<skill-name>` 别名

### 创建新 Skill

1. 创建目录 `skills/<your-skill>/`
2. 创建 `SKILL.md`，frontmatter 格式：

   ```yaml
   ---
   name: your-skill
   version: 1.0.0
   description: >
     This skill should be used when the user asks to [specific trigger conditions].
   ---
   ```

3. Body 使用祈使句，SKILL.md 的 frontmatter + 核心指令部分 ≤ 1,500 词（`references/` 目录下的文件不计入此限制）
4. 脚本放 `skills/<your-skill>/scripts/`，路径引用 `${CLAUDE_PLUGIN_ROOT}/skills/<your-skill>/scripts/`
5. 验证：确认 SKILL.md 的 `name` 字段无 `moego-` 前缀，无 `triggers` 字段
6. 验证：运行 `install.sh` 确认新 Skill 能正确创建 adapter symlink

### SKILL.md 写作约束

- description 字段强制使用英文编写（Agent 据此判断何时加载）
- 不使用 `triggers` 字段 — 由 Plugin System 接管
- references/ 下的文件用于 Progressive Disclosure，降低每次推理的固定 token 开销
- 已弃用内容零提及 — 全文不出现 `deprecated`、`废弃`、`已弃用`

## 代码风格

- 文件编码：UTF-8（无 BOM）
- Markdown：标准 Markdown，代码块用反引号包裹
- Shell 脚本：`#!/usr/bin/env bash`，`set -e`
- Python 脚本：使用 `uv run` 执行（[uv 安装指南](https://docs.astral.sh/uv/getting-started/installation/)），依赖 `requests`、`python-dateutil`
- 文档语言：中文（SKILL.md 的 description 字段用英文，Body 可中文）

## 提交规范

- 格式：`type(scope): description`
- type：`feat` / `fix` / `refactor` / `docs` / `chore`
- scope：skill 名称或模块名，如 `superflow`、`e2e`、`datadog`、`plugin`
- 示例：`feat(e2e): add Page Object for grooming appointment`

## 禁止操作

- 不修改 `.claude-plugin/plugin.json` 的 `name` 字段
- 不修改 `.claude-plugin/marketplace.json` 的 `source.url`
- 不在 SKILL.md 的 `name` 字段添加 `moego-` 前缀
- 不在 SKILL.md 中添加 `triggers` 字段
- 不删除 `adapters/` 目录 — 非 Claude Code 工具依赖此层
- 不删除 `install.sh` — 作为 Plugin System 的降级方案保留
- 不在 Skill 脚本中硬编码凭证或 API Key — 使用环境变量

## ADR（架构决策记录）

- 位置：`docs/adr/NNNN-<title>.md`
- ADR 一旦 Accepted 不可修改；推翻需创建新 ADR 并标注 `Superseded by ADR-XXXX`
- 状态流转：`Proposed` → `Accepted` → `Retired` | `Superseded`

## 多工具兼容

| 工具        | 安装方式                                             | Skill 名称格式   |
| ----------- | ---------------------------------------------------- | ---------------- |
| Claude Code | `/plugin install moego@moego-ai-plugin`              | `/moego:<skill>` |
| Codex       | symlink 至 `~/.codex/skills/moego-<skill>`           | `moego-<skill>`  |
| OpenCode    | symlink 至 `~/.config/opencode/skills/moego-<skill>` | `moego-<skill>`  |
| Cursor      | `.cursorrules` 引用 SKILL.md 内容                    | 手动配置         |

修改 Skill 后需验证：adapter symlink 脚本（`install.sh`）能正确为新 Skill 创建链接。
