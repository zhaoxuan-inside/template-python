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
│   │   ├── entity.py
│   │   ├── value_object.py
│   │   └── event.py
│   └── example/                         # Example 聚合
│       ├── entities/
│       ├── value_objects/
│       ├── repositories/
│       ├── services/
│       ├── exceptions/
│       └── events/
├── application/                         # 应用层（用例编排）
│   ├── unit_of_work.py
│   └── example/
│       ├── commands/
│       ├── queries/
│       ├── use_cases/
│       └── dtos/
├── infrastructure/                      # 基础设施层（技术实现）
│   ├── config/
│   ├── logging/
│   ├── database/
│   │   ├── core.py
│   │   ├── models/
│   │   └── repositories/
│   └── external_services/
└── interface/                           # 接口层（用户交互）
    ├── cli/
    └── api/v1/
        ├── example/
        ├── health/
        └── router.py

migrations/                              # 数据库迁移
tests/                                   # 测试目录
scripts/                                 # 部署脚本
configs/vscode/                          # VSCode 团队配置
.env.example                             # 环境变量模板
pyproject.toml                           # 项目配置
```

### 2.2 环境变量模板（`.env.example`）

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

### 2.3 部署脚本

**`scripts/init.sh`**（macOS/Linux/WSL）：

```bash
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
```

**`scripts/init.ps1`**（Windows PowerShell）：

```powershell
Write-Host "=== 初始化开发环境 ==="

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "安装 UV..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
}

$env:UV_LINK_MODE = "copy"

Write-Host "创建虚拟环境..."
uv sync

Write-Host "安装 Pre-commit 钩子..."
uv run pre-commit install

Write-Host "配置 VSCode 团队设置..."
New-Item -ItemType Directory -Force -Path .vscode
Copy-Item -Path configs/vscode/settings.json -Destination .vscode/settings.json -Force:$false

Write-Host "复制环境变量模板..."
Copy-Item -Path .env.example -Destination .env -Force:$false

Write-Host "=== 环境初始化完成 ==="
Write-Host ""
Write-Host "下一步："
Write-Host "1. 编辑 .env 文件配置数据库连接"
Write-Host "2. 运行 .\scripts\verify-connection.ps1 验证连接"
Write-Host "3. 运行 uv run uvicorn src.app.main:app --reload 启动服务"
```

### 2.4 VSCode 团队配置

**`configs/vscode/settings.json`**：

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    },
    "editor.rulers": [120],
    "editor.wordWrapColumn": 120
  },
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.diagnosticMode": "workspace",
  "python.analysis.autoImportCompletions": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["--cov=src", "--cov-fail-under=80"],
  "prettier.enable": false,
  "editor.defaultFormatter": "charliermarsh.ruff"
}
```

**`configs/vscode/extensions.json`**：

```json
{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.vscode-pylance",
    "ms-python.python",
    "ms-python.isort",
    "dotjoshjohnson.xml",
    "donjayamanne.githistory",
    "ms-azuretools.vscode-docker",
    "redhat.vscode-yaml"
  ]
}
```

---

## 3. AI 代码生成治理

### 3.1 规范提示词

#### `.cursorrules`（Cursor IDE 规则）

```
# Python 技术栈约束
- 禁止使用 requests，必须使用 httpx.AsyncClient
- 禁止使用 print()，必须使用 structlog.get_logger()
- 禁止使用同步 SQLAlchemy API，必须使用 async_session
- 禁止硬编码密钥/密码，必须通过环境变量读取

# FastAPI 规范
- 路由函数必须使用 async def
- 请求参数使用 Pydantic BaseModel
- 异常处理使用 FastAPI HTTPException
- 数据库会话使用 Depends(get_db)

# DDD 架构约束
- 领域实体放在 src/app/domain/*/entities/
- 仓库接口放在 src/app/domain/*/repositories/
- 领域服务放在 src/app/domain/*/services/
- 应用用例放在 src/app/application/*/use_cases/
- 控制器放在 src/app/interface/api/v1/*/

# 代码风格
- 行长度限制 120 字符
- 使用双引号而非单引号
- 导入按顺序排列：标准库 → 第三方库 → 项目内部
- 函数和方法使用 snake_case
- 类使用 PascalCase
```

#### `.github/copilot-instructions.md`（GitHub Copilot 指令）

