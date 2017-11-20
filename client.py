#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys
# Cliente UDP simple.

# Dirección IP del servidor.
try:
    METHOD = sys.argv[1]
    puerto = sys.argv[2].split("@")[1].split(":")
    SERVER = sys.argv[2].split("@")[0]
    IP = puerto[0]
    PORT = int(puerto[1])
    LINE = METHOD + " " + "sip:" + SERVER + "@" + IP + " " + 'SIP/2.0'
except:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    print(LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    server_doc = data.decode('utf-8').split(" ")
    METHOD_SERVER = server_doc[2]
    METHODS = "Trying","Ring","OK"
    LINE_ACK = "ACK" + " " + "sip:" + SERVER + "@" + IP + " " + 'SIP/2.0' 
    if METHOD_SERVER == METHODS:
        my_socket.send(bytes(LINE_ACK, 'utf-8') + b'\r\n')
    else:
        pass
    print(data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
