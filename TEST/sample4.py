from tkinter import *

root = Tk()

w = Canvas(root, width=480, height=320, background='gray')
w.pack()

line = w.create_line(0, 50, 400, 50, dash=(4, 4), fill='yellow')
rect = w.create_rectangle(120, 80, 360, 240, outline='red')
oval = w.create_oval(120, 80, 360, 240, fill='pink')
text = w.create_text(240, 160, text='Chick')

w.coords(line, 50, 50, 400, 100)
w.itemconfig(rect, fill='blue')
w.delete(oval)

mainloop()