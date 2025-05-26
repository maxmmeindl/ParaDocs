# Keyword Search Index Builder
# Creates comprehensive searchable index of all document content

Write-Host "Building Keyword Search Index..." -ForegroundColor Green

# Initialize index structure
$keywordIndex = @{}
$documentIndex = @{}
$phraseIndex = @{}
$violationTerms = @{}

# Define critical search terms to track
$criticalTerms = @(
    "reasonable accommodation",
    "interactive process",
    "1340 days",
    "1340-day",
    "RAR0023278",
    "RAR0023261", 
    "RAR0042452",
    "RAR0046767",
    "45 days",
    "45-day",
    "disability",
    "discrimination",
    "retaliation",
    "termination",
    "FOIA",
    "no responsive records",
    "tracking system",
    "Hurricane Beryl",
    "welfare check",
    "EEO complaint",
    "age 74",
    "veteran"
)

# Legal terms to index
$legalTerms = @(
    "29 CFR 1630",
    "Rehabilitation Act",
    "Section 504",
    "Section 501", 
    "ADA",
    "ADEA",
    "Title VII",
    "42 USC",
    "29 USC 794",
    "undue hardship",
    "essential functions",
    "qualified individual",
    "adverse action",
    "temporal proximity",
    "pattern or practice",
    "systemic",
    "deliberate indifference",
    "failure to accommodate",
    "hostile work environment"
)

Write-Host "Indexing text files..." -ForegroundColor Yellow

# Function to extract keywords from text
function Extract-Keywords {
    param($text, $filename)
    
    # Convert to lowercase for indexing
    $lowerText = $text.ToLower()
    
    # Extract words (3+ characters)
    $words = [regex]::Matches($lowerText, '\b[a-z0-9]{3,}\b') | ForEach-Object { $_.Value }
    
    # Index each word
    foreach ($word in $words) {
        if (-not $keywordIndex.ContainsKey($word)) {
            $keywordIndex[$word] = @()
        }
        $keywordIndex[$word] += @{
            file = $filename
            count = 1
        }
    }
    
    # Check for critical terms
    foreach ($term in $criticalTerms) {
        if ($lowerText -match [regex]::Escape($term.ToLower())) {
            if (-not $violationTerms.ContainsKey($term)) {
                $violationTerms[$term] = @()
            }
            $violationTerms[$term] += $filename
        }
    }
    
    # Check for legal terms
    foreach ($term in $legalTerms) {
        if ($text -match [regex]::Escape($term)) {
            if (-not $phraseIndex.ContainsKey($term)) {
                $phraseIndex[$term] = @()
            }
            $phraseIndex[$term] += $filename
        }
    }
}

# Index all text-based files
$textExtensions = @(".txt", ".md", ".csv", ".json", ".html", ".xml")
$textFiles = Get-ChildItem -Recurse -File | Where-Object { $_.Extension -in $textExtensions }

