import json
from kafka import KafkaConsumer
from db.service import dbService

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

            # Get customer data from event
            customer = data.value["Customer"]
            id = customer["ID"]
            name = customer["name"]
            email = customer["email"]

            if(data.value["method"] == "create"):
                dbService().createCustomerFromEvent(id, name, email)
            
            elif(data.value["method"] == "update"):
                dbService().updateCustomerFromEvent(id, name, email)
            
            elif(data.value["method"] == "delete"):
                dbService().deleteCustomerFromEvent(id)

if __name__ == "__main__":
    syncConsumer().sync()