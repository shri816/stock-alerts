import requests
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

def get_nifty50_trends():
    """Get top 5 gainers and losers from NIFTY 50"""
    # List of NIFTY 50 components
    components = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
        'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
        'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'TITAN.NS',
        'BAJFINANCE.NS', 'WIPRO.NS', 'NESTLEIND.NS', 'HCLTECH.NS', 'ULTRACEMCO.NS',
        'SUNPHARMA.NS', 'TATAMOTORS.NS', 'POWERGRID.NS', 'NTPC.NS', 'ONGC.NS'
    ]  # Add all NIFTY 50 components
    
    trends = []
    for ticker in components:
        try:
            stock = yf.Ticker(ticker)
            current_data = stock.history(period='1d')
            if not current_data.empty:
                price_change = ((current_data['Close'].iloc[-1] - current_data['Open'].iloc[0]) / 
                              current_data['Open'].iloc[0] * 100)
                trends.append({
                    'symbol': ticker.replace('.NS', ''),
                    'change': price_change,
                    'price': current_data['Close'].iloc[-1],
                    'open': current_data['Open'].iloc[0]
                })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            continue
    
    # Sort trends by change percentage
    trends.sort(key=lambda x: x['change'])
    
    # Get top 5 losers and gainers
    losers = trends[:5]
    gainers = trends[-5:][::-1]  # Reverse to show highest gain first
    
    return gainers, losers

def format_stock_message(stock, index):
    """Format a single stock message"""
    direction = "📈" if stock['change'] > 0 else "📉"
    return f"{index}. *{stock['symbol']}*: {direction} {stock['change']:.2f}% (₹{stock['price']:.2f} from ₹{stock['open']:.2f})"

def send_slack_message(webhook_url, gainers, losers):
    """Send formatted message to Slack with gainers and losers"""
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Format message
    message = f"*NIFTY 50 Top Movers* (_as of {current_time}_)\n\n"
    
    # Add gainers section
    message += "*🟢 Top 5 Gainers:*\n"
    for i, stock in enumerate(gainers, 1):
        message += format_stock_message(stock, i) + "\n"
    
    message += "\n*🔴 Top 5 Losers:*\n"
    for i, stock in enumerate(losers, 1):
        message += format_stock_message(stock, i) + "\n"

    payload = {
        "text": message,
        "mrkdwn": True
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    # Replace with your Slack webhook URL
<<<<<<< HEAD
    V1
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
=======
    SLACK_WEBHOOK_URL = "YOUR_WEBHOOK_URL"
>>>>>>> 94b1462c286293a8945906a63f73dc4b979225a5
    
    try:
        print("Getting trends...")
        gainers, losers = get_nifty50_trends()
        print(f"Found {len(gainers)} gainers and {len(losers)} losers")
        
        print("Sending to Slack...")
        success = send_slack_message(SLACK_WEBHOOK_URL, gainers, losers)
        print(f"Message sent successfully: {success}")
    except Exception as e:
        print(f"Error: {str(e)}")
