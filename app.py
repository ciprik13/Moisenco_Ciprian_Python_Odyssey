import numpy as np
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt
import pmdarima as pm
import time
import requests
import logging
from PIL import Image

# Configure logging
logging.basicConfig(filename='project.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

API_KEY = 'e8ShAFz1nyeYApFngxejXQRKYEKYdq7D649DlBcUL2uOz19TkPKvff0RgcIhWzk0'
API_SECRET = 'WelQckGklViZ8alvPDODgVEitzXdSPAATdZdzF5rlQjfRwdt2N7QfDLc7bNWKrvR'

logging.info('START EXECUTION')

# Define global variables
crypto_currency = "BTC"
against_currency = "USDT"  # Binance uses USDT instead of USD
prediction_days = 60
binance_url = 'https://api.binance.com/api/v3/klines'

# Function to fetch Bitcoin prices from Binance API
@st.cache_data(ttl=60)  # Cache the function to limit API calls and reduce latency
def fetch_data():
    try:
        logging.info('Fetching data from Binance API...')
        params = {
            'symbol': f'{crypto_currency}{against_currency}',
            'interval': '1m',
            'limit': 1
        }
        response = requests.get(binance_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        klines = response.json()
        if not klines:
            logging.warning('No data received from Binance API')
            return None
        price = float(klines[0][4])  # Closing price
        logging.info(f'Fetched price: {price}')
        return price
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        st.write(f"Error fetching data: {e}")
        return None

# Function to predict the price using ARIMA
def predict_price(prices):
    logging.info('Starting price prediction using ARIMA...')
    model = pm.auto_arima(prices, seasonal=False, stepwise=True)
    forecast, conf_int = model.predict(n_periods=prediction_days, return_conf_int=True)
    logging.info('Price prediction completed.')
    return forecast, conf_int

# Streamlit app
logo = Image.open("sigmoid_logo.jpg")
col1, col2 = st.columns([1, 6])
col1.image(logo, use_column_width=True)
col2.title("Real-Time Cryptocurrency Price Prediction")

st.write(f"Prediction for {crypto_currency}/{against_currency}")

# Placeholder for the plot and the price display
plot_placeholder = st.empty()
price_placeholder = st.empty()
time_placeholder = st.empty()
data_placeholder = st.empty()

# Initialize session state variables
if 'price_history' not in st.session_state:
    st.session_state.price_history = []

if 'stop_button' not in st.session_state:
    st.session_state.stop_button = False

# Stop button callback function
def stop_loop():
    st.session_state.stop_button = True

stop_button = st.button("Stop", on_click=stop_loop, key="stop_button_key")

# Run the main loop if stop button is not pressed
if not st.session_state.stop_button:
    while not st.session_state.stop_button:
        # Show current time
        current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_placeholder.text(f"Current time: {current_time}")
        logging.info(f'Current time: {current_time}')

        # Fetch the latest price
        logging.info('Started Fetching data from binance')
        current_price = fetch_data()
        logging.info('Ending Fetching data from binance')

        if current_price is not None:
            st.session_state.price_history.append(current_price)
            price_placeholder.text(f"Latest BTC Price: {current_price:.2f} USDT")
            data_placeholder.text(f"Current length of price history: {len(st.session_state.price_history)}")
            logging.info(f'Latest BTC Price: {current_price:.2f} USDT')
            logging.info(f'Current length of price history: {len(st.session_state.price_history)}')

            logging.info(f'Price history length: {len(st.session_state.price_history)} and prediction days: {prediction_days}')
            if len(st.session_state.price_history) >= prediction_days:
                # Prepare the data for prediction
                logging.info('Preparing data for prediction...')
                train_data = np.array(st.session_state.price_history[-prediction_days:])

                # Remove NaN values from train_data
                train_data = train_data[~np.isnan(train_data)]

                logging.info(f'train_data {train_data}')
                # Check if train_data has enough data points after removing NaN values
                if len(train_data) < prediction_days:
                    logging.warning('Not enough data points for prediction after removing NaN values.')
                    plot_placeholder.text("Not enough data points for prediction after removing NaN values.")
                else:
                    # Predict the next `prediction_days` values
                    forecast, conf_int = predict_price(train_data)

                    # Plot the actual and predicted prices
                    fig, ax = plt.subplots()
                    ax.plot(st.session_state.price_history, color='blue', label='Actual Price')

                    # Plot the forecasted prices
                    forecast_index = range(len(st.session_state.price_history), len(st.session_state.price_history) + prediction_days)
                    ax.plot(forecast_index, forecast, color='red', linestyle='--', label='Predicted Price')

                    # Plot confidence intervals
                    ax.fill_between(forecast_index, conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.3)

                    # Set axis labels
                    ax.set_xlabel('Timp (minute)', fontsize=12)
                    ax.set_ylabel('Preț BTC (USDT)', fontsize=12)

                    ax.legend()
                    plot_placeholder.pyplot(fig)
                    logging.info('Plot updated with actual and predicted prices.')

            else:
                plot_placeholder.text("Collecting data...")
                logging.info('Collecting data...')

        else:
            st.write("Unable to fetch data. Retrying in 60 seconds...")
            logging.warning("Unable to fetch data. Retrying in 60 seconds...")

        time.sleep(1)  # Update each second

        # Check if stop button was pressed
        if st.session_state.stop_button:
            logging.info('Stop button pressed. Exiting loop.')
            break
else:
    st.write("Application stopped.")
