#!/usr/bin/env python3
"""
Communication Timeline Template
Shows how to add your actual case communications to the timeline
"""

from create_communication_timeline import CommunicationTimelineAnalyzer

# Example: How to create a timeline with your actual communications
def create_custom_timeline():
    """
    Replace the sample events below with your actual case communications
    """
    
    # Your actual communications - add each email, letter, meeting, etc.
    my_communications = [
        {
            'date': '2023-01-15',  # Format: YYYY-MM-DD
            'type': 'accommodation_request',  # Types: accommodation_request, denial, meeting, discipline, eeo_activity, medical, deadline
            'subject': 'Initial Request for Reasonable Accommodation',
            'from': 'John Smith (Employee)',
            'to': 'Jane Doe (Supervisor)',
            'description': 'Requested telework accommodation due to disability',
            'keywords': ['accommodation', 'telework', 'disability', 'ADA'],  # Add relevant keywords for searching
            'documents': ['Email_2023-01-15_Accommodation_Request.pdf'],  # List related documents
            'response_time': None  # Leave None for initial requests, add days for responses
        },
        {
            'date': '2023-01-20',
            'type': 'medical',
            'subject': 'Medical Documentation Submitted',
            'from': 'John Smith',
            'to': 'HR Department',
            'description': 'Submitted doctor\'s note supporting accommodation request',
            'keywords': ['medical', 'doctor', 'documentation'],
            'documents': ['Medical_Documentation_2023-01-20.pdf'],
            'response_time': 5  # 5 days after initial request
        },
        {
            'date': '2023-02-28',
            'type': 'denial',
            'subject': 'Accommodation Request Denied',
            'from': 'HR Department',
            'to': 'John Smith',
            'description': 'Denied accommodation without interactive process or undue hardship analysis',
            'keywords': ['denial', 'accommodation', 'denied'],
            'documents': ['Denial_Letter_2023-02-28.pdf'],
            'response_time': 44  # 44 days after initial request - VIOLATION!
        },
        # Add more communications here...
    ]
    
    # Create analyzer
    analyzer = CommunicationTimelineAnalyzer('YOUR-CASE-NUMBER-HERE')
    
    # Generate timeline with your communications
    timeline_data = analyzer.create_timeline(events=my_communications)
    
    # Generate reports
    analyzer.generate_timeline_report(timeline_data)
    analyzer.generate_html_timeline(timeline_data)
    
    # Search for specific keywords
    accommodation_events = analyzer.search_timeline(timeline_data, ['accommodation'])
    print(f"\nFound {len(accommodation_events)} accommodation-related communications")
    
    denial_events = analyzer.search_timeline(timeline_data, ['denial', 'denied'])
    print(f"Found {len(denial_events)} denial-related communications")
    
    return timeline_data


# Template for different types of communications
COMMUNICATION_TEMPLATES = {
    'accommodation_request': {
        'date': 'YYYY-MM-DD',
        'type': 'accommodation_request',
        'subject': 'Request for [Specific Accommodation]',
        'from': 'Employee Name',
        'to': 'Supervisor/HR',
        'description': 'Detailed description of what was requested',
        'keywords': ['accommodation', 'ADA', 'disability'],
        'documents': ['Document_Name.pdf'],
        'response_time': None
    },
    'meeting': {
        'date': 'YYYY-MM-DD',
        'type': 'meeting',
        'subject': 'Interactive Process Meeting',
        'from': 'HR/Management',
        'to': 'Employee',
        'description': 'Discussion of accommodation options',
        'keywords': ['meeting', 'interactive process'],
        'documents': ['Meeting_Notes.pdf'],
        'response_time': None  # Days from initial request
    },
    'denial': {
        'date': 'YYYY-MM-DD',
        'type': 'denial',
        'subject': 'Denial of Accommodation',
        'from': 'Management/HR',
        'to': 'Employee',
        'description': 'Reason given for denial',
        'keywords': ['denial', 'denied', 'accommodation'],
        'documents': ['Denial_Letter.pdf'],
        'response_time': None  # Days from request - critical if >30
    },
    'discipline': {
        'date': 'YYYY-MM-DD',
        'type': 'discipline',
        'subject': 'Disciplinary Action',
        'from': 'Supervisor',
        'to': 'Employee',
        'description': 'Type of discipline and stated reason',
        'keywords': ['discipline', 'warning', 'termination'],
        'documents': ['Disciplinary_Notice.pdf'],
        'response_time': None
    },
    'eeo_activity': {
        'date': 'YYYY-MM-DD',
        'type': 'eeo_activity',
        'subject': 'EEO Complaint Filed',
        'from': 'Employee',
        'to': 'EEO Office',
        'description': 'Filed complaint alleging discrimination',
        'keywords': ['EEO', 'complaint', 'discrimination'],
        'documents': ['EEO_Complaint.pdf'],
        'response_time': None
    }
}


# Tips for building your timeline
TIMELINE_TIPS = """
Tips for Building Your Communication Timeline:

1. **Gather All Communications**: 
   - Emails (with timestamps)
   - Letters (dated)
   - Meeting notes/minutes
   - Phone call logs
   - Text messages
   - Any written documentation

2. **Key Dates to Include**:
   - Initial accommodation request
   - Medical documentation submissions
   - Interactive process meetings (or lack thereof)
   - Responses from management
   - Disciplinary actions
   - EEO complaint filing
   - Any adverse actions after protected activity

3. **Calculate Response Times**:
   - Count days between request and response
   - Flag any responses over 30 days as violations
   - Note periods of silence/no response

4. **Keywords for Cross-Reference**:
   - Include specific accommodation terms
   - Medical conditions mentioned
   - Legal terms used
   - Names of key people involved

5. **Document Everything**:
   - List all supporting documents
   - Note missing documentation
   - Identify communications referenced but not provided

6. **Look for Patterns**:
   - Delays after accommodation requests
   - Discipline after protected activity
   - Changes in treatment over time
   - Inconsistent responses
"""


if __name__ == "__main__":
    print("Communication Timeline Template")
    print("=" * 50)
    print(TIMELINE_TIPS)
    print("\nTo use this template:")
    print("1. Edit the 'my_communications' list with your actual case communications")
    print("2. Run: python communication_timeline_template.py")
    print("3. Review the generated timeline and reports")
    print("\nRefer to COMMUNICATION_TEMPLATES above for examples of each type") 