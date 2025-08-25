#!/usr/bin/env python3
"""
OLX Car Cover Search Scraper
Scrapes OLX.in for car cover listings and saves results to a file.

IMPORTANT DISCLAIMER:
- This script is for educational purposes only
- Please respect OLX's robots.txt and terms of service
- Use appropriate delays between requests to avoid being blocked
- Consider using OLX's official API if available
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

class OLXScraper:
    def __init__(self):
        self.base_url = "https://www.olx.in"
        self.search_url = "https://www.olx.in/items/q-car-cover"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Add random delay to appear more human-like"""
        delay = random.uniform(min_seconds, max_seconds)
        print(f"Waiting {delay:.1f} seconds...")
        time.sleep(delay)
        
    def get_page(self, url, max_retries=3):
        """Get page content with retry logic"""
        for attempt in range(max_retries):
            try:
                print(f"Fetching: {url} (Attempt {attempt + 1})")
                
                # Add random delay between attempts
                if attempt > 0:
                    self.random_delay(3, 8)
                
                # Increase timeout and add verify=False for SSL issues
                response = self.session.get(url, timeout=30, verify=True, allow_redirects=True)
                response.raise_for_status()
                
                # Check if we got a valid response
                if len(response.content) < 1000:
                    print(f"Response too short ({len(response.content)} bytes), might be blocked")
                    if attempt < max_retries - 1:
                        continue
                
                return response
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                if attempt == max_retries - 1:
                    return None
                # Exponential backoff with randomization
                delay = (2 ** attempt) + random.uniform(1, 3)
                print(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
        return None
    
    def parse_listing(self, listing_element):
        """Parse individual listing element"""
        try:
            listing_data = {}
            
            # Title
            title_elem = listing_element.find('span', {'data-aut-id': 'itemTitle'})
            listing_data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Price
            price_elem = listing_element.find('span', {'data-aut-id': 'itemPrice'})
            listing_data['price'] = price_elem.get_text(strip=True) if price_elem else 'N/A'
            
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
            print(f"Error parsing listing: {e}")
            return None
    
    def scrape_search_results(self, max_pages=3):
        """Scrape search results from OLX"""
        all_listings = []
        
        print("🔍 Starting to scrape OLX...")
        print("💡 Tip: If this fails, try using a VPN or check if OLX is accessible in your browser")
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.search_url
            else:
                url = f"{self.search_url}?page={page}"
            
            print(f"\nScraping page {page}...")
            
            # Add delay before each page (except first)
            if page > 1:
                self.random_delay(3, 6)
            
            response = self.get_page(url)
            
            if not response:
                print(f"Failed to fetch page {page}")
                print("💡 Troubleshooting tips:")
                print("   - Check if you can access the URL in your browser")
                print("   - Try using a VPN")
                print("   - OLX might be temporarily blocking your IP")
                continue
            
            # Check response content
            print(f"Response size: {len(response.content)} bytes")
            if "blocked" in response.text.lower() or "captcha" in response.text.lower():
                print("⚠️  Detected possible blocking or CAPTCHA")
                print("💡 Try again later or use a different IP/VPN")
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Save first page HTML for inspection
            if page == 1:
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("📄 Saved first page HTML as 'debug_page.html' for inspection")
            
            # Find listings - OLX uses different selectors, trying common ones
            selectors_to_try = [
                ('div', {'data-aut-id': 'itemBox'}),
                ('div', {'class': lambda x: x and 'EIR5N' in str(x)}),
                ('div', {'class': lambda x: x and '_1ONrY' in str(x)}),
                ('div', {'class': lambda x: x and 'item' in str(x).lower()}),
                ('a', {'href': lambda x: x and '/item/' in str(x)}),
            ]
            
            listings = []
            for tag, attrs in selectors_to_try:
                listings = soup.find_all(tag, attrs)
                if listings:
                    print(f"✓ Found listings using selector: {tag} with {attrs}")
                    break
            
            if not listings:
                print("❌ No listings found with any selector")
                print("🔍 Trying to find any links that might be listings...")
                
                # Try to find any links that look like listings
                all_links = soup.find_all('a', href=True)
                listings = [link for link in all_links if '/item/' in link.get('href', '')]
                
                if not listings:
                    print("📊 Page analysis:")
                    print(f"   - Total links found: {len(all_links)}")
                    print(f"   - Page title: {soup.title.string if soup.title else 'No title'}")
                    print("   - This might indicate the page structure has changed")
                
            print(f"Found {len(listings)} listings on page {page}")
            
            for listing in listings:
                parsed_listing = self.parse_listing(listing)
                if parsed_listing and parsed_listing['title'] != 'N/A':
                    all_listings.append(parsed_listing)
            
            print(f"✅ Successfully parsed {len([l for l in all_listings if l])} listings from page {page}")
        
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
        print(f"Results saved to {filename}")
    
    def save_to_csv(self, listings, filename='olx_car_cover_results.csv'):
        """Save listings to CSV file"""
        if not listings:
            print("No listings to save")
            return
            
        fieldnames = listings[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)
        print(f"Results saved to {filename}")
    
    def print_summary(self, listings):
        """Print summary of results"""
        print(f"\n{'='*50}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*50}")
        print(f"Total listings found: {len(listings)}")
        print(f"Search URL: {self.search_url}")
        print(f"Scraped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if listings:
            print(f"\nSample listings:")
            for i, listing in enumerate(listings[:3], 1):
                print(f"\n{i}. {listing['title']}")
                print(f"   Price: {listing['price']}")
                print(f"   Location: {listing['location']}")
                print(f"   Date: {listing['date']}")
                print(f"   URL: {listing['url'][:80]}...")

def main():
    print("OLX Car Cover Search Scraper")
    print("=" * 40)
    print("DISCLAIMER: This script is for educational purposes only.")
    print("Please respect OLX's terms of service and robots.txt")
    print("=" * 40)
    
    # Ask user for confirmation
    confirm = input("\nDo you want to proceed with scraping? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Scraping cancelled.")
        return
    
    try:
        scraper = OLXScraper()
        
        # Get max pages from user
        try:
            max_pages = int(input("Enter number of pages to scrape (default 2): ") or "2")
            max_pages = max(1, min(max_pages, 10))  # Limit to reasonable range
        except ValueError:
            max_pages = 2
        
        print(f"\nStarting scrape for {max_pages} pages...")
        listings = scraper.scrape_search_results(max_pages=max_pages)
        
        if listings:
            # Save results
            scraper.save_to_json(listings)
            scraper.save_to_csv(listings)
            scraper.print_summary(listings)
        else:
            print("\nNo listings found. This could be due to:")
            print("1. OLX's page structure has changed")
            print("2. The search query returned no results")
            print("3. Anti-scraping measures are in place")
            print("4. Network connectivity issues")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()