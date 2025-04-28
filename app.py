from flask import Flask, render_template_string
import requests

app = Flask(__name__)

SYMBOLS = ["BTC", "ETH", "DOGE", "LTC", "SOL", "ADA", "AVAX", "SHIB"]  # Add or remove as needed

# Store last prices to compare
last_prices = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kaido Live Crypto</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial, sans-serif; background-color: #0d0d0d; color: #f0f0f0; }
        table { margin: auto; border-collapse: collapse; width: 90%; }
        th, td { padding: 10px; border: 1px solid #333; text-align: center; }
        th { background-color: #222; }
        tr:nth-child(even) { background-color: #1a1a1a; }
        .up { color: #00ff00; }    /* Bright green for up */
        .down { color: #ff3333; }  /* Bright red for down */
    </style>
</head>
<body>
    <h1>Kaido Live Feed (Auto every 5 sec)</h1>
    <table>
        <tr>
            <th>Symbol</th>
            <th>Price (USD)</th>
        </tr>
        {% for symbol, info in prices.items() %}
        <tr>
            <td>{{ symbol }}</td>
            <td class="{{ info['class'] }}">{{ info['price'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    prices = {}
    for symbol in SYMBOLS:
        try:
            url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
            r = requests.get(url)
            price = float(r.json()["data"]["amount"])
            
            # Compare price movement
            if symbol in last_prices:
                if price > last_prices[symbol]:
                    color_class = "up"
                elif price < last_prices[symbol]:
                    color_class = "down"
                else:
                    color_class = ""
            else:
                color_class = ""
            
            prices[symbol] = {"price": f"${price:.4f}", "class": color_class}
            last_prices[symbol] = price

        except Exception as e:
            prices[symbol] = {"price": "Error", "class": "down"}
    return render_template_string(HTML_TEMPLATE, prices=prices)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
