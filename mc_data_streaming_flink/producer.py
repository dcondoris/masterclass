from kafka import KafkaProducer
from tqdm import tqdm

IP_ADDRESS= "...."
kafka_producer = KafkaProducer(
  bootstrap_servers=f"{IP_ADDRESS}:9093"
)


import json

path = "/home/ubuntu/mc_streaming/large_tweets.json"

with open(path, 'r') as file:
    tweets = json.load(file)



import time 
import random

n_tweets = len(tweets)

for i in tqdm(range(1, 3000)):
    time.sleep(.5)
    kafka_producer.send(
        topic="Twitter",
        value=json.dumps(tweets[random.randint(0, n_tweets)-1]).encode("utf-8")
    )

kafka_producer.flush()