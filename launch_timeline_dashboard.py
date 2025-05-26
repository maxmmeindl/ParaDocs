import webbrowser
import os
import sys

def launch_timeline_dashboard():
    """Launch the Timeline-Enhanced ParaDocs Dashboard in the default browser."""
    # Get the absolute path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, "paradocs_master_timeline_enhanced.html")
    
    if not os.path.exists(html_file):
        print("❌ Error: paradocs_master_timeline_enhanced.html not found!")
        print(f"Expected location: {html_file}")
        return False
    
    # Convert to file:// URL for browser
    file_url = f"file:///{html_file.replace(os.sep, '/')}"
    
    print("🚀 Launching ParaDocs Timeline-Enhanced Dashboard...")
    print(f"📂 Opening: {html_file}")
    print(f"🌐 URL: {file_url}")
    
    # Open in default browser
    webbrowser.open(file_url)
    
    print("\n✅ Timeline-Enhanced Dashboard launched successfully!")
    print("\nThis dashboard includes:")
    print("• Complete EEO investigation timeline (2018-2025)")
    print("• 15 documented events with full details")
    print("• 30 total violations across multiple statutes")
    print("• Key actors analysis with violation counts")
    print("• Interactive search and filtering")
    print("• Direct quotes from communications")
    print("• Processing delay tracking (up to 1,195 days)")
    print("\nTimeline data files:")
    print("• eeo_timeline_events.csv - Spreadsheet format")
    print("• eeo_timeline_enhanced.json - Complete JSON data")
    print("• eeo_timeline_comprehensive_report.json - Full analysis")
    
    return True

if __name__ == "__main__":
    launch_timeline_dashboard() 