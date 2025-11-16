import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import time

# Target website
URL = "https://coinmarketcap.com/"

# Function to fetch a single coin's price
def fetch_crypto_price(crypto_name):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    row = soup.find("p", string=crypto_name)
    if row:
        price = row.find_next("span").text.replace("$", "").replace(",", "")
        return float(price)
    return None

# ✅ List of 6 cryptocurrencies
cryptos = [
    "Bitcoin",
    "Ethereum",
    "BNB",
    "Solana",
    "XRP",
    "Dogecoin"
]

file_name = "crypto_prices.csv"

# Loop forever to update prices every minute
while True:
    data_list = []
    for coin in cryptos:
        price = fetch_crypto_price(coin)
        data_list.append([coin, price])

    # Create DataFrame
    df = pd.DataFrame(data_list, columns=["Crypto", "Price"])
    df["Time"] = datetime.datetime.now()

    # If file already exists, compare prices and show trends
    if os.path.exists(file_name):
        old_df = pd.read_csv(file_name)
        last_prices = dict(zip(old_df["Crypto"], old_df["Price"]))

        print("\n=== Trend Prediction ===")
        for index, row in df.iterrows():
            name = row["Crypto"]
            new_price = row["Price"]
            if name in last_prices:
                old_price = last_prices[name]
                if new_price > old_price:
                    print(f"{name}: 📈 Increased ({old_price} → {new_price})")
                elif new_price < old_price:
                    print(f"{name}: 📉 Decreased ({old_price} → {new_price})")
                else:
                    print(f"{name}: No Change ({new_price})")

        # Append latest prices to CSV
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        # Create new CSV if not found
        df.to_csv(file_name, index=False)
        print("CSV Created ✅")

    # Print latest prices
    print("\nLatest Prices:\n", df)
    print("-" * 40)

    # Wait 60 seconds before updating again
    time.sleep(60)