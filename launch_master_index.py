import webbrowser
import os
import sys

def launch_master_index():
    """Launch the ParaDocs Master Index in the default browser."""
    # Get the absolute path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, "MASTER_INDEX.html")
    
    if not os.path.exists(html_file):
        print("❌ Error: MASTER_INDEX.html not found!")
        print(f"Expected location: {html_file}")
        return False
    
    # Convert to file:// URL for browser
    file_url = f"file:///{html_file.replace(os.sep, '/')}"
    
    print("🚀 Launching ParaDocs Master Index...")
    print(f"📂 Opening: {html_file}")
    print(f"🌐 URL: {file_url}")
    
    # Open in default browser
    webbrowser.open(file_url)
    
    print("\n✅ Master Index launched successfully!")
    print("\n🏠 This is your main hub featuring:")
    print("• $2.27M Total Damages calculated")
    print("• 1,340 Days of violations (645% over limit)")
    print("• 8 Federal violations documented")
    print("• 24+ Analysis tools integrated")
    print("\n📊 Interactive Visualizations:")
    print("• Complete Interactive Timeline")
    print("• Legal Timeline Exhibit")
    print("• Complete Email Index")
    print("\n🔗 Quick Access to:")
    print("• Comprehensive EEO Investigation")
    print("• Timeline-Enhanced Dashboard")
    print("• All data files and evidence")
    print("\n🔍 Use the search box to find any document or information!")
    
    return True

if __name__ == "__main__":
    launch_master_index() 