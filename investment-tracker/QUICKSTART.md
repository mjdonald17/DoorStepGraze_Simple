# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (First Time Only)
```bash
cd investment-tracker
pip install -r requirements.txt
```

### 2. Start the Server
```bash
cd backend
python app.py
```

Or use the convenience script:
```bash
./start.sh
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## First Steps

1. **Add RKLB (Rocket Lab)** to your portfolio:
   - Go to Portfolio tab
   - Type "RKLB" in the input box
   - Click "Add Stock"

2. **View Detailed Analysis**:
   - Click "View Details" button on the RKLB card
   - See comprehensive stock metrics

3. **Check News**:
   - Go to News tab
   - Select RKLB from dropdown
   - Click "Load News"
   - See articles sorted by engagement

## Optional: Get Better News Data

### NewsAPI (Free - Takes 2 minutes)
1. Visit: https://newsapi.org/register
2. Get your free API key
3. Edit `backend/news_aggregator.py`
4. Replace: `NEWS_API_KEY = 'demo'` with your key
5. Restart the server

### Reddit API (Optional - Takes 5 minutes)
For social engagement metrics:
1. Visit: https://www.reddit.com/prefs/apps
2. Click "create application"
3. Select "script" type
4. Get client_id and client_secret
5. Edit `backend/news_aggregator.py`
6. Update Reddit credentials
7. Restart the server

## Tips

- Start simple: Use the app without API keys first
- Add your stocks gradually
- News loads faster than detailed reports
- Engagement scores show how popular articles are
- All data is stored locally in `data/portfolio.json`

## Common Issues

**Port 5000 in use?**
- Edit `backend/app.py`, change port to 5001

**Dependencies not installing?**
- Make sure you have Python 3.8+
- Try: `pip3 install -r requirements.txt`

**Stock data slow?**
- First load takes longer
- Subsequent loads are faster
- Some stocks have less data available

---

Enjoy tracking your investments! 📈
