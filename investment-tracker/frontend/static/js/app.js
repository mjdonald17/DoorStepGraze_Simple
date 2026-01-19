// API Base URL - automatically uses the current host
// This allows access from iPhone, iPad, or any device on your network
const API_BASE = `${window.location.protocol}//${window.location.hostname}:5000/api`;

// State management
let currentPortfolio = [];
let currentStockDetails = null;
let currentNews = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeEventListeners();
    loadPortfolio();
});

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Event Listeners
function initializeEventListeners() {
    // Add stock button
    document.getElementById('add-stock-btn').addEventListener('click', addStock);

    // Enter key on stock input
    document.getElementById('stock-symbol').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addStock();
    });

    // Load details button
    document.getElementById('load-details-btn').addEventListener('click', loadStockDetails);

    // Load news button
    document.getElementById('load-news-btn').addEventListener('click', loadNews);
}

// Portfolio Management
async function loadPortfolio() {
    try {
        const response = await fetch(`${API_BASE}/portfolio`);
        const data = await response.json();
        currentPortfolio = data.stocks || [];
        renderPortfolio();
        updateStockSelectors();
    } catch (error) {
        showAlert('Error loading portfolio', 'error');
        console.error('Error:', error);
    }
}

function renderPortfolio() {
    const container = document.getElementById('portfolio-list');

    if (currentPortfolio.length === 0) {
        container.innerHTML = '<p class="empty-state">No stocks in portfolio. Add your first stock above.</p>';
        return;
    }

    container.innerHTML = '';
    currentPortfolio.forEach(stock => {
        const card = createStockCard(stock);
        container.appendChild(card);
    });
}

function createStockCard(stock) {
    const card = document.createElement('div');
    card.className = 'stock-card';
    card.innerHTML = `
        <h3>${stock.symbol}</h3>
        <p>Added: ${stock.added_date || 'N/A'}</p>
        <div class="actions">
            <button class="btn-primary" onclick="viewStockDetails('${stock.symbol}')">View Details</button>
            <button class="btn-danger" onclick="removeStock('${stock.symbol}')">Remove</button>
        </div>
    `;
    return card;
}

async function addStock() {
    const input = document.getElementById('stock-symbol');
    const symbol = input.value.trim().toUpperCase();

    if (!symbol) {
        showAlert('Please enter a stock symbol', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/portfolio`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symbol: symbol,
                added_date: new Date().toISOString().split('T')[0]
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(`${symbol} added to portfolio!`, 'success');
            input.value = '';
            loadPortfolio();
        } else {
            showAlert(data.error || 'Error adding stock', 'error');
        }
    } catch (error) {
        showAlert('Error adding stock', 'error');
        console.error('Error:', error);
    }
}

async function removeStock(symbol) {
    if (!confirm(`Remove ${symbol} from portfolio?`)) return;

    try {
        const response = await fetch(`${API_BASE}/portfolio/${symbol}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showAlert(`${symbol} removed from portfolio`, 'success');
            loadPortfolio();
        } else {
            showAlert('Error removing stock', 'error');
        }
    } catch (error) {
        showAlert('Error removing stock', 'error');
        console.error('Error:', error);
    }
}

// Stock Details
function updateStockSelectors() {
    const detailSelect = document.getElementById('detail-stock-select');
    const newsSelect = document.getElementById('news-stock-select');

    [detailSelect, newsSelect].forEach(select => {
        select.innerHTML = '<option value="">Select a stock from your portfolio</option>';
        currentPortfolio.forEach(stock => {
            const option = document.createElement('option');
            option.value = stock.symbol;
            option.textContent = stock.symbol;
            select.appendChild(option);
        });
    });
}

function viewStockDetails(symbol) {
    document.getElementById('detail-stock-select').value = symbol;
    switchTab('stock-details');
    loadStockDetails();
}

