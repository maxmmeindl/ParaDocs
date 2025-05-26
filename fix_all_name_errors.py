#!/usr/bin/env python3
"""
Fix all name errors in case documentation
Replaces "Nolly" with "Max J. Meindl III"
"""

import os
import re
from pathlib import Path

def fix_name_errors():
    """Fix all instances of incorrect names in case files"""
    
    # Files to fix
    files_to_fix = [
        'COMPREHENSIVE_COMMUNICATION_TIMELINE.html',
        'COMPLETE_EMAIL_INDEX.html',
        'timeline_exhibit_HS-FEMA-02430-2024.html',
        'extract_roi_dates.py',
        'comprehensive_timeline_HS-FEMA-02430-2024.json',
        'comprehensive_timeline_analysis.py',
        'actual_timeline_from_roi.json',
        'verification_report.json',
        'GAMMA_APP_PRESENTATION.html',
        'paradocs-eeo-website/frontend/src/pages/Timeline.tsx',
        'manual_timeline_HS-FEMA-02430-2024.json',
        'roi_comprehensive_analysis_HS-FEMA-02430-2024.json',
        'roi_comprehensive_analysis_HS-FEMA-02430-2024.md'
    ]
    
    # Replacements to make
    replacements = {
        'Nolly (Complainant)': 'Max J. Meindl III (Complainant)',
        'Nolly': 'Max J. Meindl III',
        'Complainant (Nolly)': 'Max J. Meindl III (Complainant)',
        'Employee': 'Max J. Meindl III',
        'Employee/Representative': 'Max J. Meindl III/Representative',
        # Generic complainant references
        '"Complainant"': '"Max J. Meindl III"',
        '>Complainant<': '>Max J. Meindl III<',
        'Complainant<br>': 'Max J. Meindl III<br>',
        'To:</strong> Complainant': 'To:</strong> Max J. Meindl III',
        'From:</strong> Complainant': 'From:</strong> Max J. Meindl III'
    }
    
    fixed_files = []
    errors = []
    
    for file_path in files_to_fix:
        try:
            full_path = Path(file_path)
            if not full_path.exists():
                print(f"File not found: {file_path}")
                continue
                
            # Read the file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply replacements
            for old_text, new_text in replacements.items():
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    print(f"Replaced '{old_text}' in {file_path}")
            
            # Special case for employee references that shouldn't be changed in certain contexts
            # (e.g., "federal employees", "other employees", etc.)
            content = re.sub(r'\bEmployee\s+(?!benefits|and|with|ID|termination)', 
                           'Max J. Meindl III ', content)
            
            # Write back if changes were made
            if content != original_content:
                # Create backup
                backup_path = f"{full_path}.backup_before_name_fix"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_files.append(file_path)
                print(f"✓ Fixed: {file_path}")
            else:
                print(f"No changes needed: {file_path}")
                
        except Exception as e:
            errors.append(f"{file_path}: {str(e)}")
            print(f"✗ Error fixing {file_path}: {e}")
    
    # Generate report
    print("\n" + "="*60)
    print("NAME ERROR FIX REPORT")
    print("="*60)
    print(f"\nFiles fixed: {len(fixed_files)}")
    for f in fixed_files:
        print(f"  - {f}")
    
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
    
    print("\nRECOMMENDATIONS:")
    print("1. Review the fixed files to ensure corrections are appropriate")
    print("2. Update any other names that appear to be placeholders:")
    print("   - John Smith → [Actual Supervisor Name]")
    print("   - Sarah Johnson → [Actual HR Manager Name]")
    print("   - Jennifer Wilson → [Actual New Supervisor Name]")
    print("   - Robert Brown → [Actual HR Director Name]")
    print("   - Michael Davis → [Actual Department Head Name]")
    print("   - Patricia Lee → [Actual EEO Counselor Name]")
    print("   - Maria Garcia → [Actual EEO Investigator Name]")
    print("   - David Martinez → [Actual EEO Director Name]")
    print("   - Lisa Chen → [Actual FEMA Legal Counsel Name]")
    print("   - Judge Thompson → [Actual Judge Name]")
    print("\n3. If these are the actual names, no further action needed")
    print("4. Consider running this script again after updating the replacements dictionary")

if __name__ == "__main__":
    fix_name_errors() 