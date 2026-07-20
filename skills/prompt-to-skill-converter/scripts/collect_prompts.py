#!/usr/bin/env python3
"""
Prompt Collection Script

Collects AI prompts from X (Twitter) using the twitter-search skill.
Saves results to structured JSON for further processing.
"""

import json
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Default parameters
DEFAULT_MAX_RESULTS = 200
DEFAULT_MIN_LIKES = 20
DEFAULT_MIN_RETWEETS = 10
DEFAULT_QUERY = "prompts"


def load_twitter_api_key():
    """Load Twitter API key from environment."""
    import os

    api_key = os.environ.get("TWITTER_API_KEY")
    if not api_key:
        # Try to load from .bashrc or .zshrc
        home = Path.home()
        for bashrc_file in [home / ".bashrc", home / ".zshrc"]:
            if bashrc_file.exists():
                with open(bashrc_file) as f:
                    for line in f:
                        if line.strip().startswith("export TWITTER_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
                if api_key:
                    break

    if not api_key:
        print("ERROR: Twitter API key not found")
        print("Set TWITTER_API_KEY in ~/.bashrc or ~/.zshrc, or pass --api-key")
        sys.exit(1)

    return api_key


def build_search_query(query_type="prompts", lang="en", min_likes=None, min_retweets=None):
    """Build search query based on parameters."""
    query_templates = {
        "prompts": '"prompt engineering" OR "ChatGPT prompts" OR "Claude prompts" OR "AI prompts"',
        "automation": '"AI automation" OR "workflow automation" OR "agent" OR "AI tools"',
        "tools": '"AI tool" OR "AI software" OR "AI app" OR "machine learning tool"',
        "coding": '"coding assistant" OR "code generation" OR "AI programmer" OR "code helper"',
        "writing": '"AI writing" OR "content generation" OR "writing assistant" OR "copywriting"',
    }

    base_query = query_templates.get(query_type, query_type)

    # Add engagement filters if specified
    if min_likes:
        base_query += f" min_faves:{min_likes}"
    if min_retweets:
        base_query += f" min_retweets:{min_retweets}"

    # Add language filter
    if lang:
        base_query += f" lang:{lang}"

    return base_query


def search_twitter(
    api_key,
    query,
    max_results=200,
    query_type="Top",
    output_format="json",
):
    """Execute Twitter search using the improved script."""
    skill_path = Path("/root/clawd/skills/twitter-search-skill")
    script_path = skill_path / "scripts" / "twitter_search_improved.py"

    if not script_path.exists():
        print(f"ERROR: Twitter search script not found at {script_path}")
        print("Ensure twitter-search-skill is installed")
        sys.exit(1)

    # Build command
    cmd = [
        "python3",
        str(script_path),
        api_key,
        query,
        "--max-results",
        str(max_results),
        "--query-type",
        query_type,
        "--format",
        output_format,
    ]

    print(f"Running: {' '.join(cmd)}")
    print(f"Query: {query}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Twitter search failed")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def parse_results(raw_output):
    """Parse Twitter search results into structured data."""
    try:
        data = json.loads(raw_output)

        # Extract relevant fields
        tweets = []
        if isinstance(data, dict) and "tweets" in data:
            tweets = data["tweets"]
        elif isinstance(data, list):
            tweets = data

        # Normalize tweet data
        normalized = []
        for tweet in tweets:
            normalized_tweet = {
                "id": tweet.get("id", ""),
                "text": tweet.get("text", ""),
                "author": tweet.get("author", {}).get("username", tweet.get("author_screen_name", "")),
                "author_display": tweet.get("author", {}).get("name", ""),
                "author_followers": tweet.get("author", {}).get("public_metrics", {}).get("followers_count", 0),
                "created_at": tweet.get("created_at", ""),
                "metrics": {
                    "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                    "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0),
                    "replies": tweet.get("public_metrics", {}).get("reply_count", 0),
                    "quotes": tweet.get("public_metrics", {}).get("quote_count", 0),
                    "views": tweet.get("public_metrics", {}).get("impression_count", 0),
                },
                "url": f"https://x.com/{tweet.get('author', {}).get('username', '')}/status/{tweet.get('id', '')}",
                "collected_at": datetime.now().isoformat(),
            }
            normalized.append(normalized_tweet)

        return {
            "query": data.get("query", ""),
            "total_count": len(normalized),
            "collected_at": datetime.now().isoformat(),
            "tweets": normalized,
        }

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON output")
        print(f"Exception: {e}")
        sys.exit(1)


