#!/usr/bin/env python3
"""
Enhanced OLX Car Cover Search Scraper with Advanced Anti-Blocking
Designed to work around common anti-bot protections
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import sys
import random
from urllib.parse import urljoin
from datetime import datetime
import urllib3

# Disable SSL warnings for troubleshooting
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EnhancedOLXScraper:
    def __init__(self):
        self.base_url = "https://www.olx.in"
        self.search_url = "https://www.olx.in/items/q-car-cover"
        
        # More realistic browser headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Configure session for better compatibility
        self.session.max_redirects = 10
        
    def random_delay(self, min_seconds=3, max_seconds=8):
        """Add random delay to appear more human-like"""
        delay = random.uniform(min_seconds, max_seconds)
        print(f"⏳ Waiting {delay:.1f} seconds to avoid detection...")
        time.sleep(delay)
        
    def get_page_with_fallbacks(self, url, max_retries=3):
        """Try multiple approaches to get the page"""
        
        # Method 1: Standard HTTPS request
        print(f"🔄 Method 1: Standard HTTPS request")
        response = self.try_request(url, max_retries)
        if response:
            return response
            
        # Method 2: Try without SSL verification
        print(f"🔄 Method 2: Without SSL verification")
        response = self.try_request(url, max_retries, verify_ssl=False)
        if response:
            return response
            
        # Method 3: Try HTTP instead of HTTPS
        http_url = url.replace('https://', 'http://')
        print(f"🔄 Method 3: HTTP instead of HTTPS")
        response = self.try_request(http_url, max_retries)
        if response:
            return response
            
        # Method 4: Try with different user agent
        print(f"🔄 Method 4: Different User-Agent")
        old_ua = self.session.headers['User-Agent']
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        response = self.try_request(url, max_retries)
        self.session.headers['User-Agent'] = old_ua  # Restore original
        if response:
            return response
            
        return None
    
    def try_request(self, url, max_retries=3, verify_ssl=True):
        """Try to make a request with retries"""
        for attempt in range(max_retries):
            try:
                print(f"   📡 Attempt {attempt + 1}: {url}")
                
                # Progressive timeout increase
                timeout = 15 + (attempt * 10)  # 15, 25, 35 seconds
                
                response = self.session.get(
                    url, 
                    timeout=timeout, 
                    verify=verify_ssl,
                    allow_redirects=True,
                    stream=False
                )
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📦 Size: {len(response.content)} bytes")
                
                if response.status_code == 200 and len(response.content) > 1000:
                    return response
                elif response.status_code == 403:
                    print(f"   🚫 Access forbidden - likely blocked")
                elif response.status_code == 429:
                    print(f"   ⏰ Rate limited - need to wait longer")
                    self.random_delay(10, 20)
                else:
                    print(f"   ⚠️  Unexpected status or small response")
                
            except requests.exceptions.Timeout:
                print(f"   ⏰ Timeout after {timeout} seconds")
            except requests.exceptions.ConnectionError as e:
                print(f"   🔌 Connection error: {str(e)[:100]}...")
            except requests.exceptions.SSLError as e:
                print(f"   🔒 SSL error: {str(e)[:100]}...")
            except Exception as e:
                print(f"   ❌ Unexpected error: {str(e)[:100]}...")
            
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + random.uniform(2, 5)
                print(f"   ⏳ Waiting {delay:.1f}s before retry...")
                time.sleep(delay)
        
        return None
    
    def parse_listing(self, listing_element):
        """Parse individual listing element"""
        try:
            listing_data = {}
            
            # Multiple selectors for title
            title_selectors = [
                ('span', {'data-aut-id': 'itemTitle'}),
                ('h3', {}),
                ('a', {'data-aut-id': 'itemTitle'}),
            ]
            
            title = 'N/A'
            for tag, attrs in title_selectors:
                elem = listing_element.find(tag, attrs)
                if elem:
                    title = elem.get_text(strip=True)
                    break
            listing_data['title'] = title
            
            # Multiple selectors for price
            price_selectors = [
                ('span', {'data-aut-id': 'itemPrice'}),
                ('span', {'class': lambda x: x and 'price' in str(x).lower()}),
            ]
            
            price = 'N/A'
            for tag, attrs in price_selectors:
                elem = listing_element.find(tag, attrs)
                if elem:
                    price = elem.get_text(strip=True)
                    break
            listing_data['price'] = price
            
            # Location
            location_elem = listing_element.find('span', {'data-aut-id': 'item-location'})
            listing_data['location'] = location_elem.get_text(strip=True) if location_elem else 'N/A'
            
            # Date
            date_elem = listing_element.find('span', {'data-aut-id': 'item-date'})
            listing_data['date'] = date_elem.get_text(strip=True) if date_elem else 'N/A'
            
            # Link
            link_elem = listing_element.find('a')
            if link_elem and link_elem.get('href'):
                listing_data['url'] = urljoin(self.base_url, link_elem['href'])
            else:
                listing_data['url'] = 'N/A'
            
            # Image URL
            img_elem = listing_element.find('img')
            listing_data['image_url'] = img_elem.get('src', 'N/A') if img_elem else 'N/A'
            
            return listing_data
            
        except Exception as e:
            print(f"   ⚠️  Error parsing listing: {e}")
            return None
    
    def scrape_search_results(self, max_pages=2):
        """Scrape search results from OLX with enhanced methods"""
        all_listings = []
        
        print("🚀 Starting enhanced OLX scraping...")
        print("💡 This version tries multiple methods to bypass blocking")
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.search_url
            else:
                url = f"{self.search_url}?page={page}"
            
            print(f"\n📄 Scraping page {page}...")
            
            # Add delay before each page (except first)
            if page > 1:
                self.random_delay(5, 10)
            
            response = self.get_page_with_fallbacks(url)
            
            if not response:
                print(f"❌ Failed to fetch page {page} with all methods")
                continue
            
            # Save response for debugging
            debug_filename = f'debug_page_{page}.html'
            with open(debug_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"💾 Saved page {page} as '{debug_filename}' for inspection")
            
            # Check for blocking indicators
            content_lower = response.text.lower()
            if any(word in content_lower for word in ['blocked', 'captcha', 'robot', 'access denied']):
                print("⚠️  Detected possible blocking in content")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors for listings
            selectors_to_try = [
                ('div', {'data-aut-id': 'itemBox'}),
                ('div', {'class': lambda x: x and any(cls in str(x) for cls in ['EIR5N', '_1ONrY', 'item'])}),
                ('li', {'data-aut-id': 'itemBox'}),
                ('article', {}),
            ]
            
            listings = []
            for tag, attrs in selectors_to_try:
                listings = soup.find_all(tag, attrs)
                if listings:
                    print(f"✅ Found {len(listings)} listings using: {tag} {attrs}")
                    break
            
            if not listings:
                print("🔍 Trying fallback: looking for any links with '/item/'")
                all_links = soup.find_all('a', href=True)
                listings = [link.parent for link in all_links if '/item/' in link.get('href', '')]
                
                if listings:
                    print(f"✅ Found {len(listings)} potential listings via fallback")
                else:
                    print("❌ No listings found with any method")
                    print(f"📊 Page analysis:")
                    print(f"   - Total links: {len(all_links)}")
                    print(f"   - Page title: {soup.title.string if soup.title else 'No title'}")
                    continue
            
            # Parse listings
            page_listings = []
            for listing in listings:
                parsed = self.parse_listing(listing)
                if parsed and parsed['title'] != 'N/A':
                    page_listings.append(parsed)
            
            all_listings.extend(page_listings)
            print(f"✅ Successfully parsed {len(page_listings)} listings from page {page}")
        
        return all_listings
    
    def save_to_json(self, listings, filename='olx_car_cover_results.json'):
        """Save listings to JSON file"""
        data = {
            'search_query': 'car cover',
            'search_url': self.search_url,
            'scraped_at': datetime.now().isoformat(),
            'total_results': len(listings),
            'listings': listings
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")
    
    def save_to_csv(self, listings, filename='olx_car_cover_results.csv'):
        """Save listings to CSV file"""
        if not listings:
            print("❌ No listings to save")
            return
            
        fieldnames = listings[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)
        print(f"💾 Results saved to {filename}")
    
    def print_summary(self, listings):
        """Print summary of results"""
        print(f"\n{'='*60}")
        print(f"🎯 SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"📊 Total listings found: {len(listings)}")
        print(f"🔗 Search URL: {self.search_url}")
        print(f"⏰ Scraped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if listings:
            print(f"\n📋 Sample listings:")
            for i, listing in enumerate(listings[:3], 1):
                print(f"\n{i}. {listing['title']}")
                print(f"   💰 Price: {listing['price']}")
                print(f"   📍 Location: {listing['location']}")
                print(f"   📅 Date: {listing['date']}")
                print(f"   🔗 URL: {listing['url'][:80]}...")

def main():
    print("🔧 Enhanced OLX Car Cover Search Scraper")
    print("=" * 50)
    print("⚠️  DISCLAIMER: This script is for educational purposes only.")
    print("Please respect OLX's terms of service and robots.txt")
    print("=" * 50)
    
    # Ask user for confirmation
    confirm = input("\n🚀 Do you want to proceed with enhanced scraping? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Scraping cancelled.")
        return
    
    try:
        scraper = EnhancedOLXScraper()
        
        # Get max pages from user
        try:
            max_pages = int(input("📄 Enter number of pages to scrape (default 2): ") or "2")
            max_pages = max(1, min(max_pages, 5))  # Limit to reasonable range
        except ValueError:
            max_pages = 2
        
        print(f"\n🎯 Starting enhanced scrape for {max_pages} pages...")
        print("💡 This may take longer but has better success rates")
        
        listings = scraper.scrape_search_results(max_pages=max_pages)
        
        if listings:
            # Save results
            scraper.save_to_json(listings)
            scraper.save_to_csv(listings)
            scraper.print_summary(listings)
            
            print(f"\n🎉 SUCCESS! Found {len(listings)} listings")
            print("📁 Check these files:")
            print("   - olx_car_cover_results.json")
            print("   - olx_car_cover_results.csv")
            
        else:
            print("\n❌ No listings found. Possible reasons:")
            print("1. 🚫 OLX has strong anti-bot protection for your IP")
            print("2. 🌐 Try using a VPN from a different location")
            print("3. ⏰ Wait a few hours and try again")
            print("4. 📱 Try from mobile data instead of WiFi")
            print("5. 🔍 Check the saved debug_page_*.html files")
            
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()