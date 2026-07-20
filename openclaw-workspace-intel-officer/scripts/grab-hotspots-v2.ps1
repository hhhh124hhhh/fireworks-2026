# ============================================
# Hotspot Grabber v3 - OpenCLI (Faster)
# Date: 2026-03-21  Maintainer: intel-officer
# Performance: 3-7x faster than v2
# ============================================
param(
    [string]$OutputDir = "D:\openclaw-data\.openclaw\workspace-intel-officer\tmp",
    [switch]$Quiet
)
$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$tsFile = Get-Date -Format "yyyyMMdd-HHmmss"
$result = @{ timestamp = $timestamp; platforms = @{}; errors = @(); summary = @{ total = 0 } }
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }
function Log($msg, [string]$color = "White") { if (-not $Quiet) { Write-Host $msg -ForegroundColor $color } }

# 1. Weibo (opencli)
Log "`n[1/3] Weibo (opencli)..." "Yellow"
try {
    $weiboRaw = opencli weibo hot --limit 50 -f json 2>$null | Out-String
    if ($weiboRaw) {
        $weiboJson = $weiboRaw | ConvertFrom-Json
        $items = @()
        foreach ($item in $weiboJson) {
            $items += [PSCustomObject]@{
                rank = $item.rank
                title = $item.word
                hot = $item.hot_value
                label = $item.label
                link = $item.url
                platform = "weibo"
                category = $item.category
            }
        }
        $result.platforms.weibo = @{ count = $items.Count; items = $items }
        $result.summary.weibo = $items.Count
        $result.summary.total += $items.Count
        Log "  [OK] Weibo $($items.Count) items" "Green"
    } else {
        throw "opencli returned empty result"
    }
} catch {
    $result.errors += "weibo: $($_.Exception.Message)"
    $result.platforms.weibo = @{ count = 0; items = @() }
    Log "  [FAIL] Weibo" "Red"
}

# 2. Zhihu (opencli)
Log "`n[2/3] Zhihu (opencli)..." "Yellow"
try {
    $zhihuRaw = opencli zhihu hot --limit 30 -f json 2>$null | Out-String
    if ($zhihuRaw) {
        $zhihuJson = $zhihuRaw | ConvertFrom-Json
        $items = @()
        foreach ($item in $zhihuJson) {
            $items += [PSCustomObject]@{
                rank = $item.rank
                title = $item.title
                hot = $item.heat
                answers = $item.answers
                link = $item.url
                platform = "zhihu"
            }
        }
        $result.platforms.zhihu = @{ count = $items.Count; items = $items }
        $result.summary.zhihu = $items.Count
        $result.summary.total += $items.Count
        Log "  [OK] Zhihu $($items.Count) items" "Green"
    } else {
        throw "opencli returned empty result"
    }
} catch {
    $result.errors += "zhihu: $($_.Exception.Message)"
    $result.platforms.zhihu = @{ count = 0; items = @() }
    Log "  [FAIL] Zhihu" "Red"
}

# 3. Baidu (Web Scraping)
Log "`n[3/3] Baidu (Web Scraping)..." "Yellow"
try {
    $baiduHtml = Invoke-RestMethod -Uri "https://top.baidu.com/board?tab=realtime" -UseBasicParsing -TimeoutSec 15
    # Extract JSON data from HTML (look for "cards" array in the inline JSON)
    if ($baiduHtml -match '"cards":\[(.*?)\],"curBoardName"') {
        $cardsJson = "{" + $matches[1] + "}"
        $cardsData = ConvertFrom-Json $cardsJson
        $items = @()
        $hotList = $cardsData.content
        for ($i = 0; $i -lt [Math]::Min($hotList.Count, 30); $i++) {
            $item = $hotList[$i]
            $items += [PSCustomObject]@{
                rank = $i + 1
                title = $item.word
                hot = $item.hotScore
                link = $item.url
                platform = "baidu"
            }
        }
        $result.platforms.baidu = @{ count = $items.Count; items = $items }
        $result.summary.baidu = $items.Count
        $result.summary.total += $items.Count
        Log "  [OK] Baidu $($items.Count) items" "Green"
    } else {
        throw "Failed to parse Baidu hot search data"
    }
} catch {
    $result.errors += "baidu: $($_.Exception.Message)"
    $result.platforms.baidu = @{ count = 0; items = @() }
    Log "  [FAIL] Baidu" "Red"
}

# Summary
Log "`n========================================" "Cyan"
Log "  Total: $($result.summary.total)" "Cyan"
Log "  Weibo: $($result.summary.weibo) | Zhihu: $($result.summary.zhihu) | Baidu: $($result.summary.baidu)" "Cyan"
if ($result.errors.Count -gt 0) { Log "  Errors: $($result.errors.Count)" "Red" }
Log "========================================" "Cyan"

$jsonPath = Join-Path $OutputDir "hotspots-v3-$tsFile.json"
$result | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding utf8
Log "`nSaved: $jsonPath" "DarkGray"
$result | ConvertTo-Json -Depth 5
