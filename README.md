# BlueSky---WebScraping-

````markdown
# Bluesky Profile Scraper

A Python script to scrape posts from Bluesky profiles, including titles, likes, comments, and interaction counts.

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install pandas selenium beautifulsoup4 requests
  ```
````

- ChromeDriver (compatible with your Chrome version)

## Setting Up ChromeDriver

1. **Download ChromeDriver:**

   - Visit the [ChromeDriver downloads page](https://chromedriver.chromium.org/downloads).
   - Download the version matching your installed Google Chrome version.

2. **Check Chrome Version:**

   - Open Chrome and go to `chrome://settings/help` to find your version.

3. **Set the ChromeDriver Path:**

   - Extract ChromeDriver and copy its file path.
   - Update the line in the script:
     ```python
     chrome_driver_path = "/path/to/chromedriver"
     ```
   - Replace `/path/to/chromedriver` with the full path to the `chromedriver` executable.

4. **Add ChromeDriver to PATH (optional):**
   - Add the folder containing `chromedriver` to your system's PATH for easier access.

## Usage

1. Run the script:
   ```bash
   python scraper.py
   ```
2. Results are saved in `bluesky_posts.csv`.
