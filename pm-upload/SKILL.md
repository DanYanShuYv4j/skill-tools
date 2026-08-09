---
name: pm-upload
description: Use when a product manager wants to upload/submit their PRD or Demo files to the repository. Triggers on 「上传」「提交」「交底」「更新demo」「更新prd」「帮我把」「放到」etc. PMs don't use git — the AI handles everything conversationally.
---

# PM Upload — 产品经理文件上传助手

引导产品经理以对话方式将 PRD 或 Demo 文件上传到正确模块目录，自动更新索引、提交并推送。

## 三种内容类型

pm-upload 支持三种内容类型：PRD、Demo、优化清单。

| 类型 | 触发词 | 目标位置 |
|------|-------|---------|
| PRD | "上传 PRD" | `docs/prd/<author>/vX.Y.Z-xxx.md` |
| Demo | "上传 Demo" | `docs/demos/<author>/v{版本号}-{模块}/{功能中文名}/` |
| 优化清单 | "记个优化""优化清单加一条" | `releases/vX.Y.Z/optimizations.md` |

### 批量模式（推荐）

用户一次性给出全部信息，AI 直接执行，无需逐步问答：

```
模块：feature-module
版本：v2.0
作者：author-a
文件：/path/to/xxx.md
```

或更简洁：

```
上传 PRD 到release-version，我写的，文件在 /path/to/your/file.md
```

AI 自动推断：
- **类型**：`.md` 文件 → PRD；目录含 `index.html` → Demo；描述单点小改动 → 优化清单
- **PRD 版本号**：从 PRD 内容 `# xxx PRD` 或 `版本：v1.x` 提取
- **场景名**（Demo）：从 `index.html` 的 `<title>` 提取，或按需询问
- **Demo 路径**：`v{版本号}-{模块}/{功能中文名}`（按版本，非日期）

**⚠️ 班车版本为必确认项。** 如果用户没说版本号（如只说"上传 PRD 到feature-x"），必须追问确认。不可自动推断、不可跳过。详见 §①.⑤。

**缺少信息时才追问，不缺就直接执行。变更记录为必问项，见 §⑩。**

### 引导模式

用户只说"上传"但信息不全时，逐步引导：

```
PM 说"上传/提交/交底"
  → ① 确定模块（必确认）
  → ①.⑤ 确定班车版本（必确认）
  → ② 确定类型（PRD / Demo）
  → ③ 确定作者（拼音）
  → ④ 收集文件
  → ⑤ 放到正确位置
  → ⑥ 更新 INDEX + CHANGELOG
  → ⑥.⑤ 更新 release README + releases/INDEX.md
  → ⑦ 展示变更摘要，等待用户确认
  → ⑧ 用户确认后 commit & push
  → ⑨ 报告结果
```

## ① 确定目标模块（必确认项）

⚠️ **模块必须由 PM 明确确认，不可自动推断。** 如果用户输入中没有提供模块，必须停下来追问，确认后才能继续后续步骤。

读取 `docs/module-map.md` 获取可用模块列表。向用户提问：

> "你要上传到哪个模块？"
>
> 1. 订单系统 (order-system)
> 2. 数据分析 (analytics)
> 3. 消息通知 (notification)
> 4. feature-module (feature-module)
> 5. 支付结算 (billing)
> 6. 文件管理 (file-management)
> 7. feature-x (feature-x)
> 8. admin-config (admin-config)

用户可以用中文名或数字回答。

如果用户不确定属于哪个模块，根据 PRD 内容关键词推荐，但**最终必须由 PM 确认**。推荐规则见底部「常见情况处理 → 用户不知道模块」。

**PM 没有明确确认模块之前，禁止执行 §①.⑤ 及之后任何步骤。**

## ①.⑤ 确定班车版本（必确认项）

⚠️ **班车版本必须由 PM 明确确认，不可自动推断。** 如果用户输入中没有提供版本号，必须停下来追问，确认后才能继续后续步骤。

### 情况 A：用户已提供版本号

用户说了"上传到 V1.0.4"或"版本：v2.0"，直接确认：

