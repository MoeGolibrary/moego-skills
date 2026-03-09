# Kiro Adapter

Kiro 从 0.9 版本起原生支持 Agent Skills（基于 [agentskills.io](https://agentskills.io) 开放标准）。

Skills 发现路径：

- 用户级：`~/.kiro/skills/<name>/SKILL.md`
- 工作区级：`<repo>/.kiro/skills/<name>/SKILL.md`

Kiro 启动时仅加载 SKILL.md 的 name 和 description（frontmatter），完整内容按需加载。MoeGo Plugin 的 SKILL.md 格式与 Kiro 完全兼容，无需转换。

## 自动安装

运行 `install.sh` 会自动为所有 Skills 创建带 `moego-` 前缀的符号链接至 `~/.kiro/skills/`。

## 手动配置

```bash
mkdir -p ~/.kiro/skills
PLUGIN_ROOT=~/.claude/plugins/moego-ai-plugin
for skill_dir in "$PLUGIN_ROOT"/skills/*/; do
  skill=$(basename "$skill_dir")
  [ -f "$skill_dir/SKILL.md" ] && ln -sfn "${skill_dir%/}" ~/.kiro/skills/moego-${skill}
done
```

安装后可通过 `/moego-superflow`、`/moego-e2e` 等 slash command 调用，或由 Kiro 根据 description 自动匹配加载。

如需工作区级生效，可在项目下创建 `.kiro/skills` 并建立同样的链接。工作区级 Skills 在名称冲突时优先于用户级。
