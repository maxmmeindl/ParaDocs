#!/usr/bin/env python3
"""
Comprehensive Case Indexing System
Creates detailed, organized indexes correlating topics, damages, timeline events, and evidence
"""

import csv
import json
from datetime import datetime

class ComprehensiveCaseIndexer:
    """Create multiple correlated indexes for the case"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        
    def create_master_index_template(self):
        """Create a master index that correlates everything"""
        
        print("CREATING COMPREHENSIVE CASE INDEXES")
        print("=" * 70)
        
        # Master Index Structure
        master_index = {
            'accommodation_violations': {
                'events': [
                    {
                        'id': 'AV-001',
                        'date': '2020-09-15',
                        'event': 'First Accommodation Request',
                        'response_time': '1,340 days (NEVER)',
                        'damages': '$550,684.93',
                        'evidence': ['Email EM-001', 'ROI pp. 11-15', 'No response documented'],
                        'legal_violations': ['ADA', '29 CFR 1630.2(o)(3)', 'Rehabilitation Act'],
                        'witnesses': ['HR Director', 'Supervisor'],
                        'exhibits': ['A-1', 'A-2', 'A-3']
                    },
                    {
                        'id': 'AV-002',
                        'date': '2023-11-09',
                        'event': 'Second Accommodation Request (Telework)',
                        'response_time': '36 days',
                        'damages': '$14,794.52',
                        'evidence': ['Email EM-004', 'ROI pp. 11-12'],
                        'legal_violations': ['Exceeded 30-day requirement'],
                        'witnesses': ['New HR Manager'],
                        'exhibits': ['B-1', 'B-2']
                    }
                ],
                'total_damages': '$565,479.45',
                'key_findings': [
                    'No interactive process ever conducted',
                    'No tracking system for accommodations',
                    'Pattern of ignoring requests'
                ]
            },
            'retaliation_events': {
                'events': [
                    {
                        'id': 'RE-001',
                        'date': '2024-03-15',
                        'event': 'EEO Complaint Accepted',
                        'protected_activity': True,
                        'evidence': ['LOA', 'Complaint filing'],
                        'exhibits': ['C-1']
                    },
                    {
                        'id': 'RE-002',
                        'date': '2024-03-20',
                        'event': 'PIP Issued',
                        'days_after_eeo': 5,
                        'damages': 'Supports punitive damages',
                        'evidence': ['Email EM-007', 'PIP document'],
                        'legal_violations': ['42 USC 2000e-3(a)'],
                        'exhibits': ['D-1']
                    },
                    {
                        'id': 'RE-003',
                        'date': '2025-01-06',
                        'event': 'TERMINATION',
                        'days_after_eeo': 297,
                        'damages': '$1,132,422.80+',
                        'evidence': ['Termination letter', 'During investigation'],
                        'legal_violations': ['Per se retaliation'],
                        'exhibits': ['D-2']
                    }
                ],
                'total_damages': '$1,432,422.80+ (ongoing)',
                'pattern_evidence': 'Clear temporal proximity between EEO activity and adverse actions'
            },
            'damage_categories': {
                'economic_damages': {
                    'immediate': {
                        'lost_wages': {'amount': '$57,079.50', 'ongoing': True, 'daily_rate': '$410.96'},
                        'lost_benefits': {'amount': '$17,123.85', 'ongoing': True},
                        'cobra_costs': {'amount': '$8,219.45', 'ongoing': True}
                    },
                    'future': {
                        'front_pay': {'amount': '$300,000', 'period': '2-3 years'},
                        'pension_loss': {'amount': '$750,000', 'calculation': 'Actuarial'}
                    },
                    'total_economic': '$1,132,422.80'
                },
                'non_economic_damages': {
                    'emotional_distress': {
                        'discrimination': {'amount': '$150,000', 'period': '3.7 years'},
                        'termination': {'amount': '$100,000', 'impact': 'Ongoing'}
                    },
                    'total_non_economic': '$250,000'
                },
                'punitive_damages': {
                    'amount': '$300,000',
                    'basis': '1,340-day violation + retaliation',
                    'cap': 'Federal statutory maximum'
                }
            }
        }
        
        # Create Timeline Index
        timeline_index = [
            {'date': '2020-09-15', 'type': 'accommodation', 'event': 'First Request', 'outcome': 'Ignored 1,340 days'},
            {'date': '2020-10-15', 'type': 'follow_up', 'event': 'Follow-up #1', 'outcome': 'No response'},
            {'date': '2021-01-10', 'type': 'follow_up', 'event': 'Follow-up #2', 'outcome': 'No response'},
            {'date': '2021-06-XX', 'type': 'follow_up', 'event': 'Follow-up #3', 'outcome': 'No response'},
            {'date': '2023-11-09', 'type': 'accommodation', 'event': 'Second Request', 'outcome': '36-day delay'},
            {'date': '2023-12-15', 'type': 'denial', 'event': 'Denial', 'outcome': 'No interactive process'},
            {'date': '2024-01-08', 'type': 'eeo', 'event': 'EEO Contact', 'outcome': 'Counseling initiated'},
            {'date': '2024-02-20', 'type': 'eeo', 'event': 'Formal Complaint', 'outcome': 'Filed'},
            {'date': '2024-03-15', 'type': 'eeo', 'event': 'LOA Issued', 'outcome': 'Accepted'},
            {'date': '2024-04-15', 'type': 'eeo', 'event': 'Investigation Begins', 'outcome': 'Ongoing'},
            {'date': '2024-07-25', 'type': 'eeo', 'event': 'ROI Complete', 'outcome': 'Transmitted'},
            {'date': '2024-08-15', 'type': 'eeo', 'event': 'Election', 'outcome': 'Hearing requested'},
            {'date': '2025-01-06', 'type': 'retaliation', 'event': 'TERMINATION', 'outcome': 'During investigation'},
            {'date': '2025-05-20', 'type': 'eeo', 'event': 'Venue Change', 'outcome': 'Requested'}
        ]
        
        # Create Evidence Correlation Index
        evidence_index = {
            'emails': {
                'template': 'Replace with actual emails from case',
                'categories': ['accommodation_requests', 'denials', 'follow_ups', 'eeo_communications', 'retaliation'],
                'critical_emails': [
                    'September 2020 accommodation request',
                    'Multiple follow-ups with no response',
                    'November 2023 telework request',
                    'December 2023 denial',
                    'PIP notification (March 2024)',
                    'Termination notice (January 2025)'
                ]
            },
            'documents': {
                'roi_sections': {
                    'pp_11-15': 'Accommodation request history',
                    'pp_16-20': 'Witness statements',
                    'pp_26-29': 'Email evidence',
                    'pp_45': 'PIP documentation'
                },
                'key_admissions': [
                    'No accommodation tracking system',
                    'No interactive process conducted',
                    'No essential functions analysis',
                    'No undue hardship assessment'
                ]
            }
        }
        
        # Generate CSV Files
        self._generate_timeline_csv(timeline_index)
        self._generate_damages_csv(master_index['damage_categories'])
        self._generate_violations_csv(master_index)
        self._generate_evidence_csv(evidence_index)
        
        # Generate Master JSON
        with open(f'master_case_index_{self.case_number}.json', 'w') as f:
            json.dump(master_index, f, indent=2)
        
        # Generate Instructions
        self._generate_indexing_instructions()
        
        return master_index
    
    def _generate_timeline_csv(self, timeline):
        """Generate timeline CSV"""
        filename = f'timeline_index_{self.case_number}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'type', 'event', 'outcome'])
            writer.writeheader()
            writer.writerows(timeline)
        print(f"Generated: {filename}")
    
    def _generate_damages_csv(self, damages):
        """Generate damages breakdown CSV"""
        filename = f'damages_index_{self.case_number}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Subcategory', 'Type', 'Amount', 'Status'])
            
            # Economic damages
            for subcat, items in damages['economic_damages'].items():
                if isinstance(items, dict) and subcat != 'total_economic':
                    for item_name, details in items.items():
                        writer.writerow(['Economic', subcat, item_name, details['amount'], 
                                       'Ongoing' if details.get('ongoing') else 'Fixed'])
            
            # Non-economic damages
            for subcat, items in damages['non_economic_damages'].items():
                if isinstance(items, dict) and subcat != 'total_non_economic':
                    for item_name, details in items.items():
                        writer.writerow(['Non-Economic', subcat, item_name, details['amount'], 
                                       details.get('period', 'N/A')])
            
            # Punitive
            writer.writerow(['Punitive', 'N/A', 'Federal Cap', damages['punitive_damages']['amount'], 
                           damages['punitive_damages']['basis']])
            
            # Totals
            writer.writerow(['TOTAL', 'Economic', '', damages['economic_damages']['total_economic'], ''])
            writer.writerow(['TOTAL', 'Non-Economic', '', damages['non_economic_damages']['total_non_economic'], ''])
            writer.writerow(['TOTAL', 'ALL DAMAGES', '', '$2,272,902.25', 'As of May 2025'])
        
        print(f"Generated: {filename}")
    
    def _generate_violations_csv(self, master_index):
        """Generate violations tracking CSV"""
        filename = f'violations_index_{self.case_number}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Violation Type', 'Date', 'Event', 'Legal Violation', 'Evidence', 'Damages'])
            
            # Accommodation violations
            for event in master_index['accommodation_violations']['events']:
                writer.writerow(['Accommodation', event['date'], event['event'], 
                               ', '.join(event['legal_violations']), 
                               ', '.join(event['evidence']), event['damages']])
            
            # Retaliation violations
            for event in master_index['retaliation_events']['events']:
                if 'legal_violations' in event:
                    writer.writerow(['Retaliation', event['date'], event['event'],
                                   ', '.join(event['legal_violations']),
                                   ', '.join(event['evidence']), 
                                   event.get('damages', 'See damage calculations')])
        
        print(f"Generated: {filename}")
    
    def _generate_evidence_csv(self, evidence_index):
        """Generate evidence correlation CSV"""
        filename = f'evidence_index_{self.case_number}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Evidence Type', 'Location', 'Description', 'Relevance'])
            
            # ROI sections
            for pages, desc in evidence_index['documents']['roi_sections'].items():
                writer.writerow(['ROI', pages, desc, 'Primary evidence'])
            
            # Key admissions
            for admission in evidence_index['documents']['key_admissions']:
                writer.writerow(['Admission', 'ROI', admission, 'Proves violations'])
            
            # Critical emails (template)
            for email in evidence_index['emails']['critical_emails']:
                writer.writerow(['Email', 'TBD', email, 'Documentary evidence'])
        
        print(f"Generated: {filename}")
    
    def _generate_indexing_instructions(self):
        """Generate instructions for using the indexes"""
        with open('INDEX_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
            f.write("# Case Index System Instructions\n\n")
            f.write("## Files Generated\n\n")
            f.write("1. **master_case_index_[case].json** - Complete correlated data\n")
            f.write("2. **timeline_index_[case].csv** - Chronological events\n")
            f.write("3. **damages_index_[case].csv** - Damage calculations breakdown\n")
            f.write("4. **violations_index_[case].csv** - Legal violations tracking\n")
            f.write("5. **evidence_index_[case].csv** - Evidence correlation\n\n")
            
            f.write("## How to Use\n\n")
            f.write("### For Email Indexing:\n")
            f.write("1. Open the CSV templates\n")
            f.write("2. Add your actual emails with:\n")
            f.write("   - Date/time sent\n")
            f.write("   - From/to parties\n")
            f.write("   - Subject line\n")
            f.write("   - Which violation it relates to\n")
            f.write("   - Response time (if any)\n")
            f.write("   - Exhibit number\n\n")
            
            f.write("### For Correlation:\n")
            f.write("- Each event has an ID (AV-001, RE-001, etc.)\n")
            f.write("- Cross-reference IDs across indexes\n")
            f.write("- Link emails to specific violations\n")
            f.write("- Track damages to specific events\n\n")
            
            f.write("### For Settlement/Trial:\n")
            f.write("- Sort timeline_index by date for chronology\n")
            f.write("- Sort damages_index by amount for impact\n")
            f.write("- Use violations_index for legal arguments\n")
            f.write("- Use evidence_index for discovery\n\n")
            
            f.write("## Key Insights from Indexes\n\n")
            f.write("1. **1,340-day violation** drives accommodation damages\n")
            f.write("2. **January 6, 2025 termination** drives economic damages\n")
            f.write("3. **5-day PIP timing** proves retaliation\n")
            f.write("4. **No interactive process** = per se violation\n")
        
        print("Generated: INDEX_INSTRUCTIONS.md")


def main():
    indexer = ComprehensiveCaseIndexer()
    
    print("\nThis will create comprehensive indexes that correlate:")
    print("- Timeline events")
    print("- Damages by category")
    print("- Legal violations")
    print("- Evidence locations")
    print("- Email tracking templates\n")
    
    # Create all indexes
    master_index = indexer.create_master_index_template()
    
    print("\n" + "="*70)
    print("INDEXES CREATED:")
    print("="*70)
    print("\n1. Timeline Index - Shows every event chronologically")
    print("2. Damages Index - Breaks down all $2.27M in damages")
    print("3. Violations Index - Tracks each legal violation")
    print("4. Evidence Index - Correlates ROI pages, emails, exhibits")
    print("5. Master Index (JSON) - Links everything together")
    print("\nREAD: INDEX_INSTRUCTIONS.md for how to use these files")
    print("\nNEXT STEP: Add your actual emails to the templates!")


if __name__ == "__main__":
    main() 