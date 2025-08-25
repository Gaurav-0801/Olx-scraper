#!/usr/bin/env python3
"""
Quick test to check if we can reach OLX at all
"""

import requests
import time

def quick_test():
    print("🔍 Quick OLX Connection Test")
    print("=" * 40)
    
    # Test with minimal request
    try:
        print("Testing basic connection...")
        response = requests.get('https://httpbin.org/get', timeout=10)
        print(f"✅ Internet works: {response.status_code}")
    except:
        print("❌ No internet connection")
        return
    
    # Test OLX with browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    urls = [
        'https://www.olx.in',
        'http://www.olx.in',  # Try HTTP
        'https://www.olx.in/sitemap.xml'
    ]
    
    for url in urls:
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"✅ Success: {response.status_code} ({len(response.content)} bytes)")
            if response.status_code == 200:
                print("🎉 This URL works! Try the enhanced scraper.")
                break
        except requests.exceptions.Timeout:
            print("❌ Timeout")
        except requests.exceptions.ConnectionError:
            print("❌ Connection refused")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n💡 Recommendations:")
    print("1. Try VPN (different country)")
    print("2. Use mobile data instead of WiFi")
    print("3. Wait 1-2 hours and try again")
    print("4. Run: python olx_scraper_enhanced.py")

if __name__ == "__main__":
    quick_test()