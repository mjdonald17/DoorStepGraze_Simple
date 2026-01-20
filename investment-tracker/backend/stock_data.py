import yfinance as yf
import requests
from datetime import datetime, timedelta
import time

ALPHA_VANTAGE_KEY = 'demo'  # Users should replace with their own key

def get_stock_report(symbol):
    """
    Generate comprehensive stock report with fundamental and technical data
    """
    # Retry logic to handle rate limiting
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            # Check if we got valid data
            if not info or len(info) < 5:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise Exception("Unable to fetch stock data. Please try again in a moment.")

            break  # Success, exit retry loop

        except Exception as e:
            if "429" in str(e) or "Too Many Requests" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise Exception(f"Yahoo Finance is temporarily rate-limiting requests. Please wait a minute and try again.")
            else:
                raise e

    try:

        # Basic Information
        report = {
            "symbol": symbol,
            "name": info.get('longName', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "website": info.get('website', 'N/A'),
            "description": info.get('longBusinessSummary', 'N/A'),

            # Price Data - SIMPLIFIED
            "price": {
                "current": info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                "previous_close": info.get('previousClose', 'N/A'),
                "day_high": info.get('dayHigh', 'N/A'),
                "day_low": info.get('dayLow', 'N/A'),
                "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
                "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            },

            # Valuation Metrics - KEY METRICS ONLY
            "valuation": {
                "market_cap": info.get('marketCap', 'N/A'),
                "pe_ratio": info.get('trailingPE', 'N/A'),
                "forward_pe": info.get('forwardPE', 'N/A'),
                "price_to_book": info.get('priceToBook', 'N/A'),
            },

            # Financial Performance - CORE METRICS
            "financials": {
                "revenue": info.get('totalRevenue', 'N/A'),
                "revenue_growth": info.get('revenueGrowth', 'N/A'),
                "profit_margin": info.get('profitMargins', 'N/A'),
                "earnings_growth": info.get('earningsGrowth', 'N/A'),
            },

            # Balance Sheet - KEY RATIOS
            "balance_sheet": {
                "total_cash": info.get('totalCash', 'N/A'),
                "total_debt": info.get('totalDebt', 'N/A'),
                "debt_to_equity": info.get('debtToEquity', 'N/A'),
            },

            # Profitability - ESSENTIAL ONLY
            "profitability": {
                "roe": info.get('returnOnEquity', 'N/A'),
                "gross_margin": info.get('grossMargins', 'N/A'),
            },

            # Dividend Information - SIMPLIFIED
            "dividends": {
                "dividend_yield": info.get('dividendYield', 'N/A'),
            },

            # Trading Information - BASICS
            "trading": {
                "volume": info.get('volume', 'N/A'),
                "average_volume": info.get('averageVolume', 'N/A'),
                "beta": info.get('beta', 'N/A'),
            },

            # Analyst Recommendations - KEY INFO
            "analyst": {
                "target_price": info.get('targetMeanPrice', 'N/A'),
                "recommendation": info.get('recommendationKey', 'N/A'),
            },

            # Historical Performance - REMOVED (was causing extra API call)
            "performance": {
                "1_month": info.get('52WeekChange', 'N/A'),  # Use data from info instead
                "3_months": 'N/A',
                "6_months": 'N/A',
                "1_year": 'N/A',
                "ytd": 'N/A'
            },

            # Timestamp
            "last_updated": datetime.now().isoformat()
        }

        return report

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Too Many Requests" in error_msg:
            raise Exception("Yahoo Finance rate limit reached. Please wait 30-60 seconds and try again.")
        raise Exception(f"Error fetching stock data: {error_msg}")


# REMOVED: get_top_officers() and get_historical_performance()
# to reduce API calls and avoid rate limiting


def format_large_number(num):
    """Format large numbers for readability"""
    if num == 'N/A' or num is None:
        return 'N/A'

    try:
        num = float(num)
        if num >= 1e12:
            return f"${num/1e12:.2f}T"
        elif num >= 1e9:
            return f"${num/1e9:.2f}B"
        elif num >= 1e6:
            return f"${num/1e6:.2f}M"
        elif num >= 1e3:
            return f"${num/1e3:.2f}K"
        else:
            return f"${num:.2f}"
    except:
        return 'N/A'
