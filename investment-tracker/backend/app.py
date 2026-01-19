from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from stock_data import get_stock_report
from news_aggregator import get_stock_news

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

PORTFOLIO_FILE = '../data/portfolio.json'

def load_portfolio():
    """Load portfolio from JSON file"""
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return {"stocks": []}

def save_portfolio(portfolio):
    """Save portfolio to JSON file"""
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2)

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get all stocks in portfolio"""
    portfolio = load_portfolio()
    return jsonify(portfolio)

@app.route('/api/portfolio', methods=['POST'])
def add_stock():
    """Add a stock to portfolio"""
    data = request.json
    symbol = data.get('symbol', '').upper()

    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    portfolio = load_portfolio()

    # Check if stock already exists
    if any(stock['symbol'] == symbol for stock in portfolio['stocks']):
        return jsonify({"error": "Stock already in portfolio"}), 400

    portfolio['stocks'].append({
        "symbol": symbol,
        "added_date": data.get('added_date', '')
    })

    save_portfolio(portfolio)
    return jsonify({"message": "Stock added successfully", "portfolio": portfolio})

@app.route('/api/portfolio/<symbol>', methods=['DELETE'])
def remove_stock(symbol):
    """Remove a stock from portfolio"""
    symbol = symbol.upper()
    portfolio = load_portfolio()

    portfolio['stocks'] = [s for s in portfolio['stocks'] if s['symbol'] != symbol]
    save_portfolio(portfolio)

    return jsonify({"message": "Stock removed successfully", "portfolio": portfolio})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_details(symbol):
    """Get detailed report for a specific stock"""
    symbol = symbol.upper()
    try:
        report = get_stock_report(symbol)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/<symbol>', methods=['GET'])
def get_news(symbol):
    """Get news for a specific stock"""
    symbol = symbol.upper()
    try:
        news = get_stock_news(symbol)
        return jsonify(news)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
