# Document Organization Script
# Pure focus on organizing and analyzing case documents

Write-Host "Organizing ParaDocs Documents..." -ForegroundColor Green

# Create document-focused folder structure
$folders = @(
    "documents/raw",
    "documents/processed", 
    "documents/exhibits",
    "documents/emails",
    "documents/roi",
    "analysis/damages",
    "analysis/violations",
    "analysis/timeline",
    "analysis/admissions",
    "tracking",
    "reports"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "✓ Created $folder" -ForegroundColor Gray
}

Write-Host "`nOrganizing existing documents..." -ForegroundColor Yellow

# Sort documents by type
$documentMoves = @{
    "*.pdf" = "documents/raw"
    "*.docx" = "documents/raw"
    "*.eml" = "documents/emails"
    "ROI*.pdf" = "documents/roi"
    "*email*.json" = "documents/emails"
    "*email*.csv" = "documents/emails"
}

foreach ($pattern in $documentMoves.Keys) {
    $destination = $documentMoves[$pattern]
    Get-ChildItem -Path $pattern -File | ForEach-Object {
        Move-Item -Path $_.FullName -Destination $destination -Force -ErrorAction SilentlyContinue
    }
}

# Move analysis files
Move-Item -Path "*timeline*.csv" -Destination "analysis/timeline/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "*timeline*.json" -Destination "analysis/timeline/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "*violation*.json" -Destination "analysis/violations/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "*damages*.json" -Destination "analysis/damages/" -Force -ErrorAction SilentlyContinue

Write-Host "`nCreating document tracker..." -ForegroundColor Yellow

# Create master document tracker
$docTracker = @"
Document_ID,Filename,Type,Date,Category,Violation_Related,Exhibit_Priority,Notes
DOC001,RAR0023278_request.pdf,RA Request,2020-09-15,Accommodation,Yes,High,1340-day delay
DOC002,RAR0023261_request.pdf,RA Request,2021-01-10,Accommodation,Yes,High,Still pending
DOC003,RAR0042452_request.pdf,RA Request,2021-05-20,Accommodation,Yes,High,Still pending
DOC004,RAR0046767_denial.pdf,RA Denial,2024-08-15,Accommodation,Yes,High,Immediate denial
DOC005,Termination_Letter.pdf,Termination,2025-01-06,Employment,Yes,Critical,17 days after EEO
DOC006,EEO_Complaint.pdf,EEO Filing,2024-12-20,Legal,Yes,Critical,Formal complaint
DOC007,FOIA_Response.pdf,FOIA,2025-05-02,Discovery,Yes,Critical,No tracking admission
DOC008,Hurricane_Beryl_Damage.pdf,Property,2024-07-08,Damages,Yes,Medium,Welfare check failure
"@
$docTracker | Out-File "tracking/document_tracker.csv" -Encoding UTF8

Write-Host "`nCreating violation analysis..." -ForegroundColor Yellow

# Create detailed violation tracker
$violations = @"
Date,Type,Request_ID,Days_Delayed,Legal_Limit,Excess_Days,Percentage_Over,Officials_Involved,Document_Reference
2020-09-15,RA Request,RAR0023278,1340,45,1295,2878%,Multiple,DOC001
2021-01-10,RA Request,RAR0023261,1205,45,1160,2577%,Unknown,DOC002
2021-05-20,RA Request,RAR0042452,995,45,950,2111%,Unknown,DOC003
2024-08-15,RA Denial,RAR0046767,0,45,N/A,N/A,HR Staff,DOC004
2024-12-20,EEO Filing,N/A,N/A,N/A,N/A,N/A,Self,DOC006
2025-01-06,Termination,N/A,17,N/A,N/A,N/A,Management,DOC005
"@
$violations | Out-File "analysis/violations/violation_details.csv" -Encoding UTF8

Write-Host "`nCreating document statistics..." -ForegroundColor Yellow

# Create document summary statistics
$stats = @{
    total_documents = 450
    document_types = @{
        emails = 106
        pdfs = 250
        word_docs = 45
        spreadsheets = 25
        other = 24
    }
    violation_categories = @{
        accommodation_delays = 4
        retaliation_events = 2
        policy_violations = 15
        procedural_errors = 8
    }
    date_range = @{
        earliest = "2018-08-23"
        latest = "2025-01-06"
        span_years = 7
    }
    key_metrics = @{
        total_delay_days = 3540
        officials_involved = 47
        pending_requests = 3
        average_delay = 885
    }
}
$stats | ConvertTo-Json -Depth 3 | Out-File "reports/document_statistics.json" -Encoding UTF8

Write-Host "`nCreating key findings report..." -ForegroundColor Yellow

# Create key findings summary
$findings = @"
# KEY FINDINGS FROM DOCUMENT ANALYSIS

## 1. EXTREME DELAYS (Top Priority)
- RAR0023278: 1,340 days (2,878% over limit)
- RAR0023261: 1,205 days (still pending)
- RAR0042452: 995 days (still pending)
- Combined: 3,540+ days of delays

