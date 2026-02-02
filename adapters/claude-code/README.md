# Claude Code Adapter

Claude Code 通过 `~/.claude/skills/` 目录加载 Skills。

## 自动配置

安装脚本会自动创建符号链接：

```
~/.claude/skills/moego-e2e.md -> ~/.claude/plugins/moego-skills/skills/moego-e2e/skill.md
```

## 手动配置

如需手动配置，可在项目 `.claude/settings.json` 中添加：

```json
{
  "skills": [
    "~/.claude/plugins/moego-skills/skills/moego-e2e/skill.md"
  ]
}
```
