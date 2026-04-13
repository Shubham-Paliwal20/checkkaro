# CheckKaro - Git Push Script
# Run this script to push your changes to GitHub

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              CheckKaro - Git Push Helper                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if remote exists
$remoteExists = git remote -v
if (-not $remoteExists) {
    Write-Host "⚠️  No remote repository configured!" -ForegroundColor Yellow
    Write-Host "`nPlease add your GitHub repository URL:" -ForegroundColor White
    Write-Host "Example: https://github.com/YOUR_USERNAME/checkkaro.git`n" -ForegroundColor Gray
    
    $repoUrl = Read-Host "Enter your GitHub repository URL"
    
    if ($repoUrl) {
        Write-Host "`n📝 Adding remote repository..." -ForegroundColor Yellow
        git remote add origin $repoUrl
        Write-Host "✅ Remote repository added!`n" -ForegroundColor Green
    } else {
        Write-Host "`n❌ No URL provided. Exiting..." -ForegroundColor Red
        exit
    }
}

# Show current status
Write-Host "📊 Current Status:" -ForegroundColor Cyan
git status --short

# Confirm push
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n"
Write-Host "Ready to push to GitHub!" -ForegroundColor Green
Write-Host "This will upload all your changes to the remote repository.`n"

$confirm = Read-Host "Do you want to continue? (Y/N)"

if ($confirm -eq "Y" -or $confirm -eq "y") {
    Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
    
    # Try to push
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║                  ✅ SUCCESS! ✅                             ║" -ForegroundColor Green
        Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
        Write-Host "Your changes have been pushed to GitHub!" -ForegroundColor Green
        Write-Host "`n📦 What was pushed:" -ForegroundColor Cyan
        Write-Host "   • 118 products with full ingredient lists" -ForegroundColor White
        Write-Host "   • Detailed harmful effects for 180+ ingredients" -ForegroundColor White
        Write-Host "   • Consistent classification system" -ForegroundColor White
        Write-Host "   • Production-ready backend and frontend" -ForegroundColor White
        Write-Host "`n🎉 Your CheckKaro project is now on GitHub!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Push failed!" -ForegroundColor Red
        Write-Host "`nCommon solutions:" -ForegroundColor Yellow
        Write-Host "1. Check your GitHub credentials" -ForegroundColor White
        Write-Host "2. Verify repository URL is correct" -ForegroundColor White
        Write-Host "3. Make sure you have write access" -ForegroundColor White
        Write-Host "4. Try: git pull origin main --rebase" -ForegroundColor White
        Write-Host "`nFor more help, see GIT_PUSH_GUIDE.md" -ForegroundColor Gray
    }
} else {
    Write-Host "`n❌ Push cancelled." -ForegroundColor Yellow
    Write-Host "Your changes are still committed locally." -ForegroundColor White
    Write-Host "Run this script again when you're ready to push." -ForegroundColor White
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n"