```markdown
# Python3 团队代码规范

## 技术栈

- **Web 框架**: FastAPI 0.115+
- **ORM**: SQLAlchemy 2.0+ (异步模式)
- **配置**: Pydantic Settings 2.5+
- **日志**: structlog 24.0+
- **HTTP 客户端**: httpx.AsyncClient
- **代码检查**: Ruff
- **类型检查**: Basedpyright (strict mode)
- **测试**: pytest + pytest-asyncio

## 架构模式

项目采用 DDD（领域驱动设计）架构，分为四层：

1. **Domain Layer** (`src/app/domain/`)
   - 实体（entities）、值对象（value_objects）
   - 仓库接口（repositories）、领域服务（services）
   - 领域事件（events）、领域异常（exceptions）

2. **Application Layer** (`src/app/application/`)
   - 命令（commands）、查询（queries）
   - 用例（use_cases）、数据传输对象（dtos）
   - 工作单元（unit_of_work）

3. **Infrastructure Layer** (`src/app/infrastructure/`)
   - 数据库实现（database）
   - 外部服务（external_services）
   - 配置（config）、日志（logging）

4. **Interface Layer** (`src/app/interface/`)
   - API 控制器（api）
   - 命令行接口（cli）

## 代码规范

### 1. 异步优先

所有数据库操作和外部 API 调用必须使用异步模式：

```python
# 正确
async def get_user(self, user_id: int) -> User:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await self._session.execute(stmt)
    return result.scalar_one_or_none()

# 错误
def get_user(self, user_id: int) -> User:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = self._session.execute(stmt)  # 同步调用
```

### 2. 日志规范

使用 structlog 而非 print 或 logging：

```python
# 正确
import structlog

logger = structlog.get_logger()
logger.info("User created", user_id=user_id)

# 错误
print(f"User created: {user_id}")  # 禁止
logging.info(f"User created: {user_id}")  # 禁止
```

### 3. 配置管理

通过 Pydantic Settings 从环境变量读取配置：

```python
# 正确
from app.infrastructure.config.settings import settings

database_url = settings.database_url

# 错误
DATABASE_URL = "postgresql://user:pass@localhost:5432/app"  # 硬编码
```

### 4. HTTP 客户端

使用 httpx.AsyncClient：

```python
# 正确
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# 错误
import requests
response = requests.get(url)  # 禁止
```

### 5. 异常处理

定义领域异常并在接口层转换为 HTTPException：

```python
# 领域层
class UserNotFoundError(Exception):
    pass

# 接口层
try:
    user = await service.get_user(user_id)
except UserNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e)) from e
```

### 6. 类型提示

所有函数必须包含完整的类型提示：

```python
# 正确
async def create_user(self, name: str, email: str) -> User:
    pass

# 错误
async def create_user(self, name, email):  # 缺少类型提示
    pass
```

### 7. 测试规范

为所有新增功能编写单元测试，覆盖率 ≥ 80%：

```python
@pytest.mark.asyncio
async def test_create_user():
    async with AsyncSessionLocal() as session:
        repository = UserRepositoryImpl(session)
        service = UserService(repository)
        user = await service.create_user("test", "test@example.com")
        assert user.name == "test"
```

## 禁止事项

1. ❌ 禁止使用同步数据库操作
2. ❌ 禁止使用 print() 进行日志记录
3. ❌ 禁止硬编码密钥、密码、URL
4. ❌ 禁止使用 requests 库
5. ❌ 禁止使用旧式类（class Foo:）
6. ❌ 禁止使用全局变量存储配置
7. ❌ 禁止在领域层引入外部依赖
8. ❌ 禁止提交未通过 Ruff 检查的代码

## 最佳实践

1. ✅ 使用 dataclass 定义领域实体
2. ✅ 使用 Pydantic BaseModel 定义 DTO
3. ✅ 使用 Annotated[Type, Depends(...)] 进行依赖注入
4. ✅ 在异常重新抛出时使用 `raise ... from e`
5. ✅ 数据库会话通过依赖注入管理
6. ✅ 事务在应用层或接口层管理
7. ✅ 使用 Alembic 进行数据库迁移
8. ✅ 在 CI 中运行类型检查和测试
```

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

**步骤详解：**

#### 步骤一：克隆代码

```bash
# macOS/Linux/WSL
git clone git@github.com:your-org/your-project.git
cd your-project

# Windows
git clone git@github.com:your-org/your-project.git
cd your-project
```

#### 步骤二：一键初始化

```bash
# macOS/Linux/WSL
./scripts/init.sh

# Windows PowerShell
.\scripts\init.ps1
```

**脚本执行内容：**
1. 检测并安装 UV（如未安装）
2. 创建虚拟环境
3. 安装依赖（`uv sync`）
4. 安装 Pre-commit 钩子
5. 配置 VSCode 团队设置（复制 `configs/vscode/settings.json`）
6. 复制环境变量模板（`.env.example` → `.env`）

#### 步骤三：配置环境变量

编辑 `.env` 文件，配置数据库连接等信息：

```env
APP_NAME=smart-chat
APP_ENV=development
APP_DEBUG=true

DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/app
REDIS_URL=redis://localhost:6379/0
```

