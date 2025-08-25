# Step-by-Step Setup Guide for OLX Car Cover Scraper

## Prerequisites
- Python 3.6 or higher installed on your computer
- Internet connection
- **NO OLX LOGIN REQUIRED** - This scraper works with public search results

## Step 1: Check if Python is Installed
Open your terminal/command prompt and type:
```bash
python --version
```
or
```bash
python3 --version
```

If you don't have Python, download it from: https://python.org/downloads/

## Step 2: Download the Files
1. Copy all the files from this project to a folder on your computer:
   - `olx_scraper.py`
   - `requirements.txt`
   - `README.md`

## Step 3: Install Required Libraries
Open terminal/command prompt in the folder where you saved the files and run:

```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4 lxml
```

## Step 4: Run the Scraper
In the same folder, run:
```bash
python olx_scraper.py
```

Or if that doesn't work:
```bash
python3 olx_scraper.py
```

## Step 5: Follow the Prompts
The script will ask you:
1. **Confirmation**: Type `y` and press Enter to proceed
2. **Number of pages**: Enter how many pages to scrape (default is 2)

## Step 6: Wait for Results
The script will:
- Show progress as it scrapes each page
- Display found listings count
- Save results to two files:
  - `olx_car_cover_results.json` (structured data)
  - `olx_car_cover_results.csv` (spreadsheet format)

## What You'll Get
Each listing will contain:
- **Title**: Product name
- **Price**: Listed price
- **Location**: Seller location
- **Date**: When posted
- **URL**: Direct link to the listing
- **Image URL**: Product image link

## Troubleshooting

### "No listings found"
- OLX might have changed their website structure
- Try running again after a few minutes
- Check your internet connection

### "Permission denied" or "Module not found"
- Make sure you installed the requirements: `pip install -r requirements.txt`
- Try using `python3` instead of `python`

### "Connection error"
- Check your internet connection
- OLX might be temporarily blocking requests
- Wait a few minutes and try again

### Windows Users
If you're on Windows and get errors:
1. Open Command Prompt as Administrator
2. Use `py` instead of `python`:
   ```bash
   py olx_scraper.py
   ```

## Important Notes
- **No login required** - This scrapes public search results
- The script is respectful and includes delays between requests
- Results are saved in the same folder as the script
- You can open the CSV file in Excel or Google Sheets

## Example Output
```
OLX Car Cover Search Scraper
========================================
DISCLAIMER: This script is for educational purposes only.
Please respect OLX's terms of service and robots.txt
========================================

Do you want to proceed with scraping? (y/N): y
Enter number of pages to scrape (default 2): 3

Starting scrape for 3 pages...

Scraping page 1...
Fetching: https://www.olx.in/items/q-car-cover (Attempt 1)
Found 25 listings on page 1
Waiting before next page...

Scraping page 2...
Fetching: https://www.olx.in/items/q-car-cover?page=2 (Attempt 1)
Found 25 listings on page 2
Waiting before next page...

Scraping page 3...
Fetching: https://www.olx.in/items/q-car-cover?page=3 (Attempt 1)
Found 20 listings on page 3

Results saved to olx_car_cover_results.json
Results saved to olx_car_cover_results.csv

==================================================
SCRAPING SUMMARY
==================================================
Total listings found: 70
Search URL: https://www.olx.in/items/q-car-cover
Scraped at: 2025-01-27 15:30:45
```

That's it! You now have all the car cover listings from OLX saved in files on your computer.