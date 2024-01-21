import json
from kafka import KafkaConsumer

class syncConsumer:
    kafka_server = ["localhost"]

    topic = "stripe_outgoing"

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_server,
        value_deserializer=json.loads,
        auto_offset_reset="latest",
    )

    consumer.subscribe(topic)

    def sync(self):
        while True:
            data = next(self.consumer)
            print(data.value)

if __name__ == "__main__":
    syncConsumer().sync()