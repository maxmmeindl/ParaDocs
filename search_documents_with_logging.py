#!/usr/bin/env python3
"""
ParaDocs Document Search Tool with Logging
Search and organize EEO documents efficiently with full action tracking
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import argparse
import shutil

class ActionLogger:
    """Handles logging of all actions to ACTION_LOG.md"""
    
    def __init__(self, log_file="ACTION_LOG.md"):
        self.log_file = Path(log_file)
        
    def log_action(self, action_type, details, results=None):
        """Add an action entry to the log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Read existing log
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = self._create_initial_log()
        
        # Find the Action History section
        history_marker = "## Action History"
        if history_marker in content:
            # Insert new entry after the Action History marker
            parts = content.split(history_marker, 1)
            
            # Create new entry
            entry = f"\n\n### {timestamp} - {action_type}\n"
            entry += f"- **Action**: {details}\n"
            
            if results:
                entry += "- **Results**:\n"
                for key, value in results.items():
                    entry += f"  - {key}: {value}\n"
            
            # Reconstruct content
            content = parts[0] + history_marker + entry + parts[1]
        
        # Write updated log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_initial_log(self):
        """Create initial log structure"""
        return """# ParaDocs Action Log

## Project Overview
**Purpose**: Interactive reference guide for legal documentation based on EEOC materials
**Started**: """ + datetime.now().strftime("%B %d, %Y") + """
**Initial Setup By**: System Administrator

---

## Action History

---

## Notes
- System designed to be extensible for additional documents
- All actions are logged with timestamps
- Original file structure preserved during initial implementation
- Search index can be regenerated at any time with `scan` command

---

*This log will be continuously updated as the system evolves*
"""

