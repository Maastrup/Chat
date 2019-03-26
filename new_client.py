#!/Users/Svampen/anaconda3/envs/chat/bin/python3.7

from tkinter import *
from tkinter import messagebox
from threading import Lock, Thread
from Crypto.Hash import SHA3_256
import socket
import my_encryption as crypto
import pickle
import secrets

root = Tk()
root.title('Chit-chat')

print_LOCK = Lock()
curr_y = 0
msg_spacing = 6

# key = b'Sixteen byte keySixteen byte key'


def my_print(msg, sending=False):
    print_LOCK.acquire()

    global curr_y
    anchor = NW
    x = 3

    if sending:
        anchor = NE
        x = msg_list.winfo_width() # width of canvas
        my_msg.set('')

    item_handle = msg_list.create_text(
        x, curr_y,
        anchor=anchor,
        width=175,
        text=msg
    )

    curr_y = msg_list.bbox(item_handle)[3] + msg_spacing
    msg_list.config(scrollregion=msg_list.bbox('all'))
    msg_list.yview('moveto', 1.0)
    print_LOCK.release()


def send(event=None):
    msg = my_msg.get()
    s.send(crypto.pack(msg, key))
    my_print(msg, True)


def receiver():
    while True:
        try:
            received = s.recv(1024)
            text = crypto.unpack(received, key)
            if text is '{server closed}':
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root.destroy()
                    # return
                else:
                    my_print('None of your messages are sent, since server has shutdown')
                    return
            else:
                my_print(text)
        except OSError:
            print('! -- Disconnected -- !')
            return


def on_closing():
    try:
        s.send(crypto.pack('{quit}', key))
        s.close()
    except BrokenPipeError:
        print('Server not available at the moment')
    root.destroy()


"""GUI SETUP"""
scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.grid(column=2, row=0, sticky=N+S)

msg_list = Canvas(
    root,
    yscrollcommand=scrollbar.set,
    width=355,
    height=250,
    bg='#e9e9e9',
    highlightthickness=0
)
msg_list.grid(row=0, columnspan=2)

scrollbar.config(command=msg_list.yview)

my_msg = StringVar()
my_msg.set('Type your message here')

entry = Entry(root, textvariable=my_msg)
entry.bind('<FocusIn>', lambda e: my_msg.set(''))
entry.bind('<Return>', send)
entry.grid(sticky=E)

img = PhotoImage(file='Resources/ikon.png')
button = Button(
    root,
    image=img,
    command=send
)
button.grid(column=1, row=1, sticky=N+W)

msg_list.config(scrollregion=msg_list.bbox('all'))
root.protocol("WM_DELETE_WINDOW", on_closing)

"""CONNECTION SETUP"""
s = socket.socket()

host = 'KJs-MacBook-Pro.local'
port = 6000

s.connect((host, port))

s.send(bytes('{CLIENT}', 'utf-8'))

""" Diffie-Hellman key exchange first thing after 
    establishing a connection
"""

# Receive base, g, and prime modulus, p
g, p = pickle.loads(s.recv(2048))

print('g: {}, p: {}'.format(g, p))

# g^a mod p
a = secrets.randbits(128)
A = pow(g, a, p)
s.send(pickle.dumps(A))

# receive servers exponential modulus
B = pickle.loads(s.recv(1024))
shared_secret = pow(B, a, p)

key = SHA3_256.new(data=bytes(str(shared_secret), 'utf-8')).digest()

print('Shared key:', key)


# Receives welcome msg
my_print(crypto.unpack(s.recv(1024), key))

recv_thread = Thread(target=receiver)
recv_thread.start()


""" Start program """
root.mainloop()
