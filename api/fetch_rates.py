import requests
from server.db_operations import insert_price

def fetch_and_store_prices():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,the-open-network&vs_currencies=usd,eur')
        data = response.json()

        for crypto, prices in data.items():
            insert_price(crypto, prices['usd'], prices['eur'])
    except Exception as e:
        print(f"Ошибка при обновлении данных: {e}")

if __name__ == "__main__":
    fetch_and_store_prices()