class DocumentSearcher:
    def __init__(self, base_path=".", enable_logging=True):
        self.base_path = Path(base_path)
        self.index_file = self.base_path / "document_index.json"
        self.documents = []
        self.logger = ActionLogger() if enable_logging else None
        
    def scan_documents(self):
        """Scan the directory and build document index"""
        print("Scanning documents...")
        documents = []
        doc_id = 1
        
        # Define patterns for different document types
        table_pattern = re.compile(r'Table B-(\d+[a-z]?)\s+FY (\d{4})\s+(.+)\.(xlsx|xls)')
        
        # Track statistics
        stats = {
            'total_files': 0,
            'by_type': {},
            'by_category': {}
        }
        
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.xlsx', '.xls', '.docx', '.pdf']:
                # Skip log files and indices
                if file_path.name in ['document_index.json', 'ACTION_LOG.md', 'CATEGORY_REPORT.md']:
                    continue
                    
                # Extract metadata from filename
                filename = file_path.name
                
                doc_info = {
                    'id': f'{doc_id:03d}',
                    'filename': filename,
                    'path': str(file_path.relative_to(self.base_path)),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'type': file_path.suffix[1:],
                    'keywords': []
                }
                
                # Update type statistics
                file_type = doc_info['type']
                stats['by_type'][file_type] = stats['by_type'].get(file_type, 0) + 1
                
                # Parse table files
                table_match = table_pattern.match(filename)
                if table_match:
                    table_num = table_match.group(1)
                    year = table_match.group(2)
                    description = table_match.group(3)
                    
                    doc_info['table'] = f'B-{table_num}'
                    doc_info['year'] = year
                    doc_info['description'] = description
                    
                    # Categorize based on table number
                    doc_info['category'] = self._categorize_table(table_num, description)
                    doc_info['keywords'] = self._extract_keywords(description)
                
                # Handle other document types
                elif 'Form 462' in filename:
                    doc_info['category'] = 'forms'
                    doc_info['keywords'] = ['form', '462', 'complaints']
                elif filename.endswith('.pdf'):
                    doc_info['category'] = 'manuals'
                    doc_info['keywords'] = self._extract_keywords(filename)
                
                # Update category statistics
                category = doc_info.get('category', 'uncategorized')
                stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                
                documents.append(doc_info)
                doc_id += 1
        
        self.documents = documents
        stats['total_files'] = len(documents)
        
        print(f"Found {len(documents)} documents")
        
        # Log the action
        if self.logger:
            self.logger.log_action(
                "Document Scan",
                f"Scanned directory {self.base_path}",
                {
                    "Total documents found": stats['total_files'],
                    "File types": ", ".join([f"{k}: {v}" for k, v in stats['by_type'].items()]),
                    "Categories": ", ".join([f"{k}: {v}" for k, v in stats['by_category'].items()])
                }
            )
        
        return documents
    
    def _categorize_table(self, table_num, description):
        """Categorize tables based on their number and description"""
        categories = {
            'workforce': ['1', '1a'],
            'counseling': ['2', '2a', '3', '3a'],
            'adr': ['4', '5', '19', '20'],
            'timeliness': ['7', '7a', '10', '12', '14', '14a', '17', '18'],
            'closures': ['11', '11a', '13', '15', '16'],
            'benefits': ['6', '21', '24', '24a'],
            'training': ['25', '26', '27', '28'],
            'complaints': ['8', '9', '22', '23']
        }
        
        for category, numbers in categories.items():
            if table_num in numbers:
                return category
        
        return 'other'
    
    def _extract_keywords(self, text):
        """Extract keywords from text"""
        # Common EEO-related keywords
        keywords = []
        text_lower = text.lower()
        
        keyword_map = {
            'complaint': ['complaint', 'complaints'],
            'counseling': ['counsel', 'counseling'],
            'adr': ['adr', 'alternative', 'dispute', 'resolution'],
            'dismissal': ['dismiss', 'dismissal'],
            'discrimination': ['discriminat'],
            'timely': ['timely', 'timeliness'],
            'processing': ['process', 'processing'],
            'closure': ['closure', 'closed'],
            'workforce': ['workforce', 'work force'],
            'training': ['training'],
            'benefits': ['benefit', 'benefits'],
            'agency': ['agency'],
            'staff': ['staff'],
            'resources': ['resource', 'resources']
        }
        
        for keyword, patterns in keyword_map.items():
            if any(pattern in text_lower for pattern in patterns):
                keywords.append(keyword)
        
        return keywords
    
    def save_index(self):
        """Save document index to JSON file"""
        # Create backup if index exists
        if self.index_file.exists():
            backup_name = self.index_file.with_suffix('.backup.json')
            shutil.copy2(self.index_file, backup_name)
        
        with open(self.index_file, 'w') as f:
            json.dump({'documents': self.documents, 'last_updated': datetime.now().isoformat()}, f, indent=2)
        
        print(f"Index saved to {self.index_file}")
        
        if self.logger:
            self.logger.log_action(
                "Index Update",
                f"Saved document index with {len(self.documents)} documents",
                {"Index file": str(self.index_file), "Document count": len(self.documents)}
            )
    
    def load_index(self):
        """Load document index from JSON file"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                data = json.load(f)
                self.documents = data.get('documents', [])
                last_updated = data.get('last_updated', 'Unknown')
            print(f"Loaded {len(self.documents)} documents from index (Last updated: {last_updated})")
            return True
        return False
    
    def search(self, query, category=None, year=None, doc_type=None):
        """Search documents based on query and filters"""
        results = []
        query_lower = query.lower()
        
        for doc in self.documents:
            # Apply filters
            if category and doc.get('category') != category:
                continue
            if year and doc.get('year') != year:
                continue
            if doc_type and doc.get('type') != doc_type:
                continue
            
            # Search in various fields
            searchable_fields = [
                doc.get('filename', ''),
                doc.get('description', ''),
                ' '.join(doc.get('keywords', [])),
                doc.get('table', ''),
                doc.get('category', '')
            ]
            
            if any(query_lower in field.lower() for field in searchable_fields):
                results.append(doc)
        
        # Log search action
        if self.logger:
            self.logger.log_action(
                "Document Search",
                f"Query: '{query}'",
                {
                    "Results found": len(results),
                    "Filters": f"category={category}, year={year}, type={doc_type}"
                }
            )
        
        return results
    
    def list_categories(self):
        """List all unique categories"""
        categories = set()
        for doc in self.documents:
            if 'category' in doc:
                categories.add(doc['category'])
        return sorted(categories)
    
    def list_years(self):
        """List all unique years"""
        years = set()
        for doc in self.documents:
            if 'year' in doc:
                years.add(doc['year'])
        return sorted(years)
    
    def generate_category_report(self):
        """Generate a report organized by category"""
        report = {}
        for doc in self.documents:
            category = doc.get('category', 'uncategorized')
            if category not in report:
                report[category] = []
            report[category].append(doc)
        
        # Save category report
        report_path = self.base_path / "CATEGORY_REPORT.md"
        with open(report_path, 'w') as f:
            f.write("# ParaDocs Category Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Documents: {len(self.documents)}\n\n")
            
            for category, docs in sorted(report.items()):
                f.write(f"## {category.title()} ({len(docs)} documents)\n\n")
                for doc in sorted(docs, key=lambda x: x.get('table', x['filename'])):
                    f.write(f"- **{doc['filename']}**\n")
                    if 'description' in doc:
                        f.write(f"  - Description: {doc['description']}\n")
                    if 'table' in doc:
                        f.write(f"  - Table: {doc['table']}\n")
                    f.write(f"  - Path: {doc['path']}\n")
                    f.write(f"  - Size: {doc['size']:} bytes\n")
                    f.write("\n")
        
        print(f"Category report saved to {report_path}")
        
        if self.logger:
            self.logger.log_action(
                "Report Generation",
                "Generated category report",
                {"Report file": str(report_path), "Categories": len(report)}
            )
        
        return report
    
    def add_document_note(self, doc_id, note):
        """Add a note to a document (for future annotation features)"""
        for doc in self.documents:
            if doc['id'] == doc_id:
                if 'notes' not in doc:
                    doc['notes'] = []
                doc['notes'].append({
                    'timestamp': datetime.now().isoformat(),
                    'note': note
                })
                self.save_index()
                
                if self.logger:
                    self.logger.log_action(
                        "Document Annotation",
                        f"Added note to document {doc_id}",
                        {"Document": doc['filename'], "Note": note}
                    )
                return True
        return False


def main():
    parser = argparse.ArgumentParser(description='Search ParaDocs documents with logging')
    parser.add_argument('action', choices=['scan', 'search', 'list', 'report', 'log'],
                       help='Action to perform')
    parser.add_argument('-q', '--query', help='Search query')
    parser.add_argument('-c', '--category', help='Filter by category')
    parser.add_argument('-y', '--year', help='Filter by year')
    parser.add_argument('-t', '--type', help='Filter by file type')
    parser.add_argument('--no-log', action='store_true', help='Disable logging')
    
    args = parser.parse_args()
    
    searcher = DocumentSearcher(enable_logging=not args.no_log)
    
    if args.action == 'scan':
        # Scan and index documents
        searcher.scan_documents()
        searcher.save_index()
        searcher.generate_category_report()
        
    elif args.action == 'search':
        # Load index and search
        if not searcher.load_index():
            print("No index found. Run 'scan' first.")
            return
        
        if not args.query:
            print("Please provide a search query with -q")
            return
        
        results = searcher.search(args.query, args.category, args.year, args.type)
        
        print(f"\nFound {len(results)} results for '{args.query}':\n")
        for doc in results:
            print(f"- {doc['filename']}")
            if 'description' in doc:
                print(f"  Description: {doc['description']}")
            print(f"  Path: {doc['path']}")
            if 'category' in doc:
                print(f"  Category: {doc['category']}")
            print()
    
    elif args.action == 'list':
        # List categories and years
        if not searcher.load_index():
            print("No index found. Run 'scan' first.")
            return
        
        print("\nCategories:")
        for cat in searcher.list_categories():
            count = sum(1 for doc in searcher.documents if doc.get('category') == cat)
            print(f"  - {cat}: {count} documents")
        
        print("\nYears:")
        for year in searcher.list_years():
            count = sum(1 for doc in searcher.documents if doc.get('year') == year)
            print(f"  - {year}: {count} documents")
    
    elif args.action == 'report':
        # Generate category report
        if not searcher.load_index():
            print("No index found. Run 'scan' first.")
            return
        
        searcher.generate_category_report()
    
    elif args.action == 'log':
        # Display recent log entries
        log_file = Path("ACTION_LOG.md")
        if log_file.exists():
            print("\n=== Recent Action Log Entries ===\n")
            with open(log_file, 'r') as f:
                content = f.read()
                # Show last 50 lines or so
                lines = content.split('\n')
                recent_lines = lines[-50:] if len(lines) > 50 else lines
                print('\n'.join(recent_lines))
        else:
            print("No action log found.")


if __name__ == "__main__":
    main() 