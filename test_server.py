#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Geekbrains - Python Level 2 - Homework Messenger
# Author: Kardash Vadim
# https://github.com/kardvv/GB_messenger
# The pytests for server part of messenger


import pytest
import time

import server

def test_server_time():
    assert server.server_time() == int(time.time())

def test_encoding_message():
    test = {'action': 'presence'}
    test_b = b'{"action": "presence"}'
    assert server.encoding_message(test) == test_b

def test_decoding_message():
    test = {'action': 'probe'}
    test_b = b'{"action": "probe"}'
    assert server.decoding_message(test_b) == test

if __name__ == "__main__":
    test_server_time()
    test_encoding_message()
    test_decoding_message()
