#!/usr/bin/env python3
"""
Create comprehensive Excel template for email indexing
"""

import csv
from datetime import datetime

def create_comprehensive_email_template():
    """Create a comprehensive template for email tracking"""
    
    # Define all columns for comprehensive email tracking
    columns = [
        'email_id',
        'date_sent',
        'time_sent',
        'date_received',
        'time_received',
        'from_name',
        'from_email',
        'from_title',
        'to_name',
        'to_email',
        'to_title',
        'cc_names',
        'cc_emails',
        'bcc_names',
        'bcc_emails',
        'subject',
        'thread_id',
        'in_reply_to',
        'category',
        'subcategory',
        'key_content_summary',
        'full_text_location',
        'attachments',
        'attachment_types',
        'attachment_sizes',
        'response_requested',
        'response_deadline',
        'response_received',
        'response_date',
        'days_to_response',
        'legal_significance',
        'violation_type',
        'damage_relevance',
        'exhibit_number',
        'roi_reference',
        'deposition_reference',
        'mentioned_parties',
        'keywords',
        'privileged',
        'confidential',
        'produced_in_discovery',
        'production_bates',
        'objections',
        'authentication_method',
        'chain_of_custody',
        'metadata_preserved',
        'hash_value',
        'file_path',
        'backup_location',
        'notes',
        'review_status',
        'reviewed_by',
        'review_date',
        'flag_for_attorney',
        'action_required'
    ]
    
    # Create template rows with examples
    template_rows = [
        {
            'email_id': 'EM-001',
            'date_sent': '2020-09-15',
            'time_sent': '09:30:00',
            'date_received': '2020-09-15',
            'time_received': '09:31:00',
            'from_name': '[Complainant Name]',
            'from_email': '[complainant@email.com]',
            'from_title': '[Position Title]',
            'to_name': '[HR Director Name]',
            'to_email': '[hr.director@agency.gov]',
            'to_title': 'HR Director',
            'cc_names': '[Supervisor Name]',
            'cc_emails': '[supervisor@agency.gov]',
            'bcc_names': '',
            'bcc_emails': '',
            'subject': 'Request for Reasonable Accommodation - Telework',
            'thread_id': 'THR-001',
            'in_reply_to': '',
            'category': 'accommodation_request',
            'subcategory': 'initial_request',
            'key_content_summary': 'Initial request for telework accommodation due to disability, includes medical documentation',
            'full_text_location': 'exhibits/emails/EM-001_full.pdf',
            'attachments': 'Medical_Documentation_Sept2020.pdf',
            'attachment_types': 'PDF',
            'attachment_sizes': '2.3MB',
            'response_requested': 'Yes',
            'response_deadline': '2020-10-15',
            'response_received': 'No',
            'response_date': 'Never',
            'days_to_response': '1340',
            'legal_significance': 'CRITICAL - Start of 1,340-day violation',
            'violation_type': 'Failure to accommodate, failure to engage in interactive process',
            'damage_relevance': 'Primary evidence of discrimination',
            'exhibit_number': 'Exhibit A-1',
            'roi_reference': 'ROI Part 1, pages 26-27',
            'deposition_reference': '',
            'mentioned_parties': '[Complainant], [HR Director], [Supervisor]',
            'keywords': 'accommodation, telework, disability, medical',
            'privileged': 'No',
            'confidential': 'Yes - Medical',
            'produced_in_discovery': 'Yes',
            'production_bates': 'AGENCY-001234',
            'objections': 'None',
            'authentication_method': 'Email headers, metadata',
            'chain_of_custody': 'Preserved by agency IT',
            'metadata_preserved': 'Yes',
            'hash_value': '[SHA-256 hash]',
            'file_path': 'evidence/emails/2020/september/EM-001.msg',
            'backup_location': 'backup/emails/EM-001.msg',
            'notes': 'Never received any acknowledgment or response. This is the starting point of the 1,340-day violation.',
            'review_status': 'Complete',
            'reviewed_by': '[Attorney Name]',
            'review_date': '2024-11-15',
            'flag_for_attorney': 'Yes',
            'action_required': 'Lead with this in summary judgment motion'
        },
        # Add empty template rows for easy copying
        {col: '' for col in columns},
        {col: '' for col in columns},
        {col: '' for col in columns},
        {col: '' for col in columns}
    ]
    
    # Create CSV file
    filename = 'email_tracking_template_comprehensive.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(template_rows)
    
    # Create instructions file
    with open('email_tracking_instructions.md', 'w', encoding='utf-8') as f:
        f.write("# Email Tracking Template Instructions\n\n")
        f.write("## Purpose\n")
        f.write("This comprehensive email tracking system helps organize all email evidence for your case.\n\n")
        
        f.write("## Column Descriptions\n\n")
        f.write("### Identification Fields\n")
        f.write("- **email_id**: Unique identifier (e.g., EM-001, EM-002)\n")
        f.write("- **thread_id**: Groups related emails in a conversation\n")
        f.write("- **in_reply_to**: ID of email this responds to\n\n")
        
        f.write("### Temporal Fields\n")
        f.write("- **date_sent/time_sent**: When email was sent\n")
        f.write("- **date_received/time_received**: When received (from headers)\n")
        f.write("- **days_to_response**: Business days until response (if any)\n\n")
        
        f.write("### Party Information\n")
        f.write("- **from/to/cc/bcc**: Names, emails, and titles\n")
        f.write("- **mentioned_parties**: Anyone referenced in the email\n\n")
        
        f.write("### Content Classification\n")
        f.write("- **category**: Main type (accommodation_request, denial, retaliation, etc.)\n")
        f.write("- **subcategory**: Specific subtype\n")
        f.write("- **keywords**: Searchable terms\n\n")
        
        f.write("### Legal Analysis\n")
        f.write("- **legal_significance**: Why this email matters\n")
        f.write("- **violation_type**: Specific legal violations evidenced\n")
        f.write("- **damage_relevance**: How it supports damages\n\n")
        
        f.write("### Discovery & Evidence\n")
        f.write("- **exhibit_number**: Formal exhibit designation\n")
        f.write("- **roi_reference**: Where found in investigation\n")
        f.write("- **production_bates**: Discovery production numbers\n\n")
        
        f.write("### Technical/Preservation\n")
        f.write("- **metadata_preserved**: Yes/No\n")
        f.write("- **hash_value**: For authentication\n")
        f.write("- **file_path**: Where stored\n\n")
        
        f.write("### Review Tracking\n")
        f.write("- **review_status**: Not Started/In Progress/Complete\n")
        f.write("- **flag_for_attorney**: Priority items\n")
        f.write("- **action_required**: Next steps\n\n")
        
        f.write("## Best Practices\n")
        f.write("1. Use consistent date format (YYYY-MM-DD)\n")
        f.write("2. Preserve email metadata\n")
        f.write("3. Track every follow-up\n")
        f.write("4. Note response times carefully\n")
        f.write("5. Cross-reference with other evidence\n")
        f.write("6. Update regularly as case progresses\n")
    
    print(f"Created comprehensive email tracking template: {filename}")
    print("Created instructions: email_tracking_instructions.md")
    print("\nThis CSV file can be opened in Excel for easy editing and sorting.")
    print("Use filters to find emails by category, date, or legal significance.")

if __name__ == "__main__":
    create_comprehensive_email_template() 