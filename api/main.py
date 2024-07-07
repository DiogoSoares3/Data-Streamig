from fastapi import FastAPI
import random
from datetime import datetime
import time
from pydantic import BaseModel
from typing import List


app = FastAPI()

class USStock(BaseModel):
    ticket: str
    price: float
    timestamp: datetime


class BRStock(BaseModel):
    ticket: str
    price: float
    timestamp: datetime


class Crypto(BaseModel):
    ticket: str
    name: str
    price: float
    timestamp: datetime


@app.get("/brazilian-stocks", response_model=List[BRStock])
async def get_acoes_brasileiras():
    acoes = [
        BRStock(ticket="PETR4", price=generate_random_price(20.0, 30.0), timestamp=datetime.now()),
        BRStock(ticket="ITUB4", price=generate_random_price(15.0, 25.0), timestamp=datetime.now()),
        BRStock(ticket="VALE3", price=generate_random_price(90.0, 110.0), timestamp=datetime.now()),
        BRStock(ticket="ABEV3", price=generate_random_price(14.0, 18.0), timestamp=datetime.now())
    ]
    
    random_time = random.uniform(0.5, 3)
    time.sleep(random_time)

    return acoes


@app.get("/american-stocks", response_model=List[USStock])
async def get_stock_prices():
    stocks = [
        USStock(ticket="AMZN", price=generate_random_price(170, 185), timestamp=datetime.now()),
        USStock(ticket="GOOGL", price=generate_random_price(160, 176), timestamp=datetime.now()),
        USStock(ticket="MSFT", price=generate_random_price(195.0, 213), timestamp=datetime.now()),
        USStock(ticket="AAPL", price=generate_random_price(204.0, 227.0), timestamp=datetime.now())
    ]
    
    random_time = random.uniform(0.5, 3)
    time.sleep(random_time)

    return stocks


@app.get("/cripto", response_model=List[Crypto])
async def get_criptomoedas():
    criptos = [
        Crypto(ticket="BTC", name="Bitcoin", price=generate_random_price(30000.0, 40000.0), timestamp=datetime.now()),
        Crypto(ticket="ETH", name="Ethereum", price=generate_random_price(2000.0, 3000.0), timestamp=datetime.now()),
        Crypto(ticket="XMR", name="Monero", price=generate_random_price(150.0, 250.0), timestamp=datetime.now()),
        Crypto(ticket="SOL", name="Solana", price=generate_random_price(40.0, 60.0), timestamp=datetime.now())
    ]
    
    random_time = random.uniform(0.5, 3)
    time.sleep(random_time)

    return criptos


def generate_random_price(min_value: float, max_value: float) -> float:
    return random.uniform(min_value, max_value)



if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1",
                port=8000, log_level='info',
                reload=True)
