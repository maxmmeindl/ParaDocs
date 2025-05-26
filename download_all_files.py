import os
import requests
import time
from urllib.parse import quote

# GitHub repository details
OWNER = "maxmmeindl"
REPO = "ParaDocs"
BRANCH = "main"

# Get list of files in root directory
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents?ref={BRANCH}"

# File extensions we want to download
target_extensions = {'.pdf', '.docx', '.xlsx', '.md', '.doc', '.eml', '.csv', '.png', '.jpg'}

def download_file(filename, download_url, local_path):
    """Download a file from GitHub."""
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  Error downloading {filename}: {str(e)}")
        return False

def main():
    # Create directory for new downloads
    new_downloads_dir = "downloaded_root"
    os.makedirs(new_downloads_dir, exist_ok=True)
    
    print("Fetching file list from GitHub root directory...")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        items = response.json()
    except Exception as e:
        print(f"Error fetching repository contents: {str(e)}")
        return
    
    # Filter for files with target extensions
    files_to_download = []
    for item in items:
        if item['type'] == 'file':
            name = item['name']
            ext = os.path.splitext(name.lower())[1]
            if ext in target_extensions or name.lower() == 'license' or name.lower() == 'readme.md':
                files_to_download.append({
                    'name': name,
                    'download_url': item['download_url']
                })
    
    print(f"\nFound {len(files_to_download)} files to download from root directory")
    
    # Check existing downloads to avoid duplicates
    existing_files = set()
    if os.path.exists("downloaded"):
        existing_files.update(os.listdir("downloaded"))
    if os.path.exists("downloaded/archive"):
        existing_files.update(os.listdir("downloaded/archive"))
    
    # Download files
    downloaded_count = 0
    skipped_count = 0
    
    for i, file_info in enumerate(files_to_download, 1):
        filename = file_info['name']
        
        # Skip if already downloaded
        if filename in existing_files or filename.replace('%20', ' ') in existing_files:
            print(f"[{i}/{len(files_to_download)}] Skipping {filename} (already exists)")
            skipped_count += 1
            continue
        
        local_path = os.path.join(new_downloads_dir, filename)
        print(f"[{i}/{len(files_to_download)}] Downloading {filename}...")
        
        if download_file(filename, file_info['download_url'], local_path):
            downloaded_count += 1
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    print(f"\n✅ Download complete!")
    print(f"   - Downloaded: {downloaded_count} files")
    print(f"   - Skipped (already exist): {skipped_count} files")
    print(f"   - Files saved to: {new_downloads_dir}/")

if __name__ == "__main__":
    main() 