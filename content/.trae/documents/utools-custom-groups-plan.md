# uTools 用户自定义分组功能实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 uTools 主界面的"已固定"区域实现用户自定义分组功能，支持创建、重命名、删除分组，以及将功能在不同分组间拖拽移动。

**Architecture:** 采用"视图层分组 + localStorage 配置"的薄层架构。在现有 React 组件（Ge/He/je）的数据流中注入分组拆分逻辑，配置持久化使用 `window.localStorage`，零外部依赖。拖拽系统复用现有 `je` 组件的 86px 网格拖拽，扩展跨分组检测。

**Tech Stack:** Electron (uTools 5.x), React (打包后), localStorage, Vanilla JS patch

---

## Summary

uTools 主界面当前将"已固定"功能作为一个整体平面网格展示（`je` 组件渲染 86x86 flex-wrap 网格）。本计划在**不重构整体架构**的前提下，通过修改 `dist/index.js` 中的关键数据流和交互逻辑，实现：

1. 用户可创建任意数量的自定义分组
2. 每个分组独立渲染为带标题栏的 `result-panel-group`
3. 同分组内保留现有拖拽排序，扩展支持跨分组拖拽移动
4. 配置通过 `localStorage` 持久化，首次使用完全兼容原版

---

## Current State Analysis

### 代码位置

- **打包源文件**: `C:\Users\gfbj\AppData\Local\Programs\utools\resources\app.asar`
- **解压后工作文件**: `c:\Users\gfbj\.trae-cn\work\6a45d8014f4d85c1c8975cd5\utools_extracted\dist\index.js`
- **目标部署文件**: 修改后的 `dist/index.js` 需重新打包为 `app.asar` 或替换原文件

### 核心组件结构

| 组件 | 职责 | 关键发现 |
|------|------|----------|
| `Ge` | 结果面板主容器，管理 `resultGroups` 状态 | 硬编码分组逻辑：`recent` → "最近使用"(9个)、`menus` → "已固定"(全部)、`store` → "市场精选"(9个) |
| `He` | 分组容器，渲染标题栏 + 内容区 | 根据 `group.render.type` 分发到 `je` / `Me` / `Ve`；标题来自 `group.source.cmd.label` |
| `je` | 网格菜单渲染（86x86） | 已支持同分组内拖拽排序，基于 `86px` 网格计算位置，每行固定 9 个 |
| `ze` | 单个菜单项渲染 | 支持右键菜单 `window.services.showMainCmdMenu` |

### 现有数据流

```
window.services.getPluginContainer() ──> Ge 组件
                                              |
                                              v
                                    searchResult.forEach
                                              |
                                              v
                                    n=[recent, menus, others]
                                              |
                                              v
                                    n.forEach -> resultGroups
                                              |
                                              v
                                    render -> result-panel
```

### 现有存储机制

- **`window.localStorage`**: 已存储 `recentcmdlog`，说明可用且稳定
- **`window.services.sortMainCmdMenus({pluginId, label}, {pluginId, label})`**: 后端 API，保存整体排序，必须保留调用
- **LevelDB**: uTools 内部使用，但无 renderer 暴露接口，不直接使用

---

## Proposed Changes

### Task 1: 注入全局配置模块

**Files:**
- Modify: `dist/index.js`（全局注入点，文件顶部 IIFE 开头）

**定位方式**: 搜索字符串 `"use strict";var e=` 之后的第一处可插入位置。

- [ ] **Step 1: 在全局作用域注入 `window.__customGroups` 模块**

在 `(()=>{"use strict";` 后的第一个可执行位置插入以下代码：

```javascript
window.__customGroups = function(){
  var KEY = 'utools_custom_groups_v1';
  var DEFAULT = {v:1, groups:[{id:'__default', name:'已固定', items:[]}]};
  return {
    load: function(){
      try { var d = JSON.parse(window.localStorage.getItem(KEY)); if(d && d.v === 1) return d; } catch(e){}
      return JSON.parse(JSON.stringify(DEFAULT));
    },
    save: function(data){
      window.localStorage.setItem(KEY, JSON.stringify(data));
      window.dispatchEvent(new Event('utools_custom_groups_changed'));
    },
    getCmdKey: function(cmd){ return cmd.pluginId + '|' + cmd.featureCode + '|' + cmd.label; }
  };
}();
```

- [ ] **Step 2: 验证注入位置正确**