> "确认归入 V1.0.4 班车？"

PM 确认后继续。

### 情况 B：用户未提供版本号

用户只说"上传 PRD 到feature-x"，没提版本。此时**必须追问**：

> "这个 PRD 归入哪个班车版本？"（如 v2.0、v1.0.5）

列出可选参考（读取 `releases/INDEX.md`）：
- 当前"收集中"的版本（如有）
- 最近已发布的版本号（供参考下一个版本号）

如果没有任何版本或 PM 不确定，提示：

> "还没有班车版本。要创建一个吗？告诉我版本号（如 v2.0），我来初始化。"

### 情况 C：PM 确认创建新版本

PM 给出新版本号后：

1. 创建 `releases/<version>/` 目录
2. 从 `shared/templates/release-readme-template.md` 复制模板创建 `releases/<version>/README.md`
3. 更新 `releases/INDEX.md`，追加版本行（状态：收集中）

**新增版本到 INDEX 格式：**
```markdown
| v2.0 | — | 收集中 | — |
```

### 未确认 = 不执行

PM 没有明确确认版本号之前，**禁止**执行 §② 及之后任何步骤。

## ② 确定内容类型

> "是 PRD 文档、交互 Demo 还是优化清单？"

- **PRD** → 单个 .md 文件，放到 `prd/<author>/` 下，走完整上传流程
- **Demo** → 4 个文件（index.html, tokens.css, demo.css, demo.js），放到 `demos/<author>/v{版本号}-{模块}/{功能中文名}/` 下，走完整上传流程
- **优化清单** → 追加一行到 `releases/<version>/optimizations.md`，走简化流程 §⑪

## ③ 确定作者

询问：

> "你的名字拼音全拼是什么？"（如 author-c、author-b）

必须用拼音全拼，不缩写。如果用户给了缩写（如 fanglh），纠正为全拼（author-c）。

## ④ 收集文件

### PRD 文件

先让用户提供文件路径：
> "PRD 文件在哪个位置？把文件路径给我。（可以直接拖文件到终端）"

**命名规则：** `v{班车版本号}-{模块}.md`。模块名 = `docs/module-map.md` 中的目录名（如 `analytics`），一个版本一个模块一个 PRD。

**同版本同模块合并规则：** 如果目标路径已存在同文件，说明该版本该模块已有 PRD。不是覆盖，而是**合并追加**：将新内容追加到现有文件末尾，更新变更记录。

**跨版本迭代规则：** 每次班车迭代建新文件，旧版本冻结不动：
```
author-a/
  v1.0-your-feature.md    ← 首版冻结
  v1.3-feature-x.md    ← 迭代版（新文件）
```

确认目标路径后告知用户：
> "将保存为 `docs/prd/v1.0-your-feature.md`，对吗？"

### Demo 文件

> "你的 Demo 文件在哪个目录？把目录路径给我。（包含 index.html, tokens.css, demo.css, demo.js）"

检查目录下是否有这 4 个文件。如果有缺失，告知用户缺了哪些。

> "这个 Demo 的功能名称是什么？"（中文名，如 质量任务、数据血缘DAG）

**目录结构：**
```
demos/<author>/v{版本号}-{模块}/{功能中文名}/
```

外层路径对齐 PRD（`v{版本号}-{模块}`），内层按功能中文名分目录。

确认：
> "将保存为 `docs/billing/demos/author-c/v1.2-billing/角色配置/`，对吗？"

## ⑤ 放置文件

用户确认后：

1. 创建目标目录 `docs/<module>/{prd,demos}/<author>/<filename-or-dir>/`
2. 用 `cp` 复制文件到目标位置（PRD 单个文件，Demo 整个目录）
3. 检查文件是否复制成功

## ⑥ 更新 INDEX

读取 `docs/<module>/{prd,demos}/INDEX.md`，追加一行记录：

**PRD INDEX 追加格式：**
```markdown
| v{版本号} | <author>/v{版本号}-{slug}.md | <author> | 草稿 | <MMDD> |
```

