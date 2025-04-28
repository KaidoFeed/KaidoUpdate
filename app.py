from flask import Flask
import requests
import threading
import time

app = Flask(__name__)

price_data = {
    "BTC": None,
    "ETH": None,
    "LTC": None,
    "DOGE": None
}

def fetch_prices():
    while True:
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin,dogecoin&vs_currencies=usd')
            if response.status_code == 200:
                data = response.json()
                price_data['BTC'] = data['bitcoin']['usd']
                price_data['ETH'] = data['ethereum']['usd']
                price_data['LTC'] = data['litecoin']['usd']
                price_data['DOGE'] = data['dogecoin']['usd']
        except Exception as e:
            print("Error fetching prices:", e)
        time.sleep(30)

@app.route('/')
def index():
    html = """
    <html>
    <head>
        <title>Kaido - Live Crypto Prices</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #0a0a0a; color: white; text-align: center; }
            table { margin: auto; border-collapse: collapse; margin-top: 50px; }
            th, td { padding: 15px; border: 1px solid white; }
            th { background-color: #333; }
            tr:nth-child(even) { background-color: #222; }
        </style>
    </head>
    <body>
        <h1>Kaido - Live Crypto Prices</h1>
        <table>
            <tr><th>Crypto</th><th>Price (USD)</th></tr>
            <tr><td>BTC</td><td>${}</td></tr>
            <tr><td>ETH</td><td>${}</td></tr>
            <tr><td>LTC</td><td>${}</td></tr>
            <tr><td>DOGE</td><td>${}</td></tr>
        </table>
    </body>
    </html>
    """.format(price_data['BTC'], price_data['ETH'], price_data['LTC'], price_data['DOGE'])
    return html

if __name__ == '__main__':
    price_thread = threading.Thread(target=fetch_prices)
    price_thread.start()
    app.run(host='0.0.0.0', port=10000)
