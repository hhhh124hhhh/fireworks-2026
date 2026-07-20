#!/bin/bash

echo "=========================================="
echo "阶段 1 优化验证脚本"
echo "=========================================="
echo ""

# 检查文件是否存在
echo "1. 检查文件是否存在..."
if [ -f "index.html" ]; then
    echo "✓ index.html 存在"
else
    echo "✗ index.html 不存在"
    exit 1
fi

if [ -f "css/brand-system.css" ]; then
    echo "✓ css/brand-system.css 存在"
else
    echo "✗ css/brand-system.css 不存在"
    exit 1
fi

if [ -f "BRAND-DESIGN-REPORT.md" ]; then
    echo "✓ BRAND-DESIGN-REPORT.md 存在"
else
    echo "✗ BRAND-DESIGN-REPORT.md 不存在"
    exit 1
fi

echo ""

# 检查字体更新
echo "2. 检查字体更新..."
if grep -q "Cormorant+Garamond" index.html && grep -q "DM+Sans" index.html; then
    echo "✓ 新字体已引入（Cormorant Garamond + DM Sans）"
else
    echo "✗ 新字体未正确引入"
    exit 1
fi

if grep -q "font-display: swap" css/brand-system.css; then
    echo "✓ font-display: swap 已配置"
else
    echo "✗ font-display: swap 未配置"
    exit 1
fi

if grep -q "unicode-range" css/brand-system.css; then
    echo "✓ unicode-range 已配置"
else
    echo "✗ unicode-range 未配置"
    exit 1
fi

echo ""

# 检查品牌系统 CSS
echo "3. 检查品牌系统 CSS..."
if grep -q "brand-logo" css/brand-system.css; then
    echo "✓ 品牌 Logo 样式已定义"
else
    echo "✗ 品牌 Logo 样式未定义"
    exit 1
fi

if grep -q "brand-decoration-line" css/brand-system.css; then
    echo "✓ 装饰线样式已定义"
else
    echo "✗ 装饰线样式未定义"
    exit 1
fi

if grep -q "brand-corner" css/brand-system.css; then
    echo "✓ 装饰角样式已定义"
else
    echo "✗ 装饰角样式未定义"
    exit 1
fi

if grep -q "brand-gradient-border" css/brand-system.css; then
    echo "✓ 渐变边框样式已定义"
else
    echo "✗ 渐变边框样式未定义"
    exit 1
fi

if grep -q "brand-divider" css/brand-system.css; then
    echo "✓ 分隔线样式已定义"
else
    echo "✗ 分隔线样式未定义"
    exit 1
fi

echo ""

# 检查色彩体系
echo "4. 检查色彩体系..."
if grep -q "brand-gold" css/brand-system.css && grep -q "brand-gold-light" css/brand-system.css; then
    echo "✓ 金色系统已定义"
else
    echo "✗ 金色系统未完整定义"
    exit 1
fi

if grep -q "brand-tech" css/brand-system.css; then
    echo "✓ 科技蓝已添加"
else
    echo "✗ 科技蓝未添加"
    exit 1
fi

if grep -q "gradient-gold\|gradient-brand\|gradient-tech" css/brand-system.css; then
    echo "✓ 渐变色系统已定义"
else
    echo "✗ 渐变色系统未完整定义"
    exit 1
fi

echo ""

# 检查 HTML 应用
echo "5. 检查 HTML 应用..."
if grep -q "css/brand-system.css" index.html; then
    echo "✓ brand-system.css 已引入"
else
    echo "✗ brand-system.css 未引入"
    exit 1
fi

if grep -q "brand-logo" index.html; then
    echo "✓ 品牌 Logo 已应用"
else
    echo "✗ 品牌 Logo 未应用"
    exit 1
fi

if grep -q "brand-decoration-line" index.html; then
    echo "✓ 装饰线已应用"
else
    echo "✗ 装饰线未应用"
    exit 1
fi

if grep -q "brand-corner" index.html; then
    echo "✓ 装饰角已应用"
else
    echo "✗ 装饰角未应用"
    exit 1
fi

if grep -q "brand-gradient-border" index.html; then
    echo "✓ 渐变边框已应用"
else
    echo "✗ 渐变边框未应用"
    exit 1
fi

if grep -q "brand-divider" index.html; then
    echo "✓ 分隔线已应用"
else
    echo "✗ 分隔线未应用"
    exit 1
fi

echo ""

# 检查字体加载检测
echo "6. 检查字体加载检测..."
if grep -q "document.fonts.ready" index.html; then
    echo "✓ 字体加载检测脚本已添加"
else
    echo "✗ 字体加载检测脚本未添加"
    exit 1
fi

if grep -q "font-loading\|font-loaded" index.html; then
    echo "✓ 字体加载类已使用"
else
    echo "✗ 字体加载类未使用"
    exit 1
fi

echo ""

# 检查 SVG Logo
echo "7. 检查 SVG Logo..."
if grep -q "svg.*viewBox.*40 40" index.html; then
    echo "✓ SVG Logo 已添加"
else
    echo "✗ SVG Logo 未添加"
    exit 1
fi

if grep -q "logoGradient" index.html; then
    echo "✓ Logo 渐变已定义"
else
    echo "✗ Logo 渐变未定义"
    exit 1
fi

echo ""

# 检查可访问性
echo "8. 检查可访问性..."
if grep -q 'aria-label="Jack 首页"' index.html; then
    echo "✓ Logo ARIA 标签已添加"
else
    echo "✗ Logo ARIA 标签未添加"
    exit 1
fi

if grep -q "aria-hidden" index.html; then
    echo "✓ 装饰元素 ARIA 标签已添加"
else
    echo "✗ 装饰元素 ARIA 标签未添加"
    exit 1
fi

echo ""

# 统计信息
echo "9. 文件统计..."
echo "index.html 大小: $(wc -c < index.html) 字节"
echo "css/brand-system.css 大小: $(wc -c < css/brand-system.css) 字节"
echo "BRAND-DESIGN-REPORT.md 大小: $(wc -c < BRAND-DESIGN-REPORT.md) 字节"

echo ""

# 备份文件
echo "10. 备份文件..."
if ls index.html.backup-stage1-* 1> /dev/null 2>&1; then
    echo "✓ 阶段 1 备份已创建"
    ls -lh index.html.backup-stage1-* | awk '{print "   " $9 " (" $5 ")"}'
else
    echo "⚠ 阶段 1 备份未创建"
fi

echo ""
echo "=========================================="
echo "✅ 所有检查通过！阶段 1 优化完成！"
echo "=========================================="
echo ""
echo "摘要:"
echo "  - 字体系统重构: Cormorant Garamond + DM Sans"
echo "  - 字体加载优化: font-display: swap + unicode-range"
echo "  - 品牌 Logo: SVG 图标（首字母 J + AI 电路）"
echo "  - 品牌装饰元素: 装饰线、装饰角、渐变边框、分隔线"
echo "  - 色彩体系: 完整的金色系统 + 科技蓝"
echo "  - 响应式设计: 适配所有设备"
echo "  - 可访问性优化: ARIA 标签"
echo ""
echo "下一步:"
echo "  1. 在浏览器中打开 index.html 预览效果"
echo "  2. 检查字体加载和动画过渡"
echo "  3. 验证响应式设计（调整浏览器窗口大小）"
echo "  4. 开始阶段 2: 动画与交互增强"
echo ""
