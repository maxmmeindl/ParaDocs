#!/usr/bin/env python3
"""
Communication Timeline Analyzer
Creates searchable timeline of all case communications with keyword cross-referencing
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import argparse

class CommunicationTimelineAnalyzer:
    """Analyzes and creates timeline of all case communications"""
    
    def __init__(self, case_number="HS-FEMA-02430-2024"):
        self.case_number = case_number
        self.base_path = Path(".")
        self.timeline_file = self.base_path / f"communication_timeline_{case_number}.json"
        self.timeline_report = self.base_path / f"communication_timeline_{case_number}.md"
        self.timeline_html = self.base_path / f"communication_timeline_{case_number}.html"
        
        # Key event categories
        self.event_categories = {
            'accommodation_request': {
                'keywords': ['accommodation', 'reasonable accommodation', 'ADA', 'disability', 'medical'],
                'color': '#FF6B6B',
                'importance': 'critical'
            },
            'denial': {
                'keywords': ['denied', 'deny', 'rejection', 'cannot', 'unable', 'refuse'],
                'color': '#845EC2',
                'importance': 'critical'
            },
            'medical': {
                'keywords': ['doctor', 'physician', 'medical', 'health', 'diagnosis', 'treatment'],
                'color': '#4E8397',
                'importance': 'high'
            },
            'meeting': {
                'keywords': ['meeting', 'discussion', 'conference', 'interactive process'],
                'color': '#00C9A7',
                'importance': 'high'
            },
            'discipline': {
                'keywords': ['warning', 'discipline', 'corrective', 'performance', 'termination'],
                'color': '#C34A36',
                'importance': 'critical'
            },
            'eeo_activity': {
                'keywords': ['EEO', 'complaint', 'discrimination', 'retaliation', 'protected'],
                'color': '#FF8066',
                'importance': 'critical'
            },
            'deadline': {
                'keywords': ['deadline', 'due date', 'must', 'required by', 'within days'],
                'color': '#4FFBDF',
                'importance': 'high'
            }
        }
        
        # Sample timeline events (would be populated from actual documents)
        self.sample_events = [
            {
                'date': '2023-01-15',
                'type': 'accommodation_request',
                'subject': 'Initial Accommodation Request',
                'from': 'Employee',
                'to': 'Supervisor',
                'description': 'Requested reasonable accommodation for disability',
                'keywords': ['accommodation', 'disability'],
                'documents': ['Email_2023-01-15.pdf'],
                'response_time': None
            },
            {
                'date': '2023-02-01',
                'type': 'meeting',
                'subject': 'Interactive Process Meeting',
                'from': 'HR',
                'to': 'Employee',
                'description': 'Scheduled interactive process meeting',
                'keywords': ['meeting', 'interactive process'],
                'documents': ['Meeting_Notice_2023-02-01.pdf'],
                'response_time': 17  # days from request
            },
            {
                'date': '2023-02-15',
                'type': 'denial',
                'subject': 'Accommodation Denial',
                'from': 'Management',
                'to': 'Employee',
                'description': 'Denied accommodation request without undue hardship analysis',
                'keywords': ['denied', 'accommodation'],
                'documents': ['Denial_Letter_2023-02-15.pdf'],
                'response_time': 31  # days from request
            },
            {
                'date': '2023-03-01',
                'type': 'discipline',
                'subject': 'Performance Warning',
                'from': 'Supervisor',
                'to': 'Employee',
                'description': 'Written warning for performance issues',
                'keywords': ['warning', 'performance'],
                'documents': ['Warning_2023-03-01.pdf'],
                'response_time': None
            },
            {
                'date': '2023-03-15',
                'type': 'eeo_activity',
                'subject': 'EEO Complaint Filed',
                'from': 'Employee',
                'to': 'EEO Office',
                'description': 'Filed formal EEO complaint',
                'keywords': ['EEO', 'complaint', 'discrimination'],
                'documents': ['EEO_Complaint_2023-03-15.pdf'],
                'response_time': None
            }
        ]
    
    def create_timeline(self, events=None):
        """Create timeline from events or use sample data"""
        if events is None:
            events = self.sample_events
        
        # Sort events by date
        sorted_events = sorted(events, key=lambda x: x['date'])
        
        # Calculate delays and patterns
        timeline_data = {
            'case_number': self.case_number,
            'created': datetime.now().isoformat(),
            'events': sorted_events,
            'statistics': self._calculate_statistics(sorted_events),
            'patterns': self._identify_patterns(sorted_events),
            'delays': self._calculate_delays(sorted_events)
        }
        
        # Save timeline data
        with open(self.timeline_file, 'w') as f:
            json.dump(timeline_data, f, indent=2)
        
        return timeline_data
    
    def _calculate_statistics(self, events):
        """Calculate timeline statistics"""
        stats = {
            'total_events': len(events),
            'event_types': defaultdict(int),
            'response_times': [],
            'communication_gaps': []
        }
        
        for event in events:
            stats['event_types'][event['type']] += 1
            if event.get('response_time'):
                stats['response_times'].append(event['response_time'])
        
        # Calculate gaps between events
        for i in range(1, len(events)):
            prev_date = datetime.strptime(events[i-1]['date'], '%Y-%m-%d')
            curr_date = datetime.strptime(events[i]['date'], '%Y-%m-%d')
            gap = (curr_date - prev_date).days
            stats['communication_gaps'].append(gap)
        
        if stats['response_times']:
            stats['avg_response_time'] = sum(stats['response_times']) / len(stats['response_times'])
        
        return dict(stats)
    
    def _identify_patterns(self, events):
        """Identify patterns in communications"""
        patterns = []
        
        # Pattern 1: Retaliation timing
        eeo_date = None
        for event in events:
            if event['type'] == 'eeo_activity':
                eeo_date = datetime.strptime(event['date'], '%Y-%m-%d')
                break
        
        if eeo_date:
            post_eeo_discipline = []
            for event in events:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                if event_date > eeo_date and event['type'] == 'discipline':
                    days_after = (event_date - eeo_date).days
                    post_eeo_discipline.append({
                        'event': event['subject'],
                        'days_after_eeo': days_after
                    })
            
            if post_eeo_discipline:
                patterns.append({
                    'type': 'potential_retaliation',
                    'description': 'Disciplinary actions after EEO activity',
                    'events': post_eeo_discipline
                })
        
        # Pattern 2: Delayed responses
        delayed_responses = []
        for event in events:
            response_time = event.get('response_time')
            if response_time and response_time > 30:
                delayed_responses.append({
                    'event': event['subject'],
                    'delay_days': response_time
                })
        
        if delayed_responses:
            patterns.append({
                'type': 'delayed_responses',
                'description': 'Responses exceeding 30 days',
                'events': delayed_responses
            })
        
        return patterns
    
    def _calculate_delays(self, events):
        """Calculate significant delays"""
        delays = []
        
        # Check accommodation request delays
        accommodation_requests = [e for e in events if e['type'] == 'accommodation_request']
        for request in accommodation_requests:
            request_date = datetime.strptime(request['date'], '%Y-%m-%d')
            
            # Find response
            response = None
            for event in events:
                if event['date'] > request['date'] and any(kw in event.get('keywords', []) for kw in ['denied', 'approved', 'accommodation']):
                    response = event
                    break
            
            if response:
                response_date = datetime.strptime(response['date'], '%Y-%m-%d')
                delay_days = (response_date - request_date).days
                delays.append({
                    'request': request['subject'],
                    'response': response['subject'],
                    'delay_days': delay_days,
                    'violation': delay_days > 30
                })
        
        return delays
    
    def search_timeline(self, timeline_data, keywords):
        """Search timeline for specific keywords"""
        results = []
        
        for event in timeline_data['events']:
            # Check if any keyword matches
            event_text = f"{event['subject']} {event['description']} {' '.join(event.get('keywords', []))}"
            if any(keyword.lower() in event_text.lower() for keyword in keywords):
                results.append(event)
        
        return results
    
    def generate_timeline_report(self, timeline_data):
        """Generate markdown report of timeline"""
        print("\nGenerating timeline report...")
        
        with open(self.timeline_report, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Communication Timeline Analysis\n")
            f.write(f"## Case: {self.case_number}\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary Statistics
            f.write("## Summary Statistics\n\n")
            stats = timeline_data['statistics']
            f.write(f"- **Total Communications**: {stats['total_events']}\n")
            f.write(f"- **Average Response Time**: {stats.get('avg_response_time', 'N/A'):.1f} days\n")
            f.write(f"- **Event Types**:\n")
            for event_type, count in stats['event_types'].items():
                f.write(f"  - {event_type.replace('_', ' ').title()}: {count}\n")
            f.write("\n")
            
            # Identified Patterns
            f.write("## Identified Patterns\n\n")
            for pattern in timeline_data['patterns']:
                f.write(f"### {pattern['type'].replace('_', ' ').title()}\n")
                f.write(f"**Description**: {pattern['description']}\n\n")
                for event in pattern['events']:
                    f.write(f"- {event}\n")
                f.write("\n")
            
            # Delays Analysis
            f.write("## Critical Delays\n\n")
            for delay in timeline_data['delays']:
                f.write(f"- **{delay['request']}** → **{delay['response']}**\n")
                f.write(f"  - Delay: {delay['delay_days']} days")
                if delay['violation']:
                    f.write(" ⚠️ **VIOLATION**")
                f.write("\n\n")
            
            # Chronological Timeline
            f.write("## Chronological Timeline\n\n")
            f.write("| Date | Type | Subject | From → To | Response Time | Keywords |\n")
            f.write("|------|------|---------|-----------|---------------|----------|\n")
            
            for event in timeline_data['events']:
                response_time = f"{event.get('response_time', '-')} days" if event.get('response_time') else '-'
                keywords = ', '.join(event.get('keywords', []))
                f.write(f"| {event['date']} | {event['type']} | {event['subject']} | ")
                f.write(f"{event['from']} → {event['to']} | {response_time} | {keywords} |\n")
            
            # Legal Implications
            f.write("\n## Legal Implications\n\n")
            
            # Check for interactive process violations
            accommodation_events = [e for e in timeline_data['events'] if 'accommodation' in e.get('keywords', [])]
            if accommodation_events:
                f.write("### Interactive Process Analysis\n")
                f.write("- Total accommodation-related communications: {}\n".format(len(accommodation_events)))
                
                # Check for delays
                delays = [d for d in timeline_data['delays'] if d['violation']]
                if delays:
                    f.write("- **Violations Found**: {} instances of delayed response (>30 days)\n".format(len(delays)))
                    f.write("- **Legal Impact**: Failure to engage in timely interactive process (29 CFR 1630.2(o)(3))\n\n")
            
            # Check for retaliation
            retaliation_patterns = [p for p in timeline_data['patterns'] if p['type'] == 'potential_retaliation']
            if retaliation_patterns:
                f.write("### Potential Retaliation\n")
                f.write("- **Pattern Detected**: Adverse actions following protected EEO activity\n")
                f.write("- **Legal Impact**: Prima facie retaliation case\n\n")
            
            # Visual Timeline Recommendation
            f.write("## Visual Timeline\n\n")
            f.write("```\n")
            
            # Create ASCII timeline
            events = timeline_data['events']
            if events:
                start_date = datetime.strptime(events[0]['date'], '%Y-%m-%d')
                end_date = datetime.strptime(events[-1]['date'], '%Y-%m-%d')
                total_days = (end_date - start_date).days
                
                for event in events:
                    event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                    position = int(((event_date - start_date).days / total_days) * 50) if total_days > 0 else 0
                    
                    # Create timeline bar
                    bar = ['-'] * 50
                    if 0 <= position < 50:
                        bar[position] = '|'
                        
                        # Mark critical events
                        if event['type'] in ['accommodation_request', 'denial', 'eeo_activity']:
                            bar[position] = '!'
                    
                    f.write(f"{event['date']} {''.join(bar)} {event['type'][:15]}\n")
            
            f.write("```\n\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            f.write("1. **Document Review**: Cross-reference all communications with documents listed\n")
            f.write("2. **Pattern Evidence**: Use identified patterns in legal arguments\n")
            f.write("3. **Timeline Exhibit**: Create visual timeline for hearing/ADR\n")
            f.write("4. **Discovery Focus**: Request missing communications during identified gaps\n")
            
            f.write("\n---\n")
            f.write("*Use keyword search to find specific topics across all communications*\n")
        
        print(f"Timeline report saved to: {self.timeline_report}")
    
    def generate_html_timeline(self, timeline_data):
        """Generate interactive HTML timeline"""
        print("\nGenerating interactive HTML timeline...")
        
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Communication Timeline - {case}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .timeline {{ position: relative; max-width: 1200px; margin: 0 auto; }}
        .timeline::after {{ content: ''; position: absolute; width: 6px; background-color: #ddd; top: 0; bottom: 0; left: 50%; margin-left: -3px; }}
        .container {{ padding: 10px 40px; position: relative; background-color: inherit; width: 50%; }}
        .container::after {{ content: ''; position: absolute; width: 25px; height: 25px; right: -17px; background-color: white; border: 4px solid #FF9F55; top: 15px; border-radius: 50%; z-index: 1; }}
        .left {{ left: 0; }}
        .right {{ left: 50%; }}
        .left::before {{ content: " "; height: 0; position: absolute; top: 22px; width: 0; z-index: 1; right: 30px; border: medium solid #ddd; border-width: 10px 0 10px 10px; border-color: transparent transparent transparent #ddd; }}
        .right::before {{ content: " "; height: 0; position: absolute; top: 22px; width: 0; z-index: 1; left: 30px; border: medium solid #ddd; border-width: 10px 10px 10px 0; border-color: transparent #ddd transparent transparent; }}
        .right::after {{ left: -16px; }}
        .content {{ padding: 20px 30px; background-color: white; position: relative; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .accommodation_request {{ border-left: 5px solid #FF6B6B; }}
        .denial {{ border-left: 5px solid #845EC2; }}
        .meeting {{ border-left: 5px solid #00C9A7; }}
        .discipline {{ border-left: 5px solid #C34A36; }}
        .eeo_activity {{ border-left: 5px solid #FF8066; }}
        .search-box {{ margin: 20px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
        .search-box input {{ width: 300px; padding: 5px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ background: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center; }}
        .violation {{ color: red; font-weight: bold; }}
        h2 {{ color: #333; }}
        .date {{ color: #666; font-weight: bold; }}
        .keywords {{ color: #999; font-size: 0.9em; font-style: italic; }}
    </style>
    <script>
        function searchTimeline() {{
            var input = document.getElementById('searchInput').value.toLowerCase();
            var events = document.getElementsByClassName('container');
            
            for (var i = 0; i < events.length; i++) {{
                var content = events[i].textContent.toLowerCase();
                if (content.includes(input)) {{
                    events[i].style.display = 'block';
                }} else {{
                    events[i].style.display = 'none';
                }}
            }}
        }}
    </script>
</head>
<body>
    <h1>Communication Timeline Analysis</h1>
    <h2>Case: {case}</h2>
    
    <div class="search-box">
        <label>Search Timeline: </label>
        <input type="text" id="searchInput" onkeyup="searchTimeline()" placeholder="Enter keywords...">
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h3>Total Events</h3>
            <p>{total_events}</p>
        </div>
        <div class="stat-box">
            <h3>Average Response Time</h3>
            <p>{avg_response} days</p>
        </div>
        <div class="stat-box">
            <h3>Critical Delays</h3>
            <p class="violation">{violations}</p>
        </div>
    </div>
    
    <div class="timeline">
        {timeline_events}
    </div>
</body>
</html>
        """
        
        # Generate timeline events HTML
        timeline_events = ""
        for i, event in enumerate(timeline_data['events']):
            side = "left" if i % 2 == 0 else "right"
            
            event_html = f"""
        <div class="container {side}">
            <div class="content {event['type']}">
                <p class="date">{event['date']}</p>
                <h3>{event['subject']}</h3>
                <p><strong>{event['from']}</strong> → <strong>{event['to']}</strong></p>
                <p>{event['description']}</p>
                {'<p class="violation">Response Time: ' + str(event.get('response_time', '')) + ' days</p>' if event.get('response_time') and event.get('response_time') > 30 else ''}
                <p class="keywords">Keywords: {', '.join(event.get('keywords', []))}</p>
            </div>
        </div>
            """
            timeline_events += event_html
        
        # Calculate statistics
        stats = timeline_data['statistics']
        violations = len([d for d in timeline_data['delays'] if d.get('violation', False)])
        
        # Fill in the template
        html_filled = html_content.format(
            case=self.case_number,
            total_events=stats['total_events'],
            avg_response=f"{stats.get('avg_response_time', 0):.1f}",
            violations=violations,
            timeline_events=timeline_events
        )
        
        # Save HTML file
        with open(self.timeline_html, 'w', encoding='utf-8') as f:
            f.write(html_filled)
        
        print(f"Interactive HTML timeline saved to: {self.timeline_html}")


