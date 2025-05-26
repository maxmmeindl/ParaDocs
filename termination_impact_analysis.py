#!/usr/bin/env python3
"""
Termination Impact Analysis - The Real Harm
Focus on getting FIRED as the primary damage
"""

from datetime import datetime, timedelta
import json

class TerminationImpactAnalysis:
    """Analyze the real impact of getting FIRED"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.termination_date = datetime(2024, 5, 30)
        self.current_date = datetime.now()
        
    def calculate_termination_damages(self, annual_salary=150000):
        """Calculate comprehensive termination damages"""
        
        print("TERMINATION IMPACT ANALYSIS - THE REAL HARM")
        print("=" * 70)
        print(f"\nYou were FIRED on {self.termination_date.strftime('%B %d, %Y')}")
        print(f"During an active EEO investigation (Per Se Retaliation)")
        print("\n")
        
        # Time calculations
        days_since_termination = (self.current_date - self.termination_date).days
        months_since_termination = days_since_termination / 30.44
        years_since_termination = days_since_termination / 365.25
        
        damages = {
            'immediate_losses': {
                'lost_wages': {
                    'description': 'Wages lost since termination',
                    'calculation': f'{months_since_termination:.1f} months × ${annual_salary/12:,.0f}/month',
                    'amount': (annual_salary / 12) * months_since_termination,
                    'ongoing': True
                },
                'lost_benefits': {
                    'description': 'Health insurance, retirement, etc.',
                    'calculation': '30% of salary value',
                    'amount': (annual_salary * 0.30 / 12) * months_since_termination,
                    'components': [
                        'Health insurance ($1,500/month)',
                        'Retirement matching (6% of salary)',
                        'Life insurance',
                        'Disability insurance',
                        'FSA/HSA contributions'
                    ]
                },
                'cobra_costs': {
                    'description': 'Out-of-pocket health insurance',
                    'calculation': f'{months_since_termination:.1f} months × $1,800/month',
                    'amount': 1800 * months_since_termination
                }
            },
            'future_losses': {
                'front_pay': {
                    'description': 'Future lost wages until comparable employment',
                    'typical_period': '2-3 years for federal employee',
                    'calculation': '2 years × annual salary',
                    'amount': annual_salary * 2,
                    'factors': [
                        'Specialized federal position',
                        'Security clearance requirements',
                        'Limited comparable positions',
                        'Reputational harm from termination'
                    ]
                },
                'pension_impact': {
                    'description': 'Lost federal retirement benefits',
                    'calculation': 'Actuarial calculation needed',
                    'amount': annual_salary * 5,  # Conservative estimate
                    'components': [
                        'FERS pension reduction',
                        'TSP matching losses',
                        'Retiree health benefits',
                        'Years of service credit'
                    ]
                },
                'career_progression': {
                    'description': 'Lost promotions and advancement',
                    'calculation': '20% salary growth over 5 years',
                    'amount': annual_salary * 0.20 * 5
                }
            },
            'consequential_damages': {
                'job_search_costs': {
                    'description': 'Resume services, travel, training',
                    'amount': 10000
                },
                'relocation_costs': {
                    'description': 'May need to move for new job',
                    'amount': 25000
                },
                'credit_impact': {
                    'description': 'Financial stress, credit damage',
                    'amount': 15000
                },
                'emotional_distress': {
                    'description': 'Anxiety, depression from job loss',
                    'amount': 100000,
                    'factors': [
                        'Sudden loss of income',
                        'Career destruction',
                        'Family stress',
                        'Loss of professional identity'
                    ]
                }
            },
            'retaliation_multiplier': {
                'description': 'Termination during EEO = egregious retaliation',
                'factors': [
                    'Fired DURING investigation',
                    'Clear temporal proximity',
                    'No legitimate reason',
                    'Pattern of retaliation (PIP first)'
                ],
                'legal_significance': 'Jury will be outraged',
                'punitive_eligibility': 'Maximum punitive damages justified'
            }
        }
        
        # Calculate totals
        immediate_total = sum(item['amount'] for item in damages['immediate_losses'].values())
        future_total = sum(item['amount'] for item in damages['future_losses'].values())
        consequential_total = sum(item['amount'] for item in damages['consequential_damages'].values())
        
        total_termination_damages = immediate_total + future_total + consequential_total
        
        # Generate report
        with open('termination_impact_analysis.md', 'w') as f:
            f.write("# TERMINATION IMPACT ANALYSIS\n")
            f.write(f"## Case: {self.case_number}\n\n")
            
            f.write("## THE REAL HARM: YOU GOT FIRED!\n\n")
            
            f.write(f"**Termination Date**: May 30, 2024\n")
            f.write(f"**Time Since Termination**: {months_since_termination:.1f} months\n")
            f.write(f"**Status**: FIRED during active EEO investigation (PER SE RETALIATION)\n\n")
            
            f.write("## Immediate Financial Impact\n\n")
            f.write(f"### Lost Wages: ${damages['immediate_losses']['lost_wages']['amount']:,.2f}\n")
            f.write(f"- {months_since_termination:.1f} months without income\n")
            f.write(f"- Still accumulating at ${annual_salary/12:,.0f}/month\n\n")
            
            f.write(f"### Lost Benefits: ${damages['immediate_losses']['lost_benefits']['amount']:,.2f}\n")
            for component in damages['immediate_losses']['lost_benefits']['components']:
                f.write(f"- {component}\n")
            f.write("\n")
            
            f.write(f"### COBRA Costs: ${damages['immediate_losses']['cobra_costs']['amount']:,.2f}\n")
            f.write("- Paying full premium out of pocket\n")
            f.write("- While having NO INCOME\n\n")
            
            f.write(f"**IMMEDIATE LOSSES: ${immediate_total:,.2f}**\n\n")
            
            f.write("## Future Financial Impact\n\n")
            f.write(f"### Front Pay: ${damages['future_losses']['front_pay']['amount']:,.2f}\n")
            f.write("Why 2-3 years is reasonable:\n")
            for factor in damages['future_losses']['front_pay']['factors']:
                f.write(f"- {factor}\n")
            f.write("\n")
            
            f.write(f"### Pension/Retirement Loss: ${damages['future_losses']['pension_impact']['amount']:,.2f}\n")
            f.write("Federal retirement benefits destroyed:\n")
            for component in damages['future_losses']['pension_impact']['components']:
                f.write(f"- {component}\n")
            f.write("\n")
            
            f.write(f"**FUTURE LOSSES: ${future_total:,.2f}**\n\n")
            
            f.write("## Consequential Damages\n\n")
            for category, details in damages['consequential_damages'].items():
                f.write(f"### {category.replace('_', ' ').title()}: ${details['amount']:,.2f}\n")
                f.write(f"{details['description']}\n\n")
            
            f.write(f"**CONSEQUENTIAL DAMAGES: ${consequential_total:,.2f}**\n\n")
            
            f.write("## Why This Is PER SE Retaliation\n\n")
            f.write("Timeline that proves retaliation:\n")
            f.write("1. **March 15, 2024**: EEO complaint accepted\n")
            f.write("3. **April 15, 2024**: Investigation begins\n")
            f.write("4. **May 30, 2024**: FIRED during investigation\n\n")
            
            f.write("No employer can explain this timing!\n\n")
            
            f.write("## TOTAL TERMINATION DAMAGES\n\n")
            f.write(f"- Immediate Losses: ${immediate_total:,.2f}\n")
            f.write(f"- Future Losses: ${future_total:,.2f}\n")
            f.write(f"- Consequential: ${consequential_total:,.2f}\n\n")
            f.write(f"**TOTAL: ${total_termination_damages:,.2f}**\n\n")
            
            f.write("## Bottom Line\n\n")
            f.write("Getting FIRED is the worst thing that happened here. Yes, the 1,340-day ")
            f.write("accommodation violation is outrageous, but:\n\n")
            f.write("- You LOST YOUR JOB\n")
            f.write("- You LOST YOUR INCOME\n")
            f.write("- You LOST YOUR CAREER\n")
            f.write("- You LOST YOUR BENEFITS\n")
            f.write("- You LOST YOUR RETIREMENT\n\n")
            f.write("And they did it WHILE you had an active EEO complaint!\n\n")
            f.write("**This is why juries award big verdicts.**")
        
        return total_termination_damages
    
    def compare_to_accommodation_damages(self):
        """Compare termination vs accommodation damages"""
        
        print("\nDAMAGE COMPARISON")
        print("=" * 70)
        
        comparison = {
            'accommodation_violation': {
                'amount': 550684.93,
                'description': '1,340 days of no accommodation',
                'impact': 'Had to work without accommodation',
                'ongoing': 'No - ended when fired'
            },
            'termination': {
                'amount': self.calculate_termination_damages(150000),
                'description': 'FIRED during EEO investigation',
                'impact': 'Lost everything - job, income, career',
                'ongoing': 'YES - still suffering every day'
            }
        }
        
        print(f"\nAccommodation damages: ${comparison['accommodation_violation']['amount']:,.2f}")
        print(f"Termination damages: ${comparison['termination']['amount']:,.2f}")
        print(f"\nTermination is {comparison['termination']['amount']/comparison['accommodation_violation']['amount']:.1f}x worse!")
        
        return comparison


def main():
    analyzer = TerminationImpactAnalysis()
    
    # Calculate termination damages
    total_damages = analyzer.calculate_termination_damages(annual_salary=150000)
    
    # Compare to accommodation damages
    analyzer.compare_to_accommodation_damages()
    
    print("\n" + "="*70)
    print("GENERATED: termination_impact_analysis.md")
    print("="*70)
    print("\nKEY TAKEAWAY: Getting FIRED is the biggest harm.")
    print("Lead with the termination. It's what juries understand.")


if __name__ == "__main__":
    main() 