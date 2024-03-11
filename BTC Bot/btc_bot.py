import time
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

# Initialize last_request_time with the current time
last_request_time = time.time()

# List of major cryptocurrencies
major_cryptos = [
    "bitcoin", "ethereum", "ripple", "litecoin", "bitcoin-cash",
    "cardano", "polkadot", "chainlink", "stellar", "binancecoin",
    "usd-coin", "uniswap", "dogecoin", "eos", "wrapped-bitcoin",
    "aave", "monero", "cosmos", "tron", "tezos", "vechain",
    "neo", "nem", "maker", "theta", "filecoin", "terra-luna",
    "cryptocom-chain", "ftx-token", "dash", "huobi-token", "algorand",
    "compound", "the-graph", "avalanche-2", "klaytn", "iota", "waves",
    "bitcoin-sv", "chiliz", "hedera-hashgraph", "zcash", "quant-network",
    "yearn-finance", "decred", "sushi", "huobi-btc", "loopring"
]

# Function to fetch the most recent price data for a specific cryptocurrency with rate limiting and progress bar
def get_current_price(coin_id):
    global last_request_time
    
    # Calculate the time elapsed since the last request
    elapsed_time = time.time() - last_request_time
    
    # If less than the minimum interval between requests has passed, wait before making the next request
    if elapsed_time < 3600 / 30:  # 3600 seconds in an hour, 30 requests per hour
        with tqdm(total=int((3600 / 30) - elapsed_time), desc="Rate Limiting") as pbar:
            for _ in range(int((3600 / 30) - elapsed_time)):
                time.sleep(1)
                pbar.update(1)
    
    # Make the API request
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    # Update the time of the last request
    last_request_time = time.time()
    
    return data.get(coin_id, {}).get("usd")

# Function to preprocess the fetched data
def preprocess_data(prices):
    # Convert the data into a DataFrame
    df = pd.DataFrame(prices.values(), index=prices.keys(), columns=['price'])
    
    # Add your preprocessing steps here
    # For example, you might want to handle missing values, scale the features, etc.
    # Replace this with your actual preprocessing logic
    
    # For demonstration, let's just scale the prices by dividing by the maximum price
    max_price = df['price'].max()
    df['scaled_price'] = df['price'] / max_price
    
    return df

# Function to train a linear regression model
def train_model(data):
    # Implement your model training logic here
    # For demonstration, let's train a simple linear regression model
    X = data.index.astype(int).values.reshape(-1, 1)  # Assuming timestamps are used as features
    y = data['price'].values
    model = LinearRegression()
    model.fit(X, y)
    return model

# Placeholder function to predict the next hour's prices using the trained model
def predict_next_hour_prices(model, last_timestamp):
    # Implement your prediction logic here
    # For demonstration, let's predict a constant price increase
    next_timestamp = last_timestamp + 3600  # Add one hour (3600 seconds) to the last timestamp
    next_hour_price = model.predict([[next_timestamp]])
    return next_hour_price

# Flag variable to control loop execution
prediction_done = False

# Main loop for continuous data fetching, preprocessing, training, and prediction
while not prediction_done:
    # Fetch the most recent price data for all major cryptocurrencies
    current_prices = {}
    for coin_id in major_cryptos:
        current_prices[coin_id] = get_current_price(coin_id)
    
    # Preprocess the fetched data
    processed_data = preprocess_data(current_prices)
    
    # Train the model
    model = train_model(processed_data)
    
    # Get the last timestamp from the data
    last_timestamp = processed_data.index[-1]
    
    # Predict the next hour's prices
    next_hour_prices = predict_next_hour_prices(model, last_timestamp)
    
    # Output the prediction
    predicted_best_coin = processed_data.index[next_hour_prices.argmax()]
    print("Predicted best coin for the next hour:", predicted_best_coin)
    
    # Set the flag to True to stop further loop iterations
    prediction_done = True
