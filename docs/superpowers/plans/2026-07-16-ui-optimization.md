# Quartz UI 优化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Quartz 默认 UI 升级为 "Editorial Botanical"（编辑式植物学）设计风格，通过色彩、字体、纹理、动效、布局五个维度全面提升视觉品质。

**Architecture:** 仅修改 4 个文件（quartz.config.yaml、variables.scss、base.scss、custom.scss），不新增文件、不改动组件逻辑。所有视觉增强通过 CSS 变量和 SCSS 样式实现，零额外资源依赖。

**Tech Stack:** SCSS / CSS Custom Properties / Quartz v5 构建系统

**设计方向：** Editorial Botanical — 暖纸张底色 + 苔藓绿强调 + 衬线编辑字体 + 纸张噪点纹理 + 克制动效

**验证方式：** 每个任务后执行 `npx quartz build -d docs -o public`，构建成功即 SCSS 语法正确。首次构建可能较慢（需安装插件），后续增量构建会快很多。

**文件总览：**

| 文件 | 职责 |
|------|------|
| `quartz.config.yaml` | 色彩值 + 字体配置（YAML 格式） |
| `quartz/styles/variables.scss` | SCSS 变量：间距、断点、网格 |
| `quartz/styles/base.scss` | 全局基础样式：排版、链接、代码、表格、图片等 |
| `quartz/styles/custom.scss` | 自定义样式入口（当前为空），由 `componentResources.ts` 导入 |

---

## Task 1: 色彩与字体配置

**Files:**
- Modify: `quartz.config.yaml:18-42`

**说明：** 替换 `theme.typography` 和 `theme.colors` 配置，将蓝灰色系改为植物学暖色系，将通用字体改为有性格的编辑字体。

- [ ] **Step 1: 替换 typography 和 colors 配置**

在 `quartz.config.yaml` 中，将第 18-42 行（typography + colors 块）替换为以下内容：

**旧内容（第 18-42 行）：**
```yaml
    typography:
      header: Schibsted Grotesk
      body: Source Sans Pro
      code: IBM Plex Mono
    colors:
      lightMode:
        light: "#faf8f8"
        lightgray: "#e5e5e5"
        gray: "#b8b8b8"
        darkgray: "#4e4e4e"
        dark: "#2b2b2b"
        secondary: "#284b63"
        tertiary: "#84a59d"
        highlight: rgba(143, 159, 169, 0.15)
        textHighlight: "#fff23688"
      darkMode:
        light: "#161618"
        lightgray: "#393639"
        gray: "#646464"
        darkgray: "#d4d4d4"
        dark: "#ebebec"
        secondary: "#7b97aa"
        tertiary: "#84a59d"
        highlight: rgba(143, 159, 169, 0.15)
        textHighlight: "#b3aa0288"
```

**新内容：**
```yaml
    typography:
      header: Fraunces
      body: Newsreader
      code: JetBrains Mono
    colors:
      lightMode:
        light: "#f7f5f0"
        lightgray: "#e8e4dc"
        gray: "#a8a39a"
        darkgray: "#3d3a35"
        dark: "#26241f"
        secondary: "#3d5a3d"
        tertiary: "#8b9d6a"
        highlight: rgba(139, 157, 106, 0.12)
        textHighlight: "#e8d88288"
      darkMode:
        light: "#1a1a17"
        lightgray: "#3a3735"
        gray: "#6a6560"
        darkgray: "#d4d4d4"
        dark: "#ebebec"
        secondary: "#8aab7a"
        tertiary: "#9bb87a"
        highlight: rgba(139, 157, 106, 0.12)
        textHighlight: "#b3aa0288"
```

- [ ] **Step 2: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功，无 YAML 解析错误。页面颜色和字体应已变化。

- [ ] **Step 3: 格式化并提交**

```bash
npx prettier --write quartz.config.yaml
git add quartz.config.yaml
git commit -m "feat(ui): switch to editorial botanical color palette and fonts"
```

---

## Task 2: 布局间距优化

**Files:**
- Modify: `quartz/styles/variables.scss:20-21`
- Modify: `quartz/styles/base.scss:163` (page max-width)
- Modify: `quartz/styles/base.scss:225` (sidebar padding)
- Modify: `quartz/styles/base.scss:559` (line-height)

