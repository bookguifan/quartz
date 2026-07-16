# Quartz v5 Code Wiki

## 目录

1. [项目概述](#项目概述)
2. [整体架构](#整体架构)
3. [目录结构](#目录结构)
4. [主要模块职责](#主要模块职责)
5. [关键类与函数](#关键类与函数)
6. [依赖关系图](#依赖关系图)
7. [项目运行方式](#项目运行方式)
8. [配置系统](#配置系统)
9. [插件系统](#插件系统)
10. [构建流程](#构建流程)
11. [组件系统](#组件系统)

---

## 项目概述

### 项目简介

**Quartz** 是一个数字花园（Digital Garden）静态网站生成器，用于将 Markdown 笔记和知识库发布为现代化的网站。它是一个基于 Node.js 和 TypeScript 的 SSG（Static Site Generator），特别优化了对 Obsidian 笔记格式的支持。

- **版本**: v5.0.0
- **许可证**: MIT
- **作者**: jackyzha0
- **主页**: https://quartz.jzhao.xyz

### 核心特性

- 📝 **Markdown 驱动**: 基于 remark/rehype 生态的强大 Markdown 处理
- 🌱 **数字花园**: 支持双向链接、反向链接、知识图谱
- 🔌 **插件系统**: 高度可扩展的插件架构（Transformer / Filter / Emitter / PageType）
- 🎨 **组件化**: 基于 Preact 的组件系统，支持自定义布局
- 🌍 **国际化**: 支持 25+ 种语言
- ⚡ **性能优化**: 多线程构建、增量构建、SPA 路由
- 📱 **响应式**: 移动端友好的设计
- 🔐 **加密页面**: 支持加密内容保护
- 🧩 **社区插件**: 丰富的社区插件生态系统

---

## 整体架构

Quartz v5 采用**流水线架构**，核心构建过程分为三个主要阶段：

```
Markdown 文件 → 解析(Parse) → 过滤(Filter) → 发射(Emit) → 静态网站
```

### 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                     CLI 层 (cli/)                       │
│  create / build / upgrade / sync / restore / plugin     │
├─────────────────────────────────────────────────────────┤
│                   配置加载层 (loader/)                   │
│     config-loader / plugin-loader / git-loader         │
├─────────────────────────────────────────────────────────┤
│                    插件系统层 (plugins/)                  │
│  Transformers │ Filters │ Emitters │ PageTypes          │
├─────────────────────────────────────────────────────────┤
│                   处理器层 (processors/)                  │
│         parse.ts │ filter.ts │ emit.ts                  │
├─────────────────────────────────────────────────────────┤
│                    组件层 (components/)                   │
│   Frames │ Pages │ Body │ Head │ Sidebar components     │
├─────────────────────────────────────────────────────────┤
│                     工具层 (util/)                       │
│  path / ctx / log / perf / resources / theme / slug    │
└─────────────────────────────────────────────────────────┘
```

### 数据流

1. **输入**: Markdown 文件 + YAML 配置
2. **配置加载**: 读取 `quartz.config.yaml`，安装并实例化插件
3. **解析阶段**: Markdown → MDAST → HAST（HTML AST）
4. **过滤阶段**: 根据规则决定哪些页面发布
5. **发射阶段**: 生成 HTML 页面、静态资源、索引文件
6. **输出**: 完整的静态网站

---

## 目录结构

```
my-digital-garden/
├── docs/                          # 文档目录（Quartz文档站的内容源）
│   ├── advanced/                  # 高级主题文档
│   ├── cli/                       # CLI 命令文档
│   ├── features/                  # 功能特性文档
│   ├── getting-started/           # 入门指南
│   ├── plugins/                   # 插件文档
│   └── tags/                      # 标签分类文档
│
├── quartz/                        # Quartz 核心源码
│   ├── cli/                       # 命令行工具
│   │   ├── templates/             # 配置模板
│   │   │   ├── default.yaml
│   │   │   ├── obsidian.yaml
│   │   │   ├── blog.yaml
│   │   │   └── ttrpg.yaml
│   │   ├── args.js                # CLI 参数定义
│   │   ├── handlers.js            # 命令处理函数
│   │   ├── helpers.js             # CLI 辅助函数
│   │   ├── constants.js           # 常量定义
│   │   ├── plugin-data.js         # 插件数据管理
│   │   └── plugin-git-handlers.js # 插件Git操作
│   │
│   ├── components/                # UI 组件系统
│   │   ├── frames/                # 页面框架（布局模板）
│   │   │   ├── DefaultFrame.tsx   # 默认框架
│   │   │   ├── FullWidthFrame.tsx # 全宽框架
│   │   │   ├── MinimalFrame.tsx   # 极简框架
│   │   │   ├── registry.ts        # 框架注册表
│   │   │   └── types.ts           # 框架类型
│   │   ├── pages/                 # 特殊页面组件
│   │   │   └── 404.tsx            # 404页面
│   │   ├── scripts/               # 前端脚本
│   │   │   ├── popover.inline.ts  # 悬停预览
│   │   │   ├── spa.inline.ts      # SPA路由
│   │   │   └── util.ts            # 工具函数
│   │   ├── styles/                # 组件样式
│   │   ├── Body.tsx               # 页面主体
│   │   ├── Head.tsx               # 页面头部
│   │   ├── Header.tsx             # 页眉
│   │   ├── renderPage.tsx         # 页面渲染核心
│   │   ├── registry.ts            # 组件注册表
│   │   └── types.ts               # 组件类型定义
│   │
│   ├── i18n/                      # 国际化
│   │   ├── locales/               # 语言包（25+种语言）
│   │   └── index.ts               # i18n 入口
│   │
│   ├── plugins/                   # 插件系统
│   │   ├── emitters/              # 内置发射器插件
│   │   │   ├── assets.ts          # 资源发射
│   │   │   ├── static.ts          # 静态文件
│   │   │   ├── componentResources.ts # 组件资源
│   │   │   └── helpers.ts         # 发射器辅助
│   │   ├── filters/               # 过滤器插件
│   │   ├── loader/                # 插件加载器
│   │   │   ├── config-loader.ts   # 配置加载器
│   │   │   ├── gitLoader.ts       # Git插件加载
│   │   │   ├── componentLoader.ts # 组件加载器
│   │   │   ├── frameLoader.ts     # 框架加载器
│   │   │   ├── conditions.ts      # 渲染条件
│   │   │   └── types.ts           # 加载器类型
│   │   ├── pageTypes/             # 页面类型插件
│   │   │   ├── dispatcher.ts      # 页面类型调度器
│   │   │   ├── 404.ts             # 404页面类型
│   │   │   └── matchers.ts        # 页面匹配器
│   │   ├── transformers/          # 转换器插件
│   │   ├── config.ts              # 插件配置
│   │   ├── types.ts               # 插件类型定义
│   │   ├── vfile.ts               # 虚拟文件类型
│   │   └── index.ts               # 插件入口
│   │
│   ├── processors/                # 构建处理器
│   │   ├── parse.ts               # Markdown解析
│   │   ├── filter.ts              # 内容过滤
│   │   └── emit.ts                # 内容发射
│   │
│   ├── static/                    # 静态资源
│   │   ├── giscus/                # 评论系统样式
│   │   ├── icon.png               # 网站图标
│   │   └── og-image.png           # 社交分享图片
│   │
│   ├── styles/                    # 全局样式
│   │   ├── base.scss              # 基础样式
│   │   ├── variables.scss         # CSS变量
│   │   ├── callouts.scss          # 提示框样式
│   │   ├── syntax.scss            # 代码高亮
│   │   └── custom.scss            # 自定义样式
│   │
│   ├── util/                      # 工具函数
│   │   ├── path.ts                # 路径处理
│   │   ├── ctx.ts                 # 构建上下文
│   │   ├── log.ts                 # 日志工具
│   │   ├── perf.ts                # 性能计时
│   │   ├── resources.tsx          # 资源管理
│   │   ├── theme.ts               # 主题工具
│   │   ├── fileTrie.ts            # 文件前缀树
│   │   ├── glob.ts                # 文件匹配
│   │   ├── slugCollisions.ts      # Slug冲突检测
│   │   ├── clone.ts               # 深拷贝
│   │   ├── escape.ts              # 转义工具
│   │   ├── emoji.ts               # 表情符号
│   │   ├── jsx.tsx                # JSX工具
│   │   ├── lang.ts                # 语言工具
│   │   ├── random.ts              # 随机数
│   │   ├── sourcemap.ts           # Source Map
│   │   └── trace.ts               # 错误追踪
│   │
│   ├── bootstrap-cli.mjs          # CLI启动入口
│   ├── bootstrap-worker.mjs       # Worker启动入口
│   ├── build.ts                   # 构建主流程
│   ├── cfg.ts                     # 配置类型
│   └── worker.ts                  # Worker线程
│
├── quartz.config.yaml             # 主配置文件
├── quartz.config.default.yaml     # 默认配置
├── quartz.ts                      # 配置入口（旧式）
├── quartz.lock.json               # 插件锁文件
├── package.json                   # 项目依赖
├── tsconfig.json                  # TypeScript配置
├── Dockerfile                     # Docker配置
├── README.md                      # 项目说明
└── CODE_WIKI.md                   # 本文档
```

---

## 主要模块职责

### 1. CLI 模块 (`quartz/cli/`)

**职责**: 提供命令行用户界面，处理用户输入，协调构建流程。

| 文件 | 职责 |
|------|------|
| [handlers.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/handlers.js) | 核心命令处理函数：`handleCreate`, `handleBuild`, `handleUpgrade`, `handleSync`, `handleRestore` |
| [args.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/args.js) | CLI 参数定义和解析（基于 yargs） |
| [helpers.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/helpers.js) | CLI 辅助函数：Git操作、文件操作、符号链接等 |
| [constants.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/constants.js) | 常量定义：版本号、路径、远程仓库配置等 |
| [plugin-data.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/plugin-data.js) | 插件数据读写管理 |
| [plugin-git-handlers.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/plugin-git-handlers.js) | 插件的Git安装、更新、恢复操作 |

### 2. 插件加载器 (`quartz/plugins/loader/`)

**职责**: 加载配置、安装插件、实例化插件、构建布局系统。

| 文件 | 职责 |
|------|------|
| [config-loader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/config-loader.ts) | 核心配置加载器，负责读取YAML配置、验证依赖、分类和实例化插件 |
| [gitLoader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/gitLoader.ts) | 从Git仓库加载社区插件，管理插件安装 |
| [componentLoader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/componentLoader.ts) | 从插件包中加载组件到组件注册表 |
| [frameLoader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/frameLoader.ts) | 从插件包中加载页面框架 |
| [conditions.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/conditions.ts) | 组件渲染条件判断（如 `not-index`） |
| [types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/types.ts) | 加载器相关类型定义 |

### 3. 处理器模块 (`quartz/processors/`)

**职责**: 实现构建流水线的三个核心阶段。

| 文件 | 职责 |
|------|------|
| [parse.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/parse.ts) | Markdown解析：Text → MDAST → HAST，支持多线程Worker |
| [filter.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/filter.ts) | 内容过滤：应用所有Filter插件决定哪些页面发布 |
| [emit.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/emit.ts) | 内容发射：按阶段运行Emitter插件生成输出文件 |

### 4. 组件系统 (`quartz/components/`)

**职责**: 基于 Preact 的 UI 组件系统，负责页面渲染。

| 文件/目录 | 职责 |
|-----------|------|
| [renderPage.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/renderPage.tsx) | 页面渲染核心：处理Transclude、组装布局、渲染HTML |
| [types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/types.ts) | 组件类型定义：`QuartzComponent`, `QuartzComponentProps` |
| [registry.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/registry.ts) | 组件注册表：管理组件注册、实例化、选项覆盖 |
| [frames/](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/frames/) | 页面框架：定义不同的页面布局模板 |
| [Body.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/Body.tsx) | 页面主体组件 |
| [Head.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/Head.tsx) | HTML头部组件 |
| [scripts/](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/scripts/) | 前端交互脚本（SPA、Popover等） |

### 5. 工具模块 (`quartz/util/`)

**职责**: 提供通用工具函数供各模块使用。

| 文件 | 职责 |
|------|------|
| [path.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/path.ts) | 路径处理：Slug生成、URL解析、相对路径计算 |
| [ctx.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/ctx.ts) | 构建上下文：`BuildCtx` 定义，贯穿整个构建流程 |
| [log.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/log.ts) | 日志工具：进度条、格式化输出 |
| [perf.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/perf.ts) | 性能计时：`PerfTimer` 类 |
| [resources.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/resources.tsx) | 资源管理：CSS/JS资源收集和处理 |
| [fileTrie.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/fileTrie.ts) | 文件前缀树：高效的文件层级结构表示 |
| [slugCollisions.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/slugCollisions.ts) | Slug冲突检测和警告 |
| [theme.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/theme.ts) | 主题配置类型和工具 |

---

## 关键类与函数

### 核心类型定义

#### 1. `BuildCtx` - 构建上下文

**位置**: [quartz/util/ctx.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/ctx.ts#L31-L47)

构建上下文是贯穿整个构建流程的核心数据结构，包含构建所需的所有状态。

```typescript
interface BuildCtx {
  buildId: string                    // 构建唯一标识
  argv: Argv                         // CLI参数
  cfg: QuartzConfig                  // 完整配置（全局配置+插件）
  allSlugs: FullSlug[]               // 所有页面Slug
  allFiles: FilePath[]               // 所有文件路径
  trie?: FileTrieNode<BuildTimeTrieData>  // 文件前缀树
  incremental: boolean               // 是否增量构建
  virtualPages: ProcessedContent[]   // 虚拟页面（标签页、文件夹页等）
  hashedResourceNames?: HashedResourceNames  // 内容哈希资源名
  componentCssMap?: Map<string, string>     // 组件CSS映射
  extractedInlineResources?: Map<string, string>  // 提取的内联资源
}
```

**关键作用**:
- 在解析、过滤、发射各阶段之间传递状态
- 存储全局配置和所有文件元数据
- 支持增量构建的状态管理

---

#### 2. `QuartzConfig` - Quartz配置

**位置**: [quartz/cfg.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cfg.ts#L86-L90)

```typescript
interface QuartzConfig {
  configuration: GlobalConfiguration  // 全局配置
  plugins: PluginTypes                // 插件实例集合
  externalPlugins?: PluginSpecifier[] // 外部插件说明
}
```

---

#### 3. `GlobalConfiguration` - 全局配置

**位置**: [quartz/cfg.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cfg.ts#L59-L84)

```typescript
interface GlobalConfiguration {
  pageTitle: string           // 页面标题
  pageTitleSuffix?: string    // 标题后缀
  enableSPA: boolean          // 启用SPA路由
  enablePopovers: boolean     // 启用悬停预览
  analytics: Analytics        // 分析配置
  ignorePatterns: string[]    // 忽略模式
  baseUrl?: string            // 基础URL
  theme: Theme                // 主题配置
  locale: ValidLocale         // 语言设置
}
```

---

### 插件类型体系

#### 1. `QuartzTransformerPlugin` - 转换器插件

**位置**: [quartz/plugins/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/types.ts#L24-L33)

在解析阶段运行，处理 Markdown 文本和 AST。

```typescript
type QuartzTransformerPlugin<Options> = (opts?: Options) => {
  name: string
  textTransform?: (ctx: BuildCtx, src: string) => string  // 文本级转换
  markdownPlugins?: (ctx: BuildCtx) => PluggableList      // MDAST插件
  htmlPlugins?: (ctx: BuildCtx) => PluggableList          // HAST插件
  externalResources?: ExternalResourcesFn                 // 外部资源
}
```

---

#### 2. `QuartzFilterPlugin` - 过滤器插件

**位置**: [quartz/plugins/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/types.ts#L35-L41)

在过滤阶段运行，决定哪些页面应该发布。

```typescript
type QuartzFilterPlugin<Options> = (opts?: Options) => {
  name: string
  shouldPublish(ctx: BuildCtx, content: ProcessedContent): boolean
}
```

---

#### 3. `QuartzEmitterPlugin` - 发射器插件

**位置**: [quartz/plugins/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/types.ts#L49-L72)

在发射阶段运行，生成输出文件。

```typescript
type QuartzEmitterPlugin<Options> = (opts?: Options) => {
  name: string
  // 完整构建时调用
  emit: (ctx, content, resources) => Promise<FilePath[]> | AsyncGenerator<FilePath>
  // 增量构建时调用（可选）
  partialEmit?: (ctx, content, resources, changeEvents) => Promise<FilePath[]> | AsyncGenerator<FilePath> | null
  // 获取使用的组件
  getQuartzComponents?: (ctx: BuildCtx) => QuartzComponent[]
  externalResources?: ExternalResourcesFn
}
```

---

#### 4. `QuartzPageTypePlugin` - 页面类型插件

**位置**: [quartz/plugins/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/types.ts#L105-L121)

定义不同类型的页面及其渲染方式。

```typescript
type QuartzPageTypePlugin<Options> = (opts?: Options) => {
  name: string
  priority?: number              // 匹配优先级
  fileExtensions?: string[]      // 支持的文件扩展名
  match: PageMatcher             // 匹配函数
  generate?: PageGenerator       // 生成虚拟页面
  layout: string                 // 布局名称
  frame?: string                 // 页面框架
  body: QuartzComponentConstructor  // 页面主体组件
  treeTransforms?: (ctx) => TreeTransform[]  // HAST树转换
}
```

---

### 核心函数

#### 1. `buildQuartz()` - 构建主函数

**位置**: [quartz/build.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/build.ts#L52-L107)

Quartz 构建的主入口函数，协调整个构建流程。

```typescript
async function buildQuartz(argv: Argv, mut: Mutex, clientRefresh: () => void)
```

**执行流程**:
1. 初始化构建上下文 `BuildCtx`
2. 清理输出目录
3. 扫描所有 Markdown 文件
4. 调用 `parseMarkdown()` 解析文件
5. 检测 Slug 冲突
6. 调用 `filterContent()` 过滤内容
7. 调用 `emitContent()` 发射内容
8. 如果启用 watch 模式，启动文件监视器

---

#### 2. `parseMarkdown()` - Markdown解析

**位置**: [quartz/processors/parse.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/parse.ts#L148-L221)

将 Markdown 文件解析为 HTML AST（HAST）。

```typescript
async function parseMarkdown(ctx: BuildCtx, fps: FilePath[]): Promise<ProcessedContent[]>
```

**两阶段解析**:
1. **Text → MDAST**: 使用 `remark-parse` 解析 Markdown 文本为 Markdown AST
2. **MDAST → HAST**: 使用 `remark-rehype` 转换为 HTML AST

**多线程优化**:
- 文件数 > 128 时自动启用多线程
- 使用 `workerpool` 创建 Worker 线程池
- 分块（每块128个文件）并行处理

---

#### 3. `filterContent()` - 内容过滤

**位置**: [quartz/processors/filter.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/filter.ts#L5-L24)

依次应用所有过滤器插件，筛选出需要发布的内容。

```typescript
function filterContent(ctx: BuildCtx, content: ProcessedContent[]): ProcessedContent[]
```

---

#### 4. `emitContent()` - 内容发射

**位置**: [quartz/processors/emit.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/emit.ts#L48-L100)

按阶段运行发射器插件，生成最终输出文件。

```typescript
async function emitContent(ctx: BuildCtx, content: ProcessedContent[])
```

**三阶段发射**:
1. **Phase 0 - ComponentResources**: 先处理组件资源，生成内容哈希文件名
2. **Phase 1 - PageTypeDispatcher**: 运行页面类型调度器，生成虚拟页面
3. **Phase 2 - 其他Emitters**: 运行所有其他发射器，包含虚拟页面数据

---

#### 5. `renderPage()` - 页面渲染

**位置**: [quartz/components/renderPage.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/renderPage.tsx#L300-L376)

将 HAST 树和组件渲染为完整的 HTML 字符串。

```typescript
function renderPage(
  cfg: GlobalConfiguration,
  slug: FullSlug,
  componentData: QuartzComponentProps,
  components: RenderComponents,
  pageResources: StaticResources,
  treeTransforms?: TreeTransform[],
): string
```

**关键步骤**:
1. 深拷贝 HAST 树（避免修改缓存数据）
2. 处理 Transclude（嵌入内容），支持循环检测
3. 应用插件提供的树转换
4. 组装页面布局（Head / Header / Left / Body / Right / Footer）
5. 使用 Preact SSR 渲染为 HTML 字符串

---

#### 6. `loadQuartzConfig()` - 加载配置

**位置**: [quartz/plugins/loader/config-loader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/config-loader.ts#L238-L504)

从 YAML 配置文件加载并实例化所有插件。

```typescript
export async function loadQuartzConfig(
  configOverrides?: Partial<GlobalConfiguration>,
): Promise<QuartzConfig>
```

**核心流程**:
1. 读取 `quartz.config.yaml`
2. 安装所有启用的插件（从 Git 拉取）
3. 收集插件原生依赖并安装
4. 验证插件依赖关系（检查循环依赖、顺序依赖）
5. 按类别分类插件（Transformer / Filter / Emitter / PageType）
6. 按 order 字段排序插件
7. 实例化所有插件
8. 构建页面布局
9. 返回完整的 `QuartzConfig`

---

#### 7. `PageTypeDispatcher.emit()` - 页面类型调度器

**位置**: [quartz/plugins/pageTypes/dispatcher.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/pageTypes/dispatcher.ts#L160-L246)

核心的页面发射器，负责将内容分配给对应的页面类型并渲染。

```typescript
async *emit(ctx, content, resources)
```

**三阶段发射**:
1. **生成虚拟页面**: 调用所有 PageType 插件的 `generate()` 方法
2. **发射普通页面**: 遍历所有内容，找到匹配的页面类型并渲染
3. **发射虚拟页面**: 渲染所有生成的虚拟页面（标签页、文件夹页等）

---

### 组件类型

#### `QuartzComponent` - Quartz组件

**位置**: [quartz/components/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/types.ts#L21-L26)

```typescript
type QuartzComponent = ((props: QuartzComponentProps) => any) & {
  displayName?: string
  css?: StringResource           // 组件CSS
  beforeDOMLoaded?: StringResource  // DOM加载前执行的脚本
  afterDOMLoaded?: StringResource   // DOM加载后执行的脚本
}
```

#### `QuartzComponentProps` - 组件属性

**位置**: [quartz/components/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/types.ts#L8-L19)

```typescript
type QuartzComponentProps = {
  ctx: BuildCtx                  // 构建上下文
  externalResources: StaticResources  // 外部资源
  fileData: QuartzPluginData     // 当前文件数据
  cfg: GlobalConfiguration       // 全局配置
  children: (QuartzComponent | JSX.Element)[]  // 子组件
  tree: Node                     // HAST树
  allFiles: QuartzPluginData[]   // 所有文件数据
  displayClass?: "mobile-only" | "desktop-only"  // 显示类
}
```

---

## 依赖关系图

### 核心模块依赖

```
build.ts (主构建入口)
  ├── processors/parse.ts      (Markdown解析)
  │   ├── unified / remark-parse / remark-rehype
  │   ├── workerpool            (多线程)
  │   └── plugins/types.ts
  ├── processors/filter.ts     (内容过滤)
  │   └── plugins/types.ts
  └── processors/emit.ts       (内容发射)
      ├── plugins/index.ts
      ├── components/renderPage.tsx
      │   ├── preact / preact-render-to-string
      │   ├── components/Body.tsx
      │   ├── components/Head.tsx
      │   └── components/frames/
      └── plugins/emitters/
          ├── assets.ts
          ├── static.ts
          └── componentResources.ts

plugins/loader/config-loader.ts (配置加载)
  ├── plugins/loader/gitLoader.ts      (Git插件加载)
  ├── plugins/loader/componentLoader.ts (组件加载)
  ├── plugins/loader/frameLoader.ts    (框架加载)
  ├── components/registry.ts           (组件注册表)
  └── yaml                             (YAML解析)

components/ (组件系统)
  ├── preact                          (UI框架)
  ├── components/frames/              (页面框架)
  ├── components/scripts/             (前端脚本)
  └── util/resources.tsx              (资源管理)

util/ (工具层)
  ├── path.ts                         (路径处理)
  ├── ctx.ts                          (构建上下文)
  ├── log.ts                          (日志)
  ├── perf.ts                         (性能计时)
  └── fileTrie.ts                     (文件树)
```

### 插件依赖链

```
配置文件 (quartz.config.yaml)
  ↓
config-loader.ts
  ├─ 安装插件 (gitLoader)
  ├─ 验证依赖 (validateDependencies)
  ├─ 分类插件
  │   ├─ Transformers (按order排序)
  │   ├─ Filters (按order排序)
  │   ├─ Emitters (按order排序)
  │   └─ PageTypes (按priority排序)
  ├─ 实例化插件
  └─ 构建布局
      ├─ 默认布局 (所有带layout的组件)
      └─ 按页面类型布局 (byPageType)
```

### 构建数据流

```
输入: .md 文件
  ↓
parseMarkdown()
  ├─ textTransform (文本级转换)
  ├─ remark-parse → MDAST
  ├─ markdownPlugins (MDAST转换)
  ├─ remark-rehype → HAST
  └─ htmlPlugins (HAST转换)
  ↓
输出: ProcessedContent [HAST, VFile]
  ↓
filterContent()
  ├─ Filter 1
  ├─ Filter 2
  └─ Filter N
  ↓
输出: 过滤后的 ProcessedContent[]
  ↓
emitContent()
  ├─ Phase 0: ComponentResources (生成资源哈希)
  ├─ Phase 1: PageTypeDispatcher (生成虚拟页面+渲染)
  │   ├─ generate() → virtualPages
  │   ├─ 匹配页面类型
  │   └─ renderPage() → HTML
  └─ Phase 2: 其他Emitters
      ├─ ContentIndex (sitemap/RSS/search index)
      ├─ Assets
      └─ ...
  ↓
输出: 静态网站文件
```

---

## 项目运行方式

### 环境要求

- **Node.js**: >= 22
- **npm**: >= 10.9.2
- **Git**: 用于安装社区插件

### 安装依赖

```bash
npm install
```

### 可用脚本

| 命令 | 说明 |
|------|------|
| `npm run quartz` | 运行 Quartz CLI |
| `npm run docs` | 构建并启动文档站（开发模式） |
| `npm run check` | 类型检查 + Prettier 检查 |
| `npm run format` | Prettier 格式化代码 |
| `npm run test` | 运行测试 |
| `npm run profile` | 性能分析 |
| `npm run install-plugins` | 安装配置中的插件 |

### 核心 CLI 命令

#### 1. 创建新项目

```bash
npx quartz create
```

交互式创建新的 Quartz 项目，支持：
- 选择模板（default / obsidian / ttrpg / blog）
- 选择内容来源（新建 / 复制 / 符号链接）
- 配置链接解析方式
- 设置基础 URL

#### 2. 构建网站

```bash
# 基本构建
npx quartz build

# 开发模式（文件监听 + 本地服务器）
npx quartz build --serve

# 指定内容目录
npx quartz build -d ./content

# 指定输出目录
npx quartz build -o ./public

# 启用详细日志
npx quartz build --verbose

# 并发线程数
npx quartz build --concurrency 4
```

**常用参数**:
- `--serve`: 启动本地开发服务器
- `--watch`: 监听文件变化自动重建
- `--port <port>`: 服务器端口（默认 8080）
- `--wsPort <port>`: WebSocket 端口（默认 3001）
- `-d, --directory <dir>`: 内容目录
- `-o, --output <dir>`: 输出目录
- `-v, --verbose`: 详细输出

#### 3. 升级 Quartz

```bash
npx quartz upgrade
```

从上游仓库拉取最新版本，自动处理冲突和依赖更新。

#### 4. 同步内容

```bash
# 完整同步（pull + commit + push）
npx quartz sync

# 只提交
npx quartz sync --commit

# 只推送
npx quartz sync --push

# 只拉取
npx quartz sync --pull

# 自定义提交信息
npx quartz sync --commit -m "my message"
```

#### 5. 插件管理

```bash
# 安装插件
npx quartz plugin add <plugin-source>

# 移除插件
npx quartz plugin remove <plugin-name>

# 列出已安装插件
npx quartz plugin list

# 恢复插件（从lockfile）
npx quartz plugin restore

# 检查插件兼容性
npx quartz plugin check
```

#### 6. 恢复内容

```bash
npx quartz restore
```

从 Git 暂存区恢复内容文件夹。

### Docker 运行

项目提供了 Dockerfile 支持容器化运行：

```bash
# 构建镜像
docker build -t quartz .

# 运行容器（开发模式）
docker run -p 8080:8080 -v $(pwd):/usr/src/app quartz
```

---

## 配置系统

### 配置文件位置

主配置文件: `quartz.config.yaml`

默认配置: `quartz.config.default.yaml`

### 配置结构

```yaml
# 全局配置
configuration:
  pageTitle: "Quartz 5"           # 网站标题
  enableSPA: true                  # 启用SPA
  enablePopovers: true             # 启用悬停预览
  analytics:                       # 分析配置
    provider: plausible
  locale: en-US                    # 语言
  baseUrl: example.com             # 基础URL
  ignorePatterns:                  # 忽略模式
    - private
    - templates
    - .obsidian
  theme:                           # 主题配置
    fontOrigin: googleFonts
    typography:
      header: "Schibsted Grotesk"
      body: "Source Sans Pro"
      code: "IBM Plex Mono"
    colors:
      lightMode: { ... }
      darkMode: { ... }

# 插件配置
plugins:
  - source: github:quartz-community/created-modified-date
    enabled: true
    options: { ... }
    order: 10
    layout:                        # 组件布局配置
      position: right              # 位置: left / right / beforeBody / afterBody
      priority: 30                 # 优先级（越小越靠前）
      group: toolbar               # 分组名
      display: all                 # 显示: all / mobile-only / desktop-only
      condition: not-index         # 渲染条件

# 布局配置
layout:
  groups:                          # 分组配置
    toolbar:
      priority: 35
      direction: row
      gap: 0.5rem
  byPageType:                      # 按页面类型的布局覆盖
    "404": { ... }
    folder:
      exclude:
        - reader-mode
    tag:
      exclude:
        - reader-mode
```

### 插件源格式

支持多种插件源格式：

```yaml
# GitHub 简写
source: github:quartz-community/plugin-name

# 带版本号
source: github:quartz-community/plugin-name#v1.0.0

# 子目录
source: github:owner/repo#main:subdir/path

# 完整 Git URL
source: git+https://github.com/owner/repo.git

# 本地路径
source: ./my-local-plugin
```

### 布局位置

组件可以放置在以下位置：

| 位置 | 说明 |
|------|------|
| `head` | HTML `<head>` 内 |
| `header` | 页面顶部页眉 |
| `beforeBody` | 正文内容之前 |
| `left` | 左侧边栏 |
| `right` | 右侧边栏 |
| `afterBody` | 正文内容之后 |
| `footer` | 页面底部 |

---

## 插件系统

### 插件分类

Quartz 有四种类型的插件，在构建流水线的不同阶段运行：

#### 1. Transformers（转换器）

**运行阶段**: 解析阶段 (Parse)

**作用**: 转换 Markdown 内容和 AST

**可介入点**:
- `textTransform`: 原始文本转换（在解析之前）
- `markdownPlugins`: remark 插件，操作 MDAST
- `htmlPlugins`: rehype 插件，操作 HAST
- `externalResources`: 声明需要的外部资源

**常见转换器插件**:
- Obsidian Flavored Markdown
- GitHub Flavored Markdown
- Syntax Highlighting
- Table of Contents
- LaTeX
- Citations
- Crawl Links
- Hard Line Breaks

#### 2. Filters（过滤器）

**运行阶段**: 过滤阶段 (Filter)

**作用**: 决定哪些页面应该被发布

**核心方法**:
- `shouldPublish(ctx, content): boolean` - 返回 true 表示发布

**常见过滤器插件**:
- Remove Drafts（移除草稿）
- Explicit Publish（显式发布）
- Unlisted Pages（隐藏页面）
- Encrypted Pages（加密页面）

#### 3. Emitters（发射器）

**运行阶段**: 发射阶段 (Emit)

**作用**: 生成输出文件

**核心方法**:
- `emit(ctx, content, resources)` - 完整构建
- `partialEmit(ctx, content, resources, changeEvents)` - 增量构建（可选）

**内置发射器**:
- `ComponentResources` - 组件资源（CSS/JS打包）
- `Assets` - 资源文件复制
- `Static` - 静态文件复制
- `PageTypeDispatcher` - 页面类型调度器（核心）

**社区发射器插件**:
- ContentIndex（搜索索引 / Sitemap / RSS）
- Favicon
- CNAME
- Alias Redirects
- Custom OG Images

#### 4. PageTypes（页面类型）

**运行阶段**: 发射阶段（由 PageTypeDispatcher 调用）

**作用**: 定义不同类型页面的渲染方式，可生成虚拟页面

**核心方法**:
- `match({ slug, fileData, cfg })` - 匹配页面类型
- `generate({ content, cfg, ctx })` - 生成虚拟页面（可选）
- `body` - 页面主体组件构造器
- `treeTransforms` - HAST 树转换（可选）

**常见页面类型插件**:
- ContentPage（普通 Markdown 页面）
- FolderPage（文件夹索引页）
- TagPage（标签索引页）
- CanvasPage（Obsidian Canvas）
- BasesPage（数据库视图）
- NotFoundPage（404页面）

### 插件加载流程

```
1. 读取 quartz.config.yaml
   ↓
2. 遍历所有 enabled: true 的插件
   ↓
3. 解析插件源 (parsePluginSource)
   ↓
4. 安装插件 (installPlugin)
   - 检查本地缓存
   - 从 Git 克隆/拉取
   - 安装原生依赖
   ↓
5. 收集插件清单 (manifest)
   ↓
6. 验证依赖关系
   - 检查缺失依赖
   - 检查顺序依赖
   - 检测循环依赖
   ↓
7. 按 category 分类插件
   ↓
8. 按 order / priority 排序
   ↓
9. 实例化插件
   - 合并 defaultOptions + entry.options + 注册覆盖
   - 调用工厂函数
   ↓
10. 加载组件/框架
    - 从 plugin.components 注册组件
    - 从 plugin.frames 注册框架
    ↓
11. 构建页面布局
    - 收集所有带 layout 的组件
    - 按 position 分组
    - 按 priority 排序
    - 解析 flex group
    ↓
12. 返回 QuartzConfig
```

### 插件依赖验证

`validateDependencies()` 函数检查：

1. **缺失依赖**: 插件 A 依赖 B，但 B 未安装 → Error
2. **禁用依赖**: 插件 A 依赖 B，但 B 被禁用 → Warning
3. **顺序错误**: 插件 A 依赖 B，但 A 的 order 小于 B → Error
4. **循环依赖**: A→B→C→A → Error

---

## 构建流程

### 完整构建流程

```
npx quartz build
  ↓
handleBuild() [CLI层]
  ├─ 使用 esbuild 转译 build.ts
  ├─ 创建构建互斥锁
  └─ 调用 buildQuartz()
      ↓
buildQuartz() [build.ts]
  ├─ 初始化 BuildCtx
  ├─ 清理输出目录 (rm -rf output)
  ├─ 扫描文件 (glob **/*.* + ignorePatterns)
  ├─ 筛选 .md 文件
  │
  ├─ [Phase 1] parseMarkdown()
  │   ├─ 多线程？→ 使用 WorkerPool
  │   ├─ 创建 MdProcessor (remark-parse + transformers.markdownPlugins)
  │   ├─ 创建 HtmlProcessor (remark-rehype + transformers.htmlPlugins)
  │   ├─ 对每个文件：
  │   │   ├─ 读取文件
  │   │   ├─ textTransform 转换
  │   │   ├─ remark-parse → MDAST
  │   │   ├─ 运行 markdownPlugins
  │   │   ├─ remark-rehype → HAST
  │   │   └─ 运行 htmlPlugins
  │   └─ 返回 ProcessedContent[]
  │
  ├─ 检测 Slug 冲突
  │
  ├─ [Phase 2] filterContent()
  │   └─ 依次应用所有 filter.shouldPublish()
  │
  └─ [Phase 3] emitContent()
      ├─ Phase 0: ComponentResources
      │   └─ 打包组件CSS/JS，生成内容哈希文件名
      ├─ Phase 1: PageTypeDispatcher
      │   ├─ 1. generate() 生成虚拟页面
      │   │   └─ 所有 pageType.generate()
      │   ├─ 2. 匹配并渲染普通页面
      │   │   ├─ 遍历所有内容
      │   │   ├─ pageType.match() 匹配
      │   │   └─ renderPage() 渲染
      │   └─ 3. 渲染虚拟页面
      │       └─ renderPage() 渲染
      └─ Phase 2: 其他 Emitters
          ├─ ContentIndex (sitemap, RSS, search)
          ├─ Assets
          ├─ Static
          └─ ...
```

### 增量构建（Watch 模式）

当使用 `--watch` 或 `--serve` 时，Quartz 会启动文件监视器：

```
chokidar 监听内容目录
  ↓
文件变更 (add/change/unlink)
  ↓
防抖 100ms
  ↓
rebuild() [build.ts]
  ├─ 更新 contentMap
  ├─ 重新解析变更的文件
  ├─ 收集 changeEvents
  ├─ 更新 allFiles / allSlugs
  ├─ 重新过滤
  └─ 增量发射
      ├─ PageTypeDispatcher.partialEmit()
      │   ├─ 重新生成所有虚拟页面
      │   └─ 只重新渲染变更的页面
      └─ 其他 Emitter.partialEmit()
          └─ 只处理变更的文件
  ↓
WebSocket 通知前端刷新
```

### 多线程构建

当文件数量较多时，Quartz 自动启用多线程：

```
主线程
  ├─ 转译 worker.ts
  ├─ 创建 WorkerPool
  │   ├─ Worker 1
  │   ├─ Worker 2
  │   └─ Worker N (默认 = files/128, 最多4)
  ├─ 分块 (每块128文件)
  ├─ 并行执行 Text→MDAST
  ├─ 合并结果
  ├─ 并行执行 MDAST→HAST
  └─ 合并结果
```

并发数计算公式：
```
concurrency = min(max(round(files / 128), 1), 4)
```

---

## 组件系统

### 组件结构

Quartz 组件是增强版的 Preact 函数组件，附带 CSS 和 JS 资源。

### 组件注册

组件通过 `componentRegistry` 进行管理：

```typescript
// 注册组件
componentRegistry.register(name, {
  component: ComponentConstructor,
  options: defaultOptions
})

// 获取组件
const registered = componentRegistry.get(name)

// 实例化组件
const instance = componentRegistry.instantiate(constructor, options)
```

### 页面布局

页面由多个布局槽位组成：

```
┌─────────────────────────────────────────┐
│            Header (页眉)                │
├──────────┬──────────────────┬───────────┤
│          │  Before Body     │           │
│          │  (正文前)         │           │
│  Left    ├──────────────────┤  Right    │
│  (左侧)  │                  │  (右侧)   │
│          │   Page Body      │           │
│          │   (正文主体)      │           │
│          │                  │           │
│          ├──────────────────┤           │
│          │  After Body      │           │
│          │  (正文后)         │           │
├──────────┴──────────────────┴───────────┤
│            Footer (页脚)                │
└─────────────────────────────────────────┘
```

### 页面框架 (Frames)

框架定义了页面的整体结构布局：

| 框架 | 说明 | 适用场景 |
|------|------|----------|
| `default` | 默认框架，含侧边栏 | 普通页面 |
| `full-width` | 全宽框架，无边栏 | 内容密集页面 |
| `minimal` | 极简框架 | 特殊页面 |

### 组件渲染条件

组件可以配置渲染条件：

| 条件 | 说明 |
|------|------|
| `not-index` | 非首页时显示 |
| `is-index` | 仅首页显示 |

### 显示修饰

| 修饰 | 说明 |
|------|------|
| `mobile-only` | 仅移动端显示 |
| `desktop-only` | 仅桌面端显示 |
| `all` | 始终显示（默认） |

### Flex 分组

多个组件可以组合成 Flex 容器：

```yaml
layout:
  groups:
    toolbar:           # 组名
      priority: 35     # 组优先级
      direction: row   # 排列方向: row / column
      gap: 0.5rem      # 间距
  ...
  - source: some-plugin
    layout:
      group: toolbar   # 加入组
      groupOptions:
        grow: true     # flex-grow
        shrink: false  # flex-shrink
```

---

## 国际化 (i18n)

### 支持的语言

Quartz 支持 25+ 种语言：

| 语言代码 | 语言名称 |
|----------|----------|
| `en-US` | 英语（美国） |
| `en-GB` | 英语（英国） |
| `zh-CN` | 简体中文 |
| `zh-TW` | 繁体中文 |
| `ja-JP` | 日语 |
| `ko-KR` | 韩语 |
| `fr-FR` | 法语 |
| `de-DE` | 德语 |
| `es-ES` | 西班牙语 |
| `pt-BR` | 葡萄牙语（巴西） |
| `ru-RU` | 俄语 |
| `ar-SA` | 阿拉伯语 |
| `fa-IR` | 波斯语 |
| `he-IL` | 希伯来语 |
| ... | ... |

### 配置方式

```yaml
configuration:
  locale: zh-CN  # 设置为简体中文
```

### i18n 使用

```typescript
import { i18n } from "../i18n"

// 获取翻译
const text = i18n(cfg.locale).components.someComponent.someKey

// 带参数
const text = i18n(cfg.locale).components.transcludes.transcludeOf({
  targetSlug: slug
})
```

---

## 附录

### 核心技术栈

| 技术 | 用途 |
|------|------|
| **TypeScript** | 主开发语言 |
| **Node.js** | 运行时 |
| **Preact** | 轻量级 React 兼容 UI 库 |
| **unified** | 文本处理生态 |
| **remark** | Markdown 解析和转换 |
| **rehype** | HTML 解析和转换 |
| **esbuild** | 快速构建工具 |
| **workerpool** | 多线程 Worker 池 |
| **chokidar** | 文件监听 |
| **SASS/SCSS** | CSS 预处理器 |
| **lightningcss** | CSS 优化 |
| **yaml** | YAML 解析 |
| **sharp** | 图片处理 |
| **isomorphic-git** | 纯 JS Git 实现 |
| **micromorph** | SPA 页面转换动画 |

### 关键目录索引

| 路径 | 说明 |
|------|------|
| [quartz/build.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/build.ts) | 构建主入口 |
| [quartz/cfg.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cfg.ts) | 配置类型定义 |
| [quartz/processors/parse.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/parse.ts) | Markdown 解析 |
| [quartz/processors/filter.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/filter.ts) | 内容过滤 |
| [quartz/processors/emit.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/processors/emit.ts) | 内容发射 |
| [quartz/plugins/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/types.ts) | 插件类型 |
| [quartz/plugins/loader/config-loader.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/loader/config-loader.ts) | 配置加载器 |
| [quartz/plugins/pageTypes/dispatcher.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/plugins/pageTypes/dispatcher.ts) | 页面调度器 |
| [quartz/components/renderPage.tsx](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/renderPage.tsx) | 页面渲染 |
| [quartz/components/types.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/components/types.ts) | 组件类型 |
| [quartz/util/ctx.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/ctx.ts) | 构建上下文 |
| [quartz/util/path.ts](file:///e:/Obsidian_notebook/my-digital-garden/quartz/util/path.ts) | 路径工具 |
| [quartz/cli/handlers.js](file:///e:/Obsidian_notebook/my-digital-garden/quartz/cli/handlers.js) | CLI 处理器 |
| [quartz.config.yaml](file:///e:/Obsidian_notebook/my-digital-garden/quartz.config.yaml) | 主配置文件 |

### 参考资源

- **官方文档**: https://quartz.jzhao.xyz/
- **GitHub 仓库**: https://github.com/jackyzha0/quartz
- **Discord 社区**: https://discord.gg/cRFFHYye7t
