# 新人 Onboarding 指南

欢迎加入 Python3 开发团队！这份指南将帮助你快速融入团队并开始开发工作。

## 前置准备

### 1. 安装必要工具

- **VSCode**: 团队统一 IDE
- **Git**: 版本控制工具
- **Docker**: 可选，用于本地中间件
- **Python 3.12**: 运行环境（UV 会自动管理）

### 2. 配置 VSCode

安装推荐扩展：
- Ruff (charliermarsh.ruff)
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)

## 快速开始

### 1. 克隆代码

```bash
git clone https://github.com/your-org/app.git
cd app
```

### 2. 一键初始化

```bash
# macOS/Linux/WSL
./scripts/init.sh

# Windows PowerShell
./scripts/init.ps1
```

初始化脚本会自动完成：
- 安装 UV（如未安装）
- 创建虚拟环境
- 安装依赖
- 安装 Pre-commit 钩子
- 复制环境变量模板
- 运行连接验证

### 3. 配置环境变量

编辑 `.env` 文件，填写运维团队提供的中间件连接信息：

```env
DATABASE_URL=postgresql://user:pass@dev-db:5432/app
REDIS_URL=redis://dev-redis:6379/0
```

### 4. 验证连接

```bash
# macOS/Linux/WSL
./scripts/verify-connection.sh

# Windows PowerShell
./scripts/verify-connection.ps1
```

### 5. 启动开发服务器

```bash
uv run uvicorn src.app.main:app --reload
```

访问 `http://localhost:8000/docs` 查看 API 文档。

### 6. 运行测试

```bash
uv run pytest
```

## 开发流程

### 分支策略

- `main`: 生产分支
- `develop`: 开发分支
- `feature/*`: 功能开发分支
- `hotfix/*`: 紧急修复分支

### 提交规范

```
type: description

body (optional)
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 代码重构
- `docs`: 文档更新
- `test`: 测试补充
- `chore`: 杂项

### PR 流程

1. 从 `develop` 分支创建 `feature/*` 分支
2. 开发并提交代码
3. 运行测试和代码检查
4. 创建 PR 到 `develop`
5. 等待 Code Review
6. 合并到 `develop`

## 常用命令

```bash
# 安装依赖
uv sync

# 添加新依赖
uv add package-name

# 代码检查
uv run ruff check src

# 代码格式化
uv run ruff format src

# 类型检查
uv run basedpyright

# 运行测试
uv run pytest

# 启动开发服务器
uv run uvicorn src.app.main:app --reload

# 启动本地中间件（可选）
docker compose -f docker-compose.local.yml up

# 运行连接验证
./scripts/verify-connection.sh
```

## 常见问题排查

### IDE 问题

**Q: VSCode 无法找到虚拟环境？**
A: 打开命令面板（Ctrl+Shift+P），选择 "Python: Select Interpreter"，选择 `.venv/bin/python`

**Q: Ruff 格式化不生效？**
A: 确保已安装 Ruff 扩展，并在设置中启用 `editor.formatOnSave`

### 依赖问题

**Q: UV 安装失败？**
A: 检查网络连接，或使用国内镜像：`uv config set registry https://mirrors.aliyun.com/pypi/simple/`

**Q: 依赖冲突？**
A: 删除 `uv.lock` 和 `.venv`，重新运行 `uv sync`

### 调试问题

**Q: 断点无法命中？**
A: 确保使用 "FastAPI: Development" 调试配置，并勾选 "justMyCode": false

### 类型检查

**Q: Pylance 报告错误但 CI 通过？**
A: 确保 VSCode 中 `python.analysis.typeCheckingMode` 设置为 `strict`

### 跨平台问题

**Q: Windows 上脚本无法执行？**
A: 使用 PowerShell 运行 `.ps1` 脚本，或使用 WSL

**Q: 文件换行符问题？**
A: `.gitattributes` 已配置统一换行符，确保 Git 全局配置 `core.autocrlf=false`

### 容器问题

**Q: Docker 端口冲突？**
A: 修改 `docker-compose.local.yml` 中的端口映射，或使用运维提供的共享开发环境

## 资源

- **项目文档**: `README.md`
- **API 文档**: `http://localhost:8000/docs`
- **团队 Wiki**: [链接]
- **首次贡献**: `FIRST_CONTRIBUTION.md`

## 联系我们

如有问题，请联系：
- Tech Lead: [姓名]
- DevOps: [姓名]
- Mentor: [姓名]