**Demo INDEX 追加格式：**
```markdown
| <场景中文> | <author>/v{版本号}-{模块}/{功能中文名}/ | <author> | <一句话说明> | 完成 |
```

如果 INDEX 表当前全是 `-` 占位行，替换第一行占位行；否则追加新行。

## ⑥.⑤ 更新 release README（自动扫描生成）

Release README 不再手动逐条更新，而是**每次上传后自动扫描重新生成**。

### 生成逻辑

1. 读取 `releases/<version>/README.md` 模板头部（状态、日期等元信息）
2. 扫描 `docs/*/prd/**/v{version}-*.md` 找到所有该版本 PRD
3. 扫描 `docs/*/demos/**/v{version}-*/` 找到所有该版本 Demo
4. 按模块聚合，重新生成 `## 📄 涉及 PRD` 和 `## 🔗 相关 Demo` 两张表格

### PRD 扫描

对每个匹配 `v{version}-{module}.md` 的文件：
- 提取模块名（从路径 `docs/<module>/prd/` 中提取）
- 提取作者（从文件父目录名）
- 生成链接

### Demo 扫描

对每个匹配 `v{version}-{module}/` 的目录：
- 列出内层 `{功能中文名}/` 子目录（含 index.html 的）
- 提取模块名、场景名、作者

### 更新 releases/INDEX.md

如果该版本在 INDEX 中的"涉及模块"列不包含当前模块，追加模块名。

## ⑦ 确认提交（禁止直接提交）

文件放置、INDEX 更新、变更记录全部就绪后，**禁止直接 commit**。必须先向用户展示变更摘要，等待用户确认。

### 展示变更摘要

列出所有将要提交的内容：

```
📋 待提交变更确认

模块：feature-x (feature-x)
操作：上传 PRD（新版本 v1.2）
作者：author-b
班车：V1.0.4

变更文件：
  M  docs/prd/author-b/v1.2-user-apply.md   (PRD 内容更新)
  M  docs/prd/INDEX.md                          (索引更新)
  M  docs/CHANGELOG.md                          (变更日志)
  M  releases/v2.0/README.md                                  (发布说明)
  M  releases/INDEX.md                                        (版本索引)

提交信息：
  feat(feature-x): upload prd v1.2 by author-b - 新增新增筛选、批量操作

确认提交？回复"确认"或"可以"执行提交，回复"取消"放弃。
```

### 用户确认后执行

只有用户明确回复"确认""可以""提交""OK"等肯定词后，才执行 §⑧。

### 用户取消

用户回复"取消""不提交""算了"等，放弃所有变更：

```bash
git checkout -- .   # 撤销所有未提交的修改
```

告知用户："已取消，文件未提交。"

## ⑧ 执行提交

用户确认后执行：

```bash
git add -A
git commit -m "<confirmed-message>"
git push
```

## ⑨ 报告结果 + 团队变更通知

上传完成后输出两个部分：

### 第一部分：简要确认

```
✅ 已上传并推送！
模块：feature-x / 类型：PRD / 提交：ac55f9d
```

### 第二部分：团队变更通知（必须输出）

格式固定为一行分隔线 + 版本标识 + 汇总 + 入口清单，方便 PM 直接复制发送给开发/测试：

```
---
📦 V{major}.{minor}.{iteration} 班车本次变更，涉及 N 个模块，PRD + Demo 共 M 个入口：

{模块名}
  {文件路径}  →  {版本号}
  内容：{一句话说明}

{模块名}
  {文件路径}  →  {版本号}
  内容：{一句话说明}

...
```

**规则：**
- 按模块分组，每个文件一行路径 + 一行内容说明
- 路径使用 repo 相对路径，可直接跳转
- 新文件标注 `→ v1.0（新增）`
- 已有文件标注 `→ v2.2 → v3.0` 格式显示版本变化
- Demo 目录标注 `→ 交互原型`
- 内容说明控制在 20 字以内，说清改了什么

**示例输出：**

