import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests

# Send an HTTP request to the Bluesky profile URL
response = requests.get('https://bsky.app/profile/nytimes.com')
print(response)

# Set up custom headers to mimic a browser request
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

# Send a second request with custom headers
response = requests.get('https://bsky.app/profile/nytimes.com', headers=header)
print(response)

# Example cookies for the request
cookies = {
    'AWSALB': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
    'AWSALBCORS': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
}

# Custom headers for additional requests
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
    'Referer': 'https://bsky.social/',
    'Priority': 'u=0, i',
}

# Send another request with cookies and headers
response = requests.get(
    'https://bsky.app/profile/nytimes.com', cookies=cookies, headers=headers)

# Parse the HTML content of the response
soup = bs(response.text)
print(soup)

# Path to ChromeDriver (replace with the correct path for your system)
chrome_driver_path = "/usr/local/bin/chromedriver"
service = Service(chrome_driver_path)

# Initialize the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: run without a graphical interface
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

# URL of the Bluesky profile page
url = "https://bsky.app/profile/nytimes.com"
driver.get(url)

# Wait for the initial page load
time.sleep(5)

# Function to scroll down the page and load more posts
def scroll_and_load(driver, scroll_times=10, delay=2):
    action = ActionChains(driver)
    for _ in range(scroll_times):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down
        time.sleep(delay)

# Perform scrolling to load more posts
scroll_and_load(driver, scroll_times=10, delay=2)

# Get the rendered HTML content
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# List to store extracted posts
data_list = []

# Locate all post elements on the page
# General class for post elements
posts = soup.find_all("div", class_="css-175oi2r")

# Extract data from each post
for post in posts:
    try:
        # Extract the title
        title_element = post.find(
            "div", class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01")
        title = title_element.text.strip() if title_element else None

        # Extract the number of likes
        likes_element = post.find("div", {"data-testid": "likeCount"})
        likes = int(likes_element.text.strip()) if likes_element else 0

        # Extract the number of comments
        comment_count_element = post.find("div", {"data-testid": "replyBtn"})
        comment_count = int(comment_count_element.text.strip()) if comment_count_element else 0

        # Extract the text of comments
        comments = []
        comment_elements = post.find_all(
            "div", {"data-word-wrap": "1", "class": "css-146c3p1 r-1xnzce8"})
        for comment in comment_elements:
            comments.append(comment.text.strip())

        # Create a dictionary to represent the post data
        post_data = {
            "title": title,
            "likes": likes,
            "comment_count": comment_count,
            "comments": comments
        }

        # Add the post data to the list
        data_list.append(post_data)

    except Exception as e:
        print(f"Error processing a post: {e}")

# Close the browser
driver.quit()

# Display the collected posts
for post in data_list:
    print(post)

# Optional: Save the data to a CSV file
df = pd.DataFrame(data_list)
df.to_csv("bluesky_posts.csv", index=False, encoding="utf-8")
print("Data saved to 'bluesky_posts.csv'")
