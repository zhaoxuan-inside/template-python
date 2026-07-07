# Python3 开发团队工程方案

## 目录

1. [核心技术选型](#1-核心技术选型)
2. [项目模板机制](#2-项目模板机制)
3. [AI 代码生成治理](#3-ai-代码生成治理)
4. [新人 Onboarding 流程](#4-新人-onboarding-流程)
5. [跨平台与一致性保障](#5-跨平台与一致性保障)
6. [中间件管理策略](#6-中间件管理策略)
7. [代码自动格式化](#7-代码自动格式化)
8. [CI/CD 流水线](#8-cicd-流水线)
9. [落地执行清单](#9-落地执行清单)
10. [快速命令索引](#10-快速命令索引)

---

## 1. 核心技术选型

### 1.1 技术栈总览

| 领域 | 选型 | 版本 | 说明 |
|------|------|------|------|
| **Python** | CPython | 3.12+ | 运行环境 |
| **包管理** | UV | latest | 统一包管理与虚拟环境工具 |
| **代码检查** | Ruff | 0.5.x | 代码检查 + 格式化一体化 |
| **类型检查** | Basedpyright | latest | CI 严格模式类型检查 |
| **IDE 类型提示** | Pylance | latest | 实时类型提示 |
| **Web 框架** | FastAPI | 0.115+ | 现代 Web 框架 |
| **ORM** | SQLAlchemy | 2.0+ | 异步模式 |
| **配置管理** | Pydantic Settings | 2.5+ | 环境变量配置 |
| **测试框架** | pytest | 8.3+ | 单元测试 |
| **日志** | structlog | 24.0+ | 结构化日志 |
| **可观测性** | OpenTelemetry | latest | 分布式追踪 |

### 1.2 架构决策

**为什么选择 UV 而非 pip/poetry/pyenv？**

- **速度**: UV 比 pip 快 10-100 倍
- **确定性**: 锁文件保证依赖版本一致
- **一体化**: 虚拟环境管理 + 包管理 + 依赖解析
- **跨平台**: 原生支持 Windows/macOS/Linux

**为什么选择 Ruff？**

- **一体化**: 代码检查 + 格式化，无需 black+flake8 组合
- **速度**: 比 flake8 快 10-100 倍
- **配置简单**: 单文件配置
- **修复能力**: 自动修复常见问题

**为什么选择 SQLAlchemy 2.0 异步模式？**

- **性能**: 异步 IO 提升并发能力
- **现代 API**: 新的声明式 API
- **类型安全**: 完整的类型提示

---

## 2. 项目模板机制

### 2.1 目录结构（DDD 聚合优先）

```
src/app/
├── domain/                              # 领域层（业务核心）
│   ├── shared/                          # 共享内核
│   │   ├── entity.py                    # 实体基类
│   │   ├── value_object.py              # 值对象基类
│   │   └── event.py                     # 领域事件基类
│   └── example/                         # Example 聚合
│       ├── entities/                    # 实体
│       ├── value_objects/               # 值对象
│       ├── repositories/                # 仓库接口
│       ├── services/                    # 领域服务
│       ├── exceptions/                  # 领域异常
│       └── events/                      # 领域事件
├── application/                         # 应用层（用例编排）
│   ├── unit_of_work.py                  # 工作单元接口
│   └── example/                         # Example 聚合的应用服务
│       ├── commands/                    # 命令（写操作）
│       ├── queries/                     # 查询（读操作）
│       ├── use_cases/                   # 用例
│       └── dtos/                        # 数据传输对象
├── infrastructure/                      # 基础设施层（技术实现）
│   ├── config/                          # 配置
│   ├── logging/                         # 日志配置
│   ├── database/                        # 数据库
│   │   ├── core.py                      # SQLAlchemy 核心配置
│   │   ├── models/                      # ORM 模型
│   │   └── repositories/                # 仓库实现
│   └── external_services/               # 外部服务
└── interface/                           # 接口层（用户交互）
    ├── cli/                             # 命令行接口
    └── api/                             # HTTP API
        └── v1/
            ├── example/                 # Example 聚合控制器
            ├── health/                  # 健康检查
            └── router.py                # 路由聚合

migrations/                              # 数据库迁移（项目根目录）
tests/                                   # 测试目录
scripts/                                 # 脚本目录
configs/vscode/                          # VSCode 团队配置
.env.example                             # 环境变量模板
pyproject.toml                           # 项目配置
```

### 2.2 核心代码示例

#### 2.2.1 应用入口 (`main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.infrastructure.config.settings import settings
from app.infrastructure.logging.config import configure_logging
from app.interface.api.v1.router import router as v1_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Template project for FastAPI with DDD",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.app_name, "version": "1.0.0"}


if settings.app_env != "development":
    FastAPIInstrumentor.instrument_app(app)
```

#### 2.2.2 配置管理 (`infrastructure/config/settings.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "app"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/app"
    redis_url: str = "redis://localhost:6379/0"

    kafka_bootstrap_servers: str | None = None

    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None

    log_level: str = "INFO"
    log_format: str = "json"

    otel_traces_exporter: str = "console"
    otel_metrics_exporter: str = "console"


settings = Settings()
```

#### 2.2.3 实体定义 (`domain/example/entities/example.py`)

```python
from dataclasses import dataclass
from typing import Optional

from app.domain.shared.entity import Entity


@dataclass
class Example(Entity):
    id: int
    name: str
    description: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.name:
            raise ValueError("Name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Name cannot exceed 255 characters")
```

#### 2.2.4 数据库核心配置 (`infrastructure/database/core.py`)

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.infrastructure.config.settings import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

### 2.3 配置即代码

**pyproject.toml**:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "app"
version = "0.1.0"
description = "Python3 DDD FastAPI project template"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "sqlalchemy[asyncio]>=2.0.30",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "structlog>=24.0.0",
    "redis>=5.0.0",
    "httpx>=0.27.0",
    "psycopg[binary]>=3.1.0",
    "alembic>=1.13.0",
    "opentelemetry-api>=1.27.0",
    "opentelemetry-sdk>=1.27.0",
    "opentelemetry-instrumentation>=0.48b0",
    "opentelemetry-instrumentation-fastapi>=0.48b0",
    "opentelemetry-semantic-conventions>=0.48b0",
]

[project.scripts]
app = "app.cli:main"

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "basedpyright",
    "pre-commit",
    "fastapi[all]",
    "aiosqlite",
]

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.format]
quote-style = "double"
line-ending = "lf"

[tool.ruff.lint]
select = ["E", "W", "F", "B", "I"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/app --cov-fail-under=80 --cov-report=term-missing"
asyncio_mode = "auto"

[tool.basedpyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

---

## 3. AI 代码生成治理

### 3.1 技术栈约束

通过 `.cursorrules` 和 `.github/copilot-instructions.md` 向 AI 工具注入团队规范：

**禁止使用**:
- `requests` → 使用 `httpx.AsyncClient`
- `print()` → 使用 `structlog.get_logger()`
- 同步数据库操作 → 使用 SQLAlchemy 异步 API
- 硬编码密钥/密码 → 使用环境变量

**强制要求**:
- 所有数据库操作必须使用异步模式
- 所有外部 API 调用必须使用 `httpx.AsyncClient`
- 所有日志必须使用 `structlog`
- 所有配置必须通过 `pydantic-settings` 从环境变量读取

### 3.2 AI 验收清单

PR 模板内嵌 AI 验收清单（8 项必查）：

1. ✅ 通过 Ruff 检查
2. ✅ 通过 Ruff 格式化
3. ✅ 通过 Basedpyright 类型检查
4. ✅ 所有数据库操作使用异步模式
5. ✅ 使用 structlog 而非 print/logging
6. ✅ 无硬编码密钥/密码
7. ✅ 包含单元测试
8. ✅ 测试覆盖率 ≥ 80%

---

## 4. 新人 Onboarding 流程

### 4.1 标准化接入 SOP

```
克隆代码 → 一键初始化 → 配置环境变量 → 验证连接 → 启动服务 → 运行测试
```

**一键初始化脚本** (`scripts/init.sh` / `scripts/init.ps1`)：

- 自动检测平台（macOS/Linux/WSL/Windows）
- 安装 UV（如未安装）
- 创建虚拟环境
- 安装依赖
- 安装 Pre-commit 钩子
- 配置 VSCode 团队设置
- 复制环境变量模板
- 运行连接验证

### 4.2 首次贡献引导

以"添加健康检查端点"为具体任务，帮助新成员熟悉开发流程：

1. 创建健康检查服务
2. 更新路由
3. 运行测试
4. 代码检查与格式化
5. 提交代码
6. 创建 PR

### 4.3 常见问题排查

覆盖 IDE、依赖、调试、类型检查、跨平台、容器等 11 类高频问题。

---

## 5. 跨平台与一致性保障

### 5.1 换行符统一

通过 `.gitattributes` 强制统一换行符为 LF：

```
* text=auto eol=lf
*.ps1 text eol=crlf
```

### 5.2 UV 链接模式

针对 WSL 与 Windows 的 NTFS 硬链接限制，初始化脚本自动启用 `UV_LINK_MODE=copy`：

```bash
# Linux/macOS/WSL
if grep -q Microsoft /proc/version; then
    export UV_LINK_MODE=copy
fi

# Windows
$env:UV_LINK_MODE = "copy"
```

### 5.3 Docker 平台可配置化

Dockerfile 通过 `ARG TARGETPLATFORM` 支持多架构构建：

```dockerfile
ARG TARGETPLATFORM=linux/amd64
FROM python:3.12-slim
```

---

## 6. 中间件管理策略

### 6.1 职责分离

**运维团队负责**:
- 中间件部署与维护
- 提供连接信息
- 监控与告警

**开发团队负责**:
- 通过环境变量连接中间件
- 编写连接验证脚本

### 6.2 连接配置

**`.env.example`**:

```env
APP_NAME=app
APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/app
REDIS_URL=redis://localhost:6379/0

KAFKA_BOOTSTRAP_SERVERS=

S3_ENDPOINT_URL=
S3_ACCESS_KEY=
S3_SECRET_KEY=

LOG_LEVEL=INFO
LOG_FORMAT=json

OTEL_TRACES_EXPORTER=console
OTEL_METRICS_EXPORTER=console
```

### 6.3 连接验证

提供跨平台连接验证脚本：

```bash
# macOS/Linux/WSL
./scripts/verify-connection.sh

# Windows PowerShell
./scripts/verify-connection.ps1
```

---

## 7. 代码自动格式化

### 7.1 VSCode 推荐插件

| 插件 | 用途 | 说明 |
|------|------|------|
| **Ruff** | 代码检查与格式化 | 替代 black + flake8 |
| **Pylance** | 类型提示 | 实时类型检查 |
| **isort** | 导入排序 | 配合 Ruff 使用 |
| **Python** | 基础支持 | Microsoft 官方插件 |
| **Jinja** | 模板高亮 | HTML 模板支持 |
| **Docker** | 容器管理 | Dockerfile 支持 |
| **Remote - WSL** | WSL 开发 | Windows 用户必备 |

### 7.2 配置详情

**VSCode settings.json**:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  }
}
```

**Pre-commit 配置** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key
      - id: pretty-format-json
        args: ["--autofix", "--no-sort-keys"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.5
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format
```

---

## 8. CI/CD 流水线

### 8.1 三阶段流水线

```
质量检查 → 测试 → 镜像构建
```

**阶段一：质量检查**
- 代码格式化检查 (`ruff format --check`)
- 代码检查 (`ruff check`)
- 类型检查 (`basedpyright`)
- 锁文件检查 (`uv lock --check`)
- 安全审计 (`uv audit`)

**阶段二：测试**
- 运行单元测试
- 覆盖率门禁（≥ 80%）

**阶段三：镜像构建**
- 构建 Docker 镜像
- 仅在 main 分支触发

### 8.2 GitHub Actions 配置

**`.github/workflows/ci.yml`**:

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality-check:
    name: Quality Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: |
            .venv
            uv.lock
          key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml', 'uv.lock') }}
          restore-keys: |
            ${{ runner.os }}-uv-

      - name: Sync dependencies
        run: uv sync

      - name: Format check
        run: uv run ruff format --check

      - name: Lint check
        run: uv run ruff check

      - name: Type check
        run: uv run basedpyright

      - name: Lock file check
        run: uv lock --check

      - name: Security audit
        run: uv audit

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: quality-check
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: |
            .venv
            uv.lock
          key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml', 'uv.lock') }}

      - name: Sync dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest --cov=src --cov-fail-under=80

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: ${{ github.repository }}:${{ github.sha }}
          build-args: TARGETPLATFORM=linux/amd64
```

---

## 9. 落地执行清单

| 交付物 | 负责人 | 状态 |
|--------|--------|------|
| 模板仓库创建 | Tech Lead | ☐ |
| AI 规范文件 | Tech Lead | ☐ |
| PR 模板 | Tech Lead | ☐ |
| 首次贡献引导 | Tech Lead | ☐ |
| 跨平台脚本 | DevOps | ☐ |
| CI 流水线 | DevOps | ☐ |
| 团队 Wiki 文档 | Tech Lead | ☐ |
| 首次培训 | Tech Lead | ☐ |
| 试点项目验证 | 全员 | ☐ |
| 全团队发布 | Tech Lead | ☐ |

### 9.1 维护策略

- 每季度回顾工具链版本
- 更新最佳实践文档
- 收集团队反馈

### 9.2 推广路径

```
试点项目验证 → 反馈微调 → 全团队发布 → 纳入新人 Onboarding 必修
```

---

## 10. 快速命令索引

### 10.1 环境管理

```bash
# 初始化环境（首次）
./scripts/init.sh          # macOS/Linux/WSL
./scripts/init.ps1         # Windows PowerShell

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux/WSL
.venv\Scripts\Activate.ps1 # Windows

# 安装依赖
uv sync

# 添加新依赖
uv add package-name

# 更新依赖
uv update package-name
```

### 10.2 开发命令

```bash
# 启动开发服务器
uv run uvicorn src.app.main:app --reload

# 验证中间件连接
./scripts/verify-connection.sh

# 运行迁移
uv run alembic upgrade head
```

### 10.3 代码质量

```bash
# 代码检查
uv run ruff check src

# 代码格式化
uv run ruff format src

# 类型检查
uv run basedpyright

# 运行测试
uv run pytest

# 测试覆盖率
uv run pytest --cov=src
```

### 10.4 Git 工作流

```bash
# 创建功能分支
git checkout -b feature/your-feature

# 提交代码
git add .
git commit -m "feat: description"
git push origin feature/your-feature

# 创建 PR → 等待 Review → 合并
```

---

## 附录

### A. 提交规范

```
type: description

body (optional)
```

类型说明：
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 代码重构
- `docs`: 文档更新
- `test`: 测试补充
- `chore`: 杂项

### B. 分支策略

| 分支 | 用途 | 保护策略 |
|------|------|----------|
| `main` | 生产分支 | 强制 PR + 代码审查 |
| `develop` | 开发分支 | 强制 PR + 代码审查 |
| `feature/*` | 功能开发 | 无 |
| `hotfix/*` | 紧急修复 | 无 |

### C. API 版本化

使用路径参数进行 API 版本化：

```
/api/v1/users
/api/v1/health
```

---

**文档版本**: 1.0  
**最后更新**: 2026-07-07  
**适用团队**: Python3 开发团队（10人）
