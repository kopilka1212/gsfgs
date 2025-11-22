import customtkinter
import socket
import threading
from tkinter import END

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.username = "User" + str(hash(self))[:4]
        self.sock = None
        self.host = 'localhost'
        self.port = 8080

        self.title("Чат LogiTalk ")
        self.geometry("900x650")
        self.configure(fg_color="gray")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar_width = 230

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=self.sidebar_width, corner_radius=0, fg_color="burlywood"
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_visible = True

        self.close_sidebar_button = customtkinter.CTkButton(
            self.sidebar_frame, text="⮜", width=30, fg_color="wheat",
            hover_color="steelblue", command=self.toggle_sidebar
        )
        self.close_sidebar_button.grid(row=0, column=0, padx=5, pady=5, sticky="ne")

        self.sidebar_title_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Введіть налаштування",
            text_color="black", font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.sidebar_title_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.settings_entry = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text=self.username,
            fg_color="dimgray", text_color="black"
        )
        self.settings_entry.grid(row=2, column=0, padx=20, pady=10)

        self.connect_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Підключитися",
            fg_color="midnightblue", hover_color="royalblue",
            command=self.connect_to_server
        )
        self.connect_button.grid(row=3, column=0, padx=20, pady=10)

        self.open_sidebar_button = customtkinter.CTkButton(
            self, text="☰", width=30, fg_color="midnightblue",
            hover_color="royalblue", command=self.toggle_sidebar
        )
        self.open_sidebar_button.grid_remove()

        self.main_frame = customtkinter.CTkFrame(self, fg_color="tan")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)

        self.textbox = customtkinter.CTkTextbox(
            self.main_frame, wrap="word", fg_color="navy", text_color="lightgray"
        )
        self.textbox.insert("0.0", "Це поле повідомлень.\n")
        self.textbox.grid(row=0, column=0, columnspan=2,
                          padx=20, pady=(20, 10), sticky="nsew")

        self.input_entry = customtkinter.CTkEntry(
            self.main_frame, placeholder_text="Повідомлення...",
            fg_color="slategray", text_color="white"
        )
        self.input_entry.grid(row=1, column=0, padx=(20, 10),
                              pady=(10, 20), sticky="ew")

        self.send_button = customtkinter.CTkButton(
            self.main_frame, text="Відправити",
            fg_color="lightskyblue", hover_color="lime",
            command=self.send_message_wrapper
        )
        self.send_button.grid(row=1, column=1, padx=(0, 20),
                              pady=(10, 20), sticky="e")

        self.input_entry.bind("<Return>", lambda event: self.send_message_wrapper())

    def add_message(self, message):
        self.textbox.configure(state='normal')
        self.textbox.insert(END, f"[LogiTalk] {message}\n")
        self.textbox.configure(state='disabled')
        self.textbox.see(END)

    def connect_to_server(self):
        name = self.settings_entry.get() or self.username
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.send(name.encode())
            self.sock = sock
            self.username = name
            threading.Thread(target=self.recv_message, daemon=True).start()
            self.add_message(f"Підключено як {self.username}")
        except Exception:
            self.add_message('Не вдалося підключитися до сервера')

    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                self.after(0, lambda m=message: self.add_message(f"Нове повідомлення: {m}"))
            except Exception:
                self.after(0, lambda: self.add_message("З'єднання втрачено."))
                break
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_message_wrapper(self):
        message = self.input_entry.get()
        if not message or not self.sock:
            self.add_message("Повідомлення не відправлено (немає тексту або підключення).")
            return
        self.input_entry.delete(0, END)
        self.add_message(f"Ви: {message}")
        self.send_message(message)

    def send_message(self, message):
        try:
            self.sock.send(message.encode())
        except Exception:
            self.add_message("Помилка відправки.")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.sidebar_visible = False
            self.open_sidebar_button.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        else:
            self.open_sidebar_button.grid_remove()
            self.sidebar_visible = True
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

    def send_notification(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
