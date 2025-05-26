#!/usr/bin/env python3
"""
Email Indexing System for Case Documentation
Generates CSV and HTML indexes of all emails
"""

import csv
import json
from datetime import datetime
import re

class EmailIndexingSystem:
    """Comprehensive email indexing and tracking system"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.email_categories = {
            'accommodation_requests': 'Accommodation-related emails',
            'denials': 'Denial communications',
            'follow_ups': 'Follow-up emails',
            'eeo_communications': 'EEO process emails',
            'retaliation': 'Post-EEO adverse actions',
            'roi_related': 'Investigation emails',
            'internal': 'Internal agency communications',
            'medical': 'Medical documentation emails'
        }
    
    def create_email_template(self):
        """Create template for email indexing"""
        
        # Sample email entries - replace with actual emails
        email_template = [
            {
                'email_id': 'EM-001',
                'date': '2020-09-15',
                'time': '09:30 AM',
                'from': 'Complainant',
                'to': 'HR Director',
                'cc': 'Supervisor',
                'bcc': '',
                'subject': 'Request for Reasonable Accommodation',
                'category': 'accommodation_requests',
                'key_content': 'Initial request for telework accommodation due to disability',
                'attachments': 'Medical documentation.pdf',
                'response_received': 'No',
                'response_date': 'Never',
                'days_to_response': '1340',
                'legal_significance': 'Start of 1,340-day violation',
                'exhibit_number': 'Exhibit A-1',
                'roi_reference': 'ROI Part 1, p. 26',
                'notes': 'CRITICAL - Never acknowledged'
            },
            {
                'email_id': 'EM-002',
                'date': '2020-10-15',
                'time': '02:15 PM',
                'from': 'Complainant',
                'to': 'HR Director',
                'cc': 'Supervisor, HR Assistant',
                'bcc': '',
                'subject': 'Follow-up: Accommodation Request',
                'category': 'follow_ups',
                'key_content': 'First follow-up, no response to September request',
                'attachments': 'None',
                'response_received': 'No',
                'response_date': 'Never',
                'days_to_response': 'N/A',
                'legal_significance': 'Shows agency had notice',
                'exhibit_number': 'Exhibit A-2',
                'roi_reference': 'ROI Part 1, p. 27',
                'notes': 'Proves knowledge of request'
            },
            {
                'email_id': 'EM-003',
                'date': '2021-01-10',
                'time': '11:00 AM',
                'from': 'Complainant',
                'to': 'HR Director, Supervisor',
                'cc': '',
                'bcc': '',
                'subject': 'Urgent: Still Awaiting Accommodation Response',
                'category': 'follow_ups',
                'key_content': 'Multiple follow-ups ignored, requesting any response',
                'attachments': 'Previous_emails.pdf',
                'response_received': 'No',
                'response_date': 'Never',
                'days_to_response': 'N/A',
                'legal_significance': 'Pattern of ignoring requests',
                'exhibit_number': 'Exhibit A-3',
                'roi_reference': 'ROI Part 1, p. 28',
                'notes': 'Shows persistent attempts'
            },
            {
                'email_id': 'EM-004',
                'date': '2023-11-09',
                'time': '08:45 AM',
                'from': 'Complainant',
                'to': 'New HR Manager',
                'cc': 'Supervisor',
                'bcc': '',
                'subject': 'Renewed Request for Telework Accommodation',
                'category': 'accommodation_requests',
                'key_content': 'New accommodation request after management change',
                'attachments': 'Updated_medical.pdf',
                'response_received': 'Yes',
                'response_date': '2023-12-15',
                'days_to_response': '36',
                'legal_significance': '36-day delay violation',
                'exhibit_number': 'Exhibit B-1',
                'roi_reference': 'ROI Part 1, p. 11',
                'notes': 'Second violation'
            },
            {
                'email_id': 'EM-005',
                'date': '2023-12-15',
                'time': '04:30 PM',
                'from': 'HR Manager',
                'to': 'Complainant',
                'cc': '',
                'bcc': '',
                'subject': 'RE: Telework Accommodation Request',
                'category': 'denials',
                'key_content': 'Denial without interactive process',
                'attachments': 'None',
                'response_received': 'N/A',
                'response_date': 'N/A',
                'days_to_response': 'N/A',
                'legal_significance': 'No interactive process violation',
                'exhibit_number': 'Exhibit B-2',
                'roi_reference': 'ROI Part 1, p. 12',
                'notes': 'Flat denial, no alternatives'
            },
            {
                'email_id': 'EM-006',
                'date': '2024-01-08',
                'time': '10:00 AM',
                'from': 'Complainant',
                'to': 'EEO Counselor',
                'cc': '',
                'bcc': '',
                'subject': 'Request for EEO Counseling',
                'category': 'eeo_communications',
                'key_content': 'Initiating EEO process due to discrimination',
                'attachments': 'Accommodation_history.pdf',
                'response_received': 'Yes',
                'response_date': '2024-01-09',
                'days_to_response': '1',
                'legal_significance': 'Protected activity begins',
                'exhibit_number': 'Exhibit C-1',
                'roi_reference': 'ROI Part 1, p. 3',
                'notes': 'Start of EEO process'
            },
            {
                'email_id': 'EM-007',
                'date': '2024-03-21',
                'time': '09:00 AM',
                'from': 'Supervisor',
                'to': 'Complainant',
                'cc': 'HR',
                'bcc': '',
                'subject': 'Performance Improvement Plan',
                'category': 'retaliation',
                'attachments': 'PIP_document.pdf',
                'response_received': 'N/A',
                'response_date': 'N/A',
                'days_to_response': 'N/A',
                'legal_significance': 'Retaliation - temporal proximity',
                'exhibit_number': 'Exhibit D-1',
                'roi_reference': 'ROI Part 1, p. 45',
                'notes': 'Clear retaliation'
            },
            {
                'email_id': 'EM-008',
                'date': '2024-05-30',
                'time': '03:00 PM',
                'from': 'HR Director',
                'to': 'Complainant',
                'cc': 'Legal',
                'bcc': '',
                'subject': 'Notice of Termination',
                'category': 'retaliation',
                'key_content': 'Termination during pending EEO investigation',
                'attachments': 'Termination_letter.pdf',
                'response_received': 'N/A',
                'response_date': 'N/A',
                'days_to_response': 'N/A',
                'legal_significance': 'Per se retaliation',
                'exhibit_number': 'Exhibit D-2',
                'roi_reference': 'ROI Part 2, p. 15',
                'notes': 'Termination during investigation'
            }
        ]
        
        return email_template
    
    def generate_csv_index(self, emails):
        """Generate CSV file with email index"""
        
        filename = f'email_index_{self.case_number}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'email_id', 'date', 'time', 'from', 'to', 'cc', 'bcc',
                'subject', 'category', 'key_content', 'attachments',
                'response_received', 'response_date', 'days_to_response',
                'legal_significance', 'exhibit_number', 'roi_reference', 'notes'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for email in emails:
                writer.writerow(email)
        
        print(f"CSV index generated: {filename}")
        return filename
    
    def generate_html_index(self, emails):
        """Generate searchable HTML index"""
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Index - Case """ + self.case_number + """</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #1a472a;
        }
        .search-box {
            margin: 20px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #1a472a;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .critical {
            background-color: #fee;
            font-weight: bold;
        }
        .category {
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            color: white;
        }
        .accommodation_requests { background-color: #28a745; }
        .denials { background-color: #dc3545; }
        .follow_ups { background-color: #ffc107; color: black; }
        .eeo_communications { background-color: #17a2b8; }
        .retaliation { background-color: #dc3545; }
    </style>
</head>
<body>
    <h1>Email Index - Case """ + self.case_number + """</h1>
    
    <div class="search-box">
        <input type="text" id="searchInput" onkeyup="filterTable()" 
               placeholder="Search emails by any field...">
    </div>
    
    <table id="emailTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>From</th>
                <th>To</th>
                <th>Subject</th>
                <th>Category</th>
                <th>Response Time</th>
                <th>Legal Significance</th>
                <th>Exhibit</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for email in emails:
            row_class = 'critical' if '1340' in str(email.get('days_to_response', '')) else ''
            html_content += f"""
            <tr class="{row_class}">
                <td>{email['email_id']}</td>
                <td>{email['date']}</td>
                <td>{email['from']}</td>
                <td>{email['to']}</td>
                <td>{email['subject']}</td>
                <td><span class="category {email['category']}">{email['category'].replace('_', ' ').title()}</span></td>
                <td>{email.get('days_to_response', 'N/A')} days</td>
                <td>{email['legal_significance']}</td>
                <td>{email['exhibit_number']}</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
    
    <script>
    function filterTable() {
        var input = document.getElementById("searchInput");
        var filter = input.value.toUpperCase();
        var table = document.getElementById("emailTable");
        var tr = table.getElementsByTagName("tr");
        
        for (var i = 1; i < tr.length; i++) {
            var td = tr[i].getElementsByTagName("td");
            var found = false;
            
            for (var j = 0; j < td.length; j++) {
                if (td[j]) {
                    var txtValue = td[j].textContent || td[j].innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }
            
            tr[i].style.display = found ? "" : "none";
        }
    }
    </script>
</body>
</html>
"""
        
        filename = f'email_index_{self.case_number}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML index generated: {filename}")
        return filename
    
    def generate_summary_statistics(self, emails):
        """Generate summary statistics of email patterns"""
        
        stats = {
            'total_emails': len(emails),
            'categories': {},
            'response_times': [],
            'unanswered': 0,
            'critical_delays': 0
        }
        
        for email in emails:
            # Category counts
            cat = email['category']
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            # Response analysis
            if email['response_received'] == 'No':
                stats['unanswered'] += 1
            
            # Critical delays
            if email['days_to_response'] != 'N/A':
                try:
                    days = int(email['days_to_response'])
                    stats['response_times'].append(days)
                    if days > 30:
                        stats['critical_delays'] += 1
                except:
                    pass
        
        # Generate summary report
        with open(f'email_statistics_{self.case_number}.txt', 'w') as f:
            f.write(f"EMAIL ANALYSIS SUMMARY\n")
            f.write(f"Case: {self.case_number}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total Emails Indexed: {stats['total_emails']}\n")
            f.write(f"Unanswered Emails: {stats['unanswered']}\n")
            f.write(f"Critical Delays (>30 days): {stats['critical_delays']}\n\n")
            
            f.write("Email Categories:\n")
            for cat, count in stats['categories'].items():
                f.write(f"  - {cat.replace('_', ' ').title()}: {count}\n")
            
            if stats['response_times']:
                f.write(f"\nResponse Time Analysis:\n")
                f.write(f"  - Longest delay: {max(stats['response_times'])} days\n")
                f.write(f"  - Average delay: {sum(stats['response_times'])/len(stats['response_times']):.1f} days\n")
                f.write(f"  - Delays over 30 days: {len([d for d in stats['response_times'] if d > 30])}\n")
        
        return stats


def main():
    indexer = EmailIndexingSystem()
    
    print("EMAIL INDEXING SYSTEM")
    print("=" * 70)
    
    # Create email template data
    emails = indexer.create_email_template()
    
    # Generate CSV index
    csv_file = indexer.generate_csv_index(emails)
    
    # Generate HTML index
    html_file = indexer.generate_html_index(emails)
    
    # Generate statistics
    stats = indexer.generate_summary_statistics(emails)
    
    print("\nGenerated Files:")
    print(f"1. {csv_file} - Excel-compatible email index")
    print(f"2. {html_file} - Searchable HTML index")
    print(f"3. email_statistics_{indexer.case_number}.txt - Summary analysis")
    
    print("\nKey Findings:")
    print(f"- Total emails: {stats['total_emails']}")
    print(f"- Unanswered: {stats['unanswered']}")
    print(f"- Critical delays: {stats['critical_delays']}")
    
    print("\nNext Steps:")
    print("1. Replace template data with actual emails")
    print("2. Add any additional email fields needed")
    print("3. Import CSV into Excel for sorting/filtering")
    print("4. Use HTML version for quick searching")


if __name__ == "__main__":
    main() 