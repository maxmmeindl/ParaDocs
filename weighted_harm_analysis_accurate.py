#!/usr/bin/env python3
"""
Weighted Harm Analysis - Accurate with January 6, 2025 Termination
Comprehensive analysis of all harms by weight, validity, and legal support
"""

from datetime import datetime, timedelta
import json

class WeightedHarmAnalysis:
    """Analyze all harms with proper weighting and legal support"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.termination_date = datetime(2025, 1, 6)  # CORRECT DATE
        self.current_date = datetime.now()
        self.annual_salary = 150000  # Adjust based on actual
        
    def calculate_all_harms(self):
        """Calculate and weight all harms with legal support"""
        
        print("WEIGHTED HARM ANALYSIS - ALL DAMAGES")
        print("=" * 70)
        print(f"Termination Date: January 6, 2025")
        print(f"Current Date: {self.current_date.strftime('%B %d, %Y')}")
        print(f"Time Since Termination: {(self.current_date - self.termination_date).days} days")
        print("\n")
        
        # Calculate time periods
        days_since_termination = (self.current_date - self.termination_date).days
        months_since_termination = days_since_termination / 30.44
        
        harms = {
            'tier_1_immediate_economic': {
                'weight': 10,  # Highest weight - immediate, quantifiable
                'validity': 'CERTAIN',
                'harms': {
                    'lost_wages': {
                        'description': 'Wages lost since January 6, 2025',
                        'calculation': f'{months_since_termination:.1f} months × ${self.annual_salary/12:,.0f}/month',
                        'amount': (self.annual_salary / 12) * months_since_termination,
                        'legal_support': [
                            'Back pay automatic for discriminatory termination - 42 USC 2000e-5(g)',
                            'Mount Healthy v. Doyle, 429 U.S. 274 (1977)',
                            'Albemarle Paper Co. v. Moody, 422 U.S. 405 (1975)'
                        ],
                        'evidence_strength': 'Payroll records, termination letter',
                        'ongoing': True
                    },
                    'lost_benefits': {
                        'description': 'Health insurance, retirement matching, etc.',
                        'amount': (self.annual_salary * 0.30 / 12) * months_since_termination,
                        'legal_support': [
                            'Benefits part of make-whole relief',
                            'EEOC Compliance Manual on Remedies'
                        ],
                        'evidence_strength': 'Benefits statements, HR records'
                    },
                    'cobra_costs': {
                        'description': 'Out-of-pocket health insurance',
                        'amount': 1800 * months_since_termination,
                        'legal_support': [
                            'Mitigation expenses recoverable',
                            'EEOC v. Goodyear Aerospace, 813 F.2d 1539 (9th Cir. 1987)'
                        ],
                        'evidence_strength': 'COBRA payment receipts'
                    }
                }
            },
            'tier_2_future_economic': {
                'weight': 9,  # Very high - quantifiable with expert testimony
                'validity': 'HIGHLY PROBABLE',
                'harms': {
                    'front_pay': {
                        'description': 'Future lost wages (2-3 years typical)',
                        'amount': self.annual_salary * 2,
                        'legal_support': [
                            'Front pay when reinstatement not feasible',
                            'Pollard v. E.I. du Pont, 532 U.S. 843 (2001)',
                            '29 CFR 1614.501(a)(2)'
                        ],
                        'evidence_strength': 'Labor market analysis, job search efforts'
                    },
                    'pension_loss': {
                        'description': 'Federal retirement benefits (FERS/TSP)',
                        'amount': self.annual_salary * 5,  # Conservative
                        'legal_support': [
                            'Loeffler v. Frank, 486 U.S. 549 (1988)',
                            'Make-whole includes retirement losses'
                        ],
                        'evidence_strength': 'Actuarial calculations, TSP statements'
                    }
                }
            },
            'tier_3_accommodation_violation': {
                'weight': 8,  # High - clear violation but damages harder to quantify
                'validity': 'CERTAIN',
                'harms': {
                    '1340_day_violation': {
                        'description': '1,340 days without accommodation (Sept 2020 - May 2024)',
                        'amount': 550684.93,
                        'legal_support': [
                            'Each day = continuing violation',
                            'Hostile work environment damages',
                            'National R.R. Passenger Corp. v. Morgan, 536 U.S. 101 (2002)'
                        ],
                        'evidence_strength': 'ROI admissions, email trail'
                    },
                    '36_day_violation': {
                        'description': '36-day delay on second request',
                        'amount': 14794.52,  # 36 days × daily rate
                        'legal_support': [
                            'Exceeded 30-day requirement',
                            '29 CFR 1630.2(o)(3)'
                        ],
                        'evidence_strength': 'Date stamps on request/denial'
                    }
                }
            },
            'tier_4_emotional_distress': {
                'weight': 7,  # Significant but requires testimony
                'validity': 'PROBABLE',
                'harms': {
                    'termination_distress': {
                        'description': 'Emotional harm from wrongful firing',
                        'amount': 100000,
                        'legal_support': [
                            'Carey v. Piphus, 435 U.S. 247 (1978)',
                            'Memphis Community School Dist. v. Stachura, 477 U.S. 299 (1986)',
                            'EEOC v. Ind. Bell Tel. Co., 256 F.3d 516 (7th Cir. 2001)'
                        ],
                        'evidence_strength': 'Medical records, therapy, testimony'
                    },
                    'discrimination_distress': {
                        'description': '3.7 years of accommodation denial',
                        'amount': 150000,
                        'legal_support': [
                            'Duration and severity factors',
                            'EEOC Enforcement Guidance on Compensatory Damages'
                        ],
                        'evidence_strength': 'Daily suffering testimony'
                    }
                }
            },
            'tier_5_consequential': {
                'weight': 6,  # Real but secondary harms
                'validity': 'LIKELY',
                'harms': {
                    'job_search_costs': {
                        'description': 'Resume, networking, training costs',
                        'amount': 10000,
                        'legal_support': [
                            'Mitigation costs recoverable',
                            'Rasimas v. Mich. Dept of Mental Health, 714 F.2d 614 (6th Cir. 1983)'
                        ],
                        'evidence_strength': 'Receipts, documentation'
                    },
                    'credit_damage': {
                        'description': 'Financial stress impacts',
                        'amount': 15000,
                        'legal_support': [
                            'Consequential damages if foreseeable',
                            'Tooson v. MSPB, 325 F.3d 1342 (Fed. Cir. 2003)'
                        ],
                        'evidence_strength': 'Credit reports, late fees'
                    }
                }
            },
            'tier_6_punitive': {
                'weight': 10,  # Maximum impact on agency behavior
                'validity': 'HIGHLY LIKELY',
                'harms': {
                    'punitive_damages': {
                        'description': 'Punishment for egregious conduct',
                        'amount': 300000,  # Federal cap
                        'legal_support': [
                            '42 USC 1981a(b)(3) - Federal cap $300K',
                            'Kolstad v. ADA, 527 U.S. 526 (1999)',
                            'EEOC v. Fed. Express, 513 F.3d 360 (4th Cir. 2008)'
                        ],
                        'evidence_strength': '1,340 days + retaliation = malice'
                    }
                }
            }
        }
        
        # Generate comprehensive report
        with open('weighted_harm_analysis.md', 'w') as f:
            f.write("# WEIGHTED HARM ANALYSIS\n")
            f.write(f"## Case: {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%B %d, %Y')}\n\n")
            
            f.write("## Key Facts\n")
            f.write(f"- **Termination Date**: January 6, 2025\n")
            f.write(f"- **Days Since Termination**: {days_since_termination}\n")
            f.write(f"- **Months Since Termination**: {months_since_termination:.1f}\n")
            f.write(f"- **Annual Salary**: ${self.annual_salary:}\n\n")
            
            total_damages = 0
            
            for tier_name, tier_data in harms.items():
                tier_total = sum(harm['amount'] for harm in tier_data['harms'].values())
                total_damages += tier_total
                
                f.write(f"\n## {tier_name.replace('_', ' ').title()}\n")
                f.write(f"**Weight**: {tier_data['weight']}/10 | ")
                f.write(f"**Validity**: {tier_data['validity']} | ")
                f.write(f"**Total**: ${tier_total:,.2f}\n\n")
                
                for harm_name, harm_data in tier_data['harms'].items():
                    f.write(f"### {harm_name.replace('_', ' ').title()}: ${harm_data['amount']:,.2f}\n")
                    f.write(f"**Description**: {harm_data['description']}\n\n")
                    
                    f.write("**Legal Support**:\n")
                    for citation in harm_data['legal_support']:
                        f.write(f"- {citation}\n")
                    
                    f.write(f"\n**Evidence**: {harm_data['evidence_strength']}\n\n")
                    f.write("---\n\n")
            
            f.write(f"\n## TOTAL DAMAGES: ${total_damages:,.2f}\n\n")
            
            # Priority ranking
            f.write("## Priority Ranking by Weight & Validity\n\n")
            f.write("1. **Lost Wages Since Termination** (Weight: 10, Validity: CERTAIN)\n")
            f.write("   - Easiest to prove, ongoing harm\n")
            f.write("   - Clear documentation available\n\n")
            
            f.write("2. **1,340-Day Accommodation Violation** (Weight: 8, Validity: CERTAIN)\n")
            f.write("   - Per se liability established\n")
            f.write("   - ROI contains admissions\n\n")
            
            f.write("3. **Punitive Damages** (Weight: 10, Validity: HIGHLY LIKELY)\n")
            f.write("   - 1,340 days = malice/reckless indifference\n")
            f.write("   - Retaliation pattern strengthens claim\n\n")
            
            f.write("4. **Front Pay** (Weight: 9, Validity: HIGHLY PROBABLE)\n")
            f.write("   - Standard remedy when reinstatement not feasible\n")
            f.write("   - 2-3 years typical for federal employees\n\n")
            
            f.write("## Strategic Recommendations\n\n")
            f.write("### Lead With:\n")
            f.write("1. **Termination damages** - Most immediate, relatable harm\n")
            f.write("2. **1,340-day violation** - Shocking, establishes bad faith\n")
            f.write("3. **Retaliation pattern** - PIP to Termination timeline\n\n")
            
            f.write("### Settlement Positioning:\n")
            f.write("- **Floor**: $1M (economic damages alone)\n")
            f.write("- **Target**: $1.5M (with emotional distress)\n")
            f.write("- **Ceiling**: $2M+ (with punitive damages)\n\n")
            
            f.write("### Trial Strategy:\n")
            f.write("- Day 1: Lost wages calculator running in courtroom\n")
            f.write("- Exhibit A: 1,340-day timeline poster\n")
            f.write("- Witness 1: You testifying about financial devastation\n")
            f.write("- Expert: Vocational economist on career loss\n")
        
        return total_damages


def main():
    analyzer = WeightedHarmAnalysis()
    
    print("Generating weighted harm analysis with correct dates...")
    total = analyzer.calculate_all_harms()
    
    print(f"\nTOTAL DAMAGES CALCULATED: ${total:,.2f}")
    print("\nGenerated: weighted_harm_analysis.md")
    print("\nKey Finding: Recent termination (Jan 2025) means damages are still accumulating!")


if __name__ == "__main__":
    main() 