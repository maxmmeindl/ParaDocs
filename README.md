# ParaDocs - EEO Document Management System

## Overview
ParaDocs is an organized document management system for EEO (Equal Employment Opportunity) files, including FY 2021 complaint tables, forms, manuals, and related documentation.

## Quick Start

### 1. Initial Setup
First, scan and index all documents in the directory:
```bash
python search_documents.py scan
```

This will:
- Scan all documents in the current directory
- Create a searchable index (`document_index.json`)
- Generate a category report (`CATEGORY_REPORT.md`)

### 2. Search Documents

#### Basic Search
```bash
python search_documents.py search -q "counseling"
```

#### Search with Filters
```bash
# Search by category
python search_documents.py search -q "complaint" -c "adr"

# Search by year
python search_documents.py search -q "workforce" -y "2021"

# Search by file type
python search_documents.py search -q "manual" -t "pdf"
```

### 3. List Categories and Years
```bash
python search_documents.py list
```

### 4. Generate Reports
```bash
python search_documents.py report
```

## Document Categories

- **Workforce & Complaints**: Employee and complaint statistics
- **Counseling**: Pre-complaint counseling data
- **ADR**: Alternative Dispute Resolution information
- **Timeliness**: Processing time and deadline compliance
- **Closures**: Complaint closure types and outcomes
- **Benefits**: Settlement benefits and resources
- **Training**: Staff training records
- **Forms**: Official forms and templates
- **Manuals**: Instruction manuals and guides

## File Structure

```
ParaDocs/
├── PROJECT_ORGANIZATION.md    # Detailed organization guide
├── README.md                  # This file
├── search_documents.py        # Search tool
├── document_index.json        # Generated document index
├── CATEGORY_REPORT.md         # Generated category report
├── paradocs-agent/            # Document processing tools
└── [Your document files]      # EEO tables, forms, and manuals
```

## Search Examples

### Find all ADR-related documents:
```bash
python search_documents.py search -q "adr"
```

### Find training tables:
```bash
python search_documents.py search -q "training" -c "training"
```

### Find all 2021 workforce data:
```bash
python search_documents.py search -q "workforce" -y "2021"
```

### Find Form 462:
```bash
python search_documents.py search -q "462"
```

## Advanced Usage

### Using the Document Index
The `document_index.json` file contains detailed metadata for all documents:
- Document ID
- Original filename
- Category
- Keywords
- Description
- File path
- Last modified date

You can also search this file directly using any JSON viewer or text editor.

### Category Report
The `CATEGORY_REPORT.md` file provides a organized view of all documents grouped by category, making it easy to browse related documents.

## Tips for Effective Searching

1. **Use keywords**: Common keywords include "complaint", "counseling", "adr", "training", "benefits"
2. **Filter by category**: Narrow results by specifying a category
3. **Check the category report**: Browse `CATEGORY_REPORT.md` for a visual overview
4. **Rescan after changes**: Run `python search_documents.py scan` after adding new documents

## Troubleshooting

### "No index found" error
Run `python search_documents.py scan` to create the index.

### Missing Python
Ensure Python 3.6+ is installed. Check with `python --version`.

### Permission errors
Make sure you have read permissions for all document files.

## Future Enhancements

See `PROJECT_ORGANIZATION.md` for planned improvements including:
- Directory reorganization
- Enhanced metadata
- Full-text search
- Web interface

---

For more detailed information about the project organization strategy, see `PROJECT_ORGANIZATION.md`.
