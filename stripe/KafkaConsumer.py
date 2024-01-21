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

            if(data.value["method"] == "create"):
                customer = data.value["Customer"]
                name = customer["name"]
                email = customer["email"]
                stripeCustomer = stripeService().createCustomer(email, name)
                print(stripeCustomer)
            
            elif(data.value["method"] == "update"):
                print("Here")
                customer = data.value["Customer"]
                name = customer["name"]
                email = customer["email"]
                
                stripeCustomer = stripeService().updateCustomer(email, name)
                print(stripeCustomer)
            
            elif(data.value["method"] == "delete"):
                customer = data.value["Customer"]
                stripe_id = customer["ID"]
                
                stripeCustomer = stripeService().deleteCustomer(stripe_id)

if __name__ == "__main__":
    syncConsumer().sync()