```
---
📦 V1.0.4 班车本次变更，涉及 3 个模块，PRD + Demo 共 4 个入口：

feature-x
  docs/prd/author-b/v1.2-user-apply.md  →  v1.2
  内容：资产列表 6 类 Tab、空间视图切换、申请去掉工作空间选择

  docs/prd/v1.0-your-feature.md  →  v1.2（新增）
  内容：功能模块一级模块，跨空间服务浏览、购物车、按空间拆分审批单

  docs/demos/v1.0-your-feature/功能模块/  →  交互原型
  内容：功能模块交互 Demo，打开 index.html 查看效果

数据管理
  docs/file-management/prd/author-d/v1.2-file-management.md  →  v1.2
  内容：数据源空间级配置、密码保护、权限开关、表授权全部表/单表模式

admin-config
  docs/prd/v1.0-your-feature.md  →  v1.2（新增）
  内容：租户级算子管理，租户管理员 CRUD，自动下发至所有空间

📋 完整发布说明：releases/v2.0/README.md
```

## ⑩ PRD 变更记录（必做）

PRD 上传/更新后，**必须**询问变更内容。这是必问项，不可跳过：

### 新 PRD（目标路径不存在）

> "这个 PRD 是全新创建，还是有前置版本？
> - 如果是全新的：我标注为初始版本
> - 如果基于旧版本修改：旧 PRD 文件在哪个路径？"

全新：自动写入初始变更记录。
基于旧版：对比两个文件，询问主要变更点。

### 版本更新（目标路径已存在同作者 PRD）

> "检测到已有 `v1.0-your-feature.md`，这次更新主要变更了哪些内容？"

用户用自然语言描述即可，如："新增了数据表角色配置，API申请流程，把批量勾选改为支持统一提交"

### 自动写入

将变更内容写入两个位置：

**a) PRD 文件末尾追加/更新变更记录表：**

```markdown
## 变更记录

| 版本 | 日期 | 作者 | 变更内容 |
|-----|------|------|---------|
| v1.1 | 0611 | author-b | 新增数据表角色配置(R11-R15)、API申请(R16-R18)；批量勾选支持统一提交 |
| v1.0 | 0610 | author-b | 初始版本：数据集角色配置流程 |
```

**b) 模块级 `docs/<module>/CHANGELOG.md`：**

读取或创建 CHANGELOG，顶部追加条目：

```markdown
## 2026-06-11
- **v1.2** [数据集申请流程](prd/author-b/v1.2-user-apply.md) by author-b
  - 新增：数据表角色配置（数据查看/编辑/表编辑）
  - 新增：API应用角色配置
  - 变更：批量勾选统一提交
```

### 提取变更摘要规则

从用户自然语言描述中提取为简短要点（每条 <30 字），前缀标注：
- `新增：` — 新功能/需求
- `变更：` — 修改已有行为
- `删除：` — 移除的功能
- `修复：` — 问题修正

## ⑪ 优化清单录入

当 PM 描述单点小改动（不涉及新页面/新流程），主动问：「这个算优化清单还是单独写 PRD？」

### 触发判断

以下情况建议走优化清单：
- 改动单点、一句话能说清
- 不涉及新页面/新流程
- 文案、样式、校验规则等小调整

如果用户明确说"记个优化""优化清单加一条"，直接进入优化清单流程。

### 录入流程（极简，无需 §①-⑩ 完整流程）

**第一问：确认版本和模块**

> "归入哪个班车版本？哪个模块的优化？"

版本必确认（复用 §①.⑤ 逻辑）。模块用编号选择（复用 §① 逻辑）。

**第二问：收集信息**

> "一句话描述优化内容，类型和优先级（P0-P3）："

确认：
- 优化点：一句话描述
- 类型：`UI` / `交互` / `规则`
- 优先级：`P0` / `P1` / `P2` / `P3`
- 备注：可选（关联 PRD、需求编号等）

### 写入操作

1. 检查 `releases/<version>/optimizations.md` 是否存在
2. **不存在** → 自动创建文件，初始化模块分区（读取 `docs/module-map.md` 生成所有模块的 `## 模块名` 空分区）
3. 找到对应模块的 `## 模块名` 分区，在表格末尾追加一行：

