import webbrowser
import os
import sys

def launch_comprehensive_investigation():
    """Launch the Comprehensive EEO Investigation Dashboard in the default browser."""
    # Get the absolute path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, "paradocs_comprehensive_eeo_investigation.html")
    
    if not os.path.exists(html_file):
        print("❌ Error: paradocs_comprehensive_eeo_investigation.html not found!")
        print(f"Expected location: {html_file}")
        return False
    
    # Convert to file:// URL for browser
    file_url = f"file:///{html_file.replace(os.sep, '/')}"
    
    print("🚀 Launching ParaDocs Comprehensive EEO Investigation Dashboard...")
    print(f"📂 Opening: {html_file}")
    print(f"🌐 URL: {file_url}")
    
    # Open in default browser
    webbrowser.open(file_url)
    
    print("\n✅ Comprehensive EEO Investigation Dashboard launched!")
    print("\n📊 Dashboard includes:")
    print("• 30+ timeline events from Aug 2018 to Jan 2025")
    print("• Investigation questions for 13 key individuals")
    print("• 76 total violations documented")
    print("• Maximum delay: 1,275 days (2,733% over requirement)")
    print("• HIPAA breach documentation")
    print("• $15,000 Hurricane Beryl damage")
    print("• 38 months of successful remote work")
    print("\n📁 Supporting data files:")
    print("• eeo_comprehensive_investigation.json - Complete case data")
    print("• eeo_comprehensive_timeline.csv - All timeline events")
    print("• eeo_investigation_questions.csv - Interview questions")
    print("\n🔍 Key patterns identified:")
    print("• Systematic RA processing delays")
    print("• Documentation rejection pattern")
    print("• Leadership inaction (Traci Brasher)")
    print("• Age-based discrimination")
    print("• Retaliatory termination (17 days after EEO filing)")
    
    return True

if __name__ == "__main__":
    launch_comprehensive_investigation() 