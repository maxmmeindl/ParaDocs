#!/usr/bin/env python3
"""
EEOC Case Document Analyzer and Cross-Reference System
Analyzes complaint documents and finds supporting evidence from EEOC resources
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import argparse
from collections import defaultdict

class CaseAnalyzer:
    """Analyzes EEOC case documents and cross-references with support materials"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.case_docs_path = self.base_path / "paradocs-agent" / "downloaded"
        self.index_file = self.base_path / "document_index.json"
        self.case_analysis_file = self.base_path / f"case_analysis_{case_number}.json"
        self.report_file = self.base_path / f"case_support_report_{case_number}.md"
        
        # Key terms and patterns to look for
        self.key_terms = {
            'ada': ['ADA', 'Americans with Disabilities Act', 'disability', 'accommodation', 
                    'reasonable accommodation', 'interactive process'],
            'termination': ['termination', 'terminated', 'discharge', 'fired', 'removal', 
                           'separation', 'dismissal'],
            'discrimination': ['discrimination', 'discriminate', 'disparate treatment', 
                              'hostile work environment', 'harassment'],
            'retaliation': ['retaliation', 'reprisal', 'retaliatory', 'whistleblower'],
            'fema': ['FEMA', 'Federal Emergency Management Agency', 'DHS', 
                     'Department of Homeland Security'],
            'process': ['due process', 'procedural', 'timeline', 'deadline', 'notice']
        }
        
        # EEOC table mappings for different claim types
        self.table_mappings = {
            'ada': ['8', '15', '16', '22'],  # Complaints by basis, findings
            'termination': ['11', '13', '15', '16'],  # Closure types, dismissals
            'adr': ['4', '5', '19', '20'],  # ADR statistics
            'timeliness': ['7', '10', '12', '14', '17', '18'],  # Processing times
            'benefits': ['6', '21'],  # Settlements and benefits
            'process': ['2', '3', '9']  # Counseling, investigations
        }
        
    def analyze_case_documents(self):
        """Analyze case documents to extract key claims and facts"""
        print(f"\nAnalyzing case documents for {self.case_number}...")
        
        case_data = {
            'case_number': self.case_number,
            'documents_analyzed': [],
            'key_claims': defaultdict(list),
            'dates': [],
            'parties': {
                'complainant': '',
                'respondent': 'FEMA',
                'agency': 'Department of Homeland Security'
            },
            'current_stage': 'ADR/Pre-Hearing',
            'analysis_date': datetime.now().isoformat()
        }
        
        # Find and analyze case documents
        case_files = list(self.case_docs_path.glob(f"*{self.case_number}*"))
        complaint_files = list(self.case_docs_path.glob("*complaint*"))
        rebuttal_files = list(self.case_docs_path.glob("*[Rr]ebuttal*"))
        
        all_case_files = case_files + complaint_files + rebuttal_files
        
        for file_path in all_case_files:
            if file_path.suffix in ['.pdf', '.docx']:
                doc_info = {
                    'filename': file_path.name,
                    'path': str(file_path),
                    'type': self._classify_document(file_path.name)
                }
                case_data['documents_analyzed'].append(doc_info)
                
                # Extract key information based on document type
                if 'complaint' in file_path.name.lower():
                    case_data['key_claims']['primary_complaint'] = [
                        "ADA violation - failure to accommodate",
                        "Wrongful termination",
                        "Discrimination based on disability"
                    ]
                elif 'ROI' in file_path.name:
                    doc_info['description'] = "Report of Investigation"
                elif 'LOA' in file_path.name:
                    doc_info['description'] = "Letter of Acceptance"
                elif 'rebuttal' in file_path.name.lower():
                    doc_info['description'] = "Rebuttal to witness statements"
        
        # Save case analysis
        with open(self.case_analysis_file, 'w') as f:
            json.dump(case_data, f, indent=2)
        
        print(f"Analyzed {len(case_data['documents_analyzed'])} case documents")
        return case_data
    
    def _classify_document(self, filename):
        """Classify document type based on filename"""
        filename_lower = filename.lower()
        if 'complaint' in filename_lower:
            return 'complaint'
        elif 'roi' in filename_lower:
            return 'investigation_report'
        elif 'loa' in filename_lower:
            return 'acceptance_letter'
        elif 'election' in filename_lower:
            return 'election_letter'
        elif 'rebuttal' in filename_lower:
            return 'rebuttal'
        else:
            return 'other'
    
    def find_supporting_evidence(self, case_data):
        """Find supporting evidence from EEOC tables and documents"""
        print("\nSearching for supporting evidence...")
        
        # Load document index
        if not self.index_file.exists():
            print("Document index not found. Please run 'python search_documents.py scan' first.")
            return None
        
        with open(self.index_file, 'r') as f:
            index_data = json.load(f)
            documents = index_data.get('documents', [])
        
        support_data = {
            'ada_statistics': [],
            'termination_data': [],
            'adr_outcomes': [],
            'processing_times': [],
            'similar_outcomes': [],
            'relevant_tables': defaultdict(list)
        }
        
        # Find relevant tables based on claim types
        for doc in documents:
            table_num = doc.get('table', '').replace('B-', '')
            
            # ADA-related tables
            if table_num in self.table_mappings['ada']:
                support_data['relevant_tables']['ada'].append({
                    'table': doc.get('table'),
                    'title': doc.get('description', doc.get('filename')),
                    'relevance': 'Shows ADA complaint statistics and outcomes',
                    'path': doc.get('path')
                })
            
            # Termination-related tables
            if table_num in self.table_mappings['termination']:
                support_data['relevant_tables']['termination'].append({
                    'table': doc.get('table'),
                    'title': doc.get('description', doc.get('filename')),
                    'relevance': 'Shows termination case outcomes and statistics',
                    'path': doc.get('path')
                })
            
            # ADR process tables
            if table_num in self.table_mappings['adr']:
                support_data['relevant_tables']['adr'].append({
                    'table': doc.get('table'),
                    'title': doc.get('description', doc.get('filename')),
                    'relevance': 'Shows ADR participation rates and success statistics',
                    'path': doc.get('path')
                })
            
            # Timeline and processing tables
            if table_num in self.table_mappings['timeliness']:
                support_data['relevant_tables']['timeliness'].append({
                    'table': doc.get('table'),
                    'title': doc.get('description', doc.get('filename')),
                    'relevance': 'Shows processing timelines and deadlines',
                    'path': doc.get('path')
                })
        
        return support_data
    
    def generate_cross_reference_report(self, case_data, support_data):
        """Generate comprehensive cross-reference report"""
        print("\nGenerating cross-reference report...")
        
        with open(self.report_file, 'w') as f:
            # Header
            f.write(f"# EEOC Case Support Analysis Report\n")
            f.write(f"## Case: {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write("This report provides cross-referenced supporting evidence from EEOC ")
            f.write("statistical tables and manuals for your case against FEMA regarding:\n")
            f.write("- ADA violations and failure to accommodate\n")
            f.write("- Wrongful termination\n")
            f.write("- Current ADR process heading to AJ hearing\n\n")
            
            # Case Documents Analyzed
            f.write("## Case Documents Analyzed\n\n")
            for doc in case_data['documents_analyzed']:
                f.write(f"- **{doc['filename']}** ({doc['type']})\n")
            f.write("\n")
            
            # Supporting Evidence by Claim Type
            f.write("## Supporting Evidence by Claim Type\n\n")
            
            # ADA Claims Support
            f.write("### 1. ADA Discrimination Claims\n\n")
            f.write("#### Relevant EEOC Tables:\n")
            for table in support_data['relevant_tables']['ada']:
                f.write(f"- **{table['table']}**: {table['title']}\n")
                f.write(f"  - *Relevance*: {table['relevance']}\n")
                f.write(f"  - *File*: `{table['path']}`\n\n")
            
            f.write("#### Key Statistics to Reference:\n")
            f.write("- Table B-8: Shows basis of complaints filed (look for disability percentages)\n")
            f.write("- Table B-15: Finding of discrimination rates for ADA cases\n")
            f.write("- Table B-22: Complaints by statute (ADA specific data)\n\n")
            
            # Termination Claims Support
            f.write("### 2. Wrongful Termination\n\n")
            f.write("#### Relevant EEOC Tables:\n")
            for table in support_data['relevant_tables']['termination']:
                f.write(f"- **{table['table']}**: {table['title']}\n")
                f.write(f"  - *Relevance*: {table['relevance']}\n")
                f.write(f"  - *File*: `{table['path']}`\n\n")
            
            # ADR Process Support
            f.write("### 3. ADR Process and Outcomes\n\n")
            f.write("#### Relevant EEOC Tables:\n")
            for table in support_data['relevant_tables']['adr']:
                f.write(f"- **{table['table']}**: {table['title']}\n")
                f.write(f"  - *Relevance*: {table['relevance']}\n")
                f.write(f"  - *File*: `{table['path']}`\n\n")
            
            f.write("#### ADR Strategy Insights:\n")
            f.write("- Table B-20: ADR resolution rates in formal complaints\n")
            f.write("- Table B-19: ADR participation statistics\n")
            f.write("- Table B-5: Pre-complaint ADR outcomes (for comparison)\n\n")
            
            # Processing Timelines
            f.write("### 4. Processing Timelines and Deadlines\n\n")
            f.write("#### Relevant EEOC Tables:\n")
            for table in support_data['relevant_tables']['timeliness']:
                f.write(f"- **{table['table']}**: {table['title']}\n")
                f.write(f"  - *Relevance*: {table['relevance']}\n")
                f.write(f"  - *File*: `{table['path']}`\n\n")
            
            # Recommendations
            f.write("## Strategic Recommendations\n\n")
            f.write("### For ADR Preparation:\n")
            f.write("1. **Review Table B-20** for ADR success rates to set realistic expectations\n")
            f.write("2. **Analyze Table B-21** for typical benefits/remedies in settlements\n")
            f.write("3. **Check Table B-15** for discrimination finding rates in similar cases\n\n")
            
            f.write("### For AJ Hearing Preparation:\n")
            f.write("1. **Study Table B-17** for AJ decision implementation timelines\n")
            f.write("2. **Review Table B-15 & B-16** for discrimination vs. no discrimination findings\n")
            f.write("3. **Examine Table B-8** for complaint basis statistics to show pattern\n\n")
            
            f.write("### Key Data Points to Emphasize:\n")
            f.write("- Federal agency ADA complaint rates and outcomes\n")
            f.write("- FEMA/DHS specific complaint patterns (if available in sub-component data)\n")
            f.write("- Average processing times vs. your case timeline\n")
            f.write("- Settlement amounts and remedies in similar cases\n\n")
            
            # Next Steps
            f.write("## Next Steps\n\n")
            f.write("1. **Extract specific statistics** from identified tables\n")
            f.write("2. **Create visual charts** showing relevant trends\n")
            f.write("3. **Build timeline comparison** with EEOC averages\n")
            f.write("4. **Compile precedent cases** from similar complaints\n")
            f.write("5. **Prepare statistical evidence package** for ADR/hearing\n\n")
            
            f.write("---\n")
            f.write("*This report will be updated as additional analysis is performed*\n")
        
        print(f"Cross-reference report saved to: {self.report_file}")
        return self.report_file


def main():
    parser = argparse.ArgumentParser(description='Analyze EEOC case documents')
    parser.add_argument('--case', default='HS-FEMA-02430-2024', 
                       help='Case number to analyze')
    parser.add_argument('--action', choices=['analyze', 'report', 'extract'],
                       default='report', help='Action to perform')
    
    args = parser.parse_args()
    
    analyzer = CaseAnalyzer(args.case)
    
    if args.action == 'analyze':
        # Just analyze case documents
        case_data = analyzer.analyze_case_documents()
        print(f"\nCase analysis saved to: {analyzer.case_analysis_file}")
        
    elif args.action == 'report':
        # Full analysis and report generation
        case_data = analyzer.analyze_case_documents()
        support_data = analyzer.find_supporting_evidence(case_data)
        
        if support_data:
            report_path = analyzer.generate_cross_reference_report(case_data, support_data)
            print(f"\nComplete analysis available at: {report_path}")
            print("\nTo view the report, open the markdown file or run:")
            print(f"  type \"{report_path}\"")
    
    elif args.action == 'extract':
        # Future feature: Extract specific data from Excel tables
        print("Data extraction feature coming soon...")


if __name__ == "__main__":
    main() 