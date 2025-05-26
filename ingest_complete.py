import os
import requests
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import mammoth
from langchain.schema import Document

load_dotenv()

OWNER = "maxmmeindl"
REPO = "ParaDocs"
BRANCH = "main"

def categorize_document(filename):
    """Enhanced categorization based on filename patterns."""
    filename_lower = filename.lower()
    
    categories = {
        'FMLA_Documents': ['fmla', 'family medical leave', 'wh-380', 'wh-381', 'wh-382'],
        'RA_Documents': ['reasonable accommodation', ' ra ', 'ra.', 'ra_', 'rar0', '256-0-1', '256-0-2'],
        'EEOC_Complaints': ['eeoc', 'complaint', 'eeo ', 'eeo_', 'eeo.', 'hs-fema-02430'],
        'OSC_Documents': ['osc', 'office of special counsel', 'ma-20-1288'],
        'Email_Communications': ['.eml', 'email', 'mail items'],
        'Medical_Records': ['medical', 'health', 'doctor', 'va medical', 'heart condition'],
        'Policy_Documents': ['policy', 'directive', 'manual', 'fm-', 'fd_', 'instruction'],
        'Forms_and_Tables': ['form', 'table b-', 'worksheet'],
        'Legal_Documents': ['affidavit', 'rebuttal', 'interrogator', 'legal', 'attorney'],
        'Telework_Documents': ['telework', 'remote work'],
        'Training_Documents': ['training', 'staff resources'],
        'FOIA_Documents': ['foia', 'freedom of information'],
        'Financial_Documents': ['loan', 'eft', 'pslf', 'payment'],
        'ROI_Documents': ['roi', 'report of investigation'],
        'Letters_Correspondence': ['letter', 'correspondence', 'memo'],
        'FY_Reports': ['fy 2021', 'fy 2024', 'fiscal year'],
        'ADR_Documents': ['adr', 'mediation', 'alternative dispute'],
        'VA_Documents': ['va ', 'veteran', 'va medical'],
        'Date_Stamped': ['2017-', '2018-', '2019-', '2020-', '2021-', '2022-', '2024-', '2025-'],
        'Miscellaneous': []
    }
    
    # Check each category
    for category, patterns in categories.items():
        if category == 'Miscellaneous':
            continue
        for pattern in patterns:
            if pattern in filename_lower:
                return category
    
    return 'Miscellaneous'

def merge_download_folders():
    """Merge downloaded files from different sources into one organized structure."""
    all_downloads = "all_downloads"
    os.makedirs(all_downloads, exist_ok=True)
    
    # Sources to merge
    sources = ["downloaded", "downloaded_root"]
    
    file_count = 0
    for source in sources:
        if os.path.exists(source):
            for item in os.listdir(source):
                if item == 'archive':  # Skip archive folder
                    continue
                    
                source_path = os.path.join(source, item)
                if os.path.isfile(source_path):
                    dest_path = os.path.join(all_downloads, item)
                    if not os.path.exists(dest_path):
                        shutil.copy2(source_path, dest_path)
                        file_count += 1
    
    print(f"Merged {file_count} files into {all_downloads}/")
    return all_downloads

