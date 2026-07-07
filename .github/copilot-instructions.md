# GitHub Copilot 团队规范

## 技术栈约束

- **Python**: 3.12+
- **Web 框架**: FastAPI
- **ORM**: SQLAlchemy 2.0 (异步模式)
- **包管理**: UV (替代 pip/poetry)
- **代码检查**: Ruff
- **代码格式化**: Ruff
- **类型检查**: Basedpyright (strict 模式)
- **日志**: structlog
- **测试**: pytest

## 安全规则

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

## 代码风格

- 缩进: 4 空格
- 行宽: 120 字符
- 引号: 双引号
- 导入顺序: 标准库 → 第三方库 → 本地库
- 文档字符串: Google 风格

## AI 生成代码质量检查清单

1. ✅ 通过 Ruff 检查 (`uv run ruff check`)
2. ✅ 通过 Ruff 格式化 (`uv run ruff format`)
3. ✅ 通过 Basedpyright 类型检查 (`uv run basedpyright`)
4. ✅ 所有数据库操作使用异步模式
5. ✅ 使用 structlog 而非 print/logging
6. ✅ 无硬编码密钥/密码
7. ✅ 包含单元测试
8. ✅ 测试覆盖率 ≥ 80%