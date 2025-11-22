from customtkinter import *

def click():
    global score
    score += 1
    score_text.configure(text=f"{score}")

win = CTk()
win.geometry("400x400")
win.title("Clicker")
font = ("Arial", 30, "bold")
score = 0

score_text = CTkLabel(win, text=f"{score}", font=font, text_color="red")
score_text.pack(pady=15)

click_btn = CTkButton(win,text="click",command=click,width=150, font=("Arial", 20, "bold"))
click_btn.pack(side="bottom", pady=10)

win.mainloop()
