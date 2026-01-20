import requests
from datetime import datetime
import time

# Alpha Vantage API (free tier: 25 requests/day)
# Get your free API key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_KEY = 'demo'  # Replace with your free API key

# Simple cache to avoid re-fetching the same stock
_stock_cache = {}
_last_request_time = 0
_MIN_REQUEST_INTERVAL = 2  # 2 seconds between requests

def get_stock_report(symbol):
    """
    Generate stock report using Alpha Vantage API
    """
    global _last_request_time

    # Check cache first (valid for 5 minutes)
    cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M')}"
    if cache_key in _stock_cache:
        return _stock_cache[cache_key]

    # Enforce minimum time between requests
    time_since_last = time.time() - _last_request_time
    if time_since_last < _MIN_REQUEST_INTERVAL:
        wait_time = _MIN_REQUEST_INTERVAL - time_since_last
        time.sleep(wait_time)

    try:
        # Get company overview from Alpha Vantage
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        _last_request_time = time.time()

        data = response.json()

        # Check if we got valid data
        if not data or 'Symbol' not in data:
            if 'Note' in data:
                raise Exception("API rate limit reached. Alpha Vantage free tier allows 25 requests/day and 5/minute. Please wait a minute or get a free API key at https://www.alphavantage.co/support/#api-key")
            raise Exception(f"Unable to fetch data for {symbol}. The stock symbol may be invalid or Alpha Vantage is temporarily unavailable.")

        # Get current quote
        quote_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        time.sleep(1)  # Small delay between requests
        quote_response = requests.get(quote_url, timeout=10)
        quote_data = quote_response.json().get('Global Quote', {})

        # Build simplified report
        report = {
            "symbol": symbol,
            "name": data.get('Name', 'N/A'),
            "sector": data.get('Sector', 'N/A'),
            "industry": data.get('Industry', 'N/A'),
            "website": 'N/A',
            "description": data.get('Description', 'N/A'),

            # Price Data
            "price": {
                "current": float(quote_data.get('05. price', 0)) if quote_data.get('05. price') else 'N/A',
                "previous_close": float(quote_data.get('08. previous close', 0)) if quote_data.get('08. previous close') else 'N/A',
                "day_high": float(quote_data.get('03. high', 0)) if quote_data.get('03. high') else 'N/A',
                "day_low": float(quote_data.get('04. low', 0)) if quote_data.get('04. low') else 'N/A',
                "52_week_high": float(data.get('52WeekHigh', 0)) if data.get('52WeekHigh') else 'N/A',
                "52_week_low": float(data.get('52WeekLow', 0)) if data.get('52WeekLow') else 'N/A',
            },

            # Valuation Metrics
            "valuation": {
                "market_cap": float(data.get('MarketCapitalization', 0)) if data.get('MarketCapitalization') else 'N/A',
                "pe_ratio": float(data.get('PERatio', 0)) if data.get('PERatio') else 'N/A',
                "forward_pe": float(data.get('ForwardPE', 0)) if data.get('ForwardPE') else 'N/A',
                "price_to_book": float(data.get('PriceToBookRatio', 0)) if data.get('PriceToBookRatio') else 'N/A',
            },

            # Financial Performance
            "financials": {
                "revenue": float(data.get('RevenueTTM', 0)) if data.get('RevenueTTM') else 'N/A',
                "revenue_growth": float(data.get('QuarterlyRevenueGrowthYOY', 0)) if data.get('QuarterlyRevenueGrowthYOY') else 'N/A',
                "profit_margin": float(data.get('ProfitMargin', 0)) if data.get('ProfitMargin') else 'N/A',
                "earnings_growth": float(data.get('QuarterlyEarningsGrowthYOY', 0)) if data.get('QuarterlyEarningsGrowthYOY') else 'N/A',
            },

            # Balance Sheet
            "balance_sheet": {
                "total_cash": 'N/A',
                "total_debt": 'N/A',
                "debt_to_equity": float(data.get('DebtToEquity', 0)) if data.get('DebtToEquity') else 'N/A',
            },

            # Profitability
            "profitability": {
                "roe": float(data.get('ReturnOnEquityTTM', 0)) if data.get('ReturnOnEquityTTM') else 'N/A',
                "gross_margin": float(data.get('GrossProfitTTM', 0)) if data.get('GrossProfitTTM') else 'N/A',
            },

            # Dividend Information
            "dividends": {
                "dividend_yield": float(data.get('DividendYield', 0)) if data.get('DividendYield') else 'N/A',
            },

            # Trading Information
            "trading": {
                "volume": float(quote_data.get('06. volume', 0)) if quote_data.get('06. volume') else 'N/A',
                "average_volume": 'N/A',
                "beta": float(data.get('Beta', 0)) if data.get('Beta') else 'N/A',
            },

            # Analyst Recommendations
            "analyst": {
                "target_price": float(data.get('AnalystTargetPrice', 0)) if data.get('AnalystTargetPrice') else 'N/A',
                "recommendation": 'N/A',
            },

            # Historical Performance
            "performance": {
                "1_month": float(data.get('50DayMovingAverage', 0)) if data.get('50DayMovingAverage') else 'N/A',
                "3_months": 'N/A',
                "6_months": 'N/A',
                "1_year": float(data.get('52WeekChange', 0)) if data.get('52WeekChange') else 'N/A',
                "ytd": 'N/A'
            },

            # Timestamp
            "last_updated": datetime.now().isoformat()
        }

        # Cache the result for 5 minutes
        _stock_cache[cache_key] = report

        return report

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: Unable to connect to Alpha Vantage. Check your internet connection.")
    except Exception as e:
        error_msg = str(e)
        raise Exception(f"Error: {error_msg}")


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
