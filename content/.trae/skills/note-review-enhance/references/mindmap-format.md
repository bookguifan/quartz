# 知识地图与思维导图输出格式规范

> **适用范围**：当用户要求基于已增强的学习笔记生成知识地图（Markdown 目录索引）或思维导图（XMind）时，AI 应遵循本规范输出。
> **前置依赖**：必须先完成 Markdown 增强版笔记的生成，知识地图和思维导图必须基于增强版内容生成，不得基于原始笔记。

---

## 一、知识地图（Markdown 目录索引）

### 1.1 触发条件

用户明确说"生成知识地图"、"整理成目录"、"生成概念索引"等。

### 1.2 输出文件

- **文件路径**：与增强版笔记同目录，文件名为 `知识地图.md` 或 `[主题]知识地图.md`
- **内容来源**：基于已生成的全部增强版笔记（N.主题名（AI增强版）.md）聚合提取

### 1.3 格式骨架

```markdown
# [主题] 知识地图

## 左栏：概念速查索引

### [概念类别1]
- **[概念A]**：[一句话定义]（来源：[[N.主题名（AI增强版）]]）
- **[概念B]**：[一句话定义]（来源：[[N.主题名（AI增强版）]]）

### [概念类别2]
...

## 右栏：学习路径与关联

### 学习路径
```
阶段1 → 阶段2 → 阶段3
```

### 知识网络
- **课内联动**：[概念A] 与 [概念B] 的关系
- **前后衔接**：前置知识 → 当前主题 → 后续延伸

## sklearn API 速查

| 算法 | 核心类 | 关键参数 | 适用场景 |
|------|--------|---------|---------|
| [算法名] | `[类名]` | [参数] | [场景] |

## FAQ

> **Q1**：[常见问题]
> **A1**：[简明回答]

## 标签云

#[主题标签] #[子标签1] #[子标签2] ...
```

### 1.4 生成规则

1. **概念索引**：从每篇增强版笔记的"1️⃣ 完整知识库"模块提取核心概念，按逻辑分类组织，每个概念附一句话定义和来源链接。
2. **学习路径**：根据笔记序号（day01→day02...）或逻辑依赖关系排列学习顺序。
3. **API 速查**：仅当主题涉及 sklearn/框架 API 时生成，提取增强版中的速查卡片信息。
4. **FAQ**：从增强版笔记的"避坑指南"模块提取高频问题。
5. **来源链接**：使用 Obsidian 内部链接 `[[笔记名]]` 指向增强版笔记。

---

## 二、思维导图（XMind）

### 2.1 触发条件

用户明确说"生成思维导图"、"XMind版本"、"可视化知识网络"等。

### 2.2 输出文件

- **文件路径**：与增强版笔记同目录，文件名为 `[主题]思维导图.xmind`
- **内容来源**：基于已生成的增强版笔记 + 知识地图内容聚合
- **格式**：XMind 2026 兼容格式（ZIP 包含 content.json + manifest.json + metadata.json）

### 2.3 XMind 2026 文件格式规范

AI 必须通过 Python 脚本生成 `.xmind` 文件，不得仅提供文本描述让用户手动创建。

#### 2.3.1 ZIP 结构

```
[文件名].xmind
├── content.json      # 主数据文件（JSON）
├── manifest.json     # 文件清单（ZIP根目录，JSON格式）
└── metadata.json     # 元数据（dataStructureVersion: "3"）
```

#### 2.3.2 content.json 结构

```json
[
  {
    "id": "uuid",
    "revisionId": "uuid",
    "class": "sheet",
    "title": "画布 1",
    "rootTopic": {
      "id": "uuid",
      "class": "topic",
      "title": "[中心主题]",
      "structureClass": "org.xmind.ui.logic.right",
      "extensions": [
        {
          "provider": "org.xmind.ui.map.unbalanced",
          "content": [{"name": "right-number", "content": "-1"}]
        }
      ],
      "children": {
        "attached": [
          // 主分支列表
        ]
      }
    },
    "arrangeableLayerOrder": ["rootTopic-id"],
    "zones": [],
    "extensions": [
      {
        "provider": "org.xmind.ui.skeleton.structure.style",
        "content": {"centralTopic": "org.xmind.ui.logic.right"}
      }
    ],
    "theme": { /* 参见 2.3.4 */ }
  }
]
```

#### 2.3.3 节点结构规则

**根节点（rootTopic）**：
- 必须包含 `"class": "topic"` 和 `"structureClass": "org.xmind.ui.logic.right"`
- 必须包含 `"extensions"` 数组（如上所示）
- 标题为中心主题（如"机器学习(ML)"）

**子节点**：
- 基本结构：`{"id": "uuid", "title": "节点标题"}`
- 有子节点的分支必须添加 `"branch": "folded"`
- **不要**给子节点添加 `"class": "topic"` 或 `"structureClass"`
- 子节点的内容直接作为子节点展示，不使用 notes 字段存储描述

