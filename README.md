# MoeGo Skills

MoeGo 团队共享的 AI Agent Skills 仓库，支持 Claude Code、Cursor、Codex、OpenCode 等工具。

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/MoeGolibrary/moego-skills/main/install.sh | bash
```

## 使用

安装完成后，可在支持的 AI 工具中使用以下 Skills：

| Skill | 说明 | 调用方式 |
|-------|------|----------|
| moego:e2e | E2E 测试规划与代码生成 | `/moego:e2e` |
| moego:superflow | AI Native 开发工作流（需 superpowers） | `/moego:superflow` |

## 管理命令

```bash
# 更新所有 skills
moego-skills update

# 查看已安装的 skills
moego-skills list

# 查看帮助
moego-skills help
```

## 贡献新 Skill

### Skill 命名规范

所有 MoeGo Skills 必须使用 `moego:` 前缀，以便与其他来源的 skills 区分。

| 规则 | 说明 | 示例 |
|------|------|------|
| 前缀 | 必须使用 `moego:` | `moego:e2e`, `moego:superflow` |
| 目录名 | 简短描述性名称，无前缀 | `skills/e2e/`, `skills/superflow/` |
| SKILL.md name 字段 | 完整名称，带前缀 | `name: moego:e2e` |
| triggers | 使用完整名称 | `- /moego:e2e` |

**示例 SKILL.md 头部：**

```yaml
---
name: moego:your-skill-name
description: 简短描述
triggers:
  - /moego:your-skill-name
---
```

### 添加新 Skill 步骤

1. 在 `skills/` 目录下创建新文件夹，如 `skills/your-skill/`
2. 创建 `SKILL.md` 定义 Skill 内容（注意大写）
3. 确保 `name` 字段使用 `moego:` 前缀
4. 如需要，在 `adapters/` 下添加工具适配配置
5. 提交 PR

## 目录结构

```
moego-skills/
├── install.sh              # 安装脚本
├── bin/
│   └── moego-skills        # CLI 命令
├── skills/
│   ├── e2e/                # E2E 测试 Skill
│   │   └── SKILL.md
│   └── superflow/          # AI Native 开发工作流
│       └── SKILL.md
└── adapters/               # AI 工具适配配置
    ├── claude-code/
    ├── cursor/
    ├── codex/
    └── opencode/
```

## License

MIT
