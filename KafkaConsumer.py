import json
from kafka import KafkaConsumer
from customers.service import stripeService

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
            data = next(self.consumer)

            if(data.value["method"] == "create"):
                customer = data.value["Customer"]
                name = customer["name"]
                email = customer["email"]
                
                stripeCustomer = stripeService().createCustomer(email, name)