Run: 启动 uTools（或测试环境），在 DevTools Console 执行 `window.__customGroups.load()`
Expected: 返回 `{v:1, groups:[{id:'__default', name:'已固定', items:[]}]}`

---

### Task 2: 修改 Ge 组件的分组构建逻辑

**Files:**
- Modify: `dist/index.js`（约 227300 字符附近）

**定位方式**: 搜索字符串 `n=[{all:[],type:"recent"},{all:[],type:"menus"` 定位当前分组收集逻辑。

- [ ] **Step 1: 将 `menus` 单数组收集改为扁平收集 + 按配置拆分**

将当前代码段：
```javascript
n=[{all:[],type:"recent"},{all:[],type:"menus",bar:{label:"全部 >",action:this.props.goSettingsFeatureCmds}},{all:[]}],
e.searchResult.forEach(e=>{"recent"===e.type?n[0].all.push(e):"menus"===e.type?n[1].all.push(e):n[2].all.push(e)});
```

替换为：
```javascript
var recentAll=[], menusAll=[], othersAll=[];
e.searchResult.forEach(function(item){
  if(item.type==="recent") recentAll.push(item);
  else if(item.type==="menus") menusAll.push(item);
  else othersAll.push(item);
});
var cg = window.__customGroups.load();
var menuGroups = [];
if(cg && cg.groups && cg.groups.length > 0){
  var menuMap = {};
  menusAll.forEach(function(m){ menuMap[window.__customGroups.getCmdKey(m.cmd)] = m; });
  cg.groups.forEach(function(g){
    var groupItems = [];
    g.items.forEach(function(k){ if(menuMap[k]){ groupItems.push(menuMap[k]); delete menuMap[k]; } });
    if(groupItems.length > 0 || g.id === '__default'){
      menuGroups.push({all:groupItems, type:"menus", bar:{label:"全部 >",action:this.props.goSettingsFeatureCmds}, __cgId:g.id, __cgName:g.name});
    }
  });
  Object.keys(menuMap).forEach(function(k){
    var def = menuGroups.find(function(x){ return x.__cgId === '__default'; });
    if(def) def.all.push(menuMap[k]);
  });
} else {
  menuGroups = [{all:menusAll, type:"menus", bar:{label:"全部 >",action:this.props.goSettingsFeatureCmds}, __cgId:'__default', __cgName:'已固定'}];
}
n = [{all:recentAll, type:"recent"}].concat(menuGroups).concat([{all:othersAll}]);
```

- [ ] **Step 2: 修改后续 `n.forEach` 循环以识别自定义分组标题**

在 `n.forEach((n,a)=>{...})` 循环中，找到 `else if(1===a)o="已固定"` 分支，替换为动态标题逻辑：

```javascript
else if(n.__cgName){ o = n.__cgName; }
```

确保该分支在 `else if(0===a)o="最近使用"` 之后、原 `else if(1===a)o="已固定"` 之前执行。

- [ ] **Step 3: 验证分组拆分正确**

Run: 启动 uTools，DevTools 中执行 `window.__customGroups.save({v:1, groups:[{id:'__default', name:'已固定', items:[]}, {id:'cg_dev', name:'开发工具', items:[]}]})`，刷新界面
Expected: 出现两个标题分别为"已固定"和"开发工具"的网格分组

---

### Task 3: Ge 组件响应配置变更事件

**Files:**
- Modify: `dist/index.js`（`class Ge` 的生命周期方法区域）

**定位方式**: 搜索 `componentDidMount(){window.services.listenFromPluginPush(this.handleFromPluginPush)}`

- [ ] **Step 1: 在 `componentDidMount` 中注册自定义分组事件监听**

在 `componentDidMount` 方法内追加：
```javascript
window.addEventListener('utools_custom_groups_changed', this.handleCustomGroupsChange);
```

- [ ] **Step 2: 在 `componentWillUnmount` 中注销监听（如方法不存在则新建）**

搜索 `componentWillUnmount`，若存在则在末尾追加：
```javascript
window.removeEventListener('utools_custom_groups_changed', this.handleCustomGroupsChange);
```

若不存在，在 `componentDidMount` 之后新建该方法：
```javascript
componentWillUnmount(){
  window.services.listenFromPluginPush(null);
  window.removeEventListener('utools_custom_groups_changed', this.handleCustomGroupsChange);
}
```

- [ ] **Step 3: 新增 `handleCustomGroupsChange` 方法**

