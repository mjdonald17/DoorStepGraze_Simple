# Investment Tracker

A comprehensive web application for tracking your investment portfolio with detailed stock analysis and news monitoring.

## Features

### 1. Portfolio Management
- Add and remove stocks from your portfolio
- Track up to 20 stocks simultaneously
- Quick access to detailed reports for any stock

### 2. Comprehensive Stock Analysis
Get detailed reports on any stock including:

**Price Information**
- Current price, day range, 52-week range
- Historical performance (1 month, 3 months, 6 months, 1 year, YTD)

**Valuation Metrics**
- Market cap, enterprise value
- P/E ratio, Forward P/E, PEG ratio
- Price-to-book, price-to-sales ratios
- EV/Revenue, EV/EBITDA

**Financial Performance**
- Revenue and revenue growth
- Gross profit, EBITDA, net income
- Profit margins, operating margins
- Free cash flow

**Balance Sheet**
- Total cash and debt
- Debt-to-equity ratio
- Current ratio, book value

**Profitability Metrics**
- Return on Equity (ROE)
- Return on Assets (ROA)
- Gross and operating margins

**Dividend Information**
- Dividend rate and yield
- Payout ratio
- Ex-dividend date

**Trading Information**
- Volume metrics
- Beta
- Moving averages (50-day, 200-day)

**Analyst Recommendations**
- Target prices (mean, high, low)
- Analyst ratings and recommendations

**Company Information**
- Business description
- Sector and industry
- Key executives

### 3. News Aggregation & Engagement Tracking
- Aggregate news from multiple sources (Yahoo Finance, NewsAPI, Reddit)
- Track engagement metrics to see how widely read articles are
- Social media discussions with upvotes and comment counts
- Sort by engagement to see most popular content first
- Filter news specific to your stocks

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (web framework)
- yfinance (stock data)
- NewsAPI (news aggregation)
- Reddit API (social engagement)

**Frontend:**
- HTML5
- CSS3 (modern, responsive design)
- Vanilla JavaScript

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd investment-tracker
pip install -r requirements.txt
```

### Step 2: API Keys (Optional but Recommended)

#### NewsAPI (Free)
1. Get a free API key from [https://newsapi.org/register](https://newsapi.org/register)
2. Open `backend/news_aggregator.py`
3. Replace `NEWS_API_KEY = 'demo'` with your actual key

#### Reddit API (Optional - for engagement metrics)
1. Create a Reddit account if you don't have one
2. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
3. Click "create application"
4. Select "script" type
5. Get your client_id and client_secret
6. Open `backend/news_aggregator.py`
7. Update the Reddit configuration:
```python
REDDIT_CLIENT_ID = 'your_client_id'
REDDIT_CLIENT_SECRET = 'your_client_secret'
```

**Note:** The app works without these API keys, but you'll get:
- Limited news without NewsAPI key
- No social engagement metrics without Reddit API

## Usage

### Start the Application

```bash
cd investment-tracker/backend
python app.py
```

The server will start on `http://localhost:5000`

### Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

### Using the Application

#### 1. Add Stocks to Portfolio
- Navigate to the "Portfolio" tab
- Enter a stock symbol (e.g., RKLB for Rocket Lab)
- Click "Add Stock"
- Your portfolio can hold up to 20 stocks

#### 2. View Stock Details
- Click "View Details" on any stock card, OR
- Go to the "Stock Details" tab
- Select a stock from the dropdown
- Click "Load Details"
- View comprehensive analysis including:
  - Company overview
  - Price and valuation metrics
  - Financial performance
  - Balance sheet data
  - Historical performance
  - Analyst recommendations

#### 3. Monitor News
- Go to the "News" tab
- Select a stock from the dropdown
- Click "Load News"
- View aggregated news sorted by engagement
- See engagement metrics (upvotes, comments) on social posts

## Example: Analyzing Rocket Lab (RKLB)

1. **Add to Portfolio**: Enter "RKLB" in the portfolio tab
2. **View Details**: Click "View Details" to see:
   - Aerospace & Defense industry classification
   - Market cap and valuation metrics
   - Revenue growth and profitability
   - Analyst price targets
   - Historical performance
3. **Check News**: View latest news about Rocket Lab with engagement metrics

## Data Sources

- **Stock Data**: Yahoo Finance (via yfinance library)
- **News**: Yahoo Finance News, NewsAPI
- **Social Engagement**: Reddit (r/stocks, r/investing, r/wallstreetbets, r/StockMarket)

## Understanding Engagement Metrics

The app tracks how "widely read" articles are using:
- **Reddit Posts**: Upvotes + comments = engagement score
- **Engagement Levels**:
  - Unknown: No engagement data available
  - Low: < 100 interactions
  - Moderate: 100-500 interactions
  - High: 500-2000 interactions
  - Very High: 2000+ interactions

## Project Structure

```
investment-tracker/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── stock_data.py          # Stock data fetching and processing
│   └── news_aggregator.py     # News aggregation and engagement tracking
├── frontend/
│   ├── index.html             # Main HTML page
│   └── static/
│       ├── css/
│       │   └── styles.css     # Application styling
│       └── js/
│           └── app.js         # Frontend JavaScript
├── data/
│   └── portfolio.json         # Portfolio storage (auto-generated)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, edit `backend/app.py` and change:
```python
app.run(debug=True, port=5000)
```
to a different port (e.g., 5001).

### Stock Data Not Loading
- Check your internet connection
- Some stocks may not have complete data available
- Wait a few seconds and try again (API rate limits)

### News Not Showing
- If using 'demo' NewsAPI key, news will be limited
- Sign up for a free API key for better results
- Reddit API is optional for social engagement metrics

### API Rate Limits
- Yahoo Finance: Generally no strict limits for personal use
- NewsAPI: 100 requests/day on free tier
- Reddit: 60 requests/minute

## Future Enhancements

Potential features to add:
- Price alerts and notifications
- Portfolio performance tracking
- Comparison tools for multiple stocks
- Sentiment analysis on news articles
- Export reports to PDF
- Mobile-responsive improvements
- Dark mode
- Historical price charts

## Security Notes

- All data is stored locally
- No sensitive information is transmitted
- API keys should be kept private
- Don't share your `news_aggregator.py` with API keys

## License

This project is for personal use. Stock data is provided by Yahoo Finance and other sources - please review their terms of service.

## Support

For issues or questions:
1. Check this README
2. Verify all dependencies are installed
3. Check console/terminal for error messages

## Contributing

Feel free to fork and customize this application for your own needs!

---

**Disclaimer**: This tool is for informational purposes only. Not financial advice. Always do your own research before making investment decisions.
