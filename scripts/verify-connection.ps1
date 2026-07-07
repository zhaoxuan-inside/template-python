$ErrorActionPreference = "SilentlyContinue"

$scriptPath = $MyInvocation.MyCommand.Definition
$scriptDir = Split-Path -Parent $scriptPath
$projectRoot = Split-Path -Parent $scriptDir

function Write-Info($message) { Write-Host "`e[1;34m[INFO]`e[0m $message" }
function Write-Success($message) { Write-Host "`e[1;32m[OK]`e[0m $message" }
function Write-Fail($message) { Write-Host "`e[1;31m[FAIL]`e[0m $message" }

Write-Info "=== 中间件连接验证 ==="

$envFile = Join-Path $projectRoot ".env"
if (Test-Path $envFile) {
    Write-Info "加载环境变量..."
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
} else {
    Write-Info ".env 文件不存在，跳过验证"
    exit 0
}

$dbUrl = [Environment]::GetEnvironmentVariable("DATABASE_URL")
if ($dbUrl) {
    Write-Info "验证 PostgreSQL 连接..."
    try {
        uv run python -c "import psycopg; psycopg.connect('$dbUrl'); print('OK')"
        Write-Success "PostgreSQL 连接成功"
    } catch {
        Write-Fail "PostgreSQL 连接失败"
    }
} else {
    Write-Info "未配置 DATABASE_URL，跳过 PostgreSQL 验证"
}

$redisUrl = [Environment]::GetEnvironmentVariable("REDIS_URL")
if ($redisUrl) {
    Write-Info "验证 Redis 连接..."
    try {
        uv run python -c "import redis; redis.from_url('$redisUrl').ping(); print('OK')"
        Write-Success "Redis 连接成功"
    } catch {
        Write-Fail "Redis 连接失败"
    }
} else {
    Write-Info "未配置 REDIS_URL，跳过 Redis 验证"
}

Write-Info "=== 连接验证完成 ==="