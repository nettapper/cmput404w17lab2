#!/usr/bin/env python

import socket
import os
from random import randint

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # should help the 'port in use'

portNum = randint(8000, 8800)
print ("Using port number ", portNum)
print ("########################")

# Note: 0.0.0.0 will listen on ALL addrs for this machine
serverSocket.bind(("0.0.0.0", portNum))  # only root users can use ports less than 1024
serverSocket.listen(5)  # start listening, up to 5 connections in a queue

while True:
  (incomingSocket, address) = serverSocket.accept()
  print "We got a connection from %s" % (str(address))
  if os.fork() != 0:
      continue

  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  clientSocket.connect(("www.google.com", 80))

  incomingSocket.setblocking(0)
  clientSocket.setblocking(0)

  while True:  # keep checking if client/server has something to say
    request = bytearray()
    while True:  # request connection from client
      try:
        part = incomingSocket.recv(1024)
      except IOError, e:
        if e.errno == 11:
          part = None
        else:
          raise
      if (part):
        clientSocket.sendall(part)
        request.extend(part)
      else:
        break

    if len(request) > 0:
      print "### REQUEST ###"
      print request

    response = bytearray()
    while True:  # response from server
      try:
        part = clientSocket.recv(1024)
      except IOError, e:
        if e.errno == 11:
          part = None
        else:
          raise
      if (part):
        incomingSocket.sendall(part)
        response.extend(part)
      else:
        break

    if len(response) > 0:
      print "### RESPONSE ###"
      print response
