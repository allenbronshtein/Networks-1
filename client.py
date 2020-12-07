from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
dest_ip = '127.0.0.1'
dest_port = 12345
msg = input("Message to send:")
while not msg == 'quit':
    s.sendto(msg.encode(), (dest_ip, dest_port))
    while True:
        data, sender_info = s.recvfrom(2048)
        if data.decode() == "halt":
            break
        print(data.decode())
    msg = input("Message to send:")
s.close()

