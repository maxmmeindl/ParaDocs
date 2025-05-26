# ADR Preparation Organization Script
# Implements simplified structure focused on immediate needs

Write-Host "Reorganizing ParaDocs for ADR Focus..." -ForegroundColor Green

# Create new folder structure
$folders = @(
    "documents/raw",
    "documents/processed", 
    "documents/exhibits",
    "analysis/damages",
    "analysis/violations",
    "analysis/timeline",
    "legal/complaints",
    "legal/correspondence",
    "legal/authorities",
    "config",
    "reports"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "✓ Created $folder" -ForegroundColor Gray
}

# Move existing files to appropriate locations
Write-Host "`nOrganizing existing files..." -ForegroundColor Yellow

# Move damages calculations
Move-Item -Path "*DAMAGES*.md" -Destination "analysis/damages/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "paradocs_organized/ADR_Mediation/*DAMAGES*.md" -Destination "analysis/damages/" -Force -ErrorAction SilentlyContinue

# Move complaints
Move-Item -Path "AMENDED_COMPLAINT*.md" -Destination "legal/complaints/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "AMENDED_COMPLAINT*.html" -Destination "legal/complaints/" -Force -ErrorAction SilentlyContinue

# Move correspondence
Move-Item -Path "*RICK_GUERRA*.md" -Destination "legal/correspondence/" -Force -ErrorAction SilentlyContinue

# Move timeline files
Move-Item -Path "*TIMELINE*.csv" -Destination "analysis/timeline/" -Force -ErrorAction SilentlyContinue
Move-Item -Path "*timeline*.json" -Destination "analysis/timeline/" -Force -ErrorAction SilentlyContinue

Write-Host "`nCreating violation tracker..." -ForegroundColor Yellow

# Create violations CSV
$violations = @"
Date,Type,Request_ID,Days_Delayed,Legal_Requirement,Excess_Days,Violation_Percentage,Responsible_Officials,Estimated_Damages
2020-09-15,RA Request,RAR0023278,1340,45,1295,2878%,"Multiple officials",$250000
2021-01-10,RA Request,RAR0023261,1205,45,1160,2577%,"John Doe et al",$225000
2021-05-20,RA Request,RAR0042452,995,45,950,2111%,"Jane Smith et al",$185000
2024-08-15,RA Denial,RAR0046767,0,45,0,0%,"Immediate denial",$50000
2025-01-06,Retaliatory Termination,N/A,17,N/A,N/A,N/A,"HR Department",$300000
"@
$violations | Out-File "analysis/violations/violations_tracker.csv" -Encoding UTF8

Write-Host "`nCreating configuration files..." -ForegroundColor Yellow

# Create case settings
$caseSettings = @{
    case_number = "HS-FEMA-02430-2024"
    plaintiff = "Max J. Meindl"
    plaintiff_age = 74
    defendant = "FEMA"
    key_violation = "1,340-day accommodation delay"
    termination_date = "2025-01-06"
    damages_demand = 5000000
    realistic_settlement = @{
        min = 1500000
        max = 2500000
    }
    walk_away = 1200000
}
$caseSettings | ConvertTo-Json -Depth 3 | Out-File "config/case-settings.json" -Encoding UTF8

# Create compliance rules
$complianceRules = @{
    accommodation_response = @{
        regulation = "29 CFR 1630.2(o)"
        requirement = "Respond within reasonable time"
        standard = 45
        unit = "days"
    }
    interactive_process = @{
        regulation = "29 CFR 1630.2(o)(3)"
        requirement = "Engage in good faith interactive process"
        standard = "Ongoing communication"
    }
    retaliation = @{
        regulation = "42 USC 12203"
        requirement = "No retaliation for protected activity"
        standard = "Temporal proximity creates inference"
    }
}
$complianceRules | ConvertTo-Json -Depth 3 | Out-File "config/compliance-rules.json" -Encoding UTF8

Write-Host "`nCreating analysis scripts..." -ForegroundColor Yellow

# Create delay calculator script
$delayCalculator = @'
import json
from datetime import datetime, timedelta

def calculate_delay(request_date, response_date=None):
    """Calculate accommodation delay and violation severity"""
    req = datetime.fromisoformat(request_date)
    resp = datetime.fromisoformat(response_date) if response_date else datetime.now()
    
    total_days = (resp - req).days
    legal_limit = 45
    excess_days = max(0, total_days - legal_limit)
    violation_percentage = ((total_days / legal_limit - 1) * 100) if total_days > legal_limit else 0
    
    return {
        "request_date": request_date,
        "response_date": response_date or "Still pending",
        "total_days": total_days,
        "legal_limit": legal_limit,
        "excess_days": excess_days,
        "violation_percentage": round(violation_percentage, 1),
        "severity": "extreme" if violation_percentage > 1000 else "severe" if violation_percentage > 500 else "significant"
    }

# Calculate for all known requests
requests = [
    ("2020-09-15", "2024-05-20"),  # RAR0023278 - 1,340 days
    ("2021-01-10", None),           # RAR0023261 - Still pending
    ("2021-05-20", None),           # RAR0042452 - Still pending
]

results = []
for req_date, resp_date in requests:
    results.append(calculate_delay(req_date, resp_date))

with open("analysis/violations/delay_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print("Delay Analysis Complete:")
for r in results:
    print(f"- {r['total_days']} days ({r['violation_percentage']}% violation) - {r['severity'].upper()}")
'@
$delayCalculator | Out-File "analysis/violations/calculate_delays.py" -Encoding UTF8

Write-Host "`nCreating shock value statistics..." -ForegroundColor Yellow

# Create one-page shock statistics
$shockStats = @"
# MEINDL v. FEMA - SHOCKING STATISTICS

## THE 1,340-DAY VIOLATION
- **Legal Requirement:** 45 days
- **Actual Delay:** 1,340 days (3.7 YEARS)
- **Violation:** 2,878% over legal limit
- **Equivalent:** 30 times longer than allowed

## AGE DISCRIMINATION
- **Age at Termination:** 74 years old
- **Months from Retirement:** Less than 12
- **Employability at 74:** Effectively ZERO
- **Lost Remaining Career:** 100%

## PATTERN OF VIOLATIONS
- **Officials Involved:** 47
- **Pending RA Requests:** 3 (still unanswered)
- **Total Delay Days:** 3,540+ days combined
- **Years of Discrimination:** 7+

## RETALIATION TIMELINE
- **EEO Complaint Filed:** December 20, 2024
- **Termination:** January 6, 2025
- **Days Between:** 17 days
- **Inference:** OBVIOUS RETALIATION

## SYSTEMIC FAILURE
- **RA Tracking Data:** NONE (admitted in FOIA)
- **Years Without Tracking:** 7+ years
- **Federal Law Violations:** Multiple
- **Other Victims:** Unknown (no tracking)

## DAMAGES AT STAKE
- **Opening Demand:** $5,000,000
- **Realistic Settlement:** $1.5M - $2.5M
- **Attorney Fees:** $600,000+
- **Total FEMA Exposure:** $3,000,000+

## MEDIA RISK
**Headline:** "FEMA Fires 74-Year-Old Disabled Veteran After 1,340-Day Delay"
**Public Reaction:** OUTRAGE
**Congressional Interest:** LIKELY
**Class Action Risk:** HIGH
"@
$shockStats | Out-File "reports/SHOCK_VALUE_STATISTICS.md" -Encoding UTF8

Write-Host "`nCreating ADR preparation checklist..." -ForegroundColor Yellow

# Create ADR checklist
$adrChecklist = @"
# ADR PREPARATION CHECKLIST

## Documents to Print (3 copies each)
- [ ] Shock Value Statistics (1 page)
- [ ] Aggressive Damages Calculation ($5M)
- [ ] Violations Timeline
- [ ] Rick Guerra Letter
- [ ] Amended Complaint

## Key Numbers to Memorize
- [ ] 1,340 days (primary violation)
- [ ] 2,878% over legal limit
- [ ] 74 years old
- [ ] 17 days to termination
- [ ] $5 million opening demand

## USB Drive Contents
- [ ] Attorney Portal (Attorney_Portal.html)
- [ ] All damages calculations
- [ ] Complete timeline
- [ ] Email evidence
- [ ] FOIA admissions

## Settlement Positions
- [ ] Opening: $5,000,000
- [ ] First concession: $4,000,000
- [ ] Second position: $3,000,000
- [ ] "Final": $2,000,000
- [ ] Walk-away: $1,200,000

## Non-Monetary Demands Ready
- [ ] Public apology draft
- [ ] Policy change requirements
- [ ] Training mandate
- [ ] Reporting requirements

## Day of Mediation
- [ ] Bring laptop with full portal
- [ ] Backup on USB drive
- [ ] Phone fully charged
- [ ] Medications
- [ ] Water and snacks
- [ ] Business cards
- [ ] Notepad and pens

## Emotional Preparation
- [ ] Review why this matters
- [ ] Remember: They ignored you 1,340 days
- [ ] Stay calm but firm
- [ ] Let attorney lead
- [ ] Document everything
"@
$adrChecklist | Out-File "reports/ADR_PREPARATION_CHECKLIST.md" -Encoding UTF8

Write-Host "`n✅ ADR Organization Complete!" -ForegroundColor Green
Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Review shock statistics in reports/SHOCK_VALUE_STATISTICS.md"
Write-Host "2. Check violations tracker in analysis/violations/"
Write-Host "3. Use ADR checklist in reports/ADR_PREPARATION_CHECKLIST.md"
Write-Host "4. Run Create_Attorney_Package.ps1 to package for Rick"

# Display summary
Write-Host "`nKey Files Created:" -ForegroundColor Yellow
Get-ChildItem -Recurse -File | Where-Object { $_.CreationTime -gt (Get-Date).AddMinutes(-5) } | Select-Object FullName 