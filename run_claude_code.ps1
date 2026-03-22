# ================================================
# Claude Code 接入 OpenClaw - 快捷脚本
# 使用方式: powershell -File run_claude_code.ps1 "你的任务描述"
# ================================================
param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string]$Task
)

$env:ANTHROPIC_BASE_URL = "http://www.claudecodeserver.top/api"
$env:ANTHROPIC_AUTH_TOKEN = "sk_4f99b0f81b70afdb62137239037f7e562e77fbda002d4d3ae3881615aef71d25"
$env:CLAUDE_CODE_PERMISSION_MODE = "bypassPermissions"

if (-not $Task) {
    Write-Host "用法: .\run_claude_code.ps1 '任务描述'"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\run_claude_code.ps1 '帮我写一个Python爬虫抓取豆瓣Top250电影'"
    Write-Host "  .\run_claude_code.ps1 'Review这段代码有什么问题'"
    exit 0
}

$workDir = if ($PWD.Path -eq $env:USERPROFILE) { $PWD.Path } else { Split-Path $PWD.Path -Parent }
if (-not $workDir) { $workDir = $PWD.Path }

Write-Host "[嬴 🤖] 正在启动 Claude Code..."
Write-Host "[任务] $Task"
Write-Host "[工作目录] $workDir"
Write-Host ""

Set-Location $workDir
claude --permission-mode bypassPermissions --print $Task
