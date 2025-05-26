#!/usr/bin/env python3
"""
Final cleanup script to remove ALL PIP references and replace with warnings
"""

import os
import re
import json
from datetime import datetime

# Files to skip
SKIP_FILES = {
    'FINAL_PIP_CLEANUP_SCRIPT.py',
    'COMPREHENSIVE_PROJECT_REVIEW_AND_CORRECTIONS.md',
    'CORRECTED_MASTER_INDEX_VERIFIED.html'
}

# Track changes
changes_made = []

def clean_pip_references(content, filename):
    """Remove or replace PIP references with warnings"""
    original = content
    changes = []
    
    # Pattern replacements
    replacements = [
        # Timeline HTML files
        (r'<div class="date">March 20, 2024</div>\s*<h2>Performance Improvement Plan \(PIP\) Issued</h2>.*?</div>', 
         '<!-- REMOVED: Fabricated PIP reference - no documentation exists -->', re.DOTALL),
        
        # JSON event entries
        (r'{\s*"date":\s*"2024-03-20"[^}]*"PIP"[^}]*},?\s*', '', re.DOTALL),
        (r'{\s*"event":\s*"Performance Improvement Plan[^}]*},?\s*', '', re.DOTALL),
        
        # Email subjects
        (r'Performance Improvement Plan Required', '[UNVERIFIED] Performance Concerns Raised', 0),
        (r'PIP Progress Review.*?Unsatisfactory', '[UNVERIFIED] Performance Discussion', 0),
        
        # Descriptions mentioning PIP
        (r'PIP during EEO case', 'Performance concerns raised during EEO case [UNVERIFIED]', 0),
        (r'Negative PIP review', 'Negative performance feedback [UNVERIFIED]', 0),
        (r'PIP issued.*?after', 'Performance concerns raised after', 0),
        
        # Settlement/legal documents
        (r'March 20, 2024: Sudden "performance concerns".*?\n', 
         'March 2024: Alleged performance concerns raised [NO DOCUMENTATION FOUND]\n', 0),
        (r'December 2024: Placed on Performance Improvement Plan.*?\n',
         'December 2024: Alleged performance issues [UNVERIFIED]\n', 0),
        
        # General PIP references
        (r'\bPIP\b(?!\s*cleanup)', '[UNVERIFIED CLAIM]', 0),
        (r'Performance Improvement Plan', '[UNVERIFIED Performance Action]', 0),
        
        # Specific dates with PIP
        (r'March 20, 2024.*?PIP.*?\n', 'March 2024: [FABRICATED EVENT REMOVED]\n', re.IGNORECASE),
    ]
    
    for pattern, replacement, flags in replacements:
        if flags:
            new_content, count = re.subn(pattern, replacement, content, flags=flags)
        else:
            new_content, count = re.subn(pattern, replacement, content)
        
        if count > 0:
            content = new_content
            changes.append(f"Replaced {count} instances of pattern: {pattern[:50]}...")
    
    # Clean up JSON arrays that might have trailing commas
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Add warning header to certain file types
    if filename.endswith('.md') and 'SETTLEMENT' in filename:
        if '**DATA VERIFICATION WARNING**' not in content:
            warning = """**DATA VERIFICATION WARNING**: This document contains references to events that may be unverified or reconstructed. All dates, events, and claims must be verified against original documentation before use in legal proceedings.\n\n---\n\n"""
            content = warning + content
            changes.append("Added verification warning header")
    
    if content != original:
        changes_made.append({
            'file': filename,
            'changes': changes
        })
    
    return content

def process_directory(directory):
    """Process all files in directory"""
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        if any(skip in root for skip in ['.git', 'node_modules', '.backup', 'duplicates_removed']):
            continue
            
        for file in files:
            if file in SKIP_FILES:
                continue
                
            # Process text-based files
            if file.endswith(('.py', '.md', '.html', '.json', '.csv', '.txt')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    cleaned = clean_pip_references(content, file)
                    
                    if cleaned != content:
                        # Backup original
                        backup_path = filepath + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        # Write cleaned version
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(cleaned)
                        
                        print(f"✓ Cleaned: {filepath}")
                    
                except Exception as e:
                    print(f"✗ Error processing {filepath}: {e}")

def create_cleanup_report():
    """Create a report of all changes made"""
    report = f"""# PIP Reference Cleanup Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
Total files modified: {len(changes_made)}

## Critical Notice
The March 20, 2024 Performance Improvement Plan (PIP) reference has been identified as FABRICATED. 
No documentation exists for this event. All references have been removed or marked as unverified.

## Changes Made by File

"""
    
    for change in changes_made:
        report += f"\n### {change['file']}\n"
        for c in change['changes']:
            report += f"- {c}\n"
    
    report += """
## Recommendations

1. **Verify all remaining events** against source documents
2. **Do not use any [UNVERIFIED] items** in legal proceedings
3. **Consult with attorney** before using this information
4. **Cross-reference all dates** with original EEO documents

## Files Requiring Manual Review

The following types of content still need verification:
- Email counts (many are estimates)
- Generic names (John Smith, Sarah Johnson, etc.)
- Damage calculations
- Timeline events without source citations
"""
    
    with open('PIP_CLEANUP_REPORT.md', 'w') as f:
        f.write(report)
    
    print(f"\n✓ Cleanup report created: PIP_CLEANUP_REPORT.md")

def main():
    print("Starting comprehensive PIP reference cleanup...")
    print("=" * 60)
    
    # Process current directory
    process_directory('.')
    
    # Create report
    create_cleanup_report()
    
    print(f"\n✓ Cleanup complete! Modified {len(changes_made)} files")
    print("⚠️  Please review PIP_CLEANUP_REPORT.md for details")

if __name__ == "__main__":
    main() 