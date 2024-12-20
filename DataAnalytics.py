import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests

# Sending a request to the URL
response = requests.get('https://bsky.app/profile/nytimes.com')
print(response)

# User-Agent to mimic a browser request
My_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

# Header for the request
header = {
    'user-agent': My_user_agent
}

# Sending another request with the User-Agent
response = requests.get('https://bsky.app/profile/nytimes.com', headers=header)
print(response)

# Cookies to handle session-based content
cookies = {
    'AWSALB': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
    'AWSALBCORS': 'fueERgSwBSzAPX/OHUdsfquSGXd/rnkUXjal+TCYydWqZsCC/S9yRcIZCFnc2v4q4QcNOXY2pS3nNmU6jWt53l3tcgiQ4mGqaEXFeSgkNIQFeRh7RgmqXCFNCyzN',
}

# Additional headers for the request
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': My_user_agent,
    'Referer': 'https://bsky.social/',
    'Priority': 'u=0, i',
}

# Making a request with cookies and headers
response = requests.get(
    'https://bsky.app/profile/nytimes.com', cookies=cookies, headers=headers)
soup = bs(response.text, "html.parser")
print(soup)

# Path to ChromeDriver (replace with your own path)
chrome_driver_path = r"C:\Users\gusta\Downloads\chromedriver.exe"
service = Service(chrome_driver_path)

# Initialize Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

# Target URL for scraping profile data
url = "https://bsky.app/profile/nytimes.com"
driver.get(url)

# Wait for the initial page load
time.sleep(5)

# Function to perform scrolling to load more posts
def scroll_and_load(driver, scroll_times=10, delay=2):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down
        time.sleep(delay)

# Perform scrolling to load additional posts
scroll_and_load(driver, scroll_times=10, delay=2)

# Get the rendered HTML from the page
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# List to store collected posts
posts_list = []

# Locate all posts on the page
# General class for posts
posts = soup.find_all("div", class_="css-175oi2r")

# Loop through each post to extract data
for post in posts:
    try:
        # Extract the post title
        title_element = post.find(
            "div", class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01")
        title = title_element.text.strip() if title_element else None

        # Extract the number of likes
        likes_element = post.find("div", {"data-testid": "likeCount"})
        likes = int(likes_element.text.strip()) if likes_element else 0

        # Extract the number of comments
        comment_count_element = post.find("div", {"data-testid": "replyBtn"})
        comment_count = int(comment_count_element.text.strip()) if comment_count_element else 0

        # Extract text from comments
        comments = []
        comment_elements = post.find_all(
            "div", {"data-word-wrap": "1", "class": "css-146c3p1 r-1xnzce8"})
        for comment in comment_elements:
            comments.append(comment.text.strip())

        # Create a dictionary for the post
        if title:
            post_data = {
                "title": title,
                "likes": likes,
                "comment_count": comment_count,
                "comments": comments
            }
            # Add the post data to the list
            posts_list.append(post_data)
    except Exception as e:
        print(f"Error processing a post: {e}")

# Close the browser
driver.quit()

# Display the collected posts
for post in posts_list:
    print(post)

# Optional: Save the data to a CSV file
df = pd.DataFrame(posts_list)
df.to_csv("bluesky_posts.csv", index=False, encoding="utf-8")
print("Data saved to 'bluesky_posts.csv'")
