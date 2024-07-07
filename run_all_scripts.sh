#!/usr/bin/env bash

PORT=8000

# Initialising containers
start_containers() {
  docker compose up -d
  while ! docker compose ps | grep -q "Up"; do
    sleep 1; done
  echo "Containers initialised!"
}

#Call
start_containers

# initialising FastAPI app
python3 ./api/main.py &

# Wait for FastAPI initialisation
while ! nc -z localhost $PORT; do
  echo "Waiting for FastAPI initialisation at the port $PORT..."
  sleep 1; done

echo 'FastAPI initialised'

# Initialise producers
python3 ./producers/producer_american_stocks.py &
python3 ./producers/producer_brazilian_stocks.py &
python3 ./producers/producer_crypto.py &

# Initialise consumers
python3 ./consumers/consumer_american_stocks.py &
python3 ./consumers/consumer_brazilian_stocks.py &
python3 ./consumers/consumer_crypto.py &

#Execução
#streamlit run ./app.py
streamlit run frontend/app.py


# Wait and out
wait && exit 0