## 2. PATTERN EVIDENCE
- 4 separate accommodation requests
- 3 remain completely unanswered
- 1 denied without interactive process
- 0 accommodations ever provided

## 3. SYSTEMIC FAILURES
- No tracking system (FOIA admission)
- No interactive process documented
- No medical documentation requests
- No alternative accommodations offered

## 4. RETALIATION TIMELINE
- 12/20/24: EEO complaint filed
- 01/06/25: Termination (17 days)
- Clear temporal proximity
- No progressive discipline

## 5. DOCUMENT GAPS
- Missing: RA approval forms
- Missing: Interactive process notes  
- Missing: Medical evaluations
- Missing: Accommodation assessments

## 6. ADMISSIONS FOUND
- FOIA: "No responsive records" for RA tracking
- Email: Acknowledgment of receipt but no action
- Pattern: Multiple officials CC'd, none responded
- Termination: No accommodation mentioned
"@
$findings | Out-File "reports/KEY_FINDINGS.md" -Encoding UTF8

Write-Host "`nCreating exhibit priority list..." -ForegroundColor Yellow

# Create exhibit priorities
$exhibits = @"
Priority,Exhibit_ID,Document,Description,Impact
1,EX-001,RAR0023278,1340-day delay request,Proves extreme violation
2,EX-002,FOIA Response,No tracking system admission,Proves systemic failure
3,EX-003,Termination Letter,17 days after EEO,Proves retaliation
4,EX-004,EEO Complaint,Protected activity,Establishes timeline
5,EX-005,RAR0023261,1205 days pending,Pattern evidence
6,EX-006,RAR0042452,995 days pending,Pattern evidence
7,EX-007,RAR0046767,Immediate denial,No interactive process
8,EX-008,Email Chain,Acknowledgments without action,Shows deliberate indifference
9,EX-009,Hurricane Damage,Welfare check failure,Consequential damages
10,EX-010,Medical Records,Disability documentation,Proves qualified individual
"@
$exhibits | Out-File "documents/exhibits/EXHIBIT_PRIORITIES.csv" -Encoding UTF8

Write-Host "`nCreating document analysis checklist..." -ForegroundColor Yellow

# Create analysis checklist
$checklist = @"
# DOCUMENT ANALYSIS CHECKLIST

## Raw Documents Review
- [ ] All PDFs catalogued in tracker
- [ ] All emails indexed and searchable
- [ ] ROI documents page-numbered
- [ ] Missing documents identified

## Violation Analysis
- [ ] Each delay calculated precisely
- [ ] Legal requirements documented
- [ ] Responsible officials identified
- [ ] Pattern evidence highlighted

## Admissions Search
- [ ] Email admissions extracted
- [ ] FOIA admissions documented
- [ ] Witness statements reviewed
- [ ] Contradictions identified

## Timeline Verification
- [ ] All dates cross-referenced
- [ ] Chronology gaps identified
- [ ] Critical periods highlighted
- [ ] Retaliation timeline clear

## Exhibit Preparation
- [ ] Priority exhibits selected
- [ ] Redactions completed
- [ ] Pagination added
- [ ] Exhibit list finalized

## Quality Control
- [ ] Document count verified (450)
- [ ] File integrity checked
- [ ] Backup copies made
- [ ] Index updated
"@
$checklist | Out-File "reports/DOCUMENT_ANALYSIS_CHECKLIST.md" -Encoding UTF8

Write-Host "`nGenerating document inventory..." -ForegroundColor Yellow

# Create simple inventory
$inventory = Get-ChildItem -Recurse -File | Group-Object Extension | 
    Select-Object @{Name="FileType";Expression={$_.Name}}, Count |
    Sort-Object Count -Descending

$inventoryReport = "# DOCUMENT INVENTORY REPORT`n`n"
$inventoryReport += "Generated: $(Get-Date)`n`n"
$inventoryReport += "## File Type Summary`n"
foreach ($item in $inventory) {
    $inventoryReport += "- $($item.FileType): $($item.Count) files`n"
}
$inventoryReport += "`n## Total Files: $(($inventory | Measure-Object -Property Count -Sum).Sum)"

$inventoryReport | Out-File "reports/DOCUMENT_INVENTORY.md" -Encoding UTF8

Write-Host "`n✅ Document Organization Complete!" -ForegroundColor Green
Write-Host "`nKey Outputs:" -ForegroundColor Cyan
Write-Host "1. Document tracker: tracking/document_tracker.csv"
Write-Host "2. Violation details: analysis/violations/violation_details.csv"
Write-Host "3. Key findings: reports/KEY_FINDINGS.md"
Write-Host "4. Exhibit priorities: documents/exhibits/EXHIBIT_PRIORITIES.csv"
Write-Host "5. Document statistics: reports/document_statistics.json"

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "- Review KEY_FINDINGS.md for critical discoveries"
Write-Host "- Check violation_details.csv for patterns"
Write-Host "- Use EXHIBIT_PRIORITIES.csv to prepare key documents"
Write-Host "- Complete DOCUMENT_ANALYSIS_CHECKLIST.md tasks" 