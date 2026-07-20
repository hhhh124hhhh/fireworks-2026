#!/bin/bash

# 优化验证脚本
# 验证 GLM-5 优化的关键点

echo "==================================="
echo "优化验证 - GLM-5 主页优化"
echo "==================================="
echo ""

# 检查文件是否存在
echo "1. 检查文件是否存在..."
if [ -f "index.html" ]; then
    echo "✅ index.html 存在"
else
    echo "❌ index.html 不存在"
fi

if [ -f "css/common.css" ]; then
    echo "✅ css/common.css 存在"
else
    echo "❌ css/common.css 不存在"
fi

if [ -f "OPTIMIZATION-REPORT-GLM5.md" ]; then
    echo "✅ OPTIMIZATION-REPORT-GLM5.md 存在"
else
    echo "❌ OPTIMIZATION-REPORT-GLM5.md 不存在"
fi

echo ""
echo "2. 验证性能优化..."
# 检查 Google Fonts 优化
if grep -q "display=swap" index.html; then
    echo "✅ Google Fonts display=swap 已启用"
else
    echo "❌ Google Fonts display=swap 未找到"
fi

# 检查字体权重减少
if grep -q "wght@400;500;600" index.html; then
    echo "✅ 字体权重已优化（减少到核心权重）"
else
    echo "⚠️ 字体权重优化未确认"
fi

# 检查回退字体链
if grep -q "'Georgia', serif" css/common.css; then
    echo "✅ 回退字体链已设置"
else
    echo "⚠️ 回退字体链未确认"
fi

echo ""
echo "3. 验证代码质量..."
# 检查 CSS 分离
if grep -q '<link rel="stylesheet" href="css/common.css">' index.html; then
    echo "✅ common.css 已正确引用"
else
    echo "❌ common.css 引用未找到"
fi

# 检查 CSS 变量定义
if grep -q ":root" css/common.css; then
    echo "✅ CSS 变量已定义"
else
    echo "⚠️ CSS 变量未确认"
fi

echo ""
echo "4. 验证响应式设计..."
# 检查 clamp() 函数
if grep -q "clamp(" css/common.css; then
    echo "✅ 流体间距已使用 clamp() 函数"
else
    echo "❌ clamp() 函数未找到"
fi

# 检查触摸目标
if grep -q "touch-target" css/common.css; then
    echo "✅ 触摸目标已优化"
else
    echo "⚠️ 触摸目标优化未确认"
fi

# 检查容器查询
if grep -q "container-type" css/common.css || grep -q "container-type" index.html; then
    echo "✅ 容器查询已使用"
else
    echo "⚠️ 容器查询未确认"
fi

# 检查移动端菜单
if grep -q "mobile-menu-toggle" index.html; then
    echo "✅ 移动端菜单已添加"
else
    echo "❌ 移动端菜单未找到"
fi

echo ""
echo "5. 验证可访问性..."
# 检查 ARIA 标签
if grep -q 'role="navigation"' index.html; then
    echo "✅ ARIA 标签已添加"
else
    echo "❌ ARIA 标签未找到"
fi

# 检查跳过导航
if grep -q "skip-to-content" index.html; then
    echo "✅ 跳过导航链接已添加"
else
    echo "❌ 跳过导航链接未找到"
fi

# 检查焦点样式
if grep -q ":focus-visible" css/common.css; then
    echo "✅ 焦点可见性已设置"
else
    echo "⚠️ 焦点可见性未确认"
fi

# 检查减少动画
if grep -q "prefers-reduced-motion" css/common.css; then
    echo "✅ 减少动画支持已添加"
else
    echo "⚠️ 减少动画支持未确认"
fi

echo ""
echo "6. 验证 SEO 优化..."
# 检查基础 SEO 标签
if grep -q "name=\"keywords\"" index.html && grep -q "name=\"author\"" index.html; then
    echo "✅ 基础 SEO 标签已完善"
else
    echo "⚠️ 基础 SEO 标签未确认"
fi

# 检查 Open Graph
if grep -q "og:title" index.html && grep -q "og:description" index.html; then
    echo "✅ Open Graph 标签已添加"
else
    echo "❌ Open Graph 标签未找到"
fi

# 检查 Twitter Card
if grep -q "twitter:card" index.html && grep -q "twitter:title" index.html; then
    echo "✅ Twitter Card 标签已添加"
else
    echo "❌ Twitter Card 标签未找到"
fi

# 检查结构化数据
if grep -q "application/ld+json" index.html; then
    echo "✅ 结构化数据（JSON-LD）已添加"
else
    echo "❌ 结构化数据未找到"
fi

echo ""
echo "7. 文件大小统计..."
index_size=$(du -h index.html | cut -f1)
css_size=$(du -h css/common.css | cut -f1)
report_size=$(du -h OPTIMIZATION-REPORT-GLM5.md | cut -f1)

echo "index.html: $index_size"
echo "css/common.css: $css_size"
echo "OPTIMIZATION-REPORT-GLM5.md: $report_size"

echo ""
echo "==================================="
echo "优化验证完成"
echo "==================================="
