# ParaDocs - Legal Document Management System

A comprehensive, compliance-focused document management system for EEOC case management and legal document processing.

## 🎯 Overview

ParaDocs is a "living" repository system designed to manage Equal Employment Opportunity Commission (EEOC) cases and Federal Emergency Management Agency (FEMA) employment actions. It provides automated document processing, compliance validation, searchable indexing, and audit trail capabilities while maintaining strict adherence to federal regulations.

## 🏗️ Architecture

```
paradocs/
├── docs/                    # Document storage
│   ├── raw/                # Original documents
│   │   ├── EEOC/          # EEOC documents by case
│   │   ├── FEMA/          # FEMA documents by case
│   │   └── OTHER/         # Other agency documents
│   └── processed/         # OCR output and metadata
├── src/                    # Source code modules
│   ├── ingestion/         # Document intake and OCR
│   ├── validation/        # Compliance validation
│   ├── indexing/          # Search index creation
│   └── workflow/          # Automation and alerts
├── config/                 # Configuration files
│   ├── compliance-rules/  # EEOC/FEMA regulations
│   ├── metadata_schema.json
│   └── cursor.rules.json
├── scripts/               # Automation scripts
├── search_index/          # Generated search indexes
├── logs/                  # Processing logs
└── backup/               # Backup storage
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git with Git LFS
- PowerShell (Windows) or Bash (Linux/Mac)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/paradocs.git
   cd paradocs
   ```

2. **Initialize Git LFS**
   ```bash
   git lfs install
   ```

3. **Set up the folder structure**
   ```powershell
   ./scripts/create_paradocs_structure.ps1
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables**
   ```bash
   # For Census API (NAICS validation)
   export CENSUS_API_KEY="your-api-key"
   ```

### First Run

1. **Migrate existing files** (dry run first)
   ```powershell
   ./scripts/migrate_existing_files.ps1 -DryRun true
   # Review output, then run:
   ./scripts/migrate_existing_files.ps1 -DryRun false
   ```

2. **Process documents**
   ```bash
   python scripts/run_pipeline.py
   ```

3. **Generate search indexes**
   ```bash
   python scripts/run_indexing.py
   ```

## 📋 Features

### Document Processing
- **likely Classification**: Documents are classified by agency (EEOC/FEMA) and type
- **Metadata Extraction**: likely extraction of dates, case numbers, parties, and violations
- **OCR Support**: Process scanned documents (OCR integration ready)
- **Hash Verification**: SHA-256 hashing for document integrity

### Compliance Validation
- **EEOC Rules**: 29 CFR 1630 (ADA), 29 CFR 1614 (Federal Sector EEO)
- **FEMA Rules**: 44 CFR 206, 5 CFR 752 (Adverse Actions), 5 USC 2302
- **NAICS Code Validation**: Real-time validation via Census API
- **Workforce Snapshot**: EEO-1 reporting date compliance
- **Deadline Tracking**: likely extraction and monitoring of critical dates

### Search & Indexing
- **Keyword Index**: Full-text search across all documents
- **Date Index**: Timeline-based document retrieval
- **Metadata Search**: Search by case number, parties, violations, etc.
- **Legal Citation Index**: likely extraction of regulation references

### Security & Audit
- **Chain of Custody**: Complete audit trail for every document
- **Access Control**: Role-based permissions (ready for implementation)
- **Privacy Compliance**: FOIA and Privacy Act adherence
- **Immutable Logs**: Tamper-resistant logging system

## 🔧 Configuration

### Metadata Schema
Documents are tagged with comprehensive metadata including:
- Document type and classification
- Agency and regulation references
- Case numbers and party information
- Critical dates and deadlines
- Processing and validation status

See `config/metadata_schema.json` for the complete schema.

### Compliance Rules
Agency-specific rules are defined in:
- `config/compliance-rules/eeoc-rules.json`
- `config/compliance-rules/fema-rules.json`

### AI Integration
Claude Opus prompt templates are configured in `config/cursor.rules.json` for:
- EEOC compliance validation
- EEO-1 classification
- Deadline extraction
- Violation identification
- Metadata extraction

## 📊 Usage Examples

### Search for Documents
```python
# Using the generated indexes
import json

# Load keyword index
with open('search_index/keyword_index.json', 'r') as f:
    keyword_index = json.load(f)

# Find all documents mentioning "reasonable accommodation"
for entry in keyword_index:
    if entry['keyword'] == 'reasonable accommodation':
        print(f"Found in {len(entry['documents'])} documents")
        for doc in entry['documents']:
            print(f"  - {doc}")
```

### Validate a Document
```python
from src.validation.naics_validator import NAICSValidator

validator = NAICSValidator()
valid, description = validator.validate("922140")
print(f"NAICS 922140: {description if valid else 'Invalid'}")
```

### Generate Timeline Report
```python
# Load date index
with open('search_index/date_index.json', 'r') as f:
    date_index = json.load(f)

# Find all events in 2024
events_2024 = [entry for entry in date_index if entry['date'].startswith('2024')]
print(f"Found {len(events_2024)} events in 2024")
```

## 🛡️ Legal Compliance

### EEOC Requirements
- Title VII compliance tracking
- ADA reasonable accommodation documentation
- Interactive process timeline management
- Confidentiality protections

### FOIA Compliance
- Dual-layer architecture (public/confidential)
- Automated redaction capabilities (planned)
- Request tracking and deadline management
- Exemption categorization

### Privacy Act
- System of Records Notice (SORN) compliance
- Individual access rights management
- Purpose limitation enforcement
- Consent tracking

## 🔄 Automation

### Folder Monitoring
The system can watch for new documents and automatically process them:
```powershell
# Coming soon: watch_folder.ps1
```

### Scheduled Processing
Set up daily processing via Task Scheduler (Windows) or cron (Linux):
```bash
# Run daily at 2 AM
0 2 * * * /usr/bin/python /path/to/paradocs/scripts/run_pipeline.py
```

## 🐛 Troubleshooting

### Common Issues

1. **"No metadata file found"**
   - Ensure documents are in the `docs/raw` directory
   - Run the processing pipeline: `python scripts/run_pipeline.py`

2. **"Census API error"**
   - Check your CENSUS_API_KEY environment variable
   - Verify internet connectivity

3. **"Git LFS not initialized"**
   - Run `git lfs install` in the repository

### Logs
Check logs in the `logs/` directory for detailed error information:
```bash
tail -f logs/pipeline_*.log
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure all validations pass
4. Submit a pull request

## 📝 License

This project is proprietary and confidential. All rights reserved.

## 🆘 Support

For support, please contact the ParaDocs administrator or file an issue in the project repository.

---

**Remember**: This system handles sensitive legal documents. Always ensure proper authorization before accessing or modifying any files.
