#!/usr/bin/env python3
"""
ParaDocs Master Pipeline Script
Orchestrates document processing, validation, and indexing
"""

import os
import sys
import json
import logging
import hashlib
import shutil  # Added for file copying/quarantine
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.validation.naics_validator import NAICSValidator, check_workforce_snapshot

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"pipeline_{datetime.now():%Y%m%d_%H%M%S}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes raw documents into validated, indexed format"""
    
    def __init__(self):
        self.config = self._load_config()
        self.metadata_schema = self._load_metadata_schema()
        self.compliance_rules = self._load_compliance_rules()
        self.naics_validator = NAICSValidator()
        self.stats = {
            "processed": 0,
            "validated": 0,
            "errors": 0,
            "warnings": 0
        }
    
    def _load_config(self) -> Dict:
        """Load cursor.rules.json configuration"""
        config_path = Path("config/cursor.rules.json")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning("Config file not found, using defaults")
            return {}
    
    def _load_metadata_schema(self) -> Dict:
        """Load metadata schema"""
        schema_path = Path("config/metadata_schema.json")
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning("Metadata schema not found")
            return {}
    
    def _load_compliance_rules(self) -> Dict:
        """Load compliance rules"""
        rules = {}
        rules_dir = Path("config/compliance-rules")
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.json"):
                with open(rule_file, 'r') as f:
                    agency = rule_file.stem.split('-')[0].upper()
                    rules[agency] = json.load(f)
        return rules
    
    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _extract_case_number(self, filepath: Path) -> str:
        """Extract case number from file path or name"""
        # Check parent directory first
        parent = filepath.parent.name
        if parent not in ["EEOC", "FEMA", "OTHER"]:
            return parent
        
        # Try to extract from filename
        import re
        patterns = [
            r'HS-FEMA-\d{5}-\d{4}',
            r'EEO-\d{2}-\d{5}',
            r'\d{4}-EEO-\d{2}-\d{5}',
            r'CASE-\d{4}-\d{3}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filepath.name)
            if match:
                return match.group(0)
        
        return "UNKNOWN"
    
    def _classify_document(self, filepath: Path) -> List[str]:
        """Classify document type based on filename and content"""
        doc_types = []
        filename_lower = filepath.name.lower()
        
        # Richer classification dictionary – easy to extend with external JSON later
        type_patterns = {
            # External filings / charges
            "EEOC_Charge": ["eeoc charge", "formal complaint", "eeo complaint", "form 5", "form 256"],

            # Accommodation process
            "Interactive_Process": ["interactive process", "ipa meeting", "ra meeting", "ra discussion"],

            # Medical evidence / FMLA / doctor letters
            "Medical_Documentation": [
                "medical", "doctor", "physician", "fmla", "ada form", "hipaa", "phi", "clinic", "diagnosis", "form 256-0", "medication"
            ],

            # Email or message exports
            "Email_Communication": [".eml", ".msg", "all mail items", "inbox", "outlook", "gmail"],

            # Personnel actions
            "Agency_Action": [
                "termination", "removal", "separation", "notice of decision", "ndr letter", "denial", "response", "final agency decision", "fad"
            ],

            # Policy / directive / manuals
            "Policy_Guidance": [
                "policy", "directive", "manual", "instruction", "guide", "handbook", "256-", "fd-", "fema manual", "opm"],

            # Investigation materials
            "Investigation_File": ["roi", "investigation", "affidavit", "tab f-", "witness statement"],

            # Timelines or event tables
            "Timeline_Document": ["timeline", "chronology", "table of events"],

            # Financial / damages
            "Damage_Calculation": ["damage", "back pay", "lost wage", "compensatory", "monetary"],
        }
        
        for doc_type, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in filename_lower:
                    doc_types.append(doc_type)
                    break
        
        if not doc_types:
            doc_types.append("Other")
        
        return doc_types
    
    def _create_initial_metadata(self, filepath: Path) -> Dict:
        """Create initial metadata for a document"""
        now = datetime.now().isoformat()
        agency = filepath.parent.parent.name  # e.g., docs/raw/EEOC/case/file
        
        metadata = {
            "document_id": f"{agency}-{filepath.stem}-{datetime.now():%Y%m%d}",
            "document_type": self._classify_document(filepath),
            "agency": [agency] if agency in ["EEOC", "FEMA"] else ["OTHER"],
            "case_number": self._extract_case_number(filepath),
            "created_date": datetime.now().date().isoformat(),
            "file_info": {
                "original_filename": filepath.name,
                "file_size": filepath.stat().st_size,
                "file_hash": self._calculate_file_hash(filepath),
                "mime_type": self._get_mime_type(filepath)
            },
            "processing_info": {
                "processed_date": now,
                "validation_status": "Pending",
                "validation_errors": []
            },
            "audit_trail": [{
                "timestamp": now,
                "action": "Created",
                "user": os.environ.get('USERNAME', 'system'),
                "details": "Initial metadata creation"
            }]
        }
        
        return metadata
    
    def _get_mime_type(self, filepath: Path) -> str:
        """Get MIME type based on file extension"""
        ext_map = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.eml': 'message/rfc822',
            '.msg': 'application/vnd.ms-outlook',
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.csv': 'text/csv',
            '.html': 'text/html'
        }
        return ext_map.get(filepath.suffix.lower(), 'application/octet-stream')
    
    def _extract_text(self, filepath: Path) -> Optional[str]:
        """Extract full-text from common legal file types.

        Returns the extracted text or None if extraction fails.
        Dependencies are imported lazily so the script still runs even
        if optional OCR packages are missing.  Failures are logged but
        do **not** crash the pipeline – the file will be quarantined.
        """
        try:
            suffix = filepath.suffix.lower()

            # -------- PDF --------
            if suffix == '.pdf':
                try:
                    from pdfminer.high_level import extract_text  # type: ignore
                except ModuleNotFoundError:
                    logger.error("pdfminer.six not installed – cannot OCR PDFs")
                    return None
                return extract_text(str(filepath))

            # -------- DOCX / DOC --------
            if suffix == '.docx':
                try:
                    from docx import Document  # type: ignore
                except ModuleNotFoundError:
                    logger.error("python-docx not installed – cannot read .docx files")
                    return None
                return "\n".join(p.text for p in Document(str(filepath)).paragraphs)

            if suffix == '.doc':
                try:
                    import textract  # type: ignore
                except ModuleNotFoundError:
                    logger.error("textract not installed – cannot read .doc files")
                    return None
                return textract.process(str(filepath)).decode('utf-8', errors='ignore')

            # -------- E-mail --------
            if suffix in ('.eml', '.msg'):
                try:
                    import mailparser  # type: ignore
                    mail = mailparser.parse_from_file(str(filepath))
                    return mail.body or ''
                except Exception:
                    try:
                        import extract_msg  # type: ignore
                        msg = extract_msg.Message(str(filepath))
                        return msg.body or ''
                    except Exception as e:
                        logger.error(f"E-mail extraction failed: {e}")
                        return None

            # Other types not handled – skip
            return ''

        except Exception as e:
            logger.error(f"Text extraction failed for {filepath}: {e}")
            return None
    
    def validate_metadata(self, metadata: Dict) -> List[str]:
        """Validate metadata against schema and compliance rules"""
        errors = []
        
        # Check required fields
        required_fields = ["document_id", "document_type", "agency", "case_number", "created_date"]
        for field in required_fields:
            if field not in metadata or not metadata[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate NAICS code if present
        if "naics_code" in metadata:
            valid, desc = self.naics_validator.validate(metadata["naics_code"])
            if not valid:
                errors.append(f"Invalid NAICS code: {desc}")
        
        # Validate workforce snapshot if present
        if "workforce_snapshot" in metadata:
            valid, msg = check_workforce_snapshot(metadata["workforce_snapshot"])
            if not valid:
                errors.append(f"Invalid workforce snapshot: {msg}")
        
        # Check agency-specific rules
        agencies = metadata.get("agency", [])
        for agency in agencies:
            if agency in self.compliance_rules:
                # Validate against agency rules
                # This is simplified - in practice would be more complex
                pass
        
        return errors
    
    def process_document(self, raw_path: Path) -> bool:
        """Process a single document"""
        logger.info(f"Processing: {raw_path}")
        
        try:
            # Create processed directory structure
            relative_path = raw_path.relative_to("docs/raw")
            processed_path = Path("docs/processed") / relative_path
            processed_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if already processed
            json_path = processed_path.with_suffix('.json')
            if json_path.exists():
                logger.info(f"Already processed: {raw_path}")
                return True
            
            # Create initial metadata
            metadata = self._create_initial_metadata(raw_path)
            
            # ----------------------------------------------------------
            # 🆕 Copy raw file to processed dir & extract text
            # ----------------------------------------------------------
            shutil.copy2(raw_path, processed_path)

            text_content = self._extract_text(raw_path)

            if text_content is not None:
                txt_path = processed_path.with_suffix('.txt')
                try:
                    with open(txt_path, 'w', encoding='utf-8') as f_txt:
                        f_txt.write(text_content)
                except Exception as e:
                    logger.error(f"Failed to write text file for {raw_path}: {e}")

            else:
                # Mark extraction failure in metadata (will still continue)
                metadata.setdefault('processing_info', {}).setdefault('validation_errors', []).append(
                    'TEXT_EXTRACTION_FAILED')
            
            # Validate metadata
            errors = self.validate_metadata(metadata)
            if errors:
                metadata["processing_info"]["validation_status"] = "Failed"
                metadata["processing_info"]["validation_errors"] = errors
                logger.warning(f"Validation errors for {raw_path}: {errors}")
                self.stats["warnings"] += len(errors)

                # Quarantine: copy raw file & metadata to docs/quarantine/
                quarantine_base = Path('docs/quarantine') / relative_path
                quarantine_base.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(raw_path, quarantine_base)
                    with open(quarantine_base.with_suffix('.err.json'), 'w', encoding='utf-8') as f_err:
                        json.dump(metadata, f_err, indent=2)
                except Exception as q_err:
                    logger.error(f"Failed to quarantine {raw_path}: {q_err}")
            else:
                metadata["processing_info"]["validation_status"] = "Validated"
                self.stats["validated"] += 1
            
            # Save metadata
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Update audit trail
            metadata["audit_trail"].append({
                "timestamp": datetime.now().isoformat(),
                "action": "Processed",
                "user": os.environ.get('USERNAME', 'system'),
                "details": f"Processed with {len(errors)} validation errors"
            })
            
            self.stats["processed"] += 1
            logger.info(f"Successfully processed: {raw_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {raw_path}: {e}")
            self.stats["errors"] += 1
            return False
    
    def process_all_documents(self):
        """Process all documents in raw directory"""
        raw_dir = Path("docs/raw")
        if not raw_dir.exists():
            logger.error("Raw documents directory not found!")
            return
        
        # Find all documents to process
        extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.eml', '.msg']
        documents = []
        for ext in extensions:
            documents.extend(raw_dir.rglob(f"*{ext}"))
        
        logger.info(f"Found {len(documents)} documents to process")
        
        # Process each document
        for doc in documents:
            self.process_document(doc)
        
        # Print summary
        logger.info("Processing complete!")
        logger.info(f"Processed: {self.stats['processed']}")
        logger.info(f"Validated: {self.stats['validated']}")
        logger.info(f"Warnings: {self.stats['warnings']}")
        logger.info(f"Errors: {self.stats['errors']}")


def main():
    """Main execution function"""
    logger.info("Starting ParaDocs pipeline...")
    
    # Create processor and run
    processor = DocumentProcessor()
    processor.process_all_documents()
    
    # Run indexing
    logger.info("Running document indexing...")
    import subprocess
    result = subprocess.run([sys.executable, "scripts/run_indexing.py"], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("Indexing completed successfully")
    else:
        logger.error(f"Indexing failed: {result.stderr}")
    
    logger.info("Pipeline complete!")


if __name__ == "__main__":
    main() 