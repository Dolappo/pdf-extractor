#!/usr/bin/env python3
"""
Easy NERDC PDF Download Script
Simple interface for downloading NERDC curriculum PDFs
"""

import sys
import os

# Add the batch downloader to the path
sys.path.append(os.path.dirname(__file__))

from batch_downloader import NERDCDownloader 
from url_config import BASIC_URLS, DETAILED_URLS, MATHEMATICS_URLS, ENGLISH_URLS, ALL_PRIMARY_SUBJECTS

def interactive_download():
    """Interactive mode for selecting what to download"""
    print("🎓 NERDC Curriculum PDF Downloader")
    print("=" * 50)
    print("Choose what you want to download:")
    print()
    print("1. Download specific URLs (enter manually)")
    print("2. Download from predefined collections:")
    print("   a. Basic Science documents")
    print("   b. Mathematics documents") 
    print("   c. English documents")
    print("   d. All Primary subjects")
    print("3. Download from a text file")
    print("4. Exit")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        return manual_url_entry()
    elif choice == '2':
        return choose_collection()
    elif choice == '3':
        return load_from_file()
    elif choice == '4':
        print("Goodbye!")
        return None
    else:
        print("Invalid choice. Please try again.")
        return interactive_download()

def manual_url_entry():
    """Allow manual entry of URLs"""
    print("\n Manual URL Entry")
    print("Enter URLs one by one (press Enter twice to finish):")
    print("Example: https://nerdc.gov.ng/content_manager/view_pri.html?pdf=filename.pdf")
    print()
    
    urls = []
    while True:
        url = input(f"URL {len(urls) + 1}: ").strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("No URLs entered.")
        return None
    
    print(f"\nYou entered {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    confirm = input("\nProceed with download? (y/n): ").lower()
    if confirm == 'y':
        return urls
    else:
        return None

def choose_collection():
    """Choose from predefined collections"""
    print("\nPredefined Collections")
    print("a. Basic Science documents")
    print("b. Mathematics documents")
    print("c. English documents") 
    print("d. All Primary subjects")
    print()
    
    choice = input("Choose collection (a-d): ").lower()
    
    collections = {
        'a': ("Basic Science", DETAILED_URLS),
        'b': ("Mathematics", MATHEMATICS_URLS),
        'c': ("English", ENGLISH_URLS),
        'd': ("All Primary Subjects", ALL_PRIMARY_SUBJECTS)
    }
    
    if choice in collections:
        name, urls = collections[choice]
        print(f"\nSelected: {name}")
        print(f"This will download {len(urls)} documents.")
        
        confirm = input("Proceed? (y/n): ").lower()
        if confirm == 'y':
            return urls
    
    return None

def load_from_file():
    """Load URLs from a text file"""
    print("\nLoad from File")
    filename = input("Enter filename (e.g., my_urls.txt): ").strip()
    
    if not filename:
        return None
    
    try:
        urls = []
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        
        if urls:
            print(f"Loaded {len(urls)} URLs from {filename}")
            return urls
        else:
            print("No valid URLs found in file.")
            return None
            
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def quick_download(urls_list_name):
    """Quick download function for predefined lists"""
    url_lists = {
        'basic': BASIC_URLS,
        'detailed': DETAILED_URLS,
        'math': MATHEMATICS_URLS,
        'english': ENGLISH_URLS,
        'primary': ALL_PRIMARY_SUBJECTS
    }
    
    if urls_list_name in url_lists:
        urls = url_lists[urls_list_name]
        print(f"Quick download: {urls_list_name} ({len(urls)} documents)")
        return start_download(urls)
    else:
        print(f"Unknown list: {urls_list_name}")
        print(f"Available lists: {list(url_lists.keys())}")
        return False

def start_download(urls):
    """Start the download process"""
    if not urls:
        print("No URLs to download.")
        return False
    
    print(f"\n Starting download of {len(urls)} documents...")
    
    # Create downloader with user-friendly settings
    downloader = NERDCDownloader(
        download_dir="NERDC_Curriculum_PDFs",
        delay_between_downloads=1  # Be respectful to the server
    )
    
    # Start batch download
    downloader.download_batch(urls)
    
    # Save results
    downloader.save_results_log()
    
    return len(downloader.successful_downloads) > 0

def main():
    """Main function"""
    # Check for command line arguments for quick downloads
    if len(sys.argv) > 1:
        quick_download(sys.argv[1])
    else:
        # Interactive mode
        urls = interactive_download()
        if urls:
            start_download(urls)

if __name__ == "__main__":
    main()