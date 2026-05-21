from flask import Flask, render_template
import urllib.request
import json

app = Flask(__name__)

# Configured Target Assets with predefined Baseline Comparison prices in INR (₹)
TRACKED_ASSETS = {
    "bitcoin": {"name": "Bitcoin", "baseline_price": 8000000.00},
    "ethereum": {"name": "Ethereum", "baseline_price": 230000.00},
    "solana": {"name": "Solana", "baseline_price": 12000.00},
    "binancecoin": {"name": "BNB", "baseline_price": 50000.00},
    "ripple": {"name": "Ripple", "baseline_price": 50.00},
    "cardano": {"name": "Cardano", "baseline_price": 40.00}
}

ASSET_IDS = ",".join(TRACKED_ASSETS.keys())
# API URL updated to query prices against INR instead of USD
API_ENDPOINT = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ASSET_IDS}&order=market_cap_desc"

def fetch_live_rates():
    try:
        req = urllib.request.Request(
            API_ENDPOINT, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                raw_data = json.loads(response.read().decode())
                
                # Inject backend baseline INR prices into the active stream data matrix
                for coin in raw_data:
                    coin_id = coin['id']
                    if coin_id in TRACKED_ASSETS:
                        coin['baseline_price'] = TRACKED_ASSETS[coin_id]['baseline_price']
                return raw_data
    except Exception as e:
        print(f"Error fetching live data: {e}")
    return []

@app.route('/')
def home():
    market_data = fetch_live_rates()
    return render_template('index.html', market_data=market_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)