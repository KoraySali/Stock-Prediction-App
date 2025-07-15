# Stock Prediction App  
**Title: Interactive Stock Price Prediction Using LSTM Neural Networks**

## Description  
This project presents an interactive application for forecasting stock prices using deep learning, specifically Long Short Term Memory (LSTM) neural networks. The application is built with **Streamlit**, providing an intuitive web interface for users to input a stock ticker and visualise both historical and predicted price trends. Leveraging **TensorFlow**, **Keras**, **yfinance**, and **scikit learn**, the project demonstrates the application of time series modelling in financial forecasting.

## Technical Aspects

### Data Source  
The application pulls historical stock price data using the `yfinance` library. Users can select a ticker symbol (for example AAPL or TSLA) and define the time period for analysis.

### Libraries Used  
- `streamlit`: for interactive user interface rendering  
- `yfinance`: for fetching stock price data  
- `pandas` and `numpy`: for data manipulation and processing  
- `scikit learn`: for data scaling and preprocessing  
- `matplotlib`: for plotting graphs  
- `keras` (TensorFlow backend): for building and training the LSTM model

## Data Preprocessing

### Normalisation  
Historical closing prices are scaled using `MinMaxScaler` to ensure the data is suitable for training a neural network.

### Sequence Generation  
Data is segmented into sequences of 60 day windows to capture time dependent trends. These windows form the input for the LSTM model, with the 61st day as the prediction target.

### Train and Test Split  
Data is split into training and validation sets to assess model performance. The model is trained on historical patterns and validated on unseen data.

## LSTM Model Architecture

The LSTM model consists of:  
- A single LSTM layer with 50 units  
- A Dense output layer with one unit for predicting the next closing price  
- Trained over 1 epoch with a batch size of 1 (note: minimal training for demonstration purposes)

### Loss Function  
The model uses Mean Squared Error (MSE) to evaluate prediction error during training.

## Streamlit App Features

### Interactive Ticker Input  
Users can input any stock ticker (compatible with Yahoo Finance) directly into the app.

### Visualisations  
- Historical closing prices  
- Predicted versus actual closing prices (on test data)  
- Future prediction trends based on recent stock behaviour  

### Live Execution  
The app fetches the latest stock data in real time, preprocesses it, and visualises both historical and forecasted data dynamically.



## Limitations and Notes  
- The model is trained with limited epochs for demonstration and speed. Longer training and tuning of parameters would significantly improve accuracy.  
- The prediction is based solely on past closing prices. Real world forecasting should ideally incorporate broader market indicators, news sentiment, and macroeconomic factors.

## Summary  
This project serves as a simplified but functional demonstration of using LSTM neural networks for stock price forecasting. It combines deep learning with an easy to use interactive frontend, highlighting the practical applications of artificial intelligence in finance. The project is ideal for those exploring time series forecasting, neural networks, or building deployable machine learning tools using Streamlit.
