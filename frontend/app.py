import streamlit as st
import asyncio
import websockets
import json
import polars as pl
import altair as alt
import os


def read_data(type):
    if type == 0:
        file_path = "frontend/cache/data_american_stocks.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return []
    elif type == 1:
        file_path = "frontend/cache/data_brazilian_stocks.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return []
    else:
        file_path = "frontend/cache/data_crypto.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return []


def write_data(data, type):
    if type == 0:
        file_path = "frontend/cache/data_american_stocks.json"
        with open(file_path, "w") as f:
            json.dump(data, f)
    elif type == 1:
        file_path = "frontend/cache/data_brazilian_stocks.json"
        with open(file_path, "w") as f:
            json.dump(data, f)
    else:
        file_path = "frontend/cache/data_crypto.json"
        with open(file_path, "w") as f:
            json.dump(data, f)
     
  
def transform_data(data):    
    unified_data = [item for sublist in data for item in sublist]
    df = pl.DataFrame(unified_data)
    return df


st.title('Stocks and Crypto Prices in Real Time!')

placeholder = st.empty()

refresh_rate = st.sidebar.slider('Refresh rate (seconds)', min_value=1, max_value=60, value=1)


def load_graph(message, type):
    if message:
        data = json.loads(message)
        current_data1 = read_data(type)
        current_data1.append(data)
        write_data(current_data1, type)
  
    current_data1 = read_data(0)
    current_data2 = read_data(1)
    current_data3 = read_data(2)
   
    df1 = transform_data(current_data1)
    df2 = transform_data(current_data2)
    df3 = transform_data(current_data3)
    
    with placeholder.container():
        chart1 = alt.Chart(df1).mark_line().encode(
            x='timestamp:T',
            y='price:Q',
            color='ticket:N'
        ).properties(
            title='Big Techs stock prices over the time',
            width=800,
            height=400
        )

        chart2 = alt.Chart(df2).mark_line().encode(
            x='timestamp:T',
            y='price:Q',
            color='ticket:N'
        ).properties(
            title='Main brazilian stock prices over the time',
            width=800,
            height=400
        )

        chart3 = alt.Chart(df3).mark_line().encode(
            x='timestamp:T',
            y='price:Q',
            color='ticket:N'
        ).properties(
            title='Main crypto prices over the time',
            width=800,
            height=400
        )
        
        st.altair_chart(chart1)
        st.altair_chart(chart2)
        st.altair_chart(chart3)


async def listen_to_server_stocks():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        while True:

            load_graph(False, type=0)
            message = await websocket.recv()
            load_graph(message, type=0)

            await websocket.close()
            
            await asyncio.sleep(refresh_rate)
            st.rerun()

            
async def listen_to_server_acoes():
    uri = "ws://localhost:6790"
    async with websockets.connect(uri) as websocket:
        while True:

            load_graph(False, type=1)
            message = await websocket.recv()
            load_graph(message, type=1)

            await websocket.close()
            
            await asyncio.sleep(refresh_rate)
            st.rerun()

            
async def listen_to_server_cripto():
    uri = "ws://localhost:6791"
    async with websockets.connect(uri) as websocket:
        while True:

            load_graph(False, type=2)
            message = await websocket.recv()
            load_graph(message, type=2)

            await websocket.close()
            
            await asyncio.sleep(refresh_rate)
            st.rerun()


async def main():
    task_1 = asyncio.create_task(listen_to_server_stocks())
    task_2 = asyncio.create_task(listen_to_server_acoes())
    task_3 = asyncio.create_task(listen_to_server_cripto())

    await asyncio.gather(task_1, task_2, task_3)


if __name__ == "__main__":
    asyncio.run(main())
