# ADR-0001: 将 moego-skills 升级为 Claude Code Plugin 架构

## Status

Accepted — 2026-03-04

## Context

### 背景

`moego-skills` 仓库目前以手工 symlink 方式分发 AI Agent Skills，支持 Claude Code、AMP、Codex、OpenCode 等工具。现有方案存在以下约束：

1. **命名冲突**：Claude Code Plugin System 需要 SKILL.md 使用 bare name（如 `name: superflow`），由 plugin 元数据自动追加命名空间（`moego:superflow`）；而 AMP/Codex 直接读取 SKILL.md 的 `name` 字段作为最终名称，需要 `name: moego-superflow` 才能避免命名冲突。两个约束互斥，单一 SKILL.md 无法同时满足。

2. **分发复杂度**：当前基于 `install.sh` + symlink 的安装方式需要手工维护。Claude Code 官方 Plugin System 提供了一套标准化分发机制（Marketplace），安装体验显著更好（一行命令）。

3. **能力边界**：随着团队需求增长，Skills 之外还需要纳入 Agents（autonomous 代理）、Commands（slash 快捷操作）、Hooks（会话级上下文注入）等能力。当前扁平的 `skills/` 目录结构没有为这些扩展预留标准位置。

4. **官方标准对齐**：Anthropic 已发布 Claude Code Plugin 规范，包含完整的目录结构、`plugin.json` manifest、组件自动发现机制。当前 moego-skills 架构与官方规范存在差距。

### 现有架构

```
moego-skills/
├── install.sh              # curl 安装脚本
├── bin/moego-skills        # CLI 管理命令
├── skills/
│   ├── superflow/SKILL.md  # name: moego-superflow（带前缀）
│   ├── e2e/SKILL.md
│   ├── datadog/SKILL.md
│   ├── writing-prompts/SKILL.md
│   └── writing-system-documents/SKILL.md
└── adapters/
    ├── claude-code/
    ├── amp/
    ├── codex/
    └── opencode/
```

安装路径：`~/.claude/plugins/moego-skills/skills/` + symlinks at `~/.claude/skills/moego-xxx`

### 参考案例

Superpowers（obra/superpowers）是目前最成熟的 Claude Code Plugin 实践，采用：
- `.claude-plugin/plugin.json` 声明 `"name": "superpowers"`
- SKILL.md 使用 bare name（`name: brainstorming`）
- 独立 `superpowers-marketplace` repo 管理分发
- 无 `triggers` 字段，完全依赖 Plugin System 命名空间

## Decision

**将 moego-skills 重构为标准 Claude Code Plugin，同时保留 adapter 层兼容 AMP/Codex。**

### 核心目录结构

```
moego-ai-plugin/
│   └── plugin.json                  # Plugin manifest，name: "moego"
├── skills/
│   ├── superflow/
│   │   ├── SKILL.md                 # name: superflow（bare，Plugin 接管命名）
│   │   ├── references/              # 详细文档，按需加载
│   │   └── scripts/
│   ├── e2e/
│   │   └── SKILL.md
│   ├── datadog/
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── writing-prompts/
│   │   └── SKILL.md
│   └── writing-system-documents/
│       └── SKILL.md
├── agents/                          # 未来：autonomous 代理定义
├── commands/                        # 未来：slash command 定义
├── hooks/
│   └── hooks.json                   # SessionStart：注入 MoeGo 项目上下文
├── adapters/                        # 保留：非 Claude Code 工具的安装适配
│   ├── amp/README.md
│   ├── codex/README.md
│   └── opencode/README.md
├── docs/
│   └── adr/                         # 架构决策记录
└── install.sh                       # 保留：兼容旧有安装流程
```

### `plugin.json` 规范

```json
{
  "name": "moego",
  "version": "2.0.0",
  "description": "MoeGo engineering team plugin — E2E testing, Superflow workflow, Datadog observability, and writing skills for MoeGo pet services platform.",
  "author": "MoeGo Engineering",
  "homepage": "https://github.com/MoeGolibrary/moego-ai-plugin",
  "repository": "https://github.com/MoeGolibrary/moego-ai-plugin",
  "license": "MIT",
  "keywords": ["moego", "e2e", "testing", "datadog", "superflow", "bff"]
}
```

**命名结果**：`plugin.json` 的 `"name": "moego"` + SKILL.md 的 `name: superflow` → Claude Code 自动暴露 `/moego:superflow`

### SKILL.md 规范变更

```yaml
# 变更前
---
name: moego-superflow
triggers:
  - /moego-superflow
---

# 变更后
---
name: superflow
version: 1.x.0
description: >
  This skill should be used when the user invokes the Superflow workflow,
  asks about branch management, wants to run PR review flow, or references
  the MoeGo release pipeline.
---
```

**关键变化**：去掉 `moego-` 前缀，去掉 `triggers` 字段（由 Plugin System 接管）。

### AMP/Codex 双轨兼容方案

