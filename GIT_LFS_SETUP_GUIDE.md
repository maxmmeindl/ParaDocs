# Git LFS Setup Guide for ParaDocs

## Why Git LFS?

Git LFS is essential for ParaDocs because:
- Excel files (.xlsx, .xls) can be several MB each
- PDF manuals can be very large (you have a 4.4MB PDF)
- Regular Git isn't optimized for binary files
- Prevents repository bloat over time

## Prerequisites

1. **Install Git LFS**
   ```bash
   # Windows (with Git Bash)
   git lfs install
   
   # If not installed, download from: https://git-lfs.github.com/
   ```

2. **Verify Installation**
   ```bash
   git lfs version
   ```

## Step-by-Step Setup

### 1. Initialize Git Repository
```bash
cd "C:\Users\Max\Documents\EEO FILES\ParaDocs"
git init
```

### 2. Configure Git LFS
```bash
# Initialize LFS in the repository
git lfs install

# Track document file types with LFS
git lfs track "*.xlsx"
git lfs track "*.xls"
git lfs track "*.pdf"
git lfs track "*.docx"
git lfs track "*.doc"
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.jpeg"

# Track any large data files
git lfs track "*.json" --filename="document_index.json"
git lfs track "*.prn"
git lfs track "*.mht"
git lfs track "core"

# This creates/updates .gitattributes
```

### 3. Create Enhanced .gitignore
```bash
# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# ParaDocs Git Ignore File

# Temporary and backup files
*.tmp
*.temp
*.bak
*.backup
~$*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.project
.pydevproject

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# Logs
*.log
logs/
dev*.log
server*.log

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local
.env.production

# Node (for future web interface)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# ParaDocs specific - exclude sensitive originals
/data/documents/originals/
/data/temp/
/data/private/

# Large generated files that change frequently
document_index.backup.json

# IMPORTANT: Do NOT ignore document_index.json - it's tracked with LFS
# IMPORTANT: Do NOT ignore CATEGORY_REPORT.md - it's useful for the repo
EOF
```

### 4. Create .gitattributes (automatically created by git lfs track)
```bash
# Verify .gitattributes was created correctly
cat .gitattributes
```

### 5. Initial Commit Structure
```bash
# Stage the LFS and Git configuration files first
git add .gitattributes
git add .gitignore
git commit -m "Initialize Git LFS configuration"

# Add project documentation (small files)
git add README.md
git add PROJECT_ORGANIZATION.md
git add INTERACTIVE_REFERENCE_ROADMAP.md
git add SYSTEM_OVERVIEW.md
git add ACTION_LOG.md
git add PROJECT_ANALYSIS_REPORT.md
git add GIT_LFS_SETUP_GUIDE.md
git commit -m "Add project documentation"

# Add source code
git add search_documents.py
git add search_documents_with_logging.py
git add setup_project_structure.py
git add requirements.txt
git commit -m "Add source code and requirements"

# Add generated files (these will use LFS if large)
git add document_index.json
git add CATEGORY_REPORT.md
git commit -m "Add generated indices and reports"

# Check LFS tracking
git lfs ls-files
```

### 6. Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named `paradocs`
3. Make it PRIVATE (contains sensitive data)
4. Don't initialize with README (we already have one)

### 7. Connect to GitHub
```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/paradocs.git

# Verify LFS files before pushing
git lfs status

# Push to GitHub (including LFS files)
git push -u origin main
```

## Important Considerations

### Storage Limits
- GitHub Free: 1GB storage, 1GB bandwidth/month
- GitHub Pro: 2GB storage, 2GB bandwidth/month
- Additional packs: $5/month per 50GB

### Best Practices for ParaDocs

1. **Separate Sensitive Data**
   ```bash
   # Create structure for sensitive vs. public data
   mkdir -p data/documents/samples  # Sample docs for repo
   mkdir -p data/documents/private  # Real docs (git ignored)
   ```

2. **Use Symbolic Links for Local Development**
   ```bash
   # Link private documents for local use
   mklink /D data\documents\working data\documents\private
   ```

3. **Document Samples Only**
   - Only commit sanitized sample documents
   - Keep real EEOC documents in ignored directories

## Verification Commands

```bash
# Check which files are tracked by LFS
git lfs ls-files

# Check LFS status
git lfs status

# See all files that would be tracked
git lfs track

# Check file sizes before committing
find . -type f -size +1M -exec ls -lh {} \;
```

## Troubleshooting

### If you accidentally commit large files without LFS:
```bash
# Remove from Git history
git rm --cached large_file.pdf
git commit -m "Remove large file"

# Re-add with LFS
git lfs track "*.pdf"
git add large_file.pdf
git commit -m "Add large file with LFS"
```

### If push fails due to large files:
```bash
# Check which files are causing issues
git lfs migrate info --everything

# Migrate existing files to LFS
git lfs migrate import --include="*.pdf,*.xlsx" --everything
```

## Recommended Repository Structure

```
paradocs/
├── .git/
├── .gitattributes       # LFS tracking rules
├── .gitignore          # Ignore patterns
├── README.md           # Project overview
├── requirements.txt    # Python dependencies
├── src/               # Source code
│   ├── __init__.py
│   ├── search_documents.py
│   └── search_documents_with_logging.py
├── docs/              # Documentation
│   ├── PROJECT_ORGANIZATION.md
│   ├── INTERACTIVE_REFERENCE_ROADMAP.md
│   └── ...
├── data/
│   ├── samples/       # Example documents (in repo)
│   │   └── README.md  # Explains sample data
│   ├── generated/     # Generated files (in repo)
│   │   ├── document_index.json (LFS)
│   │   └── CATEGORY_REPORT.md
│   └── documents/     # Real documents (git ignored)
│       └── .gitkeep
├── config/           # Configuration files
├── tests/           # Unit tests
└── scripts/         # Utility scripts
```

## Security Checklist

- [ ] Repository is PRIVATE
- [ ] Real documents are in .gitignored directories
- [ ] Only sanitized samples are committed
- [ ] No personally identifiable information in commits
- [ ] LFS is tracking all large binary files
- [ ] Sensitive paths are in .gitignore

## Next Steps

1. Complete Git LFS setup
2. Create private repository on GitHub
3. Push initial structure
4. Create `data/samples/` with sanitized examples
5. Move real documents to ignored directories
6. Set up GitHub Actions for automated testing

Remember: Never commit actual EEOC documents with sensitive information. Use Git LFS for large files, but keep sensitive data local only. 