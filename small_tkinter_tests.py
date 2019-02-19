#!/Users/Svampen/anaconda3/envs/chat/bin/python


from tkinter import *

root = Tk()


# class MsgDisplay:
#     def __init__(self, master, **kw):
#         apply(Canvas.__init__, (self, master), kw)


w = Canvas(root, width=355, height=250, bg='#e6e6e6', highlightthickness=0) # correct msg_box size
w.grid()

scrollbar = Scrollbar(root)
scrollbar.grid(column=1, row=0)

item_handler = w.create_text(3, 0, anchor=NW, tags='t1', width=165, text='Hegfdhdfddytredcfgytredcfvghtfrdcvbghygtfcdvbhytfdxcvbghytrfdcvghytfrdcvbgtfrdcvghytfrjsa')
w.create_text(3, 114, anchor=NW, tags='t2', text='Hejsa')

print(w.bbox(item_handler)[3])



mainloop()
