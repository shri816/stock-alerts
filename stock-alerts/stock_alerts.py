import requests
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

def get_nifty50_trends():
    """Get top 5 trending stocks from NIFTY 50"""
    # Get NIFTY 50 components
    nifty50 = "^NSEI"  # NIFTY 50 ticker
    nifty_stock = yf.Ticker(nifty50)
    
    # Get top components (you might need to modify this based on the data source)
    components = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']  # Example components
    
    trends = []
    for ticker in components:
        stock = yf.Ticker(ticker)
        current_data = stock.history(period='1d')
        if not current_data.empty:
            price_change = ((current_data['Close'].iloc[-1] - current_data['Open'].iloc[0]) / 
                          current_data['Open'].iloc[0] * 100)
            trends.append({
                'symbol': ticker.replace('.NS', ''),
                'change': price_change,
                'price': current_data['Close'].iloc[-1]
            })
    
    # Sort by absolute change to get top movers
    trends.sort(key=lambda x: abs(x['change']), reverse=True)
    return trends[:5]

def send_slack_message(webhook_url, trends):
    """Send formatted message to Slack"""
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Format message
    message = f"*Top 5 NIFTY Stock Trends* (_as of {current_time}_)\n\n"
    for i, trend in enumerate(trends, 1):
        direction = "📈" if trend['change'] > 0 else "📉"
        message += f"{i}. *{trend['symbol']}*: {direction} {trend['change']:.2f}% (₹{trend['price']:.2f})\n"

    payload = {
        "text": message,
        "mrkdwn": True
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    # Replace with your Slack webhook URL
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
    
    try:
        trends = get_nifty50_trends()
        success = send_slack_message(SLACK_WEBHOOK_URL, trends)
        print(f"Message sent successfully: {success}")
    except Exception as e:
        print(f"Error: {str(e)}")
