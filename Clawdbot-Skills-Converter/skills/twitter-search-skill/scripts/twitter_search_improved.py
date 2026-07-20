#!/usr/bin/env python3
"""
Improved Twitter Advanced Search Script

Enhanced version with:
- Better default search queries for AI prompts
- Language filtering (default: English only)
- Engagement filtering (min likes/retweets/replies)
- Smart query construction
- Better error handling for rate limits

Usage:
    python twitter_search_improved.py <api_key> <query> [options]

Examples:
    # Search for AI prompts with minimum engagement
    python twitter_search_improved.py "$API_KEY" "AI prompt" --min-likes 10 --min-retweets 5

    # Search only English tweets
    python twitter_search_improved.py "$API_KEY" "prompt engineering" --lang en

    # Search with smart query for AI prompts
    python twitter_search_improved.py "$API_KEY" --smart-query "prompts" --min-likes 20
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install it with: pip install requests")
    sys.exit(1)


# Constants
API_BASE_URL = "https://api.twitterapi.io/twitter/tweet/advanced_search"
DEFAULT_MAX_RESULTS = 1000
RESULTS_PER_PAGE = 20


class TwitterSearchError(Exception):
    """Custom exception for Twitter search errors."""
    pass


# Predefined smart queries for AI prompts
SMART_QUERIES = {
    "prompts": [
        '"prompt engineering" OR "AI prompts" OR "ChatGPT prompts" OR "Claude prompts"',
        '"prompt template" OR "writing prompts" OR "AI writing"',
        '"best AI prompts" OR "effective prompts" OR "prompting tips"'
    ],
    "automation": [
        '"AI automation" OR "workflow automation" OR "no-code AI"',
        '"AI agents" OR "AI assistants" OR "AI tools"',
        '"automate with AI" OR "AI workflows" OR "AI productivity"'
    ],
    "tools": [
        '"AI tools" OR "AI software" OR "AI applications"',
        '"new AI" OR "AI technology" OR "AI platform"',
        '"AI startups" OR "AI companies" OR "AI services"'
    ],
    "clawdbot": [
        '"Clawdbot" OR "Clawdbot AI" OR "Clawdbot skills"'
    ]
}


def build_smart_query(topic: str, lang: Optional[str] = None, min_engagement: Optional[Dict[str, int]] = None) -> str:
    """
    Build an optimized search query for AI-related content.

    Args:
        topic: Topic key from SMART_QUERIES
        lang: Language code (e.g., 'en', 'ja')
        min_engagement: Dict with 'likes', 'retweets', 'replies' minimums

    Returns:
        Optimized search query string
    """
    # Get base queries for the topic
    base_queries = SMART_QUERIES.get(topic, SMART_QUERIES["prompts"])

    # Use the first query as base
    query = base_queries[0]

    # Add language filter
    if lang:
        query += f' lang:{lang}'

    # Add engagement filters
    if min_engagement:
        if min_engagement.get('retweets'):
            query += f' min_retweets:{min_engagement["retweets"]}'
        if min_engagement.get('likes'):
            query += f' min_faves:{min_engagement["likes"]}'
        if min_engagement.get('replies'):
            query += f' min_replies:{min_engagement["replies"]}'

    # Add date filter (last 30 days)
    since_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    query += f' since:{since_date}'

    return query


def get_api_key(api_key_arg: Optional[str]) -> str:
    """Get API key from argument or environment variable."""
    api_key = api_key_arg or os.environ.get("TWITTER_API_KEY")
    if not api_key:
        raise TwitterSearchError(
            "API key is required. Provide it as an argument or set TWITTER_API_KEY environment variable."
        )
    return api_key


def fetch_tweets(api_key: str, query: str, query_type: str = "Top", cursor: str = "") -> Dict[str, Any]:
    """Fetch a single page of tweets from the Twitter API."""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    params = {
        "query": query,
        "queryType": query_type,
        "cursor": cursor
    }

    try:
        response = requests.get(API_BASE_URL, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            raise TwitterSearchError("Rate limit exceeded. Please wait before making more requests.")
        elif response.status_code == 401:
            raise TwitterSearchError("Invalid API key. Please check your TWITTER_API_KEY.")
        else:
            raise TwitterSearchError(f"HTTP {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise TwitterSearchError(f"API request failed: {str(e)}")


def filter_tweets_by_engagement(tweets: List[Dict[str, Any]], min_likes: int = 0,
                                  min_retweets: int = 0, min_replies: int = 0) -> List[Dict[str, Any]]:
    """
    Filter tweets by minimum engagement metrics.

    Args:
        tweets: List of tweet objects
        min_likes: Minimum like count
        min_retweets: Minimum retweet count
        min_replies: Minimum reply count

    Returns:
        Filtered list of tweets
    """
    filtered = []
    for tweet in tweets:
        likes = tweet.get("likeCount", 0)
        retweets = tweet.get("retweetCount", 0)
        replies = tweet.get("replyCount", 0)

        if likes >= min_likes and retweets >= min_retweets and replies >= min_replies:
            filtered.append(tweet)

    return filtered


def filter_tweets_by_language(tweets: List[Dict[str, Any]], lang: str = "en") -> List[Dict[str, Any]]:
    """
    Filter tweets by language.

    Args:
        tweets: List of tweet objects
        lang: Language code (default: 'en' for English)

    Returns:
        Filtered list of tweets
    """
    return [t for t in tweets if t.get("lang") == lang]


def fetch_all_tweets(api_key: str, query: str, max_results: int = DEFAULT_MAX_RESULTS,
                     query_type: str = "Top", lang: Optional[str] = None,
                     min_likes: int = 0, min_retweets: int = 0, min_replies: int = 0) -> List[Dict[str, Any]]:
    """
    Fetch all tweets up to max_results with filtering.

    Args:
        api_key: Twitter API key
        query: Search query string
        max_results: Maximum number of results to fetch
        query_type: Query type ("Latest" or "Top")
        lang: Filter by language code
        min_likes: Minimum like count filter
        min_retweets: Minimum retweet count filter
        min_replies: Minimum reply count filter

    Returns:
        List of filtered tweet objects
    """
    all_tweets = []
    cursor = ""
    page_count = 0
    max_pages = (max_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    print(f"Fetching tweets with query: {query}", file=sys.stderr)

    while len(all_tweets) < max_results:
        try:
            data = fetch_tweets(api_key, query, query_type, cursor)
            page_count += 1

            # Extract tweets from response
            tweets = data.get("tweets", [])
            if not tweets:
                print(f"No more tweets found after {page_count} pages.", file=sys.stderr)
                break

            # Apply filters
            if lang:
                tweets = filter_tweets_by_language(tweets, lang)
                print(f"  Page {page_count}: {len(tweets)} tweets after language filter", file=sys.stderr)

            if min_likes > 0 or min_retweets > 0 or min_replies > 0:
                before_count = len(tweets)
                tweets = filter_tweets_by_engagement(tweets, min_likes, min_retweets, min_replies)
                print(f"  Page {page_count}: {before_count} -> {len(tweets)} after engagement filter", file=sys.stderr)

            all_tweets.extend(tweets)
            print(f"  Total collected: {len(all_tweets)}/{max_results}", file=sys.stderr)

            # Check if we've reached max_results
            if len(all_tweets) >= max_results:
                all_tweets = all_tweets[:max_results]
                break

            # Check if there's a next page
            has_next = data.get("has_next_page", False)
            if not has_next:
                print(f"No more pages available after {page_count} pages.", file=sys.stderr)
                break

            cursor = data.get("next_cursor", "")

            # Safety check to prevent infinite loops
            if page_count >= max_pages + 5:
                print(f"Warning: Reached maximum page limit ({page_count} pages)", file=sys.stderr)
                break

            # Small delay to avoid rate limiting
            import time
            time.sleep(0.5)

        except TwitterSearchError as e:
            print(f"Warning: Failed to fetch page {page_count + 1}: {str(e)}", file=sys.stderr)
            break

    return all_tweets


def extract_tweet_summary(tweet: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key information from a tweet for summary output."""
    author = tweet.get("author", {})

    return {
        "id": tweet.get("id"),
        "url": tweet.get("url"),
        "text": tweet.get("text"),
        "created_at": tweet.get("createdAt"),
        "lang": tweet.get("lang"),
        "metrics": {
            "retweets": tweet.get("retweetCount", 0),
            "replies": tweet.get("replyCount", 0),
            "likes": tweet.get("likeCount", 0),
            "quotes": tweet.get("quoteCount", 0),
            "views": tweet.get("viewCount", 0),
            "bookmarks": tweet.get("bookmarkCount", 0)
        },
        "author": {
            "username": author.get("userName"),
            "name": author.get("name"),
            "followers": author.get("followers", 0),
            "verified": author.get("isBlueVerified", False)
        },
        "hashtags": [h.get("text") for h in tweet.get("entities", {}).get("hashtags", [])],
        "mentions": [m.get("screen_name") for m in tweet.get("entities", {}).get("user_mentions", [])],
        "is_reply": tweet.get("isReply", False),
        "conversation_id": tweet.get("conversationId")
    }


