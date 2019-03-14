#!/Users/Svampen/anaconda3/envs/chat/bin/python

from tkinter import *
from tkinter import messagebox
from threading import Lock, Thread
import socket

root = Tk()
root.title('Chit-chat')

print_LOCK = Lock()
curr_y = 0
msg_spacing = 4


def my_print(msg, sending=False):
    print_LOCK.acquire()

    global curr_y
    anchor = NW
    x = 3

    if sending:
        anchor = NE
        x = msg_list.winfo_width() # width of canvas
        my_msg.set('')

    item_handler = msg_list.create_text(
        x, curr_y,
        anchor=anchor,
        width=175,
        text=msg
    )

    curr_y = msg_list.bbox(item_handler)[3] + msg_spacing

    print_LOCK.release()


def send(event=None):
    msg = my_msg.get()
    my_print(msg, True)
    s.send(bytes(msg, 'utf-8'))
    # my_print(my_msg.get(), False)


def receiver():
    while True:
        try:
            received = s.recv(1024).decode()
            my_print(received)
        except OSError:
            print('! -- Disconnected -- !')
            return


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        s.send(bytes('\quit', 'utf-8'))
        s.close()
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

root.update()
msg_list.config(scrollregion=msg_list.bbox('all'))


"""CONNECTION SETUP"""
s = socket.socket()

host = socket.gethostname()
port = 6000

s.connect((host, port))

# Receives welcome msg
my_print(s.recv(1024).decode())

recv_thread = Thread(target=receiver)
recv_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
