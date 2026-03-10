# Kiro Adapter

Kiro 从 0.9 版本起原生支持 Agent Skills（基于 [agentskills.io](https://agentskills.io) 开放标准）。

Skills 发现路径：

- 用户级：`~/.kiro/skills/<name>/SKILL.md`
- 工作区级：`<repo>/.kiro/skills/<name>/SKILL.md`

Kiro 启动时仅加载 SKILL.md 的 name 和 description（frontmatter），完整内容按需加载。MoeGo Plugin 的 SKILL.md 格式与 Kiro 完全兼容，无需转换。

## 自动安装

运行 `install.sh` 会自动将所有 Skills 以 `moego-` 前缀复制至 `~/.kiro/skills/`。

> **注意**：Kiro 不支持发现文件夹级别的符号链接，因此采用直接复制而非 symlink。每次更新会先删除旧目录再重新复制。

> ⚠️ **重启才能真正激活**：安装或更新全局 Skills 后，Kiro UI 上可能已显示新 Skill，但在重启 Kiro 之前，Skill 可能无法自动激活，或无法完整读取 SKILL.md 及 references 中的所有文件。请在安装/更新后重启 Kiro 以确保 Skill 真正激活。

## 手动配置

```bash
mkdir -p ~/.kiro/skills
PLUGIN_ROOT=~/.claude/plugins/moego-ai-plugin
for skill_dir in "$PLUGIN_ROOT"/skills/*/; do
  skill=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    rm -rf ~/.kiro/skills/moego-${skill}
    cp -r "${skill_dir%/}" ~/.kiro/skills/moego-${skill}
  fi
done
```

安装后可通过 `/moego-superflow`、`/moego-e2e` 等 slash command 调用，或由 Kiro 根据 description 自动匹配加载。

如需工作区级生效，可在项目下创建 `.kiro/skills` 并将 Skill 目录复制至其中。工作区级 Skills 在名称冲突时优先于用户级。