def calculate_statistics(tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate statistics from tweets."""
    if not tweets:
        return {}

    total_likes = sum(t.get("metrics", {}).get("likes", 0) for t in tweets)
    total_retweets = sum(t.get("metrics", {}).get("retweets", 0) for t in tweets)
    total_replies = sum(t.get("metrics", {}).get("replies", 0) for t in tweets)
    total_quotes = sum(t.get("metrics", {}).get("quotes", 0) for t in tweets)
    total_views = sum(t.get("metrics", {}).get("views", 0) for t in tweets)

    # Language distribution
    languages = {}
    for t in tweets:
        lang = t.get("lang", "unknown")
        languages[lang] = languages.get(lang, 0) + 1

    # Top hashtags
    all_hashtags = []
    for t in tweets:
        all_hashtags.extend(t.get("hashtags", []))
    hashtag_counts = {}
    for tag in all_hashtags:
        hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1

    # Top mentioned users
    all_mentions = []
    for t in tweets:
        all_mentions.extend(t.get("mentions", []))
    mention_counts = {}
    for mention in all_mentions:
        mention_counts[mention] = mention_counts.get(mention, 0) + 1

    # Reply vs original tweets
    reply_count = sum(1 for t in tweets if t.get("is_reply", False))

    # Most influential authors (by followers)
    authors = {}
    for t in tweets:
        username = t.get("author", {}).get("username")
        if username:
            if username not in authors:
                authors[username] = {
                    "name": t.get("author", {}).get("name"),
                    "followers": t.get("author", {}).get("followers", 0),
                    "verified": t.get("author", {}).get("verified", False),
                    "tweet_count": 0
                }
            authors[username]["tweet_count"] += 1

    return {
        "total_tweets": len(tweets),
        "total_engagement": {
            "likes": total_likes,
            "retweets": total_retweets,
            "replies": total_replies,
            "quotes": total_quotes,
            "views": total_views
        },
        "averages": {
            "likes_per_tweet": round(total_likes / len(tweets), 2),
            "retweets_per_tweet": round(total_retweets / len(tweets), 2),
            "replies_per_tweet": round(total_replies / len(tweets), 2)
        },
        "language_distribution": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)),
        "top_hashtags": dict(sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
        "top_mentions": dict(sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
        "reply_ratio": round(reply_count / len(tweets) * 100, 2),
        "top_authors_by_followers": sorted(
            [{"username": k, **v} for k, v in authors.items()],
            key=lambda x: x["followers"],
            reverse=True
        )[:10],
        "most_active_authors": sorted(
            [{"username": k, **v} for k, v in authors.items()],
            key=lambda x: x["tweet_count"],
            reverse=True
        )[:10]
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Improved Twitter search with language and engagement filtering"
    )
    parser.add_argument("api_key", nargs="?", help="Twitter API key (or set TWITTER_API_KEY env var)")
    parser.add_argument("query", nargs="?", help="Search query (use --smart-query instead)")
    parser.add_argument("--smart-query", choices=["prompts", "automation", "tools", "clawdbot"],
                       help="Use predefined smart query templates")
    parser.add_argument("--max-results", type=int, default=DEFAULT_MAX_RESULTS,
                       help=f"Maximum results to fetch (default: {DEFAULT_MAX_RESULTS})")
    parser.add_argument("--query-type", choices=["Latest", "Top"], default="Top",
                       help="Query type (default: Top)")
    parser.add_argument("--format", choices=["json", "summary"], default="summary",
                       help="Output format (default: summary)")
    parser.add_argument("--lang", default="en",
                       help="Filter by language code (default: en)")
    parser.add_argument("--min-likes", type=int, default=0,
                       help="Minimum like count filter (default: 0)")
    parser.add_argument("--min-retweets", type=int, default=0,
                       help="Minimum retweet count filter (default: 0)")
    parser.add_argument("--min-replies", type=int, default=0,
                       help="Minimum reply count filter (default: 0)")
    parser.add_argument("--skip-lang-filter", action="store_true",
                       help="Skip language filtering in the query itself")

    args = parser.parse_args()

    try:
        # Get API key
        api_key = get_api_key(args.api_key)

        # Build query
        query = args.query
        if args.smart_query:
            min_engagement = {}
            if args.min_likes > 0:
                min_engagement['likes'] = args.min_likes
            if args.min_retweets > 0:
                min_engagement['retweets'] = args.min_retweets
            if args.min_replies > 0:
                min_engagement['replies'] = args.min_replies

            lang_param = None if args.skip_lang_filter else args.lang
            query = build_smart_query(args.smart_query, lang_param, min_engagement)

        if not query:
            parser.error("Either provide a query or use --smart-query")

        # Display search parameters
        print(f"🔍 Twitter Search (Improved)", file=sys.stderr)
        print(f"=" * 50, file=sys.stderr)
        print(f"Query: {query}", file=sys.stderr)
        print(f"Query type: {args.query_type}", file=sys.stderr)
        print(f"Max results: {args.max_results}", file=sys.stderr)
        print(f"Language filter: {args.lang}", file=sys.stderr)
        print(f"Min engagement: likes≥{args.min_likes}, retweets≥{args.min_retweets}, replies≥{args.min_replies}", file=sys.stderr)
        print(f"=" * 50, file=sys.stderr)
        print(file=sys.stderr)

        # Fetch tweets with filtering
        raw_tweets = fetch_all_tweets(
            api_key, query, args.max_results, args.query_type,
            args.lang if not args.skip_lang_filter else None,
            args.min_likes, args.min_retweets, args.min_replies
        )

        if not raw_tweets:
            print("No tweets found matching your criteria.", file=sys.stderr)
            sys.exit(0)

        print(f"\n✅ Successfully fetched {len(raw_tweets)} tweets.", file=sys.stderr)

        # Process tweets
        tweet_summaries = [extract_tweet_summary(t) for t in raw_tweets]
        statistics = calculate_statistics(tweet_summaries)

        # Output results
        result = {
            "query": query,
            "query_type": args.query_type,
            "filters": {
                "language": args.lang,
                "min_likes": args.min_likes,
                "min_retweets": args.min_retweets,
                "min_replies": args.min_replies
            },
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "total_tweets": len(tweet_summaries),
            "statistics": statistics,
            "tweets": tweet_summaries if args.format == "json" else []
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TwitterSearchError as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏸️  Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
