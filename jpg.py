from customtkinter import *

win = CTk()
win.geometry("800x600")
def button_adaptive():
    window_width = win.winfo_width()
    btn.configure(width=window_width-120)
    win.after(50,button_adaptive)

btn = CTkButton(win, text = "кнопка", width=300,height=100)
btn.place(x=50, y=40)

button_adaptive()

win.mainloop()