**说明：** 减小顶部留白、收窄侧栏、缩窄内容最大宽度、增加正文行高，改善内容呼吸感。

- [ ] **Step 1: 修改 variables.scss 间距变量**

将 `quartz/styles/variables.scss` 第 20-21 行：

```scss
$sidePanelWidth: 320px; //380px;
$topSpacing: 6rem;
```

替换为：

```scss
$sidePanelWidth: 300px;
$topSpacing: 4rem;
```

- [ ] **Step 2: 修改 page 最大宽度**

将 `quartz/styles/base.scss` 第 163 行：

```scss
  max-width: calc(#{map.get($breakpoints, desktop)} + 300px);
```

替换为：

```scss
  max-width: calc(#{map.get($breakpoints, desktop)} + 200px);
```

- [ ] **Step 3: 修改 sidebar padding**

将 `quartz/styles/base.scss` 第 225 行：

```scss
      padding: $topSpacing 2rem 2rem 2rem;
```

替换为：

```scss
      padding: $topSpacing 1.5rem 2rem 1.5rem;
```

- [ ] **Step 4: 修改正文行高**

将 `quartz/styles/base.scss` 第 556-560 行：

```scss
tbody,
li,
p {
  line-height: 1.6rem;
}
```

替换为：

```scss
tbody,
li,
p {
  line-height: 1.7rem;
}
```

- [ ] **Step 5: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。布局间距应有变化——侧栏变窄、顶部留白减少、行距更宽松。

- [ ] **Step 6: 格式化并提交**

```bash
npx prettier --write quartz/styles/variables.scss quartz/styles/base.scss
git add quartz/styles/variables.scss quartz/styles/base.scss
git commit -m "feat(ui): adjust layout spacing for better content breathing room"
```

---

## Task 3: 阴影系统与圆角节奏

**Files:**
- Modify: `quartz/styles/base.scss:29` (text-highlight radius)
- Modify: `quartz/styles/base.scss:492` (pre radius)
- Modify: `quartz/styles/base.scss:551` (code radius)
- Modify: `quartz/styles/base.scss:600` (img radius)
- Modify: `quartz/styles/base.scss:621` (audio/video radius)
- Modify: `quartz/components/styles/popover.scss:38-39` (popover radius + shadow)
- Modify: `quartz/styles/base.scss:513` (highlighted chars radius)

**说明：** 将全局统一的 `5px` 圆角改为有节奏的层级——内联元素更紧凑，容器元素更柔和。同步优化 popover 阴影。

- [ ] **Step 1: 修改 text-highlight 圆角**

将 `quartz/styles/base.scss` 第 29 行：

```scss
  border-radius: 5px;
```

替换为：

```scss
  border-radius: 4px;
```

> 注意：第 29 行位于 `.text-highlight` 块内。如果 `border-radius: 5px;` 在文件中出现多次，需要使用更大上下文来唯一定位。使用以下替换：

旧：
```scss
.text-highlight {
  background-color: var(--textHighlight);
  padding: 0 0.1rem;
  border-radius: 5px;
```

新：
```scss
.text-highlight {
  background-color: var(--textHighlight);
  padding: 0 0.1rem;
  border-radius: 4px;
```

- [ ] **Step 2: 修改 pre 圆角**

将 `quartz/styles/base.scss` 第 489-495 行：

```scss
pre {
  font-family: var(--codeFont);
  padding: 0 0.5rem;
  border-radius: 5px;
  overflow-x: auto;
  border: 1px solid var(--lightgray);
  position: relative;
```

替换为：

```scss
pre {
  font-family: var(--codeFont);
  padding: 0 0.5rem;
  border-radius: 8px;
  overflow-x: auto;
  border: 1px solid var(--lightgray);
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
```

- [ ] **Step 3: 修改 highlighted chars 圆角**

将 `quartz/styles/base.scss` 第 512-514 行：

```scss
    & [data-highlighted-chars] {
      background-color: var(--highlight);
      border-radius: 5px;
    }
```

替换为：

```scss
    & [data-highlighted-chars] {
      background-color: var(--highlight);
      border-radius: 4px;
    }
```

