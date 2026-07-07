$ErrorActionPreference = "Stop"

$scriptPath = $MyInvocation.MyCommand.Definition
$scriptDir = Split-Path -Parent $scriptPath
$projectRoot = Split-Path -Parent $scriptDir

function Write-Info($message) { Write-Host "`e[1;34m[INFO]`e[0m $message" }
function Write-Success($message) { Write-Host "`e[1;32m[OK]`e[0m $message" }
function Write-Error($message) { Write-Host "`e[1;31m[ERROR]`e[0m $message"; exit 1 }

Write-Info "=== Python3 项目初始化脚本 ==="
Write-Info "项目根目录: $projectRoot"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Info "UV 已安装，版本: $(uv --version)"
} else {
    Write-Info "正在安装 UV..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:PATH += ";$env:USERPROFILE\.cargo\bin;$env:USERPROFILE\.local\bin"
}

Write-Info "启用 UV_LINK_MODE=copy (Windows NTFS 兼容)"
$env:UV_LINK_MODE = "copy"

Write-Info "创建虚拟环境..."
uv venv --python 3.12

Write-Info "安装项目依赖..."
uv sync

Write-Info "安装 pre-commit 钩子..."
uv run pre-commit install

Write-Info "配置 VSCode 团队设置..."
$vscodeDir = Join-Path $projectRoot ".vscode"
$configVscodeDir = Join-Path $projectRoot "configs\vscode"
if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}
if (Test-Path $configVscodeDir) {
    Copy-Item -Path "$configVscodeDir\*" -Destination $vscodeDir -Force
    Write-Success "VSCode 配置已复制"
} else {
    Write-Info "VSCode 配置目录不存在，跳过"
}

$envTemplate = Join-Path $projectRoot ".env.development.template"
$envFile = Join-Path $projectRoot ".env"
if (Test-Path $envTemplate) {
    if (-not (Test-Path $envFile)) {
        Write-Info "复制环境变量模板..."
        Copy-Item $envTemplate $envFile
        Write-Info "请编辑 .env 文件配置中间件连接信息"
    } else {
        Write-Info ".env 文件已存在，跳过复制"
    }
}

Write-Info "运行连接验证..."
$verifyScript = Join-Path $projectRoot "scripts\verify-connection.ps1"
if (Test-Path $verifyScript) {
    & $verifyScript
} else {
    Write-Info "连接验证脚本不存在，跳过"
}

Write-Success "=== 初始化完成 ==="
Write-Host ""
Write-Info "快速开始:"
Write-Host "  1. 激活虚拟环境: .venv\Scripts\Activate.ps1"
Write-Host "  2. 启动开发服务器: uv run uvicorn src.app.main:app --reload"
Write-Host "  3. 运行测试: uv run pytest"
Write-Host "  4. 代码检查: uv run ruff check src"
Write-Host "  5. 代码格式化: uv run ruff format src"