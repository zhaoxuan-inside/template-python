#!/usr/bin/env bash
set -e

echo "=== 初始化开发环境 ==="

if ! command -v uv &> /dev/null; then
    echo "安装 UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env"
fi

if grep -q Microsoft /proc/version; then
    export UV_LINK_MODE=copy
fi

echo "创建虚拟环境..."
uv sync

echo "安装 Pre-commit 钩子..."
uv run pre-commit install

echo "配置 VSCode 团队设置..."
mkdir -p .vscode
cp -n configs/vscode/settings.json .vscode/settings.json

echo "复制环境变量模板..."
cp -n .env.example .env

echo "=== 环境初始化完成 ==="
echo ""
echo "下一步："
echo "1. 编辑 .env 文件配置数据库连接"
echo "2. 运行 ./scripts/verify-connection.sh 验证连接"
echo "3. 运行 uv run uvicorn src.app.main:app --reload 启动服务"
