#!/bin/bash

echo "🔮 算命机器人 - 本地启动脚本"
echo "================================"

if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env配置文件"
    echo "📝 正在从.env.example创建.env文件..."
    cp .env.example .env
    echo "✅ 已创建.env文件，请编辑该文件配置您的API密钥"
    echo ""
    echo "请按以下步骤操作："
    echo "1. 打开.env文件"
    echo "2. 将LLM_API_KEY=your-api-key-here替换为您的实际API密钥"
    echo "3. 根据需要修改LLM_BASE_URL和LLM_MODEL"
    echo "4. 重新运行此脚本"
    echo ""
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "🔧 激活虚拟环境..."
source venv/bin/activate

echo "📥 安装依赖包..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "🚀 启动服务..."
echo ""
python app.py
