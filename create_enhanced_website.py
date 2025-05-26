import json
import os
from datetime import datetime

def load_analysis_results():
    """Load all analysis results from the tools."""
    results = {}
    
    # Load each analysis result
    analysis_files = {
        'document_scan': 'document_scan_results.json',
        'timeline': 'timeline_analysis_results.json',
        'roi_contradictions': 'roi_contradiction_analysis.json',
        'damages': 'damages_calculation_report.json',
        'email_analysis': 'email_analysis_report.json',
        'cleanup': 'cleanup_report.json'
    }
    
    for key, filename in analysis_files.items():
        try:
            with open(filename, 'r') as f:
                results[key] = json.load(f)
        except:
            results[key] = None
    
    # Load the main file index
    try:
        with open('paradocs_all_files.json', 'r') as f:
            results['all_files'] = json.load(f)
    except:
        results['all_files'] = []
    
    return results

def create_enhanced_html(results):
    """Create enhanced HTML with integrated analysis results."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ParaDocs - Enhanced Case Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --danger-color: #e74c3c;
            --warning-color: #f39c12;
            --info-color: #16a085;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }
        
        .navbar {
            background-color: var(--primary-color) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .stats-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
            transition: transform 0.2s;
        }
        
        .stats-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,.15);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .analysis-section {
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        
        .timeline-item {
            border-left: 3px solid var(--secondary-color);
            padding-left: 20px;
            margin-bottom: 20px;
            position: relative;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -8px;
            top: 0;
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: var(--secondary-color);
            border: 3px solid white;
        }
        
        .damage-category {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .damage-amount {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--danger-color);
        }
        
        .key-finding {
            background: #fff3cd;
            border-left: 4px solid var(--warning-color);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        
        .email-thread {
            background: #e7f3ff;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .tab-content {
            padding-top: 20px;
        }
        
        .filter-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .document-table {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        
        .badge-category {
            font-size: 0.85rem;
            padding: 5px 10px;
            margin-right: 5px;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .critical-alert {
            background: #fee;
            border-left: 4px solid var(--danger-color);
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        
        .recommendation-card {
            background: #e8f5e9;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <i class="bi bi-folder-fill"></i> ParaDocs Enhanced
            </a>
            <span class="navbar-text text-white">
                Comprehensive Case Analysis System
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <!-- Analysis Results Tabs -->
        <ul class="nav nav-tabs" id="analysisTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button">
                    <i class="bi bi-speedometer2"></i> Overview
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="documents-tab" data-bs-toggle="tab" data-bs-target="#documents" type="button">
                    <i class="bi bi-file-text"></i> Documents
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="timeline-tab" data-bs-toggle="tab" data-bs-target="#timeline" type="button">
                    <i class="bi bi-clock-history"></i> Timeline
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="damages-tab" data-bs-toggle="tab" data-bs-target="#damages" type="button">
                    <i class="bi bi-calculator"></i> Damages
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="emails-tab" data-bs-toggle="tab" data-bs-target="#emails" type="button">
                    <i class="bi bi-envelope"></i> Emails
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="findings-tab" data-bs-toggle="tab" data-bs-target="#findings" type="button">
                    <i class="bi bi-exclamation-triangle"></i> Key Findings
                </button>
            </li>
        </ul>

        <div class="tab-content" id="analysisTabContent">
            <!-- Overview Tab -->
            <div class="tab-pane fade show active" id="overview" role="tabpanel">
                <div class="row" id="statsContainer">
                    <!-- Stats will be populated by JavaScript -->
                </div>
                <div class="analysis-section mt-4">
                    <h3>Case Summary</h3>
                    <div id="caseSummary"></div>
                </div>
            </div>

            <!-- Documents Tab -->
            <div class="tab-pane fade" id="documents" role="tabpanel">
                <div class="filter-section">
                    <div class="row">
                        <div class="col-md-4">
                            <input type="text" class="form-control" id="searchInput" placeholder="Search documents...">
                        </div>
                        <div class="col-md-3">
                            <select class="form-select" id="categoryFilter">
                                <option value="">All Categories</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <select class="form-select" id="typeFilter">
                                <option value="">All Types</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <button class="btn btn-primary w-100" onclick="exportToCSV()">
                                <i class="bi bi-download"></i> Export
                            </button>
                        </div>
                    </div>
                </div>
                <div class="document-table">
                    <table class="table table-hover" id="documentsTable">
                        <thead>
                            <tr>
                                <th>Filename</th>
                                <th>Category</th>
                                <th>Type</th>
                                <th>Date</th>
                                <th>Keywords</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="documentsTableBody">
                            <!-- Documents will be populated by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Timeline Tab -->
            <div class="tab-pane fade" id="timeline" role="tabpanel">
                <div class="analysis-section">
                    <h3>Event Timeline Analysis</h3>
                    <div id="timelineStats" class="mb-4"></div>
                    <div id="timelineEvents"></div>
                </div>
            </div>

            <!-- Damages Tab -->
            <div class="tab-pane fade" id="damages" role="tabpanel">
                <div class="analysis-section">
                    <h3>Damages Calculation</h3>
                    <div id="damagesSummary" class="mb-4"></div>
                    <div id="damagesBreakdown"></div>
                </div>
            </div>

            <!-- Emails Tab -->
            <div class="tab-pane fade" id="emails" role="tabpanel">
                <div class="analysis-section">
                    <h3>Email Communications Analysis</h3>
                    <div id="emailStats" class="mb-4"></div>
                    <div id="emailThreads"></div>
                    <div id="keyEmails" class="mt-4"></div>
                </div>
            </div>

            <!-- Key Findings Tab -->
            <div class="tab-pane fade" id="findings" role="tabpanel">
                <div class="analysis-section">
                    <h3>Critical Findings & Recommendations</h3>
                    <div id="criticalFindings"></div>
                    <div id="recommendations" class="mt-4"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="paradocs-enhanced.js"></script>
</body>
</html>"""
    
    return html_content

