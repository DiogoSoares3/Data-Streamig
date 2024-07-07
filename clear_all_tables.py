import asyncpg
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
MY_USER = os.getenv('MY_USER')
MY_PASSWORD = os.getenv('MY_PASSWORD')


async def clear_tables():

    conn = await asyncpg.connect(
        database='Kafka', 
        user=MY_USER, 
        password=MY_PASSWORD, 
        host='127.0.0.1',
    )

    try:
        async with conn.transaction():
                        
            await conn.execute('''
                TRUNCATE american_stocks;
                TRUNCATE crypto;
                TRUNCATE brazilian_stocks;
            ''')
                        
    finally:
        await conn.close()
        

if __name__ == "__main__":
    asyncio.run(clear_tables())