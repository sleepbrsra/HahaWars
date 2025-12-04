import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

BG_COLOR = "#1E1E2F"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#9B59B6"
CARD_COLOR = "#2C2C3E"

CARD_DISPLAY_WIDTH = 160
CARD_DISPLAY_HEIGHT = 240
HAND_PADDING = 10

# --- глобальные переменные для GUI ---
current_situation = ""
player_hand = []
table_cards = []
selected_card = {"path": None}
game_frame = None
client = None  # объект RoomClient для отправки сыгранной карты


def load_card_image(path, w=CARD_DISPLAY_WIDTH, h=CARD_DISPLAY_HEIGHT):
    img = Image.open(path)
    img = img.resize((w, h))
    return ImageTk.PhotoImage(img)


def start_game_gui(frame, hand, situation, cl):
    """
    frame: контейнер game_frame из HUB
    hand: список путей карт игрока
    situation: текст ситуации
    cl: объект RoomClient
    """
    global game_frame, player_hand, current_situation, client, table_cards, selected_card
    game_frame = frame
    player_hand = hand
    current_situation = situation
    client = cl
    table_cards.clear()
    selected_card["path"] = None
    update_gui()


def update_gui():
    global game_frame
    if not game_frame:
        return
    for w in game_frame.winfo_children():
        w.destroy()

    # --- Ситуация ---
    tk.Label(
        game_frame,
        text=f"Ситуация: {current_situation}",
        bg=BG_COLOR,
        fg=FG_COLOR,
        font=("Arial", 16, "bold"),
        wraplength=700,
        justify="center"
    ).pack(pady=10)

    # --- Стол ---
    table_frame = tk.Frame(game_frame, bg=BG_COLOR)
    table_frame.pack(fill="both", expand=True, pady=10)
    for card_path in table_cards:
        img = load_card_image(card_path)
        lbl = tk.Label(table_frame, image=img, bg=BG_COLOR)
        lbl.image = img
        lbl.pack(side="left", padx=10)

    # --- Рука игрока ---
    hand_frame = tk.Frame(game_frame, bg=BG_COLOR)
    hand_frame.pack(pady=10)

    for card_path in player_hand:
        img = load_card_image(card_path, 120, 180)
        btn = tk.Button(
            hand_frame,
            image=img,
            bg=BG_COLOR,
            bd=3,
            highlightthickness=2,
            highlightbackground=ACCENT_COLOR if selected_card["path"] == card_path else BG_COLOR,
            command=lambda p=card_path: select_card(p)
        )
        btn.image = img
        btn.pack(side="left", padx=HAND_PADDING)

    # --- Кнопки ---
    buttons_frame = tk.Frame(game_frame, bg=BG_COLOR)
    buttons_frame.pack(pady=10)
    tk.Button(
        buttons_frame,
        text="Сыграть карту",
        command=play_card,
        bg=ACCENT_COLOR,
        fg=FG_COLOR,
        font=("Arial", 12)
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Проголосовать",
        command=lambda: messagebox.showinfo("Инфо", "Голосование ещё не реализовано"),
        bg=ACCENT_COLOR,
        fg=FG_COLOR,
        font=("Arial", 12)
    ).pack(side="left", padx=10)


def select_card(path):
    selected_card["path"] = path
    update_gui()


def play_card():
    path = selected_card["path"]
    if not path:
        messagebox.showwarning("Предупреждение", "Выберите карту!")
        return
    if path not in player_hand:
        messagebox.showerror("Ошибка", "Карты нет в руке")
        return

    # удаляем карту из руки игрока и добавляем на стол
    table_cards.append(path)
    player_hand.remove(path)
    selected_card["path"] = None
    update_gui()

    # отправляем серверу через RoomClient
    if client:
        client.send_move(path)  # <-- вот это уже есть в client.py


def handle_server_message(msg):
    """
    msg: словарь от RoomClient
    """
    global current_situation, player_hand, table_cards
    t = msg.get("type")

    if t == "game_start":
        # Запуск GUI игры
        start_game_gui(game_frame, msg["hand"], msg["situation"], client)

    elif t == "player_move":
        # Добавляем карту на стол
        card_path = msg["card"]
        table_cards.append(card_path)
        # если игрок локальный, убираем карту из руки
        if msg.get("player") == client.name and card_path in player_hand:
            player_hand.remove(card_path)
        update_gui()

    elif t == "update_table":
        table_cards.clear()
        table_cards.extend(msg["table"])
        update_gui()

    elif t == "game_end":
        messagebox.showinfo("Игра завершена", msg.get("reason", "Игра завершена"))
        # очищаем GUI
        for w in game_frame.winfo_children():
            w.destroy()
