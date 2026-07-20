# OpenCLI Hotspot Grabber - PowerShell Wrapper
# Usage: .\run-grabber.ps1 [-Platforms hackernews,github,v2ex] [-OutputDir tmp] [-Quiet]

param(
    [string]$Platforms = "all",
    [string]$OutputDir = "tmp",
    [switch]$Quiet
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptPath "hotspot_grabber.py"

# 构建平台参数
$PlatformArgs = @()
if ($Platforms -ne "all") {
    $PlatformList = $Platforms -split ',' | ForEach-Object { $_.Trim() }
    $PlatformArgs = @("-p") + $PlatformList
}

# 构建输出目录参数
$OutputArgs = @("-o", $OutputDir)

# 安静模式
$QuietArgs = @()
if ($Quiet) {
    $QuietArgs = @("-q")
}

# 执行 Python 脚本
Write-Host "[OPENCLI] Starting hotspot grabber..." -ForegroundColor Cyan
Write-Host "[PLATFORMS] $Platforms" -ForegroundColor Cyan
Write-Host "[OUTPUT] $OutputDir" -ForegroundColor Cyan

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

python $PythonScript @PlatformArgs @OutputArgs @QuietArgs

$stopwatch.Stop()
Write-Host ""
Write-Host "[DONE] Completed in $($stopwatch.Elapsed.TotalSeconds.ToString('F1')) seconds" -ForegroundColor Green
