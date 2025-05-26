#!/usr/bin/env python3
"""
GitHub Pages Setup Guide and Document Organization Structure
"""

from datetime import datetime
import json

class GitHubPagesSetupGuide:
    """Complete guide for GitHub Pages documentation site"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.repo_name = "paradocs-evidence"
        
    def generate_setup_guide(self):
        """Generate comprehensive GitHub Pages setup guide"""
        
        with open('github_pages_setup_guide.md', 'w', encoding='utf-8') as f:
            f.write("# GitHub Pages Documentation Site Setup Guide\n")
            f.write(f"## Case: {self.case_number}\n\n")
            
            f.write("## Quick Setup Steps\n\n")
            
            f.write("### 1. Repository Setup\n")
            f.write("```bash\n")
            f.write("# Navigate to your ParaDocs folder\n")
            f.write("cd 'C:/Users/Max/Documents/EEO FILES/ParaDocs'\n\n")
            f.write("# Initialize git if not already done\n")
            f.write("git init\n\n")
            f.write("# Add all files\n")
            f.write("git add .\n\n")
            f.write("# Initial commit\n")
            f.write("git commit -m 'Initial case documentation commit'\n\n")
            f.write("# Add GitHub remote (replace USERNAME with your GitHub username)\n")
            f.write("git remote add origin https://github.com/USERNAME/paradocs-evidence.git\n\n")
            f.write("# Push to GitHub\n")
            f.write("git push -u origin main\n")
            f.write("```\n\n")
            
            f.write("### 2. Enable GitHub Pages\n")
            f.write("1. Go to your repository on GitHub\n")
            f.write("2. Click 'Settings' tab\n")
            f.write("3. Scroll to 'Pages' section\n")
            f.write("4. Under 'Source', select 'Deploy from a branch'\n")
            f.write("5. Choose 'main' branch and '/ (root)' folder\n")
            f.write("6. Click 'Save'\n")
            f.write("7. Your site will be available at: `https://USERNAME.github.io/paradocs-evidence/`\n\n")
            
            f.write("### 3. Create Index Page\n")
            f.write("Create `index.html` in your root directory:\n\n")
            f.write("```html\n")
            f.write(self.generate_index_html())
            f.write("```\n\n")
            
            f.write("## Recommended Directory Structure\n\n")
            f.write("```\n")
            f.write("paradocs-evidence/\n")
            f.write("├── index.html                    # Main landing page\n")
            f.write("├── README.md                     # Repository description\n")
            f.write("├── _config.yml                   # Jekyll configuration\n")
            f.write("├── assets/\n")
            f.write("│   ├── css/\n")
            f.write("│   │   └── style.css            # Custom styles\n")
            f.write("│   └── js/\n")
            f.write("│       └── search.js            # Search functionality\n")
            f.write("├── evidence/\n")
            f.write("│   ├── timeline/\n")
            f.write("│   │   ├── visual-timeline.html\n")
            f.write("│   │   ├── 1340-day-violation/\n")
            f.write("│   │   │   ├── index.md\n")
            f.write("│   │   │   └── supporting-docs/\n")
            f.write("│   │   └── chronology.json\n")
            f.write("│   ├── accommodations/\n")
            f.write("│   │   ├── 2020-request/\n")
            f.write("│   │   ├── 2023-request/\n")
            f.write("│   │   └── tracking-failures/\n")
            f.write("│   ├── retaliation/\n")
            f.write("│   │   ├── pip-timeline/\n")
            f.write("│   │   ├── termination/\n")
            f.write("│   │   └── pattern-evidence/\n")
            f.write("│   ├── roi-analysis/\n")
            f.write("│   │   ├── contradictions/\n")
            f.write("│   │   ├── missing-evidence/\n")
            f.write("│   │   └── key-admissions/\n")
            f.write("│   └── damages/\n")
            f.write("│       ├── calculations/\n")
            f.write("│       └── supporting-docs/\n")
            f.write("├── legal/\n")
            f.write("│   ├── complaint/\n")
            f.write("│   ├── motions/\n")
            f.write("│   ├── briefs/\n")
            f.write("│   └── citations/\n")
            f.write("├── discovery/\n")
            f.write("│   ├── requests/\n")
            f.write("│   ├── responses/\n")
            f.write("│   └── deficiencies/\n")
            f.write("├── exhibits/\n")
            f.write("│   ├── emails/\n")
            f.write("│   ├── documents/\n")
            f.write("│   └── policies/\n")
            f.write("└── analysis/\n")
            f.write("    ├── reports/\n")
            f.write("    ├── expert-opinions/\n")
            f.write("    └── data-visualizations/\n")
            f.write("```\n\n")
            
            f.write("## Key Pages to Create\n\n")
            
            f.write("### 1. Main Evidence Dashboard (`evidence/index.md`)\n")
            f.write("```markdown\n")
            f.write("# Evidence Dashboard\n\n")
            f.write("## Critical Violations\n")
            f.write("- [1,340-Day Violation](./timeline/1340-day-violation/) ⚠️ EXTREME\n")
            f.write("- [36-Day Delay](./accommodations/2023-request/)\n")
            f.write("- [Zero Interactive Process](./accommodations/tracking-failures/)\n\n")
            f.write("## Retaliation Timeline\n")
            f.write("- [PIP After EEO](./retaliation/pip-timeline/)\n")
            f.write("- [Termination During Investigation](./retaliation/termination/)\n")
            f.write("```\n\n")
            
            f.write("### 2. 1,340-Day Violation Page (`evidence/timeline/1340-day-violation/index.md`)\n")
            f.write("```markdown\n")
            f.write("# 1,340-Day Accommodation Violation\n\n")
            f.write("## Summary\n")
            f.write("FEMA ignored accommodation request for **1,340 days** (3.7 years)\n\n")
            f.write("## Key Evidence\n")
            f.write("- [Initial Request (Sept 2020)](./supporting-docs/initial-request.pdf)\n")
            f.write("- [Follow-up Emails](./supporting-docs/follow-ups/)\n")
            f.write("- [ROI Admissions](./supporting-docs/roi-excerpts.pdf)\n\n")
            f.write("## Legal Impact\n")
            f.write("- Per se liability\n")
            f.write("- $550,684 in damages for this violation alone\n")
            f.write("```\n\n")
            
            f.write("### 3. Timeline Visualization (`evidence/timeline/visual-timeline.html`)\n")
            f.write("Use the already generated timeline exhibit HTML\n\n")
            
            f.write("## Jekyll Configuration (`_config.yml`)\n")
            f.write("```yaml\n")
            f.write("title: EEOC Case HS-FEMA-02430-2024 Evidence Repository\n")
            f.write("description: Comprehensive case documentation and evidence\n")
            f.write("theme: jekyll-theme-minimal\n")
            f.write("plugins:\n")
            f.write("  - jekyll-relative-links\n")
            f.write("  - jekyll-sitemap\n")
            f.write("relative_links:\n")
            f.write("  enabled: true\n")
            f.write("  collections: true\n")
            f.write("```\n\n")
            
            f.write("## Security Considerations\n\n")
            f.write("### Public vs Private Repository\n")
            f.write("**IMPORTANT**: Consider making the repository PRIVATE if it contains:\n")
            f.write("- Personal identifying information\n")
            f.write("- Confidential settlement discussions\n")
            f.write("- Attorney-client privileged information\n")
            f.write("- Medical records\n\n")
            
            f.write("### Redaction Strategy\n")
            f.write("1. Redact SSN, addresses, phone numbers\n")
            f.write("2. Use initials instead of full names for non-parties\n")
            f.write("3. Remove account numbers and employee IDs\n")
            f.write("4. Keep case-relevant information visible\n\n")
            
            f.write("## Maintenance Commands\n\n")
            f.write("```bash\n")
            f.write("# Add new evidence\n")
            f.write("git add evidence/new-document.pdf\n")
            f.write("git commit -m 'Add [description of evidence]'\n")
            f.write("git push\n\n")
            f.write("# Update timeline\n")
            f.write("git add evidence/timeline/\n")
            f.write("git commit -m 'Update timeline with new events'\n")
            f.write("git push\n\n")
            f.write("# Full update\n")
            f.write("git add .\n")
            f.write("git commit -m 'Update case documentation'\n")
            f.write("git push\n")
            f.write("```\n\n")
            
            f.write("## Search Functionality\n")
            f.write("Add search to your site by including this in your pages:\n\n")
            f.write("```html\n")
            f.write('<div class="search-container">\n')
            f.write('  <input type="text" id="search-input" placeholder="Search evidence...">\n')
            f.write('  <div id="search-results"></div>\n')
            f.write('</div>\n')
            f.write("```\n\n")
            
            f.write("## Next Steps\n")
            f.write("1. Create the directory structure\n")
            f.write("2. Move documents into appropriate folders\n")
            f.write("3. Create index pages for each section\n")
            f.write("4. Add navigation menu\n")
            f.write("5. Test locally before pushing\n")
            f.write("6. Enable GitHub Pages\n")
            f.write("7. Share secure link with legal team\n")
    
    def generate_index_html(self):
        """Generate main index.html content"""
        return """<!DOCTYPE html>
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
        <p>Last Updated: """ + datetime.now().strftime('%B %d, %Y') + """</p>
    </footer>
</body>
</html>"""
    
    def generate_css_template(self):
        """Generate CSS template for styling"""
        css_content = """/* Custom styles for evidence repository */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background-color: #1a472a;
    color: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}

nav ul {
    list-style: none;
    padding: 0;
    display: flex;
    gap: 2rem;
    background-color: #f4f4f4;
    padding: 1rem;
    border-radius: 8px;
}

nav a {
    text-decoration: none;
    color: #1a472a;
    font-weight: bold;
}

.alert {
    background-color: #fee;
    border-left: 5px solid #c00;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
}

.alert h3 {
    color: #c00;
    margin: 0 0 0.5rem 0;
}

section {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1rem;
    color: #666;
}"""
        
        with open('style_template.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        return css_content


def main():
    guide = GitHubPagesSetupGuide()
    
    print("GENERATING GITHUB PAGES SETUP GUIDE")
    print("=" * 70)
    
    try:
        # Generate setup guide
        guide.generate_setup_guide()
        
        # Generate CSS template
        guide.generate_css_template()
        
        print("\nGenerated Files:")
        print("1. github_pages_setup_guide.md - Complete setup instructions")
        print("2. style_template.css - CSS template for your site")
        
        print("\nNext: Creating email indexing system...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 