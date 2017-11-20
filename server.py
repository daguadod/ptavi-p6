#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    FILE = sys.argv[3] 
except:
    sys.exit("Usage: python3 server.py IP port audio_file")

if not os.path.exists(FILE):
    sys.exit("Document does not exist")
      


TRYING = b"SIP/2.0 100 Trying\r\n"
RINGING = b"SIP/2.0 180 Ringing\r\n"
OK = b"SIP/2.0 200 OK\r\n"
BAD = b"SIP/2.0 400 Bad Request\r\n"
Not_Allowed =b"SIP/2.0 405 Method Not Allowed\r\n"

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        doc = line.decode('utf-8').split(" ")
        METHOD = doc[0]
        if METHOD == "INVITE":
            print("INVITE RECIVED")
            self.wfile.write(TRYING + RINGING + OK)
            aEjecutar = 'chmod +x mp32rtp & mp32rtp -i 127.0.0.1 -p 23032 <' + FILE
            os.system(aEjecutar)
        elif METHOD == "BYE":
            print("BYE RECIVED")
            self.wfile.write(OK)
        elif METHOD == "ACK":
            pass
        else:
            self.wfile.write(Not_Allowed)
        
        # Si no hay más líneas salimos del bucle infinito

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
        