在 `Ge` 类中新增方法（建议放在 `handleFromPluginPush` 附近）：
```javascript
this.handleCustomGroupsChange = () => {
  this._buildResultGroups(this.props);
};
```

注意：`this._buildResultGroups` 是对当前分组构建逻辑的提取。如果构建逻辑直接内联在 `render` 或 `componentDidUpdate` 中，需要将其提取为独立方法以便复用。提取方式为将 `const t=[],n=...` 开始的构建代码块移入 `_buildResultGroups(props)` 方法，并在原位置调用 `this._buildResultGroups(this.props)`。

---

### Task 4: je 组件同步排序到配置

**Files:**
- Modify: `dist/index.js`（`je` 组件 `handleMouseUp` 方法内）

**定位方式**: 搜索 `window.services.sortMainCmdMenus({pluginId:o.cmd.pluginId`

- [ ] **Step 1: 在同分组排序完成后同步 `__customGroups`**

在 `i.splice(r,0,o)` 之后、`this.forceUpdate()` 之前插入：
```javascript
var cgid = this.props.render.__cgId;
if(cgid){
  var cg = window.__customGroups.load();
  var g = cg.groups.find(function(x){ return x.id === cgid; });
  if(g){
    g.items = i.map(function(item){ return window.__customGroups.getCmdKey(item.cmd); });
    window.__customGroups.save(cg);
  }
}
```

- [ ] **Step 2: 保留原 `sortMainCmdMenus` 调用**

确保原调用 `window.services.sortMainCmdMenus(...)` 仍然执行，以维持与 uTools 原生设置页的兼容性。

---

### Task 5: 实现跨分组拖拽

**Files:**
- Modify: `dist/index.js`（`je` 组件 `handleMouseUp` + `He` 组件 `render`）

**定位方式**: `je` 中搜索 `if(null===r)return;`

- [ ] **Step 1: 修改 `je.handleMouseUp` 的 null 检测分支**

将 `if(null===r)return;` 替换为：
```javascript
if(null===r){
  var el = document.elementFromPoint(e.clientX, e.clientY);
  while(el && !el.classList.contains('result-panel-group')) el = el.parentElement;
  var selfGroup = this.boxRef.closest('.result-panel-group');
  if(el && el !== selfGroup){
    var targetKey = el.getAttribute('data-group-key');
    var fromCid = this.props.render.__cgId;
    var draggedItem = this.props.render.data[a];
    if(targetKey && fromCid && draggedItem){
      window.dispatchEvent(new CustomEvent('utools_menu_drag_to_group', {
        detail: { fromCid: fromCid, toGroupKey: targetKey, cmd: draggedItem.cmd }
      }));
    }
  }
  // 原有清理逻辑保持不变
  this._dragMenuItem=null;
  if(this._dragMenuItem && this._dragMenuItem.dragRef) this._dragMenuItem.dragRef.remove();
  // ... 其余清理代码
  return;
}
```

- [ ] **Step 2: 在 `He` 组件渲染根元素上添加 `data-group-key`**

搜索 `class He extends r.PureComponent` 的 `render` 方法中：
```javascript
r.createElement("div",{className:"result-panel-group"}, ...)
```

替换为：
```javascript
r.createElement("div",{className:"result-panel-group", "data-group-key": n.key}, ...)
```

- [ ] **Step 3: 在 `Ge` 组件中监听跨分组拖拽事件**

在 `componentDidMount` 中追加：
```javascript
window.addEventListener('utools_menu_drag_to_group', this.handleDragToGroup);
```

在 `componentWillUnmount` 中追加：
```javascript
window.removeEventListener('utools_menu_drag_to_group', this.handleDragToGroup);
```

新增方法 `handleDragToGroup`：
```javascript
this.handleDragToGroup = function(e){
  var detail = e.detail;
  var cg = window.__customGroups.load();
  var cmdKey = window.__customGroups.getCmdKey(detail.cmd);
  // 从源分组移除
  var fromG = cg.groups.find(function(g){ return g.id === detail.fromCid; });
  if(fromG){
    var idx = fromG.items.indexOf(cmdKey);
    if(idx > -1) fromG.items.splice(idx, 1);
  }
  // 找到目标分组的 __cgId
  var targetGroup = this.state.resultGroups.find(function(rg){ return rg.key === detail.toGroupKey; });
  if(targetGroup && targetGroup.render && targetGroup.render.__cgId){
    var toG = cg.groups.find(function(g){ return g.id === targetGroup.render.__cgId; });
    if(toG && toG.items.indexOf(cmdKey) === -1){
      toG.items.push(cmdKey);
    }
  }
  window.__customGroups.save(cg);
  this.handleCustomGroupsChange();
}.bind(this);
```

