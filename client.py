#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Geekbrains - Python Level 2 - Homework Messenger
# Author: Kardash Vadim
# https://github.com/kardvv/GB_messenger
# The client part of messenger

import socket
import json
import time
import sys
import argparse

version = '0.1'

# Constant
client_name = 'Test_Client'
client_status = 'Test_Status'


# param from command line
def param_parser():
    parser = argparse.ArgumentParser(
        prog='GB_messenger',
        description='Client part of messenger',
        epilog='GB_messenger (c) 2018.',
    )
    parent_group = parser.add_argument_group(title='Options')
#    parent_group.add_argument('--help', '-h', action='help', help='Справка')
    parent_group.add_argument('--ver',
                              action='version',
                              help='Version',
                              version='%(prog)s {}'.format(version)
    )
    parent_group.add_argument('--addr', default='localhost', help='Server ip (default localhost)')
    parent_group.add_argument('--port', type=int, default=7777, help='Server socket (default 7777)')
    return parser


# Current time of client
def client_time():
    return int(time.time())


# convert message before sending to server
def encoding_message(message):
    message_json = json.dumps(message)
    message_b = message_json.encode('utf-8')
    return message_b


# convert message after receiving from server
def decoding_message(message_b):
    message_json = message_b.decode('utf-8')
    message = json.loads(message_json)
    return message


# Messages
connection_message = {
    'action': 'presence',
    'time': client_time(),
    'user': {
        'name': client_name,
        'status': client_status
    }
}

if __name__ == '__main__':
    # command line parameters parser
    command_param = param_parser()
    command_param_name = command_param.parse_args(sys.argv[1:])
    server_addr = command_param_name.addr
    server_port = command_param_name.port

    print('Client is start!')
    # Create TCP soket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # start connection to server
        client_socket.connect((server_addr, server_port))
        # receiving from server
        data = client_socket.recv(1024)
        input_message = decoding_message(data)
        #
        if input_message['action'] == 'probe':
            print('Connection to Server is OK!')
            client_socket.send(encoding_message(connection_message))
        # close connection to server
        client_socket.close()
    except ConnectionRefusedError:
        print('Server is not answer')

    print('Client is stop!')
