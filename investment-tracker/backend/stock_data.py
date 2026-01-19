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

            # Price Data
            "price": {
                "current": info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                "previous_close": info.get('previousClose', 'N/A'),
                "open": info.get('open', 'N/A'),
                "day_high": info.get('dayHigh', 'N/A'),
                "day_low": info.get('dayLow', 'N/A'),
                "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
                "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            },

            # Valuation Metrics
            "valuation": {
                "market_cap": info.get('marketCap', 'N/A'),
                "enterprise_value": info.get('enterpriseValue', 'N/A'),
                "pe_ratio": info.get('trailingPE', 'N/A'),
                "forward_pe": info.get('forwardPE', 'N/A'),
                "peg_ratio": info.get('pegRatio', 'N/A'),
                "price_to_book": info.get('priceToBook', 'N/A'),
                "price_to_sales": info.get('priceToSalesTrailing12Months', 'N/A'),
                "ev_to_revenue": info.get('enterpriseToRevenue', 'N/A'),
                "ev_to_ebitda": info.get('enterpriseToEbitda', 'N/A'),
            },

            # Financial Performance
            "financials": {
                "revenue": info.get('totalRevenue', 'N/A'),
                "revenue_growth": info.get('revenueGrowth', 'N/A'),
                "gross_profit": info.get('grossProfits', 'N/A'),
                "ebitda": info.get('ebitda', 'N/A'),
                "net_income": info.get('netIncomeToCommon', 'N/A'),
                "earnings_growth": info.get('earningsGrowth', 'N/A'),
                "profit_margin": info.get('profitMargins', 'N/A'),
                "operating_margin": info.get('operatingMargins', 'N/A'),
                "free_cash_flow": info.get('freeCashflow', 'N/A'),
            },

            # Balance Sheet
            "balance_sheet": {
                "total_cash": info.get('totalCash', 'N/A'),
                "total_debt": info.get('totalDebt', 'N/A'),
                "debt_to_equity": info.get('debtToEquity', 'N/A'),
                "current_ratio": info.get('currentRatio', 'N/A'),
                "book_value": info.get('bookValue', 'N/A'),
                "cash_per_share": info.get('totalCashPerShare', 'N/A'),
            },

            # Profitability Metrics
            "profitability": {
                "roe": info.get('returnOnEquity', 'N/A'),
                "roa": info.get('returnOnAssets', 'N/A'),
                "gross_margin": info.get('grossMargins', 'N/A'),
                "operating_margin": info.get('operatingMargins', 'N/A'),
            },

            # Dividend Information
            "dividends": {
                "dividend_rate": info.get('dividendRate', 'N/A'),
                "dividend_yield": info.get('dividendYield', 'N/A'),
                "payout_ratio": info.get('payoutRatio', 'N/A'),
                "ex_dividend_date": info.get('exDividendDate', 'N/A'),
            },

            # Trading Information
            "trading": {
                "volume": info.get('volume', 'N/A'),
                "average_volume": info.get('averageVolume', 'N/A'),
                "beta": info.get('beta', 'N/A'),
                "50_day_average": info.get('fiftyDayAverage', 'N/A'),
                "200_day_average": info.get('twoHundredDayAverage', 'N/A'),
            },

            # Analyst Recommendations
            "analyst": {
                "target_price": info.get('targetMeanPrice', 'N/A'),
                "target_high": info.get('targetHighPrice', 'N/A'),
                "target_low": info.get('targetLowPrice', 'N/A'),
                "recommendation": info.get('recommendationKey', 'N/A'),
                "number_of_analysts": info.get('numberOfAnalystOpinions', 'N/A'),
            },

            # Share Statistics
            "shares": {
                "shares_outstanding": info.get('sharesOutstanding', 'N/A'),
                "float_shares": info.get('floatShares', 'N/A'),
                "shares_short": info.get('sharesShort', 'N/A'),
                "short_ratio": info.get('shortRatio', 'N/A'),
                "short_percent_float": info.get('shortPercentOfFloat', 'N/A'),
            },

            # Company Officers (Top 3)
            "officers": get_top_officers(info),

            # Historical Performance
            "performance": get_historical_performance(stock),

            # Timestamp
            "last_updated": datetime.now().isoformat()
        }

        # Add small delay to avoid rate limiting on subsequent requests
        time.sleep(1)

        return report

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Too Many Requests" in error_msg:
            raise Exception("Yahoo Finance rate limit reached. Please wait 30-60 seconds and try again.")
        raise Exception(f"Error fetching stock data: {error_msg}")


def get_top_officers(info):
    """Extract top company officers"""
    officers = info.get('companyOfficers', [])
    top_officers = []
    for officer in officers[:3]:  # Top 3 officers
        top_officers.append({
            "name": officer.get('name', 'N/A'),
            "title": officer.get('title', 'N/A'),
            "pay": officer.get('totalPay', 'N/A')
        })
    return top_officers


def get_historical_performance(stock):
    """Calculate historical performance metrics"""
    try:
        # Add delay before making another API call to avoid rate limiting
        time.sleep(0.5)

        # Get historical data for different periods
        today = datetime.now()
        periods = {
            "1_month": today - timedelta(days=30),
            "3_months": today - timedelta(days=90),
            "6_months": today - timedelta(days=180),
            "1_year": today - timedelta(days=365),
            "ytd": datetime(today.year, 1, 1)
        }

        performance = {}
        hist = stock.history(period="1y")

        if not hist.empty:
            current_price = hist['Close'].iloc[-1]

            for period_name, start_date in periods.items():
                hist_period = hist[hist.index >= start_date]
                if not hist_period.empty:
                    start_price = hist_period['Close'].iloc[0]
                    change = ((current_price - start_price) / start_price) * 100
                    performance[period_name] = round(change, 2)
                else:
                    performance[period_name] = 'N/A'
        else:
            for period_name in periods.keys():
                performance[period_name] = 'N/A'

        return performance

    except Exception as e:
        return {
            "1_month": 'N/A',
            "3_months": 'N/A',
            "6_months": 'N/A',
            "1_year": 'N/A',
            "ytd": 'N/A'
        }


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
