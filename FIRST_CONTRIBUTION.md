# 首次贡献指南

欢迎加入团队！这份指南将帮助你完成第一次代码贡献。

## 任务：添加健康检查端点

我们将为项目添加一个详细的健康检查端点，展示如何与数据库和 Redis 进行交互。

### 步骤

1. **克隆代码**
   ```bash
   git clone https://github.com/your-org/app.git
   cd app
   ```

2. **初始化环境**
   ```bash
   # macOS/Linux/WSL
   ./scripts/init.sh

   # Windows PowerShell
   ./scripts/init.ps1
   ```

3. **激活虚拟环境**
   ```bash
   # macOS/Linux/WSL
   source .venv/bin/activate

   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

4. **创建健康检查服务**

   创建 `src/app/services/health.py`：
   ```python
   from redis import asyncio as aioredis
   from sqlalchemy.ext.asyncio import AsyncSession

   from app.config import settings

   async def check_database(db: AsyncSession) -> bool:
       try:
           await db.execute("SELECT 1")
           return True
       except Exception:
           return False

   async def check_redis() -> bool:
       try:
           redis = aioredis.from_url(settings.redis_url)
           await redis.ping()
           await redis.close()
           return True
       except Exception:
           return False

   async def get_health_status(db: AsyncSession) -> dict:
       db_status = await check_database(db)
       redis_status = await check_redis()

       return {
           "status": "ok" if all([db_status, redis_status]) else "degraded",
           "checks": {
               "database": db_status,
               "redis": redis_status,
           },
       }
   ```

5. **更新健康检查路由**

   更新 `src/app/api/v1/health.py`：
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.ext.asyncio import AsyncSession

   from app.database import get_db
   from app.services.health import get_health_status

   router = APIRouter(prefix="/health")

   @router.get("")
   async def health_check(db: AsyncSession = Depends(get_db)):
       return await get_health_status(db)
   ```

6. **运行测试**
   ```bash
   uv run pytest
   ```

7. **代码检查与格式化**
   ```bash
   uv run ruff check src
   uv run ruff format src
   ```

8. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add detailed health check endpoint"
   git push origin feature/health-check
   ```

9. **创建 Pull Request**

   在 GitHub 上创建 PR，参考 `.github/pull_request_template.md` 填写内容。

## 完成后的端点

完成后，你可以访问：
- `GET /api/v1/health` - 详细健康检查（数据库 + Redis）
- `GET /health` - 基础健康检查

## 下一步

完成首次贡献后，你可以：
1. 查看团队 Wiki 了解更多项目规范
2. 参与项目讨论，了解当前开发任务
3. 开始处理第一个正式任务