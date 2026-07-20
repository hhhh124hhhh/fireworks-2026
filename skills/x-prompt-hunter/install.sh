#!/bin/bash
# AI 提示词系统 - 依赖安装脚本

set -e  # 遇到错误立即退出

echo "============================================================"
echo "AI 提示词系统 - 依赖安装"
echo "============================================================"
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python3 --version || {
    echo "错误: Python 3 未安装"
    exit 1
}
echo "✓ Python 3 已安装"
echo ""

# 检查 pip
echo "检查 pip..."
python3 -m pip --version || {
    echo "错误: pip 未安装"
    exit 1
}
echo "✓ pip 已安装"
echo ""

# 升级 pip
echo "升级 pip..."
python3 -m pip install --upgrade pip -q
echo "✓ pip 已升级"
echo ""

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境？(推荐) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    VENV_NAME="venv"
    echo "创建虚拟环境: $VENV_NAME"
    python3 -m venv $VENV_NAME

    echo "激活虚拟环境..."
    source $VENV_NAME/bin/activate

    echo "✓ 虚拟环境已创建并激活"
    echo ""
fi

# 安装依赖
echo "安装 Python 依赖包..."
echo "这可能需要几分钟时间，请耐心等待..."
echo ""

python3 -m pip install -r requirements.txt -q || {
    echo "错误: 依赖安装失败"
    exit 1
}

echo "✓ 依赖安装完成"
echo ""

# 验证关键包
echo "验证关键依赖包..."
python3 -c "
import yaml
import sentence_transformers
import requests
import anthropic
try:
    import langfuse
    print('✓ langfuse')
except ImportError:
    print('⚠ langfuse (可选，未安装)')
try:
    from github import Github
    print('✓ PyGithub')
except ImportError:
    print('⚠ PyGithub (可选，未安装)')
try:
    from datasets import load_dataset
    print('✓ datasets')
except ImportError:
    print('⚠ datasets (可选，未安装)')
" || {
    echo "错误: 依赖验证失败"
    exit 1
}

echo ""
echo "============================================================"
echo "安装完成！"
echo "============================================================"
echo ""
echo "下一步："
echo "1. 配置环境变量："
echo "   cp .env.example .env"
echo "   编辑 .env 文件，填入你的 API 密钥"
echo ""
echo "2. 运行测试："
echo "   python3 test.py"
echo ""
echo "3. 查看帮助："
echo "   python3 main.py --help"
echo ""
echo "4. 运行完整流程："
echo "   python3 main.py pipeline --query 'test' --limit 10 --evaluate-limit 5"
echo ""
echo "如需更多帮助，请查看 README.md"
echo ""
