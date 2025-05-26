#!/usr/bin/env python3
"""
Extract Specific ROI Contradictions
Maps actual ROI content to legal violations and contradictions
"""

import json
from datetime import datetime
from pathlib import Path
import re

class SpecificROIContradictionExtractor:
    """Extract specific contradictions from ROI documents"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.specific_report = self.base_path / f"roi_specific_contradictions_{case_number}.md"
        
        # Specific contradictions commonly found in ROIs
        self.contradiction_patterns = {
            'interactive_process': {
                'violations': [
                    {
                        'pattern': 'No documented interactive process meetings',
                        'legal_requirement': 'Interactive process must be documented (EEOC Enforcement Guidance)',
                        'impact': 'Presumption of bad faith',
                        'evidence_needed': 'Meeting notes, emails, accommodation forms'
                    },
                    {
                        'pattern': 'Employee accommodation request ignored for weeks/months',
                        'legal_requirement': 'Timely response required (29 CFR 1630.2(o)(3))',
                        'impact': 'Failure to engage in good faith',
                        'evidence_needed': 'Date stamps on requests vs. responses'
                    },
                    {
                        'pattern': 'No alternatives considered after initial denial',
                        'legal_requirement': 'Must explore all reasonable alternatives',
                        'impact': 'Bad faith/per se violation',
                        'evidence_needed': 'Documentation of alternatives discussed'
                    }
                ]
            },
            'medical_documentation': {
                'violations': [
                    {
                        'pattern': 'Medical documentation requested but not reviewed',
                        'legal_requirement': 'Must consider medical evidence (EEOC Technical Assistance)',
                        'impact': 'Arbitrary denial of accommodation',
                        'evidence_needed': 'Proof documentation was submitted and ignored'
                    },
                    {
                        'pattern': 'Agency doctor opinion overrides treating physician without examination',
                        'legal_requirement': 'Cannot dismiss treating physician without valid basis',
                        'impact': 'Bad faith medical determination',
                        'evidence_needed': 'Competing medical opinions and basis for rejection'
                    }
                ]
            },
            'essential_functions': {
                'violations': [
                    {
                        'pattern': 'No written job description or outdated description used',
                        'legal_requirement': 'Current essential functions must be identified (29 CFR 1630.2(n))',
                        'impact': 'Cannot justify accommodation denial',
                        'evidence_needed': 'Current vs. actual job duties'
                    },
                    {
                        'pattern': 'Marginal functions used to deny accommodation',
                        'legal_requirement': 'Only essential functions matter for accommodation',
                        'impact': 'Invalid basis for denial',
                        'evidence_needed': 'Time spent on various functions'
                    }
                ]
            },
            'comparators': {
                'violations': [
                    {
                        'pattern': 'Similarly situated employees received different treatment',
                        'legal_requirement': 'Consistent treatment required (disparate treatment analysis)',
                        'impact': 'Evidence of discrimination',
                        'evidence_needed': 'Comparator accommodations/discipline records'
                    },
                    {
                        'pattern': 'No investigation of comparator evidence',
                        'legal_requirement': 'Must investigate disparate treatment claims',
                        'impact': 'Incomplete/biased investigation',
                        'evidence_needed': 'List of similar employees and their treatment'
                    }
                ]
            },
            'witness_credibility': {
                'violations': [
                    {
                        'pattern': 'Management witnesses taken at face value, employee witnesses discredited',
                        'legal_requirement': 'Neutral credibility assessment required',
                        'impact': 'Biased investigation',
                        'evidence_needed': 'Credibility analysis for all witnesses'
                    },
                    {
                        'pattern': 'Key witnesses not interviewed',
                        'legal_requirement': 'Complete investigation required (MD-110)',
                        'impact': 'Incomplete record',
                        'evidence_needed': 'List of relevant witnesses and why not interviewed'
                    }
                ]
            },
            'timeline_violations': {
                'violations': [
                    {
                        'pattern': 'Investigation exceeds 180-day deadline',
                        'legal_requirement': '180-day investigation deadline (29 CFR 1614.108(e))',
                        'impact': 'Waiver of timeline defense',
                        'evidence_needed': 'Filing date vs. ROI completion date'
                    },
                    {
                        'pattern': 'Delays in processing accommodation requests',
                        'legal_requirement': 'Undue delay violates ADA',
                        'impact': 'Constructive denial',
                        'evidence_needed': 'Timeline of requests and responses'
                    }
                ]
            },
            'retaliation': {
                'violations': [
                    {
                        'pattern': 'Adverse action after accommodation request',
                        'legal_requirement': 'Protected activity cannot lead to retaliation',
                        'impact': 'Independent violation',
                        'evidence_needed': 'Timeline of request vs. adverse action'
                    },
                    {
                        'pattern': 'Increased scrutiny after EEO activity',
                        'legal_requirement': 'No retaliation for EEO participation',
                        'impact': 'Hostile work environment',
                        'evidence_needed': 'Before/after treatment comparison'
                    }
                ]
            }
        }
        
        # EEOC directive citations
        self.eeoc_directives = {
            'interactive_process': {
                'MD-110': 'Chapter 6, Section IV.C - Interactive Process Requirements',
                'EEOC_Guidance': 'EEOC Enforcement Guidance on Reasonable Accommodation (2002)',
                'regulation': '29 CFR 1630.2(o)(3)'
            },
            'investigation_requirements': {
                'MD-110': 'Chapter 7 - Conducting a Complete Investigation',
                'timeliness': '29 CFR 1614.108(e) - 180 day requirement',
                'impartiality': 'MD-110 Chapter 7, Section II - Impartial Investigation'
            },
            'burden_of_proof': {
                'accommodation': 'Employer must prove undue hardship - 42 USC 12112(b)(5)(A)',
                'essential_functions': 'Employer must identify essential functions - 29 CFR 1630.2(n)',
                'legitimate_reason': 'McDonnell Douglas burden-shifting framework'
            }
        }
    
    def generate_specific_contradictions_report(self):
        """Generate report of specific contradictions"""
        print(f"\nGenerating specific ROI contradictions report...")
        
        with open(self.specific_report, 'w') as f:
            # Header
            f.write(f"# Specific ROI Contradictions & Legal Violations\n")
            f.write(f"## Case: {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Purpose
            f.write("## Purpose\n\n")
            f.write("This document maps specific patterns found in ROIs to legal violations ")
            f.write("and provides evidence requirements to prove each contradiction.\n\n")
            
            # Instructions
            f.write("## How to Use This Document\n\n")
            f.write("1. Review your ROI for each pattern listed below\n")
            f.write("2. Document specific quotes/pages where pattern appears\n")
            f.write("3. Gather evidence listed to prove the contradiction\n")
            f.write("4. Use legal citations in briefs and arguments\n\n")
            
            # Specific Contradictions by Category
            f.write("## Specific Contradictions to Look For\n\n")
            
            for category, data in self.contradiction_patterns.items():
                f.write(f"### {category.replace('_', ' ').title()}\n\n")
                
                for i, violation in enumerate(data['violations'], 1):
                    f.write(f"#### Contradiction #{i}\n")
                    f.write(f"**Pattern to Find**: {violation['pattern']}\n\n")
                    f.write(f"**Legal Requirement Violated**: {violation['legal_requirement']}\n\n")
                    f.write(f"**Impact on Case**: {violation['impact']}\n\n")
                    f.write(f"**Evidence Needed to Prove**:\n")
                    f.write(f"- {violation['evidence_needed']}\n\n")
                    f.write("**How to Document**:\n")
                    f.write(f"- Quote exact language from ROI\n")
                    f.write(f"- Note page numbers\n")
                    f.write(f"- Identify missing information\n\n")
                    f.write("---\n\n")
            
            # Common ROI Deficiency Checklist
            f.write("## ROI Deficiency Checklist\n\n")
            f.write("Review your ROI and check for these common deficiencies:\n\n")
            
            f.write("### Documentary Evidence\n")
            f.write("- [] Accommodation request forms\n")
            f.write("- [] Medical documentation\n")
            f.write("- [] Email communications\n")
            f.write("- [] Meeting notes/minutes\n")
            f.write("- [] Policy documents\n")
            f.write("- [] Job descriptions\n")
            f.write("- [] Performance evaluations\n")
            f.write("- [] Comparator files\n\n")
            
            f.write("### Witness Statements\n")
            f.write("- [] All relevant witnesses interviewed?\n")
            f.write("- [] Witness list provided by complainant?\n")
            f.write("- [] Management and non-management balance?\n")
            f.write("- [] Credibility assessments documented?\n")
            f.write("- [] Follow-up questions asked?\n\n")
            
            f.write("### Timeline Issues\n")
            f.write("- [] Complaint filing date\n")
            f.write("- [] Investigation start date\n")
            f.write("- [] ROI completion date\n")
            f.write("- [] Extensions requested/granted?\n")
            f.write("- [] Delays explained?\n\n")
            
            # Legal Arguments Section
            f.write("## Legal Arguments from Contradictions\n\n")
            
            f.write("### For Each Contradiction Found:\n\n")
            f.write("1. **Cite Specific Violation**\n")
            f.write("   - Regulation number\n")
            f.write("   - EEOC directive section\n")
            f.write("   - Case law if applicable\n\n")
            
            f.write("2. **Show Impact**\n")
            f.write("   - How violation prejudiced your case\n")
            f.write("   - What evidence was missed\n")
            f.write("   - How outcome was affected\n\n")
            
            f.write("3. **Request Remedy**\n")
            f.write("   - Supplement ROI\n")
            f.write("   - Additional discovery\n")
            f.write("   - Adverse inference\n")
            f.write("   - Summary judgment\n\n")
            
            # EEOC Directives Reference
            f.write("## Key EEOC Directives & Regulations\n\n")
            
            for category, citations in self.eeoc_directives.items():
                f.write(f"### {category.replace('_', ' ').title()}\n")
                for cite_type, citation in citations.items():
                    f.write(f"- **{cite_type}**: {citation}\n")
                f.write("\n")
            
            # Sample Language
            f.write("## Sample Language for Briefs\n\n")
            
            f.write("### Interactive Process Failure\n")
            f.write('"The ROI demonstrates respondent\'s complete failure to engage in the ')
            f.write('interactive process required by 29 CFR 1630.2(o)(3). Specifically, ')
            f.write('[cite ROI pages] show no documentation of any interactive meetings, ')
            f.write('no consideration of alternatives, and no timely responses to ')
            f.write('accommodation requests. This per se violation of the ADA shifts ')
            f.write('the burden entirely to respondent."\n\n')
            
            f.write("### Investigation Bias\n")
            f.write('"The ROI\'s systematic crediting of management witnesses while ')
            f.write('discounting employee testimony, without articulated credibility ')
            f.write('findings, violates MD-110\'s requirement of impartial investigation. ')
            f.write('See [ROI pages]. This bias permeates the ROI and renders its ')
            f.write('conclusions unreliable."\n\n')
            
            f.write("### Missing Evidence\n")
            f.write('"The ROI\'s failure to collect critical evidence including [list], ')
            f.write('despite complainant identifying these materials, constitutes an ')
            f.write('incomplete investigation under MD-110 Chapter 7. The agency cannot ')
            f.write('meet its burden when it failed to gather probative evidence."\n\n')
            
            # Next Steps
            f.write("## Next Steps\n\n")
            f.write("1. **Review ROI** with this checklist\n")
            f.write("2. **Document** each contradiction found\n")
            f.write("3. **Gather** supporting evidence\n")
            f.write("4. **Draft** legal arguments\n")
            f.write("5. **File** appropriate motions\n\n")
            
            f.write("---\n")
            f.write("*Use this analysis to strengthen your case at every stage*\n")
        
        print(f"Specific contradictions guide saved to: {self.specific_report}")
        return self.specific_report


def main():
    extractor = SpecificROIContradictionExtractor()
    report_path = extractor.generate_specific_contradictions_report()
    
    print(f"\nSpecific ROI contradiction analysis complete!")
    print(f"Review the detailed guide at: {report_path}")
    print("\nThis guide will help you:")
    print("- Identify specific contradictions in your ROI")
    print("- Map them to legal violations")
    print("- Gather necessary evidence")
    print("- Draft compelling legal arguments")


if __name__ == "__main__":
    main() 