import requests
from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def fetch_crypto_prices():
    response = requests.get("http://localhost:8000/cripto")
    if response.status_code == 200:
        return response.json()


def produce_crypto_prices():
    while True: 
        stock_prices = fetch_crypto_prices()
        if stock_prices:
            producer.send('crypto_topic', stock_prices)
            print("Crypto prices obtained. Waiting for new updates!")


if __name__ == "__main__":
    produce_crypto_prices()