def main():
    parser = argparse.ArgumentParser(description='Create and analyze communication timeline')
    parser.add_argument('--case', default='HS-FEMA-02430-2024', help='Case number')
    parser.add_argument('--search', nargs='+', help='Search timeline for keywords')
    parser.add_argument('--format', choices=['md', 'html', 'both'], default='both', 
                       help='Output format for timeline')
    
    args = parser.parse_args()
    
    analyzer = CommunicationTimelineAnalyzer(args.case)
    
    # Create timeline
    timeline_data = analyzer.create_timeline()
    print(f"\nTimeline created with {len(timeline_data['events'])} events")
    
    # Search if requested
    if args.search:
        print(f"\nSearching for: {' '.join(args.search)}")
        results = analyzer.search_timeline(timeline_data, args.search)
        print(f"Found {len(results)} matching events:")
        for event in results:
            print(f"  - {event['date']}: {event['subject']}")
    
    # Generate reports
    if args.format in ['md', 'both']:
        analyzer.generate_timeline_report(timeline_data)
    
    if args.format in ['html', 'both']:
        analyzer.generate_html_timeline(timeline_data)
    
    print(f"\nTimeline analysis complete!")
    print(f"- JSON data: {analyzer.timeline_file}")
    if args.format in ['md', 'both']:
        print(f"- Markdown report: {analyzer.timeline_report}")
    if args.format in ['html', 'both']:
        print(f"- Interactive HTML: {analyzer.timeline_html}")
    
    # Print key findings
    print("\nKey Findings:")
    print(f"- Identified {len(timeline_data['patterns'])} concerning patterns")
    print(f"- Found {len(timeline_data['delays'])} significant delays")
    violations = [d for d in timeline_data['delays'] if d.get('violation', False)]
    if violations:
        print(f"- ⚠️  {len(violations)} delays exceed legal requirements")


if __name__ == "__main__":
    main() 