import streamlit as st
from datetime import date
import yfinance as yf
from prophet.forecaster import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

# Constants
DEFAULT_START_DATE = "1990-01-01"
CURRENT_DATE = date.today().strftime("%Y-%m-%d")

# List of companies
stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B", "UNH", "JPM",
    "V", "MA", "HD", "DIS", "PYPL", "NFLX", "INTC", "CSCO", "PEP", "KO",
    "NKE", "MRK", "XOM", "WMT", "ABT", "CRM", "COST", "CVX", "TMO", "ABNB",
    "BABA", "MA", "BAC", "MCD", "WFC", "ORCL", "UPS", "AVGO", "ADBE", "IBM",
    "AMT", "T", "MDT", "GS", "LMT", "QCOM", "TXN", "HON", "BA", "AMGN",
    "GILD", "IBM", "MS", "MU", "SBUX", "ADP", "FIS", "CVS", "PFE"
]

# App title and sidebar
st.title("KorAlytics")
st.subheader("Stock Prediction")
st.sidebar.header("Choose your stock and settings")

# Sidebar inputs
selected_stock = st.sidebar.selectbox("Select stock", stocks)
start_date = st.sidebar.date_input("Start date", pd.to_datetime(DEFAULT_START_DATE))
end_date = st.sidebar.date_input("End date", pd.to_datetime(CURRENT_DATE))
n_years = st.sidebar.slider("Years of prediction:", 0, 5, 1)
n_months = st.sidebar.slider("Months of predicition", 0, 12, 1)
n_days = st.sidebar.slider("Days of prediction:", 0, 365, 1)
chart_type = st.sidebar.selectbox("Select current stock chart type", ["Line", "Bar"])
show_technical_indicators = st.sidebar.checkbox("Show Technical Indicators", value=False)
compare_stock = st.sidebar.selectbox("Compare with another stock (optional)", ["None"] + stocks)
period_year = n_years * 365
period_months = n_months * 30
period_days = n_days * 1

@st.cache_data
def load_data(stock, start, end):
    data = yf.download(stock, start, end)
    data.reset_index(inplace=True)
    return data

# Load data
data = load_data(selected_stock, start_date, end_date)

# Compute the change and direction
last_close = data['Close'].iloc[-1]
previous_close = data['Close'].iloc[-2] if len(data) > 1 else last_close
change = last_close - previous_close
arrow = "↑" if change > 0 else "↓" if change < 0 else "⸺"
change_text = f"{arrow} {abs(change):.2f} USD"

# Key Stats
st.markdown(
    """
    <style>
    .stats-card {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        margin: 10px;
        text-align: center; /* Center text inside the card */
        width: 140px;
        height: 120px;
        display: inline-block;
        vertical-align: top;
    }
    .container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0px;
        margin: 0 auto;
        max-width: 800px;
    }
    .neon {
        color: #FF6F00; /* Neon green color */
        font-family: 'Arial Black', sans-serif;
        font-size: 18px;
        text-align: center; /* Center the neon text */
        margin: 0px; /* Remove default margin */
        margin-bottom: 10px;
        padding: 0; /* Remove default padding */
        padding-left: 19px;
        padding-top: -5px;
        padding-bottom: -2px;
    }
    .stats-card p {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        margin-top: 0; /* Remove default margin to better center text */
        padding-top: -5px;
        font-weight: bold;
    }
    h1 {
        font-size: 60px;
        text-align: center;
        font-family: "Proxima Nova";
        font-weight: normal;
        padding-bottom: 0px;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        padding-left: 10px;
    } 
    h2, h3, h4 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        font-size: 40px;
    }
    .header-margin {
        margin-bottom: 40px; /* Increase bottom margin */
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Example statistics
st.markdown(
    f"""
    <div class="container header-margin">
        <div class="stats-card">
            <h3 class="neon">Open</h3>
            <p>{data['Open'].iloc[-1]:.2f} USD</p>
        </div>
        <div class="stats-card">
            <h3 class="neon">Close</h3>
            <p><span class="arrow">{arrow} {data['Close'].iloc[-1]:.2f} USD</span><br>{change_text}</p>
        </div>
        <div class="stats-card">
            <h3 class="neon">High</h3>
            <p>{data['High'].max():.2f} USD</p>
        </div>
        <div class="stats-card">
            <h3 class="neon">Low</h3>
            <p>{data['Low'].min():.2f} USD</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Plot stock data
st.subheader("Current Stock Data Overview")
fig1 = go.Figure()
if chart_type == "Line":
    fig1.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="Open", mode='lines'))
    fig1.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close", mode='lines'))
elif chart_type == "Bar":
    fig1.add_trace(go.Bar(x=data["Date"], y=data["Open"], name="Open"))
    fig1.add_trace(go.Bar(x=data["Date"], y=data["Close"], name="Close"))

fig1.update_layout(
    title=f"{selected_stock} Time Series Data",
    title_x=0,  # Align title to the left
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=True
)
st.plotly_chart(fig1, use_container_width=True)

# Show technical indicators
if show_technical_indicators:
    # Simple Moving Averages
    data['SMA_30'] = data['Close'].rolling(window=30).mean()
    data['SMA_100'] = data['Close'].rolling(window=100).mean()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close", mode='lines'))
    fig2.add_trace(go.Scatter(x=data["Date"], y=data["SMA_30"], name="SMA 30", mode='lines', line=dict(color='orange')))
    fig2.add_trace(go.Scatter(x=data["Date"], y=data["SMA_100"], name="SMA 100", mode='lines', line=dict(color='blue')))
    fig2.update_layout(
        title=f"{selected_stock} with Technical Indicators",
        title_x=0,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# Comparison feature
if compare_stock != "None":
    compare_data = load_data(compare_stock, start_date, end_date)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name=selected_stock, mode='lines'))
    fig3.add_trace(go.Scatter(x=compare_data["Date"], y=compare_data["Close"], name=compare_stock, mode='lines'))
    fig3.update_layout(
        title=f"{selected_stock} vs {compare_stock}",
        title_x=0,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig3, use_container_width=True)

# Predict future prices
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet(interval_width=0.95)
m.fit(df_train)
period = period_year + period_months + period_days
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Plot forecast
st.subheader("Forecast Data")
fig4 = plot_plotly(m, forecast)

# Update trace colors and axis names
fig4.update_traces(line_color='#A020F0')  # Change the color of the forecast line to neon purple
fig4.update_layout(
    title=f"{selected_stock} Price Forecast",
    title_x=0,  # Align title to the left
    xaxis_title="Date",  # Change the x-axis title
    yaxis_title="Predicted Price" # Change the y-axis title
)
st.plotly_chart(fig4, use_container_width=True)
