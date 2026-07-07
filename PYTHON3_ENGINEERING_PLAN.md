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

### 2.1 目录结构

```
app/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI 应用入口
│       ├── config.py            # 配置管理
│       ├── logger.py            # 日志配置
│       ├── database.py          # 数据库连接
│       ├── api/
│       │   └── v1/              # API v1 版本
│       │       ├── __init__.py
│       │       ├── router.py    # 路由注册
│       │       └── health.py    # 健康检查端点
│       └── models/              # SQLAlchemy 模型
├── tests/                       # 测试目录
├── scripts/                     # 脚本目录
├── configs/                     # 配置模板目录
│   └── vscode/                  # VSCode 团队配置
├── .env.development.template    # 环境变量模板
├── pyproject.toml               # 项目配置
├── .pre-commit-config.yaml      # Pre-commit 配置
├── .gitignore                   # Git 忽略规则
├── .gitattributes               # Git 属性配置
└── docker-compose.local.yml     # 可选本地中间件
```

### 2.2 配置即代码

所有配置文件均纳入 Git 版本管理：

- **pyproject.toml**: 项目依赖、Ruff 配置、pytest 配置、Basedpyright 配置
- **.pre-commit-config.yaml**: 代码门禁配置
- **.gitattributes**: 跨平台换行符统一
- **configs/vscode/**: VSCode 团队统一配置

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

通过 `.env.development.template` 提供连接模板：

```env
DATABASE_URL=postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}
REDIS_URL=redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}
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

**Pre-commit 配置**:
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  hooks:
    - id: ruff
      args: ["--fix"]
    - id: ruff-format
```

**CI 门禁**:
```yaml
- name: Format Check
  run: uv run ruff format --check

- name: Lint Check
  run: uv run ruff check --fix
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

配置文件：`.github/workflows/ci.yml`

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
| Docker Compose 本地配置 | DevOps | ☐ |
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

# 启动本地中间件（可选）
docker compose -f docker-compose.local.yml up

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