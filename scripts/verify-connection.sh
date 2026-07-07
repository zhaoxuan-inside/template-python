#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." &>/dev/null && pwd)

info() { echo -e "\033[1;34m[INFO]\033[0m $*"; }
success() { echo -e "\033[1;32m[OK]\033[0m $*"; }
fail() { echo -e "\033[1;31m[FAIL]\033[0m $*"; }

info "=== 中间件连接验证 ==="

if [ -f "$PROJECT_ROOT/.env" ]; then
    info "加载环境变量..."
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
else
    info ".env 文件不存在，跳过验证"
    exit 0
fi

if [ -n "$DATABASE_URL" ]; then
    info "验证 PostgreSQL 连接..."
    if uv run python -c "import psycopg; psycopg.connect('$DATABASE_URL'); print('OK')" &>/dev/null; then
        success "PostgreSQL 连接成功"
    else
        fail "PostgreSQL 连接失败"
    fi
else
    info "未配置 DATABASE_URL，跳过 PostgreSQL 验证"
fi

if [ -n "$REDIS_URL" ]; then
    info "验证 Redis 连接..."
    if uv run python -c "import redis; redis.from_url('$REDIS_URL').ping(); print('OK')" &>/dev/null; then
        success "Redis 连接成功"
    else
        fail "Redis 连接失败"
    fi
else
    info "未配置 REDIS_URL，跳过 Redis 验证"
fi

info "=== 连接验证完成 ==="