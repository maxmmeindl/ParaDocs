# GitHub Pages Documentation Site Setup Guide
## Case: HS-FEMA-02430-2024

## Quick Setup Steps

### 1. Repository Setup
```bash
# Navigate to your ParaDocs folder
cd 'C:/Users/Max/Documents/EEO FILES/ParaDocs'

# Initialize git if not already done
git init

# Add all files
git add .

# Initial commit
git commit -m 'Initial case documentation commit'

# Add GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/paradocs-evidence.git

# Push to GitHub
git push -u origin main
```

### 2. Enable GitHub Pages
1. Go to your repository on GitHub
2. Click 'Settings' tab
3. Scroll to 'Pages' section
4. Under 'Source', select 'Deploy from a branch'
5. Choose 'main' branch and '/ (root)' folder
6. Click 'Save'
7. Your site will be available at: `https://USERNAME.github.io/paradocs-evidence/`

### 3. Create Index Page
Create `index.html` in your root directory:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EEOC Case HS-FEMA-02430-2024 - Evidence Repository</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <h1>Case Evidence Repository</h1>
        <p>EEOC Case No. HS-FEMA-02430-2024</p>
    </header>
    
    <nav>
        <ul>
            <li><a href="#critical">Critical Evidence</a></li>
            <li><a href="#timeline">Timeline</a></li>
            <li><a href="#damages">Damages</a></li>
            <li><a href="#legal">Legal Documents</a></li>
        </ul>
    </nav>
    
    <main>
        <section id="critical">
            <h2>⚠️ Critical Evidence</h2>
            <div class="alert">
                <h3>1,340-Day Violation</h3>
                <p>FEMA ignored accommodation request for <strong>3.7 years</strong></p>
                <a href="evidence/timeline/1340-day-violation/">View Evidence</a>
            </div>
        </section>
        
        <section id="timeline">
            <h2>📅 Case Timeline</h2>
            <a href="evidence/timeline/visual-timeline.html">Interactive Timeline</a>
        </section>
        
        <section id="damages">
            <h2>💰 Damage Calculations</h2>
            <p>Total Damages: <strong>$1,511,684.93</strong></p>
            <a href="evidence/damages/">View Breakdown</a>
        </section>
    </main>
    
    <footer>
        <p>Last Updated: May 25, 2025</p>
    </footer>
</body>
</html>```

## Recommended Directory Structure

```
paradocs-evidence/
├── index.html                    # Main landing page
├── README.md                     # Repository description
├── _config.yml                   # Jekyll configuration
├── assets/
│   ├── css/
│   │   └── style.css            # Custom styles
│   └── js/
│       └── search.js            # Search functionality
├── evidence/
│   ├── timeline/
│   │   ├── visual-timeline.html
│   │   ├── 1340-day-violation/
│   │   │   ├── index.md
│   │   │   └── supporting-docs/
│   │   └── chronology.json
│   ├── accommodations/
│   │   ├── 2020-request/
│   │   ├── 2023-request/
│   │   └── tracking-failures/
│   ├── retaliation/
│   │   ├── pip-timeline/
│   │   ├── termination/
│   │   └── pattern-evidence/
│   ├── roi-analysis/
│   │   ├── contradictions/
│   │   ├── missing-evidence/
│   │   └── key-admissions/
│   └── damages/
│       ├── calculations/
│       └── supporting-docs/
├── legal/
│   ├── complaint/
│   ├── motions/
│   ├── briefs/
│   └── citations/
├── discovery/
│   ├── requests/
│   ├── responses/
│   └── deficiencies/
├── exhibits/
│   ├── emails/
│   ├── documents/
│   └── policies/
└── analysis/
    ├── reports/
    ├── expert-opinions/
    └── data-visualizations/
```

## Key Pages to Create

### 1. Main Evidence Dashboard (`evidence/index.md`)
```markdown
# Evidence Dashboard

## Critical Violations
- [1,340-Day Violation](./timeline/1340-day-violation/) ⚠️ EXTREME
- [36-Day Delay](./accommodations/2023-request/)
- [Zero Interactive Process](./accommodations/tracking-failures/)

## Retaliation Timeline
- [PIP After EEO](./retaliation/pip-timeline/)
- [Termination During Investigation](./retaliation/termination/)
```

### 2. 1,340-Day Violation Page (`evidence/timeline/1340-day-violation/index.md`)
```markdown
# 1,340-Day Accommodation Violation

## Summary
FEMA ignored accommodation request for **1,340 days** (3.7 years)

## Key Evidence
- [Initial Request (Sept 2020)](./supporting-docs/initial-request.pdf)
- [Follow-up Emails](./supporting-docs/follow-ups/)
- [ROI Admissions](./supporting-docs/roi-excerpts.pdf)

## Legal Impact
- Per se liability
- $550,684 in damages for this violation alone
```

### 3. Timeline Visualization (`evidence/timeline/visual-timeline.html`)
Use the already generated timeline exhibit HTML

## Jekyll Configuration (`_config.yml`)
```yaml
title: EEOC Case HS-FEMA-02430-2024 Evidence Repository
description: Comprehensive case documentation and evidence
theme: jekyll-theme-minimal
plugins:
  - jekyll-relative-links
  - jekyll-sitemap
relative_links:
  enabled: true
  collections: true
```

## Security Considerations

### Public vs Private Repository
**IMPORTANT**: Consider making the repository PRIVATE if it contains:
- Personal identifying information
- Confidential settlement discussions
- Attorney-client privileged information
- Medical records

### Redaction Strategy
1. Redact SSN, addresses, phone numbers
2. Use initials instead of full names for non-parties
3. Remove account numbers and employee IDs
4. Keep case-relevant information visible

## Maintenance Commands

```bash
# Add new evidence
git add evidence/new-document.pdf
git commit -m 'Add [description of evidence]'
git push

# Update timeline
git add evidence/timeline/
git commit -m 'Update timeline with new events'
git push

# Full update
git add .
git commit -m 'Update case documentation'
git push
```

## Search Functionality
Add search to your site by including this in your pages:

```html
<div class="search-container">
  <input type="text" id="search-input" placeholder="Search evidence...">
  <div id="search-results"></div>
</div>
```

## Next Steps
1. Create the directory structure
2. Move documents into appropriate folders
3. Create index pages for each section
4. Add navigation menu
5. Test locally before pushing
6. Enable GitHub Pages
7. Share secure link with legal team
