---
name: "note-review-enhance"
description: "Use when user provides raw study notes, learning materials, or course notes and asks for AI-enhanced structured output, note auditing, content enrichment, or conversion to Obsidian Markdown format"
---

# 学习笔记审核与增强

学习笔记审核与增强专家。对原始笔记进行完整留存、审核纠错、补齐增强与结构化输出，生成符合 Obsidian 语法规范的 Markdown 笔记。支持可选衍生输出：知识地图（Markdown）与思维导图（XMind）。

## When to Use

加载此 skill 的触发条件：

- 用户提供了一段学习笔记、课堂笔记或课程资料
- 用户要求"增强"、"审核"、"优化"、"整理"笔记
- 用户要求转换为 Obsidian Markdown 格式
- 用户要求生成知识地图、思维导图等衍生输出
- 用户反馈已生成的增强笔记有遗漏或错误，需要迭代更新

## When NOT to Use

- 用户仅要求翻译笔记（无增强需求）
- 用户要求从零创作新内容（非基于已有笔记）
- 用户提供的是已经高度结构化的文档（无需重组）
- 用户要求写代码/调试程序 → 使用 coding/debugging skills
- 用户要求分析数据 → 使用 data-analysis skills
- 用户要求生成图片/视频 → 使用 creative skills

## Quick Reference

| 输入 | 输出 | 触发条件 |
|------|------|---------|
| 原始笔记 `.md` | `N.主题（AI增强版）.md` | 用户要求增强笔记 |
| 多篇原始笔记 | `知识地图.md` | 用户要求知识地图 |
| 增强版笔记 | `[主题]思维导图.xmind` | 用户要求思维导图 |
| 已增强笔记 + 反馈 | 增量更新补丁 | 用户要求补充/修正 |

| 验收项 | 通过标准 |
|--------|---------|
| 语法验收 | 7项全部通过（参见 `references/obsidian-format.md`） |
| 逻辑验收 | 11项全部通过（含概念完整性） |
| 概念完整性 | 增强版 ≥ 原始笔记（不得简略） |
| 图片资源 | 迁移成功 + 验证存在 + 清理未引用 + 无占位符 |

## Core Pattern

### Step 1: 输入预处理
1. 提取原始笔记中的所有概念、定义、流程、代码、图片引用
2. 复制图片到 `asset/` 目录（迁移→验证→清理三步法）
3. 识别并删除空模板（无需记录）

### Step 2: 概念完整性核对（关键！）
- 逐条对照原始笔记，确认每个概念在增强版中有等价或更详细的表达
- **禁止行为**：将正文描述压缩为 callout、仅保留名词不保留解释、删除流程步骤、丢失 A=B 对应关系
- **强制规则**：原始笔记中"定义+用法+关联+局限"的完整链条不得拆解丢失；A=B 对应关系必须保留
- 若概念位置变动，在"8️⃣ AI 附加说明"的"👣 结构调整说明"中标注

### Step 3: 审核纠错
- 知识正确性 → 用 `[!bug]` callout 标注修正
- 代码可用性 → 按三级标准处理（可独立运行 / 依赖内置数据 / 依赖外部文件）
- 逻辑一致性 → 矛盾处用 `[!warning]` 标注
- 标注 ≥5 处时，正文内省略行内标注，集中到"AI 附加说明"

### Step 4: 补齐增强
- 缺失定义 → 补充
- 核心概念 → 提供 ≤10行可运行代码示例
- 易混概念 → 添加对比表（至少1组）
- 复杂逻辑 → 提供分步演算
- 扩展块 → 按 N 值区间规则插入（基础：N≤3→1个, N=4~6→1~2个, N≥7→2~3个；进阶：N≥3→1个, N≥6→1~2个）

### Step 5: 结构化输出
- 严格按输出格式骨架组织（参见 `references/output-format.md`）
- 执行语法验收（7项）+ 逻辑验收（11项）
- 输出最终笔记 + AI 附加说明

### Step 6: 可选衍生输出
- 知识地图 → 参见 `references/mindmap-format.md` 第一章
- 思维导图 → 参见 `references/mindmap-format.md` 第二章

## Implementation

详细规范参见 `references/` 目录：