**节点内容组织原则**：
- 每个知识点用一句话描述作为节点标题（5-15字）
- 长描述拆分为多个原子节点，而不是一个长标题
- 使用中间分类节点承上启下（如"概述"、"特点"、"API"）

#### 2.3.4 Theme 配置（必须包含）

```json
{
  "subTopic": {
    "id": "uuid", "properties": {
      "fo:font-family": "Droid Serif", "fo:font-size": "14pt",
      "shape-class": "org.xmind.topicShape.roundedRect",
      "line-class": "org.xmind.branchConnection.roundedElbow"
    }
  },
  "centralTopic": {
    "id": "uuid", "properties": {
      "fo:font-family": "Droid Serif", "fo:font-size": "30pt",
      "svg:fill": "#000229", "shape-class": "org.xmind.topicShape.roundedRect"
    }
  },
  "mainTopic": {
    "id": "uuid", "properties": {
      "fo:font-family": "Droid Serif", "fo:font-size": "18pt",
      "shape-class": "org.xmind.topicShape.roundedRect"
    }
  },
  "map": {
    "id": "uuid", "properties": {
      "svg:fill": "#ffffff",
      "multi-line-colors": "#F9423A #F6A04D #F3D321 #00BC7B #486AFF #4D49BE",
      "color-list": "#000229 #1F2766 #52CC83 #4D86DB #99142F #245570"
    }
  },
  "skeletonThemeId": "c1fbada1b45ba2e3bfc3b8b57b",
  "colorThemeId": "Rainbow-#000229-MULTI_LINE_COLORS"
}
```

#### 2.3.5 metadata.json

```json
{
  "dataStructureVersion": "3",
  "creator": {"name": "AI Enhanced Notes", "version": "26.02.04171"},
  "layoutEngineVersion": "5"
}
```

#### 2.3.6 manifest.json

```json
{"file-entries": {"content.json": {}, "metadata.json": {}}}
```

### 2.4 内容组织策略

#### 策略 A：按学习路径递进式（推荐）

当笔记按学习顺序（day01→day02...）组织时，按阶段排列主分支：

```
[主题]
  ├── 第一阶段：[基础概述]
  ├── 第二阶段：[算法1]
  ├── 第三阶段：[算法2]
  ├── ...
  └── 通用工具与核心概念
```

#### 策略 B：按知识体系分类式

当笔记按知识类别组织时，按模块排列主分支：

```
[主题]
  ├── [模块1：基础概念]
  ├── [模块2：核心算法]
  ├── [模块3：进阶主题]
  └── [模块4：工具与评估]
```

**选择原则**：询问用户偏好，若用户无明确要求，默认使用策略 A（学习路径递进式）。

### 2.5 生成脚本模板

AI 应使用以下 Python 脚本模板生成 XMind 文件：

```python
import json, zipfile, uuid, os

def uid():
    return str(uuid.uuid4())

def t(title, children=None):
    topic = {"id": uid(), "title": title}
    if children:
        topic["children"] = {"attached": children}
        topic["branch"] = "folded"
    return topic

# 构建节点树...
# 组装 content_json...
# 写入 ZIP...
```

**关键注意点**：
1. 生成前若目标文件已存在，必须先 `os.remove()` 删除，避免 ZIP 中残留旧文件
2. ZIP 中不要包含 `META-INF/` 目录
3. `manifest.json` 必须在 ZIP 根目录，且为 JSON 格式
4. 主题每个层级的 id 都必须唯一

---

## 三、两种格式的关系

| 维度 | 知识地图（Markdown） | 思维导图（XMind） |
|------|---------------------|------------------|
| 用途 | 快速检索、文字复习 | 可视化结构、整体认知 |
| 内容粒度 | 一句话定义 + 链接 | 原子化短节点 |
| 更新频率 | 随笔记增量更新 | 阶段性重构 |
| 用户场景 | Obsidian 中浏览 | XMind 软件中查看 |

**生成顺序**：必须先完成 Markdown 增强版 → 再生成知识地图 → 最后生成思维导图。思维导图的内容应基于知识地图的聚合结构，但节点粒度更细。

---

## 四、常见错误与规避

| 错误 | 原因 | 正确做法 |
|------|------|---------|
| XMind "not a valid file" | manifest.xml 放在 META-INF/ 下 | manifest.json 放在 ZIP 根目录 |
| 子节点颜色不生效 | 给子节点加了 "class": "topic" | 只有 rootTopic 加 class，子节点不加 |
| 描述内容不显示 | 用 notes 字段存储描述 | 描述直接作为子节点展示 |
| 标题过长导致重叠 | 一个节点塞了长段落 | 拆分为 5-15 字的原子节点 |
| 旧文件残留 | xmind.load() 会追加到现有 ZIP | 生成前删除旧文件 |
