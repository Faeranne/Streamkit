import socket, json, time, struct

CMD_GROUP = '239.255.1.1'
CMD_PORT = 1234
CMD_TTS = 2

command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
command_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, CMD_TTS)
command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
command_socket.bind((CMD_GROUP, CMD_PORT))

mreq = struct.pack("4sl", socket.inet_aton(CMD_GROUP), socket.INADDR_ANY)

command_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(json.dumps(command_socket.recv(4096).decode('utf-8')))