def create_enhanced_javascript(results):
    """Create enhanced JavaScript with integrated analysis functionality."""
    js_content = f"""// Enhanced ParaDocs System with Analysis Integration
const analysisData = {json.dumps(results, indent=2)};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {{
    loadOverview();
    loadDocuments();
    loadTimeline();
    loadDamages();
    loadEmails();
    loadFindings();
    setupFilters();
}});

function loadOverview() {{
    const statsContainer = document.getElementById('statsContainer');
    const stats = [
        {{
            label: 'Total Documents',
            value: analysisData.all_files ? analysisData.all_files.length : 0,
            icon: 'bi-file-earmark-text',
            color: 'primary'
        }},
        {{
            label: 'Critical Documents',
            value: analysisData.document_scan?.summary?.critical_documents_found || 0,
            icon: 'bi-exclamation-circle',
            color: 'danger'
        }},
        {{
            label: 'Timeline Events',
            value: analysisData.timeline?.timeline_summary?.total_events || 0,
            icon: 'bi-calendar-event',
            color: 'info'
        }},
        {{
            label: 'Total Damages',
            value: analysisData.damages?.executive_summary?.total_potential_damages || '$0',
            icon: 'bi-currency-dollar',
            color: 'warning'
        }},
        {{
            label: 'Email Threads',
            value: analysisData.email_analysis?.summary?.email_threads || 0,
            icon: 'bi-envelope-open',
            color: 'success'
        }},
        {{
            label: 'Key Communications',
            value: analysisData.email_analysis?.summary?.key_communications || 0,
            icon: 'bi-chat-square-text',
            color: 'secondary'
        }}
    ];
    
    statsContainer.innerHTML = stats.map(stat => `
        <div class="col-md-4 col-lg-2">
            <div class="stats-card text-center">
                <i class="bi ${{stat.icon}} text-${{stat.color}}" style="font-size: 2rem;"></i>
                <p class="stat-number text-${{stat.color}}">${{stat.value}}</p>
                <p class="stat-label">${{stat.label}}</p>
            </div>
        </div>
    `).join('');
    
    // Load case summary
    const caseSummary = document.getElementById('caseSummary');
    if (analysisData.cleanup?.summary_created) {{
        caseSummary.innerHTML = `
            <div class="alert alert-info">
                <h5>ParaDocs Federal Employment Discrimination Case</h5>
                <p><strong>Case Type:</strong> Multi-statute discrimination and retaliation</p>
                <p><strong>Date Range:</strong> 2018-2025</p>
                <p><strong>Key Evidence:</strong> 450+ documents, 106 emails, documented 1340-day delay</p>
            </div>
        `;
    }}
}}

function loadDocuments() {{
    const tbody = document.getElementById('documentsTableBody');
    const categoryFilter = document.getElementById('categoryFilter');
    const typeFilter = document.getElementById('typeFilter');
    
    if (!analysisData.all_files) return;
    
    // Populate filters
    const categories = [...new Set(analysisData.all_files.map(f => f.category))];
    const types = [...new Set(analysisData.all_files.map(f => f.type))];
    
    categoryFilter.innerHTML = '<option value="">All Categories</option>' + 
        categories.map(c => `<option value="${{c}}">${{c}}</option>`).join('');
    
    typeFilter.innerHTML = '<option value="">All Types</option>' + 
        types.map(t => `<option value="${{t}}">${{t}}</option>`).join('');
    
    // Display documents
    displayDocuments(analysisData.all_files);
}}

function displayDocuments(documents) {{
    const tbody = document.getElementById('documentsTableBody');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    
    // Filter documents
    const filtered = documents.filter(doc => {{
        const matchesSearch = !searchTerm || 
            doc.filename.toLowerCase().includes(searchTerm) ||
            (doc.keywords && doc.keywords.some(k => k.toLowerCase().includes(searchTerm)));
        const matchesCategory = !categoryFilter || doc.category === categoryFilter;
        const matchesType = !typeFilter || doc.type === typeFilter;
        
        return matchesSearch && matchesCategory && matchesType;
    }});
    
    // Display filtered documents
    tbody.innerHTML = filtered.slice(0, 100).map(doc => {{
        const keywords = doc.keywords || [];
        const keywordBadges = keywords.slice(0, 3).map(k => 
            `<span class="badge bg-secondary badge-category">${{k}}</span>`
        ).join('');
        
        return `
            <tr>
                <td>${{doc.filename}}</td>
                <td><span class="badge bg-primary">${{doc.category}}</span></td>
                <td>${{doc.type}}</td>
                <td>${{doc.date || 'N/A'}}</td>
                <td>${{keywordBadges}}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewDocument('${{doc.filename}}')">
                        <i class="bi bi-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    }}).join('');
}}

function loadTimeline() {{
    const timelineStats = document.getElementById('timelineStats');
    const timelineEvents = document.getElementById('timelineEvents');
    
    if (!analysisData.timeline) return;
    
    const summary = analysisData.timeline.timeline_summary;
    timelineStats.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <div class="stats-card">
                    <p class="stat-label">Date Range</p>
                    <p class="fw-bold">${{summary.date_range.start}} to ${{summary.date_range.end}}</p>
                    <p class="text-muted">${{summary.date_range.span_days}} days</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card">
                    <p class="stat-label">Total Events</p>
                    <p class="stat-number text-info">${{summary.total_events}}</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card">
                    <p class="stat-label">Violations Found</p>
                    <p class="stat-number text-danger">${{analysisData.timeline.violations_found.length}}</p>
                </div>
            </div>
        </div>
    `;
    
    // Display key timeline events
    const events = analysisData.timeline.visual_timeline || [];
    timelineEvents.innerHTML = '<h4>Key Timeline Events</h4>' + 
        events.slice(0, 20).map(event => `
            <div class="timeline-item">
                <h6>${{event.date}}</h6>
                <strong>${{event.title}}</strong>
                <p class="text-muted mb-0">${{event.description}}</p>
            </div>
        `).join('');
}}

function loadDamages() {{
    const damagesSummary = document.getElementById('damagesSummary');
    const damagesBreakdown = document.getElementById('damagesBreakdown');
    
    if (!analysisData.damages) return;
    
    const summary = analysisData.damages.executive_summary;
    damagesSummary.innerHTML = `
        <div class="alert alert-warning">
            <h4 class="damage-amount">${{summary.total_potential_damages}}</h4>
            <p class="mb-0">Total Potential Damages</p>
        </div>
    `;
    
    // Display breakdown
    const categories = summary.damage_categories;
    damagesBreakdown.innerHTML = Object.entries(categories).map(([category, amount]) => `
        <div class="damage-category">
            <div class="d-flex justify-content-between align-items-center">
                <h5>${{category}}</h5>
                <span class="damage-amount">${{amount}}</span>
            </div>
        </div>
    `).join('');
}}

function loadEmails() {{
    const emailStats = document.getElementById('emailStats');
    const emailThreads = document.getElementById('emailThreads');
    const keyEmails = document.getElementById('keyEmails');
    
    if (!analysisData.email_analysis) return;
    
    const summary = analysisData.email_analysis.summary;
    emailStats.innerHTML = `
        <div class="row">
            <div class="col-md-3">
                <div class="stats-card">
                    <p class="stat-number text-primary">${{summary.total_emails_indexed}}</p>
                    <p class="stat-label">Total Emails</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <p class="stat-number text-success">${{summary.email_threads}}</p>
                    <p class="stat-label">Email Threads</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <p class="stat-number text-warning">${{summary.key_communications}}</p>
                    <p class="stat-label">Key Communications</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card">
                    <p class="stat-number text-info">${{summary.unique_senders}}</p>
                    <p class="stat-label">Unique Senders</p>
                </div>
            </div>
        </div>
    `;
    
    // Display important threads
    const threads = analysisData.email_analysis.important_threads || [];
    emailThreads.innerHTML = '<h4>Important Email Threads</h4>' + 
        threads.slice(0, 10).map(thread => `
            <div class="email-thread">
                <h6>${{thread.subject}}</h6>
                <p class="mb-1"><strong>${{thread.email_count}} emails</strong> | 
                   ${{thread.date_range.start}} to ${{thread.date_range.end}}</p>
                <p class="text-muted mb-0">Categories: ${{thread.categories.join(', ')}}</p>
            </div>
        `).join('');
}}

function loadFindings() {{
    const criticalFindings = document.getElementById('criticalFindings');
    const recommendations = document.getElementById('recommendations');
    
    // Critical findings from document scan
    if (analysisData.document_scan?.critical_findings) {{
        const findings = analysisData.document_scan.critical_findings;
        criticalFindings.innerHTML = '<h4>Critical Document Findings</h4>' + 
            findings.map(finding => `
                <div class="key-finding">
                    <h6>${{finding.category}}</h6>
                    <p class="mb-1"><strong>${{finding.document_count}} documents found</strong></p>
                    <p class="mb-0">Common issues: ${{finding.common_issues.join(', ')}}</p>
                </div>
            `).join('');
    }}
    
    // Recommendations
    const allRecommendations = [];
    
    if (analysisData.document_scan?.recommendations) {{
        allRecommendations.push(...analysisData.document_scan.recommendations);
    }}
    if (analysisData.damages?.detailed_calculations?.recommendations) {{
        allRecommendations.push(...analysisData.damages.detailed_calculations.recommendations);
    }}
    if (analysisData.cleanup?.recommendations) {{
        allRecommendations.push(...analysisData.cleanup.recommendations);
    }}
    
    recommendations.innerHTML = '<h4>Recommendations</h4>' + 
        [...new Set(allRecommendations)].map(rec => `
            <div class="recommendation-card">
                <i class="bi bi-check-circle text-success"></i> ${{rec}}
            </div>
        `).join('');
}}

function setupFilters() {{
    document.getElementById('searchInput').addEventListener('input', () => displayDocuments(analysisData.all_files || []));
    document.getElementById('categoryFilter').addEventListener('change', () => displayDocuments(analysisData.all_files || []));
    document.getElementById('typeFilter').addEventListener('change', () => displayDocuments(analysisData.all_files || []));
}}

function viewDocument(filename) {{
    // In a real implementation, this would open the document
    alert(`Opening document: ${{filename}}`);
}}

function exportToCSV() {{
    if (!analysisData.all_files) return;
    
    const headers = ['Filename', 'Category', 'Type', 'Date', 'Size', 'Keywords'];
    const rows = analysisData.all_files.map(doc => [
        doc.filename,
        doc.category,
        doc.type,
        doc.date || '',
        doc.size || '',
        (doc.keywords || []).join('; ')
    ]);
    
    const csv = [headers, ...rows].map(row => 
        row.map(cell => `"${{String(cell).replace(/"/g, '""')}}"`).join(',')
    ).join('\\n');
    
    const blob = new Blob([csv], {{ type: 'text/csv' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'paradocs_enhanced_export.csv';
    a.click();
    URL.revokeObjectURL(url);
}}
"""
    
    return js_content

