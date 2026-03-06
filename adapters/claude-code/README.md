# Claude Code Adapter

Claude Code 通过 Plugin System 原生支持 MoeGo Plugin，无需手工配置 symlink。

## 推荐安装方式（Plugin System）

```bash
/plugin marketplace add MoeGolibrary/moego-ai-plugin
/plugin install moego@moego-ai-plugin
```

安装后 Slash Command 自动可用：`/moego:superflow`、`/moego:e2e` 等。

## 手动安装（备用）

如无法使用 Marketplace，可直接克隆并符号链接：

```bash
git clone https://github.com/MoeGolibrary/moego-ai-plugin ~/.claude/plugins/moego-ai-plugin
```

Claude Code 会自动发现 `.claude-plugin/plugin.json` 并注册所有 Skills。
