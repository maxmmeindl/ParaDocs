import webbrowser
import os
import sys

def launch_paradocs():
    """Launch the ParaDocs Enhanced website in the default browser."""
    # Get the absolute path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, "paradocs-enhanced.html")
    
    if not os.path.exists(html_file):
        print("❌ Error: paradocs-enhanced.html not found!")
        print(f"Expected location: {html_file}")
        return False
    
    # Convert to file:// URL for browser
    file_url = f"file:///{html_file.replace(os.sep, '/')}"
    
    print("🚀 Launching ParaDocs Enhanced Case Management System...")
    print(f"📂 Opening: {html_file}")
    print(f"🌐 URL: {file_url}")
    
    # Open in default browser
    webbrowser.open(file_url)
    
    print("\n✅ Website launched successfully!")
    print("\nIf the browser didn't open automatically:")
    print(f"1. Copy this path: {html_file}")
    print("2. Open your browser")
    print("3. Press Ctrl+O (or Cmd+O on Mac)")
    print("4. Paste the path and press Enter")
    
    return True

if __name__ == "__main__":
    launch_paradocs() 