def filter_prompt_candidates(tweets):
    """Filter tweets that are likely to contain AI prompts."""
    prompt_keywords = [
        "prompt",
        "template",
        "here's a prompt",
        "try this prompt",
        "use this prompt",
        "chatgpt",
        "claude",
        "gpt-4",
        "prompt engineering",
        "system prompt",
        "custom instruction",
    ]

    prompt_tweets = []
    for tweet in tweets:
        text_lower = tweet["text"].lower()
        # Check if tweet contains prompt-related keywords
        if any(keyword in text_lower for keyword in prompt_keywords):
            # Also check if it has some engagement (likes or retweets)
            if tweet["metrics"]["likes"] > 0 or tweet["metrics"]["retweets"] > 0:
                prompt_tweets.append(tweet)

    return prompt_tweets


def save_results(data, output_path):
    """Save results to JSON file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(data['tweets'])} tweets to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Collect AI prompts from X (Twitter)"
    )
    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help="Search query or smart query type (prompts, automation, tools, coding, writing)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help="Maximum number of tweets to collect",
    )
    parser.add_argument(
        "--min-likes",
        type=int,
        default=DEFAULT_MIN_LIKES,
        help="Minimum number of likes",
    )
    parser.add_argument(
        "--min-retweets",
        type=int,
        default=DEFAULT_MIN_RETWEETS,
        help="Minimum number of retweets",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Language filter (e.g., en, zh, etc.)",
    )
    parser.add_argument(
        "--query-type",
        choices=["Top", "Latest"],
        default="Top",
        help="Twitter query type",
    )
    parser.add_argument(
        "--api-key",
        help="Twitter API key (overrides environment)",
    )
    parser.add_argument(
        "--output",
        default="/tmp/prompts.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--filter-prompts",
        action="store_true",
        help="Filter for likely prompt candidates",
    )

    args = parser.parse_args()

    # Load API key
    api_key = args.api_key or load_twitter_api_key()

    # Build query
    if args.query in ["prompts", "automation", "tools", "coding", "writing"]:
        query = build_search_query(
            query_type=args.query,
            lang=args.lang,
            min_likes=args.min_likes,
            min_retweets=args.min_retweets,
        )
    else:
        query = args.query

    # Execute search
    print(f"\n🔍 Searching Twitter for: {query}")
    print(f"📊 Max results: {args.max_results}")
    print(f"👍 Min likes: {args.min_likes}")
    print(f"🔄 Min retweets: {args.min_retweets}")
    print()

    raw_results = search_twitter(
        api_key=api_key,
        query=query,
        max_results=args.max_results,
        query_type=args.query_type,
    )

    # Parse results
    parsed_data = parse_results(raw_results)
    print(f"✅ Found {parsed_data['total_count']} tweets")

    # Filter for prompt candidates if requested
    if args.filter_prompts:
        prompt_tweets = filter_prompt_candidates(parsed_data["tweets"])
        print(f"🎯 Filtered to {len(prompt_tweets)} prompt candidates")
        parsed_data["tweets"] = prompt_tweets
        parsed_data["total_count"] = len(prompt_tweets)
        parsed_data["filtered"] = True

    # Save results
    save_results(parsed_data, args.output)

    # Print summary
    print("\n📈 Summary:")
    print(f"  Total tweets: {parsed_data['total_count']}")
    if parsed_data["total_count"] > 0:
        total_likes = sum(t["metrics"]["likes"] for t in parsed_data["tweets"])
        total_retweets = sum(t["metrics"]["retweets"] for t in parsed_data["tweets"])
        avg_likes = total_likes / parsed_data["total_count"]
        avg_retweets = total_retweets / parsed_data["total_count"]
        print(f"  Total likes: {total_likes}")
        print(f"  Total retweets: {total_retweets}")
        print(f"  Avg likes per tweet: {avg_likes:.1f}")
        print(f"  Avg retweets per tweet: {avg_retweets:.1f}")

    print(f"\n✅ Collection complete!")
    print(f"📁 Output: {args.output}")
    print(f"Next step: Run evaluate_prompts.py to score and rank prompts")


if __name__ == "__main__":
    main()
