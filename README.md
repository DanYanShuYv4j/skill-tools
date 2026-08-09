# AI Skill 工具箱

产品经理的 AI 工作流工具箱。出自「产品小祥聊AI」的实际工作流。

## 这是什么

给 Claude 这类 AI 用的"工作说明书"（圈内叫 Skill）。告诉 AI：遇到什么情况、按什么步骤、产出什么东西。

```
描述场景 → AI 执行 Skill → 产出结果
```

## 产品经理系列（5 个 Skill，覆盖完整工作流）

| # | Skill | 作用 | 触发词 |
|---|-------|------|--------|
| 1 | **prd-generator** | 写PRD | "写PRD""帮我写需求" |
| 2 | **interactive-demo-generator** | 画原型 | "画原型""做个Demo""生成可交互原型" |
| 3 | **interaction-review** | 审交互 | "审交互""帮我审查""交互检查" |
| 4 | **test-case-generator** | 出测试 | "出测试用例""生成测试" |
| 5 | **pm-upload** | 归档 | "上传PRD""提交文件""帮我归档" |

### 工作流串联

```
需求 → prd-generator（写PRD）
     → interactive-demo-generator（画原型）
     → interaction-review（审交互）
     → test-case-generator（出测试）
     → pm-upload（归档到仓库）
```

### 1. prd-generator — 写PRD

让 AI 一步步追问、逼你想闭环。5 步对话（背景→用户故事→角色权限→功能需求→边界场景）+ Given/When/Then 验收条件 + AI 主动列异常清单。

```
"写PRD" → AI 逐步追问 → 你确认 → 生成完整PRD
```

详见 `prd-generator/SKILL.md`

### 2. interactive-demo-generator — 画原型

把 PRD 或截图变成可交互的 HTML 原型。四阶段工作流：理解需求→生成原型→交互验证→交付。支持五态覆盖（正常/空态/加载/错误/禁用）。

```
"画原型" → 读取PRD/截图 → 生成可交互HTML → 验证交互
```

详见 `interactive-demo-generator/SKILL.md`

### 3. interaction-review — 审交互

7 层交互审查模型，自动扫描原型或截图，输出 P0/P1/P2 分级报告。覆盖：信息架构、任务流、可见性、组件状态、反馈、一致性、认知负担。

```
"审交互" → 给原型/截图 → 自动逐层扫描 → 输出问题清单
```

详见 `interaction-review/SKILL.md`

### 4. test-case-generator — 出测试

按 PRD 自动生成测试用例。正反各一（正常路径+异常路径），绝不截断，按功能模块分组。

```
"出测试用例" → 读取PRD → 生成分模块测试用例
```

详见 `test-case-generator/SKILL.md`

### 5. pm-upload — 归档

对话式 git 上传，产品经理不用懂 git 命令。AI 自动判断文件类型、放到正确目录、更新索引、提交推送。

```
"上传PRD" → AI 对话确认模块/版本/作者 → 自动提交推送
```

详见 `pm-upload/SKILL.md`

## 工具类 Skill（2 个）

| Skill | 作用 | 触发词 |
|-------|------|--------|
| **skill-builder** | 造新 Skill | "帮我创建一个Skill" |
| **skill-quality-evaluator** | 给 Skill 打分 | "审查这个Skill" |

## 快速上手

### 方式一：装进 Claude Code

把文件夹放进 `.claude/skills/` 目录，然后在对话里说触发词。

### 方式二：直接用

把 SKILL.md 内容告诉你的 AI，然后描述你的场景。

## 作者

产品小祥聊AI。干了六年研发，转做产品。写真实判断，不写教程。

> 系列文章见公众号「产品小祥聊AI」——《产品经理的AI技能》系列
