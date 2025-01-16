from atproto import Client
import pandas as pd
from pprint import pprint
import json
import re

# Initialize the Bluesky API client
client = Client()

# Authenticate with your Bluesky credentials
USERNAME = "vhfk.bsky.social"  # Replace with your Bluesky handle (e.g., 'you.bsky.social')
PASSWORD = "vinihessfroeskenzo"  # Replace with your Bluesky password


def fetch_political_posts_and_replies(client: Client, actor: str, max_posts: int, output_file: str) -> None:
    """
    Fetches up to max_posts posts with links containing "politics" and their replies, and saves to a CSV.

    Parameters:
    - client: The authenticated Bluesky client.
    - actor: The handle or DID of the actor.
    - max_posts: Maximum number of posts to fetch.
    - output_file: Name of the CSV file to save the data.
    """
    all_data = []  # List to store post and reply data
    cursor = None
    fetched_posts = 0

    while fetched_posts < max_posts:
        # Fetch a batch of posts
        response = client.app.bsky.feed.get_author_feed({'actor': actor, 'limit': 100, 'cursor': cursor})
        
        for feed_view in response.feed:
            if fetched_posts >= max_posts:
                break  # Stop if we've reached the max_posts limit

            # Check if the post has a link in the record.embed
            if hasattr(feed_view.post.record, 'embed') and feed_view.post.record.embed:
                embed = feed_view.post.record.embed
                if hasattr(embed, 'external') and embed.external:
                    url = embed.external.uri.lower()  # Get the URL and make it lowercase
                    
                    # Use a regular expression to check for "politics" in the URL
                    if re.search(r"\bpolitics\b", url):
                        # Prepare post data
                        post_data = {
                            "post_text": feed_view.post.record.text,
                            "post_timestamp": feed_view.post.indexed_at,
                            "post_link": url,
                            "replies": []
                        }

                        # Fetch replies if the post has any
                        if feed_view.post.reply_count > 0:
                            post_uri = feed_view.post.uri
                            thread_response = client.app.bsky.feed.get_post_thread({'uri': post_uri})
                            
                            if hasattr(thread_response.thread, 'replies'):
                                for reply in thread_response.thread.replies:
                                    reply_data = {
                                        "reply_text": reply.post.record.text,
                                        "reply_timestamp": reply.post.record.created_at
                                    }
                                    post_data["replies"].append(reply_data)

                        # Append the post and its replies to the data list
                        all_data.append(post_data)
                        fetched_posts += 1

        # Update cursor for the next batch
        cursor = response.cursor
        if not cursor:
            break  # No more posts to fetch

    # Save to a CSV file
    rows = []
    for post in all_data:
        for reply in post["replies"]:
            rows.append({
                "Post Text": post["post_text"],
                "Post Timestamp": post["post_timestamp"],
                "Post Link": post["post_link"],
                "Reply Text": reply["reply_text"],
                "Reply Timestamp": reply["reply_timestamp"]
            })
       
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    client.login(USERNAME, PASSWORD)
    fetch_political_posts_and_replies(client, "nbcnews.com", max_posts=1000, output_file="politics_posts_and_replies_NBC.csv")
