# ParaDocs Status Check Script
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

$missingFolders = @()
foreach ($folder in $requiredFolders) {
    if (Test-Path $folder) {
        Write-Host "  ✓ $folder" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $folder" -ForegroundColor Red
        $missingFolders += $folder
    }
}

if ($missingFolders.Count -gt 0) {
    Write-Host "`n[WARNING] Missing folders detected. Run: ./scripts/create_paradocs_structure.ps1" -ForegroundColor Yellow
}

# Check Git status
Write-Host "`n📊 Git Status:" -ForegroundColor Yellow
if (Test-Path .git) {
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Host "  ⚠️  Uncommitted changes detected" -ForegroundColor Yellow
        $changes = ($gitStatus | Measure-Object).Count
        Write-Host "  Files changed: $changes" -ForegroundColor Gray
    } else {
        Write-Host "  ✓ Working directory clean" -ForegroundColor Green
    }
    
    # Check Git LFS
    $lfsInstalled = git lfs version 2>$null
    if ($lfsInstalled) {
        Write-Host "  ✓ Git LFS installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Git LFS not installed" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ Not a Git repository" -ForegroundColor Red
    Write-Host "  Run: git init" -ForegroundColor Gray
}

# Count documents
Write-Host "`n📄 Document Statistics:" -ForegroundColor Yellow

# Raw documents
$rawDocs = @{
    EEOC = 0
    FEMA = 0
    OTHER = 0
    Total = 0
}

if (Test-Path "docs/raw") {
    $rawDocs.EEOC = (Get-ChildItem -Path "docs/raw/EEOC" -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
    $rawDocs.FEMA = (Get-ChildItem -Path "docs/raw/FEMA" -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
    $rawDocs.OTHER = (Get-ChildItem -Path "docs/raw/OTHER" -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
    $rawDocs.Total = $rawDocs.EEOC + $rawDocs.FEMA + $rawDocs.OTHER
}

Write-Host "  Raw Documents:" -ForegroundColor White
Write-Host "    EEOC:  $($rawDocs.EEOC)" -ForegroundColor Gray
Write-Host "    FEMA:  $($rawDocs.FEMA)" -ForegroundColor Gray
Write-Host "    OTHER: $($rawDocs.OTHER)" -ForegroundColor Gray
Write-Host "    Total: $($rawDocs.Total)" -ForegroundColor Gray

# Processed documents
$processedDocs = 0
if (Test-Path "docs/processed") {
    $processedDocs = (Get-ChildItem -Path "docs/processed" -Filter "*.json" -File -Recurse -ErrorAction SilentlyContinue | 
                     Where-Object { $_.Name -ne "keyword_index.json" -and $_.Name -ne "date_index.json" } | 
                     Measure-Object).Count
}

Write-Host "`n  Processed Documents: $processedDocs" -ForegroundColor White

if ($rawDocs.Total -gt 0) {
    $processedPercent = [math]::Round(($processedDocs / $rawDocs.Total) * 100, 1)
    Write-Host "  Processing Rate: $processedPercent%" -ForegroundColor Gray
}

# Check indexes
Write-Host "`n🔍 Search Indexes:" -ForegroundColor Yellow
if (Test-Path "search_index/keyword_index.json") {
    $keywordIndex = Get-Content "search_index/keyword_index.json" | ConvertFrom-Json
    $keywordCount = $keywordIndex.Count
    Write-Host "  ✓ Keyword Index: $keywordCount keywords" -ForegroundColor Green
} else {
    Write-Host "  ✗ Keyword Index not found" -ForegroundColor Red
}

if (Test-Path "search_index/date_index.json") {
    $dateIndex = Get-Content "search_index/date_index.json" | ConvertFrom-Json
    $dateCount = $dateIndex.Count
    Write-Host "  ✓ Date Index: $dateCount dates" -ForegroundColor Green
} else {
    Write-Host "  ✗ Date Index not found" -ForegroundColor Red
}

# Check configuration
Write-Host "`n⚙️  Configuration:" -ForegroundColor Yellow
$configFiles = @(
    "config/metadata_schema.json",
    "config/cursor.rules.json",
    "config/compliance-rules/eeoc-rules.json",
    "config/compliance-rules/fema-rules.json"
)

foreach ($config in $configFiles) {
    if (Test-Path $config) {
        Write-Host "  ✓ $config" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $config" -ForegroundColor Red
    }
}

# Check logs
Write-Host "`n📝 Recent Logs:" -ForegroundColor Yellow
if (Test-Path "logs") {
    $recentLogs = Get-ChildItem -Path "logs" -Filter "*.log" -ErrorAction SilentlyContinue | 
                  Sort-Object LastWriteTime -Descending | 
                  Select-Object -First 3
    
    if ($recentLogs) {
        foreach ($log in $recentLogs) {
            $age = (Get-Date) - $log.LastWriteTime
            $ageStr = if ($age.TotalDays -lt 1) { 
                "{0:N0} hours ago" -f $age.TotalHours 
            } else { 
                "{0:N0} days ago" -f $age.TotalDays 
            }
            Write-Host "  • $($log.Name) ($ageStr)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  No log files found" -ForegroundColor Gray
    }
}

# Environment check
Write-Host "`n🔐 Environment:" -ForegroundColor Yellow
if ($env:CENSUS_API_KEY) {
    Write-Host "  ✓ CENSUS_API_KEY is set" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  CENSUS_API_KEY not set (NAICS validation limited)" -ForegroundColor Yellow
}

# Python check
$pythonVersion = python --version 2>$null
if ($pythonVersion) {
    Write-Host "  ✓ Python installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
}

# Recommendations
Write-Host "`n💡 Recommendations:" -ForegroundColor Yellow

if ($missingFolders.Count -gt 0) {
    Write-Host "  1. Create folder structure: ./scripts/create_paradocs_structure.ps1" -ForegroundColor White
}

if ($rawDocs.Total -eq 0) {
    Write-Host "  2. Migrate existing files: ./scripts/migrate_existing_files.ps1" -ForegroundColor White
} elseif ($processedDocs -lt $rawDocs.Total) {
    Write-Host "  2. Process documents: python scripts/run_pipeline.py" -ForegroundColor White
}

if (-not (Test-Path "search_index/keyword_index.json")) {
    Write-Host "  3. Generate indexes: python scripts/run_indexing.py" -ForegroundColor White
}

if (-not (Test-Path .git)) {
    Write-Host "  4. Initialize Git: git init && git lfs install" -ForegroundColor White
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "For detailed help, see README.md" -ForegroundColor Gray
Write-Host "" 