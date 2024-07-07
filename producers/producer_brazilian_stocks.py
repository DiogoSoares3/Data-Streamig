import requests
from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def fetch_stock_prices():
    response = requests.get("http://localhost:8000/brazilian-stocks")
    if response.status_code == 200:
        return response.json()


def produce_stock_price():
    while True: 
        stock_prices = fetch_stock_prices()
        if stock_prices:
            producer.send('brazilian_stocks_topic', stock_prices)
            print("Brazilian stock prices obtained. Waiting for new updates!")


if __name__ == "__main__":
    produce_stock_price()