#!/Users/Svampen/anaconda3/envs/chat/bin/python

from tkinter import *
import socket
from threading import Lock, Thread
from my_encryption import MyAES

root = Tk()
root.title('Chit-chat')

print_LOCK = Lock()
curr_y = 0
msg_spacing = 6

crypto = MyAES(b'Sixteen byte keySixteen byte key')


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

    print_LOCK.release()


def send(event=None):
    msg = my_msg.get()
    s.send(crypto.pack(msg))
    my_print(msg, True)
    # my_print(my_msg.get(), False)


def receiver():
    while True:
        try:
            received = s.recv(1024)
            text = crypto.unpack(received)
            my_print(text)
        except OSError:
            print('! -- Disconnected -- !')
            return


def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    s.send(crypto.pack('{quit}'))
    s.close()
    root.destroy()


"""GUI SETUP"""
scrollbar = Scrollbar(root)
scrollbar.grid(column=2, row=0, sticky=W+N+S)

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

root.protocol("WM_DELETE_WINDOW", on_closing)

"""CONNECTION SETUP"""
s = socket.socket()

host = socket.gethostname()
port = 6000

s.connect((host, port))

# Receives welcome msg
my_print(crypto.unpack(s.recv(1024)))

recv_thread = Thread(target=receiver)
recv_thread.start()


""" Start program """
root.mainloop()