| 规范内容 | 参考文件 |
|---------|---------|
| Markdown 输出格式骨架 | `references/output-format.md` |
| 主题内分层归纳指南（附录A） | `references/output-format.md` |
| 难度标签判定矩阵（附录B） | `references/output-format.md` |
| Obsidian 格式适配规范 | `references/obsidian-format.md` |
| 语法验收标准（7项） | `references/obsidian-format.md` |
| 笔记逻辑验收标准（11项） | `references/obsidian-format.md` |
| 质量自检清单 | `references/obsidian-format.md` |
| 知识地图与思维导图格式 | `references/mindmap-format.md` |

## Special Cases

| 场景 | 处理 |
|------|------|
| 原笔记明显错误 | 修正 + `[!bug]` 标注 + 记录到修正记录 |
| 原笔记缺失关键定义 | 主动补充 + 在 AI 附加说明中列出 |
| 原笔记代码无法运行 | 修正 + `[!bug]` 标注 + 提供运行结果 |
| 原笔记逻辑矛盾 | 按正确知识统一 + 修正记录说明 |
| 原笔记过于简略 | 要求用户补充信息，先输出已整理部分 |
| 原笔记缺少深度内容 | 强制插入 ≥3 处扩展块（若 N≥3） |
| 原笔记包含图片引用 | 迁移到 asset/ + 验证 + 清理未引用 |
| 原笔记大量空模板 | 自动过滤，无需逐条记录 |

## Iteration

当用户对增强笔记提出补充/修正反馈时：

1. **分类反馈类型**：
   - 内容类（概念遗漏/错误）→ 回溯 Markdown 增强版修改
   - 结构类（层级/组织问题）→ 回溯 Markdown 增强版修改
   - 样式类（颜色/字体/布局）→ 针对 XMind/theme 调整
   - 格式类（文件打不开）→ 检查 XMind ZIP 结构
2. **内容/结构类**：增量生成扩展块，标注插入位置，保持原有内容不变
3. **样式/格式类**：记录变更到 Technical Notes，更新 XMind 生成脚本
4. **提供全量合并版本**（若用户要求）

## Common Mistakes

### AI 执行时常见错误

| 错误 | 后果 | 修复 |
|------|------|------|
| 将原始笔记正文描述压缩为 callout | 概念丢失，用户反馈"简略" | 正文必须保留完整描述，callout 仅用于扩展补充 |
| 仅保留名词不保留解释 | 知识点悬空 | 每个名词必须有定义或用法说明 |
| 删除原始笔记中的流程步骤 | 流程断裂 | 步骤必须完整保留，可重组但不可删除 |
| 丢失 A=B 对应关系 | 概念无法落地 | 如"L1正则化"必须对应"Lasso回归" |
| 图片只迁移不验证 | 引用失败 | 迁移后必须验证文件存在 |
| 未清理未引用图片 | 垃圾文件堆积 | 生成后扫描并删除未引用图片 |
| 保留 `[[filename.png]]` 占位符 | 显示失败 | 占位符必须删除或在不确定项中标注 |
| XMind manifest 放错位置 | 文件无法打开 | manifest.json 必须在 ZIP 根目录 |
| 给子节点加 `"class": "topic"` | 样式不生效 | 只有 rootTopic 加 class |
| 用 notes 字段存描述 | 描述不显示 | 描述直接作为子节点展示 |

### 用户反馈常见模式

| 反馈 | 原因 | 处理方式 |
|------|------|---------|
| "概念简略了" | 原始笔记描述被压缩或删除 | 回溯到原始笔记，补回缺失内容 |
| "层级不够" | 中间分类节点缺失 | 增加"概述/特点/API"等分类节点 |
| "图片显示失败" | 图片未迁移或占位符未处理 | 检查 asset/ 目录 + 清理占位符 |
| "XMind 打不开" | 格式不兼容 | 检查 manifest 位置、metadata 版本、JSON 结构 |

## Technical Notes

- **图片复制**：Windows 某些目录 shutil.copy2 可能权限失败，使用 os.path.join + shutil.copy2 组合
- **XMind 2026 格式**：ZIP 必须包含 content.json + manifest.json（根目录JSON）+ metadata.json（dataStructureVersion:"3"），不得有 META-INF/
- **Obsidian WikiLink 误报**：`[[笔记名]]` 是内部链接不是图片引用，正则匹配时需过滤
- **XMind 节点规则**：rootTopic 加 `"class":"topic"` 和 `"structureClass"`，子节点不加
- **XMind 旧文件残留**：生成前必须 os.remove() 删除旧文件，否则 ZIP 中会残留旧格式文件导致报错

---
**Skill 版本：v3.6**
