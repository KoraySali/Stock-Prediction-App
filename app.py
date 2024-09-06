import streamlit as st
from datetime import date
import yfinance
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START_DATE = "2012-01-01"
CURRENT_DATE = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("GOOG", "AAPL", "MSFT", "GME")
selected_stock = st.selectbox("Select stock", stocks)

n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

@st.cache_data
def load_data(stock):
    data = yfinance.download(stock, START_DATE, CURRENT_DATE)
    data.reset_index(inplace=True)
    return data

data = load_data(selected_stock)
st.subheader("Stock data")
st.write(data.tail())

# Plot stock data
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
fig1.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
fig1.layout.update(title_text="Time Series data", xaxis_rangeslider_visible=True)
st.plotly_chart(fig1)

# Predict future prices
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Plot forecast
st.subheader("Forecast data")
fig2 = plot_plotly(m, forecast)
st.plotly_chart(fig2)