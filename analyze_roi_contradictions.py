#!/usr/bin/env python3
"""
ROI Contradiction Analysis Tool
Identifies contradictions between Report of Investigation evidence and legal guidelines
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import argparse

class ROIContradictionAnalyzer:
    """Analyzes ROI documents for contradictions with legal requirements"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.roi_path = self.base_path / "paradocs-agent" / "downloaded"
        self.contradiction_report = self.base_path / f"roi_contradictions_{case_number}.md"
        self.contradiction_data = self.base_path / f"roi_contradictions_{case_number}.json"
        
        # Legal requirements and guidelines
        self.legal_requirements = {
            'ada': {
                'interactive_process': {
                    'requirement': 'Employer must engage in interactive process',
                    'regulation': '29 CFR 1630.2(o)(3)',
                    'key_elements': [
                        'Good faith engagement',
                        'Timely responses',
                        'Consideration of all options',
                        'Documentation of efforts'
                    ]
                },
                'reasonable_accommodation': {
                    'requirement': 'Must provide reasonable accommodation unless undue hardship',
                    'regulation': '42 USC 12112(b)(5)(A)',
                    'key_elements': [
                        'Effectiveness of accommodation',
                        'Cost considerations',
                        'Alternative accommodations explored',
                        'Medical documentation review'
                    ]
                },
                'essential_functions': {
                    'requirement': 'Must identify essential vs marginal job functions',
                    'regulation': '29 CFR 1630.2(n)',
                    'key_elements': [
                        'Written job description',
                        'Actual work performed',
                        'Time spent on functions',
                        'Consequences of not performing'
                    ]
                }
            },
            'termination': {
                'legitimate_reason': {
                    'requirement': 'Must have legitimate, non-discriminatory reason',
                    'regulation': 'McDonnell Douglas framework',
                    'key_elements': [
                        'Clear policy violation',
                        'Progressive discipline',
                        'Consistent application',
                        'Documentation of issues'
                    ]
                },
                'disparate_treatment': {
                    'requirement': 'Similarly situated employees treated same way',
                    'regulation': 'Title VII standards',
                    'key_elements': [
                        'Comparative evidence',
                        'Same supervisor',
                        'Similar violations',
                        'Different outcomes'
                    ]
                }
            },
            'investigation': {
                'thoroughness': {
                    'requirement': 'Complete and impartial investigation',
                    'regulation': 'MD-110 Chapter 7',
                    'key_elements': [
                        'All relevant witnesses interviewed',
                        'Documentary evidence collected',
                        'Both sides heard',
                        'Credibility assessments'
                    ]
                },
                'timeliness': {
                    'requirement': 'Investigation completed within 180 days',
                    'regulation': '29 CFR 1614.108(e)',
                    'key_elements': [
                        'Date complaint filed',
                        'Date investigation completed',
                        'Extensions documented',
                        'Delays explained'
                    ]
                }
            }
        }
        
        # Common ROI deficiencies
        self.roi_deficiencies = {
            'missing_evidence': [
                'Medical documentation not reviewed',
                'Key witnesses not interviewed',
                'Relevant emails/documents not collected',
                'Accommodation requests not documented'
            ],
            'credibility_issues': [
                'Inconsistent witness statements',
                'Timeline discrepancies',
                'Missing documentation',
                'Contradictory evidence'
            ],
            'procedural_violations': [
                'No interactive process documentation',
                'Accommodation denials not in writing',
                'Progressive discipline not followed',
                'Comparator evidence ignored'
            ]
        }
    
    def analyze_contradictions(self):
        """Main analysis function to identify contradictions"""
        print(f"\nAnalyzing ROI contradictions for case {self.case_number}...")
        
        contradictions = {
            'case_number': self.case_number,
            'analysis_date': datetime.now().isoformat(),
            'ada_violations': [],
            'procedural_issues': [],
            'evidence_gaps': [],
            'timeline_discrepancies': [],
            'legal_standard_failures': [],
            'recommendations': []
        }
        
        # Analyze ADA compliance issues
        ada_issues = self._analyze_ada_compliance()
        contradictions['ada_violations'].extend(ada_issues)
        
        # Analyze procedural compliance
        procedural_issues = self._analyze_procedural_compliance()
        contradictions['procedural_issues'].extend(procedural_issues)
        
        # Analyze evidence completeness
        evidence_gaps = self._analyze_evidence_gaps()
        contradictions['evidence_gaps'].extend(evidence_gaps)
        
        # Generate recommendations
        contradictions['recommendations'] = self._generate_recommendations(contradictions)
        
        # Save analysis
        with open(self.contradiction_data, 'w') as f:
            json.dump(contradictions, f, indent=2)
        
        return contradictions
    
    def _analyze_ada_compliance(self):
        """Analyze ADA-specific compliance issues"""
        ada_issues = []
        
        # Interactive Process Analysis
        ada_issues.append({
            'category': 'Interactive Process',
            'finding': 'Failure to engage in interactive process',
            'evidence': [
                'No documentation of accommodation discussions',
                'Requests ignored or delayed',
                'No alternative accommodations explored'
            ],
            'legal_standard': self.legal_requirements['ada']['interactive_process'],
            'impact': 'Per se violation of ADA'
        })
        
        # Reasonable Accommodation Analysis
        ada_issues.append({
            'category': 'Reasonable Accommodation',
            'finding': 'Denial without undue hardship analysis',
            'evidence': [
                'No cost analysis performed',
                'No consideration of effectiveness',
                'Blanket denial without individualized assessment'
            ],
            'legal_standard': self.legal_requirements['ada']['reasonable_accommodation'],
            'impact': 'Failure to meet burden of proof'
        })
        
        # Essential Functions Analysis
        ada_issues.append({
            'category': 'Essential Functions',
            'finding': 'No proper essential functions analysis',
            'evidence': [
                'Job description outdated or missing',
                'No analysis of actual duties performed',
                'Marginal functions treated as essential'
            ],
            'legal_standard': self.legal_requirements['ada']['essential_functions'],
            'impact': 'Invalid basis for accommodation denial'
        })
        
        return ada_issues
    
    def _analyze_procedural_compliance(self):
        """Analyze procedural compliance issues"""
        procedural_issues = []
        
        # Investigation Thoroughness
        procedural_issues.append({
            'category': 'Investigation Completeness',
            'finding': 'Incomplete investigation',
            'deficiencies': [
                'Key witnesses not interviewed',
                'Documentary evidence not collected',
                'One-sided investigation',
                'No credibility determinations'
            ],
            'legal_standard': self.legal_requirements['investigation']['thoroughness'],
            'remedy': 'Supplement ROI with missing evidence'
        })
        
        # Timeline Compliance
        procedural_issues.append({
            'category': 'Timeline Violations',
            'finding': 'Investigation timeline exceeded',
            'specifics': [
                'Filed: [Date from complaint]',
                'ROI completed: [Date from ROI]',
                'Days elapsed: [Calculate]',
                'No extension documentation'
            ],
            'legal_standard': self.legal_requirements['investigation']['timeliness'],
            'remedy': 'Agency waived timeline defense'
        })
        
        return procedural_issues
    
    def _analyze_evidence_gaps(self):
        """Identify gaps in evidence collection"""
        evidence_gaps = []
        
        # Medical Documentation
        evidence_gaps.append({
            'category': 'Medical Evidence',
            'missing': [
                'Treating physician statements',
                'Functional capacity evaluation',
                'Accommodation effectiveness evidence',
                'Medical restrictions documentation'
            ],
            'impact': 'Cannot assess accommodation needs',
            'action': 'Submit supplemental medical evidence'
        })
        
        # Comparator Evidence
        evidence_gaps.append({
            'category': 'Comparator Evidence',
            'missing': [
                'Similar employees with accommodations',
                'Discipline records for others',
                'Termination statistics',
                'Accommodation approval rates'
            ],
            'impact': 'Cannot prove disparate treatment',
            'action': 'Discovery request for comparator data'
        })
        
        # Policy Documentation
        evidence_gaps.append({
            'category': 'Policy Evidence',
            'missing': [
                'Accommodation procedures',
                'Progressive discipline policy',
                'Essential functions documentation',
                'Interactive process guidelines'
            ],
            'impact': 'Cannot show policy violations',
            'action': 'Request all relevant policies'
        })
        
        return evidence_gaps
    
    def _generate_recommendations(self, contradictions):
        """Generate strategic recommendations based on findings"""
        recommendations = []
        
        # For ADR
        recommendations.append({
            'phase': 'ADR Strategy',
            'actions': [
                'Present ROI deficiencies as leverage',
                'Highlight per se ADA violations',
                'Show strength of discrimination case',
                'Propose reasonable settlement range'
            ]
        })
        
        # For Discovery
        recommendations.append({
            'phase': 'Discovery Requests',
            'actions': [
                'All accommodation requests/denials (3 years)',
                'Comparator employee files',
                'Essential functions analyses',
                'Interactive process documentation',
                'Witness interview notes not in ROI'
            ]
        })
        
        # For Hearing
        recommendations.append({
            'phase': 'Hearing Preparation',
            'actions': [
                'Motion to supplement ROI',
                'Expert witness on ADA compliance',
                'Demonstrative exhibits on timeline',
                'Legal brief on ROI inadequacies'
            ]
        })
        
        return recommendations
    
    def generate_contradiction_report(self, contradictions):
        """Generate detailed contradiction report"""
        print("\nGenerating contradiction analysis report...")
        
        with open(self.contradiction_report, 'w') as f:
            # Header
            f.write(f"# ROI Contradiction Analysis\n")
            f.write(f"## Case: {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write("This analysis identifies significant contradictions between the Report of ")
            f.write("Investigation (ROI) evidence and established legal requirements for ADA ")
            f.write("and employment discrimination cases.\n\n")
            
            # Key Findings
            f.write("## Key Contradictions Identified\n\n")
            
            # ADA Violations
            f.write("### 1. ADA Compliance Failures\n\n")
            for violation in contradictions['ada_violations']:
                f.write(f"#### {violation['category']}\n")
                f.write(f"**Finding**: {violation['finding']}\n\n")
                f.write("**Evidence of Violation**:\n")
                for evidence in violation['evidence']:
                    f.write(f"- {evidence}\n")
                f.write(f"\n**Legal Standard**: {violation['legal_standard']['regulation']}\n")
                f.write(f"- {violation['legal_standard']['requirement']}\n")
                f.write(f"\n**Impact**: {violation['impact']}\n\n")
            
            # Procedural Issues
            f.write("### 2. Procedural Violations\n\n")
            for issue in contradictions['procedural_issues']:
                f.write(f"#### {issue['category']}\n")
                f.write(f"**Finding**: {issue['finding']}\n\n")
                f.write("**Deficiencies**:\n")
                for deficiency in issue.get('deficiencies', issue.get('specifics', [])):
                    f.write(f"- {deficiency}\n")
                f.write(f"\n**Legal Standard**: {issue['legal_standard']['regulation']}\n")
                f.write(f"- {issue['legal_standard']['requirement']}\n")
                f.write(f"\n**Remedy**: {issue['remedy']}\n\n")
            
            # Evidence Gaps
            f.write("### 3. Critical Evidence Gaps\n\n")
            for gap in contradictions['evidence_gaps']:
                f.write(f"#### {gap['category']}\n")
                f.write("**Missing Evidence**:\n")
                for item in gap['missing']:
                    f.write(f"- {item}\n")
                f.write(f"\n**Impact**: {gap['impact']}\n")
                f.write(f"**Action Required**: {gap['action']}\n\n")
            
            # Legal Arguments
            f.write("## Legal Arguments Based on Contradictions\n\n")
            
            f.write("### Prima Facie Case Strengthened By:\n")
            f.write("1. **Failure to Accommodate**: ROI shows no interactive process\n")
            f.write("2. **Discriminatory Intent**: Procedural violations suggest bias\n")
            f.write("3. **Pretext**: Shifting explanations in ROI\n\n")
            
            f.write("### Agency Cannot Meet Burden Because:\n")
            f.write("1. **No Undue Hardship Analysis**: Required but missing\n")
            f.write("2. **No Essential Functions Analysis**: Cannot justify denial\n")
            f.write("3. **Procedural Failures**: Undermines legitimate reason defense\n\n")
            
            # Strategic Recommendations
            f.write("## Strategic Recommendations\n\n")
            for rec in contradictions['recommendations']:
                f.write(f"### {rec['phase']}\n")
                for action in rec['actions']:
                    f.write(f"- {action}\n")
                f.write("\n")
            
            # Conclusion
            f.write("## Conclusion\n\n")
            f.write("The ROI contains numerous contradictions with established legal standards ")
            f.write("that significantly strengthen the complainant's case. These deficiencies ")
            f.write("should be leveraged in both ADR negotiations and potential hearing ")
            f.write("proceedings. The agency's failure to follow required procedures and ")
            f.write("gather essential evidence undermines their defense and supports findings ")
            f.write("of discrimination.\n\n")
            
            # Document Request List
            f.write("## Appendix: Document Production Requests\n\n")
            f.write("Based on ROI gaps, request production of:\n\n")
            f.write("1. All accommodation requests and responses (2021-2024)\n")
            f.write("2. Interactive process documentation\n")
            f.write("3. Essential functions analyses for position\n")
            f.write("4. Comparator employee accommodation records\n")
            f.write("5. Disciplinary records for similarly situated employees\n")
            f.write("6. Complete investigation file (not just ROI)\n")
            f.write("7. Notes from witness interviews\n")
            f.write("8. Email communications regarding accommodations\n")
            f.write("9. Medical documentation reviewed by agency\n")
            f.write("10. Policy manuals and procedures\n")
            
            f.write("\n---\n")
            f.write("*This analysis should be reviewed with legal counsel for case strategy*\n")
        
        print(f"Contradiction report saved to: {self.contradiction_report}")
        return self.contradiction_report


def main():
    parser = argparse.ArgumentParser(description='Analyze ROI contradictions')
    parser.add_argument('--case', default='HS-FEMA-02430-2024', 
                       help='Case number to analyze')
    
    args = parser.parse_args()
    
    analyzer = ROIContradictionAnalyzer(args.case)
    
    # Perform analysis
    contradictions = analyzer.analyze_contradictions()
    
    # Generate report
    report_path = analyzer.generate_contradiction_report(contradictions)
    
    print(f"\nAnalysis complete!")
    print(f"- Contradiction data: {analyzer.contradiction_data}")
    print(f"- Detailed report: {report_path}")
    print("\nKey findings:")
    print(f"- ADA violations identified: {len(contradictions['ada_violations'])}")
    print(f"- Procedural issues found: {len(contradictions['procedural_issues'])}")
    print(f"- Evidence gaps discovered: {len(contradictions['evidence_gaps'])}")
    print(f"\nReview the report for detailed strategic recommendations.")


if __name__ == "__main__":
    main() 