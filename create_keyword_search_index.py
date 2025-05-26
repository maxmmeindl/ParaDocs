import os
import json
import re
from datetime import datetime
from collections import defaultdict

print("Building Keyword Search Index...")

# Create output directory
os.makedirs("search_index", exist_ok=True)

# Critical terms to track
critical_terms = [
    "1340 days", "1340-day", "RAR0023278", "RAR0023261", "RAR0042452",
    "45 days", "45-day", "termination", "FOIA", "no responsive records",
    "reasonable accommodation", "interactive process", "retaliation",
    "Hurricane Beryl", "welfare check", "disability", "discrimination",
    "age 74", "January 6, 2025", "December 20, 2024"
]

# Initialize search data
search_index = {
    "keywords": {},
    "critical_terms": defaultdict(list),
    "documents": {},
    "metadata": {
        "created": datetime.now().isoformat(),
        "total_documents": 0,
        "critical_terms_found": 0
    }
}

# Scan all text files
text_extensions = ['.txt', '.md', '.csv', '.json', '.html', '.xml']
file_count = 0

print("Scanning documents...")
for root, dirs, files in os.walk('.'):
    # Skip certain directories
    if 'node_modules' in root or 'venv' in root:
        continue
    
    for file in files:
        if any(file.endswith(ext) for ext in text_extensions):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    file_count += 1
                    
                    # Store document info
                    search_index["documents"][file] = {
                        "path": filepath,
                        "size": os.path.getsize(filepath)
                    }
                    
                    # Check for critical terms
                    for term in critical_terms:
                        if term.lower() in content.lower():
                            search_index["critical_terms"][term].append(file)
                    
                    print(f"  ✓ Indexed: {file}")
                    
            except Exception as e:
                print(f"  ⚠ Skipped {file}: {str(e)}")

# Update metadata
search_index["metadata"]["total_documents"] = file_count
search_index["metadata"]["critical_terms_found"] = len(search_index["critical_terms"])

# Save JSON index
with open("search_index/search_index.json", "w") as f:
    json.dump(search_index, f, indent=2, default=str)

# Create HTML search interface
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>ParaDocs Keyword Search</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; }}
        .search-box {{ 
            width: 100%; 
            padding: 15px; 
            font-size: 18px; 
            border: 2px solid #3498db;
            border-radius: 5px;
            margin-bottom: 20px;
            box-sizing: border-box;
        }}
        .critical-terms {{
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .term-box {{
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 3px;
            cursor: pointer;
        }}
        .term-box:hover {{
            background: #c0392b;
        }}
        .results {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-height: 600px;
            overflow-y: auto;
        }}
        .file-item {{
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        .highlight {{
            background: yellow;
            font-weight: bold;
        }}
        .stats {{
            background: #3498db;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 ParaDocs Keyword Search</h1>
        
        <div class="stats">
            <strong>Documents Indexed:</strong> {file_count} | 
            <strong>Critical Terms Found:</strong> {len(search_index["critical_terms"])}
        </div>
        
        <input type="text" class="search-box" id="searchBox" 
               placeholder="Search for keywords (e.g., 1340 days, accommodation, termination)..." 
               onkeyup="performSearch()" />
        
        <div class="critical-terms">
            <h3>🚨 Critical Terms Found:</h3>
"""

# Add critical terms
for term, files in search_index["critical_terms"].items():
    if files:
        count = len(set(files))
        html_content += f'            <span class="term-box" onclick="searchTerm(\'{term}\')">{term} ({count})</span>\n'

html_content += """        </div>
        
        <div class="results" id="results">
            <p>Type a keyword above or click a critical term to search...</p>
        </div>
    </div>
    
    <script>
        const searchData = """ + json.dumps(search_index, default=str) + """;
        
        function searchTerm(term) {
            document.getElementById('searchBox').value = term;
            performSearch();
        }
        
        function performSearch() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            let html = '';
            
            if (searchTerm.length < 2) {
                html = '<p>Type at least 2 characters to search...</p>';
            } else {
                html = '<h3>Search Results for: <span class="highlight">' + searchTerm + '</span></h3>';
                
                // Check critical terms
                let foundCritical = false;
                for (const [term, files] of Object.entries(searchData.critical_terms)) {
                    if (term.toLowerCase().includes(searchTerm)) {
                        foundCritical = true;
                        const uniqueFiles = [...new Set(files)];
                        html += '<h4>🚨 Critical Term "' + term + '" found in ' + uniqueFiles.length + ' files:</h4><ul>';
                        uniqueFiles.forEach(file => {
                            html += '<li class="file-item">' + file + '</li>';
                        });
                        html += '</ul>';
                    }
                }
                
                // Search in filenames
                html += '<h4>📄 Files containing "' + searchTerm + '" in filename:</h4><ul>';
                let foundFiles = false;
                for (const [filename, info] of Object.entries(searchData.documents)) {
                    if (filename.toLowerCase().includes(searchTerm)) {
                        foundFiles = true;
                        html += '<li class="file-item">' + filename + ' (' + 
                                Math.round(info.size/1024) + 'KB)</li>';
                    }
                }
                
                if (!foundFiles) {
                    html += '<li>No files found with this term in the filename</li>';
                }
                html += '</ul>';
            }
            
            document.getElementById('results').innerHTML = html;
        }
    </script>
</body>
</html>"""

# Save HTML
with open("search_index/keyword_search.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Create critical terms report
report = f"""# CRITICAL TERMS SEARCH REPORT

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Documents Indexed: {file_count}

## Critical Terms Found:

"""

for term in sorted(search_index["critical_terms"].keys()):
    files = list(set(search_index["critical_terms"][term]))
    if files:
        report += f"\n### {term} (Found in {len(files)} files)\n"
        for file in sorted(files):
            report += f"- {file}\n"

with open("search_index/CRITICAL_TERMS_REPORT.md", "w", encoding="utf-8") as f:
    f.write(report)

# Create CSV for quick reference
csv_content = "Term,File_Count,Found_In\n"
for term in sorted(search_index["critical_terms"].keys()):
    files = list(set(search_index["critical_terms"][term]))
    if files:
        csv_content += f'"{term}",{len(files)},"{"; ".join(files)}"\n'

with open("search_index/critical_terms.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

print(f"\n✅ Keyword Search Index Complete!")
print(f"\nOutputs created:")
print(f"1. search_index/keyword_search.html - Open this in your browser")
print(f"2. search_index/CRITICAL_TERMS_REPORT.md - Summary of critical findings")
print(f"3. search_index/critical_terms.csv - Quick reference spreadsheet")
print(f"4. search_index/search_index.json - Full search index data")

print(f"\nSummary:")
print(f"- Documents indexed: {file_count}")
print(f"- Critical terms found: {len([t for t in search_index['critical_terms'] if search_index['critical_terms'][t]])}")

print(f"\nTop findings:")
sorted_terms = sorted([(term, len(set(files))) for term, files in search_index["critical_terms"].items() if files], 
                     key=lambda x: x[1], reverse=True)
for term, count in sorted_terms[:5]:
    print(f"  {term}: Found in {count} files") 