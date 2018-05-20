#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Geekbrains - Python Level 2 - Homework Messenger
# Author: Kardash Vadim
# https://github.com/kardvv/GB_messenger
# The pytests for client part of messenger


import pytest
import time

import client

def test_client_time():
    assert client.client_time() == int(time.time())

def test_encoding_message():
    test = {'action': 'presence'}
    test_b = b'{"action": "presence"}'
    assert client.encoding_message(test) == test_b

def test_decoding_message():
    test = {'action': 'probe'}
    test_b = b'{"action": "probe"}'
    assert client.decoding_message(test_b) == test

if __name__ == "__main__":
    test_client_time()
    test_encoding_message()
    test_decoding_message()
