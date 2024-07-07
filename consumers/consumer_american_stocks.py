import asyncio
import websockets
import json
from aiokafka import AIOKafkaConsumer
import asyncpg
from dotenv import load_dotenv
import os
from dateutil import parser


load_dotenv()

MY_USER = os.getenv('MY_USER')
MY_PASSWORD = os.getenv('MY_PASSWORD')

clients = set()

async def register(websocket):
    clients.add(websocket)
    try: 
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        

async def consumer_handler():
    consumer = AIOKafkaConsumer(
        'american_stocks_topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        auto_commit_interval_ms=1000,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    await consumer.start()
    try:
        while True:
            async for message in consumer:
                print(f"Consumed message: {message.value}")
                data = message.value
                await broadcast(data)
                
                for i in range(len(data)):
                    await commit_bd(data[i])
    finally:
        await consumer.stop()



async def commit_bd(stock_data):
    conn = await asyncpg.connect(
        database='Kafka',
        user=MY_USER,
        password=MY_PASSWORD,
        host='127.0.0.1'
    )

    try:
        async with conn.transaction():
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS american_stocks (
                    id SERIAL PRIMARY KEY,
                    ticket VARCHAR(10) NOT NULL,
                    price FLOAT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            ''')
            
            timestamp = parser.isoparse(stock_data['timestamp'])
            
            await conn.execute('''
                INSERT INTO american_stocks(ticket, price, timestamp)
                VALUES($1, $2, $3)
            ''', stock_data['ticket'], stock_data['price'], timestamp)
    finally:
        await conn.close()


async def broadcast(message):
    if clients:
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients])
    

async def register_loop():
    while True:
        async with websockets.connect("ws://localhost:6789") as websocket:
            await register(websocket)

async def main():
    async with websockets.serve(register, "localhost", 6789):
        consumer_task = asyncio.create_task(consumer_handler())
        register_loop_task = asyncio.create_task(register_loop())

        await asyncio.gather(consumer_task, register_loop_task)

if __name__ == "__main__":
    asyncio.run(main())