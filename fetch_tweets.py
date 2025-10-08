"""Fetch tweets from monitored X accounts"""
import os
import json
import requests
from datetime import datetime
from config import MONITORED_ACCOUNTS, SEEKER_KEYWORDS, TWEETS_PER_ACCOUNT

def get_user_id(username, bearer_token):
    """Get user ID from username"""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        print(f"Error getting user ID for {username}: {response.text}")
        return None

def get_user_tweets(user_id, bearer_token, max_results=10):
    """Get recent tweets from a user"""
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text,public_metrics"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error getting tweets: {response.text}")
        return []

def is_seeker_related(tweet_text):
    """Check if tweet is related to Seeker"""
    tweet_lower = tweet_text.lower()
    return any(keyword.lower() in tweet_lower for keyword in SEEKER_KEYWORDS)

def fetch_all_tweets():
    """Fetch tweets from all monitored accounts"""
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("Error: TWITTER_BEARER_TOKEN not set")
        return []

    all_tweets = []

    for username in MONITORED_ACCOUNTS:
        print(f"Fetching tweets from @{username}...")
        user_id = get_user_id(username, bearer_token)

        if user_id:
            tweets = get_user_tweets(user_id, bearer_token, TWEETS_PER_ACCOUNT)

            for tweet in tweets:
                if is_seeker_related(tweet["text"]):
                    all_tweets.append({
                        "username": username,
                        "tweet_id": tweet["id"],
                        "text": tweet["text"],
                        "created_at": tweet["created_at"],
                        "url": f"https://twitter.com/{username}/status/{tweet['id']}",
                        "likes": tweet["public_metrics"]["like_count"],
                        "retweets": tweet["public_metrics"]["retweet_count"]
                    })

    return all_tweets

if __name__ == "__main__":
    tweets = fetch_all_tweets()
    print(f"\nFound {len(tweets)} Seeker-related tweets")

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/raw_tweets.json", "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)

    print("Saved to data/raw_tweets.json")