async function loadStockDetails() {
    const symbol = document.getElementById('detail-stock-select').value;

    if (!symbol) {
        showAlert('Please select a stock', 'error');
        return;
    }

    const container = document.getElementById('stock-details-container');
    const loading = document.getElementById('details-loading');

    container.innerHTML = '';
    loading.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/stock/${symbol}`);
        const data = await response.json();

        if (response.ok) {
            currentStockDetails = data;
            renderStockDetails(data);
        } else {
            showAlert(data.error || 'Error loading stock details', 'error');
        }
    } catch (error) {
        showAlert('Error loading stock details', 'error');
        console.error('Error:', error);
    } finally {
        loading.classList.add('hidden');
    }
}

function renderStockDetails(data) {
    const container = document.getElementById('stock-details-container');

    const html = `
        <div class="stock-header">
            <h2>${data.symbol} - ${data.name}</h2>
            <p class="company-info">${data.sector} | ${data.industry}</p>
            ${data.website !== 'N/A' ? `<p class="company-info"><a href="${data.website}" target="_blank" style="color: white;">${data.website}</a></p>` : ''}
            <div class="stock-price">$${formatNumber(data.price.current)}</div>
            <p>Previous Close: $${formatNumber(data.price.previous_close)}</p>
        </div>

        ${data.description !== 'N/A' ? `
        <div class="metric-card">
            <h3>📋 Company Description</h3>
            <p>${data.description}</p>
        </div>
        ` : ''}

        <div class="metrics-grid">
            <div class="metric-card">
                <h3>📈 Price Information</h3>
                <div class="metric-row">
                    <span class="metric-label">Open</span>
                    <span class="metric-value">$${formatNumber(data.price.open)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Day Range</span>
                    <span class="metric-value">$${formatNumber(data.price.day_low)} - $${formatNumber(data.price.day_high)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">52 Week Range</span>
                    <span class="metric-value">$${formatNumber(data.price['52_week_low'])} - $${formatNumber(data.price['52_week_high'])}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>📊 Valuation Metrics</h3>
                <div class="metric-row">
                    <span class="metric-label">Market Cap</span>
                    <span class="metric-value">${formatLargeNumber(data.valuation.market_cap)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">P/E Ratio</span>
                    <span class="metric-value">${formatNumber(data.valuation.pe_ratio)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Forward P/E</span>
                    <span class="metric-value">${formatNumber(data.valuation.forward_pe)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">PEG Ratio</span>
                    <span class="metric-value">${formatNumber(data.valuation.peg_ratio)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Price/Book</span>
                    <span class="metric-value">${formatNumber(data.valuation.price_to_book)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Price/Sales</span>
                    <span class="metric-value">${formatNumber(data.valuation.price_to_sales)}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>💰 Financial Performance</h3>
                <div class="metric-row">
                    <span class="metric-label">Revenue</span>
                    <span class="metric-value">${formatLargeNumber(data.financials.revenue)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Revenue Growth</span>
                    <span class="metric-value ${getChangeClass(data.financials.revenue_growth)}">${formatPercent(data.financials.revenue_growth)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Gross Profit</span>
                    <span class="metric-value">${formatLargeNumber(data.financials.gross_profit)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">EBITDA</span>
                    <span class="metric-value">${formatLargeNumber(data.financials.ebitda)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Net Income</span>
                    <span class="metric-value">${formatLargeNumber(data.financials.net_income)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Profit Margin</span>
                    <span class="metric-value">${formatPercent(data.financials.profit_margin)}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>💵 Balance Sheet</h3>
                <div class="metric-row">
                    <span class="metric-label">Total Cash</span>
                    <span class="metric-value">${formatLargeNumber(data.balance_sheet.total_cash)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Total Debt</span>
                    <span class="metric-value">${formatLargeNumber(data.balance_sheet.total_debt)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Debt to Equity</span>
                    <span class="metric-value">${formatNumber(data.balance_sheet.debt_to_equity)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Current Ratio</span>
                    <span class="metric-value">${formatNumber(data.balance_sheet.current_ratio)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Book Value</span>
                    <span class="metric-value">$${formatNumber(data.balance_sheet.book_value)}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>📈 Profitability</h3>
                <div class="metric-row">
                    <span class="metric-label">Return on Equity (ROE)</span>
                    <span class="metric-value">${formatPercent(data.profitability.roe)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Return on Assets (ROA)</span>
                    <span class="metric-value">${formatPercent(data.profitability.roa)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Gross Margin</span>
                    <span class="metric-value">${formatPercent(data.profitability.gross_margin)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Operating Margin</span>
                    <span class="metric-value">${formatPercent(data.profitability.operating_margin)}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>💸 Dividends</h3>
                <div class="metric-row">
                    <span class="metric-label">Dividend Rate</span>
                    <span class="metric-value">$${formatNumber(data.dividends.dividend_rate)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Dividend Yield</span>
                    <span class="metric-value">${formatPercent(data.dividends.dividend_yield)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Payout Ratio</span>
                    <span class="metric-value">${formatPercent(data.dividends.payout_ratio)}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>📉 Trading Information</h3>
                <div class="metric-row">
                    <span class="metric-label">Volume</span>
                    <span class="metric-value">${formatLargeNumber(data.trading.volume)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Avg Volume</span>
                    <span class="metric-value">${formatLargeNumber(data.trading.average_volume)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Beta</span>
                    <span class="metric-value">${formatNumber(data.trading.beta)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">50 Day Avg</span>
                    <span class="metric-value">$${formatNumber(data.trading['50_day_average'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">200 Day Avg</span>
                    <span class="metric-value">$${formatNumber(data.trading['200_day_average'])}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>🎯 Analyst Ratings</h3>
                <div class="metric-row">
                    <span class="metric-label">Target Price</span>
                    <span class="metric-value">$${formatNumber(data.analyst.target_price)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Target High</span>
                    <span class="metric-value">$${formatNumber(data.analyst.target_high)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Target Low</span>
                    <span class="metric-value">$${formatNumber(data.analyst.target_low)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Recommendation</span>
                    <span class="metric-value">${data.analyst.recommendation || 'N/A'}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label"># of Analysts</span>
                    <span class="metric-value">${data.analyst.number_of_analysts || 'N/A'}</span>
                </div>
            </div>

            <div class="metric-card">
                <h3>📊 Historical Performance</h3>
                <div class="metric-row">
                    <span class="metric-label">1 Month</span>
                    <span class="metric-value ${getChangeClass(data.performance['1_month'])}">${formatPercent(data.performance['1_month'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">3 Months</span>
                    <span class="metric-value ${getChangeClass(data.performance['3_months'])}">${formatPercent(data.performance['3_months'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">6 Months</span>
                    <span class="metric-value ${getChangeClass(data.performance['6_months'])}">${formatPercent(data.performance['6_months'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">1 Year</span>
                    <span class="metric-value ${getChangeClass(data.performance['1_year'])}">${formatPercent(data.performance['1_year'])}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">YTD</span>
                    <span class="metric-value ${getChangeClass(data.performance.ytd)}">${formatPercent(data.performance.ytd)}</span>
                </div>
            </div>
        </div>

        ${data.officers && data.officers.length > 0 ? `
        <div class="metric-card">
            <h3>👔 Key Executives</h3>
            ${data.officers.map(officer => `
                <div class="metric-row">
                    <span class="metric-label">${officer.title}</span>
                    <span class="metric-value">${officer.name}</span>
                </div>
            `).join('')}
        </div>
        ` : ''}

        <p style="text-align: center; color: #6c757d; margin-top: 30px;">
            Last Updated: ${new Date(data.last_updated).toLocaleString()}
        </p>
    `;

    container.innerHTML = html;
}

// News Management
async function loadNews() {
    const symbol = document.getElementById('news-stock-select').value;

    if (!symbol) {
        showAlert('Please select a stock', 'error');
        return;
    }

    const container = document.getElementById('news-container');
    const loading = document.getElementById('news-loading');

    container.innerHTML = '';
    loading.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/news/${symbol}`);
        const data = await response.json();

        if (response.ok) {
            currentNews = data;
            renderNews(data);
        } else {
            showAlert(data.error || 'Error loading news', 'error');
        }
    } catch (error) {
        showAlert('Error loading news', 'error');
        console.error('Error:', error);
    } finally {
        loading.classList.add('hidden');
    }
}

function renderNews(data) {
    const container = document.getElementById('news-container');

    if (data.news.length === 0) {
        container.innerHTML = '<p class="empty-state">No news found for this stock.</p>';
        return;
    }

    const html = `
        <div class="news-header">
            <h3>${data.symbol} News & Discussions</h3>
            <p class="news-stats">${data.total_articles} articles found</p>
        </div>

        <div class="news-list">
            ${data.news.map(item => createNewsItemHTML(item)).join('')}
        </div>

        <p style="text-align: center; color: #6c757d; margin-top: 30px;">
            Last Updated: ${new Date(data.last_updated).toLocaleString()}
        </p>
    `;

    container.innerHTML = html;
}

function createNewsItemHTML(item) {
    const engagementClass = getEngagementClass(item.engagement_score);
    const engagementLabel = getEngagementLabel(item.engagement_score);

    return `
        <div class="news-item ${item.type}">
            <div class="news-header-row">
                <div class="news-title">
                    <a href="${item.url}" target="_blank">${item.title}</a>
                </div>
                <span class="engagement-badge engagement-${engagementClass}">${engagementLabel}</span>
            </div>

            <div class="news-meta">
                <span class="news-source">${item.source}</span>
                <span>${formatDate(item.published_date)}</span>
                <span>${item.type === 'discussion' ? '💬 Discussion' : '📰 News'}</span>
            </div>

            ${item.description ? `<p class="news-description">${item.description}</p>` : ''}

            ${item.engagement_details ? `
                <div class="engagement-details">
                    <span class="engagement-stat">👍 <strong>${item.engagement_details.upvotes}</strong> upvotes</span>
                    <span class="engagement-stat">💬 <strong>${item.engagement_details.comments}</strong> comments</span>
                    <span class="engagement-stat">📊 <strong>${(item.engagement_details.upvote_ratio * 100).toFixed(0)}%</strong> upvote ratio</span>
                </div>
            ` : ''}
        </div>
    `;
}

function getEngagementClass(score) {
    if (score === 0) return 'unknown';
    if (score < 100) return 'low';
    if (score < 500) return 'moderate';
    if (score < 2000) return 'high';
    return 'very-high';
}

function getEngagementLabel(score) {
    if (score === 0) return 'Unknown';
    if (score < 100) return `Low (~${score})`;
    if (score < 500) return `Moderate (~${score})`;
    if (score < 2000) return `High (~${score})`;
    return `Very High (${score}+)`;
}

// Utility Functions
function formatNumber(value) {
    if (value === 'N/A' || value === null || value === undefined) return 'N/A';
    return parseFloat(value).toFixed(2);
}

function formatLargeNumber(value) {
    if (value === 'N/A' || value === null || value === undefined) return 'N/A';
    const num = parseFloat(value);
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    if (num >= 1e3) return `$${(num / 1e3).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
}

function formatPercent(value) {
    if (value === 'N/A' || value === null || value === undefined) return 'N/A';
    return `${(parseFloat(value) * 100).toFixed(2)}%`;
}

function formatDate(dateString) {
    if (!dateString || dateString === 'N/A') return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function getChangeClass(value) {
    if (value === 'N/A' || value === null || value === undefined) return '';
    return parseFloat(value) >= 0 ? 'positive' : 'negative';
}

function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;

    const container = document.querySelector('.tab-content.active .section');
    container.insertBefore(alert, container.firstChild);

    setTimeout(() => alert.remove(), 5000);
}
