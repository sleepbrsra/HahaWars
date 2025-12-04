from .userdata import save_user_data, load_user_data
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

AVATAR_DIR = "avatars"

class ProfileWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HahaWars – Профиль")
        self.root.geometry("450x400")
        self.root.configure(bg="#0f0f0f")
        self.avatar_selected = None

        if not os.path.exists(AVATAR_DIR):
            os.makedirs(AVATAR_DIR)

    def show(self):
        frame = tk.Frame(self.root, bg="#0f0f0f")
        frame.pack(expand=True)

        tk.Label(frame, text="НАСТРОЙКА ПРОФИЛЯ", font=("Arial",26,"bold"), fg="#9146ff", bg="#0f0f0f").pack(pady=20)
        tk.Label(frame, text="Имя:", font=("Arial",16), fg="#e6e6e6", bg="#0f0f0f").pack()
        self.name_entry = tk.Entry(frame, font=("Arial",16), bg="#1c1c1c", fg="#e6e6e6", insertbackground="#e6e6e6")
        self.name_entry.pack(pady=10)

        data = load_user_data()
        if data:
            self.name_entry.insert(0, data["username"])
            self.avatar_selected = data.get("avatar", None)

        tk.Label(frame, text="Выберите аватарку:", font=("Arial",16), fg="#e6e6e6", bg="#0f0f0f").pack(pady=10)
        gallery = tk.Frame(frame, bg="#0f0f0f")
        gallery.pack()

        self.avatar_images = {}
        for file in os.listdir(AVATAR_DIR):
            if file.lower().endswith((".png",".jpg",".jpeg")):
                path = os.path.join(AVATAR_DIR, file)
                img = Image.open(path).resize((80,80))
                img_tk = ImageTk.PhotoImage(img)
                self.avatar_images[file] = img_tk
                btn = tk.Button(gallery, image=img_tk, bg="#1c1c1c", relief="flat", command=lambda f=path: self.select_avatar(f))
                btn.pack(side="left", padx=10)

        tk.Button(frame, text="СОХРАНИТЬ", font=("Arial",18,"bold"), bg="#9146ff", fg="white", relief="flat", command=self.continue_to_hub).pack(pady=20)
        self.root.mainloop()

    def select_avatar(self, path):
        self.avatar_selected = path

    def continue_to_hub(self):
        username = self.name_entry.get().strip()
        if not username or not self.avatar_selected:
            messagebox.showwarning("Ошибка", "Введите имя и выберите аватарку!")
            return
        save_user_data(username, self.avatar_selected)
        self.root.destroy()
        from .hub import HubWindow
        HubWindow(tk.Tk(), username, self.avatar_selected).show()
