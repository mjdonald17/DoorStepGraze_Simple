import requests
import yfinance as yf
from datetime import datetime, timedelta
import praw
import os
import time

# NewsAPI configuration (users should get their own free key from https://newsapi.org)
NEWS_API_KEY = 'demo'  # Replace with actual key

# Reddit configuration (optional - for engagement metrics)
REDDIT_CLIENT_ID = None
REDDIT_CLIENT_SECRET = None
REDDIT_USER_AGENT = 'investment-tracker:v1.0'


def get_stock_news(symbol):
    """
    Aggregate news from multiple sources with engagement metrics
    """
    all_news = []

    # 1. Get news from yfinance (Yahoo Finance)
    yahoo_news = get_yahoo_news(symbol)
    all_news.extend(yahoo_news)

    # Add delay to avoid rate limiting
    time.sleep(1)

    # 2. Get news from NewsAPI
    newsapi_news = get_newsapi_news(symbol)
    all_news.extend(newsapi_news)

    # Add delay to avoid rate limiting
    time.sleep(0.5)

    # 3. Get Reddit discussions (for engagement metrics)
    reddit_posts = get_reddit_discussions(symbol)
    all_news.extend(reddit_posts)

    # Sort by engagement score (descending)
    all_news.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)

    return {
        "symbol": symbol,
        "total_articles": len(all_news),
        "news": all_news,
        "last_updated": datetime.now().isoformat()
    }


def get_yahoo_news(symbol):
    """Get news from Yahoo Finance via yfinance"""
    news_items = []
    try:
        # Add small delay before API call
        time.sleep(0.5)

        stock = yf.Ticker(symbol)
        news = stock.news

        for item in news:
            news_items.append({
                "title": item.get('title', 'N/A'),
                "source": item.get('publisher', 'Yahoo Finance'),
                "url": item.get('link', ''),
                "published_date": datetime.fromtimestamp(item.get('providerPublishTime', 0)).isoformat() if item.get('providerPublishTime') else 'N/A',
                "thumbnail": item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url', ''),
                "engagement_score": 0,  # Yahoo doesn't provide engagement metrics
                "engagement_type": 'N/A',
                "type": 'news'
            })
    except Exception as e:
        print(f"Error fetching Yahoo Finance news: {e}")

    return news_items


def get_newsapi_news(symbol):
    """Get news from NewsAPI"""
    news_items = []

    if NEWS_API_KEY == 'demo':
        # Return empty if using demo key
        return news_items

    try:
        # Get company info for better search
        stock = yf.Ticker(symbol)
        company_name = stock.info.get('longName', symbol)

        # Calculate date range (last 7 days)
        to_date = datetime.now()
        from_date = to_date - timedelta(days=7)

        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': f'{symbol} OR "{company_name}"',
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'sortBy': 'popularity',
            'language': 'en',
            'apiKey': NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            for article in articles[:10]:  # Limit to top 10
                news_items.append({
                    "title": article.get('title', 'N/A'),
                    "source": article.get('source', {}).get('name', 'Unknown'),
                    "url": article.get('url', ''),
                    "published_date": article.get('publishedAt', 'N/A'),
                    "thumbnail": article.get('urlToImage', ''),
                    "description": article.get('description', ''),
                    "engagement_score": 0,  # NewsAPI doesn't provide engagement
                    "engagement_type": 'N/A',
                    "type": 'news'
                })

    except Exception as e:
        print(f"Error fetching NewsAPI news: {e}")

    return news_items


def get_reddit_discussions(symbol):
    """Get Reddit discussions with engagement metrics"""
    posts = []

    # If no Reddit credentials, skip
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        return posts

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Search in relevant subreddits
        subreddits = ['stocks', 'investing', 'wallstreetbets', 'StockMarket']

        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)

            # Search for the stock symbol
            for submission in subreddit.search(symbol, time_filter='week', limit=5):
                # Calculate engagement score (upvotes + comments)
                engagement_score = submission.score + submission.num_comments

                posts.append({
                    "title": submission.title,
                    "source": f"r/{subreddit_name}",
                    "url": f"https://reddit.com{submission.permalink}",
                    "published_date": datetime.fromtimestamp(submission.created_utc).isoformat(),
                    "thumbnail": '',
                    "description": submission.selftext[:200] if submission.selftext else '',
                    "engagement_score": engagement_score,
                    "engagement_details": {
                        "upvotes": submission.score,
                        "comments": submission.num_comments,
                        "upvote_ratio": submission.upvote_ratio
                    },
                    "engagement_type": 'social',
                    "type": 'discussion'
                })

    except Exception as e:
        print(f"Error fetching Reddit discussions: {e}")

    return posts


def get_engagement_estimate(news_item):
    """
    Estimate how widely read an article is based on available metrics
    Returns a score and a description
    """
    score = news_item.get('engagement_score', 0)

    if score == 0:
        return "Unknown", "Engagement data not available"
    elif score < 100:
        return "Low", f"~{score} interactions"
    elif score < 500:
        return "Moderate", f"~{score} interactions"
    elif score < 2000:
        return "High", f"~{score} interactions"
    else:
        return "Very High", f"~{score}+ interactions"


def add_sentiment_analysis(news_items):
    """
    Add basic sentiment analysis to news items
    This is a placeholder for more sophisticated sentiment analysis
    """
    # Could integrate with sentiment analysis APIs like:
    # - VADER sentiment
    # - TextBlob
    # - FinBERT (financial sentiment)
    pass
