import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # define socket variable and socket type
s.bind((socket.gethostname(),1234)) # bind socket to the host and port
s.listen(5)  # listen will accept an integer that will define the max connections


while True:
    client, address = s.accept()
    print(f"Connection from {address} has been accepted!")
    client.send(bytes("Welome to lo.", encoding="utf-8"))