---

### Task 6: 分组管理 UI（CRUD）

**Files:**
- Modify: `dist/index.js`（`He` 组件 `render` + 新增方法）
- Modify: `dist/index.js`（追加内联样式）

- [ ] **Step 1: 在 `He` 组件标题栏插入操作按钮**

在 `He` 组件 `render` 方法中，找到非应用分组（`!o`）的标题栏渲染逻辑，在 `n.source.cmd.label` 后追加操作按钮：

```javascript
// 在 label 之后插入
n.render.__cgId ? 
  r.createElement("span", {className: "cg-actions", style: {marginLeft: "auto", display: "flex", gap: "8px"}},
    n.render.__cgId !== '__default' ?
      r.createElement("span", {onClick: this.handleRenameGroup, title: "重命名", style: {cursor:"pointer", fontSize:"12px", opacity:0.6}}, "\u270E") : null,
    n.render.__cgId !== '__default' ?
      r.createElement("span", {onClick: this.handleDeleteGroup, title: "删除", style: {cursor:"pointer", fontSize:"12px", opacity:0.6}}, "\u2715") : null,
    r.createElement("span", {onClick: this.handleCreateGroup, title: "新建分组", style: {cursor:"pointer", fontSize:"12px", opacity:0.6}}, "+")
  ) : null
```

- [ ] **Step 2: 新增 `He` 组件 CRUD 方法**

在 `He` 类 `constructor` 或方法定义区域追加：

```javascript
We(this, "handleRenameGroup", function(e){
  e && e.stopPropagation();
  var cg = window.__customGroups.load();
  var g = cg.groups.find(function(x){ return x.id === n.render.__cgId; });
  if(!g) return;
  var newName = window.prompt("重命名分组", g.name);
  if(newName && newName.trim()){
    g.name = newName.trim();
    window.__customGroups.save(cg);
  }
});
We(this, "handleDeleteGroup", function(e){
  e && e.stopPropagation();
  if(!window.confirm('删除分组"' + n.render.__cgName + '"？其中的功能将移回"已固定"。')) return;
  var cg = window.__customGroups.load();
  var idx = cg.groups.findIndex(function(x){ return x.id === n.render.__cgId; });
  if(idx > -1){
    var g = cg.groups[idx];
    var def = cg.groups.find(function(x){ return x.id === '__default'; });
    if(def){
      g.items.forEach(function(k){ if(def.items.indexOf(k) === -1) def.items.push(k); });
    }
    cg.groups.splice(idx, 1);
    window.__customGroups.save(cg);
  }
});
```

注意：`handleCreateGroup` 放在全局更合适，因为它作用于所有分组。在 `He` 中新建分组时，只需：
```javascript
We(this, "handleCreateGroup", function(e){
  e && e.stopPropagation();
  var name = window.prompt("新建分组名称");
  if(name && name.trim()){
    var cg = window.__customGroups.load();
    cg.groups.push({id: 'cg_' + Date.now().toString(36), name: name.trim(), items: []});
    window.__customGroups.save(cg);
  }
});
```

- [ ] **Step 3: 追加内联样式优化按钮显示**

在 `dist/index.js` 的 CSS 字符串区域（搜索 `.result-group-bar{`），在已有规则后追加：
```css
.cg-actions > span:hover { opacity: 1 !important; }
```

---

### Task 7: 重新打包并部署

**Files:**
- Create: `c:\Users\gfbj\.trae-cn\work\6a45d8014f4d85c1c8975cd5\repack.js`
- Modify: `C:\Users\gfbj\AppData\Local\Programs\utools\resources\app.asar`

- [ ] **Step 1: 编写重新打包脚本**

创建 `repack.js`：
```javascript
const asar = require('asar');
const fs = require('fs');

const srcDir = 'c:/Users/gfbj/.trae-cn/work/6a45d8014f4d85c1c8975cd5/utools_extracted';
const outAsar = 'c:/Users/gfbj/.trae-cn/work/6a45d8014f4d85c1c8975cd5/app.asar';

asar.createPackage(srcDir, outAsar).then(() => {
  console.log('Packed to', outAsar);
}).catch(err => {
  console.error('Pack failed', err);
});
```

