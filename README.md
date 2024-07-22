# Streaming data project to monitor the price of financial assets

The implementation of the project consisted of creating a fictitious API that returned the price of financial assets at random times. Kafka producers were responsible for receiving the data from the API and sending it to their specific topics on the Kafka broker. Kafka consumers then consumed the data present in these topics and sent it via Websockets to a front-end application for visualisation. The whole process, from collecting the data, organising it, processing it and sending it to the front-end, was done in real time. The tools used in the project were FastAPI, Apache Kafka, Websockets and Streamlit.

### How to run the code


### References
https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
