#!/usr/bin/env python3
"""
ParaDocs Enhanced Search System
Citation-aware search with violation mapping and natural language queries
"""

import json
import re
from pathlib import Path
from datetime import datetime
import argparse
from search_documents import DocumentSearcher

class EnhancedSearcher(DocumentSearcher):
    def __init__(self, base_path="."):
        super().__init__(base_path)
        self.citation_registry = {}
        self.violation_taxonomy = {}
        self.load_citation_registry()
        
    def load_citation_registry(self):
        """Load citation registry and violation taxonomy"""
        registry_file = self.base_path / "citation_registry.json"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                data = json.load(f)
                # Index citations by code for quick lookup
                for citation in data.get('citations', []):
                    self.citation_registry[citation['code']] = citation
                self.violation_taxonomy = data.get('violation_taxonomy', {})
            print(f"Loaded {len(self.citation_registry)} citations")
        else:
            print("Citation registry not found. Run extract_citations.py first.")
    
    def natural_language_search(self, query):
        """Parse natural language queries and convert to filters"""
        query_lower = query.lower()
        filters = {}
        
        # Common legal query patterns
        if any(phrase in query_lower for phrase in ['ra policies', 'accommodation', 'reasonable accommodation']):
            filters['citations'] = ['FEMA Instruction 256-022-01', '29 C.F.R.']
            filters['categories'] = ['Accommodation Request']
            
        elif any(phrase in query_lower for phrase in ['timeline', 'delay', 'processing time']):
            filters['violations'] = ['timeline_breaches']
            filters['citations'] = ['29 C.F.R.']
            
        elif any(phrase in query_lower for phrase in ['discrimination', 'disability']):
            filters['violations'] = ['disability_discrimination']
            filters['citations'] = ['29 C.F.R.', '42 U.S.C.']
            
        elif any(phrase in query_lower for phrase in ['retaliation', 'adverse action']):
            filters['violations'] = ['retaliation']
            filters['citations'] = ['42 U.S.C.']
            
        elif any(phrase in query_lower for phrase in ['hipaa', 'privacy', 'medical information']):
            filters['violations'] = ['hipaa_breaches']
            
        # Extract specific citation requests
        citation_match = re.search(r'(cfr|usc|fema)\s*([\d\-\.]+)', query_lower)
        if citation_match:
            authority = citation_match.group(1).upper()
            number = citation_match.group(2)
            filters['citations'] = [f'{authority} {number}']
        
        return filters
    
    def search_by_citation(self, citation_code):
        """Search for documents related to specific citation"""
        results = []
        
        if citation_code in self.citation_registry:
            citation_data = self.citation_registry[citation_code]
            
            # Get events associated with this citation
            events = citation_data.get('events', [])
            
            for event in events:
                # Create document-like result from event
                result = {
                    'type': 'timeline_event',
                    'date': event.get('date'),
                    'title': event.get('event', ''),
                    'category': event.get('category', ''),
                    'severity': event.get('severity', ''),
                    'citation': citation_code,
                    'citation_title': citation_data.get('title', ''),
                    'authority_type': citation_data.get('authority_type', '')
                }
                results.append(result)
        
        return results
    
    def search_by_violation(self, violation_type):
        """Search for documents by violation category"""
        results = []
        
        # Search in violation taxonomy
        for main_category, subcategories in self.violation_taxonomy.items():
            for sub_category, violations in subcategories.items():
                if violation_type in [main_category, sub_category]:
                    for violation in violations:
                        citation_code = violation['citation']
                        citation_results = self.search_by_citation(citation_code)
                        results.extend(citation_results)
        
        return results
    
    def comprehensive_search(self, query, **filters):
        """Enhanced search combining documents, citations, and violations"""
        all_results = {
            'documents': [],
            'timeline_events': [],
            'citations': [],
            'violation_summary': {}
        }
        
        # Parse natural language if no specific filters
        if not filters:
            filters = self.natural_language_search(query)
        
        # Search documents using parent class
        if self.documents:
            doc_results = self.search(
                query, 
                filters.get('category'), 
                filters.get('year'), 
                filters.get('doc_type')
            )
            all_results['documents'] = doc_results
        
        # Search by citations
        if 'citations' in filters:
            for citation in filters['citations']:
                citation_results = self.search_by_citation(citation)
                all_results['timeline_events'].extend(citation_results)
                
                # Add citation info
                if citation in self.citation_registry:
                    all_results['citations'].append(self.citation_registry[citation])
        
        # Search by violations
        if 'violations' in filters:
            for violation in filters['violations']:
                violation_results = self.search_by_violation(violation)
                all_results['timeline_events'].extend(violation_results)
        
        # Generate violation summary
        all_results['violation_summary'] = self.generate_violation_summary(
            all_results['timeline_events']
        )
        
        # Remove duplicates
        all_results['timeline_events'] = self._deduplicate_events(
            all_results['timeline_events']
        )
        
        return all_results
    
    def generate_violation_summary(self, events):
        """Generate summary of violations by category"""
        summary = {}
        
        for event in events:
            category = event.get('category', 'Other')
            severity = event.get('severity', 'Unknown')
            
            if category not in summary:
                summary[category] = {
                    'count': 0,
                    'severity_breakdown': {},
                    'citations': set(),
                    'events': []
                }
            
            summary[category]['count'] += 1
            summary[category]['severity_breakdown'][severity] = \
                summary[category]['severity_breakdown'].get(severity, 0) + 1
            summary[category]['citations'].add(event.get('citation', ''))
            summary[category]['events'].append(event)
        
        # Convert sets to lists for JSON serialization
        for category in summary:
            summary[category]['citations'] = list(summary[category]['citations'])
        
        return summary
    
    def _deduplicate_events(self, events):
        """Remove duplicate events"""
        seen = set()
        unique_events = []
        
        for event in events:
            event_key = (event.get('date'), event.get('title', ''))
            if event_key not in seen:
                seen.add(event_key)
                unique_events.append(event)
        
        return unique_events
    
    def generate_case_report(self, case_number=None, output_format='json'):
        """Generate comprehensive case report with violation mapping"""
        
        # Search for all case-related content
        case_results = self.comprehensive_search('', citations=list(self.citation_registry.keys()))
        
        report = {
            'metadata': {
                'case_number': case_number or 'HS-FEMA-02430-2024',
                'generated': datetime.now().isoformat(),
                'total_events': len(case_results['timeline_events']),
                'total_citations': len(case_results['citations'])
            },
            'violation_analysis': case_results['violation_summary'],
            'timeline_events': case_results['timeline_events'],
            'legal_authorities': case_results['citations'],
            'document_evidence': case_results['documents']
        }
        
        if output_format == 'json':
            filename = f"case_report_{case_number or 'comprehensive'}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Case report saved to {filename}")
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Enhanced ParaDocs Search')
    parser.add_argument('action', choices=['search', 'citation', 'violation', 'report'],
                       help='Search action to perform')
    parser.add_argument('-q', '--query', help='Search query')
    parser.add_argument('-c', '--citation', help='Search by citation code')
    parser.add_argument('-v', '--violation', help='Search by violation type')
    parser.add_argument('--case', help='Case number for report generation')
    parser.add_argument('--format', choices=['json', 'html'], default='json',
                       help='Output format for reports')
    
    args = parser.parse_args()
    
    searcher = EnhancedSearcher()
    
    if args.action == 'search':
        if not args.query:
            print("Please provide a search query with -q")
            return
        
        results = searcher.comprehensive_search(args.query)
        
        print(f"\n=== SEARCH RESULTS FOR: '{args.query}' ===\n")
        
        # Show timeline events
        if results['timeline_events']:
            print(f"Timeline Events ({len(results['timeline_events'])}):")
            for event in results['timeline_events'][:10]:  # Show first 10
                print(f"  📅 {event.get('date', 'N/A')}: {event.get('title', 'N/A')}")
                print(f"     Category: {event.get('category', 'N/A')} | Severity: {event.get('severity', 'N/A')}")
                if event.get('citation'):
                    print(f"     Citation: {event.get('citation')} - {event.get('citation_title', '')}")
                print()
        
        # Show documents
        if results['documents']:
            print(f"\nDocuments ({len(results['documents'])}):")
            for doc in results['documents'][:5]:  # Show first 5
                print(f"  📄 {doc['filename']}")
                print(f"     Path: {doc['path']}")
                print(f"     Category: {doc.get('category', 'N/A')}")
                print()
        
        # Show violation summary
        if results['violation_summary']:
            print("\nViolation Summary:")
            for category, data in results['violation_summary'].items():
                print(f"  ⚖️  {category}: {data['count']} events")
                for severity, count in data['severity_breakdown'].items():
                    print(f"     - {severity}: {count}")
                print()
    
    elif args.action == 'citation':
        if not args.citation:
            print("Please provide a citation code with -c")
            return
        
        results = searcher.search_by_citation(args.citation)
        print(f"\n=== EVENTS FOR CITATION: {args.citation} ===\n")
        
        for event in results:
            print(f"📅 {event.get('date')}: {event.get('title')}")
            print(f"   Category: {event.get('category')} | Severity: {event.get('severity')}")
            print()
    
    elif args.action == 'violation':
        if not args.violation:
            print("Please provide a violation type with -v")
            return
        
        results = searcher.search_by_violation(args.violation)
        print(f"\n=== EVENTS FOR VIOLATION TYPE: {args.violation} ===\n")
        
        for event in results:
            print(f"📅 {event.get('date')}: {event.get('title')}")
            print(f"   Citation: {event.get('citation')}")
            print()
    
    elif args.action == 'report':
        report = searcher.generate_case_report(args.case, args.format)
        print(f"\nGenerated comprehensive case report")
        print(f"Total events: {report['metadata']['total_events']}")
        print(f"Total citations: {report['metadata']['total_citations']}")

if __name__ == "__main__":
    main() 