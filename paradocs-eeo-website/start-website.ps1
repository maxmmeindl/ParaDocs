Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Starting ParaDocs EEO Website" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install

Write-Host ""
Write-Host "Starting the development server..." -ForegroundColor Green
Write-Host ""
Write-Host "The website will open at http://localhost:5173" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

npm run dev 