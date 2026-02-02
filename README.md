# MoeGo Skills

MoeGo 团队共享的 AI Agent Skills 仓库，支持 Claude Code、Cursor 等工具。

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/MoeGolibrary/moego-skills/main/install.sh | bash
```

## 使用

安装完成后，可在支持的 AI 工具中使用以下 Skills：

| Skill | 说明 | 调用方式 |
|-------|------|----------|
| moego:e2e | E2E 测试规划与代码生成 | `/moego:e2e` |

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

1. 在 `skills/` 目录下创建新文件夹，如 `skills/moego-xxx/`
2. 创建 `skill.md` 定义 Skill 内容
3. 如需要，在 `adapters/` 下添加工具适配配置
4. 提交 PR

## 目录结构

```
moego-skills/
├── install.sh              # 安装脚本
├── bin/
│   └── moego-skills        # CLI 命令
├── skills/
│   └── moego-e2e/          # E2E 测试 Skill
│       └── skill.md
└── adapters/               # AI 工具适配配置
    ├── claude-code/
    └── cursor/
```

## License

MIT
