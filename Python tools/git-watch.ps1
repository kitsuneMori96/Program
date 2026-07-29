# git-watch.ps1 — 监控文件变更并自动提交
# 使用: PowerShell 中运行此脚本，保持窗口打开即可

$watchPath = "D:\Program\Python tools"
$debounceSeconds = 15

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $watchPath
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]::FileName -bor [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true

$timer = New-Object System.Timers.Timer
$timer.Interval = ($debounceSeconds * 1000)
$timer.AutoReset = $false

$timerAction = {
    $timer.Stop()
    try {
        Push-Location $watchPath
        $status = git status --porcelain
        if ($status) {
            $count = ($status -split "`n" | Where-Object { $_ -ne "" }).Count
            $changedFiles = ($status | ForEach-Object { $_ -replace '^\s+\S+\s+', '' }) -join ", "
            git add -A
            git commit -m "auto: $count file(s) changed [$changedFiles]"
        }
    } finally {
        Pop-Location
        $timer.Start()
    }
}

Register-ObjectEvent $watcher "Changed" -Action $timerAction | Out-Null
Register-ObjectEvent $watcher "Created" -Action $timerAction | Out-Null
Register-ObjectEvent $watcher "Deleted" -Action $timerAction | Out-Null

Write-Host "监控中: $watchPath"
Write-Host "检测到变更后 $debounceSeconds 秒无变动即自动提交"
Write-Host "按 Ctrl+C 停止监控"
try {
    while ($true) { Start-Sleep -Seconds 1 }
} finally {
    $watcher.EnableRaisingEvents = $false
    $watcher.Dispose()
    $timer.Dispose()
    Get-EventSubscriber | Unregister-Event
}
