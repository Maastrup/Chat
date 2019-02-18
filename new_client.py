#!/Users/Svampen/anaconda3/envs/chat/bin/python

from tkinter import *
from threading import Lock, Thread

root = Tk()
root.title('Chit-chat')
root.config(width=60, height=23)

print_LOCK = Lock()


def my_print(msg, sending=True):
    print_LOCK.acquire()

    align = ''
    if sending:
        align = '>'

    # TODO: Take acount msg length
    if len(msg) <= 22:
        width = 94 - len(msg)
        msg_list.insert(
            END,
            '{:{align}{width}}'.format(
                my_msg.get(),
                align=align,
                width=width
            )
        )
    else:
        curr_line = ''

        for i in range(len(msg)):
            curr_line += msg[i]

            # Index 21 because len(curr_line) == 22
            if len(curr_line) == 22:
                msg_list.insert(END, '{:{align}72}'.format(curr_line, align=align))
                curr_line = ''
            elif i == len(msg) - 1:
                # TODO: Take acount msg length
                wrapper_length = 94 - len(curr_line)
                msg_list.insert(
                    END,
                    '{:{align}{width}}'.format(
                        curr_line,
                        align=align,
                        width=wrapper_length
                    )
                )

    print_LOCK.release()


def send(event=None):
    my_print(my_msg.get())
    # my_print(my_msg.get(), False)

    my_msg.set('')


msg_frame = Frame(root, bg='#e6e6e6')

scrollbar = Scrollbar(msg_frame)
scrollbar.pack(side=RIGHT, fill=Y)

msg_list = Listbox(msg_frame , yscrollcommand=scrollbar.set, width=40, height=15)
msg_list.pack(side=TOP, fill=Y)

msg_frame.grid(columnspan=2)


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
