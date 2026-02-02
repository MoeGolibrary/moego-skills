# Codex Adapter

Codex 会从以下目录加载 Skills：

- 用户级：`~/.codex/skills`（默认 `$CODEX_HOME/skills`）
- 项目级：`<repo>/.codex/skills`

Codex 支持 skill 目录的符号链接。安装脚本会把每个 skill 目录链接到 `~/.codex/skills`。

## 手动配置

如需手动配置，可执行：

```bash
mkdir -p ~/.codex/skills
ln -sfn ~/.claude/plugins/moego-skills/skills/moego-e2e ~/.codex/skills/moego-e2e
```

如需项目级生效，可在仓库下创建 `.codex/skills` 并建立同样的链接。
