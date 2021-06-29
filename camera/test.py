#!/usr/bin/env python3
import socket
import time
import picamera
import json

CAST_GROUP = '239.255.1.2'
CAST_PORT  = 1234
CMD_GROUP  = '239.255.1.1'
CMD_PORT   = 1234

CAST_TTL = 2
CMD_TTL = 2

camera = picamera.PiCamera()
camera.resolution = (1024,768)
camera.framerate = 24

stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
stream_socket.connect((CAST_GROUP, CAST_PORT))

command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
command_socket.connect((CMD_GROUP, CMD_PORT))

connection = stream_socket.makefile('wb') 

def start_stream():
    camera.start_recording(connection, format='h264')

def stop_stream():
    try:
        camera.stop_recording()
    finally:
        connection.close()

def start_record():
    camera.start_recording('highres.h264', splitter_port=2)

def stop_stream():
    camera.stop_recording(splitter_port=2)

def checkMessage(message):
    print("Recieved message: %s"%message)
    commands = json.loads(message)
    print(commands)

start_stream()

try:
    while True:
        data, addr = command_socket.recv(4096)
        print(addr)
        checkMessage(data)
finally:
    stop_stream()
    stop_record()
    connection.close()
    stream_socket.close()
    command_socket.close()

