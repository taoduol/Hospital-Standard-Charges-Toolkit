#!/usr/bin/env python3
"""
Hospital Billing Data Scraper
Downloads machine-readable standard charges from hospital websites
Automatically converts .ashx files to .csv
"""

import os
import json
import requests
import csv
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import argparse
import sys

# Configuration
CONFIG_FILE = "hospitals_config.json"
DATA_DIR = "hospital_charges_data"
TIMEOUT = 30  # seconds


class HospitalChargeScraper:
    def __init__(self, config_file=CONFIG_FILE, data_dir=DATA_DIR):
        self.config_file = config_file
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.hospitals = self.load_config()
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
    
    def load_config(self):
        """Load hospital configuration from JSON file"""
        if not os.path.exists(self.config_file):
            print(f"❌ Config file not found: {self.config_file}")
            sys.exit(1)
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get("hospitals", [])
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {self.config_file}")
            sys.exit(1)
    
    def json_to_csv(self, json_path):
        """Convert JSON file to CSV"""
        try:
            print(f"  ✓ Converting JSON to CSV...")
            
            # Read JSON file
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                # Simple list of objects
                rows = data
            elif isinstance(data, dict):
                # Check if there's a key that contains the actual data
                if 'data' in data:
                    rows = data['data']
                elif 'charges' in data:
                    rows = data['charges']
                elif 'results' in data:
                    rows = data['results']
                else:
                    # Try to use the first list-like value
                    for key, value in data.items():
                        if isinstance(value, list):
                            rows = value
                            break
                    else:
                        # Fallback: treat dict as single row
                        rows = [data]
            else:
                print(f"  ✗ Unexpected JSON format")
                return False
            
            # Convert to CSV
            if not rows:
                print(f"  ✗ No data found in JSON")
                return False
            
            csv_path = json_path.with_suffix('.csv')
            
            # Get all unique keys from all rows
            if isinstance(rows[0], dict):
                fieldnames = set()
                for row in rows:
                    fieldnames.update(row.keys())
                fieldnames = sorted(list(fieldnames))
            else:
                fieldnames = ['value']
            
            # Write CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in rows:
                    if isinstance(row, dict):
                        writer.writerow(row)
                    else:
                        writer.writerow({'value': row})
            
            # Delete the JSON file
            json_path.unlink()
            print(f"  ✓ Saved as CSV: {csv_path.name}")
            return True
        
        except Exception as e:
            print(f"  ✗ JSON conversion failed: {e}")
            return False
    

        """Download a file from URL"""
        try:
            print(f"  ↓ Downloading: {url}")
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save file
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            # Auto-convert .ashx to .csv
            if save_path.suffix.lower() == '.ashx':
                csv_path = save_path.with_suffix('.csv')
                save_path.rename(csv_path)
                save_path = csv_path
                print(f"  ✓ Automatically converted .ashx to .csv")
            
            # Auto-convert .json to .csv
            if save_path.suffix.lower() == '.json':
                self.json_to_csv(save_path)
                return True
            
            file_size = len(response.content) / 1024  # KB
            print(f"  ✓ Saved to: {save_path} ({file_size:.1f} KB)")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed to download: {e}")
            return False
    
    def get_filename_from_url(self, url):
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename in path, use a generic name
        if not filename or '.' not in filename:
            filename = f"charges_{self.timestamp}.json"
        
        return filename
    
    def download_hospital(self, hospital):
        """Download charges for a single hospital"""
        hospital_name = hospital.get("name", "Unknown")
        short_name = hospital.get("short_name", "hospital").lower()
        file_url = hospital.get("file_url")
        billing_page = hospital.get("billing_page")
        last_verified = hospital.get("last_verified", "Unknown")
        
        if not file_url:
            print(f"⚠ No file_url configured for {hospital_name}")
            print(f"   Billing page: {billing_page}")
            print(f"   To add: Find the direct download link and update hospitals_config.json")
            return False
        
        # Create hospital-specific directory
        hospital_dir = self.data_dir / short_name / self.timestamp
        
        print(f"\n📥 {hospital_name}")
        print(f"   Billing page: {billing_page}")
        print(f"   Last verified: {last_verified}")
        print(f"   Folder: {hospital_dir}")
        
        filename = self.get_filename_from_url(file_url)
        save_path = hospital_dir / filename
        
        if self.download_file(file_url, save_path):
            return True
        return False
    
    def download_all(self):
        """Download charges from all configured hospitals"""
        if not self.hospitals:
            print("❌ No hospitals configured in hospitals_config.json")
            return
        
        print(f"\n{'='*60}")
        print(f"Hospital Billing Data Collector")
        print(f"Run Date: {self.timestamp}")
        print(f"{'='*60}")
        
        total_success = 0
        for hospital in self.hospitals:
            if self.download_hospital(hospital):
                total_success += 1
        
        print(f"\n{'='*60}")
        print(f"✓ Complete! Successfully downloaded {total_success}/{len(self.hospitals)} hospitals")
        print(f"Data saved to: {self.data_dir}")
        print(f"\nNext steps:")
        print(f"  1. Check hospital_charges_data/ for your files")
        print(f"  2. Review data for quality issues")
        print(f"  3. See Discussions for extraction workflows")
        print(f"{'='*60}\n")
    
    def download_specific(self, hospital_short_name):
        """Download charges for a specific hospital"""
        hospital = None
        for h in self.hospitals:
            if h.get("short_name", "").lower() == hospital_short_name.lower():
                hospital = h
                break
        
        if not hospital:
            print(f"❌ Hospital '{hospital_short_name}' not found in config")
            print(f"Available hospitals: {[h.get('short_name') for h in self.hospitals]}")
            return
        
        print(f"\n{'='*60}")
        print(f"Hospital Billing Data Collector")
        print(f"{'='*60}")
        
        self.download_hospital(hospital)
        
        print(f"\nData saved to: {self.data_dir}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Download hospital billing data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 download_charges.py                    # Download all hospitals
  python3 download_charges.py yale-new-haven     # Download specific hospital
        """
    )
    
    parser.add_argument(
        "hospital",
        nargs="?",
        help="Download specific hospital (short_name from config)"
    )
    
    args = parser.parse_args()
    
    scraper = HospitalChargeScraper()
    
    if args.hospital:
        scraper.download_specific(args.hospital)
    else:
        scraper.download_all()


if __name__ == "__main__":
    main()
