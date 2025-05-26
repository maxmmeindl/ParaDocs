# ParaDocs Project Organization Guide

## Current Project Structure Analysis

Your ParaDocs project appears to be an EEO (Equal Employment Opportunity) document management system containing:
- FY 2021 EEO complaint tables (Excel files)
- Form 462 documentation
- PDF manuals and guides
- A paradocs-agent subdirectory with Python/Node.js tools

## Proposed Organization Structure

### 1. Directory Reorganization

```
ParaDocs/
├── documents/                    # All source documents
│   ├── tables/                  # Excel table files
│   │   ├── fy2021/            # Organized by fiscal year
│   │   └── templates/          # Template files
│   ├── manuals/                # PDF manuals and guides
│   ├── forms/                  # Form templates and examples
│   └── reports/                # Generated reports
├── paradocs-agent/             # Document processing tools
│   ├── scripts/               # Processing scripts
│   ├── config/                # Configuration files
│   └── output/                # Processed outputs
├── database/                   # Document database
│   ├── index/                 # Search indices
│   └── metadata/              # Document metadata
└── docs/                      # Project documentation
    ├── README.md
    ├── USER_GUIDE.md
    └── API_DOCS.md
```

### 2. Document Categorization

#### Tables by Category:
- **Workforce & Complaints**: Tables B-1, B-1a
- **Counseling**: Tables B-2, B-2a, B-3, B-3a
- **ADR (Alternative Dispute Resolution)**: Tables B-4, B-5, B-19, B-20
- **Processing & Timeliness**: Tables B-7, B-7a, B-10, B-12, B-14, B-14a, B-17, B-18
- **Closures & Outcomes**: Tables B-11, B-11a, B-13, B-15, B-16
- **Benefits & Resources**: Tables B-6, B-21, B-24, B-24a
- **Training**: Tables B-25 through B-28
- **Other**: Tables B-8, B-9, B-22, B-23

### 3. Search Implementation Strategy

#### A. Metadata System
Create a metadata file for each document containing:
- Document title
- Category
- Fiscal year
- Keywords
- Description
- Last modified date
- File type

#### B. Search Index
Implement a search system using:
1. **File naming convention**: `[CATEGORY]_[YEAR]_[TABLE-NUMBER]_[DESCRIPTION].xlsx`
2. **Full-text search**: Index document contents
3. **Tag system**: Add searchable tags to each document

### 4. Implementation Steps

#### Step 1: Create Directory Structure
```bash
mkdir -p documents/{tables/{fy2021,templates},manuals,forms,reports}
mkdir -p database/{index,metadata}
mkdir -p docs
mkdir -p paradocs-agent/{scripts,config,output}
```

#### Step 2: Move and Rename Files
- Move all Table B-* files to `documents/tables/fy2021/`
- Move PDF files to `documents/manuals/`
- Move forms to `documents/forms/`

#### Step 3: Create Document Index
Generate a master index file (`documents/INDEX.json`) containing:
```json
{
  "documents": [
    {
      "id": "001",
      "filename": "workforce_complaints_fy2021_b1.xlsx",
      "original_name": "Table B-1 FY 2021 Total Work Force, Counselings, and Complaints.xlsx",
      "category": "workforce",
      "year": "2021",
      "table": "B-1",
      "keywords": ["workforce", "counseling", "complaints", "total"],
      "description": "Total workforce data with counseling and complaint statistics",
      "path": "documents/tables/fy2021/workforce_complaints_fy2021_b1.xlsx"
    }
  ]
}
```

#### Step 4: Create Search Tool
Develop a simple search tool that can:
- Search by filename
- Search by keywords
- Filter by category
- Filter by year
- Search within document contents

### 5. Quick Access Features

#### A. Category Views
Create category-specific index files:
- `ADR_documents.md`
- `Training_documents.md`
- `Timeliness_documents.md`

#### B. Quick Reference Guide
Create a one-page reference showing:
- Most frequently accessed documents
- Document relationships
- Common search queries

### 6. Maintenance Plan

1. **Regular Updates**: Schedule monthly reviews
2. **Version Control**: Track document changes
3. **Backup Strategy**: Regular backups of all documents
4. **Access Log**: Track which documents are accessed most

## Next Steps

1. Backup current structure
2. Implement new directory structure
3. Create metadata for all documents
4. Build search functionality
5. Create user documentation

This organization will make your documents easily searchable through:
- Logical directory structure
- Consistent naming conventions
- Comprehensive metadata
- Search indices
- Category-based organization 