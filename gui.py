import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import os
import json
from game_logic import Game

from modules.server import RoomServer
from modules.client import RoomClient

import io
import base64

# ---------------- Конфиги ----------------
BG_COLOR = "#1e1e2e"
FG_COLOR = "#dcd6f7"
ACCENT_COLOR = "#9a4dff"
USER_BG = "#2e2e3e"
AVATARS_DIR = "avatars"
USER_DATA_FILE = "user_data.json"

# ---------------- Работа с JSON ----------------
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------------- HUB ----------------
def start_hub(user_data, network=None):
    # ---------------- Инициализация ----------------
    if not user_data:
        user_data = {"name": "Игрок", "avatar": "Отсутствует"}

    if not network:
        network = {"status": "idle"}
    else:
        network["status"] = "idle"

    # --- ВАЖНО: создаём переменные, чтобы nonlocal работал ---
    server_obj = None
    client_obj = None
    is_host = False

    players_imgs = []
    # ---------------- GUI ----------------
    root = tk.Tk()
    root.title("HahaWars HUB")
    root.configure(bg=BG_COLOR)
    root.geometry("1000x600")

    
    # ---------------- Верхняя панель ----------------
    top_frame = tk.Frame(root, bg=BG_COLOR, height=80)
    top_frame.pack(fill="x", side="top")

    # ЛОГОТИП
    logo_path = "./etc/logo.png"
    if os.path.exists(logo_path):
        img = Image.open(logo_path).resize((150, 80))
        logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(top_frame, image=logo_img, bg=BG_COLOR)
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=20)
    else:
        logo_label = tk.Label(top_frame, text="HAHAWARS",
                              font=("Arial", 24, "bold"),
                              bg=BG_COLOR, fg=ACCENT_COLOR)
        logo_label.pack(side="left", padx=20)

    right_top_frame = tk.Frame(top_frame, bg=BG_COLOR)
    right_top_frame.pack(side="right", padx=20)

    name_label = tk.Label(right_top_frame, text=user_data['name'],
                          font=("Arial", 16, "bold"),
                          bg=BG_COLOR, fg=FG_COLOR)
    name_label.pack()

    avatar_label = tk.Label(right_top_frame, bg=BG_COLOR)
    avatar_label.pack()

    def render_avatar():
        avatar_path = user_data['avatar']
        if avatar_path != "Отсутствует" and os.path.exists(avatar_path):
            img = Image.open(avatar_path).resize((60, 60))
            avatar_img = ImageTk.PhotoImage(img)
            avatar_label.config(image=avatar_img)
            avatar_label.image = avatar_img
        else:
            avatar_label.config(text="Аватар отсутствует", image="")

    render_avatar()

    # ---------------- Основные фреймы ----------------
    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(main_frame, bg=BG_COLOR, width=300)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    game_frame = tk.Frame(main_frame, bg=BG_COLOR)
    game_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ---------------- Редактор профиля ----------------
    def open_profile_editor():
        editor = tk.Toplevel(root)
        editor.title("Редактирование профиля")
        editor.configure(bg=BG_COLOR)
        editor.geometry("400x250")

        tk.Label(editor, text="Имя:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12)).pack(pady=10)
        name_entry = tk.Entry(editor, font=("Arial", 14))
        name_entry.insert(0, user_data['name'])
        name_entry.pack()

        selected_avatar_path = ["Отсутствует"]
        
        server_obj = None
        
        client_obj = None




        def choose_avatar():
            path = filedialog.askopenfilename(title="Выберите аватарку", filetypes=[("PNG/JPG", "*.png *.jpg *.jpeg")])
            if path:
                selected_avatar_path[0] = path
                avatar_preview = Image.open(path).resize((80, 80))
                avatar_img = ImageTk.PhotoImage(avatar_preview)
                avatar_label_preview.config(image=avatar_img)
                avatar_label_preview.image = avatar_img

        tk.Button(editor, text="Выбрать аватар", command=choose_avatar, bg=ACCENT_COLOR, fg=FG_COLOR).pack(pady=5)
        avatar_label_preview = tk.Label(editor, bg=BG_COLOR)
        avatar_label_preview.pack(pady=5)

        def save_profile():
            # Обновляем имя
            user_data['name'] = name_entry.get()
            name_label.config(text=user_data['name'])
            # Копируем аватарку
            if selected_avatar_path[0] != "Отсутствует":
                if not os.path.exists(AVATARS_DIR):
                    os.makedirs(AVATARS_DIR)
                dest = os.path.join(AVATARS_DIR, os.path.basename(selected_avatar_path[0]))
                shutil.copy(selected_avatar_path[0], dest)
                user_data['avatar'] = dest
                render_avatar()
            save_user_data(user_data)
            editor.destroy()

        tk.Button(editor, text="Сохранить", command=save_profile, bg=ACCENT_COLOR, fg=FG_COLOR).pack(pady=10)

    # ---------------- HUB Логика ----------------
    def show_idle():
        for w in left_frame.winfo_children():
            w.destroy()
        tk.Label(left_frame, text="Вы не в комнате", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(left_frame, text="Создать комнату", command=create_room, bg=ACCENT_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)
        tk.Button(left_frame, text="Присоединиться к комнате", command=join_room, bg=ACCENT_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)
        tk.Button(left_frame, text="Редактировать профиль", command=open_profile_editor, bg=ACCENT_COLOR, fg=FG_COLOR, font=("Arial", 14)).pack(pady=10)

        for w in game_frame.winfo_children():
            w.destroy()
        tk.Label(game_frame, text="Игровая зона недоступна\nВы не в комнате", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 16)).pack(pady=50)

    def start_game():
        tk.messagebox.showinfo("Игра", "Игра начинается! (здесь будет запуск Game)")
        # Здесь можно добавить интеграцию с game_logic:
        # game_obj = Game(players=network['room']['players'])
        # game_obj.start()


    def show_in_game():
        nonlocal players_imgs
        players_imgs.clear()

        room_info = network.get('room', {})

        # --- Очистка фреймов ---
        for w in left_frame.winfo_children():
            w.destroy()
        for w in game_frame.winfo_children():
            w.destroy()

        # ---------------- LEFT_FRAME ----------------
        # --- Информация о комнате ---
        server_frame = tk.LabelFrame(left_frame, text="Сервер", bg=USER_BG, fg=FG_COLOR)
        server_frame.pack(fill="x", pady=10)

        tk.Label(
            server_frame,
            text=f"Название комнаты: {room_info.get('name', '—')}\nСтатус: онлайн",
            bg=USER_BG, fg=FG_COLOR
        ).pack(padx=10, pady=10)

        # --- Игроки с аватарками ---
        users_frame = tk.LabelFrame(left_frame, text="Игроки", bg=USER_BG, fg=FG_COLOR)
        users_frame.pack(fill="both", expand=True, pady=10)

        players_container = tk.Frame(users_frame, bg=USER_BG)
        players_container.pack(fill="both", expand=True, padx=10, pady=5)

        for p in room_info.get('players', []):
            player_name = p["name"]
            avatar_b64 = p.get("avatar")

            frame = tk.Frame(players_container, bg=USER_BG)
            frame.pack(fill="x", pady=2)

            if avatar_b64:
                img_data = base64.b64decode(avatar_b64)
                img = Image.open(io.BytesIO(img_data)).resize((40, 40))
                photo = ImageTk.PhotoImage(img)
                players_imgs.append(photo)
                tk.Label(frame, image=photo, bg=USER_BG).pack(side="left", padx=5)
            else:
                tk.Label(frame, text="❓", bg=USER_BG, fg=FG_COLOR, width=4).pack(side="left", padx=5)

            tk.Label(frame, text=player_name, bg=USER_BG, fg=FG_COLOR, font=("Arial", 12)).pack(side="left", padx=5)

        # --- Кнопки хоста ---
        if is_host:
            tk.Button(left_frame, text="Начать игру",
                    bg=ACCENT_COLOR, fg=FG_COLOR, font=("Arial", 14),
                    command=start_game).pack(pady=10)

        tk.Button(left_frame, text="Выйти из комнаты",
                bg=ACCENT_COLOR, fg=FG_COLOR, font=("Arial", 14),
                command=leave_room).pack(pady=10)

        # ---------------- GAME_FRAME ----------------
        tk.Label(game_frame, text=f"Игровая зона\nКомната: {room_info.get('name', '—')}",
                bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 16)).pack(pady=50)







    # ---------------- Кнопки комнаты ----------------
    def create_room():
        nonlocal server_obj, client_obj, is_host

        # Если сервер уже есть — останавливаем
        if server_obj:
            server_obj.stop()
            server_obj = None

        # Создаём сервер
        server_obj = RoomServer(room_name=f"Комната {user_data['name']}")
        server_obj.start()

        # Подключаемся как клиент (локальный)
        client_obj = RoomClient(
            name=user_data["name"],
            avatar_path=user_data.get("avatar"),  # передаем путь к аватарке
            server_ip="127.0.0.1",
            callback=network_update
        )
        client_obj.connect()

        is_host = True
        network["status"] = "in_game"

        # Добавляем себя локально в комнату как словарь
        network["room"] = {
            "name": f"Комната {user_data['name']}",
            "players": [{"name": user_data['name'], "avatar": None}]
        }

        refresh_hub()  # обновляем GUI





    def join_room():
        nonlocal client_obj, is_host

        ip = simple_input("Введите IP друга:")
        if not ip:
            return

        # Подключаемся как клиент
        client_obj = RoomClient(
            name=user_data["name"],
            avatar_path=user_data.get("avatar"),  # <-- передаем путь к аватарке
            server_ip=ip,
            callback=network_update
        )

        if client_obj.connect():
            is_host = False
            network["status"] = "in_game"
        else:
            tk.messagebox.showerror("Ошибка", "Не удалось подключиться")

        refresh_hub()




    def simple_input(text):
        win = tk.Toplevel(root)
        win.title("Ввод")
        win.geometry("300x120")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text=text, fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        result = {"value": None}

        def ok():
            result["value"] = entry.get()
            win.destroy()

        tk.Button(win, text="OK", command=ok, bg=ACCENT_COLOR).pack(pady=10)
        win.wait_window()
        return result["value"]

    def network_update(data):
        if data["type"] == "room_state":
            network["room"] = {
                "name": data["room_name"],
                "players": data["players"]
            }
            refresh_hub()


    def leave_room():
        nonlocal server_obj, client_obj, is_host

        # если игрок просто клиент
        if client_obj:
            client_obj.disconnect()
            client_obj = None

        # если это хост — закрыть сервер
        if is_host and server_obj:
            server_obj.stop()
            server_obj = None

        is_host = False
        network['status'] = "idle"
        network['room'] = {}

        refresh_hub()


    # ---------------- Обновление HUB ----------------
    def refresh_hub():
        status = network.get("status", "idle")
        if status == "idle":
            show_idle()
        else:
            show_in_game()

    refresh_hub()
    root.mainloop()
