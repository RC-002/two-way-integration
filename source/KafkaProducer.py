import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer


class syncProducer():
    kafka_server = ["localhost"]
    topic = "tests"
    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    def writeToTopic(self, method, ID, name=None, email=None):
        data = {
            "method": method,
            "Customer": {
                "ID": ID,
                "name": name,
                "email": email,
            }            
        }
        try:
            self.producer.send(self.topic, data)
        except:
            self.producer.flush()
        
   
        