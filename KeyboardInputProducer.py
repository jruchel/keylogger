from kafka import KafkaProducer
from user_details import UserDetails

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'keyboardInput'


def send_user_details(user_details: UserDetails):
    global topic
    producer.send(topic, user_details.to_json())
