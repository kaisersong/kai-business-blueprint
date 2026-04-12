# 对抗性 Review：`business-blueprint-skill` 设计稿

Date: 2026-04-12  
Reviewer: Adversarial Review Pass  
Target: `business-blueprint-architecture-skill-design.md`  
Status: Draft for discussion

---

## 总体判断

设计稿骨架扎实，IR-first 原则、语义与布局分离、Python-first 零构建等方向都是正确的。但有几处**结构性断层**，不处理的话会在第一个真实项目里暴露，而不是在后期迭代中。以下按严重程度排列。

---

## 🔴 严重问题（会在第一次真实使用时爆）

### 1. 静态 HTML "轻编辑" + 无服务器 = 保存回路根本没有设计

文档说：

> viewer 允许轻量语义编辑 → 写回布局 hints → 不依赖服务器

但没有回答最核心的问题：**用户在 viewer 里改了一个标签，然后怎么办？**

静态 HTML 唯一能做的是：

1. 用户在浏览器里编辑 → JS 内存持有修改后状态
2. 用户手动点"导出 JSON" → 下载一个新文件
3. 下次用 `--generate` 时，用户必须手动传入这个新文件

这是一个**非常摩擦的工作流**。更危险的是：如果用户改了 viewer，但下游 AI pass 拿的是旧 JSON，编辑会被静默覆盖。

文档根本没有描述这个"保存回路"。这不是实现细节，是**核心交互合同**，必须在设计阶段明确。

---

### 2. 跨视图联动是原则，但没有执行约束 → 三个视图会静默分裂

文档说 capabilities 是业务锚点，flow steps 引用 capability，systems 引用 capability。

但：

- 联动是**可选**的（`capabilityIds`，非必填）
- AI 在 Ingest 阶段可能先生成 application architecture，此时 capabilities 还没有
- 没有任何验证规则检查 **"系统覆盖率"** 或 **"流程步骤覆盖率"**

实际结果：三张图在格式上是 one model，但语义上仍然是三个互相不知道对方的孤岛。"一个语义模型，三个视图"的核心价值主张就空洞了。

**需要设计**：跨视图完整性的 minimum required linkage 是什么？至少要有一个可执行的 linkage completeness 评分，而不只是一条原则。

---

### 3. AI 实体抽取没有实体消歧协议 → IR 会充斥同义实体

Ingest phase："从文本提取候选实体，规范同义词，映射到稳定分类"

但没有回答：

- 同一个系统在不同来源里叫"ERP"、"SAP"、"业务系统"时怎么处理？
- 用户说"我们有个 CRM"，AI 提取了 `sys-crm`，后来又说"Salesforce"，AI 新建了 `sys-salesforce`——谁管它们是同一个？
- **没有 entity resolution 协议**，也没有 deduplication 策略

Stable ID 的价值建立在"每个真实概念只有一个 ID"这个前提上。这个前提在 AI-generated 场景下非常脆弱。

---

## 🟡 设计缺陷（会造成持续困惑，但不会立刻崩）

### 4. Patch Log 标记为 Optional，但它是 AI 协作的基础设施

文档说 patch log "optional in the first release"。

问题：如果没有 patch log：

- AI 不知道哪些是人工编辑，哪些是它自己生成的
- 用户在 viewer 里手改了 5 个标签，然后让 AI "再生成一遍集成图"，AI 会覆盖人工编辑
- 没有任何手段可以做 "人工编辑 + AI 建议" 的合并

这不是 optional feature，这是**防止 AI 覆盖人工输入的最低保障**。退一步说，就算 v1 不实现完整 patch log，也必须有某种机制标记哪些字段是 human-locked。

---

### 5. Clarify Phase 没有可执行定义

"提出少量高价值澄清问题，仅在关键信息缺失时"

- 谁定义"关键"？哪些字段缺失触发澄清？
- 在 headless / Claude Code 场景里，Clarify phase 怎么运行？
- 澄清结果写回到 JSON 的哪个字段？

这个 phase 目前是"美好意图"，不是可以实现的规格。如果不写清楚，每个实现者的理解都不同，最终要么跳过，要么产生一个半交互式的怪物。

