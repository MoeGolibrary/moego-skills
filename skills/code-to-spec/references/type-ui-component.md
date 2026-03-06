# UI 组件类型配置

## Research 必读文件

按优先级排序——先建立场景心智模型，再理解 API 边界，最后深入实现：

1. `__stories__/*.mdx`（使用场景描述）— 最先读，建立"预先设计"视角
2. `__stories__/*.stories.tsx`（典型用法和变体）— 理解组件的使用方式
3. `index.ts`（导出结构，对外 API 边界）— 确认公共 API 范围
4. 组件目录下所有 `.tsx` / `.ts`（主组件、样式、类型、hooks、工具函数）— 最后读实现
5. `.kiro/specs/<component>/` 目录（如存在）

## 复杂度分级

```text
组件是否包含非平凡算法（级联选中、虚拟滚动、拖拽排序等）？
├─ 是 → 复杂
└─ 否 → 组件是否有 3+ 子组件，或需要多层 Context / 状态桥接？
         ├─ 是 → 复杂
         └─ 否 → 组件是否有子组件、Context 传递、或 3 种以上状态组合？
                  ├─ 是 → 中等
                  └─ 否 → 简单
```

| 级别 | 约束条数参考 | "关键设计约束"结构 | 典型组件 |
|------|-----------|--------------------|---------|
| 简单 | 5–8 条 | 扁平列表，不分组 | Alert, Badge, Divider, Spin |
| 中等 | 8–15 条 | 按主题分 2–3 个子标题 | Switch, Button, Radio, Checkbox |
| 复杂 | 15+ 条 | 按架构层次分组，需要独立子章节 | Cascader, Table, DatePicker, Select |

## 章节模板

文件位置：`packages/ui/src/components/<ComponentName>/SPEC.md`

```markdown
# ComponentName 组件规格

本文档描述 ComponentName（中文名）组件的功能场景与关键设计约束，作为实现的核心参考。

## 终端用户场景
## 开发者场景
## 关键设计约束
## 适用场景
## 不适用场景
```

## 逆向工程示例表

| 痕迹类型 | ❌ 逆向工程写法 | ✅ 设计文档写法 |
|---------|----------------|---------------|
| 引用内部变量/函数名 | "通过 `listProps` 中删除 `onKeyDown`" | "需要禁用默认的列表键盘导航，避免干扰折叠交互" |
| 描述代码行为 | "`useCollection` 传入 `suppressTextValueWarning: true`" | （删除，属于实现细节） |
| 引用 CSS 类名 | "通过 `moe-invisible` 隐藏" | "收起时视觉隐藏但保留 DOM" |
| 描述 hack/workaround | "`indicatorPlacement` 传入 `'right'` 使条件判断不命中" | "Panel 自行管理指示器渲染，不复用容器的指示器逻辑" |
| 引用库的内部 API | "`initialEntered` 设为当前 `isExpanded` 值" | "初始已展开的项不应触发入场动画" |
| 描述命令式 DOM 操作 | "命令式操作 `style.height` 和 `style.opacity`" | "通过高度和透明度过渡实现展开/收起动画" |
| 描述 CSS 实现技巧 | "通过 `::after` 伪元素承载填充色，配合 `translateZ(0)` 强制 GPU 合成层" | "填充条通过 transform 实现视觉填充，以获得更好的渲染性能" |
| 伪装成设计语言的实现描述 | "内部需要 +1 转换为 CSS Grid 的一基索引" | "位置索引从 0 开始，与数组索引习惯一致" |
| 伪装成设计语言的实现描述 | "`align` 映射到 CSS `align-items`" | "`align` 控制每个 grid item 在其轨道内的块轴对齐" |
| 伪装成设计语言的实现描述 | "样式按 cellClassNames → classNames → className 的顺序合并" | "样式优先级从低到高为：容器级 < 组件级 classNames < 组件级 className" |
| 描述回调的精确执行顺序 | "用户回调 → 自动关闭 → 按钮 props 上的 onPress" | "回调完成后自动关闭对话框" |
| 指定具体的 DOM/属性名约定 | "在 `document.body` 上设置 `data-modal-open` 属性" | "需要向外部暴露模态状态信号" |
| 直接翻译代码条件分支 | "`isDismissable && isBlockScroll` 时锁定滚动" | "不可关闭的对话框不渲染遮罩，因此不锁定背景滚动" |
| 指定具体实现机制 | "通过首尾各放置一个 DismissButton 实现焦点陷阱" | "焦点限制在对话框内部循环" |
| 引用源码中的具体值 | "关闭按钮使用 `secondary` 变体和 `xl` 尺寸" | "关闭按钮视觉上更大更突出，以匹配悬浮定位" |

## Verify 额外过滤项

子 agent 校验时，除通用过滤规则外，还需额外过滤：

- CSS 实现技巧（如用 `::after` 还是子元素、`translateZ(0)` 等 GPU 优化手段）
- DOM 层级结构细节（如 VisuallyHidden input 模式）
- 布局补偿的具体像素值或方向限定
- 组件包装模式的选择（如 memo vs forwardRef、类型断言技巧）

## 内容取舍补充

应该写：
- 回调触发的条件和语义
- 受控/非受控模式的桥接策略

不应该写：
- forwardRef + displayName（项目规范）
- tv() slots/variants 模式（项目规范）
- filterDOMProps / useSlotName / data-slot（项目规范）
- 具体样式值（颜色 token、间距等，设计稿驱动）
- DOM 层级结构（除非直接影响组件功能）
- CSS 类名、布局补偿技巧、variant 名称

## 参考示例

- 简单组件：`packages/ui/src/components/Alert/SPEC.md`
- 中等组件：`packages/ui/src/components/Button/SPEC.md`
- 复杂组件：`packages/ui/src/components/Cascader/SPEC.md`
