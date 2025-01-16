from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objects as go
import os

app = Flask(__name__)

@app.route('/')
def irb_stock():
    # Define the stock ticker symbol for IRB Infra
    ticker_symbol = "IRB.NS"  # Use "IRB.NS" for Indian stock markets on Yahoo Finance
    
    # Fetch stock details
    ticker = yf.Ticker(ticker_symbol)
    stock_info = ticker.info
    
    # Fallback for current price if missing
    current_price = stock_info.get("regularMarketPrice", None)
    if current_price is None:
        hist = ticker.history(period="1d")
        current_price = hist["Close"].iloc[-1] if not hist.empty else "N/A"
    
    # Prepare stock data
    stock_data = {
        "symbol": ticker_symbol,
        "name": stock_info.get("longName", "N/A"),
        "current_price": current_price,
        "52_week_high": stock_info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": stock_info.get("fiftyTwoWeekLow", "N/A"),
        "market_cap": stock_info.get("marketCap", "N/A")
    }
    
    # Fetch historical data for the chart
    hist = ticker.history(period="6mo")  # Last 6 months
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Closing Price'))
    fig.update_layout(title=f"{stock_info.get('longName', ticker_symbol)} - Stock Price Chart",
                      xaxis_title="Date", yaxis_title="Price (INR)",
                      template="plotly_white")
    
    # Save the chart as HTML
    chart_file = "static/chart.html"
    if not os.path.exists("static"):
        os.makedirs("static")
    fig.write_html(chart_file)

    return render_template('irb_stock.html', stock=stock_data, chart_file=chart_file)

if __name__ == '__main__':
    app.run(debug=True)