```markdown
| N | 优化点描述 | UI/交互/规则 | P0-P3 | 可选备注 |
```

序号自动递增。

### 不触发的操作

- 不更新 `docs/<module>/prd/INDEX.md`
- 不更新 `docs/<module>/CHANGELOG.md`
- 不更新 `releases/<version>/README.md`
- 不执行 §⑥、§⑥.⑤、§⑩

### 提交

用户确认后执行：

```bash
git add releases/<version>/optimizations.md
git commit -m "chore(release): add optimization to <version> - <模块>：<优化点摘要>"
git push
```

报告：
```
✅ 已记录优化点！
版本：V1.0.0-beta / 模块：数据质量 / 类型：UI / 优先级：P2
内容：「质量报告页默认展开第一个规则」
```

## 常见情况处理

### 用户不知道模块
如果用户不确定属于哪个模块，根据 PRD 内容或 Demo 标题的关键词推荐：
- 提到"订单/购物车/结算" → order-system
- 提到"报表/统计/图表" → analytics
- 提到"通知/邮件/消息" → notification
- 提到"用户/账号/登录" → user-system
- 提到"支付/账单/发票" → billing
- 提到"文件/上传/附件" → file-management
- 提到"内容/文章/帖子" → content
- 提到"设置/配置/参数" → settings

### 同一作者同一版本多个 Demo
内层按功能中文名分目录自然区分（如 `v1.2-billing/角色配置/` 和 `v1.2-billing/账单查询/`），无需特殊处理。

### 文件已存在
如果目标路径已存在，询问用户是否覆盖：
> "目标位置已存在文件，要覆盖吗？"

### 缺少必需文件
如果 Demo 目录中缺少 index.html 或其他 3 个文件，列出缺少项，暂停等用户补全。

## 项目约定

- 仓库根目录：`/path/to/your/project`
- 分支：`dev`
- 模块列表：见 `docs/module-map.md`
- 命名规则：见 `docs/convention.md`
- Demo 固定四个文件：index.html, tokens.css, demo.css, demo.js
- PRD 命名：`v{班车版本号}-{slug}.md`（如 `v1.0-your-feature.md`）
- PRD 迭代：每次发版建新文件，旧版本冻结不动
- Demo 目录：`v{版本号}-{模块}/{功能中文名}`
- Release 结构：见 `docs/convention.md` §Release 结构
- 班车版本格式：`v{major}.{minor}.{iteration}`（如 v2.0）
- Release README 模板：`shared/templates/release-readme-template.md`

## 班车发布

当 PM 说"V1.0.4 发布""X 版本发版""发布 V1.0.4"时，自动执行：

### 发布前检查

1. 读取 `releases/<version>/README.md`
2. 检查是否有内容（至少有一个模块的功能条目）
3. 如果为空，提示："这个版本还没有任何 PRD/Demo，确定要发布吗？"

### 执行发布

1. 将 README.md 状态从"收集中"改为"已发布"
2. 补充/确认发布日期
3. 在 README 顶部生成发布摘要（从各模块表格聚合）
4. 更新 `releases/INDEX.md`：状态改为"已发布"，填入发布日期
5. git tag `<version>`
6. commit & push

### 发布后通知

```
---
🚀 V1.0.4 已发布！

本次发布包含 3 个模块、5 个功能：
- feature-x：功能模块、数据集申请
- 数据采集：数据集血缘
- 数据管理：数据源管理

📋 完整发布说明：releases/v2.0/README.md
🔖 Git tag：v2.0
```

## 功能延期/撤出

当 PM 说"XX 功能延期到 V2.4"或"XX 从 V1.0.4 撤出"时：

1. 从 `releases/<old-version>/README.md` 中移除对应行
2. 如果目标版本存在，追加到 `releases/<new-version>/README.md` 对应模块表格
3. 如果目标版本不存在，提示用户先创建新班车
4. 更新两个版本的 `releases/INDEX.md`（涉及模块列）
