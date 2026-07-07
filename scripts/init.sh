#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." &>/dev/null && pwd)

info() { echo -e "\033[1;34m[INFO]\033[0m $*"; }
success() { echo -e "\033[1;32m[OK]\033[0m $*"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $*"; exit 1; }

info "=== Python3 项目初始化脚本 ==="
info "项目根目录: $PROJECT_ROOT"

if command -v uv &>/dev/null; then
    info "UV 已安装，版本: $(uv --version)"
else
    info "正在安装 UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    if [ -f "$HOME/.cargo/bin/uv" ]; then
        export PATH="$HOME/.cargo/bin:$PATH"
    elif [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

info "检测操作系统和文件系统..."
if grep -q Microsoft /proc/version; then
    info "检测到 WSL 环境，启用 UV_LINK_MODE=copy"
    export UV_LINK_MODE=copy
fi

info "创建虚拟环境..."
uv venv --python 3.12

info "安装项目依赖..."
uv sync

info "安装 pre-commit 钩子..."
uv run pre-commit install

info "配置 VSCode 团队设置..."
mkdir -p "$PROJECT_ROOT/.vscode"
if [ -d "$PROJECT_ROOT/configs/vscode" ]; then
    cp "$PROJECT_ROOT/configs/vscode/"* "$PROJECT_ROOT/.vscode/"
    success "VSCode 配置已复制"
else
    info "VSCode 配置目录不存在，跳过"
fi

if [ -f "$PROJECT_ROOT/.env.development.template" ]; then
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        info "复制环境变量模板..."
        cp "$PROJECT_ROOT/.env.development.template" "$PROJECT_ROOT/.env"
        info "请编辑 .env 文件配置中间件连接信息"
    else
        info ".env 文件已存在，跳过复制"
    fi
fi

info "运行连接验证..."
if [ -f "$PROJECT_ROOT/scripts/verify-connection.sh" ]; then
    chmod +x "$PROJECT_ROOT/scripts/verify-connection.sh"
    "$PROJECT_ROOT/scripts/verify-connection.sh" || info "连接验证未通过，请检查 .env 配置"
else
    info "连接验证脚本不存在，跳过"
fi

success "=== 初始化完成 ==="
echo ""
info "快速开始:"
echo "  1. 激活虚拟环境: source .venv/bin/activate"
echo "  2. 启动开发服务器: uv run uvicorn src.${PROJECT_NAME:-app}.main:app --reload"
echo "  3. 运行测试: uv run pytest"
echo "  4. 代码检查: uv run ruff check src"
echo "  5. 代码格式化: uv run ruff format src"