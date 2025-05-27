# ParaDocs Structure Creation Script
# Creates comprehensive folder structure for legal-tech document management

Write-Host "Creating ParaDocs folder structure..." -ForegroundColor Green

# Define the folder structure
$folders = @(
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
    "config/templates",
    "scripts",
    "logs",
    "index",
    "search_index",
    "backup"
)

# Create folders
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    Write-Host "Created: $folder" -ForegroundColor Yellow
}

# Create .gitignore
$gitignoreContent = @"
# Logs
logs/
*.log

# Temporary files
*.tmp
*.temp
~$*

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
env/
.env

# Node
node_modules/
npm-debug.log*
yarn-debug.log*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Sensitive data
config/secrets/
*.key
*.pem

# Large files handled by Git LFS
# (These will be tracked by LFS, not ignored)
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "Created: .gitignore" -ForegroundColor Yellow

# Create .gitattributes for Git LFS
$gitattributesContent = @"
# Git LFS tracking for binary files
*.pdf filter=lfs diff=lfs merge=lfs -text
*.docx filter=lfs diff=lfs merge=lfs -text
*.doc filter=lfs diff=lfs merge=lfs -text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xls filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.tiff filter=lfs diff=lfs merge=lfs -text
*.eml filter=lfs diff=lfs merge=lfs -text
*.msg filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
"@

Set-Content -Path ".gitattributes" -Value $gitattributesContent
Write-Host "Created: .gitattributes" -ForegroundColor Yellow

# Create README files for each major directory
$readmeContents = @{
    "docs/README.md" = @"
# Documents Directory

## Structure
- `raw/` - Original documents as received (PDFs, Word docs, emails, etc.)
  - `EEOC/` - Equal Employment Opportunity Commission documents
  - `FEMA/` - Federal Emergency Management Agency documents
  - `OTHER/` - Other agency documents
- `processed/` - OCR output, extracted text, and metadata JSON files

## Naming Convention
- Agency/Year-CaseID/DocumentName.extension
- Example: `EEOC/2024-EEO-23-00123/Charge.pdf`

## Metadata Sidecar Files
Each document should have a corresponding .json metadata file.
"@

    "src/README.md" = @"
# Source Code Directory

## Modules
- `ingestion/` - OCR, preprocessing, and metadata extraction
- `validation/` - EEO/FEMA rule engines and compliance checks
- `indexing/` - Search index creation and management
- `workflow/` - Automation loops and alerting

## Usage
Run scripts from the project root using:
```
python -m src.module_name.script_name
```
"@

    "config/README.md" = @"
# Configuration Directory

## Contents
- `compliance-rules/` - EEO and FEMA compliance rule definitions
- `templates/` - Prompt templates for AI/automation
- `cursor.rules.json` - Cursor AI configuration

## Security Note
Never commit sensitive configuration (API keys, passwords) to Git.
Use environment variables or a secrets manager.
"@

    "scripts/README.md" = @"
# Scripts Directory

## Purpose
Standalone scripts for project automation and management.

## Key Scripts
- `run_pipeline.py` - End-to-end document processing
- `watch_folder.ps1` - Folder monitoring for new documents
- `run_indexing.py` - Generate search indexes
- `backup_data.ps1` - Backup documents and metadata
"@
}

foreach ($path in $readmeContents.Keys) {
    Set-Content -Path $path -Value $readmeContents[$path]
    Write-Host "Created: $path" -ForegroundColor Yellow
}

Write-Host "`nParaDocs folder structure created successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Initialize Git repository: git init" -ForegroundColor White
Write-Host "2. Install Git LFS: git lfs install" -ForegroundColor White
Write-Host "3. Run the migration script to reorganize existing files" -ForegroundColor White 