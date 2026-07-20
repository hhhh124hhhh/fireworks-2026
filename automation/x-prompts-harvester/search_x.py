#!/usr/bin/env python3
"""
X (Twitter) Search Module
Searches for AI prompts on X with specified keywords and filters.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class TwitterSearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.twitterapi.io/twitter"

    def search(self, query: str, max_results: int = 100, min_retweets: int = 20) -> List[Dict]:
        """
        Search for tweets matching the query.

        Args:
            query: Search query string
            max_results: Maximum number of results to fetch
            min_retweets: Minimum retweets to filter

        Returns:
            List of tweet dictionaries
        """
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        all_tweets = []
        next_token = None

        while len(all_tweets) < max_results:
            params = {
                "query": query,
                "max_results": min(100, max_results - len(all_tweets)),
                "tweet_fields": "created_at,public_metrics,author_id,lang,conversation_id",
                "expansions": "author_id",
                "user.fields": "username,name,public_metrics,verified"
            }

            if next_token:
                params["next_token"] = next_token

            try:
                response = requests.get(
                    f"{self.base_url}/search/recent",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()

                data = response.json()

                if "data" not in data:
                    break

                # Filter by minimum retweets
                for tweet in data["data"]:
                    metrics = tweet.get("public_metrics", {})
                    if metrics.get("retweet_count", 0) >= min_retweets:
                        all_tweets.append(tweet)

                next_token = data.get("meta", {}).get("next_token")
                if not next_token:
                    break

            except Exception as e:
                print(f"Error searching: {e}")
                break

        return all_tweets[:max_results]

    def build_prompt_queries(self) -> List[str]:
        """
        Build list of queries for AI prompt searching.

        Returns:
            List of search queries
        """
        queries = [
            # General AI prompt searches
            '("ChatGPT prompt" OR "GPT prompt" OR "AI prompt") min_retweets:20 lang:en -is:retweet',
            '("Claude prompt" OR "Claude AI prompt") min_retweets:20 lang:en -is:retweet',
            '("best prompt" OR "effective prompt") min_retweets:20 lang:en -is:retweet',
            '("prompt engineering" OR "prompt template") min_retweets:20 lang:en -is:retweet',

            # Task-specific prompts
            '("prompt for writing" OR "writing prompt") min_retweets:20 lang:en -is:retweet',
            '("prompt for coding" OR "code prompt") min_retweets:20 lang:en -is:retweet',
            '("prompt for email" OR "email prompt") min_retweets:20 lang:en -is:retweet',
            '("prompt for summary" OR "summary prompt") min_retweets:20 lang:en -is:retweet',

            # Chinese searches
            '("提示词" OR "prompt") min_retweets:20 lang:zh -is:retweet',
        ]

        return queries

    def extract_prompts_from_tweets(self, tweets: List[Dict]) -> List[Dict]:
        """
        Extract potential prompts from tweets.

        Args:
            tweets: List of tweet data

        Returns:
            List of extracted prompt candidates
        """
        prompts = []

        for tweet in tweets:
            text = tweet.get("text", "")
            metrics = tweet.get("public_metrics", {})

            # Filter for content that looks like prompts
            # Look for patterns like: "Act as...", "You are...", "Write a...", etc.
            prompt_indicators = [
                "act as", "you are a", "write a", "create a",
                "generate a", "help me", "can you", "i need you to",
                "your task is", "you should"
            ]

            text_lower = text.lower()
            if any(indicator in text_lower for indicator in prompt_indicators):
                prompts.append({
                    "text": text,
                    "author_id": tweet.get("author_id"),
                    "tweet_id": tweet.get("id"),
                    "created_at": tweet.get("created_at"),
                    "metrics": metrics,
                    "url": f"https://x.com/i/status/{tweet.get('id')}"
                })

        return prompts

    def search_prompts(self, max_results_per_query: int = 50) -> List[Dict]:
        """
        Search for AI prompts across multiple queries.

        Args:
            max_results_per_query: Maximum results per query

        Returns:
            List of unique prompt candidates
        """
        all_prompts = []
        seen_texts = set()

        queries = self.build_prompt_queries()

        for query in queries:
            print(f"Searching for: {query}")
            tweets = self.search(query, max_results=max_results_per_query)
            prompts = self.extract_prompts_from_tweets(tweets)

            for prompt in prompts:
                # Deduplicate by text content
                text_hash = hash(prompt["text"])
                if text_hash not in seen_texts:
                    seen_texts.add(text_hash)
                    all_prompts.append(prompt)

            print(f"Found {len(prompts)} prompts from this query")

        print(f"Total unique prompts found: {len(all_prompts)}")
        return all_prompts


def main():
    """Main function for testing."""
    api_key = os.environ.get("TWITTER_API_KEY")
    if not api_key:
        print("Error: TWITTER_API_KEY environment variable not set")
        print("Set it with: export TWITTER_API_KEY='your_key_here'")
        return

    searcher = TwitterSearcher(api_key)
    prompts = searcher.search_prompts(max_results_per_query=20)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"skills-generated/prompts_raw_{timestamp}.json"

    os.makedirs("skills-generated", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(prompts)} prompts to {output_file}")

    # Print sample
    print("\n=== Sample Prompts ===")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"\n{i}. {prompt['url']}")
        print(f"   {prompt['text'][:100]}...")
        print(f"   Retweets: {prompt['metrics']['retweet_count']}, Likes: {prompt['metrics']['like_count']}")


if __name__ == "__main__":
    main()
