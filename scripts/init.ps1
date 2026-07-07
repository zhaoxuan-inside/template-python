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
