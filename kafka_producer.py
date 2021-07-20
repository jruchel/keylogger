from kafka import KafkaProducer
from user_details import UserDetails


class KeyboardInputProducer:

    def __init__(self, bootstrap_server: str, topic: str):
        self.bootstrap_server = bootstrap_server
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_server)

    def publish_message(self, user_details: UserDetails):
        self.producer.send(topic=self.topic, key=bytes(user_details.ipAddress, encoding='utf8'), value=bytes(user_details.message, encoding='utf8'))
