#!/usr/bin/env python3
"""
Test script to check OLX connectivity and response
"""

import requests
import time
from bs4 import BeautifulSoup

def test_olx_connection():
    """Test basic connectivity to OLX"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    urls_to_test = [
        'https://www.olx.in',
        'https://www.olx.in/items/q-car-cover',
        'https://www.olx.in/sitemap.xml'  # This should always work
    ]
    
    session = requests.Session()
    session.headers.update(headers)
    
    print("🔍 Testing OLX connectivity...")
    print("=" * 50)
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"\n{i}. Testing: {url}")
        
        try:
            start_time = time.time()
            response = session.get(url, timeout=30, verify=True)
            end_time = time.time()
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ⏱️  Response time: {end_time - start_time:.2f} seconds")
            print(f"   📦 Content length: {len(response.content)} bytes")
            print(f"   🌐 Final URL: {response.url}")
            
            # Check for common blocking indicators
            content_lower = response.text.lower()
            if any(word in content_lower for word in ['blocked', 'captcha', 'robot', 'bot']):
                print("   ⚠️  Possible blocking detected in content")
            
            # For the search page, try to find some indicators
            if 'q-car-cover' in url:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else 'No title'
                print(f"   📄 Page title: {title}")
                
                # Look for common OLX elements
                common_elements = [
                    soup.find('div', {'data-aut-id': 'itemBox'}),
                    soup.find('div', class_=lambda x: x and 'item' in str(x).lower()),
                    soup.find_all('a', href=lambda x: x and '/item/' in str(x))
                ]
                
                found_elements = sum(1 for elem in common_elements if elem)
                print(f"   🎯 Found {found_elements}/3 expected element types")
                
                # Save the page for manual inspection
                with open(f'test_page_{i}.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"   💾 Saved response as 'test_page_{i}.html'")
            
        except requests.exceptions.Timeout:
            print("   ❌ TIMEOUT - Connection timed out")
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ CONNECTION ERROR: {e}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ REQUEST ERROR: {e}")
        except Exception as e:
            print(f"   ❌ UNEXPECTED ERROR: {e}")
        
        # Small delay between tests
        if i < len(urls_to_test):
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🔧 Troubleshooting suggestions:")
    print("1. Check if you can access https://www.olx.in in your browser")
    print("2. Try using a VPN if OLX is blocked in your region")
    print("3. Check your internet connection")
    print("4. OLX might be temporarily blocking automated requests")
    print("5. Try running the test again after a few minutes")

if __name__ == "__main__":
    test_olx_connection()