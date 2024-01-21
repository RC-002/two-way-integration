import json
from kafka import KafkaConsumer
from stripeService import stripeService

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
            customer = data.value["Customer"]
            id = customer["ID"]
            name = customer["name"]
            email = customer["email"]

            if(data.value["method"] == "create"):
                stripeCustomer = stripeService().createCustomer(email, name)
                print(stripeCustomer)
            
            elif(data.value["method"] == "update"):
                stripeCustomer = stripeService().updateCustomer(id, email, name)
                print(stripeCustomer)
            
            elif(data.value["method"] == "delete"):
                stripeCustomer = stripeService().deleteCustomer(id)

if __name__ == "__main__":
    syncConsumer().sync()