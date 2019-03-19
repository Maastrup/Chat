#!/Users/Svampen/anaconda3/bin/python

import socket
from threading import Thread, Lock
import my_encryption

""" Socket globals """
clients = {}
LOCK = Lock()
server_status = True



def broadcast(msg, name=None):
    LOCK.acquire()
    print('Broadcasting to {} client(s)'.format(len(clients)))
    for client in clients:
        if name == None:
            client.send(msg)
        elif clients[client] != name:
            msg_to_broadc = my_encryption.pack(name + ': ' + msg)
            client.send(msg_to_broadc)
    LOCK.release()


def accept_clients():
    while server_status:
        # Accept connection from the outside
        (clientsocket, address) = server_socket.accept()
        # Start thread to handle the client
        thread1 = Thread(target=handle_client, args=(clientsocket, address, ))
        thread1.start()


def handle_client(client, addr):
    # clientIndex = len(clients)

    print('Client connected with address {}:{}'.format(addr[0], addr[1]))

    # Welcome the client
    msg = 'Welcome to the chat program. Please enter your chosen name in the message field and press enter' # Please enter a chat channel (1 through 5) and press enter: '
    client.sendall(my_encryption.pack(msg))

    print('Getting name...')
    name = my_encryption.unpack(client.recv(1024))

    print('Name is ' + name)

    if name == '{GHOST}' or name == '\quit':
        return

    LOCK.acquire()
    clients[client] = name
    LOCK.release()

    client.sendall(my_encryption.pack('Hi {}, now you can start chatting with your friends'.format(name)))

    while True:
        try:
            received = client.recv(1024)
            msg = my_encryption.unpack(received)
            if msg == '\quit':
                print('! -- Client disconnected -- !')

                LOCK.acquire()
                del clients[client]
                LOCK.release()

                exit_msg = name + ' has left the chatroom'
                broadcast(exit_msg)

                return
            else:
                # msg = name + received
                broadcast(msg, clients[client])

        except OSError:
            print('! -- Client disconnected -- !')

            LOCK.acquire()
            del clients[client]
            LOCK.release()

            return


def exit_handler():
    # server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    print('Server is shutting down. Goodbye for now.')


def ghost_client():
    print('\\\\------- GHOSTING ACCEPT THREAD -------//')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 6000

    s.connect((host, port))
    s.send(my_encryption.pack('{GHOST}'))
    s.shutdown(socket.SHUT_RDWR)
    s.close()


# Create INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to a public host and a well-known port
server_socket.bind((socket.gethostname(), 6000))

# Become a server by listening
server_socket.listen(5)

accept_thread = Thread(target=accept_clients)
accept_thread.start()

while True:
    command = input()
    if command == '\quit':
        print('Server is shutting down.')
        print('Waiting for clients to disconnect...')

        server_status = False
        ghost_client()
        accept_thread.join()
        server_socket.close()
        print('Goodbye for now.')
        break
