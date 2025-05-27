# ParaDocs Status Check Script (Simple Version)
# Displays current system status and statistics

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "          ParaDocs System Status Check          " -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Check folder structure
Write-Host "[Folder Structure]" -ForegroundColor Yellow
$requiredFolders = @(
    "docs/raw/EEOC",
    "docs/raw/FEMA", 
    "docs/raw/OTHER",
    "docs/processed/EEOC",
    "docs/processed/FEMA",
    "docs/processed/OTHER",
    "src/ingestion",
    "src/validation",
    "src/indexing",
    "src/workflow",
    "config/compliance-rules",
    "scripts",
    "logs",
    "search_index",
    "backup"
)

$missingCount = 0
$presentCount = 0
foreach ($folder in $requiredFolders) {
    if (Test-Path $folder) {
        Write-Host "  [OK] $folder" -ForegroundColor Green
        $presentCount++
    } else {
        Write-Host "  [MISSING] $folder" -ForegroundColor Red
        $missingCount++
    }
}

Write-Host "`nFolder Summary: $presentCount present, $missingCount missing" -ForegroundColor White

# Check Git status
Write-Host "`n[Git Status]" -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "  [OK] Git repository initialized" -ForegroundColor Green
    
    # Check Git LFS
    $lfsInstalled = git lfs version 2>$null
    if ($lfsInstalled) {
        Write-Host "  [OK] Git LFS installed" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] Git LFS not installed" -ForegroundColor Red
    }
} else {
    Write-Host "  [MISSING] Not a Git repository" -ForegroundColor Red
}

# Count documents
Write-Host "`n[Document Statistics]" -ForegroundColor Yellow

$rawCount = 0
if (Test-Path "docs/raw") {
    $rawCount = (Get-ChildItem -Path "docs/raw" -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
}

$processedCount = 0
if (Test-Path "docs/processed") {
    $processedCount = (Get-ChildItem -Path "docs/processed" -Filter "*.json" -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
}

Write-Host "  Raw Documents: $rawCount" -ForegroundColor White
Write-Host "  Processed Documents: $processedCount" -ForegroundColor White

# Check configuration
Write-Host "`n[Configuration Files]" -ForegroundColor Yellow
$configFiles = @(
    "config/metadata_schema.json",
    "config/cursor.rules.json",
    "config/compliance-rules/eeoc-rules.json",
    "config/compliance-rules/fema-rules.json"
)

foreach ($config in $configFiles) {
    if (Test-Path $config) {
        Write-Host "  [OK] $config" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $config" -ForegroundColor Red
    }
}

# Next steps
Write-Host "`n[Next Steps]" -ForegroundColor Yellow

if ($missingCount -gt 0) {
    Write-Host "  1. Run: .\scripts\create_paradocs_structure.ps1" -ForegroundColor White
}

if ((Test-Path .git) -eq $false) {
    Write-Host "  2. Initialize Git: git init" -ForegroundColor White
    Write-Host "  3. Install Git LFS: git lfs install" -ForegroundColor White
}

if ($rawCount -eq 0) {
    Write-Host "  4. Migrate files: .\scripts\migrate_existing_files.ps1" -ForegroundColor White
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "" 