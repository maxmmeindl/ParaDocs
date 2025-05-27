# ParaDocs File Migration Script
# Migrates existing files into the new organized structure

param(
    [string]$DryRun = "true"  # Set to "false" to actually move files
)

Write-Host "ParaDocs File Migration Script" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

if ($DryRun -eq "true") {
    Write-Host "Running in DRY RUN mode - no files will be moved" -ForegroundColor Yellow
} else {
    Write-Host "Running in LIVE mode - files WILL be moved" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (yes/no)"
    if ($confirm -ne "yes") {
        Write-Host "Aborted." -ForegroundColor Yellow
        exit
    }
}

# Load file classification rules from config
$configPath = "config/cursor.rules.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    $globs = $config.globs
} else {
    Write-Host "Warning: Config file not found, using default patterns" -ForegroundColor Yellow
    $globs = @{
        EEOC = @("*charge*", "*accommodation*", "*interactive*", "*eeoc*", "*eeo*")
        FEMA = @("*termination*", "*fema*", "*position*", "*removal*")
        MEDICAL = @("*medical*", "*doctor*", "*physician*", "*health*", "*disability*")
        LEGAL = @("*brief*", "*motion*", "*complaint*", "*answer*", "*discovery*")
        EMAIL = @("*.eml", "*.msg", "*email*")
    }
}

# Function to classify a file based on patterns
function Get-FileClassification {
    param([string]$filename)
    
    $lowerName = $filename.ToLower()
    
    # Check EEOC patterns
    foreach ($pattern in $globs.EEOC) {
        if ($lowerName -like $pattern.ToLower()) {
            return "EEOC"
        }
    }
    
    # Check FEMA patterns
    foreach ($pattern in $globs.FEMA) {
        if ($lowerName -like $pattern.ToLower()) {
            return "FEMA"
        }
    }
    
    # Default to OTHER
    return "OTHER"
}

# Function to extract case number from filename
function Get-CaseNumber {
    param([string]$filename)
    
    # Common case number patterns
    $patterns = @(
        'HS-FEMA-\d{5}-\d{4}',
        'EEO-\d{2}-\d{5}',
        '\d{4}-EEO-\d{2}-\d{5}',
        'CASE-\d{4}-\d{3}',
        '\d{4}-\d{3}-[A-Z]{2}'
    )
    
    foreach ($pattern in $patterns) {
        if ($filename -match $pattern) {
            return $matches[0]
        }
    }
    
    # Extract date if no case number found
    if ($filename -match '\d{4}-\d{2}-\d{2}') {
        return $matches[0]
    }
    
    return "UNCATEGORIZED"
}

# Migration statistics
$stats = @{
    Total = 0
    Moved = 0
    Skipped = 0
    Errors = 0
    ByAgency = @{}
}

# Get all files to migrate
$sourceFiles = @()

# Add files from root
$sourceFiles += Get-ChildItem -Path "." -File | Where-Object { 
    $_.Extension -in @(".pdf", ".docx", ".doc", ".xlsx", ".xls", ".eml", ".msg", ".txt", ".json", ".csv", ".html")
}

# Add files from existing folders
$existingFolders = @("paradocs-agent", "paradocs-eeo-website", "duplicates_removed")
foreach ($folder in $existingFolders) {
    if (Test-Path $folder) {
        $sourceFiles += Get-ChildItem -Path $folder -File -Recurse | Where-Object { 
            $_.Extension -in @(".pdf", ".docx", ".doc", ".xlsx", ".xls", ".eml", ".msg", ".txt", ".json", ".csv")
        }
    }
}

Write-Host "`nFound $($sourceFiles.Count) files to process" -ForegroundColor Green

# Process each file
foreach ($file in $sourceFiles) {
    $stats.Total++
    
    # Skip if already in correct structure
    if ($file.FullName -like "*\docs\raw\*" -or $file.FullName -like "*\docs\processed\*") {
        Write-Host "Skipping (already organized): $($file.Name)" -ForegroundColor DarkGray
        $stats.Skipped++
        continue
    }
    
    # Skip certain files
    $skipPatterns = @("*.ps1", "*.py", "*.js", "*.bat", "package*.json", "*.md", ".git*")
    $skip = $false
    foreach ($pattern in $skipPatterns) {
        if ($file.Name -like $pattern) {
            $skip = $true
            break
        }
    }
    if ($skip) {
        Write-Host "Skipping (system file): $($file.Name)" -ForegroundColor DarkGray
        $stats.Skipped++
        continue
    }
    
    # Classify the file
    $agency = Get-FileClassification -filename $file.Name
    $caseNumber = Get-CaseNumber -filename $file.Name
    
    # Determine if it's raw or processed
    $isProcessed = $file.Extension -in @(".txt", ".json", ".csv") -and 
                   $file.Name -notlike "*index*" -and 
                   $file.Name -notlike "*report*"
    
    # Build target path
    if ($isProcessed) {
        $targetDir = "docs/processed/$agency/$caseNumber"
    } else {
        $targetDir = "docs/raw/$agency/$caseNumber"
    }
    
    $targetPath = Join-Path $targetDir $file.Name
    
    # Display migration info
    Write-Host "`nFile: $($file.Name)" -ForegroundColor White
    Write-Host "  From: $($file.FullName)" -ForegroundColor Gray
    Write-Host "  To: $targetPath" -ForegroundColor Gray
    Write-Host "  Agency: $agency, Case: $caseNumber" -ForegroundColor Gray
    
    # Create target directory and move file (if not dry run)
    if ($DryRun -eq "false") {
        try {
            # Create directory
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            
            # Move file
            Move-Item -Path $file.FullName -Destination $targetPath -Force
            Write-Host "  Status: Moved" -ForegroundColor Green
            $stats.Moved++
            
            # Update agency statistics
            if (-not $stats.ByAgency.ContainsKey($agency)) {
                $stats.ByAgency[$agency] = 0
            }
            $stats.ByAgency[$agency]++
            
        } catch {
            Write-Host "  Status: ERROR - $_" -ForegroundColor Red
            $stats.Errors++
        }
    } else {
        Write-Host "  Status: Would move (dry run)" -ForegroundColor Yellow
        
        # Update agency statistics for dry run
        if (-not $stats.ByAgency.ContainsKey($agency)) {
            $stats.ByAgency[$agency] = 0
        }
        $stats.ByAgency[$agency]++
    }
}

# Display summary
Write-Host "`n=============================" -ForegroundColor Cyan
Write-Host "Migration Summary" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Total files: $($stats.Total)" -ForegroundColor White
Write-Host "Moved: $($stats.Moved)" -ForegroundColor Green
Write-Host "Skipped: $($stats.Skipped)" -ForegroundColor Yellow
Write-Host "Errors: $($stats.Errors)" -ForegroundColor Red

Write-Host "`nBy Agency:" -ForegroundColor White
foreach ($agency in $stats.ByAgency.Keys | Sort-Object) {
    Write-Host "  $agency : $($stats.ByAgency[$agency])" -ForegroundColor Gray
}

if ($DryRun -eq "true") {
    Write-Host "`nThis was a DRY RUN. To actually move files, run:" -ForegroundColor Yellow
    Write-Host "  .\scripts\migrate_existing_files.ps1 -DryRun false" -ForegroundColor White
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Review the migrated structure in docs/raw and docs/processed" -ForegroundColor White
Write-Host "2. Run document processing pipeline on docs/raw files" -ForegroundColor White
Write-Host "3. Run indexing script: python scripts/run_indexing.py" -ForegroundColor White 