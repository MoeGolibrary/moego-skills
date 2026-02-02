# OpenCode Adapter

OpenCode 会从以下位置发现 Skills：

- 项目级：`.opencode/skills/<name>/SKILL.md`
- 用户级：`~/.config/opencode/skills/<name>/SKILL.md`
- 兼容路径：`.claude/skills` 与 `~/.claude/skills`

安装脚本会把技能链接到 `~/.config/opencode/skills`，同时也会创建 `~/.claude/skills`，因此无需额外配置即可被 OpenCode 识别。

## 手动配置

如需手动配置，可执行：

```bash
mkdir -p ~/.config/opencode/skills
ln -sfn ~/.claude/plugins/moego-skills/skills/moego-e2e ~/.config/opencode/skills/moego-e2e
```

如需项目级生效，可在仓库下创建 `.opencode/skills` 并建立同样的链接。