AMP 和 Codex 直接读取 SKILL.md `name` 字段。迁移为 Plugin 后，这些工具将看到 bare name（如 `superflow`），失去命名空间前缀。

**解决方案**：在 `adapters/` 下提供工具专属安装脚本，为非 Claude Code 工具创建带前缀别名的 symlink（`moego-superflow → .../skills/superflow/SKILL.md`）。适配层与 Plugin 核心解耦，独立维护。

### Marketplace 分发

`moego-ai-plugin` 仓库自身兼作 marketplace（`.claude-plugin/marketplace.json`），无需独立索引仓库：

```json
{
  "name": "moego-ai-plugin",
  "description": "MoeGo engineering team plugin marketplace",
  "owner": { "name": "MoeGo Engineering", "email": "engineering@moego.pet" },
  "plugins": [{
    "name": "moego",
    "source": {
      "source": "url",
      "url": "https://github.com/MoeGolibrary/moego-ai-plugin.git"
    }
  }]
}
```

开发者安装（两步，一次性配置）：

```bash
/plugin marketplace add MoeGolibrary/moego-ai-plugin
/plugin install moego@moego-ai-plugin
```

后续更新：

```bash
/plugin update moego
```

### Hooks 设计（SessionStart）

```json
{
  "description": "MoeGo plugin hooks — reserved for future session-level context injection (e.g. project paths, grey env info).",
  "hooks": {}
}
```

未来可在 SessionStart 中注入 MoeGo 项目路径、灰度环境信息等上下文。

## Consequences

### Positive

- **零配置命名空间**：SKILL.md 无需维护 `moego-` 前缀，Plugin System 自动处理，斜杠命令从 `/moego-superflow` 升级为 `/moego:superflow`（与 Superpowers 等主流插件体验一致）
- **官方生态对齐**：遵循 Anthropic Claude Code Plugin 规范，未来可直接发布到官方 Plugin Marketplace
- **扩展性**：`agents/`、`commands/`、`hooks/` 目录为未来能力扩展预留标准位置，无需再次重构
- **一行安装**：Marketplace 模式对比当前 `curl | bash` 方式，安装更安全、更新更便捷
- **版本管理**：`plugin.json` 的 `version` 字段 + git tag 形成完整版本链
- **Progressive Disclosure**：官方规范的三层加载（metadata → SKILL.md → references/）降低每次推理的固定 token 开销

### Negative

- **迁移成本**：所有已安装的 symlink 需要重建；现有文档和团队 onboarding 材料需要同步更新
- **AMP/Codex 维护负担增加**：双轨方案需要在 `adapters/` 下维护额外的安装脚本和文档；每次新增 Skill 时需同步更新 adapter 配置
- **Marketplace 冷启动**：~~`moego-ai-marketplace` repo 需额外创建和维护~~（已废弃，`moego-ai-plugin` 自身兼作 marketplace，通过 `.claude-plugin/marketplace.json` 实现）
- **Claude Code 依赖**：Plugin System 目前为 Claude Code 专属，非 Claude Code 工具用户无法享受自动命名空间和 Marketplace 能力

### Risks

- **Plugin System 稳定性**：Claude Code Plugin System 为相对新的功能，API 可能变化。**缓解**：保留 `install.sh` 和 adapter 层作为降级方案，确保核心 Skills 内容不与分发机制耦合。
- **团队切换成本**：已使用 `/moego-superflow` 的开发者需要适应新命令 `/moego:superflow`。**缓解**：过渡期同时维护旧 symlink，在 CHANGELOG 和 onboarding 文档中明确标注变更。
- **Marketplace 可用性**：`moego-ai-plugin` 本身即为 marketplace，仓库可用性与 plugin 可用性合一，无额外依赖。

## Implementation Plan

| Phase | 内容 | 优先级 |
|-------|------|--------|
| Phase 1 | 创建 `.claude-plugin/plugin.json`；修改所有 SKILL.md name 为 bare name；重建 symlink | 立即 |
| Phase 2 | 创建 `hooks/hooks.json`，SessionStart 注入基础上下文 | 近期 |
| Phase 3 | 在 `.claude-plugin/` 添加 `marketplace.json`，`moego-ai-plugin` 自身兼作 marketplace | 近期 |
| Phase 4 | 添加 Agents（如 `code-reviewer`）和 Commands（如 `sync-bff`）| 中期 |

## Related Decisions

- 仓库命名**重命名为 `moego-ai-plugin`**，`ai` 消歧义（避免误解为 MoeGo 产品体系的插件），语义更准确；GitHub redirect 保证旧链接兼容；所有文档已同步更新
- MCP Server 不纳入本 Plugin，由开发者通过官方 Marketplace 独立安装
- Plugin name 选用 `moego`（不加 `-skills` 后缀），使斜杠命令更简洁

## References

- [Claude Code Plugin System 官方文档](https://docs.anthropic.com/claude-code/plugins)
- [Superpowers Plugin 参考实现](https://github.com/obra/superpowers)
- [plugin-dev 官方示例插件](~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/)
