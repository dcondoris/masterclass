from kafka import KafkaConsumer
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentiment_analyzer = SentimentIntensityAnalyzer()

IP_ADDRESS= "...."
kafka_consumer = KafkaConsumer(
    "Twitter",
    bootstrap_servers=f"{IP_ADDRESS}:9092",
    auto_offset_reset="earliest"
)


for message in kafka_consumer:
    # print(message.value[:20], end="")
    dict_ = json.loads(message.value)
    score = sentiment_analyzer.polarity_scores(dict_["text"])["compound"]
    # col.insert_one(dict_)
    with open("sentiment_scores.txt", "a") as file:
        file.write(str(score) + "\n")