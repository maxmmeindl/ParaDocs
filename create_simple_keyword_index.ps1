# Simple Keyword Search Index Builder
# Works with existing ParaDocs structure

Write-Host "Building Keyword Search Index..." -ForegroundColor Green

# Create output directory if needed
New-Item -ItemType Directory -Path "search_index" -Force | Out-Null

# Initialize search data
$searchIndex = @{
    keywords = @{}
    criticalTerms = @{}
    documents = @{}
}

# Critical terms to track
$criticalTerms = @(
    "1340 days", "1340-day", "RAR0023278", "RAR0023261", "RAR0042452",
    "45 days", "45-day", "termination", "FOIA", "no responsive records",
    "reasonable accommodation", "interactive process", "retaliation"
)

Write-Host "Scanning documents..." -ForegroundColor Yellow

# Get all text files
$textFiles = Get-ChildItem -Recurse -File -Include "*.txt","*.md","*.csv","*.json","*.html" |
    Where-Object { $_.DirectoryName -notmatch "node_modules|venv" }

$fileCount = 0
foreach ($file in $textFiles) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction Stop
        $fileCount++
        
        # Track document
        $searchIndex.documents[$file.Name] = @{
            path = $file.FullName
            size = $file.Length
        }
        
        # Check for critical terms
        foreach ($term in $criticalTerms) {
            if ($content -match [regex]::Escape($term)) {
                if (-not $searchIndex.criticalTerms.ContainsKey($term)) {
                    $searchIndex.criticalTerms[$term] = @()
                }
                $searchIndex.criticalTerms[$term] += $file.Name
            }
        }
        
        Write-Host "  ✓ Indexed: $($file.Name)" -ForegroundColor Gray
    }
    catch {
        Write-Host "  ⚠ Skipped: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "`nCreating search interface..." -ForegroundColor Yellow

# Create search HTML
$searchHtml = @"
<!DOCTYPE html>
<html>
<head>
    <title>ParaDocs Keyword Search</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; }
        .search-box { 
            width: 100%; 
            padding: 15px; 
            font-size: 18px; 
            border: 2px solid #3498db;
            border-radius: 5px;
            margin-bottom: 20px;
            box-sizing: border-box;
        }
        .critical-terms {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .term-box {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 3px;
            cursor: pointer;
        }
        .term-box:hover {
            background: #c0392b;
        }
        .results {
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .file-item {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .highlight {
            background: yellow;
            font-weight: bold;
        }
        .stats {
            background: #3498db;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 ParaDocs Keyword Search</h1>
        
        <div class="stats">
            <strong>Documents Indexed:</strong> $fileCount | 
            <strong>Critical Terms Found:</strong> $($searchIndex.criticalTerms.Count)
        </div>
        
        <input type="text" class="search-box" id="searchBox" 
               placeholder="Search for keywords (e.g., 1340 days, accommodation, termination)..." 
               onkeyup="performSearch()" />
        
        <div class="critical-terms">
            <h3>🚨 Critical Terms Found:</h3>
"@

# Add critical terms
foreach ($term in $searchIndex.criticalTerms.Keys) {
    $count = $searchIndex.criticalTerms[$term].Count
    $searchHtml += "            <span class='term-box' onclick='searchTerm(`"$term`")'>$term ($count)</span>`n"
}

$searchHtml += @"
        </div>
        
        <div class="results" id="results">
            <p>Type a keyword above or click a critical term to search...</p>
        </div>
    </div>
    
    <script>
        const criticalTerms = $(ConvertTo-Json $searchIndex.criticalTerms -Compress);
        const documents = $(ConvertTo-Json $searchIndex.documents -Compress);
        
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
                for (const [term, files] of Object.entries(criticalTerms)) {
                    if (term.toLowerCase().includes(searchTerm)) {
                        foundCritical = true;
                        html += '<h4>🚨 Critical Term "' + term + '" found in:</h4><ul>';
                        files.forEach(file => {
                            html += '<li class="file-item">' + file + '</li>';
                        });
                        html += '</ul>';
                    }
                }
                
                // Search in filenames
                html += '<h4>📄 Files containing "' + searchTerm + '":</h4><ul>';
                let foundFiles = false;
                for (const [filename, info] of Object.entries(documents)) {
                    if (filename.toLowerCase().includes(searchTerm)) {
                        foundFiles = true;
                        html += '<li class="file-item">' + filename + ' (' + 
                                Math.round(info.size/1024) + 'KB)</li>';
                    }
                }
                
                if (!foundFiles) {
                    html = '<p>No files found with this term in the filename</p>';
                }
                html += '</ul>';
                
                if (!foundCritical && !foundFiles) {
                    html = '<p>No results found for "' + searchTerm + '"</p>';
                }
            }
            
            document.getElementById('results').innerHTML = html;
        }
    </script>
</body>
</html>
"@

$searchHtml | Out-File "search_index/keyword_search.html" -Encoding UTF8

# Create critical terms report
$criticalReport = @"
# CRITICAL TERMS SEARCH REPORT

Generated: $(Get-Date)
Documents Indexed: $fileCount

## Critical Terms Found:

"@

foreach ($term in $searchIndex.criticalTerms.Keys | Sort-Object) {
    $files = $searchIndex.criticalTerms[$term] | Select-Object -Unique
    $criticalReport += "`n### $term (Found in $($files.Count) files)`n"
    $files | ForEach-Object {
        $criticalReport += "- $_`n"
    }
}

$criticalReport | Out-File "search_index/CRITICAL_TERMS_REPORT.md" -Encoding UTF8

# Create CSV for quick reference
$csvContent = "Term,File_Count,Found_In`n"
foreach ($term in $searchIndex.criticalTerms.Keys | Sort-Object) {
    $files = $searchIndex.criticalTerms[$term] | Select-Object -Unique
    $csvContent += "`"$term`",$($files.Count),`"$($files -join '; ')`"`n"
}
$csvContent | Out-File "search_index/critical_terms.csv" -Encoding UTF8

Write-Host "`n✅ Keyword Search Index Complete!" -ForegroundColor Green
Write-Host "`nOutputs created:" -ForegroundColor Cyan
Write-Host "1. search_index/keyword_search.html - Open this in your browser"
Write-Host "2. search_index/CRITICAL_TERMS_REPORT.md - Summary of critical findings"
Write-Host "3. search_index/critical_terms.csv - Quick reference spreadsheet"

Write-Host "`nSummary:" -ForegroundColor Yellow
Write-Host "- Documents indexed: $fileCount"
Write-Host "- Critical terms found: $($searchIndex.criticalTerms.Count)"

Write-Host "`nTop findings:" -ForegroundColor Magenta
$searchIndex.criticalTerms.GetEnumerator() | 
    Sort-Object { $_.Value.Count } -Descending |
    Select-Object -First 5 |
    ForEach-Object {
        Write-Host "  $($_.Key): Found in $($_.Value.Count) files"
    } 