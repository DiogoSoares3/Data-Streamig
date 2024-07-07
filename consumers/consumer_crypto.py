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
        'crypto_topic',
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


async def commit_bd(cripto_data):
    conn = await asyncpg.connect(
        database='Kafka',
        user=MY_USER,
        password=MY_PASSWORD,
        host='127.0.0.1'
    )

    try:
        async with conn.transaction():
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS crypto (
                    id SERIAL PRIMARY KEY,
                    ticket VARCHAR(10) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    price FLOAT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            ''')

            timestamp = parser.isoparse(cripto_data['timestamp'])

            await conn.execute('''
                INSERT INTO crypto(ticket, name, price, timestamp)
                VALUES($1, $2, $3, $4)
            ''', cripto_data['ticket'], cripto_data['name'], cripto_data['price'], timestamp)
    finally:
        await conn.close()


async def broadcast(message):
    if clients:
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients])


async def register_loop():
    while True:
        async with websockets.connect("ws://localhost:6791") as websocket:
            await register(websocket)


async def main():
    async with websockets.serve(register, "localhost", 6791):
        consumer_task = asyncio.create_task(consumer_handler())
        register_loop_task = asyncio.create_task(register_loop())

        await asyncio.gather(consumer_task, register_loop_task)


if __name__ == "__main__":
    asyncio.run(main())