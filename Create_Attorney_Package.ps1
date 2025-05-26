# Create Attorney Package Script for Meindl v. FEMA
# This script creates a complete portable package for sharing with Rick Guerra

Write-Host "Creating Attorney Package for Meindl v. FEMA..." -ForegroundColor Green

# Create the package directory
$packageName = "Meindl_v_FEMA_Attorney_Portal"
if (Test-Path $packageName) {
    Remove-Item $packageName -Recurse -Force
}
New-Item -ItemType Directory -Path $packageName | Out-Null

Write-Host "Copying portal files..." -ForegroundColor Yellow

# Copy HTML portals
$htmlFiles = @(
    "Attorney_Portal.html",
    "MASTER_INDEX.html",
    "ADR_MEDIATION_PORTAL.html",
    "paradocs-index.html",
    "ADMINISTRATIVE_HEARING_PORTAL.html",
    "FEDERAL_LAWSUIT_PORTAL.html",
    "CASE_VIOLATIONS_SUMMARY.html",
    "paradocs_legal_strategy_dashboard.html",
    "paradocs_master_timeline_enhanced.html"
)

foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        Copy-Item $file "$packageName/" -Force
        Write-Host "  ✓ $file" -ForegroundColor Gray
    }
}

# Copy JavaScript and JSON files
Write-Host "Copying data files..." -ForegroundColor Yellow
$dataFiles = @("*.js", "*.json", "*.csv")
foreach ($pattern in $dataFiles) {
    Copy-Item $pattern "$packageName/" -Force -ErrorAction SilentlyContinue
}

# Copy the ADR_Mediation folder (most important for Rick)
Write-Host "Copying ADR documents..." -ForegroundColor Yellow
if (Test-Path "paradocs_organized/ADR_Mediation") {
    New-Item -ItemType Directory -Path "$packageName/paradocs_organized" -Force | Out-Null
    Copy-Item -Recurse "paradocs_organized/ADR_Mediation" "$packageName/paradocs_organized/" -Force
    Write-Host "  ✓ ADR_Mediation folder" -ForegroundColor Gray
}

# Create README for Rick
Write-Host "Creating instructions..." -ForegroundColor Yellow
$readme = @"
MEINDL v. FEMA - ATTORNEY CASE PORTAL
=====================================

CASE: EEOC HS-FEMA-02430-2024
DAMAGES DEMAND: $5,000,000
KEY VIOLATION: 1,340-day accommodation delay (2,878% over legal limit)

HOW TO ACCESS:
1. Double-click "Attorney_Portal.html" to start
2. Or open any .html file directly in your browser

KEY DOCUMENTS FOR ADR:
- ADR_MEDIATION_PORTAL.html - Complete settlement strategy
- paradocs_organized/ADR_Mediation/AGGRESSIVE_DAMAGES_CALCULATION.md - $5M breakdown
- paradocs_organized/ADR_Mediation/LETTER_TO_RICK_GUERRA.md - Your representation letter

FEATURES:
- Search all 450+ case documents
- View complete violation timeline
- Review damages calculations
- Access legal authorities

NO INSTALLATION REQUIRED
- Works on any computer
- Runs in any modern browser
- Completely offline - no internet needed
- Take to court/mediation on laptop

SECURITY:
This package contains confidential attorney-client privileged information.
Please maintain appropriate security and do not forward without authorization.

Contact: Max Meindl
Phone: [Your Phone]
Email: [Your Email]

"@
$readme | Out-File "$packageName/README.txt" -Encoding UTF8

# Create a quick start batch file for Windows
$quickstart = @"
@echo off
start Attorney_Portal.html
"@
$quickstart | Out-File "$packageName/CLICK_TO_START.bat" -Encoding ASCII

Write-Host "`nCreating ZIP archive..." -ForegroundColor Yellow

# Create the ZIP file
$zipPath = "$packageName.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path $packageName -DestinationPath $zipPath -CompressionLevel Optimal

# Get file size
$size = (Get-Item $zipPath).Length / 1MB
Write-Host "`n✅ SUCCESS! Package created: $zipPath" -ForegroundColor Green
Write-Host "   Size: $([math]::Round($size, 2)) MB" -ForegroundColor Gray

# Provide next steps
Write-Host "`nNEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Send '$zipPath' to Rick via:"
Write-Host "   - Encrypted email (ProtonMail, etc.)"
Write-Host "   - Secure file transfer (WeTransfer, Dropbox)"
Write-Host "   - USB drive (most secure)"
Write-Host ""
Write-Host "2. If using email:"
Write-Host "   - Password protect the ZIP"
Write-Host "   - Send password via text/phone"
Write-Host ""
Write-Host "3. Optional cloud backup:"
Write-Host "   - Upload to Google Drive"
Write-Host "   - Share link with Rick only"
Write-Host "   - Set expiration date"

# Offer to create password-protected version
Write-Host "`nCreate password-protected version? (Requires 7-Zip)" -ForegroundColor Yellow
$response = Read-Host "Enter Y for yes, N for no"

if ($response -eq 'Y') {
    $password = Read-Host "Enter password" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
    $plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    if (Get-Command 7z -ErrorAction SilentlyContinue) {
        7z a -p"$plainPassword" -mhe=on "$packageName`_Secure.7z" $packageName/
        Write-Host "✅ Secure archive created: $packageName`_Secure.7z" -ForegroundColor Green
    } else {
        Write-Host "❌ 7-Zip not found. Please install 7-Zip for password protection." -ForegroundColor Red
    }
}

Write-Host "`nPackage ready for delivery to Rick Guerra!" -ForegroundColor Green 