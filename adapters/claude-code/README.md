# Claude Code Adapter

Claude Code 通过 `~/.claude/skills/` 目录加载 Skills。

## 自动配置

安装脚本会自动创建符号链接（目录级）：

```
~/.claude/skills/moego:e2e -> ~/.claude/plugins/moego-skills/skills/e2e
```

## 手动配置

如需手动配置，可在项目 `.claude/settings.json` 中添加：

```json
{
  "skills": [
    "~/.claude/plugins/moego-skills/skills/e2e/SKILL.md"
  ]
}
```