foreach ($file in $textFiles) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction Stop
        Extract-Keywords -text $content -filename $file.Name
        
        # Store document metadata
        $documentIndex[$file.Name] = @{
            path = $file.FullName
            size = $file.Length
            modified = $file.LastWriteTime
            wordCount = ($content -split '\s+').Count
        }
    }
    catch {
        Write-Host "  ⚠ Could not index: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Creating searchable index files..." -ForegroundColor Yellow

# Create keyword frequency report
$keywordFreq = @{}
foreach ($word in $keywordIndex.Keys) {
    $keywordFreq[$word] = $keywordIndex[$word].Count
}

# Sort by frequency
$topKeywords = $keywordFreq.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 100

# Create main search index JSON
$searchIndex = @{
    metadata = @{
        created = Get-Date
        totalDocuments = $documentIndex.Count
        totalKeywords = $keywordIndex.Count
        criticalTermsFound = $violationTerms.Count
        legalTermsFound = $phraseIndex.Count
    }
    criticalTerms = $violationTerms
    legalReferences = $phraseIndex
    topKeywords = $topKeywords | ForEach-Object { @{keyword = $_.Key; frequency = $_.Value} }
    documents = $documentIndex
}

$searchIndex | ConvertTo-Json -Depth 4 | Out-File "tracking/keyword_search_index.json" -Encoding UTF8

# Create critical terms report
$criticalReport = @"
# CRITICAL TERMS SEARCH REPORT

Generated: $(Get-Date)

## Accommodation Delays Found In:
"@

foreach ($term in @("1340 days", "1340-day", "RAR0023278", "RAR0023261", "RAR0042452")) {
    if ($violationTerms.ContainsKey($term)) {
        $criticalReport += "`n### $term"
        $violationTerms[$term] | Select-Object -Unique | ForEach-Object {
            $criticalReport += "`n- $_"
        }
    }
}

$criticalReport += @"

## Legal Violations Referenced In:
"@

foreach ($term in @("29 CFR 1630", "Rehabilitation Act", "failure to accommodate")) {
    if ($phraseIndex.ContainsKey($term)) {
        $criticalReport += "`n### $term"
        $phraseIndex[$term] | Select-Object -Unique | ForEach-Object {
            $criticalReport += "`n- $_"
        }
    }
}

$criticalReport | Out-File "reports/CRITICAL_TERMS_REPORT.md" -Encoding UTF8

# Create quick search lookup CSV
$searchLookup = @"
Search_Term,Found_In_Files,Category,Priority
"1340 days","$(($violationTerms['1340 days'] | Select-Object -Unique) -join '; ')","Primary Violation","Critical"
"RAR0023278","$(($violationTerms['RAR0023278'] | Select-Object -Unique) -join '; ')","Accommodation Request","Critical"
"termination","$(($violationTerms['termination'] | Select-Object -Unique) -join '; ')","Retaliation","High"
"no responsive records","$(($violationTerms['no responsive records'] | Select-Object -Unique) -join '; ')","FOIA Admission","Critical"
"45 days","$(($violationTerms['45 days'] | Select-Object -Unique) -join '; ')","Legal Standard","High"
"@

$searchLookup | Out-File "tracking/quick_search_lookup.csv" -Encoding UTF8

# Create keyword cloud data
$cloudData = $topKeywords | Select-Object -First 50 | ForEach-Object {
    @{
        text = $_.Key
        size = [Math]::Min($_.Value * 10, 100)
        color = if ($_.Value -gt 20) { "red" } elseif ($_.Value -gt 10) { "orange" } else { "blue" }
    }
}

$cloudData | ConvertTo-Json | Out-File "reports/keyword_cloud_data.json" -Encoding UTF8

# Create search interface HTML
$searchHtml = @"
<!DOCTYPE html>
<html>
<head>
    <title>ParaDocs Keyword Search</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .search-box { 
            width: 100%; 
            padding: 15px; 
            font-size: 18px; 
            border: 2px solid #3498db;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .results { 
            background: white; 
            padding: 20px; 
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .result-item { 
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .highlight { 
            background: yellow; 
            font-weight: bold; 
        }
        .critical { 
            color: red; 
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
    <h1>ParaDocs Keyword Search Index</h1>
    
    <div class="stats">
        <strong>Index Statistics:</strong>
        Documents: $($documentIndex.Count) | 
        Keywords: $($keywordIndex.Count) | 
        Critical Terms: $($violationTerms.Count) | 
        Legal References: $($phraseIndex.Count)
    </div>
    
    <input type="text" class="search-box" id="searchBox" placeholder="Search for keywords (e.g., '1340 days', 'accommodation', 'RAR0023278')..." />
    
    <div class="results" id="results">
        <h3>Quick Links to Critical Terms:</h3>
        <p>
            <a href="#" onclick="search('1340 days')">1340 days</a> | 
            <a href="#" onclick="search('RAR0023278')">RAR0023278</a> | 
            <a href="#" onclick="search('termination')">termination</a> | 
            <a href="#" onclick="search('FOIA')">FOIA</a> | 
            <a href="#" onclick="search('45 days')">45 days</a>
        </p>
    </div>
    
    <script>
        const searchData = $($searchIndex | ConvertTo-Json -Compress);
        
        function search(term) {
            const searchTerm = term || document.getElementById('searchBox').value.toLowerCase();
            let results = '<h3>Search Results for: <span class="highlight">' + searchTerm + '</span></h3>';
            
            // Check critical terms
            if (searchData.criticalTerms[searchTerm]) {
                results += '<div class="result-item critical">⚠️ CRITICAL TERM FOUND in: ' + 
                    searchData.criticalTerms[searchTerm].join(', ') + '</div>';
            }
            
            // Check legal references
            for (const [key, files] of Object.entries(searchData.legalReferences)) {
                if (key.toLowerCase().includes(searchTerm)) {
                    results += '<div class="result-item">📜 Legal Reference "' + key + 
                        '" found in: ' + files.join(', ') + '</div>';
                }
            }
            
            // Show documents containing the term
            results += '<h4>Documents containing this term:</h4>';
            for (const [doc, info] of Object.entries(searchData.documents)) {
                if (doc.toLowerCase().includes(searchTerm)) {
                    results += '<div class="result-item">📄 ' + doc + 
                        ' (Words: ' + info.wordCount + ')</div>';
                }
            }
            
            document.getElementById('results').innerHTML = results;
            if (term) document.getElementById('searchBox').value = term;
        }
        
        document.getElementById('searchBox').addEventListener('keyup', function(e) {
            if (e.key === 'Enter') search();
        });
    </script>
</body>
</html>
"@

$searchHtml | Out-File "tracking/keyword_search.html" -Encoding UTF8

Write-Host "`n✅ Keyword Search Index Complete!" -ForegroundColor Green
Write-Host "`nKey Outputs Created:" -ForegroundColor Cyan
Write-Host "1. Search Interface: tracking/keyword_search.html (open in browser)"
Write-Host "2. Full Index: tracking/keyword_search_index.json"
Write-Host "3. Quick Lookup: tracking/quick_search_lookup.csv"
Write-Host "4. Critical Terms: reports/CRITICAL_TERMS_REPORT.md"
Write-Host "5. Keyword Cloud: reports/keyword_cloud_data.json"

Write-Host "`nSearch Statistics:" -ForegroundColor Yellow
Write-Host "- Total keywords indexed: $($keywordIndex.Count)"
Write-Host "- Documents indexed: $($documentIndex.Count)"
Write-Host "- Critical violations found: $($violationTerms.Count)"
Write-Host "- Legal references found: $($phraseIndex.Count)"

Write-Host "`nTop 10 Most Frequent Keywords:" -ForegroundColor Magenta
$topKeywords | Select-Object -First 10 | ForEach-Object {
    Write-Host "  $($_.Key): $($_.Value) occurrences"
}

Write-Host "`nTo use the search:" -ForegroundColor Green
Write-Host "1. Open tracking/keyword_search.html in your browser"
Write-Host "2. Type any keyword to search across all documents"
Write-Host "3. Click the quick links for critical terms" 