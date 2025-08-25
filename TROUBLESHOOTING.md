# Troubleshooting Guide for OLX Scraper

## Common Issues and Solutions

### 1. Timeout Errors (Most Common)
**Error**: `HTTPSConnectionPool(host='www.olx.in', port=443): Read timed out`

**Possible Causes & Solutions**:

#### A. OLX is blocking your IP
- **Solution**: Use a VPN and try from a different location
- **Test**: Open https://www.olx.in/items/q-car-cover in your browser
- **If browser works**: OLX is likely blocking automated requests from your IP

#### B. Network/ISP Issues
- **Solution**: 
  - Check your internet connection
  - Try from a different network (mobile hotspot)
  - Contact your ISP if OLX is blocked

#### C. OLX Anti-Bot Protection
- **Solution**: 
  - Wait 30-60 minutes before trying again
  - Use the improved scraper with random delays
  - Try during off-peak hours (early morning/late night)

### 2. No Listings Found
**Possible Causes**:
- Page structure changed
- Being redirected to a different page
- Content loaded via JavaScript

**Solutions**:
1. Run the test script: `python test_connection.py`
2. Check the saved HTML files for manual inspection
3. Update selectors if page structure changed

### 3. SSL/Certificate Errors
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
- Update your Python certificates
- Or modify the script to use `verify=False` (less secure)

### 4. Permission/Module Errors
**Error**: `ModuleNotFoundError` or `Permission denied`

**Solutions**:
```bash
# Install missing modules
pip install requests beautifulsoup4 lxml

# On Windows, try:
py -m pip install requests beautifulsoup4 lxml

# On Mac/Linux with permission issues:
pip3 install --user requests beautifulsoup4 lxml
```

## Step-by-Step Debugging

### Step 1: Test Basic Connectivity
```bash
python test_connection.py
```
This will test if you can reach OLX at all.

### Step 2: Check Browser Access
1. Open https://www.olx.in/items/q-car-cover in your browser
2. If it doesn't load → Network/ISP issue
3. If it loads → OLX is blocking the scraper

### Step 3: Try Different Approaches
If browser works but scraper doesn't:

#### Option A: Use VPN
1. Connect to a VPN (different country)
2. Run the scraper again

#### Option B: Wait and Retry
1. Wait 1-2 hours
2. Try again during off-peak hours

#### Option C: Use Different Headers
The improved scraper includes better headers that mimic a real browser.

## Regional Restrictions

OLX might be blocked or restricted in some regions:

### India
- Should work normally
- If blocked, try VPN to different Indian city

### Other Countries
- OLX India might block international IPs
- Use VPN with Indian server

## Alternative Solutions

### 1. Manual Method
If scraping fails completely:
1. Open the search page in browser
2. Use browser's "Save Page As" → Complete webpage
3. Parse the saved HTML file locally

### 2. Browser Automation
Consider using Selenium WebDriver:
```python
from selenium import webdriver
# This opens a real browser and is harder to block
```

### 3. API Alternative
Check if OLX provides an official API (they might for business users).

## Success Indicators

### Good Signs ✅
- Response size > 10,000 bytes
- Page title contains "OLX"
- HTML contains listing elements
- No "blocked" or "captcha" in content

### Bad Signs ❌
- Response size < 1,000 bytes
- Timeout errors
- "Access denied" or "blocked" messages
- CAPTCHA pages

## Getting Help

If none of these solutions work:

1. **Share the test results**: Run `python test_connection.py` and share the output
2. **Check saved HTML**: Look at the saved HTML files to see what OLX is returning
3. **Try different times**: OLX might have different blocking rules at different times
4. **Regional variations**: OLX behavior might vary by location

## Last Resort Options

1. **Use a different computer/network**
2. **Try mobile data instead of WiFi**
3. **Use a cloud server** (AWS, Google Cloud) to run the scraper
4. **Contact OLX** for official API access (for business use)

Remember: Web scraping should always be done respectfully and in compliance with the website's terms of service.