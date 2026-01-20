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

def safe_float(value):
    """Safely convert a value to float, return 'N/A' if not possible"""
    if value is None or value == '' or value == 'None' or value == 'null':
        return 'N/A'
    try:
        result = float(value)
        return result if result != 0 else 'N/A'
    except (ValueError, TypeError):
        return 'N/A'

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
                "current": safe_float(quote_data.get('05. price')),
                "previous_close": safe_float(quote_data.get('08. previous close')),
                "day_high": safe_float(quote_data.get('03. high')),
                "day_low": safe_float(quote_data.get('04. low')),
                "52_week_high": safe_float(data.get('52WeekHigh')),
                "52_week_low": safe_float(data.get('52WeekLow')),
            },

            # Valuation Metrics
            "valuation": {
                "market_cap": safe_float(data.get('MarketCapitalization')),
                "pe_ratio": safe_float(data.get('PERatio')),
                "forward_pe": safe_float(data.get('ForwardPE')),
                "price_to_book": safe_float(data.get('PriceToBookRatio')),
            },

            # Financial Performance
            "financials": {
                "revenue": safe_float(data.get('RevenueTTM')),
                "revenue_growth": safe_float(data.get('QuarterlyRevenueGrowthYOY')),
                "profit_margin": safe_float(data.get('ProfitMargin')),
                "earnings_growth": safe_float(data.get('QuarterlyEarningsGrowthYOY')),
            },

            # Balance Sheet
            "balance_sheet": {
                "total_cash": 'N/A',
                "total_debt": 'N/A',
                "debt_to_equity": safe_float(data.get('DebtToEquity')),
            },

            # Profitability
            "profitability": {
                "roe": safe_float(data.get('ReturnOnEquityTTM')),
                "gross_margin": safe_float(data.get('GrossProfitTTM')),
            },

            # Dividend Information
            "dividends": {
                "dividend_yield": safe_float(data.get('DividendYield')),
            },

            # Trading Information
            "trading": {
                "volume": safe_float(quote_data.get('06. volume')),
                "average_volume": 'N/A',
                "beta": safe_float(data.get('Beta')),
            },

            # Analyst Recommendations
            "analyst": {
                "target_price": safe_float(data.get('AnalystTargetPrice')),
                "recommendation": 'N/A',
            },

            # Historical Performance
            "performance": {
                "1_month": safe_float(data.get('50DayMovingAverage')),
                "3_months": 'N/A',
                "6_months": 'N/A',
                "1_year": safe_float(data.get('52WeekChange')),
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
