========================================
HahaWars
========================================

![HahaWars Banner](./etc/banner.png)


Network Meme Card Game with Dark Aesthetic

---

Description
-----------
HahaWars is a networked card game where players receive 5 random cards with text and choose the funniest card for the current situation. The card with the most votes wins the round. The game keeps score and shows the final results.

The project is designed for fun, learning network interactions, and practicing GUI development with Python Tkinter and socket networking.

---

How It Works
------------

1. Rooms
- Players can **create a room** or **join** an existing one.
- The host runs a local server and connects as a client.
- All players send their data (name and avatar) to the server.
- The server broadcasts the current room state: list of players and their avatars.

2. Gameplay
- Each player receives 5 random cards.
- In each round, players select the card they think fits the situation best.
- After voting, the round winner is determined.
- Scores are tracked and final results are displayed.

3. Interface
- GUI is in a dark theme with purple accents.
- Left panel shows room info and players.
- Right panel is the game area.
- Player avatars are base64-encoded and displayed next to names.
- The host sees a **"Start Game"** button; clients do not.

4. Profile
- Players can edit their name and avatar.
- Avatars are stored in the `avatars/` folder.
- User data is saved in `user_data.json`.

---

Installation & Running
----------------------
1. Clone the repository:

    git clone <YOUR_REPOSITORY_URL>
    cd HahaWars

2. Install dependencies:

    pip install pillow

3. Run the game:

    python3 main.py

4. Enjoy!

---

Project Structure
-----------------
.
├── avatars/        # Player avatars
├── etc/            # Logos and extra images
├── modules/        # Client, server, and helper modules
├── game_logic.py   # Main game logic
├── gui.py          # Game interface
├── main.py         # Entry point
├── user_data.json  # Current user data
└── LICENSE         # CC BY-NC 4.0 License

---

License
-------
HahaWars is licensed under [Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)](LICENSE).

- You can **use, modify, and share** the project freely.
- **Commercial use is prohibited**.
- Attribution is required when sharing.

========================================
HahaWars
========================================


Сетевая карточная игра с мемами и тёмной эстетикой

---

Описание
--------
HahaWars — это сетевая карточная игра, где игроки получают 5 случайных карт с текстом и выбирают самую смешную карту для текущей ситуации. Побеждает карта с наибольшим количеством голосов. Игра ведёт счёт и показывает финальные результаты.

Проект создан для веселья, обучения сетевому взаимодействию и практики GUI-разработки на Python Tkinter и сетевых протоколов через сокеты.

---

Как это работает
----------------

1. Комнаты
- Игроки могут **создать комнату** или **присоединиться** к существующей.
- Хост создаёт сервер локально и подключается как клиент.
- Все игроки отправляют свои данные (имя и аватар) на сервер.
- Сервер рассылает всем актуальное состояние комнаты: список игроков и их аватарки.

2. Игровой процесс
- Каждому игроку выдаются 5 случайных карточек.
- В каждом раунде игроки выбирают карту, которая, по их мнению, подходит лучше всего под ситуацию.
- После голосования определяется победитель раунда.
- Игра ведёт подсчёт очков и показывает финальные результаты.

3. Интерфейс
- GUI выполнен в тёмной теме с фиолетовыми акцентами.
- Левая панель отображает информацию о комнате и игроках.
- Правая панель — игровая зона.
- Аватарки игроков кодируются в base64 и отображаются рядом с именами.
- Хост видит кнопку **"Начать игру"**, клиенты — нет.

4. Профиль
- Игрок может редактировать своё имя и аватарку.
- Аватарки хранятся в папке `avatars/`.
- Данные пользователя сохраняются в `user_data.json`.

---

Установка и запуск
------------------
1. Клонируйте репозиторий:

    git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
    cd HahaWars

2. Установите зависимости:

    pip install pillow

3. Запустите игру:

    python3 main.py

4. Наслаждайтесь игрой!

---

Структура проекта
-----------------
.
├── avatars/        # Папка с аватарками игроков
├── etc/            # Логотипы и дополнительные изображения
├── modules/        # Клиент, сервер и вспомогательные модули
├── game_logic.py   # Основная игровая логика
├── gui.py          # Интерфейс игры
├── main.py         # Точка входа
├── user_data.json  # Данные текущего пользователя
└── LICENSE         # Лицензия CC BY-NC 4.0

---

Лицензия
--------
HahaWars распространяется под лицензией [Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)](LICENSE).

- Вы можете свободно **использовать, изменять и распространять** проект.
- **Запрещено** использование проекта в коммерческих целях.
- Обязательна **ссылка на автора** при распространении.