- [ ] **Step 4: 修改 code 圆角**

将 `quartz/styles/base.scss` 第 547-554 行：

```scss
code {
  font-size: 0.9em;
  color: var(--dark);
  font-family: var(--codeFont);
  border-radius: 5px;
  padding: 0.1rem 0.2rem;
  background: var(--lightgray);
}
```

替换为：

```scss
code {
  font-size: 0.9em;
  color: var(--dark);
  font-family: var(--codeFont);
  border-radius: 4px;
  padding: 0.1rem 0.2rem;
  background: var(--lightgray);
}
```

- [ ] **Step 5: 修改 img 圆角**

将 `quartz/styles/base.scss` 第 598-603 行：

```scss
img {
  max-width: 100%;
  border-radius: 5px;
  margin: 1rem 0;
  content-visibility: auto;
}
```

替换为：

```scss
img {
  max-width: 100%;
  border-radius: 12px;
  margin: 1rem 0;
  content-visibility: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
```

- [ ] **Step 6: 修改 audio/video 圆角**

将 `quartz/styles/base.scss` 第 618-622 行：

```scss
audio,
video {
  width: 100%;
  border-radius: 5px;
}
```

替换为：

```scss
audio,
video {
  width: 100%;
  border-radius: 8px;
}
```

- [ ] **Step 7: 修改 popover 圆角和阴影**

将 `quartz/components/styles/popover.scss` 第 38-39 行：

```scss
    border-radius: 5px;
    box-shadow: 6px 6px 36px 0 rgba(0, 0, 0, 0.25);
```

替换为：

```scss
    border-radius: 10px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
```

- [ ] **Step 8: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。圆角和阴影层次应有变化——图片更圆润、代码块有柔和阴影、popover 阴影更自然。

- [ ] **Step 9: 格式化并提交**

```bash
npx prettier --write quartz/styles/base.scss quartz/components/styles/popover.scss
git add quartz/styles/base.scss quartz/components/styles/popover.scss
git commit -m "feat(ui): introduce layered border-radius rhythm and soft shadows"
```

---

## Task 4: 纸张纹理与氛围背景

**Files:**
- Modify: `quartz/styles/custom.scss` (替换全部内容)

**说明：** 在 `body::before` 上叠加 SVG 噪点纹理和微妙的径向渐变，营造翻阅旧书的纸张质感。当前 `custom.scss` 为空（仅有一行 `@use` 和注释）。

- [ ] **Step 1: 写入 custom.scss 纸张纹理**

将 `quartz/styles/custom.scss` 全部内容替换为：

```scss
@use "./variables.scss" as *;

// ============================================================================
// Editorial Botanical — Custom Styles
// ============================================================================

// --- 纸张噪点纹理 ---
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 200px 200px;
}

// --- 氛围渐变 ---
body::after {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -2;
  background: radial-gradient(
    ellipse at top,
    rgba(139, 157, 106, 0.04),
    transparent 60%
  );
}
```

- [ ] **Step 2: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。页面背景应有微妙的纸张纹理（几乎不可见但能感受到质感）。

- [ ] **Step 3: 格式化并提交**

```bash
npx prettier --write quartz/styles/custom.scss
git add quartz/styles/custom.scss
git commit -m "feat(ui): add paper noise texture and ambient gradient background"
```

---

## Task 5: 动效系统

**Files:**
- Modify: `quartz/styles/custom.scss` (在末尾追加)

**说明：** 添加页面加载渐入动画、标题装饰下划线动画、`prefers-reduced-motion` 无障碍降级。所有动效仅使用 CSS，不引入 JS 依赖。

- [ ] **Step 1: 追加页面加载动画**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 页面加载动画 ---
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

article {
  animation: fadeInUp 0.6s ease-out;
}
```

- [ ] **Step 2: 追加标题装饰下划线**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 标题装饰下划线 ---
h1,
h2 {
  position: relative;

  &::after {
    content: "";
    position: absolute;
    bottom: -0.3rem;
    left: 0;
    width: 2rem;
    height: 2px;
    background: var(--secondary);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
  }

  &:hover::after {
    transform: scaleX(1);
  }
}
```

