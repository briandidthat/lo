import socket
import select
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")  # ask user for their username


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# Set connection to non-blocking state, so .recv() call wont block, just return some exception that we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them.  We need to encode username to bytes, then count number of bytes and prepare header of fixed size,
# that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    # Wait for user to input a message
    message = input(f'{my_username} > ')
                
    if message:  # If message is not empty - send it
        message = message.encode('utf-8')  # Encode message to bytes,
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')  #  prepare header and convert to bytes
        client_socket.send(message_header + message)  # send message to server

    try:
        while True:  # Now we want to loop over received messages (there might be more than one) and print them

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())  # Convert header to int value
            username = client_socket.recv(username_length).decode('utf-8') # Receive and decode username

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print(f'Reading error: {str(e)}')
            sys.exit()
        
        continue  # We just did not receive anything

    except Exception as e:
        # Any other exception - something happened, exit
        print(f'Reading error: {str(e)}')
        sys.exit()