# SKILL 编写与审查检查清单

编写完成后逐项检查。也可用于审查已有 SKILL 的质量。

## Frontmatter

- [ ] `name` 是 kebab-case，1-64 字符
- [ ] `name` 与目录名完全一致
- [ ] `name` 无 `moego-` 前缀
- [ ] `version` 使用语义化版本号（如 `1.0.0`）
- [ ] `description` 是纯英语（不中英混合）
- [ ] `description` 包含三要素：做什么 + 激活关键词 + 不做什么
- [ ] `description` 长度在 150-300 字符之间（不超过 1024）
- [ ] 使用 YAML 多行语法 `>` 书写 description
- [ ] 无 `triggers` 字段

## 正文结构

- [ ] frontmatter + 核心指令部分 ≤ 1,500 词（references/ 不计入）
- [ ] 开头有一句话定位（这个 SKILL 做什么）
- [ ] 有"核心原则"章节（3-5 条，引导 AI 的价值判断）
- [ ] 有"关键约束 / Edge Cases"章节（集中在顶部，不散落各处）
- [ ] 有明确的执行流程（Step 1..N）

## 执行流程

- [ ] 每个 Step 有「输入」段
- [ ] 每个 Step 有「操作」段（具体动作列表）
- [ ] 每个 Step 有「输出」段（明确产出物）
- [ ] 有 Verify / 验证步骤
- [ ] 验证步骤有失败回退机制（最多 N 轮 + 上报用户）
- [ ] 流程中引用 references 时使用相对路径链接

## Progressive Disclosure

- [ ] 代码模板放在 `references/` 而非正文
- [ ] 详细规范和示例集合放在 `references/`
- [ ] 正文只保留决策逻辑、分类矩阵、流程框架
- [ ] references 文件有清晰的标题和用途说明

## 项目约定

- [ ] 源文件在 `skills/<name>/`
- [ ] 脚本路径使用 `${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/` 引用
- [ ] 运行 `install.sh` 确认 adapter symlink 正确
- [ ] 正文和 references 建议使用中文（非强制）
- [ ] JSDoc / 代码注释使用英语（如有代码示例）
- [ ] frontmatter description 使用英语
- [ ] 脚本不硬编码凭证或 API Key — 使用环境变量
- [ ] 全文不出现 `deprecated`、`废弃`、`已弃用`

## 常见问题自检

| 问题                     | 检查方法                                              |
| ------------------------ | ----------------------------------------------------- |
| description 会误激活吗？ | 检查是否有足够的负面触发（Not for...）                |
| description 会漏激活吗？ | 检查触发关键词是否覆盖用户常用表述                    |
| 正文太长了吗？           | 检查是否超过 1,500 词，是否有可拆到 references 的内容 |
| AI 能机械执行吗？        | 检查每个 Step 是否有足够具体的操作指令                |
| 失败了怎么办？           | 检查是否有回退机制和上报用户的出口                    |
| 新人能理解吗？           | 检查核心原则是否清晰传达了"为什么这样做"              |
| 内容是否冗余？           | 对每段问"Agent 能否自行推断？"，能则删除              |
| 有安全风险吗？           | 检查脚本是否硬编码凭证，references 是否含敏感信息     |

## 效果评估（可选但推荐）

使用子 Agent A/B 对比测试（详见 [references/examples.md](references/examples.md) 第 8 节）：

- [ ] 定义了 2-3 个代表性任务
- [ ] 子 Agent A（无 SKILL）已跑出基线输出
- [ ] 子 Agent B（有 SKILL）已跑出测试输出
- [ ] B 在多数高权重维度明显优于 A
- [ ] 尝试删除某章节后重跑 B，输出质量未变差的章节已精简