- [ ] **Step 3: 追加代码块悬停效果**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 代码块悬停 ---
pre {
  transition: box-shadow 0.3s ease, border-color 0.3s ease;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border-color: var(--gray);
  }
}
```

- [ ] **Step 4: 追加图片悬停效果**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 图片悬停 ---
img {
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.01);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }
}
```

- [ ] **Step 5: 追加无障碍降级**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 无障碍：尊重 prefers-reduced-motion ---
@media (prefers-reduced-motion: reduce) {
  article,
  h1,
  h2,
  pre,
  img {
    animation: none !important;
    transition: none !important;
  }

  h1::after,
  h2::after {
    display: none;
  }
}
```

- [ ] **Step 6: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。刷新页面时正文应有渐入动画，标题悬停时显示装饰下划线。

- [ ] **Step 7: 格式化并提交**

```bash
npx prettier --write quartz/styles/custom.scss
git add quartz/styles/custom.scss
git commit -m "feat(ui): add page load animation and hover micro-interactions"
```

---

## Task 6: 内容元素增强

**Files:**
- Modify: `quartz/styles/base.scss:391-396` (blockquote)
- Modify: `quartz/styles/base.scss:591-596` (table tr)
- Modify: `quartz/styles/base.scss:610-616` (hr)

**说明：** 增强引用块（加背景、圆角、悬停）、表格行悬停效果、水平分割线美化。

- [ ] **Step 1: 增强 blockquote**

将 `quartz/styles/base.scss` 第 391-396 行：

```scss
blockquote {
  margin: 1rem 0;
  border-left: 3px solid var(--secondary);
  padding-left: 1rem;
  transition: border-color 0.2s ease;
}
```

替换为：

```scss
blockquote {
  margin: 1rem 0;
  border-left: 4px solid var(--secondary);
  padding: 0.5rem 1rem;
  border-radius: 0 6px 6px 0;
  background: var(--highlight);
  transition: border-color 0.3s ease, background 0.3s ease;

  &:hover {
    border-left-width: 5px;
  }
}
```

- [ ] **Step 2: 增强表格行悬停**

将 `quartz/styles/base.scss` 第 591-596 行：

```scss
tr {
  border-bottom: 1px solid var(--lightgray);
  &:last-child {
    border-bottom: none;
  }
}
```

替换为：

```scss
tr {
  border-bottom: 1px solid var(--lightgray);
  transition: background-color 0.2s ease;

  &:last-child {
    border-bottom: none;
  }

  tbody &:hover {
    background-color: var(--highlight);
  }
}
```

- [ ] **Step 3: 增强 hr**

将 `quartz/styles/base.scss` 第 610-616 行：

```scss
hr {
  width: 100%;
  margin: 2rem auto;
  height: 1px;
  border: none;
  background-color: var(--lightgray);
}
```

替换为：

```scss
hr {
  width: 100%;
  margin: 2rem auto;
  height: 1px;
  border: none;
  background: linear-gradient(
    to right,
    transparent,
    var(--lightgray) 20%,
    var(--lightgray) 80%,
    transparent
  );
}
```

- [ ] **Step 4: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。引用块有背景色和圆角，表格行悬停有高亮，分割线有渐变淡出效果。

- [ ] **Step 5: 格式化并提交**

```bash
npx prettier --write quartz/styles/base.scss
git add quartz/styles/base.scss
git commit -m "feat(ui): enhance blockquote, table hover, and hr with depth"
```

---

## Task 7: 链接与导航增强

**Files:**
- Modify: `quartz/styles/base.scss:94-99` (a.internal)
- Modify: `quartz/styles/base.scss:674-683` (navigation-progress)

**说明：** 精细化内部链接样式——保留 highlight 背景但收窄圆角，添加悬停下划线动画。导航进度条改为更细的渐变条。

- [ ] **Step 1: 增强 a.internal 链接**

将 `quartz/styles/base.scss` 第 94-99 行：

```scss
  &.internal {
    text-decoration: none;
    background-color: var(--highlight);
    padding: 0 0.1rem;
    border-radius: 5px;
    line-height: 1.4rem;
```

替换为：

```scss
  &.internal {
    text-decoration: none;
    background-color: var(--highlight);
    padding: 0 0.1rem;
    border-radius: 4px;
    line-height: 1.4rem;
    transition: background-color 0.2s ease, color 0.2s ease;
```

- [ ] **Step 2: 增强导航进度条**

将 `quartz/styles/base.scss` 第 674-683 行：

```scss
.navigation-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 3px;
  background: var(--secondary);
  transition: width 0.2s ease;
  z-index: 9999;
}
```

替换为：

```scss
.navigation-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(to right, var(--secondary), var(--tertiary));
  transition: width 0.2s ease;
  z-index: 9999;
}
```

- [ ] **Step 3: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。内部链接圆角更紧凑，进度条更细且有渐变色。

- [ ] **Step 4: 格式化并提交**

```bash
npx prettier --write quartz/styles/base.scss
git add quartz/styles/base.scss
git commit -m "feat(ui): refine internal links and navigation progress bar"
```

---

## Task 8: 自定义滚动条与选区

**Files:**
- Modify: `quartz/styles/custom.scss` (在末尾追加)

**说明：** 自定义窄滚动条（WebKit + Firefox），美化文本选区颜色，添加暗色模式适配。

- [ ] **Step 1: 追加自定义滚动条**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 自定义滚动条 (WebKit) ---
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--lightgray);
  border-radius: 4px;

  &:hover {
    background: var(--gray);
  }
}

// --- 自定义滚动条 (Firefox) ---
* {
  scrollbar-width: thin;
  scrollbar-color: var(--lightgray) transparent;
}
```