#### 步骤四：验证连接

```bash
# macOS/Linux/WSL
./scripts/verify-connection.sh

# Windows PowerShell
.\scripts\verify-connection.ps1
```

#### 步骤五：启动服务

```bash
uv run uvicorn src.app.main:app --reload
```

访问 `http://localhost:8000/docs` 查看 API 文档。

#### 步骤六：运行测试

```bash
uv run pytest
```

---

### 4.2 首次贡献引导

以"添加健康检查端点"为具体任务，帮助新成员熟悉开发流程：

#### 步骤 1：创建功能分支

```bash
git checkout -b feature/add-health-check
```

#### 步骤 2：创建健康检查服务

在 `src/app/interface/api/v1/health/health_controller.py` 中添加新的健康检查端点：

```python
@router.get("/detailed")
async def detailed_health_check(db: Annotated[AsyncSession, Depends(get_db)]):
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "1.0.0",
        "database": "connected"
    }
```

#### 步骤 3：更新路由

确认路由已在 `src/app/interface/api/v1/router.py` 中注册：

```python
router.include_router(health_router)
```

#### 步骤 4：运行测试

```bash
uv run pytest tests/test_health.py
```

#### 步骤 5：代码检查与格式化

```bash
uv run ruff check src
uv run ruff format src
```

#### 步骤 6：提交代码

```bash
git add .
git commit -m "feat: add detailed health check endpoint"
git push origin feature/add-health-check
```

#### 步骤 7：创建 PR

在 GitHub 上创建 Pull Request：
1. 选择 `feature/add-health-check` → `develop`
2. 填写 PR 标题和描述
3. 添加至少 1 位 reviewer
4. 等待 CI 通过和代码审查

---

### 4.3 常见问题排查

#### Q1：VSCode 无法识别虚拟环境

**现象：** VSCode 提示找不到 Python 解释器

**解决方案：**
```bash
# 查看虚拟环境路径
uv venv --print-path

# 在 VSCode 中按 Ctrl+Shift+P → Python: Select Interpreter
# 选择 .venv/bin/python（Linux/macOS）或 .venv/Scripts/python.exe（Windows）
```

#### Q2：UV 安装失败（WSL）

**现象：** 在 WSL 中执行 `uv` 命令提示 command not found

**解决方案：**
```bash
# 手动添加环境变量
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Q3：Pre-commit 钩子不生效

**现象：** 提交代码时没有自动执行 Ruff 检查

**解决方案：**
```bash
# 手动安装钩子
uv run pre-commit install

# 手动运行一次检查
uv run pre-commit run --all-files
```

#### Q4：数据库连接失败

**现象：** 启动服务时报错 `OperationalError: connection failed`

**解决方案：**
1. 检查 `.env` 文件中 `DATABASE_URL` 是否正确
2. 确认数据库服务已启动
3. 确认数据库端口未被占用

#### Q5：Ruff 格式化与预期不一致

**现象：** Ruff 修改了代码格式，但不符合个人习惯

**解决方案：**
- 团队统一使用 Ruff 配置，禁止修改个人设置
- 如有格式问题，在团队会议中讨论并更新 `pyproject.toml`

#### Q6：类型检查失败

**现象：** `uv run basedpyright` 报错 `reportUnknownMemberType`

**解决方案：**
```bash
# 安装缺失的类型提示
uv add types-requests  # 示例：安装 requests 类型
```

#### Q7：WSL 中文件权限问题

**现象：** 脚本无法执行，提示 `Permission denied`

**解决方案：**
```bash
chmod +x scripts/*.sh
```

#### Q8：测试覆盖率不足

**现象：** CI 报错 `Coverage failure: 75% < 80%`

**解决方案：**
```bash
# 查看覆盖率报告
uv run pytest --cov=src --cov-report=html
# 打开 htmlcov/index.html 查看未覆盖的代码
```

#### Q9：Git 换行符问题

**现象：** Windows 和 Linux 之间文件换行符不一致

**解决方案：**
- 确保 `.gitattributes` 文件存在且包含 `* text=auto eol=lf`
- 在 VSCode 设置中启用 `files.eol: \n`

#### Q10：Docker 构建失败

**现象：** CI 中 Docker 构建报错

**解决方案：**
- 检查 `Dockerfile` 是否正确
- 确认基础镜像版本兼容
- 检查构建参数是否正确传递

#### Q11：环境变量不生效

**现象：** 启动服务时使用的是默认配置而非 `.env` 文件

**解决方案：**
```bash
# 确认 .env 文件存在于项目根目录
ls -la .env

# 确认 pydantic-settings 已安装
uv run pip show pydantic-settings
```

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

通过 `.env.example` 提供连接模板（见第 2.2 节）。

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
