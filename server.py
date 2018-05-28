#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Geekbrains - Python Level 2 - Homework Messenger
# Author: Kardash Vadim
# https://github.com/kardvv/GB_messenger
# The client part of messenger

import select
import socket
import json
import time
import sys
import argparse
import server_log


version = '0.2'

# Constant
users = []
size = 1024

# decorration for logger
def log(func):
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        server_log.logger.info('{}({}, {}) = {}'.format(func.__name__, args, kwargs, res))
        return res
    return decorated

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
@log
def encoding_message(message):
    message_json = json.dumps(message)
    message_b = message_json.encode('utf-8')
    return message_b


# convert message after receiving from server
@log
def decoding_message(message_b):
    message_json = message_b.decode('utf-8')
    message = json.loads(message_json)
    return message


# Messages
probe_message = {
    'action': 'probe',
    'time': server_time()
}

def connection_requests(client, clients):
    try:
        client.send(encoding_message(probe_message))
        data = client.recv(size)
        input_message = decoding_message(data)
        if input_message['action'] == 'presence':
            server_log.logger.info('User: {} connection. Status: {}.'.format(
				input_message['user']['name'], input_message['user']['status'])
            )
            clients.append(client)
    except:
        server_log.logger.info('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
        clients.remove(client)
    return


if __name__ == '__main__':
    # command line parameters parser
    command_param = param_parser()
    command_param_name = command_param.parse_args(sys.argv[1:])
    listen_addr = command_param_name.a
    server_port = command_param_name.p

    # Create TCP soket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Start connection to server
    server_socket.bind((listen_addr, server_port))
    # waiting for requests
    # maximum 5 requests at a time
    server_socket.listen(5)
    server_socket.settimeout(0.2)

    clients = []

    # Main part
    while True:
        try:
            client, addr = server_socket.accept()
        except socket.timeout:
            pass
        else:
            server_log.logger.info('Received a connection request from {}'.format(addr))
            connection_requests(client, clients)
        finally:
            writes = []
            reads = []
            try:
                writes, reads, e = select.select(clients, clients, clients, 0)
            except:
                pass

            for client in writes:
                try:
                    data = client.recv(size)
                    input_message = decoding_message(data)
                    for client in reads:
                        try:
                            client.send(encoding_message(input_message))
                        except:
                            clients.remove(client)
            
                except:
                    server_log.logger.info('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                    clients.remove(client)
                    client.close()

    server_log.logger.info('Server stoped!')
