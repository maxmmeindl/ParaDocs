#!/usr/bin/env python3
"""
Extract specific data from EEOC tables for case support
"""

import os
from pathlib import Path
import json
from datetime import datetime

class TableDataExtractor:
    """Extract key statistics from EEOC tables"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.extract_report = self.base_path / f"data_extract_{case_number}.md"
        
    def extract_key_data(self):
        """Extract key data points from relevant tables"""
        print("\nExtracting key data points for case support...")
        
        # Create extraction report
        with open(self.extract_report, 'w') as f:
            f.write(f"# EEOC Data Extraction for Case {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Key Data Points for Your Case\n\n")
            
            # ADA Statistics
            f.write("### 1. ADA/Disability Discrimination Statistics\n\n")
            f.write("**From Table B-8 (Complaints by Basis):**\n")
            f.write("- Look for 'Disability' row to find:\n")
            f.write("  - Total disability complaints filed\n")
            f.write("  - Percentage of all complaints\n")
            f.write("  - Compare to other bases (race, age, etc.)\n\n")
            
            f.write("**From Table B-15 (Findings of Discrimination):**\n")
            f.write("- Find discrimination finding rates for:\n")
            f.write("  - Overall discrimination findings\n")
            f.write("  - ADA-specific findings if broken down\n")
            f.write("  - Settlement vs. judgment outcomes\n\n")
            
            # Termination Data
            f.write("### 2. Termination/Discharge Statistics\n\n")
            f.write("**From Table B-11 (Types of Closures):**\n")
            f.write("- Look for closure types related to termination\n")
            f.write("- Find percentage of cases involving discharge\n")
            f.write("- Compare merit vs. non-merit closures\n\n")
            
            # ADR Success Rates
            f.write("### 3. ADR Success Metrics\n\n")
            f.write("**From Table B-20 (ADR Resolutions):**\n")
            f.write("- ADR participation rates\n")
            f.write("- Resolution success percentages\n")
            f.write("- Average time to resolution\n\n")
            
            f.write("**From Table B-19 (ADR Participation):**\n")
            f.write("- Acceptance rates for ADR\n")
            f.write("- Outcomes when ADR is used vs. not used\n\n")
            
            # Processing Times
            f.write("### 4. Timeline Benchmarks\n\n")
            f.write("**From Table B-10 (Processing Days):**\n")
            f.write("- Average days from filing to closure\n")
            f.write("- Compare your timeline to averages\n")
            f.write("- Identify delays in your case\n\n")
            
            # Benefits and Remedies
            f.write("### 5. Settlement/Remedy Data\n\n")
            f.write("**From Table B-21 (Benefits Provided):**\n")
            f.write("- Types of remedies awarded\n")
            f.write("- Monetary compensation ranges\n")
            f.write("- Non-monetary relief types\n\n")
            
            # Data Collection Instructions
            f.write("## How to Extract This Data\n\n")
            f.write("1. **Open each Excel file** listed above\n")
            f.write("2. **Look for DHS/FEMA rows** - Many tables break down by agency\n")
            f.write("3. **Note specific numbers** for:\n")
            f.write("   - Your agency (DHS/FEMA)\n")
            f.write("   - Government-wide totals\n")
            f.write("   - Percentages and ratios\n\n")
            
            f.write("## Data Points to Highlight in Your Case\n\n")
            f.write("### For ADR Session:\n")
            f.write("- Show typical ADR success rates (Table B-20)\n")
            f.write("- Reference common settlement amounts (Table B-21)\n")
            f.write("- Demonstrate reasonableness of your requests\n\n")
            
            f.write("### For AJ Hearing:\n")
            f.write("- Present disability discrimination statistics (Table B-8)\n")
            f.write("- Show discrimination finding rates (Table B-15)\n")
            f.write("- Compare processing times to show delays (Table B-10)\n")
            f.write("- Reference typical remedies awarded (Table B-21)\n\n")
            
            f.write("## Visual Presentation Ideas\n\n")
            f.write("1. **Bar Chart**: Complaint bases showing disability percentage\n")
            f.write("2. **Timeline**: Your case vs. average processing times\n")
            f.write("3. **Pie Chart**: ADR success rates\n")
            f.write("4. **Table**: Remedy types and frequencies\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Open the Excel files and extract specific numbers\n")
            f.write("2. Create a one-page statistical summary\n")
            f.write("3. Prepare visual charts for key data\n")
            f.write("4. Draft talking points using the statistics\n\n")
        
        print(f"Data extraction guide saved to: {self.extract_report}")
        return self.extract_report

def main():
    extractor = TableDataExtractor()
    extractor.extract_key_data()
    
    print("\nTo continue building your case:")
    print("1. Review the cross-reference report: case_support_report_HS-FEMA-02430-2024.md")
    print("2. Follow the data extraction guide: data_extract_HS-FEMA-02430-2024.md")
    print("3. Open the specific Excel tables mentioned to get exact statistics")

if __name__ == "__main__":
    main() 