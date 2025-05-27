#!/usr/bin/env python3
"""
Document Indexing Script
Generates keyword and date-based search indexes for ParaDocs
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentIndexer:
    """Creates searchable indexes for legal documents"""
    
    def __init__(self, processed_dir: str = "docs/processed"):
        self.processed_dir = Path(processed_dir)
        self.keyword_index = defaultdict(lambda: {"documents": [], "counts": {}})
        self.date_index = defaultdict(list)
        self.metadata_cache = {}
        
    def load_document_metadata(self, json_path: Path) -> Dict:
        """Load metadata from JSON sidecar file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metadata from {json_path}: {e}")
            return {}
    
    def extract_keywords(self, metadata: Dict, text_content: str = "") -> Set[str]:
        """Extract keywords from metadata and text content"""
        keywords = set()
        
        # From metadata
        if 'keywords' in metadata:
            keywords.update(metadata['keywords'])
        
        # Case numbers
        if 'case_number' in metadata:
            keywords.add(metadata['case_number'].lower())
        
        # Regulation references
        if 'regulation_refs' in metadata:
            for ref in metadata['regulation_refs']:
                keywords.add(ref.lower())
        
        # Document types
        if 'document_type' in metadata:
            for doc_type in metadata['document_type']:
                keywords.add(doc_type.lower())
        
        # Party names
        if 'parties' in metadata:
            for party_type, names in metadata['parties'].items():
                if isinstance(names, list):
                    for name in names:
                        keywords.add(name.lower())
        
        # From text content - extract legal terms and citations
        if text_content:
            # Legal citations (e.g., "29 CFR 1630.2(o)")
            citations = re.findall(r'\d+\s+[A-Z]+\s+[\d.()a-z]+', text_content)
            keywords.update([c.lower() for c in citations])
            
            # Common legal terms
            legal_terms = [
                "discrimination", "retaliation", "reasonable accommodation",
                "interactive process", "undue hardship", "essential functions",
                "hostile work environment", "disparate treatment", "disparate impact",
                "protected class", "adverse action", "whistleblower"
            ]
            
            for term in legal_terms:
                if term in text_content.lower():
                    keywords.add(term)
        
        return keywords
    
    def extract_dates(self, metadata: Dict, filename: str) -> List[Tuple[str, str]]:
        """Extract dates from metadata and filename"""
        dates = []
        
        # From metadata fields
        date_fields = [
            'event_date', 'created_date', 'received_date', 
            'workforce_snapshot', 'processing_info.processed_date'
        ]
        
        for field in date_fields:
            if '.' in field:
                # Handle nested fields
                parts = field.split('.')
                value = metadata
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                if value:
                    dates.append((value, f"metadata.{field}"))
            elif field in metadata:
                dates.append((metadata[field], f"metadata.{field}"))
        
        # From deadlines array
        if 'deadlines' in metadata:
            for deadline in metadata['deadlines']:
                if 'date' in deadline:
                    dates.append((deadline['date'], "metadata.deadlines"))
        
        # From filename (ISO dates)
        filename_dates = re.findall(r'\d{4}-\d{2}-\d{2}', filename)
        for date_str in filename_dates:
            dates.append((date_str, "filename"))
        
        return dates
    
    def process_document(self, doc_path: Path):
        """Process a single document for indexing"""
        logger.info(f"Processing: {doc_path}")
        
        # Look for JSON metadata file
        json_path = doc_path.with_suffix('.json')
        if not json_path.exists():
            logger.warning(f"No metadata file found for {doc_path}")
            return
        
        metadata = self.load_document_metadata(json_path)
        if not metadata:
            return
        
        # Load text content if available
        text_content = ""
        text_path = doc_path.with_suffix('.txt')
        if text_path.exists():
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            except Exception as e:
                logger.error(f"Failed to read text content: {e}")
        
        # Extract keywords
        keywords = self.extract_keywords(metadata, text_content)
        
        # Update keyword index
        for keyword in keywords:
            self.keyword_index[keyword]["documents"].append(str(doc_path))
            # Count occurrences in text
            if text_content:
                count = text_content.lower().count(keyword)
                self.keyword_index[keyword]["counts"][str(doc_path)] = count
        
        # Extract and index dates
        dates = self.extract_dates(metadata, doc_path.name)
        for date_str, source in dates:
            self.date_index[date_str].append({
                "file": str(doc_path),
                "source": source
            })
    
    def scan_documents(self):
        """Scan all documents in processed directory"""
        logger.info(f"Scanning documents in {self.processed_dir}")
        
        # Find all JSON metadata files
        json_files = list(self.processed_dir.rglob("*.json"))
        logger.info(f"Found {len(json_files)} metadata files")
        
        for json_path in json_files:
            # Skip index files
            if json_path.name in ['keyword_index.json', 'date_index.json']:
                continue
                
            # Process the document (using base name without .json)
            doc_path = json_path.with_suffix('')
            self.process_document(doc_path)
    
    def save_indexes(self):
        """Save generated indexes to JSON files"""
        # Convert keyword index to list format
        keyword_list = []
        for keyword, data in self.keyword_index.items():
            keyword_list.append({
                "keyword": keyword,
                "documents": data["documents"],
                "counts": data["counts"]
            })
        
        # Sort by number of documents (most common keywords first)
        keyword_list.sort(key=lambda x: len(x["documents"]), reverse=True)
        
        # Save keyword index
        keyword_index_path = Path("search_index/keyword_index.json")
        keyword_index_path.parent.mkdir(exist_ok=True)
        
        with open(keyword_index_path, 'w', encoding='utf-8') as f:
            json.dump(keyword_list, f, indent=2)
        logger.info(f"Saved keyword index with {len(keyword_list)} keywords")
        
        # Convert date index to list format
        date_list = []
        for date, files in self.date_index.items():
            date_list.append({
                "date": date,
                "files": files
            })
        
        # Sort by date
        date_list.sort(key=lambda x: x["date"])
        
        # Save date index
        date_index_path = Path("search_index/date_index.json")
        
        with open(date_index_path, 'w', encoding='utf-8') as f:
            json.dump(date_list, f, indent=2)
        logger.info(f"Saved date index with {len(date_list)} dates")
        
        # Generate summary statistics
        stats = {
            "generated_at": datetime.now().isoformat(),
            "total_documents": len(set(doc for k in self.keyword_index.values() 
                                     for doc in k["documents"])),
            "total_keywords": len(keyword_list),
            "total_dates": len(date_list),
            "most_common_keywords": [
                {
                    "keyword": k["keyword"],
                    "document_count": len(k["documents"])
                }
                for k in keyword_list[:20]
            ]
        }
        
        stats_path = Path("search_index/index_stats.json")
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        logger.info("Saved index statistics")


def main():
    """Main execution function"""
    logger.info("Starting document indexing...")
    
    # Check if processed directory exists
    if not Path("docs/processed").exists():
        logger.error("Processed documents directory not found!")
        logger.info("Please run document processing pipeline first.")
        return
    
    # Create indexer and run
    indexer = DocumentIndexer()
    indexer.scan_documents()
    indexer.save_indexes()
    
    logger.info("Indexing complete!")
    
    # Print summary
    print("\n=== Indexing Summary ===")
    print(f"Documents indexed: {len(set(doc for k in indexer.keyword_index.values() for doc in k['documents']))}")
    print(f"Keywords found: {len(indexer.keyword_index)}")
    print(f"Dates found: {len(indexer.date_index)}")
    print(f"\nIndexes saved to: search_index/")
    print("  - keyword_index.json")
    print("  - date_index.json")
    print("  - index_stats.json")


if __name__ == "__main__":
    main() 