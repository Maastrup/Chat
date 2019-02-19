#!/Users/Svampen/anaconda3/envs/chat/bin/python

from tkinter import *
from threading import Lock, Thread

root = Tk()
root.title('Chit-chat')

print_LOCK = Lock()
curr_y = 0
msg_spacing = 4


def my_print(msg, sending=True):
    print_LOCK.acquire()

    global curr_y
    anchor = NW
    x = 3

    if sending:
        anchor = NE
        x = msg_list.winfo_width() # width of canvas

    item_handler = msg_list.create_text(
        x, curr_y,
        anchor=anchor,
        width=165,
        text=msg
    )

    my_msg.set('')
    curr_y = msg_list.bbox(item_handler)[3] + msg_spacing

    print(curr_y)

    print_LOCK.release()


def send(event=None):
    my_print(my_msg.get())
    # my_print(my_msg.get(), False)


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

root.mainloop()