- [ ] **Step 2: 追加选区样式**

在 `quartz/styles/custom.scss` 末尾追加：

```scss

// --- 文本选区 ---
::selection {
  background: var(--tertiary);
  color: var(--light);
  border-radius: 2px;
}
```

- [ ] **Step 3: 验证构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功。滚动条变窄并使用主题色，选中文本时显示植物绿高亮。

- [ ] **Step 4: 格式化并提交**

```bash
npx prettier --write quartz/styles/custom.scss
git add quartz/styles/custom.scss
git commit -m "feat(ui): add custom scrollbar and text selection styling"
```

---

## Task 9: 最终验证与格式化

**Files:**
- Verify: 所有修改过的文件

**说明：** 执行完整构建、Prettier 格式检查、确认所有改动一致。

- [ ] **Step 1: 运行完整构建**

运行: `npx quartz build -d docs -o public`
预期: 构建成功，无警告、无错误。

- [ ] **Step 2: 运行 Prettier 检查**

运行: `npx prettier --check quartz.config.yaml quartz/styles/variables.scss quartz/styles/base.scss quartz/styles/custom.scss quartz/components/styles/popover.scss`
预期: 所有文件格式正确。如果有不通过的，运行 `npx prettier --write` 修复。

- [ ] **Step 3: 最终提交（如有格式修复）**

```bash
git add -A
git status
# 如果有未提交的格式修复：
git commit -m "style: format all modified files"
```

- [ ] **Step 4: 清理构建产物（可选）**

```bash
# public 目录是构建输出，可加入 .gitignore 或删除
Remove-Item -Recurse -Force public -ErrorAction SilentlyContinue
```

---

## 设计决策摘要

| 决策 | 选择 | 理由 |
|------|------|------|
| 色彩方向 | 暖纸张底 + 苔藓绿强调 | 呼应"数字花园"植物学隐喻 |
| 标题字体 | Fraunces | 有机衬线体，带墨水笔触感，支持光学尺寸 |
| 正文字体 | Newsreader | 专为屏幕阅读优化的衬线体 |
| 代码字体 | JetBrains Mono | 连字支持好，辨识度高 |
| 纹理 | SVG feTurbulence 噪点 | 纯 CSS 生成，零额外资源 |
| 动效策略 | 克制——仅页面加载 + hover | 不干扰阅读，提升精致感 |
| 圆角节奏 | 4px / 8px / 12px 三级 | 内联紧凑、容器柔和、图片圆润 |
| 阴影策略 | 三个层级 soft/medium/deep | 营造深度但不突兀 |
| 无障碍 | prefers-reduced-motion 降级 | 所有动效可被禁用 |