def create_analysis_dashboard():
    """Create a dashboard summarizing all analysis results."""
    results = load_analysis_results()
    
    dashboard = {
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "overview": {
            "total_documents_analyzed": len(results.get('all_files', [])),
            "critical_documents_found": results.get('document_scan', {}).get('summary', {}).get('critical_documents_found', 0),
            "timeline_events": results.get('timeline', {}).get('timeline_summary', {}).get('total_events', 0),
            "total_potential_damages": results.get('damages', {}).get('executive_summary', {}).get('total_potential_damages', '$0'),
            "emails_analyzed": results.get('email_analysis', {}).get('summary', {}).get('total_emails_indexed', 0),
            "key_communications": results.get('email_analysis', {}).get('summary', {}).get('key_communications', 0)
        },
        "key_findings": [],
        "action_items": []
    }
    
    # Collect key findings
    if results.get('document_scan') and results['document_scan'].get('recommendations'):
        dashboard['key_findings'].extend([
            f"Document Analysis: {rec}" for rec in results['document_scan']['recommendations']
        ])
    
    if results.get('timeline') and results['timeline'].get('violations_found'):
        dashboard['key_findings'].append(
            f"Timeline Analysis: {len(results['timeline']['violations_found'])} violations identified"
        )
    
    if results.get('roi_contradictions'):
        contradictions = results['roi_contradictions'].get('summary', {}).get('total_contradictions_found', 0)
        if contradictions > 0:
            dashboard['key_findings'].append(f"ROI Analysis: {contradictions} contradictions found")
    
    # Action items
    dashboard['action_items'] = [
        "Review all critical documents flagged by the scanner",
        "Examine timeline violations for legal significance",
        "Validate damage calculations with supporting evidence",
        "Review key email communications for discovery",
        "Prepare exhibit list based on document categories"
    ]
    
    return dashboard

if __name__ == "__main__":
    print("Creating enhanced ParaDocs website with analysis integration...")
    
    # Load all analysis results
    results = load_analysis_results()
    
    # Create enhanced HTML
    html_content = create_enhanced_html(results)
    with open('paradocs-enhanced.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Create enhanced JavaScript
    js_content = create_enhanced_javascript(results)
    with open('paradocs-enhanced.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # Create analysis dashboard
    dashboard = create_analysis_dashboard()
    with open('analysis_dashboard.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    
    print("\n✅ Enhanced website created successfully!")
    print("Files generated:")
    print("- paradocs-enhanced.html (Main website)")
    print("- paradocs-enhanced.js (JavaScript functionality)")
    print("- analysis_dashboard.json (Summary dashboard)")
    print("\nOpen paradocs-enhanced.html in your browser to view the enhanced system.") 