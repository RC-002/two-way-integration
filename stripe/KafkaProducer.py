import json
from kafka import KafkaProducer


class syncProducer():
    kafka_server = ["localhost"]
    topic = "stripe_outgoing"
    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    def writeToTopic(self, method, customer):
        data = {
            "method": method,
            "Customer": customer        
        }
        try:
            self.producer.send(self.topic, data)
        except:
            self.producer.flush()
        
   
        