from kafka import KafkaConsumer

IP_ADDRESS= "...."
kafka_consumer = KafkaConsumer(
    "Test",
    bootstrap_servers=f"{IP_ADDRESS}:9092",
    auto_offset_reset="earliest"
)

for message in kafka_consumer:
    print(message.value.decode("utf-8"))