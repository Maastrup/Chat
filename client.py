#!/Users/Svampen/anaconda3/bin/python

import shutil
import socket
from threading import Thread
from my_encryption import MyAES

s = socket.socket()
host = socket.gethostname()
port = 6000

crypto = MyAES(b'Sixteen byte keySixteen byte key')

# """ Encryption globals """
# key = b'Sixteen byte keySixteen byte key'
# cipher = AES.new(key, AES.MODE_ECB)
# padding = 'acbdefghijklmnop'


def receiver():
    while True:
        try:
            received = s.recv(1024)
            msg = crypto.unpack(received)
            print('\r' + ' '*20, end='\r')
            print(msg)
            print('Your message:', end=' ', flush=True)
        except OSError:
            print('! -- Disconnected -- !')
            return


s.connect((host, port))

# Receives welcome msg
print(crypto.unpack(s.recv(1024)))
# Clients chooses name
s.send(crypto.pack(input('Choose a name: ')))


recv_thread = Thread(target=receiver)
recv_thread.start()

while True:
    msg = input('Your message: ')

    if msg == '{quit}':
        s.send(crypto.pack(msg))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        break
    else:
        columns, rows = shutil.get_terminal_size()
        print('\r' + ' ' * columns, end='\r')
        print('{:>{width}}'.format(msg, width=columns))
        s.sendall(crypto.pack(msg))
