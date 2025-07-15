# Git LFS Quick Start for ParaDocs

## Immediate Steps (Run These Now)

### 1. First, ensure you're in the ParaDocs directory
```bash
cd "C:\Users\Max\Documents\EEO FILES\ParaDocs"
```

### 2. Install Git LFS (if not already installed)
```bash
# Check if Git LFS is installed
git lfs version

# If not installed, download from https://git-lfs.github.com/
# Then run:
git lfs install
```

### 3. Initialize Git Repository
```bash
git init
```

### 4. Set up Git LFS tracking
```bash
# Track large file types
git lfs track "*.xlsx"
git lfs track "*.xls"
git lfs track "*.pdf"
git lfs track "*.docx"
git lfs track "*.doc"
git lfs track "*.png"
git lfs track "*.prn"
git lfs track "*.mht"
git lfs track "core"
```

### 5. Create safe directory structure
```bash
# Create directories for organizing data
mkdir -p data/samples/tables
mkdir -p data/samples/forms
mkdir -p data/samples/manuals
mkdir -p data/documents/private
mkdir -p data/generated
mkdir -p data/backup
```

### 6. Move sensitive documents to private folder
```bash
# Move all real EEOC documents to private (won't be committed)
# You'll need to do this manually in Windows Explorer:
# Move all Table B-*.xlsx files to data/documents/private/
# Move all .pdf files to data/documents/private/
# Move Form 462 files to data/documents/private/
```

### 7. Initial Git commits
```bash
# Add Git configuration files
git add .gitattributes
git add .gitignore
git add GIT_LFS_SETUP_GUIDE.md
git add GIT_LFS_QUICK_START.md
git commit -m "Initialize Git LFS configuration"

# Add safe documentation
git add ACTION_LOG.md
git add requirements.txt
git add PROJECT_ANALYSIS_REPORT.md
git add data/samples/README.md
git commit -m "Add project documentation and structure"

# Add source code
git add search_documents.py
git add search_documents_with_logging.py
git add setup_project_structure.py
git commit -m "Add search tools and setup scripts"

# Add other safe markdown files
git add README.md
git add PROJECT_ORGANIZATION.md
git add INTERACTIVE_REFERENCE_ROADMAP.md
git add SYSTEM_OVERVIEW.md
git commit -m "Add project planning documentation"
```

### 8. Create GitHub repository
1. Go to https://github.com/new
2. Repository name: `paradocs`
3. Set to **PRIVATE** (important!)
4. Don't initialize with any files
5. Create repository

### 9. Connect and push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/paradocs.git

# Push all commits
git branch -M main
git push -u origin main
```

## Important Reminders

### ⚠️ Before EVERY commit:
```bash
# Check what files will be committed
git status

# Make sure NO real EEOC documents are staged
# Look for any .xlsx, .pdf, .docx files that aren't samples
```

### 🔍 Verify LFS is working:
```bash
# See which files are tracked by LFS
git lfs ls-files

# Check LFS status
git lfs status
```

### 📁 Safe vs. Private Files:

**SAFE to commit:**
- All .py files (search tools)
- All .md files (documentation)
- Files in data/samples/ (sanitized only)
- .gitignore, .gitattributes
- requirements.txt

**NEVER commit:**
- Any file with real EEOC data
- Files in data/documents/private/
- Original Table B-*.xlsx files
- Real Form 462 documents
- Any file with personal information

## If You Make a Mistake

If you accidentally stage a sensitive file:
```bash
# Remove from staging
git reset HEAD sensitive_file.xlsx

# Or remove all staged files and start over
git reset HEAD .
```

## Next Steps After Git Setup

1. Create sanitized sample documents
2. Update search tools to use new paths
3. Set up automated backups
4. Begin database migration planning

Remember: This is a PRIVATE repository, but still never commit real EEOC data! 