import tkinter as tk
from tkinter import messagebox
import random

CARDS_POOL = [
    "Карта мемного момента 1",
    "Карта мемного момента 2",
    "Карта мемного момента 3",
    "Карта мемного момента 4",
    "Карта мемного момента 5",
    "Карта мемного момента 6",
    "Карта мемного момента 7",
]

class Game:
    def __init__(self, window, user_data):
        self.window = window
        self.user_data = user_data
        self.window.configure(bg="#1e1e2e")
        self.scores = {user_data['name']: 0}
        self.current_cards = []

    def start_round(self):
        self.current_cards = random.sample(CARDS_POOL, 5)
        self.show_cards()

    def show_cards(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Label(self.window, text="Выберите карту:", bg="#1e1e2e", fg="#dcd6f7", font=("Arial", 16)).pack(pady=10)

        for card in self.current_cards:
            btn = tk.Button(self.window, text=card, command=lambda c=card: self.select_card(c),
                            bg="#9a4dff", fg="#dcd6f7", font=("Arial", 14))
            btn.pack(pady=5)

    def select_card(self, card):
        messagebox.showinfo("Выбор карты", f"Вы выбрали: {card}")
        self.scores[self.user_data['name']] += 1
        self.start_round()

    def start_game():
        tk.messagebox.showinfo("Игра", "Игра начинается! (здесь будет запуск Game)")
        # Пример: game_obj = Game(players=network['room']['players'])
        # game_obj.start()