---

### 6. Command Surface 的调用者身份模糊

```
--plan / --generate / --edit / --export / --validate
```

这看起来是 CLI flags，但这是一个 Skill。**谁调用这些命令？**

- 如果是 AI agent 调用：AI 怎么知道该用 `--generate` 还是 `--edit`？根据什么判断？
- 如果是用户直接调用：这是 CLI 工具，不是 Skill
- 如果是另一个 Skill 调用：Skill-to-Skill 的调用约定在哪里？

这个 command surface 是从 `report-creator` 借来的，但 report-creator 的调用者更清晰。Blueprint skill 涉及多轮交互和多 phase 工作流，单次命令调用模型可能本身就不合适。

---

### 7. 三种图类型是假设，不是验证过的 presales 需求

文档直接设定三个视图：业务能力图、泳道流程、应用架构。

但：

- 没有说这三个是从哪里来的（客户访谈？竞品分析？个人经验？）
- Presales 常见的需求还有：价值实现路径图、竞品定位矩阵、方案对比表、实施路径时间线
- 文档把 deployment topology 直接排除在外，但这是很多客户对话的核心

三个视图的选取逻辑没有暴露出来，意味着后续任何扩展或调整都没有决策依据。

---

## 🟢 小问题（可以后处理，但值得标记）

### 8. 验证输出格式未定义

文档说"验证输出应该是结构化的，以便另一个 AI pass 可以程序化修复"，但没有定义这个结构是什么。

至少需要：

- `severity`（error / warning / info）
- `error_code`（可机读）
- `affected_ids`（受影响实体）
- `suggested_fix`（修复 hint）

没有这个，"AI 自动修复"是个空头支票。

---

### 9. Industry Packs 的边界没有定义

"不能将用户锁定在按行业划分的独立代码路径中" → 但 pack 提供"visual grouping defaults"和"terminology alignment"

这两个功能隐含 view-level 定制，会产生按行业分叉的渲染逻辑。**pack 和 code path 的边界在哪里**，文档没有给出答案。

---

### 10. "现有图表作为参考输入" 的 "weak" 语义不清楚

> existing diagrams as weak reference input

"weak" 是什么意思？

- 只接受文本可提取的 Visio / draw.io XML？
- 接受截图（vision input）？
- 接受用户口头描述的图表？

如果用户的主要现有资产是 PPT 里的截图，这个特性对他们毫无用处。需要明确边界，否则用户期望管理会失控。

---

## 总结表

| # | 问题 | 严重程度 | 必须在 v1 解决？ |
|---|------|---------|--------------|
| 1 | 静态 viewer 保存回路未设计 | 🔴 严重 | ✅ 是 |
| 2 | 跨视图联动无执行约束 | 🔴 严重 | ✅ 是 |
| 3 | 实体消歧 / 去重无协议 | 🔴 严重 | ✅ 是 |
| 4 | Patch log 降级为 optional | 🟡 设计缺陷 | 建议 v1 加最小版本 |
| 5 | Clarify phase 无可执行定义 | 🟡 设计缺陷 | ✅ 是 |
| 6 | Command surface 调用者模糊 | 🟡 设计缺陷 | ✅ 是 |
| 7 | 三视图选取无验证依据 | 🟡 设计缺陷 | 不强制，但要记录决策理由 |
| 8 | 验证输出格式未定义 | 🟢 小问题 | v1 前需要 |
| 9 | Industry pack 边界模糊 | 🟢 小问题 | 可 v1.1 |
| 10 | "weak diagram input" 语义不清 | 🟢 小问题 | 应明确边界或删除该特性 |

---

## 最高优先级行动项

最需要立刻补充的两个设计决策：

**① 保存回路（viewer ↔ canonical JSON 的双向流）**
明确用户在 viewer 编辑后，文件如何更新、如何传递给下一次 AI pass，以及如何防止 AI 覆盖人工编辑。

**② 实体消歧协议**
定义 AI 在 Ingest / Normalize 阶段如何识别同义实体、如何决定合并还是新建、如何处理跨来源的命名冲突。

这两个不是实现问题，是必须在 spec 里讲清楚的**人机协作合同**。
