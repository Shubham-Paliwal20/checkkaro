# Kill all Python processes
Write-Host "Killing all Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Kill all processes on port 8000
Write-Host "Killing all processes on port 8000..." -ForegroundColor Yellow
$processes = netstat -ano | findstr ":8000" | ForEach-Object {
    if ($_ -match '\s+(\d+)\s*$') {
        $matches[1]
    }
} | Select-Object -Unique

foreach ($processId in $processes) {
    try {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        Write-Host "Killed process $processId" -ForegroundColor Green
    } catch {
        Write-Host "Could not kill process $processId" -ForegroundColor Red
    }
}

Start-Sleep -Seconds 2

# Clear Python cache
Write-Host "Clearing Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "`nAll processes killed and cache cleared!" -ForegroundColor Green
Write-Host "Now run: venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000" -ForegroundColor Cyan
