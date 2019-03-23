#!/Users/Svampen/anaconda3/envs/chat/bin/python3.7

from Crypto.Hash import SHA3_256
import socket
import threading
import my_encryption as crypto
import pickle
import secrets

""" Socket globals """
clients = {}
LOCK = threading.Lock()
server_status = True

""" Diffie-Hellman base and prime """
# key = b'Sixteen byte keySixteen byte key'
p = crypto.gen_big_prime()
g = crypto.gen_base()
print('g: {}, p: {}'.format(g, p))
base_and_prime = pickle.dumps((g, p))


def broadcast(msg, name=None):
    LOCK.acquire()
    print('Broadcasting to {} client(s)'.format(len(clients)))
    for client in clients:
        key = clients[client][1]
        if name is None:
            client.send(crypto.pack(msg, key))
        elif clients[client][0] != name:
            msg_to_broadc = crypto.pack(name + ': ' + msg, key)
            client.send(msg_to_broadc)
    LOCK.release()


def accept_clients():
    while server_status:
        # Accept connection from the outside
        (clientsocket, address) = server_socket.accept()
        # Start thread to handle the client
        thread1 = threading.Thread(target=handle_client, args=(clientsocket, address, ))
        thread1.start()


def handle_client(client, addr):
    print('Entity connected with address {}:{}'.format(addr[0], addr[1]))

    id = client.recv(1024).decode()
    if id == '{GHOST}':
        print('Entity was GHOST')
        return
    elif id == '{CLIENT}':
        print('Entity is CLIENT')
    else:
        print('ID: {} is unknown. Exiting...'.format(id))
        return

    """ Diffie-Hellman key exchange first thing after 
        establishing a connection
    """
    # send base and prime
    client.sendall(base_and_prime)

    b = secrets.randbits(128)

    # Receive A and compute A^b mod p as DH-key
    A = pickle.loads(client.recv(1024))
    shared_secret = pow(A, b, p)

    # Compute g^b mod p and send to client
    B = pow(g, b, p)
    client.sendall(pickle.dumps(B))

    print('Shared key:', shared_secret)

    key = SHA3_256.new(data=bytes(str(shared_secret), 'utf-8')).digest()

    # Welcome the client
    msg = 'Welcome to the chat program. Please enter your chosen name in the message field and press enter' # Please enter a chat channel (1 through 5) and press enter: '
    client.sendall(crypto.pack(msg, key))

    print('Getting name...')
    name = crypto.unpack(client.recv(1024), key)

    if name == '{quit}':
        print('Client quit before choosing name')
        return

    print('Name is ' + name)

    LOCK.acquire()
    clients[client] = (name, key)
    LOCK.release()

    client.sendall(crypto.pack('Hi {}, now you can start chatting with your friends'.format(name), key))
    broadcast('{} joined the chatroom'.format(name))

    while True:
        try:
            received = client.recv(1024)
            msg = crypto.unpack(received, key)
            if msg == '{quit}':
                print('! -- Client disconnected -- !')

                LOCK.acquire()
                del clients[client]
                LOCK.release()

                exit_msg = name + ' has left the chatroom'
                broadcast(exit_msg)

                return
            else:
                # msg = name + received
                broadcast(msg, clients[client][0])

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
    s.send(bytes('{GHOST}', 'utf-8'))
    s.close()


# Create INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to a public host and a well-known port
server_socket.bind((socket.gethostname(), 6000))

# Become a server by listening
server_socket.listen(5)

accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

while True:
    command = input()
    if command == '{quit}':
        print('Server is shutting down.')
        print('Waiting for clients to disconnect...')

        server_status = False
        ghost_client()
        accept_thread.join()
        server_socket.close()
        print('Goodbye for now.')
        break
    elif command == 'status':
        print('Active threads: {}'.format(threading.active_count()))
        print('Accept thread up: {}'.format(accept_thread.is_alive()))
