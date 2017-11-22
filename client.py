#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

try:
    METHOD = str.upper(sys.argv[1])
    puerto = sys.argv[2].split("@")[1].split(":")
    SERVER = sys.argv[2].split("@")[0]
    IP = puerto[0]
    PORT = int(puerto[1])
    LINE = METHOD + " sip:" + SERVER + "@" + IP + " SIP/2.0"
except:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))
    print(LINE)
    my_socket.send(bytes(LINE, "utf-8") + b"\r\n")
    data = my_socket.recv(1024)
    server_doc = data.decode("utf-8").split(" ")
    LINE_ACK = "ACK" + " sip:" + SERVER + "@" + IP + " SIP/2.0"
    METHOD_SERVER = server_doc[2].split("\r\n")[0]
    if METHOD_SERVER == "Trying":
        my_socket.send(bytes(LINE_ACK, "utf-8") + b"\r\n")
    else:
        pass
    print(data.decode("utf-8"))
    print("Terminando socket...")
print("Fin.")
