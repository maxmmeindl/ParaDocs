#!/usr/bin/env python3
"""
Document Scanner for Timeline Events
Extracts dates and communication events from various document types
"""

import re
import json
from pathlib import Path
from datetime import datetime
import argparse
import PyPDF2
import docx
from collections import defaultdict

class DocumentTimelineScanner:
    """Scans documents to extract timeline events"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.extracted_events = []
        
        # Date patterns to search for
        self.date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # MM/DD/YYYY or MM-DD-YYYY
            r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',  # DD Month YYYY
            r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',  # Month DD, YYYY
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',  # YYYY-MM-DD
        ]
        
        # Keywords that indicate communication types
        self.event_keywords = {
            'accommodation_request': [
                'request.*accommodation', 'reasonable accommodation', 'ADA request',
                'disability accommodation', 'accommodation request', 'requesting accommodation'
            ],
            'denial': [
                'deny', 'denied', 'denying', 'denial', 'cannot approve', 'unable to grant',
                'request.*denied', 'accommodation.*denied', 'not approved'
            ],
            'medical': [
                'medical documentation', 'doctor.*note', 'physician.*statement',
                'medical evidence', 'health condition', 'medical certification'
            ],
            'meeting': [
                'meeting', 'conference', 'discussion', 'interactive process',
                'scheduled.*meet', 'meet.*discuss'
            ],
            'discipline': [
                'warning', 'written warning', 'discipline', 'disciplinary',
                'corrective action', 'performance improvement', 'termination'
            ],
            'eeo_activity': [
                'EEO complaint', 'filed.*complaint', 'discrimination complaint',
                'EEOC', 'Equal Employment', 'protected activity'
            ],
            'response': [
                'response to', 'reply to', 'regarding your', 'in response',
                'following up', 'as discussed'
            ]
        }
        
        # Subject line patterns
        self.subject_patterns = [
            r'Subject:\s*(.+?)(?:\n|$)',
            r'RE:\s*(.+?)(?:\n|$)',
            r'FW:\s*(.+?)(?:\n|$)',
            r'Regarding:\s*(.+?)(?:\n|$)'
        ]
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path):
        """Extract text from Word document"""
        try:
            doc = docx.Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
            return ""
    
    def extract_dates(self, text):
        """Extract dates from text"""
        dates_found = []
        
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1)
                try:
                    # Try to parse the date
                    parsed_date = self.parse_date(date_str)
                    if parsed_date:
                        dates_found.append({
                            'original': date_str,
                            'parsed': parsed_date,
                            'position': match.start()
                        })
                except:
                    continue
        
        return dates_found
    
    def parse_date(self, date_str):
        """Parse various date formats"""
        date_formats = [
            '%m/%d/%Y', '%m-%d-%Y', '%m/%d/%y', '%m-%d-%y',
            '%Y-%m-%d', '%Y/%m/%d',
            '%B %d, %Y', '%B %d %Y', '%d %B %Y',
            '%b %d, %Y', '%b %d %Y', '%d %b %Y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except:
                continue
        return None
    
    def identify_event_type(self, text_context):
        """Identify the type of event based on context"""
        text_lower = text_context.lower()
        
        for event_type, keywords in self.event_keywords.items():
            for keyword in keywords:
                if re.search(keyword, text_lower):
                    return event_type
        
        return 'other'
    
    def extract_subject(self, text):
        """Extract subject line from text"""
        for pattern in self.subject_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def extract_from_to(self, text):
        """Extract From and To information"""
        from_pattern = r'From:\s*(.+?)(?:\n|Sent:|$)'
        to_pattern = r'To:\s*(.+?)(?:\n|Subject:|$)'
        
        from_match = re.search(from_pattern, text, re.IGNORECASE | re.DOTALL)
        to_match = re.search(to_pattern, text, re.IGNORECASE | re.DOTALL)
        
        from_person = from_match.group(1).strip() if from_match else "Unknown"
        to_person = to_match.group(1).strip() if to_match else "Unknown"
        
        return from_person, to_person
    
    def extract_context(self, text, position, window=200):
        """Extract context around a date"""
        start = max(0, position - window)
        end = min(len(text), position + window)
        return text[start:end]
    
    def scan_document(self, file_path):
        """Scan a single document for timeline events"""
        print(f"\nScanning: {file_path.name}")
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            text = self.extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file type: {file_path.suffix}")
            return []
        
        if not text:
            return []
        
        # Extract dates
        dates = self.extract_dates(text)
        
        # Extract events for each date
        events = []
        for date_info in dates:
            context = self.extract_context(text, date_info['position'])
            
            # Extract event details
            event_type = self.identify_event_type(context)
            subject = self.extract_subject(context)
            from_person, to_person = self.extract_from_to(context)
            
            # Create event
            event = {
                'date': date_info['parsed'],
                'type': event_type,
                'subject': subject or f"Communication on {date_info['parsed']}",
                'from': from_person,
                'to': to_person,
                'description': context.replace('\n', ' ').strip()[:200] + "...",
                'keywords': self.extract_keywords(context),
                'documents': [file_path.name],
                'source_file': str(file_path),
                'response_time': None
            }
            
            events.append(event)
        
        return events
    
    def extract_keywords(self, text):
        """Extract relevant keywords from text"""
        keywords = []
        text_lower = text.lower()
        
        # Check for all event keywords
        for event_type, keyword_list in self.event_keywords.items():
            for keyword in keyword_list:
                if re.search(keyword, text_lower):
                    # Extract the actual matched phrase
                    match = re.search(keyword, text_lower)
                    if match:
                        keywords.append(match.group(0))
        
        # Remove duplicates and return
        return list(set(keywords))[:5]  # Limit to 5 keywords
    
    def scan_directory(self, directory_path):
        """Scan all documents in a directory"""
        directory = Path(directory_path)
        all_events = []
        
        # Scan all PDF and Word documents
        for pattern in ['*.pdf', '*.docx', '*.doc']:
            for file_path in directory.glob(pattern):
                events = self.scan_document(file_path)
                all_events.extend(events)
        
        # Sort by date
        all_events.sort(key=lambda x: x['date'])
        
        # Calculate response times
        self.calculate_response_times(all_events)
        
        return all_events
    
    def calculate_response_times(self, events):
        """Calculate response times between related events"""
        for i, event in enumerate(events):
            if i == 0:
                continue
            
            # Check if this might be a response to a previous event
            if event['type'] in ['denial', 'response', 'meeting']:
                # Look for related accommodation request
                for j in range(i-1, -1, -1):
                    prev_event = events[j]
                    if prev_event['type'] == 'accommodation_request':
                        # Calculate days between
                        date1 = datetime.strptime(prev_event['date'], '%Y-%m-%d')
                        date2 = datetime.strptime(event['date'], '%Y-%m-%d')
                        days_diff = (date2 - date1).days
                        event['response_time'] = days_diff
                        break
    
    def save_events(self, events, output_file):
        """Save extracted events to JSON file"""
        output_data = {
            'case_number': self.case_number,
            'scan_date': datetime.now().isoformat(),
            'total_events': len(events),
            'events': events
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nExtracted {len(events)} events saved to: {output_file}")
    
    def create_timeline_from_scan(self, events):
        """Create timeline using the extracted events"""
        from create_communication_timeline import CommunicationTimelineAnalyzer
        
        # Filter and clean events
        timeline_events = []
        for event in events:
            # Skip events without clear dates
            if event['date'] and event['date'] != 'Unknown':
                timeline_events.append(event)
        
        # Create timeline
        analyzer = CommunicationTimelineAnalyzer(self.case_number)
        timeline_data = analyzer.create_timeline(events=timeline_events)
        
        # Generate reports
        analyzer.generate_timeline_report(timeline_data)
        analyzer.generate_html_timeline(timeline_data)
        
        return timeline_data


def main():
    parser = argparse.ArgumentParser(description='Scan documents for timeline events')
    parser.add_argument('--directory', default='paradocs-agent/downloaded', 
                       help='Directory to scan for documents')
    parser.add_argument('--case', default='HS-FEMA-02430-2024', 
                       help='Case number')
    parser.add_argument('--output', default=None,
                       help='Output JSON file for extracted events')
    parser.add_argument('--timeline', action='store_true',
                       help='Generate timeline from extracted events')
    
    args = parser.parse_args()
    
    # Create scanner
    scanner = DocumentTimelineScanner(args.case)
    
    # Scan directory
    print(f"Scanning documents in: {args.directory}")
    events = scanner.scan_directory(args.directory)
    
    # Save events
    output_file = args.output or f"extracted_events_{args.case}.json"
    scanner.save_events(events, output_file)
    
    # Print summary
    print("\nEvent Summary:")
    event_types = defaultdict(int)
    for event in events:
        event_types[event['type']] += 1
    
    for event_type, count in event_types.items():
        print(f"  - {event_type}: {count}")
    
    # Generate timeline if requested
    if args.timeline and events:
        print("\nGenerating timeline from extracted events...")
        scanner.create_timeline_from_scan(events)
        print("Timeline generated successfully!")
    
    # Print sample events
    if events:
        print("\nSample extracted events:")
        for event in events[:3]:
            print(f"\n- Date: {event['date']}")
            print(f"  Type: {event['type']}")
            print(f"  Subject: {event['subject']}")
            print(f"  From: {event['from']} → To: {event['to']}")


if __name__ == "__main__":
    main() 