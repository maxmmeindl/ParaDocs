#!/usr/bin/env python3
"""
ParaDocs Enhanced System Launcher
Quick access to citation-based search and violation analysis
"""

import subprocess
import webbrowser
from pathlib import Path
import json
import os

def main():
    print("\n" + "="*60)
    print("🏛️  PARADOCS ENHANCED CITATION SYSTEM")
    print("="*60)
    print("✅ Citation Registry Built")
    print("✅ Enhanced Search System Ready") 
    print("✅ Violation Mapping Active")
    print("✅ Natural Language Queries Enabled")
    print("="*60)
    
    while True:
        print("\n📋 QUICK ACCESS MENU:")
        print("1. 🌐 Open Citation Dashboard (Web Interface)")
        print("2. 🔍 Natural Language Search")
        print("3. 📚 Search by Legal Citation")
        print("4. ⚖️  Search by Violation Type")
        print("5. 📊 Generate Case Report")
        print("6. 🔧 Rebuild Citation Registry")
        print("7. 📖 Show Documentation")
        print("0. Exit")
        
        choice = input("\nSelect option (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
            
        elif choice == "1":
            open_dashboard()
            
        elif choice == "2":
            natural_language_search()
            
        elif choice == "3":
            citation_search()
            
        elif choice == "4":
            violation_search()
            
        elif choice == "5":
            generate_case_report()
            
        elif choice == "6":
            rebuild_citations()
            
        elif choice == "7":
            show_documentation()
            
        else:
            print("❌ Invalid option. Please try again.")

def open_dashboard():
    """Open the web dashboard"""
    dashboard_file = Path("paradocs_citation_dashboard.html")
    if dashboard_file.exists():
        webbrowser.open(f'file://{dashboard_file.absolute()}')
        print("🌐 Opening Citation Dashboard in your browser...")
    else:
        print("❌ Dashboard file not found!")

def natural_language_search():
    """Perform natural language search"""
    print("\n🔍 NATURAL LANGUAGE SEARCH")
    print("Examples:")
    print("- 'RA policies and timelines'")
    print("- 'disability discrimination violations'")
    print("- 'HIPAA privacy breaches'")
    print("- 'retaliation and adverse actions'")
    
    query = input("\nEnter your search query: ").strip()
    if query:
        print(f"\n🔍 Searching for: '{query}'")
        subprocess.run(['python', 'search_enhanced.py', 'search', '-q', query])
    else:
        print("❌ No query entered.")

def citation_search():
    """Search by specific citation"""
    print("\n📚 CITATION SEARCH")
    print("Available citations:")
    citations = [
        "FEMA Instruction 256-022-01",
        "29 C.F.R.",
        "29 U.S.C.",
        "42 U.S.C.",
        "HIPAA (45 CFR §164.312)"
    ]
    
    for i, citation in enumerate(citations, 1):
        print(f"{i}. {citation}")
    
    choice = input("\nSelect citation number (1-5): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(citations):
            citation = citations[idx]
            print(f"\n📚 Searching events for: {citation}")
            subprocess.run(['python', 'search_enhanced.py', 'citation', '-c', citation])
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a number.")

def violation_search():
    """Search by violation type"""
    print("\n⚖️  VIOLATION TYPE SEARCH")
    violations = [
        "timeline_breaches",
        "disability_discrimination", 
        "age_discrimination",
        "retaliation",
        "hipaa_breaches",
        "procedural_errors"
    ]
    
    for i, violation in enumerate(violations, 1):
        print(f"{i}. {violation.replace('_', ' ').title()}")
    
    choice = input("\nSelect violation type (1-6): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(violations):
            violation = violations[idx]
            print(f"\n⚖️  Analyzing violation: {violation.replace('_', ' ')}")
            subprocess.run(['python', 'search_enhanced.py', 'violation', '-v', violation])
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a number.")

def generate_case_report():
    """Generate comprehensive case report"""
    print("\n📊 GENERATING CASE REPORT")
    case_number = input("Enter case number (or press Enter for default): ").strip()
    if not case_number:
        case_number = "HS-FEMA-02430-2024"
    
    print(f"📊 Generating report for case: {case_number}")
    subprocess.run(['python', 'search_enhanced.py', 'report', '--case', case_number])
    
    # Show summary
    report_file = f"case_report_{case_number}.json"
    if Path(report_file).exists():
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        print(f"\n📋 REPORT SUMMARY:")
        print(f"   Total Events: {report['metadata']['total_events']}")
        print(f"   Total Citations: {report['metadata']['total_citations']}")
        print(f"   Generated: {report['metadata']['generated']}")
        print(f"   File: {report_file}")

def rebuild_citations():
    """Rebuild citation registry"""
    print("\n🔧 REBUILDING CITATION REGISTRY")
    subprocess.run(['python', 'extract_citations.py'])
    print("✅ Citation registry rebuilt!")

def show_documentation():
    """Show system documentation"""
    print("\n📖 PARADOCS ENHANCED SYSTEM DOCUMENTATION")
    print("="*50)
    
    print("\n🎯 NEW CAPABILITIES (48-Hour Enhancement):")
    print("✅ Citation Registry: 9 legal authorities mapped")
    print("✅ Natural Language Queries: 'RA policies and timelines'")
    print("✅ Citation-Based Search: Find events by legal authority")
    print("✅ Violation Analysis: Timeline breaches, discrimination, etc.")
    print("✅ Comprehensive Reports: JSON output with violation mapping")
    print("✅ Web Dashboard: Interactive interface for all features")
    
    print("\n🔧 TECHNICAL COMPONENTS:")
    print("• extract_citations.py - Builds citation registry from timeline data")
    print("• search_enhanced.py - Citation-aware search with NL processing")
    print("• paradocs_citation_dashboard.html - Web interface")
    print("• citation_registry.json - Master legal authorities database")
    
    print("\n🚀 USAGE EXAMPLES:")
    print("1. Web Interface: Open dashboard for interactive search")
    print("2. Command Line: python search_enhanced.py search -q 'RA violations'")
    print("3. Citation Search: python search_enhanced.py citation -c 'FEMA Instruction 256-022-01'")
    print("4. Case Reports: python search_enhanced.py report --case HS-FEMA-02430-2024")
    
    print("\n📊 VIOLATION TAXONOMY:")
    print("• Procedural Violations: Timeline breaches, documentation errors")
    print("• Substantive Violations: Disability/age discrimination, retaliation")
    print("• Administrative Violations: HIPAA breaches, record keeping failures")
    
    print("\n🎯 LEGAL RESEARCH QUERIES NOW SUPPORTED:")
    print("• 'Show me all RA policy violations and timeline breaches'")
    print("• 'Find disability discrimination evidence'")
    print("• 'Pull up FEMA accommodation procedure violations'")
    print("• 'Analyze retaliation patterns in timeline'")

if __name__ == "__main__":
    main() 