def organize_all_documents(source_dir, organized_dir):
    """Organize all documents into categorized subdirectories."""
    os.makedirs(organized_dir, exist_ok=True)
    
    organization_map = {}
    category_counts = {}
    
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        
        if os.path.isdir(filepath):
            continue
            
        # Categorize the document
        category = categorize_document(filename)
        category_dir = os.path.join(organized_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Copy file to category folder
        dest_path = os.path.join(category_dir, filename)
        shutil.copy2(filepath, dest_path)
        
        organization_map[filename] = category
        category_counts[category] = category_counts.get(category, 0) + 1
        
    # Print summary
    print("\nOrganization Summary:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} files")
    
    return organization_map

def extract_document_content(filepath):
    """Extract text content from various document types."""
    filename_lower = filepath.lower()
    
    try:
        if filename_lower.endswith('.pdf'):
            reader = PdfReader(filepath)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
        elif filename_lower.endswith('.docx'):
            with open(filepath, 'rb') as f:
                text = mammoth.extract_raw_text(f).value
        elif filename_lower.endswith('.doc'):
            # Try to read as docx, fallback to basic text
            try:
                with open(filepath, 'rb') as f:
                    text = mammoth.extract_raw_text(f).value
            except:
                return None
        elif filename_lower.endswith('.md'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        elif filename_lower.endswith('.eml'):
            # Basic email parsing - just read as text
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            except:
                return None
        elif filename_lower.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        else:
            return None
    except Exception as e:
        print(f"Error reading {os.path.basename(filepath)}: {str(e)}")
        return None
    
    return text

def create_comprehensive_index(organized_dir, index_path):
    """Create a comprehensive index of all documents."""
    documents = []
    
    print("\nExtracting content from documents...")
    
    for category in os.listdir(organized_dir):
        category_path = os.path.join(organized_dir, category)
        
        if not os.path.isdir(category_path):
            continue
        
        print(f"\nProcessing {category}...")
        doc_count = 0
        
        for filename in os.listdir(category_path):
            filepath = os.path.join(category_path, filename)
            
            # Extract content
            content = extract_document_content(filepath)
            if content is None:
                continue
            
            # Create enhanced metadata
            metadata = {
                'source': filename,
                'category': category,
                'file_path': filepath,
                'file_type': os.path.splitext(filename)[1].lower()
            }
            
            # Add date if present in filename
            import re
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            if date_match:
                metadata['date'] = date_match.group(1)
            
            documents.append(Document(
                page_content=content,
                metadata=metadata
            ))
            doc_count += 1
        
        print(f"  Processed {doc_count} documents")
    
    if documents:
        print(f"\nCreating index with {len(documents)} documents...")
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        
        # Create embeddings and save
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(index_path)
        
        print(f"✅ Index saved to '{index_path}'")
    else:
        print("❌ No documents to index!")
    
    return documents

def generate_comprehensive_report(documents, report_path="paradocs_complete_report.txt"):
    """Generate a comprehensive report of all indexed documents."""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("PARADOCS COMPREHENSIVE INDEX REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        # Summary
        f.write(f"Total Documents Indexed: {len(documents)}\n")
        
        # Group by category
        categories = {}
        for doc in documents:
            cat = doc.metadata['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)
        
        f.write(f"Total Categories: {len(categories)}\n\n")
        
        # Category breakdown
        f.write("DOCUMENTS BY CATEGORY:\n")
        f.write("-" * 40 + "\n\n")
        
        for category in sorted(categories.keys()):
            docs = categories[category]
            f.write(f"{category}: {len(docs)} documents\n")
            
            # Sort documents by name
            sorted_docs = sorted(docs, key=lambda x: x.metadata['source'])
            for doc in sorted_docs:
                f.write(f"  - {doc.metadata['source']}")
                if 'date' in doc.metadata:
                    f.write(f" [{doc.metadata['date']}]")
                f.write("\n")
            f.write("\n")
    
    print(f"\nReport saved to '{report_path}'")

# Main execution
if __name__ == "__main__":
    print("ParaDocs Comprehensive Ingestion and Organization")
    print("=" * 50)
    
    # Step 1: Wait for downloads to complete
    print("\nNote: Make sure download_all_files.py has completed before running this!")
    
    # Step 2: Merge all downloads
    print("\nStep 1: Merging all downloaded files...")
    merged_dir = merge_download_folders()
    
    # Step 3: Organize documents
    organized_dir = "paradocs_complete"
    print("\nStep 2: Organizing documents by category...")
    organization_map = organize_all_documents(merged_dir, organized_dir)
    
    # Step 4: Create comprehensive index
    index_path = "paradocs_faiss_complete"
    print("\nStep 3: Creating comprehensive index...")
    documents = create_comprehensive_index(organized_dir, index_path)
    
    # Step 5: Generate report
    print("\nStep 4: Generating comprehensive report...")
    generate_comprehensive_report(documents)
    
    print("\n✅ ParaDocs comprehensive update complete!") 