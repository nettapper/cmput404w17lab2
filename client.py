#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET indicates that we want ipv4 socket
# socket.SOCK_STREAM indicates we want a TCP socket

clientSocket.connect(("www.google.com", 80))
# note that there is no http://, working at a lower level (we're doing the protocol)
# port 80 is the standard http port

request = "GET / HTTP/1.0\r\n\r\n"  # the server will be waiting for us to send that blank line

clientSocket.sendall(request)

response = bytearray()
while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print response
