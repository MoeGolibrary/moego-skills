# MoeGo Plugin

MoeGo 研发团队 AI Agent Plugin，支持 Claude Code Plugin System 一键安装，兼容 AMP、Codex、OpenCode 等工具。

## 安装（Claude Code — 推荐）

```bash
# 1. 添加 MoeGo Marketplace（一次性）
/plugin marketplace add MoeGolibrary/moego-ai-marketplace

# 2. 安装 MoeGo Plugin
/plugin install moego@moego-ai-marketplace
```

安装后，Slash Command 自动可用：

| Skill                          | 说明                        | 调用方式                          |
| ------------------------------ | --------------------------- | --------------------------------- |
| moego:e2e                      | E2E 测试规划与代码生成      | `/moego:e2e`                      |
| moego:superflow                | AI Native 开发工作流        | `/moego:superflow`                |
| moego:datadog                  | Datadog 日志/Trace/依赖查询 | `/moego:datadog`                  |
| moego:writing-prompts          | 编写 LLM 一次性 prompt      | `/moego:writing-prompts`          |
| moego:writing-system-documents | 编写 Agent 常驻系统文档     | `/moego:writing-system-documents` |
| moego:code-to-spec             | 模块 SPEC 规格文档编写      | `/moego:code-to-spec`             |

### 更新 Plugin

```bash
/plugin update moego
```

## 安装（AMP / Codex / OpenCode）

非 Claude Code 工具请参考对应 adapter 文档：

- [Codex Adapter](adapters/codex/README.md)
- [OpenCode Adapter](adapters/opencode/README.md)
- [Cursor Adapter](adapters/cursor/README.md)

## 目录结构

```text
moego-ai-plugin/                      ← 仓库根目录（原 moego-skills）
├── .claude-plugin/
│   └── plugin.json                   ← Plugin manifest（name: "moego"）
├── skills/
│   ├── superflow/SKILL.md            ← name: superflow
│   ├── e2e/SKILL.md                  ← name: e2e
│   ├── datadog/SKILL.md              ← name: datadog
│   ├── writing-prompts/SKILL.md      ← name: writing-prompts
│   └── writing-system-documents/SKILL.md
├── hooks/
│   └── hooks.json                    ← reserved for future session hooks
├── agents/                           ← 未来：Agent 定义
├── commands/                         ← 未来：Slash Command 定义
├── adapters/                         ← 非 Claude Code 工具适配
│   ├── claude-code/
│   ├── codex/
│   ├── cursor/
│   └── opencode/
└── docs/
    └── adr/                          ← 架构决策记录
```

## 命名规范

本 Plugin 遵循 Claude Code Plugin System 规范：

| 层级          | 规则                                | 示例               |
| ------------- | ----------------------------------- | ------------------ |
| Plugin name   | `plugin.json` 中定义，kebab-case    | `"name": "moego"`  |
| Skill name    | SKILL.md 中的 bare name（无前缀）   | `name: superflow`  |
| Slash command | Claude Code 自动拼接 `plugin:skill` | `/moego:superflow` |

> ⚠️ SKILL.md 中的 `name` 字段**不加** `moego-` 前缀。命名空间由 Plugin System 自动追加。
> AMP/Codex 等工具通过 adapter 层的 symlink 脚本获取带前缀的 `moego-xxx` 别名。

## 贡献新 Skill

1. 在 `skills/` 下创建目录，如 `skills/your-skill/`
2. 创建 `SKILL.md`，frontmatter 用 **bare name**（不加 `moego-` 前缀）：

```yaml
---
name: your-skill
version: 1.0.0
description: >
  This skill should be used when the user asks to [specific trigger conditions].
---
```

3. Body 使用祈使句，核心内容控制在 1,500 词以内；详细文档放 `references/`
4. 如有脚本，放 `skills/your-skill/scripts/`，路径用 `${CLAUDE_PLUGIN_ROOT}/skills/your-skill/scripts/`
5. 提交 PR

## Marketplace 仓库

`MoeGolibrary/moego-ai-marketplace` — 管理 Plugin 分发索引

## License

MIT
