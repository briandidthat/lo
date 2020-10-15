import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # define socket variable and socket type.
s.connect((socket.gethostname(), 1234))

msg = s.recv(1024)  # socket.rcv will recieve a stream of bytes, you must define a max
print(msg.decode(encoding="utf-8"))