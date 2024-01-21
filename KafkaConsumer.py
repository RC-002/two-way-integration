import json
from kafka import KafkaConsumer, KafkaProducer


class syncConsumer:
    kafka_server = ["localhost"]

    topic = "tests"

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_server,
        value_deserializer=json.loads,
        auto_offset_reset="latest",
    )

    consumer.subscribe(topic)

    def sync(self):
        while True:
            print("\n....................\n")
            data = next(self.consumer)
            print(data)