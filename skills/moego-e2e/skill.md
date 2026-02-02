---
name: moego-e2e
description: E2E 测试规划与代码生成，遵循 MoeGo E2E 最佳实践
triggers:
  - /moego:e2e
  - 功能开发任务中检测到需要 E2E 测试
---

# MoeGo E2E Testing Skill

为 MoeGo E2E 自动化测试项目（moego-e2e-autotest）提供测试规划和代码生成能力。

## 触发方式

| 方式 | 场景 |
|------|------|
| 独立调用 | 用户执行 `/moego:e2e` |
| 联动建议 | 检测到功能开发任务时，主动提示"是否需要规划 E2E 测试？" |

## 工作模式

### Plan 模式

**流程：**
1. 识别输入来源（Plan 文档 > 代码变更 > 现有页面）
2. 提取测试需求（功能点、边界、异常）
3. 确定覆盖深度（从 Plan 读取或询问用户）
4. 生成测试计划（场景清单 + 优先级）
5. 确认文件路径（Plan 指定 > 自动推断 > 询问）

**输出格式：**

```markdown
## E2E 测试计划

### 功能概述
[从输入来源提取的功能描述]

### 测试场景

| # | 场景 | 优先级 | 数据策略 | 预计路径 |
|---|------|--------|----------|----------|
| 1 | 正常创建预约 | P0 | UI 全流程 | tests/grooming/.../createAppt.spec.ts |
| 2 | 缺少必填字段 | P1 | API + UI | 同上 |

### 依赖的 Page Object
- [ ] `AppointmentPage` — 已存在，需扩展方法 `xxx`
- [ ] `NewFeaturePage` — 需新建

### 测试账号
- 使用账号：`xxx@moego.pet`
```

### Impl 模式

**流程：**
1. 读取测试计划
2. 检索现有资源（Page Object / Utils）
3. 生成/扩展代码（优先复用，缺失则新建）
4. 应用最佳实践
5. 输出文件（.spec.ts + Page Object）

---

## 最佳实践

### 1. 架构规范

| 规范 | 说明 |
|------|------|
| Page Object Pattern | 页面封装为类，继承 `Common`，接收 `page` + `api` |
| UI 组件封装 | 复用 `@pages/uiComponents/` 下的组件类 |
| Fixture 系统 | 使用 `@fixture/index` 的 `test` |
| Utils 分离 | 测试目录下辅助逻辑放 `utils.ts` |

### 2. 定位策略（优先级从高到低）

```typescript
// ✅ 优先：data-testid
page.getByTestId('appt-save-btn')

// ✅ 其次：语义化定位
page.getByRole('button', { name: 'Save' })
page.getByLabel('Price')
page.getByText('Submit')

// ✅ 组件定位：data-slot
page.locator('[data-slot="select-control"]')

// ⚠️ 避免：脆弱的选择器
page.locator('.btn-primary')
page.locator('div > span:nth-child(2)')
```

### 3. 等待策略

```typescript
// ✅ 等待 API 响应
const response = page.waitForResponse('/api/xxx');
await page.getByRole('button').click();
await response;

// ✅ 等待元素状态
await expect(page.locator('.loading')).toHaveCount(0);
await expect(page.getByText('Success')).toBeVisible();

// ⚠️ 避免：硬编码等待（仅在无法避免时使用）
await page.waitForTimeout(1000);
```

### 4. 数据策略（按优先级）

| 优先级 | 准备 | 核心流程 | 清理 |
|--------|------|----------|------|
| P0 | UI | UI | 可选 |
| P1/P2 | API | UI | API |

---

## 测试规范

### 命名与标签

```typescript
// 测试名格式：场景描述 + MeterSphere ID
test('create grooming appointment from client detail 110445', {
  tag: [
    '@p0',                      // 优先级：@p0 | @p1 | @p2
    '@author:vicky@moego.pet'   // 作者邮箱
  ]
}, async ({ page, api }) => {
  // ...
});
```

### 文件组织

```
project/BWeb/tests/
└── grooming/                    # 业务模块
    └── salonGrooming/           # 子模块
        └── groomingAppt/        # 功能
            ├── appointment/
            │   ├── createFlow/
            │   │   └── createAppt.spec.ts
            │   └── cancelFlow/
            │       └── cancelAppt.spec.ts
            └── apptDrawer/
                └── drawerService.spec.ts
```

### 测试账号

| 场景 | 账号命名 |
|------|----------|
| 通用测试 | `account_bd` |
| 特定功能 | `drawer-service@moego.pet` |
| UI 自动化 | `account_bd_ui_auto` |

### 代码模板

```typescript
import { test } from '@fixture/index';
import { XxxPage } from '@pages/xxx';
import { expect } from '@playwright/test';

test.beforeEach(async ({ login }) => {
  await login('dedicated-test-account@moego.pet');
});

test.describe('功能描述', () => {
  test('场景描述 123456', {
    tag: ['@p0', '@author:xxx@moego.pet']
  }, async ({ page, api }) => {
    const xxxPage = new XxxPage(page, api);
    // ... 测试逻辑
  });
});

test.afterEach(async ({ page, api }) => {
  // 清理逻辑（根据优先级决定）
});
```

---

## Page Object 规范

### 创建新 Page Object

```typescript
import { ApiType } from '@fixture/api';
import { Page, expect } from '@playwright/test';
import { Common } from './common';

export class NewFeaturePage extends Common {
  constructor(page: Page, api: ApiType) {
    super(page, api);
  }

  async goto() {
    await this.page.goto('/path/to/feature');
    await expect(this.page.locator('.page-loaded-indicator')).toBeVisible();
  }

  async doSomething(params: { name: string }) {
    const { page } = this;
    await page.getByTestId('input-name').fill(params.name);
    await page.getByRole('button', { name: 'Submit' }).click();
  }
}
```

### 扩展现有 Page Object

优先搜索 `project/BWeb/pages/` 下相关文件，找到匹配的 Page Object 后添加缺失方法。

---

## 参考示例

最佳实践参考目录：`project/BWeb/tests/grooming/`

关键示例文件：
- `salonGrooming/groomingAppt/appointment/createFlow/createAppt.spec.ts`
- `salonGrooming/groomingAppt/apptDrawer/drawerService.spec.ts`
- `salonGrooming/bookBySlot/utils.ts`
