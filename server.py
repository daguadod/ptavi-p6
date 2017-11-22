#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import socketserver

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
Not_Allowed = b"SIP/2.0 405 Method Not Allowed\r\n"


class EchoHandler(socketserver.DatagramRequestHandler):
    def handle(self):
            line = self.rfile.read()
            doc = line.decode("utf-8").split(" ")
            METHOD = doc[0]
            if len(doc) < 4 and len(doc) > 0:
                if METHOD == "INVITE":
                    print("INVITE RECIVED")
                    self.wfile.write(TRYING + RINGING + OK)
                elif METHOD == "BYE":
                    print("BYE RECIVED")
                    self.wfile.write(OK)
                elif METHOD == "ACK":
                    print("ACK RECIVED")
                    aEjecutar = "./mp32rtp -i 127.0.0.1 -p 23032 <" + FILE
                    os.system(aEjecutar)
                else:
                    self.wfile.write(Not_Allowed)
            else:
                self.wfile.write(BAD)
if __name__ == "__main__":
    serv = socketserver.UDPServer(("", PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