- [ ] **Step 2: 执行打包**

Run: `node repack.js`
Expected: 输出 `Packed to .../app.asar`

- [ ] **Step 3: 备份并替换原文件**

Run: 
```powershell
Copy-Item 'C:\Users\gfbj\AppData\Local\Programs\utools\resources\app.asar' 'C:\Users\gfbj\AppData\Local\Programs\utools\resources\app.asar.bak'
Copy-Item 'c:\Users\gfbj\.trae-cn\work\6a45d8014f4d85c1c8975cd5\app.asar' 'C:\Users\gfbj\AppData\Local\Programs\utools\resources\app.asar'
```

- [ ] **Step 4: 重启 uTools 验证**

Expected: 
- 主界面"已固定"区域正常显示
- 可点击分组标题栏旁的 `+` 新建分组
- 新建分组后可将功能从"已固定"拖拽至新分组
- 刷新或重启后分组状态保持

---

## Assumptions & Decisions

1. **Storage: localStorage over LevelDB/JSON file**
   - 理由: uTools renderer 进程已使用 localStorage 存储 `recentcmdlog`，证明该 API 可用且稳定。LevelDB 无暴露接口，Node fs 需确认 integration 状态。localStorage 5MB 上限对分组配置绰绰有余。

2. **Patch approach over fork**
   - 理由: uTools 是闭源商业软件，无法 fork 源码。只能对打包后的 `dist/index.js` 进行字符串级手术式修改。

3. **Backward compatibility: default group `__default`**
   - 理由: 首次运行时配置为空，所有 menus 归入 `__default`（显示名"已固定"），视觉与行为完全等同于原版。用户显式创建新分组后才出现差异。

4. **Drag-to-group via DOM detection**
   - 理由: `je` 组件的拖拽基于 `86px` 网格坐标计算，无法直接跨容器。利用 `document.elementFromPoint` 检测目标分组容器是改动最小的方案。降级方案为右键菜单移动，但需修改主进程代码，不可行。

5. **Preserve `sortMainCmdMenus` call**
   - 理由: 该 API 是 uTools 原生排序持久化通道。即使我们使用 localStorage 管理分组，仍需调用它以维持与 uTools 设置页的兼容性。

---

## Verification Steps

### 功能验证清单

| # | 验证项 | 操作步骤 | 预期结果 |
|---|--------|----------|----------|
| 1 | 默认兼容 | 清除 localStorage 中 `utools_custom_groups_v1`，重启 uTools | 界面与原版完全一致，"已固定"显示所有功能 |
| 2 | 新建分组 | 点击任意分组标题栏旁的 `+`，输入"开发工具" | 出现新的空分组"开发工具" |
| 3 | 跨组拖拽 | 将"Cursor"从"已固定"拖拽到"开发工具" | "Cursor"从源分组消失，出现在"开发工具"中 |
| 4 | 同组排序 | 在"开发工具"内拖拽两个功能交换位置 | 位置交换，重启后保持新顺序 |
| 5 | 重命名 | 点击"开发工具"旁的 `✎`，输入"Coding" | 分组标题变为"Coding" |
| 6 | 删除分组 | 点击"Coding"旁的 `✕`，确认删除 | 分组消失，其中功能回到"已固定" |
| 7 | 持久化 | 重启 uTools | 所有分组结构、功能归属、排序保持 |
| 8 | 新插件兜底 | 安装新插件并固定到主界面 | 新功能自动出现在"已固定"（`__default`） |

### 回归验证

- [ ] 搜索功能正常工作（`recent` / `store` 分组不受影响）
- [ ] uTools 设置页中的"固定到主界面/取消固定"功能正常
- [ ] 插件应用内部推送结果（`window.services.listenFromPluginPush`）正常显示

---

## Risk & Mitigation

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| uTools 自动更新覆盖修改 | 高 | 每次更新后需重新打 patch；可编写自动化 patch 脚本 |
| 打包后变量名变化导致定位失败 | 中 | 使用特征字符串（如 `"最近使用"` / `"已固定"` / `"result-panel-group"`）而非变量名定位 |
| localStorage 被用户手动清除 | 低 | 配置丢失后自动回退到默认状态，功能仍可用 |
| 跨分组拖拽 DOM 检测在特殊布局下失效 | 低 | 拖拽时若未检测到目标分组，行为降级为取消拖拽（无数据变更） |
