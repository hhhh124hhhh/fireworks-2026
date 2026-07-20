# GitHub 项目展示 HTML 修改说明

## 目标
移除 HTML 中的内联样式，让 CSS 文件完全控制样式，确保代码整洁和可维护性。

## 需要修改的位置

### 1. 移除标题和描述的内联样式

**原代码（第 1036-1038 行）：**
```html
<h3 class="subsection-title" style="margin-bottom: var(--spacing-xs); font-family: var(--font-display); font-size: 1.8rem; color: var(--text-primary);">GitHub 项目展示</h3>
<p class="subsection-description" style="margin-bottom: var(--spacing-lg); color: var(--text-secondary); font-size: 1.05rem; line-height: 1.7;">精选 3 个最受欢迎的开源项目，按 Stars 和访问数排序</p>
```

**修改为：**
```html
<h3 class="subsection-title">GitHub 项目展示</h3>
<p class="subsection-description">精选 3 个最受欢迎的开源项目，按 Stars 和访问数排序</p>
```

---

### 2. 移除排名数字的内联样式（3 处）

**原代码（第 1041、1061、1081 行）：**
```html
<div class="project-rank" style="font-size: 2.5rem;" aria-label="第1名">🥇</div>
```

**修改为：**
```html
<div class="project-rank" aria-label="第1名">🥇</div>
```

---

### 3. 移除统计数据区域的内联样式（3 处）

**原代码（第 1044-1046 行）：**
```html
<div class="project-stats" style="display: flex; gap: var(--spacing-sm); margin: var(--spacing-xs) 0;">
    <span style="color: var(--brand-gold); font-weight: 600;">⭐ 18</span>
    <span style="color: var(--text-secondary);">👁️ 261</span>
</div>
```

**修改为：**
```html
<div class="project-stats">
    <span>⭐ 18</span>
    <span>👁️ 261</span>
</div>
```

---

### 4. 移除按钮的内联样式（3 处）

**原代码（第 1052 行）：**
```html
<a href="https://github.com/hhhh124hhhh/godot-mcp" target="_blank" rel="noopener noreferrer" class="project-status" style="background: var(--brand-gold-alpha-15); color: var(--brand-gold); border: 1px solid rgba(212, 175, 55, 0.3); text-decoration: none;">查看项目 →</a>
```

**修改为：**
```html
<a href="https://github.com/hhhh124hhhh/godot-mcp" target="_blank" rel="noopener noreferrer" class="project-status">查看项目 →</a>
```

---

### 5. 移除"查看全部"按钮的内联样式和 JavaScript

**原代码（第 1112-1120 行）：**
```html
<div style="margin-top: var(--spacing-lg); text-align: center;">
    <a href="https://github.com/hhhh124hhhh?tab=repositories"
       class="cta-button"
       target="_blank"
       rel="noopener noreferrer"
       style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 1rem 2rem; background: var(--brand-gold); color: var(--bg-primary); text-decoration: none; border-radius: 12px; font-weight: 600; transition: all 0.4s var(--transition-smooth);"
       onmouseover="this.style.background='linear-gradient(135deg, #f0d67a 0%, #d4af37 100%)'; this.style.transform='translateY(-4px)'; this.style.boxShadow='var(--shadow-glow-hover)';"
       onmouseout="this.style.background='var(--brand-gold)'; this.style.transform='none'; this.style.boxShadow='none';">
       查看全部 68 个项目 →
    </a>
</div>
```

**修改为：**
```html
<div class="github-view-all">
    <a href="https://github.com/hhhh124hhhh?tab=repositories"
       class="github-view-all-button"
       target="_blank"
       rel="noopener noreferrer">
       查看全部 68 个项目 →
    </a>
</div>
```

**需要在 CSS 文件中添加以下样式：**
```css
.github-view-all {
    margin-top: var(--spacing-lg);
    text-align: center;
}

.github-view-all-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: var(--brand-gold);
    color: var(--bg-primary);
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.4s var(--transition-smooth);
}

.github-view-all-button:hover {
    background: linear-gradient(135deg, #f0d67a 0%, #d4af37 100%);
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow-hover);
}
```

---

## 修改步骤

### 方法 1：使用编辑器查找替换

1. **查找并替换标题样式**
   - 查找：`style="margin-bottom: var(--spacing-xs); font-family: var(--font-display); font-size: 1.8rem; color: var(--text-primary);"`
   - 替换为：空字符串

2. **查找并替换描述样式**
   - 查找：`style="margin-bottom: var(--spacing-lg); color: var(--text-secondary); font-size: 1.05rem; line-height: 1.7;"`
   - 替换为：空字符串

3. **查找并替换排名样式**
   - 查找：`style="font-size: 2.5rem;"`
   - 替换为：空字符串

4. **查找并替换按钮样式**
   - 查找：`style="background: var(--brand-gold-alpha-15); color: var(--brand-gold); border: 1px solid rgba(212, 175, 55, 0.3); text-decoration: none;"`
   - 替换为：空字符串

5. **替换"查看全部"按钮区域**
   - 手动修改第 1112-1120 行

### 方法 2：手动逐行修改

按照上面的"需要修改的位置"逐行修改。

---

## 验证修改

修改完成后，检查以下几点：

1. ✅ HTML 中不再有 `style="..."` 内联样式
2. ✅ 不再有 `onmouseover="..."` 和 `onmouseout="..."` JavaScript 代码
3. ✅ 页面显示效果保持一致
4. ✅ 所有交互效果正常（悬停、动画等）
5. ✅ 响应式布局在不同屏幕尺寸下正常工作

---

## 预期效果

完成修改后：

- ✅ HTML 代码更加简洁易读
- ✅ 样式完全由 CSS 控制，便于维护
- ✅ 和精选项目的视觉风格完全一致
- ✅ 3 个项目在桌面端排成一排
- ✅ 所有内容都能完整显示
- ✅ 响应式布局在各种设备上都能正常工作

---

## 额外建议

如果需要进一步优化，可以考虑：

1. **使用 CSS 变量**：将常用的颜色、间距等定义为 CSS 变量
2. **提取公共样式**：将重复的样式提取为公共类
3. **添加注释**：在 CSS 中添加清晰的注释说明每个部分的作用
4. **使用语义化标签**：确保 HTML 标签使用正确，便于无障碍访问
