#!/Users/Svampen/anaconda3/bin/python

import shutil
import socket
from threading import Thread


def receiver():
    while True:
        try:
            received = s.recv(1024).decode()
            print('\r' + ' '*20, end='\r')
            print(received)
            print('Your message:', end=' ', flush=True)
        except OSError:
            print('! -- Disconnected -- !')
            return


s = socket.socket()

host = socket.gethostname()
port = 6000

s.connect((host, port))

# Receives welcome msg
print(s.recv(1024).decode())
# Clients chooses name
s.send(bytes(input('Choose a name: '), 'utf-8'))


recv_thread = Thread(target=receiver)
recv_thread.start()

while True:
    msg = input('Your message: ')

    if msg == '\quit':
        s.send(bytes(msg, 'utf-8'))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        break
    else:
        columns, rows = shutil.get_terminal_size()
        print('\r' + ' ' * columns, end='\r')
        print('{:>{width}}'.format(msg, width=columns))
        s.sendall(bytes(msg, 'utf-8'))
