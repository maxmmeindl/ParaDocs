#!/usr/bin/env python3
"""
Extract all dates from existing CSV and JSON files to create a comprehensive date index.
This will serve as the authoritative source for validating dashboard dates.
"""

import csv
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Date patterns to match
date_patterns = [
    (r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),  # ISO format: 2024-01-08
    (r'[A-Z][a-z]{2} \d{1,2}, \d{4}', '%b %d, %Y'),  # Month DD, YYYY: Jan 8, 2024
    (r'\d{1,2}/\d{1,2}/\d{4}', '%m/%d/%Y'),  # MM/DD/YYYY: 01/08/2024
    (r'\d{1,2}-\d{1,2}-\d{4}', '%m-%d-%Y'),  # MM-DD-YYYY: 01-08-2024
]

def normalize_date(date_str):
    """Convert various date formats to ISO format YYYY-MM-DD"""
    for pattern, date_format in date_patterns:
        if re.match(pattern, date_str):
            try:
                # Handle special cases
                if date_format == '%b %d, %Y':
                    # Replace short month names with full names for parsing
                    date_str = date_str.replace('Jan', 'January').replace('Feb', 'February')\
                              .replace('Mar', 'March').replace('Apr', 'April')\
                              .replace('Jun', 'June').replace('Jul', 'July')\
                              .replace('Aug', 'August').replace('Sep', 'September')\
                              .replace('Oct', 'October').replace('Nov', 'November')\
                              .replace('Dec', 'December')
                    date_format = '%B %d, %Y'
                
                dt = datetime.strptime(date_str.strip(), date_format)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    return None

def extract_dates_from_csv(file_path):
    """Extract dates from CSV files"""
    dates = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, 2):  # Start at 2 to account for header
                for col_name, value in row.items():
                    if value and isinstance(value, str):
                        # Check if column name suggests date
                        if any(word in col_name.lower() for word in ['date', 'time', 'when']):
                            normalized = normalize_date(value)
                            if normalized:
                                dates[normalized].append({
                                    'file': str(file_path),
                                    'source': f'row {row_num}, column "{col_name}"',
                                    'original': value
                                })
                        
                        # Also search for dates in any text field
                        for pattern, _ in date_patterns:
                            for match in re.finditer(pattern, value):
                                date_str = match.group(0)
                                normalized = normalize_date(date_str)
                                if normalized:
                                    dates[normalized].append({
                                        'file': str(file_path),
                                        'source': f'row {row_num}, column "{col_name}"',
                                        'original': date_str
                                    })
    except Exception as e:
        print(f"Error reading CSV {file_path}: {e}")
    
    return dates

def extract_dates_from_json(file_path):
    """Extract dates from JSON files"""
    dates = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            
        def traverse_json(obj, path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if isinstance(value, str):
                        # Check if key suggests date
                        if any(word in key.lower() for word in ['date', 'time', 'when', 'created', 'modified']):
                            normalized = normalize_date(value)
                            if normalized:
                                dates[normalized].append({
                                    'file': str(file_path),
                                    'source': new_path,
                                    'original': value
                                })
                        
                        # Search for dates in any string
                        for pattern, _ in date_patterns:
                            for match in re.finditer(pattern, value):
                                date_str = match.group(0)
                                normalized = normalize_date(date_str)
                                if normalized:
                                    dates[normalized].append({
                                        'file': str(file_path),
                                        'source': new_path,
                                        'original': date_str
                                    })
                    else:
                        traverse_json(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    traverse_json(item, f"{path}[{i}]")
        
        traverse_json(data)
        
    except Exception as e:
        print(f"Error reading JSON {file_path}: {e}")
    
    return dates

def main():
    """Main function to extract dates and create index"""
    all_dates = defaultdict(list)
    
    # Find all CSV and JSON files
    csv_files = list(Path('.').glob('*.csv'))
    json_files = list(Path('.').glob('*.json'))
    
    print(f"Found {len(csv_files)} CSV files and {len(json_files)} JSON files")
    
    # Process CSV files
    for csv_file in csv_files:
        if 'venv' not in str(csv_file):
            print(f"Processing CSV: {csv_file}")
            dates = extract_dates_from_csv(csv_file)
            for date, sources in dates.items():
                all_dates[date].extend(sources)
    
    # Process JSON files
    for json_file in json_files:
        if 'venv' not in str(json_file) and 'date_index' not in str(json_file):
            print(f"Processing JSON: {json_file}")
            dates = extract_dates_from_json(json_file)
            for date, sources in dates.items():
                all_dates[date].extend(sources)
    
    # Create the date index
    date_list = []
    for date, sources in sorted(all_dates.items()):
        # Deduplicate sources
        unique_sources = []
        seen = set()
        for source in sources:
            key = (source['file'], source['source'])
            if key not in seen:
                seen.add(key)
                unique_sources.append(source)
        
        date_list.append({
            'date': date,
            'files': unique_sources
        })
    
    # Save the index
    output_path = Path('search_index/date_index.json')
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(date_list, f, indent=2)
    
    print(f"\nDate index created with {len(date_list)} unique dates")
    print(f"Saved to: {output_path}")
    
    # Create summary report
    report = [
        "# Date Extraction Summary",
        "",
        f"Total unique dates found: {len(date_list)}",
        f"Date range: {date_list[0]['date']} to {date_list[-1]['date']}" if date_list else "No dates found",
        "",
        "## Top 10 Most Referenced Dates:",
        ""
    ]
    
    # Sort by number of references
    sorted_by_refs = sorted(date_list, key=lambda x: len(x['files']), reverse=True)[:10]
    
    for entry in sorted_by_refs:
        date = entry['date']
        count = len(entry['files'])
        report.append(f"- **{date}**: {count} references")
        # Show first 3 sources
        for source in entry['files'][:3]:
            report.append(f"  - {Path(source['file']).name}: {source['source']}")
        if count > 3:
            report.append(f"  - ... and {count - 3} more")
        report.append("")
    
    report_path = Path('date_extraction_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"Summary report saved to: {report_path}")

if __name__ == '__main__':
    main() 