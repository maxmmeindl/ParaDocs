#!/usr/bin/env python3
"""
ParaDocs Citation Registry Builder
Extracts citations from existing timeline data and builds searchable registry
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CitationRegistryBuilder:
    def __init__(self):
        self.citations = {}
        self.violation_patterns = defaultdict(list)
        self.documents_by_citation = defaultdict(list)
        
    def extract_citations_from_timeline(self, timeline_file):
        """Extract all citations from timeline events"""
        with open(timeline_file, 'r') as f:
            data = json.load(f)
        
        events = data.get('timeline_events', [])
        
        for event in events:
            # Extract citations from violations array
            violations = event.get('violations', [])
            for violation in violations:
                citation = self._parse_citation(violation)
                if citation:
                    self._add_citation(citation, event, violation)
            
            # Extract from legal_basis field
            legal_basis = event.get('legal_basis', '')
            if legal_basis:
                citation = self._parse_citation(legal_basis)
                if citation:
                    self._add_citation(citation, event, legal_basis)
                    
        return self.citations
    
    def _parse_citation(self, text):
        """Parse legal citation from text"""
        patterns = [
            r'(\d+\s+C\.F\.R\.?\s*§?\s*[\d\.]+[a-z]*)',  # CFR citations
            r'(\d+\s+U\.S\.C\.?\s*§?\s*[\d\.]+[a-z]*)',   # USC citations
            r'(MD-\d+\s*§?\s*[IV\.]+[A-Z]*)',             # MD citations
            r'(FEMA\s+(?:Instruction|Manual|Directive)\s+[\d\-\.]+)', # FEMA docs
            r'(Rehabilitation Act\s*§?\s*\d+)',            # Rehab Act
            r'(ADEA\s*\(.*?\))',                          # ADEA references
            r'(HIPAA\s*\(.*?\))',                         # HIPAA references
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self._normalize_citation(match.group(1))
        return None
    
    def _normalize_citation(self, citation):
        """Normalize citation format"""
        citation = re.sub(r'\s+', ' ', citation.strip())
        citation = re.sub(r'C\.F\.R\.?', 'C.F.R.', citation)
        citation = re.sub(r'U\.S\.C\.?', 'U.S.C.', citation)
        return citation
    
    def _add_citation(self, citation, event, context):
        """Add citation to registry"""
        if citation not in self.citations:
            self.citations[citation] = {
                'id': f"cite_{len(self.citations):03d}",
                'code': citation,
                'title': self._get_citation_title(citation),
                'authority_type': self._get_authority_type(citation),
                'contexts': [],
                'violations': [],
                'events': []
            }
        
        # Add context and event
        self.citations[citation]['contexts'].append(context)
        self.citations[citation]['events'].append({
            'date': event.get('date'),
            'event': event.get('event', ''),
            'category': event.get('category', ''),
            'severity': event.get('severity', '')
        })
        
        # Extract violation pattern
        if 'violations' in event:
            for violation in event['violations']:
                if citation in violation:
                    self.citations[citation]['violations'].append(violation)
    
    def _get_citation_title(self, citation):
        """Get descriptive title for citation"""
        titles = {
            '29 C.F.R. §1614.102': 'Timely Processing of Complaints',
            '29 C.F.R. §1614.108': 'Investigation Procedures',
            '29 C.F.R. §1630.9': 'Not Making Reasonable Accommodation',
            '42 U.S.C. §12112': 'Discrimination',
            'MD-110': 'EEOC Management Directive',
            'Rehabilitation Act §501': 'Nondiscrimination in Federal Employment',
            'FEMA Instruction 256-022-01': 'Reasonable Accommodation Procedures',
        }
        
        for key, title in titles.items():
            if key in citation:
                return title
        return citation
    
    def _get_authority_type(self, citation):
        """Determine authority type"""
        if 'C.F.R.' in citation:
            return 'regulation'
        elif 'U.S.C.' in citation:
            return 'statute'
        elif 'MD-' in citation:
            return 'eeoc_directive'
        elif 'FEMA' in citation:
            return 'agency_policy'
        elif 'Act' in citation:
            return 'statute'
        return 'other'
    
    def build_violation_taxonomy(self):
        """Build violation taxonomy from existing data"""
        taxonomy = {
            'procedural_violations': {
                'timeline_breaches': [],
                'documentation_errors': [],
                'process_deviations': []
            },
            'substantive_violations': {
                'disability_discrimination': [],
                'age_discrimination': [],
                'retaliation': []
            },
            'administrative_violations': {
                'hipaa_breaches': [],
                'record_keeping': [],
                'communication_errors': []
            }
        }
        
        # Categorize violations from citations
        for citation, data in self.citations.items():
            for violation in data['violations']:
                category = self._categorize_violation(violation, citation)
                if category:
                    taxonomy[category[0]][category[1]].append({
                        'citation': citation,
                        'violation': violation,
                        'authority': data['title']
                    })
        
        return taxonomy
    
    def _categorize_violation(self, violation, citation):
        """Categorize violation type"""
        violation_lower = violation.lower()
        
        if any(word in violation_lower for word in ['timeline', 'delay', 'days', 'deadline']):
            return ('procedural_violations', 'timeline_breaches')
        elif any(word in violation_lower for word in ['blank', 'documentation', 'form']):
            return ('procedural_violations', 'documentation_errors')
        elif any(word in violation_lower for word in ['disability', 'accommodation', 'ada']):
            return ('substantive_violations', 'disability_discrimination')
        elif any(word in violation_lower for word in ['age', 'adea', 'older']):
            return ('substantive_violations', 'age_discrimination')
        elif any(word in violation_lower for word in ['retaliation', 'adverse', 'retaliatory']):
            return ('substantive_violations', 'retaliation')
        elif any(word in violation_lower for word in ['hipaa', 'phi', 'encrypted']):
            return ('administrative_violations', 'hipaa_breaches')
        
        return None
    
    def save_registry(self, output_file='citation_registry.json'):
        """Save citation registry to file"""
        registry = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'total_citations': len(self.citations),
                'authority_types': list(set(c['authority_type'] for c in self.citations.values()))
            },
            'citations': list(self.citations.values()),
            'violation_taxonomy': self.build_violation_taxonomy()
        }
        
        with open(output_file, 'w') as f:
            json.dump(registry, f, indent=2)
        
        print(f"Citation registry saved to {output_file}")
        print(f"Total citations: {len(self.citations)}")
        return registry

def main():
    builder = CitationRegistryBuilder()
    
    # Extract from main timeline file
    timeline_file = 'eeo_comprehensive_investigation.json'
    if Path(timeline_file).exists():
        builder.extract_citations_from_timeline(timeline_file)
        registry = builder.save_registry()
        
        # Print summary
        print("\nCitation Summary:")
        for citation, data in builder.citations.items():
            print(f"- {citation}: {data['title']} ({len(data['events'])} events)")
    else:
        print(f"Timeline file {timeline_file} not found")

if __name__ == "__main__":
    main() 