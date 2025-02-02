import streamlit as st
import requests
import matplotlib.pyplot as plt

# CoinGecko API URL
API_URL = "https://api.coingecko.com/api/v3"

def get_crypto_data(crypto_id):
    """Fetch real-time crypto data from CoinGecko API"""
    url = f"{API_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": crypto_id,
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": "true",
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()[0]
    else:
        return None

# Streamlit App
st.title("💰 Crypto Price Tracker")

# User Input
crypto_id = st.text_input("Enter Cryptocurrency ID (e.g., bitcoin, ethereum):", "bitcoin")

# Fetch Data
crypto_data = get_crypto_data(crypto_id)

if crypto_data:
    st.subheader(f"{crypto_data['name']} ({crypto_data['symbol'].upper()})")
    st.metric("Current Price", f"${crypto_data['current_price']:,.2f}")
    st.metric("Market Cap", f"${crypto_data['market_cap']:,.2f}")
    st.metric("24h Change", f"{crypto_data['price_change_percentage_24h']:.2f}%")

    # Price Chart
    st.subheader("📈 Price Trend (Last 7 Days)")
    sparkline_data = crypto_data['sparkline_in_7d']['price']
    plt.figure(figsize=(10, 4))
    plt.plot(sparkline_data, color="blue", linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    st.pyplot(plt)
else:
    st.error("Invalid cryptocurrency ID! Please try again.")

st.write("💡 **Powered by [CoinGecko API](https://www.coingecko.com/en/api)**")
