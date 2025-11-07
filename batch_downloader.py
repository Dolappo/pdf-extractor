#!/usr/bin/env python3
"""
Batch NERDC PDF Downloader
Downloads multiple PDFs from NERDC website with support for different URL patterns
"""
import requests
import os
import time
import json
from urllib.parse import urlparse, parse_qs
from pathlib import Path

class NERDCDownloader:
    def __init__(self, download_dir="downloads", delay_between_downloads=2):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.delay = delay_between_downloads
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        
        # Statistics
        self.successful_downloads = []
        self.failed_downloads = []
    
    def validate_pdf(self, content):
        """Check if content is a valid PDF"""
        if not content:
            return False, "Empty content"
        
        if content[:4] != b'%PDF':
            if content.startswith(b'<!DOCTYPE') or content.startswith(b'<html'):
                return False, "Got HTML instead of PDF"
            elif content.startswith(b'{') or content.startswith(b'['):
                return False, "Got JSON instead of PDF"
            return False, f"Invalid PDF header: {content[:20]}"
        
        if b'%%EOF' not in content[-1024:]:
            return False, "Missing PDF end marker"
        
        return True, "Valid PDF"
    
    def extract_pdf_filename(self, url):
        """Extract PDF filename from various URL formats"""
        # Handle viewer URLs like: view_pri.html?pdf=filename.pdf
        if 'pdf=' in url:
            return url.split('pdf=')[1].split('&')[0]
        
        # Handle direct PDF URLs
        if url.endswith('.pdf'):
            return url.split('/')[-1]
        
        # Default fallback
        return None
    
    def generate_pdf_urls(self, pdf_filename):
        """Generate possible PDF URLs for a given filename"""
        base_patterns = [
            # Primary pattern from HTML analysis
            f"https://nerdc.gov.ng/content_manager/primary/{pdf_filename}",
            # Other common patterns
            f"https://nerdc.gov.ng/content_manager/secondary/{pdf_filename}",
            f"https://nerdc.gov.ng/content_manager/{pdf_filename}",
            f"https://nerdc.gov.ng/content_manager/uploads/{pdf_filename}",
            f"https://nerdc.gov.ng/uploads/{pdf_filename}",
            f"https://nerdc.gov.ng/pdfs/{pdf_filename}",
            f"https://nerdc.gov.ng/files/{pdf_filename}",
            f"https://nerdc.gov.ng/curriculum/{pdf_filename}",
            f"https://nerdc.gov.ng/documents/{pdf_filename}",
        ]
        return base_patterns
    
    def download_single_pdf(self, url, custom_filename=None):
        """Download a single PDF from URL"""
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        
        # Extract filename
        pdf_filename = self.extract_pdf_filename(url)
        if not pdf_filename:
            print("Could not extract PDF filename from URL")
            return False
        
        print(f"Target PDF: {pdf_filename}")
        
        # Generate possible URLs
        possible_urls = self.generate_pdf_urls(pdf_filename)
        
        # Try each URL
        for i, pdf_url in enumerate(possible_urls, 1):
            print(f"\nAttempt {i}/{len(possible_urls)}: {pdf_url}")
            
            try:
                response = self.session.get(pdf_url, timeout=30)
                
                if response.status_code == 200:
                    print(f"✓ Response received ({len(response.content)} bytes)")
                    
                    # Validate PDF
                    is_valid, message = self.validate_pdf(response.content)
                    print(f"Validation: {message}")
                    
                    if is_valid:
                        # Save the PDF
                        output_filename = custom_filename or pdf_filename
                        output_path = self.download_dir / output_filename
                        
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"SUCCESS: Downloaded to {output_path}")
                        self.successful_downloads.append({
                            'original_url': url,
                            'pdf_url': pdf_url,
                            'filename': output_filename,
                            'size': len(response.content)
                        })
                        return True
                    else:
                        # Save debug info for invalid PDFs
                        debug_path = self.download_dir / f"debug_{pdf_filename}_{i}.txt"
                        with open(debug_path, 'wb') as f:
                            f.write(response.content[:2000])
                        print(f"Invalid PDF saved debug info to: {debug_path}")
                
                else:
                    print(f"HTTP {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")
                continue
        
        print(f"FAILED: Could not download {pdf_filename}")
        self.failed_downloads.append({
            'original_url': url,
            'filename': pdf_filename,
            'reason': 'All URLs failed'
        })
        return False
    
    def download_batch(self, urls):
        """Download multiple PDFs from a list of URLs"""
        print(f"Starting batch download of {len(urls)} PDFs...")
        print(f"Download directory: {self.download_dir.absolute()}")
        
        for i, url_info in enumerate(urls, 1):
            # Handle different input formats
            if isinstance(url_info, str):
                url = url_info
                custom_filename = None
            elif isinstance(url_info, dict):
                url = url_info['url']
                custom_filename = url_info.get('filename')
            else:
                print(f"Invalid URL format: {url_info}")
                continue
            
            print(f"\n[{i}/{len(urls)}] Processing...")
            
            success = self.download_single_pdf(url, custom_filename)
            
            # Delay between downloads to be respectful
            if i < len(urls):  # Don't delay after the last download
                print(f"Waiting {self.delay} seconds...")
                time.sleep(self.delay)
        
        self.print_summary()
    
    def print_summary(self):
        """Print download summary"""
        print(f"\n{'='*60}")
        print("DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"Successful: {len(self.successful_downloads)}")
        print(f"Failed: {len(self.failed_downloads)}")
        
        if self.successful_downloads:
            print(f"\nSuccessful Downloads:")
            total_size = 0
            for download in self.successful_downloads:
                size_mb = download['size'] / (1024 * 1024)
                total_size += download['size']
                print(f"  • {download['filename']} ({size_mb:.2f} MB)")
            
            print(f"\nTotal downloaded: {total_size / (1024 * 1024):.2f} MB")
        
        if self.failed_downloads:
            print(f"\nFailed Downloads:")
            for failed in self.failed_downloads:
                print(f"  • {failed['filename']} - {failed['reason']}")
    
    def save_results_log(self):
        """Save results to a JSON log file"""
        log_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'successful_downloads': self.successful_downloads,
            'failed_downloads': self.failed_downloads,
            'summary': {
                'total_attempted': len(self.successful_downloads) + len(self.failed_downloads),
                'successful': len(self.successful_downloads),
                'failed': len(self.failed_downloads)
            }
        }
        
        log_path = self.download_dir / 'download_log.json'
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"Results logged to: {log_path}")

def main():
    """Main function with example usage"""
    print("NERDC Batch PDF Downloader")
    print("=" * 60)
    
    # Example URLs - replace with your actual URLs
    urls_to_download = [
        # Format 1: Just URLs
        "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=pri1-3_basic_science_intro.pdf",
        
        # Format 2: URLs with custom filenames
        {
            "url": "https://nerdc.gov.ng/content_manager/view_pri.html?pdf=another_document.pdf",
            "filename": "custom_name.pdf"
        },
        
        # Add more URLs here...
    ]
    
    # You can also load URLs from a file
    # urls_to_download = load_urls_from_file("urls.txt")
    
    # Create downloader
    downloader = NERDCDownloader(
        download_dir="nerdc_pdfs",  # Directory to save PDFs
        delay_between_downloads=2   # Seconds to wait between downloads
    )
    
    # Start batch download
    downloader.download_batch(urls_to_download)
    
    # Save log
    downloader.save_results_log()

def load_urls_from_file(filename):
    """Load URLs from a text file (one URL per line)"""
    urls = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        print(f"Loaded {len(urls)} URLs from {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found")
    return urls

if __name__ == "__main__":
    main()