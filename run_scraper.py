#!/usr/bin/env python3
"""
Simple runner script for the OLX scraper
This makes it even easier to run the scraper
"""

import subprocess
import sys
import os

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        print(f"✓ Python found: {result.stdout.strip()}")
        return True
    except:
        print("✗ Python not found!")
        return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✓ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages")
        return False

def run_scraper():
    """Run the main scraper"""
    print("\n🚀 Starting OLX Car Cover Scraper...")
    print("=" * 50)
    try:
        subprocess.run([sys.executable, 'olx_scraper.py'])
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running scraper: {e}")

def main():
    print("🔧 OLX Scraper Setup & Runner")
    print("=" * 40)
    
    # Check if required files exist
    required_files = ['olx_scraper.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("Please make sure all files are in the same folder!")
        return
    
    # Check Python
    if not check_python():
        print("Please install Python from https://python.org/downloads/")
        return
    
    # Install requirements
    if not install_requirements():
        print("Please try installing manually: pip install requests beautifulsoup4 lxml")
        return
    
    # Run scraper
    run_scraper()
    
    print("\n✅ Done! Check the generated files:")
    print("   - olx_car_cover_results.json")
    print("   - olx_car_cover_results.csv")

if __name__ == "__main__":
    main()