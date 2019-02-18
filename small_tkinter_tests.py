#!/Users/Svampen/anaconda3/envs/chat/bin/python


from tkinter import *

root = Tk()


# class MsgDisplay:
#     def __init__(self, master, **kw):
#         apply(Canvas.__init__, (self, master), kw)


w = Canvas(root, width=355, height=250, bg='#e6e6e6') # correct msg_box size
w.grid()

scrollbar = Scrollbar(root)
scrollbar.grid(column=1, row=0)

w.create_text(3, 0, anchor=NW, text='Hejsa')

mainloop()
