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
        description='Server part of messenger',
        epilog='GB_messenger (c) 2018.',
    )
    parent_group = parser.add_argument_group(title='Options')
#    parent_group.add_argument('--help', '-h', action='help', help='Справка')
    parent_group.add_argument('--ver',
                              action='version',
                              help='Version',
                              version='%(prog)s {}'.format(version)
                              )
    parent_group.add_argument('--a', default='localhost', help='IP-adress for listening (default all ip)')
    parent_group.add_argument('--p', type=int, default=7777, help='Server socket (default 7777)')
    return parser


# Current time of client
def server_time():
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
probe_message = {
    'action': 'probe',
    'time': server_time()
}

if __name__ == '__main__':
    # command line parameters parser
    command_param = param_parser()
    command_param_name = command_param.parse_args(sys.argv[1:])
    listen_addr = command_param_name.a
    server_port = command_param_name.p

    print('Server is start!')
    # Create TCP soket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Start connection to server
    server_socket.bind((listen_addr, server_port))
    # waiting for requests
    # maximum 5 requests at a time
    server_socket.listen(5)

    # Main part
    while True:
        print('Waiting connection from clients')
        client, addr = server_socket.accept()
        print('Received a connection request from {}'.format(addr))
        # sending a massage
        client.send(encoding_message(probe_message))
        data = client.recv(1024)
        input_message = decoding_message(data)
        if input_message['action'] == 'presence':
            print('User: {} connection. Status: {}.'.format(
                input_message['user']['name'],input_message['user']['status'])
            )
        # поэтому выполняется кодирование строки
        client.close()

    print('Server is stop!')
